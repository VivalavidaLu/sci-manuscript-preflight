# SCI Manuscript Preflight Skill

[简体中文](README.zh-CN.md)

A portable agent skill / instruction pack for pre-submission and revision-stage quality control of SCI, biomedical, and bioinformatics manuscripts.

It is modeled after the idea of an arXiv-style preflight check, but adapted for journal manuscripts: AI residue scanning, reference authenticity checks, claim-to-citation review, figure/table consistency, figure/source-data/statistical integrity, reporting-guideline readiness, and submission-risk review.

## What it checks

- AI drafting residue, prompt text, placeholders, Markdown/LaTeX remnants, and unresolved notes.
- Hallucinated, fabricated, unresolved, duplicated, or mismatched references, including DOI/PMID/title/author/year inconsistencies.
- Overstated claims, unsupported claims, and clinical or mechanistic claims that exceed the cited evidence.
- Figure, table, supplementary-material, caption, abbreviation, statistical-annotation, and numbering consistency.
- Figure, source-data, and statistical integrity risks, including duplicated-looking panels, source-data gaps, quantification mismatches, and methods-results-figure contradictions.
- Methods, statistics, ethics, data availability, code availability, reporting-guideline gaps, and target-journal readiness.

## Design Inspiration

Version `v0.2.0` borrows several useful preflight dimensions from [wooly99/geng-academic-fraud-detector](https://github.com/wooly99/geng-academic-fraud-detector), but converts them into non-accusatory submission-quality checks:

| Borrowed dimension | How this skill adapts it |
|---|---|
| Image reuse | Screens for duplicated-looking figure panels, reused controls, crop/flip/rotation risks, and representative-image provenance gaps. |
| Data fabrication checks | Reframed as source-data and quantification traceability: raw values, group sizes, biological vs technical replicates, and consistency between plots and source data. |
| Image splicing/manipulation | Reframed as image assembly-artifact review for Western blots, gels, IF/IHC, microscopy, flow cytometry, and colony images. |
| Statistical anomalies | Reframed as statistical internal-consistency review: `n`, SD/SEM/CI labels, p values, ANOVA/post-hoc logic, test choice, and multiple-testing correction. |
| Output/publication anomalies | Kept only as optional context when relevant; it is not used as a routine submission blocker or author-level judgment. |
| Method contradictions | Converted into a Methods-Results-Figure consistency matrix covering groups, doses, time points, sample sizes, assays, normalization, and statistical tests. |

What was not borrowed: the satirical "spicy commentary" style and misconduct-level verdict language. This skill remains a pre-submission QC workflow. It flags risks that require author verification; it does not accuse authors of misconduct.

## Repository Contents

- `SKILL.md` - main skill instructions
- `scripts/preflight_static_scan.py` - static scan for AI residue, placeholders, Markdown/LaTeX remnants, and high-risk submission wording
- `scripts/reference_audit.py` - DOI/Crossref reference metadata audit
- `references/checklist.md` - manual pre-submission checklist
- `templates/preflight_report.md` - structured preflight report template
- `examples/example-preflight-report.md` - example submission-QC report

## Download

Clone the repository:

```bash
git clone https://github.com/VivalavidaLu/sci-manuscript-preflight.git
cd sci-manuscript-preflight
```

Or download the ZIP from GitHub:

1. Open <https://github.com/VivalavidaLu/sci-manuscript-preflight>
2. Click **Code**
3. Click **Download ZIP**
4. Extract the folder

Keep the full folder. This skill is not only `SKILL.md`; it also depends on `scripts/`, `references/`, `templates/`, and `examples/`.

## Installation

This repository is a portable agent skill. It can be used in Claude Code, Codex, Antigravity, Cursor, GitHub Copilot, Trae, or any agent that can read local instruction files.

### Claude Code

Global install:

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/VivalavidaLu/sci-manuscript-preflight.git ~/.claude/skills/sci-manuscript-preflight
```

Project install:

```bash
mkdir -p .claude/skills
git clone https://github.com/VivalavidaLu/sci-manuscript-preflight.git .claude/skills/sci-manuscript-preflight
```

Then ask Claude Code:

```text
Use the sci-manuscript-preflight skill to check this manuscript folder before submission.
```

### Codex

Global install:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/VivalavidaLu/sci-manuscript-preflight.git ~/.codex/skills/sci-manuscript-preflight
```

Then ask Codex:

```text
Use the sci-manuscript-preflight skill to check this manuscript folder for AI residue, reference problems, claim-citation mismatch, figure/data/statistical integrity issues, and submission risks.
```

### Antigravity

Use this repository as a local instruction/skill folder. Clone it into a stable workspace path and reference `SKILL.md` in the agent instructions.

```bash
git clone https://github.com/VivalavidaLu/sci-manuscript-preflight.git tools/sci-manuscript-preflight
```

Recommended instruction:

```text
When I ask for manuscript preflight, follow tools/sci-manuscript-preflight/SKILL.md and use its scripts, references, templates, and examples when relevant.
```

### Cursor

Clone the repository into a project:

```bash
git clone https://github.com/VivalavidaLu/sci-manuscript-preflight.git .cursor/skills/sci-manuscript-preflight
```

Then add a project rule or instruction:

```text
For manuscript pre-submission checks, follow .cursor/skills/sci-manuscript-preflight/SKILL.md. Treat the whole folder as the skill package.
```

### GitHub Copilot

Clone the repository into a project or shared local tools folder:

```bash
git clone https://github.com/VivalavidaLu/sci-manuscript-preflight.git .github/copilot/skills/sci-manuscript-preflight
```

Then reference it in Copilot instructions:

```text
For SCI/biomedical manuscript preflight tasks, follow .github/copilot/skills/sci-manuscript-preflight/SKILL.md and use the included scripts and templates when applicable.
```

### Trae

Clone the repository into a project:

```bash
git clone https://github.com/VivalavidaLu/sci-manuscript-preflight.git .trae/skills/sci-manuscript-preflight
```

Then add a Trae project rule or agent instruction:

```text
When reviewing a manuscript for submission readiness, follow .trae/skills/sci-manuscript-preflight/SKILL.md and keep the report structured by severity.
```

## Basic Use

Ask your agent:

```text
Use the sci-manuscript-preflight skill to check this manuscript folder for AI residue, hallucinated references, claim-citation mismatch, figure/table numbering issues, figure/data/statistical integrity issues, and SCI submission risks.
```

Recommended inputs:

- Main manuscript: `.docx`, `.pdf`, `.tex`, or `.md`
- Reference file: `.bib`, `.ris`, `.nbib`, `.xml`, `.enl`, or `.txt`
- Figure, source-data, and supplementary-material folders
- Cover letter
- Target journal instructions
- Reviewer checklist or response-to-reviewers draft

If only one file is provided, the agent should perform the feasible partial preflight and explicitly list missing inputs.

## Helper Scripts

Static residue scan:

```bash
python scripts/preflight_static_scan.py path/to/manuscript_folder --out static_scan.tsv
```

DOI/Crossref reference audit:

```bash
python scripts/reference_audit.py path/to/references.bib --out reference_audit.tsv
```

Script outputs are supporting evidence, not final judgment. Database failures, DOI metadata gaps, style-risk signals, image similarity, and statistical anomalies all require manual verification before drawing conclusions.

## Important Notes

This is not an AI detector and not a misconduct-adjudication tool. It is a pre-submission quality-control workflow for detecting high-risk residue, fabricated or mismatched references, unsupported claims, figure/source-data/statistical consistency problems, formatting issues, and compliance gaps before journal submission.

The skill distinguishes verified errors from suspicious items requiring manual confirmation. It should not silently rewrite scientific conclusions, and it should not present hypotheses as validated conclusions.
