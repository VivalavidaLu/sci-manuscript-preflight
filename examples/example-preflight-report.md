# SCI Manuscript Preflight Report Example

## 1. Executive Verdict

- Overall status: `MAJOR`
- Manuscript type: Biomedical experimental manuscript
- Target journal: Not specified
- Files reviewed: Main manuscript draft, figure legends, representative figure exports, source-data tables
- Missing files: Original raw image files, full statistical scripts
- Study type: Cell and animal experiments
- Coverage limitations: This example does not include pixel-level forensic image analysis. All image-integrity findings require author confirmation against original files.

## 2. Critical Blockers

| ID | Location | Issue | Evidence | Required fix |
|---|---|---|---|---|
| B1 | References 18 and 31 | DOI metadata mismatch | DOI lookup returns different titles and journals from the manuscript reference list. | Verify in PubMed/Crossref/Zotero and replace or correct the references before submission. |

## 3. Major Issues Before Submission

| ID | Location | Issue | Evidence | Recommended fix |
|---|---|---|---|---|
| M1 | Figure 3B and Figure S4A | Possible visual duplication requiring author confirmation | The control microscopy panels look visually similar despite representing different experiments. | Check original images. Replace the panel or add a documented explanation if the same representative image was intentionally reused. |
| M2 | Figure 4C | Statistical inconsistency | Figure legend states one-way ANOVA, Methods states unpaired t test, and source-data table has three groups. | Align Methods, legend, and analysis output. Use the appropriate omnibus and post-hoc workflow if three groups are compared. |
| M3 | Figure 5D | Source-data gap | Bar plot reports mean +/- SEM and significance symbols, but no raw values or sample sizes were provided. | Add source data with raw values, group sizes, statistical test, and exact p values. |

## 4. Minor Polish Issues

| ID | Location | Issue | Suggested fix |
|---|---|---|---|
| m1 | Figure 2 legend | Abbreviations for IF markers are not defined. | Define all markers and stains in the legend. |

## 5. AI Residue / Drafting Artifact Scan

| Severity | File | Line/Page/Section | Finding | Suggested action |
|---|---|---|---|---|
| MINOR | manuscript.docx | Discussion | "plays a pivotal role" repeated several times | Rewrite only if the journal or author wants a less generic style. |

## 6. Reference Authenticity Audit

| Ref ID | Reference | DOI/PMID/arXiv | Status | Evidence | Action |
|---|---|---|---|---|---|
| Ref18 | Example reference A | 10.xxxx/example | Metadata mismatch | DOI resolves to a different title. | Manually verify and correct. |
| Ref31 | Example reference B | PMID unavailable | Needs manual verification | No PMID found in the provided reference export. | Check PubMed, journal page, or Zotero. |

## 7. Claim-to-Citation Audit

| Claim | Location | Citation(s) | Support level | Risk | Recommended fix |
|---|---|---|---|---|---|
| "This is the first study to..." | Introduction | Ref 5, Ref 8 | Indirect support | Novelty overclaim | Soften to "To our knowledge..." or add a direct literature gap citation. |

## 8. Figure/Table/Supplement Consistency

| Item | Expected | Found | Status | Fix |
|---|---|---|---|---|
| Figure S3 | Cited in Results | File not provided | MAJOR | Provide the file or remove the citation. |

## 9. Figure, Data, and Statistical Integrity

| ID | Figure/panel/data item | Integrity risk | Evidence | Severity | Required author check or fix |
|---|---|---|---|---|---|
| F1 | Figure 3B vs Figure S4A | Possible visual duplication | Panels appear visually similar but are labeled as different experiments. | MANUAL | Compare against original raw images before submission. |
| F2 | Figure 4C | Statistical inconsistency | Three groups are plotted, but the legend and Methods name different tests. | MAJOR | Re-run or document the correct statistical test. |
| F3 | Figure 5D | Source-data gap | No raw values, n values, or exact p values were provided. | MAJOR | Add source data and exact test output. |

## 10. Source Data Traceability

| Figure panel | Raw/source file | Quantification table | Statistical test | Caption/results statement | Status |
|---|---|---|---|---|---|
| Figure 3B | Not provided | Not applicable | Not applicable | Representative microscopy image | MANUAL |
| Figure 4C | Provided | Provided | Conflicting: ANOVA vs t test | "Groups differed significantly" | MAJOR |
| Figure 5D | Not provided | Missing | Missing | "Treatment reduced marker expression" | MAJOR |

## 11. Methods-Results-Figure Consistency Matrix

| Experiment | Methods | Results | Figure legend | Supplement/source data | Status |
|---|---|---|---|---|---|
| Dose-response assay | 24 h treatment, three doses | Reports three dose groups | Lists two doses | Source table lists three doses | MAJOR |
| Animal model | n=6 per group | Results states n=5 | Legend states n=6 | Source data missing one animal ID | MANUAL |

## 12. Reporting Guideline and Reproducibility Checklist

| Domain | Item | Status | Comment |
|---|---|---|---|
| Animal study | Randomization and blinding | MANUAL | Mentioned in Methods but not described in enough detail. |
| Bioinformatics | Code availability | MAJOR | No repository or environment information provided. |

## 13. Manual Author Checklist

- [ ] Confirm all highlighted references in Zotero/EndNote/PubMed.
- [ ] Confirm all ethics/consent/data availability statements.
- [ ] Confirm all figure source data and supplementary files.
- [ ] Confirm every representative image maps to the correct raw image.
- [ ] Confirm every quantitative panel maps to source data and the stated statistical test.
- [ ] Confirm all duplicated-looking image regions are either explained or replaced.
- [ ] Confirm all sample sizes, p values, and significance symbols match the source data.
- [ ] Confirm all author contributions and conflicts of interest.
- [ ] Confirm final target-journal formatting requirements.

## 14. Exact Next Actions

1. Verify Figure 3B and Figure S4A against original raw image files.
2. Resolve the Figure 4C statistical-method mismatch and update Methods, legend, and source-data notes.
3. Add source data for Figure 5D, including raw values, n values, exact p values, and the statistical test.
