# Source Code Supplement — SCI Submission Template

> Purpose: provide editors, reviewers and readers with a compact, auditable, English-language code appendix for manuscript submission. This format borrows the traceability and continuous-code presentation of source-program identification materials, but it is **not** a software-copyright deposit and must not inherit copyright-registration pagination rules.

## 1. Cover Information

**Manuscript title:** [Title]  
**Short title:** [Short title]  
**Code supplement title:** Source Code Supplement  
**Authors:** [Authors or anonymized designation, according to journal policy]  
**Repository / archive:** [URL or private archive identifier]  
**Version:** [Release/tag]  
**Git commit / archive SHA256:** [Identifier]  
**Date frozen:** [YYYY-MM-DD]  
**Primary language(s):** [Python/R/Julia/Matlab/etc.]  
**License:** [License or “Not specified / private for peer review”]

### Scope statement
This supplement contains the author-written code required to reproduce the analyses and manuscript outputs listed below. Third-party libraries, pretrained model source code, vendor code and unrelated development utilities are excluded unless modification of those components is itself part of the scientific contribution.

## 2. Reproducibility Map

| Manuscript item | Scientific purpose | Code file / module | Entry point | Expected output |
|---|---|---|---|---|
| Fig. 1 | [Purpose] | [path] | [command/function] | [file/result] |
| Table 1 | [Purpose] | [path] | [command/function] | [file/result] |
| Primary endpoint | [Purpose] | [path] | [command/function] | [metric/result] |

Do not claim a mapping unless it has been verified against the frozen manuscript version.

## 3. Environment and Dependencies

**Operating system:** [OS and version]  
**Runtime:** [Python/R/etc. version]  
**Hardware used where relevant:** [CPU/GPU/RAM]  
**Random seed(s):** [Only if actually fixed]  
**Dependency lockfile:** [requirements.txt / environment.yml / renv.lock / etc.]  
**Container:** [Docker/Singularity image and digest, if used]

### Minimal installation
```text
[Exact verified installation command(s)]
```

### Minimal reproduction command
```text
[Exact verified command(s)]
```

State explicitly when full reproduction requires restricted data, licensed software, unavailable hardware or non-public model weights.

## 4. Input and Output Contract

### Inputs
For each required input, report:
- file or dataset name;
- provenance / DOI / accession;
- expected format;
- required columns, fields or directory structure;
- preprocessing assumptions;
- whether the data are public, restricted or synthetic.

### Outputs
For each principal output, report:
- output file name/path;
- manuscript destination (figure/table/result);
- expected schema or metric;
- whether the file is an intermediate or final analysis product.

## 5. Code Inventory

| Order | File | Role | Original / adapted | Included lines | SHA256 |
|---:|---|---|---|---|---|
| 1 | [path] | [role] | Original | [range/all] | [hash] |

### Inclusion rule
Prefer code that is necessary to reproduce the paper's scientific claims. Exclude caches, virtual environments, binaries, raw data, secrets, patient identifiers, generated figures, large third-party packages and irrelevant experimental branches.

## 6. Source Code Listing

### File 1 — `[path/to/file.py]`

**Scientific role:** [One sentence]  
**Called by:** [entry point / pipeline stage]  
**Produces:** [outputs]  
**Source status:** [original / adapted with attribution]

```python
0001  [original code line]
0002  [original code line]
0003  [original code line]
```

Rules:
- retain original executable semantics and file order;
- use continuous visible line numbers for auditability;
- do not fabricate omitted code;
- mark deliberate omissions with a neutral note outside the code block;
- do not alter calculations merely to improve appearance;
- preserve meaningful comments, function names and parameters;
- redact secrets, credentials, patient identifiers and private endpoints, and document the redaction;
- when adapting third-party code, identify the source and license.

Repeat this section for each included file.

## 7. Verification Record

Report only checks actually performed.

| Check | Status | Evidence |
|---|---|---|
| Frozen commit/archive matches listed files | PASS/PARTIAL/FAIL | [evidence] |
| Entry point executes | PASS/PARTIAL/FAIL | [evidence] |
| Main manuscript outputs regenerated | PASS/PARTIAL/FAIL | [evidence] |
| Figure/table mapping verified | PASS/PARTIAL/FAIL | [evidence] |
| Dependencies resolved from documented environment | PASS/PARTIAL/FAIL | [evidence] |
| No secrets / direct identifiers included | PASS/PARTIAL/FAIL | [evidence] |

Do not label the package “fully reproducible” unless the end-to-end workflow was independently rerun from the documented inputs and environment.

## 8. Known Limitations

Document any:
- unavailable raw data;
- platform-specific dependency;
- stochastic variation;
- nondeterministic GPU operation;
- proprietary dependency;
- model-weight restriction;
- preprocessing step not captured by code;
- manual intervention;
- excluded third-party component.

## 9. Suggested SCI Rendering Defaults

Use journal instructions when available. Otherwise:
- English throughout;
- A4 or US Letter according to journal submission system;
- 9–10 pt monospaced code font;
- 11–12 pt body text;
- continuous page numbering;
- file path in section heading or running header;
- visible line numbers;
- no syntax highlighting required;
- avoid wrapping code where possible; when wrapping is unavoidable, do not count visual wraps as new source lines;
- export to editable DOCX plus PDF when the submission system accepts both;
- ensure anonymization follows the journal's review model.

## 10. Relationship to Other Supplementary Files

This document is a code appendix, not a substitute for:
- Supplementary Methods;
- data dictionary;
- statistical analysis plan;
- model card;
- repository README;
- environment lockfile;
- full executable repository.

When the journal permits repository links or ZIP code submission, this PDF/DOCX should function as a human-readable audit layer and navigation map rather than the only copy of the software.
