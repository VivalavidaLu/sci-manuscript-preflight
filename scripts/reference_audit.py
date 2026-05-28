#!/usr/bin/env python3
"""Reference authenticity audit using DOI and Crossref metadata.

This script extracts DOI-like strings from a reference file and checks whether
Crossref can resolve them. It also flags duplicate DOI records.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Dict, List

DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)


def clean_doi(doi: str) -> str:
    return doi.strip().rstrip(".,;:)]}")


def extract_dois(text: str) -> List[str]:
    return [clean_doi(m.group(0)) for m in DOI_RE.finditer(text)]


def crossref_lookup(doi: str, timeout: int = 15) -> Dict:
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    req = urllib.request.Request(url, headers={"User-Agent": "sci-manuscript-preflight/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status != 200:
                return {"ok": False, "status": resp.status, "error": f"HTTP {resp.status}"}
            data = json.loads(resp.read().decode("utf-8"))
        msg = data.get("message", {})
        date_source = msg.get("published-print") or msg.get("published-online") or msg.get("issued") or {}
        date_parts = date_source.get("date-parts") or [[""]]
        return {
            "ok": True,
            "status": 200,
            "title": " ".join(msg.get("title", [])[:1]),
            "container_title": " ".join(msg.get("container-title", [])[:1]),
            "year": date_parts[0][0],
            "type": msg.get("type", ""),
            "publisher": msg.get("publisher", ""),
        }
    except Exception as exc:
        return {"ok": False, "status": "", "error": str(exc)}


def chunk_reference_context(text: str, doi: str) -> str:
    idx = text.lower().find(doi.lower())
    if idx < 0:
        return ""
    start = max(0, idx - 300)
    end = min(len(text), idx + 300)
    return " ".join(text[start:end].split())


def status_for(result: Dict, duplicate: bool) -> str:
    if duplicate:
        return "duplicate"
    if result.get("ok"):
        return "verified"
    return "unresolved"


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit DOI references via Crossref")
    parser.add_argument("reference_file", help="Reference file, such as .bib, .ris, .txt")
    parser.add_argument("--out", default="reference_audit.tsv", help="Output TSV file")
    args = parser.parse_args()

    path = Path(args.reference_file)
    text = path.read_text(encoding="utf-8", errors="replace")
    dois = extract_dois(text)
    counts = Counter(d.lower() for d in dois)

    rows = []
    seen = set()
    for doi in dois:
        key = doi.lower()
        duplicate = counts[key] > 1 and key in seen
        result = {"ok": True} if duplicate else crossref_lookup(doi)
        seen.add(key)
        rows.append({
            "doi": doi,
            "status": status_for(result, duplicate),
            "crossref_title": result.get("title", ""),
            "crossref_journal": result.get("container_title", ""),
            "crossref_year": result.get("year", ""),
            "type": result.get("type", ""),
            "publisher": result.get("publisher", ""),
            "error": result.get("error", ""),
            "context": chunk_reference_context(text, doi)[:500],
        })

    with open(args.out, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["doi", "status", "crossref_title", "crossref_journal", "crossref_year", "type", "publisher", "error", "context"], delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)

    unresolved = sum(1 for r in rows if r["status"] == "unresolved")
    print(f"Audited {len(rows)} DOI records; unresolved={unresolved}; wrote {args.out}")
    return 1 if unresolved else 0


if __name__ == "__main__":
    sys.exit(main())
