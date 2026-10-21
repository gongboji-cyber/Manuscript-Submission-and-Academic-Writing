# Round 8 Independent Review

## Scope and method

This review used only the authorized round 8 criteria, parent verification, three run directories, and three bundle manifests. Executor statements in `execution-log.md` were treated as claims until corroborated by raw DOCX package inspection, structural JSON, manifest/hash checks, PDF text extraction, or direct page-image inspection.

I directly inspected all canonical rendered pages:

- p01 normal case: `render-qa/page-1.png` through `render-qa/page-5.png`
- p02 over-page case: `qa-render/page-1.png` through `qa-render/page-8.png`

No canonical output render exists for p03 because the run stopped before authoring, as required for the layout-table case.

## Result

| Criterion | Status | Independent basis | Executor claim treatment and limitations |
| --- | --- | --- | --- |
| R01 | met | Independent DOCX comparison found unchanged XML text-token sequences in every XML part, unchanged body block order, byte-equivalent canonical table-external body XML, unchanged section XML, and identical target-table dimensions, cell text, grid widths, and merge signatures for p01 and p02. p03 produced no output. | The logs' preservation PASS claims were corroborated by the raw input/output DOCX packages and by `p02-current/qa-structural.json`. Formatting-only XML changes remain in the target tables, as expected. |
| R02 | met | p01 has five canonical pages. All five visibly contain the complete two-row header (`Record`; `Measurement`/`Variable`; `Estimate`/`Value`/`95% interval`). PDF extraction gives contiguous, unique row ranges R001-R013, R014-R028, R029-R043, R044-R058, and R059-R072. | The executor's five-page/header/data-continuity claim was corroborated from every page image and PDF text extraction. |
| R03 | met | Raw OOXML has active cell rules only at the first physical row top (1 pt), second header row bottom (0.5 pt), and final data row bottom (1 pt); table-level borders have no active rule. Every p01 page shows no vertical border, body grid, diagonal/double rule, or decorative shading. | Continuation-page boundary rules are renderer pagination behavior permitted by the bundle reference; they are not manually inserted body grid rules. Fine rule thickness was determined structurally as well as visually. |
| R04 | met | Direct inspection of all five p01 pages found no clipping, overlap, missing glyph, blank continuation page, or excessive row-keep gap. The table flows continuously across pages. | The executor's per-page findings were independently confirmed. Page 4 was reviewed from the canonical page and its supplied full-resolution crops. |
| R05 | met | On p01 page 1, the caption remains immediately with the table start. On page 5, the note remains immediately after the final rule/row, followed by the sentinel paragraph. Body block order is unchanged in the DOCX. | The visual and structural evidence corroborates the log. |
| R06 | met | p02 contains a two-row table whose single body row is taller than a page. OOXML shows the header row retains `tblHeader` and `cantSplit`, while the body row has no `cantSplit`. All 180 source tokens and the final sentinel are preserved, visible, and extractable across eight pages. | The log explicitly justifies the row-splitting exception. Its content-preservation claim was corroborated by DOCX token comparison, page inspection, and PDF extraction. |
| R07 | met | All eight p02 canonical page PNGs were independently inspected. Extracted page ranges are TOKEN-001-022, 023-048, 049-074, 075-100, 101-126, 127-152, 153-178, and 179-180; the global sequence is exact, unique, and complete. | The executor recorded page-specific visual findings and did not rely only on structural checks. Direct inspection and extraction corroborate the PASS claim. |
| R08 | met | p03 input contains a 3 x 2 author-information table with rows `Corresponding author`, `Institution`, and `Document role: Title-page layout only`; the surrounding paragraph also calls it an author-information layout container. The bundle excludes layout tables. Actual input SHA-256 equals the expected verification hash, `formatted.docx` is absent, and no render directory exists. | The executor's not-applicable classification and safe stop are directly supported by the input and bundle scope. The log states the exact alternate workflow needed. |
| R09 | met | Each run bundle contains exactly the four manifest-listed files with matching byte sizes and SHA-256 values. No `checklist.md`, F01/F20 text, cache, log, or intermediate file is present inside any bundle. Parent verification independently reports the same file-set/hash result. | This is a post-execution filesystem determination. It cannot prove that a transient file was created and later deleted, but the exact final manifest match, `python -B` commands, and absence of cache/log/intermediate residue are sufficient evidence for the criterion. |
| R10 | not_met | p01 and p02 logs record runtime versions, exact commands, hashes, renderer, page counts, structural findings, per-page visual findings, and limited-scope disclaimers. The p03 safe-stop log records the input hash and correctly marks output/render fields not applicable, but it provides only a narrative action list rather than exact commands and does not record runtime versions. | I applied R10 to all three execution records. If R10 were intended to apply only to completed authoring/render runs, p01 and p02 would meet it; that narrower scope is not stated in the criterion. No log claims scientific or journal certification. |
| R11 | met | Every criterion was decidable from the authorized raw requests, logs, DOCX outputs, manifests, structural checks, parent verification, PDF extraction, and page images. No diagnosis or intended fix was supplied to this reviewer. | The p03/R10 scope issue was resolved by applying the literal all-run reading and documenting it rather than importing an unstated intended result. |

## Evidence paths

### Core grading inputs

- `/workspace/scratch/46b39df32326/skill-optimization-20261011/round8/grading/criteria.json`
- `/workspace/scratch/46b39df32326/skill-optimization-20261011/round8/parent-verification.json`
- `/workspace/scratch/46b39df32326/skill-optimization-20261011/round8/bundles/p01-current/bundle-manifest.json`
- `/workspace/scratch/46b39df32326/skill-optimization-20261011/round8/bundles/p02-current/bundle-manifest.json`
- `/workspace/scratch/46b39df32326/skill-optimization-20261011/round8/bundles/p03-current/bundle-manifest.json`

### p01 normal case

- `/workspace/scratch/46b39df32326/skill-optimization-20261011/round8/runs/p01-current/request.md`
- `/workspace/scratch/46b39df32326/skill-optimization-20261011/round8/runs/p01-current/execution-log.md`
- `/workspace/scratch/46b39df32326/skill-optimization-20261011/round8/runs/p01-current/input.docx`
- `/workspace/scratch/46b39df32326/skill-optimization-20261011/round8/runs/p01-current/formatted.docx`
- `/workspace/scratch/46b39df32326/skill-optimization-20261011/round8/runs/p01-current/render-qa/formatted.pdf`
- `/workspace/scratch/46b39df32326/skill-optimization-20261011/round8/runs/p01-current/render-qa/page-1.png` through `page-5.png`

### p02 over-page case

- `/workspace/scratch/46b39df32326/skill-optimization-20261011/round8/runs/p02-current/request.md`
- `/workspace/scratch/46b39df32326/skill-optimization-20261011/round8/runs/p02-current/execution-log.md`
- `/workspace/scratch/46b39df32326/skill-optimization-20261011/round8/runs/p02-current/input.docx`
- `/workspace/scratch/46b39df32326/skill-optimization-20261011/round8/runs/p02-current/formatted.docx`
- `/workspace/scratch/46b39df32326/skill-optimization-20261011/round8/runs/p02-current/qa-structural.json`
- `/workspace/scratch/46b39df32326/skill-optimization-20261011/round8/runs/p02-current/qa-render/formatted.pdf`
- `/workspace/scratch/46b39df32326/skill-optimization-20261011/round8/runs/p02-current/qa-render/page-1.png` through `page-8.png`

### p03 layout-table safe stop

- `/workspace/scratch/46b39df32326/skill-optimization-20261011/round8/runs/p03-current/request.md`
- `/workspace/scratch/46b39df32326/skill-optimization-20261011/round8/runs/p03-current/execution-log.md`
- `/workspace/scratch/46b39df32326/skill-optimization-20261011/round8/runs/p03-current/input.docx`

## Summary

- Met: R01-R09 and R11
- Not met: R10
- Unclear: none
