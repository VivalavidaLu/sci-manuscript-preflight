# SCI Manuscript Preflight Skill

[简体中文](README.zh-CN.md)

A portable agent skill / instruction pack for pre-submission checks of SCI, biomedical, and bioinformatics manuscripts.

It is modeled after the idea of an arXiv-style preflight check, but adapted for journal manuscripts: AI residue scanning, reference authenticity checks, claim-to-citation review, figure/table consistency, and reporting-guideline readiness.

This repository can be used in Claude Code, Codex, Antigravity, Cursor, GitHub Copilot, TRAE, or any coding/research agent that can read project instructions and run helper scripts.

## What it checks

- AI residue and drafting artifacts, such as prompt text, placeholders, Markdown remnants, LaTeX remnants, and unresolved notes.
- Hallucinated, fabricated, duplicated, or mismatched references.
- DOI/Crossref metadata consistency.
- High-risk claim-to-citation support.
- Figure, table, and supplementary-material numbering consistency.
- Figure, source-data, and statistical integrity risks, including duplicated-looking panels, source-data gaps, quantification mismatches, and methods-results-figure contradictions.
- Biomedical reporting readiness, including ethics, consent, data availability, code availability, and study-type checklists.
- Bioinformatics and single-cell reproducibility details, such as data accession, software versions, QC thresholds, normalization, batch correction, clustering, annotation, DEG settings, and multiple-testing correction.

## Repository layout

```text
sci-manuscript-preflight/
|-- SKILL.md
|-- README.md
|-- README.zh-CN.md
|-- scripts/
|   |-- preflight_static_scan.py
|   `-- reference_audit.py
|-- references/
|   `-- checklist.md
|-- examples/
|   `-- example-preflight-report.md
`-- templates/
    `-- preflight_report.md
```

## Download and installation

You can install this repository either by downloading the ZIP file from GitHub or by cloning it with Git.

### Method 1: Download ZIP

1. Open the repository page:

   ```text
   https://github.com/VivalavidaLu/sci-manuscript-preflight
   ```

2. Click the green **Code** button.
3. Click **Download ZIP**.
4. Extract the downloaded ZIP file.
5. Rename the extracted folder to:

   ```text
   sci-manuscript-preflight
   ```

6. Put the folder somewhere your agent can read, such as a project folder, a skills folder, or a rules/instructions folder.

### Method 2: Install with Git

```bash
git clone https://github.com/VivalavidaLu/sci-manuscript-preflight.git
```

You can also clone it directly into the configuration folder used by your agent or IDE.

## Use in different agents and IDEs

Different tools use different names for the same basic idea: skills, rules, instructions, memories, prompts, project guidelines, or agent context. This repository is designed to work as a portable instruction pack.

### Claude Code

If your Claude Code setup supports skills, install the folder as a skill.

#### Windows PowerShell

```powershell
New-Item -ItemType Directory -Force "$HOME\.config\claude-code\skills"
git clone https://github.com/VivalavidaLu/sci-manuscript-preflight.git "$HOME\.config\claude-code\skills\sci-manuscript-preflight"
```

#### macOS / Linux

```bash
mkdir -p ~/.config/claude-code/skills
git clone https://github.com/VivalavidaLu/sci-manuscript-preflight.git ~/.config/claude-code/skills/sci-manuscript-preflight
```

After installation, restart Claude Code or reload the agent environment.

The expected layout is:

```text
skills/
└── sci-manuscript-preflight/
    ├── SKILL.md
    ├── README.md
    ├── README.zh-CN.md
    ├── scripts/
    ├── references/
    └── templates/
```

The most important check is that `SKILL.md` is directly inside the `sci-manuscript-preflight` folder.

Correct:

```text
skills/sci-manuscript-preflight/SKILL.md
```

Wrong:

```text
skills/sci-manuscript-preflight/sci-manuscript-preflight/SKILL.md
```

### OpenAI Codex

Codex may not use Claude-style `SKILL.md` natively. Use this repository as a project instruction pack.

Recommended options:

1. Clone this repository into your manuscript or analysis project.
2. Tell Codex:

   ```text
   Read sci-manuscript-preflight/SKILL.md and follow it as the pre-submission manuscript checking workflow.
   ```

3. If your Codex environment uses `AGENTS.md`, copy or summarize the contents of `SKILL.md` into your project-level `AGENTS.md`, or add a short rule such as:

   ```text
   For manuscript preflight checks, follow the workflow in sci-manuscript-preflight/SKILL.md. Use scripts/preflight_static_scan.py and scripts/reference_audit.py when useful.
   ```

### Antigravity

Use this repository as project context or an instruction/rules folder.

Recommended prompt:

```text
Use the workflow in sci-manuscript-preflight/SKILL.md as a manuscript preflight skill. Check AI residue, hallucinated references, claim-citation mismatch, figure/table consistency, and journal-submission risks.
```

You can also place the repository inside the project so Antigravity can read `SKILL.md`, `templates/preflight_report.md`, and the helper scripts.

### Cursor

Cursor can use this as project rules/context.

Recommended options:

1. Clone this repository into your manuscript project.
2. Add a Cursor rule that says:

   ```text
   When reviewing manuscripts, follow sci-manuscript-preflight/SKILL.md. Use the report template in templates/preflight_report.md. Run helper scripts when appropriate.
   ```

3. Ask Cursor Chat or Agent:

   ```text
   Follow sci-manuscript-preflight/SKILL.md and run a pre-submission check on this manuscript.
   ```

### GitHub Copilot

GitHub Copilot does not use Claude-style skills directly. Use this repository as repository instructions or project context.

Recommended options:

1. Keep this repository inside the manuscript project, or copy `SKILL.md` into your repository instructions.
2. Ask Copilot Chat:

   ```text
   Read SKILL.md and apply this workflow to check the manuscript for AI residue, reference problems, unsupported claims, and submission-readiness issues.
   ```

3. Run the helper scripts manually in the terminal when needed.

### TRAE / TRAE CN

Use this repository as rules or project context.

Recommended prompt:

```text
Read sci-manuscript-preflight/SKILL.md and use it as the manuscript preflight workflow. Produce the final report using templates/preflight_report.md.
```

If TRAE supports project rules, add a rule pointing to `SKILL.md`. If not, paste the relevant parts of `SKILL.md` into the chat before asking it to review the manuscript.

## Basic use

Ask your agent:

```text
Use the sci-manuscript-preflight workflow to check this manuscript folder for AI residue, hallucinated references, claim-citation mismatch, figure/table numbering issues, and SCI submission risks.
```

Or:

```text
Read SKILL.md and run sci-manuscript-preflight on this manuscript before journal submission.
```

## Helper scripts

The repository includes two optional helper scripts.

### Static manuscript scan

```bash
python scripts/preflight_static_scan.py path/to/manuscript_folder --out static_scan.tsv
```

This scans for AI residue, placeholders, Markdown/LaTeX remnants, editorial notes, and high-risk wording.

For `.docx` support, install:

```bash
pip install python-docx
```

For `.pdf` support, install:

```bash
pip install pymupdf
```

### DOI/Crossref reference audit

```bash
python scripts/reference_audit.py path/to/references.bib --out reference_audit.tsv
```

This extracts DOI-like strings and checks whether they resolve through Crossref. It can flag unresolved or duplicated DOI records, but it does not replace manual author verification.

## Recommended input files

For a full preflight, provide:

- Main manuscript file: `.docx`, `.pdf`, `.tex`, or `.md`
- Reference file: `.bib`, `.ris`, `.nbib`, `.xml`, or exported plain text
- Figure files
- Tables
- Supplementary files
- Target journal instructions, if available
- Reporting checklist, if applicable

## Important limitations

This is not an AI detector and should not be used to accuse authors of AI use. It is a pre-submission quality-control workflow designed to catch risky artifacts, fabricated or mismatched references, unsupported claims, and formatting/compliance issues before journal submission.

Reference checks are probabilistic and database-dependent. A reference should not be called fabricated solely because one database lookup fails. Always manually verify flagged references in PubMed, Crossref, DOI resolver, the journal website, Zotero, EndNote, or another trusted source.

## License

No license has been specified yet. Add a license before broad reuse or redistribution.
