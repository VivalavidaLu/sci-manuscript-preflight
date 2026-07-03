#!/usr/bin/env python3
"""Run or interpret a deterministic source-table scan for submission preflight.

The wrapper delegates numerical-pattern detection to paperconan and converts
scan.json into a conservative release gate. A clean scan produces only
PASS_CANDIDATE; final clearance still requires reconciliation and sign-off.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


SUPPORTED_SUFFIXES = {
    ".xlsx", ".xls", ".xlsm", ".xlsb", ".csv", ".tsv", ".pdf", ".docx"
}
FINDING_GROUPS = (
    "relations", "progressions", "equal_pairs", "row_pairs", "within_col",
    "identical_after_rounding", "grim",
)
OUTPUT_FIELDS = (
    "kind", "severity", "profile_action", "file", "sheet", "rows",
    "columns", "rule", "n", "evidence_sample", "likely_benign",
    "false_positive_context", "prefilter_reason",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_source_manifest(input_dir: Path) -> list[dict[str, Any]]:
    rows = []
    for path in sorted(input_dir.rglob("*")):
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES:
            rows.append({
                "path": path.relative_to(input_dir).as_posix(),
                "suffix": path.suffix.lower(),
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            })
    return rows


def write_tsv(rows: list[dict[str, Any]], path: Path, fields: tuple[str, ...]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def _compact(value: Any, limit: int = 500) -> str:
    if value in (None, "", [], {}):
        return ""
    text = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return text if len(text) <= limit else text[: limit - 3] + "..."


def _pair(finding: dict[str, Any], key: str) -> str:
    values = [finding.get(f"{key}_a"), finding.get(f"{key}_b")]
    if all(value is None for value in values):
        return str(finding.get(key, ""))
    return " <-> ".join(str(value) for value in values if value is not None)


def normalize_finding(finding: dict[str, Any], common: dict[str, str]) -> dict[str, Any]:
    evidence = finding.get("value_sample") or finding.get("examples")
    if not evidence:
        column_samples = {
            key: finding.get(key) for key in ("col_a_sample", "col_b_sample")
            if finding.get(key) not in (None, "", [], {})
        }
        evidence = column_samples or finding.get("evidence")
    return {
        "kind": str(finding.get("kind", "unknown")),
        "severity": str(finding.get("severity", "unknown")),
        "profile_action": str(finding.get("profile_action", "kept")),
        "file": common["file"],
        "sheet": common["sheet"],
        "rows": common["rows"],
        "columns": str(finding.get("col") or finding.get("column") or common["columns"]),
        "rule": str(finding.get("rule", "")),
        "n": finding.get("n", ""),
        "evidence_sample": _compact(evidence),
        "likely_benign": str(finding.get("likely_benign", "")),
        "false_positive_context": _compact(finding.get("false_positive_context")),
        "prefilter_reason": str(finding.get("prefilter_reason", "")),
    }


def iter_findings(scan: dict[str, Any]) -> Iterable[dict[str, Any]]:
    for relation_block in scan.get("relations_blocks") or []:
        block = relation_block.get("block") or {}
        common = {
            "file": str(relation_block.get("file", "")),
            "sheet": str(relation_block.get("sheet", "")),
            "rows": str(block.get("rows", "")),
            "columns": str(block.get("cols", "")),
        }
        for group in FINDING_GROUPS:
            for finding in relation_block.get(group) or []:
                yield normalize_finding(finding, common)

    for finding in scan.get("cross_sheet_findings") or []:
        common = {
            "file": _pair(finding, "file"),
            "sheet": _pair(finding, "sheet"),
            "rows": str(finding.get("rows", finding.get("block_rows", ""))),
            "columns": str(finding.get("columns", finding.get("block_cols", ""))),
        }
        yield normalize_finding(finding, common)

    for finding in scan.get("digit_distribution") or []:
        if not finding.get("fdr_significant"):
            continue
        normalized = dict(finding)
        normalized.setdefault("kind", "last_digit_chi_square")
        normalized.setdefault("severity", "medium")
        normalized.setdefault("profile_action", "kept")
        normalized.setdefault(
            "rule", "last-digit distribution remains significant after FDR correction"
        )
        common = {
            "file": str(finding.get("file", "")),
            "sheet": str(finding.get("sheet", finding.get("label", ""))),
            "rows": "",
            "columns": str(finding.get("column", "")),
        }
        yield normalize_finding(normalized, common)


def summarize_scan(scan: dict[str, Any]) -> dict[str, Any]:
    findings = list(iter_findings(scan))
    scan_errors = scan.get("scan_errors") or []
    n_files = int(scan.get("n_files") or 0)
    kept_review = [
        finding for finding in findings
        if finding["profile_action"] == "kept"
        and finding["severity"] in {"high", "medium"}
    ]

    if scan_errors or n_files == 0:
        decision = "BLOCKER"
        reason = "One or more expected source-data files were not successfully assessed."
    elif kept_review:
        decision = "REVIEW_REQUIRED"
        reason = "Kept high/medium signals require original-table and context review."
    elif findings:
        decision = "MANUAL_REVIEW"
        reason = "Low/demoted signals remain and their benign explanations need confirmation."
    else:
        decision = "PASS_CANDIDATE"
        reason = "No numerical signal was detected; this is not final submission clearance."

    return {
        "decision": decision,
        "decision_reason": reason,
        "tool": scan.get("tool", "paperconan"),
        "tool_version": scan.get("tool_version", "unknown"),
        "profile": scan.get("profile", "unknown"),
        "scanned_at": scan.get("scanned_at", "unknown"),
        "input_dir": scan.get("input_dir", ""),
        "n_files": n_files,
        "scan_errors": scan_errors,
        "finding_count": len(findings),
        "severity_counts": dict(Counter(item["severity"] for item in findings)),
        "profile_action_counts": dict(Counter(item["profile_action"] for item in findings)),
        "findings": findings,
        "final_pass_requires": [
            "source-to-figure/table/results reconciliation",
            "independent statistical recomputation where feasible",
            "adversarial review of unresolved high-impact findings",
            "named author sign-off",
        ],
    }


def write_gate_report(summary: dict[str, Any], path: Path) -> None:
    lines = [
        "# Table and Source-Data Integrity Gate",
        "",
        f"- Gate decision: `{summary['decision']}`",
        f"- Reason: {summary['decision_reason']}",
        f"- Scanner: `{summary['tool']} {summary['tool_version']}`",
        f"- Profile: `{summary['profile']}`",
        f"- Files assessed: {summary['n_files']}",
        f"- Findings: {summary['finding_count']}",
        f"- Scan errors: {len(summary['scan_errors'])}",
        "",
        "> Numerical anomaly scanning is a signal layer, not proof of correctness or misconduct.",
        "> `PASS_CANDIDATE` never equals final submission clearance.",
        "",
    ]
    if summary["scan_errors"]:
        lines.extend(["## Scan failures", ""])
        for error in summary["scan_errors"]:
            lines.append(
                f"- `{error.get('file', 'unknown')}`: {error.get('error', 'unknown error')}"
            )
        lines.append("")
    lines.extend(["## Required completion steps", ""])
    lines.extend(f"- [ ] {item}" for item in summary["final_pass_requires"])
    lines.extend([
        "",
        "See `findings.tsv` for file, sheet, row/column, rule, and evidence detail.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_paperconan(input_dir: Path, scanner_out: Path, profile: str) -> Path:
    executable = shutil.which("paperconan")
    if executable is None:
        raise RuntimeError(
            'paperconan is not installed. Install it in an isolated environment with '
            '`python -m pip install "paperconan[all]"`, then rerun. Do not mark the gate as passed.'
        )
    scanner_out.mkdir(parents=True, exist_ok=True)
    command = [executable, str(input_dir), "--out", str(scanner_out), "--profile", profile]
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        message = (result.stderr or result.stdout).strip()
        raise RuntimeError(f"paperconan failed with exit code {result.returncode}: {message}")
    scan_json = scanner_out / "scan.json"
    if not scan_json.exists():
        raise RuntimeError("paperconan completed without producing scan.json")
    return scan_json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input-dir", type=Path)
    source.add_argument("--scan-json", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument(
        "--profile", choices=("review", "forensic", "triage"), default="review"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    try:
        if args.input_dir:
            if not args.input_dir.is_dir():
                raise RuntimeError(f"Input directory does not exist: {args.input_dir}")
            manifest = build_source_manifest(args.input_dir)
            write_tsv(
                manifest, args.out / "source_manifest.tsv",
                ("path", "suffix", "size_bytes", "sha256"),
            )
            if not manifest:
                raise RuntimeError("No supported source-data files were found; the gate cannot pass.")
            scan_json = run_paperconan(
                args.input_dir, args.out / "paperconan", args.profile
            )
        else:
            scan_json = args.scan_json

        scan = json.loads(scan_json.read_text(encoding="utf-8"))
        summary = summarize_scan(scan)
        (args.out / "gate.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        write_tsv(summary["findings"], args.out / "findings.tsv", OUTPUT_FIELDS)
        write_gate_report(summary, args.out / "gate_report.md")
        print(f"Gate decision: {summary['decision']}")
        return 0
    except (OSError, ValueError, json.JSONDecodeError, RuntimeError) as error:
        print(f"TABLE GATE ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
