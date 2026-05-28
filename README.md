# SCI Manuscript Preflight Skill

A Claude/agent skill for pre-submission checks of SCI, biomedical, and bioinformatics manuscripts.

It is modeled after the idea of an arXiv-style preflight check, but adapted for journal manuscripts: AI residue scanning, reference authenticity checks, claim-to-citation review, figure/table consistency, and reporting-guideline readiness.

## Contents

- `SKILL.md` — main skill instructions
- `scripts/preflight_static_scan.py` — static scan for AI residue, placeholders, Markdown/LaTeX remnants, and manuscript-risk phrases
- `scripts/reference_audit.py` — DOI/Crossref metadata audit for references
- `references/checklist.md` — manual pre-submission checklist
- `templates/preflight_report.md` — structured report template

## Basic use

Ask your agent:

```text
Use the sci-manuscript-preflight skill to check this manuscript folder for AI residue, hallucinated references, claim-citation mismatch, figure/table numbering issues, and SCI submission risks.
```

Run the helper scripts directly:

```bash
python scripts/preflight_static_scan.py path/to/manuscript_folder --out static_scan.tsv
python scripts/reference_audit.py path/to/references.bib --out reference_audit.tsv
```

## Notes

This is not an AI detector and should not be used to accuse authors of AI use. It is a pre-submission quality-control workflow designed to catch risky artifacts, fabricated or mismatched references, unsupported claims, and formatting/compliance issues before journal submission.
