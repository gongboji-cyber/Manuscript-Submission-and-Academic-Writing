# Round 8 Independent Final Evidence Review

## Reviewer scope

This was a blind, evidence-only review against `grading/criteria.json`. I inspected only the permitted Round 8 requests, inputs, outputs, execution logs, bundle manifests, matching run-bundle trees, `parent-verification-final.json`, canonical PDFs, and canonical page PNGs. I did not inspect candidate source, prior review files, prior rounds, any diagnosis, or the intended fix. Run-log PASS statements were treated as claims and independently checked where the supplied artifacts allowed it.

The review uses the stated evidence composition: P01 and P02 are regression runs whose document algorithms and already-complete command logs were unchanged by the final command-recording clarification; P03 is a fresh run with the final bundle.

## Pages inspected

Every canonical page was opened at original image detail:

- P01: `runs/p01-revised/qa-render/page-1.png` through `page-5.png` (5 pages).
- P02: `runs/p02-revised/qa-formatted-v2/page-1.png` through `page-4.png` (4 pages).

## Criterion findings

| Criterion | Status | Evidence |
|---|---|---|
| R01 | met | Independent DOCX checks found identical ordered paragraph text, identical table text, one table in each input/output, unchanged dimensions (P01 74×4; P02 2×2), byte-identical parsed table-external paragraph XML, and identical section XML. The recorded P01 merge signature is unchanged. Actual hashes match the logs and parent verification: P01 input `d908…9ab1`, output `99e0…0102`; P02 input `1e61…fc8b`, output `c9ec…f9f71`. |
| R02 | met | P01 renders to 5 pages. Visual inspection shows the complete two-row header (`Record`; `Measurement`/`Variable`; `Estimate`/`Value`/`95% interval`) on every page. Independent PDF extraction finds exactly 72 unique row IDs in order: pages 1–5 contain R001–R013, R014–R028, R029–R043, R044–R058, and R059–R072, with no duplication or omission. XML flags only rows 1–2 as repeating headers. |
| R03 | met | On all five P01 pages the table has the intended top and header-bottom rules; page 5 has the final bottom rule. No vertical borders, body grid, diagonal rules, double rules, or decorative table shading are visible. Independent XML inspection finds 1 pt top rules, 0.5 pt row-2 bottom rules, 1 pt final-row bottom rules, all vertical/internal/diagonal borders `nil`, and white cell fill. Continuation-fragment boundary strokes are renderer pagination behavior, not XML body-grid rules. |
| R04 | met | All five P01 pages were visually inspected. They contain no clipping, overlap, missing glyphs, blank continuation page, or excessive row-keep gap. Rows remain readable and sequential, and the page-4 source PNG is complete. |
| R05 | met | P01 page 1 keeps `Table 1. Synthetic repeated-measures summary` with the table start. Page 5 places the note immediately below the final table rule, followed by `Sentinel after table: NORMAL-END-88421`; ownership is clear. Independent PDF extraction confirms the caption only on page 1 and the note/sentinel on page 5. |
| R06 | met | P02 documents that its single body row exceeds one page and explicitly applies the row-splitting exception. Independent XML inspection confirms the header row is repeating and unsplittable while the body row has no `cantSplit`. All four pages render completely; TOKEN-001 through TOKEN-180, the final rule, note, and `OVERPAGE-END-33017` sentinel are present. |
| R07 | met | The P02 log limits visual PASS to the four inspected pages and states each final PNG was opened at original resolution. I independently inspected all four canonical pages. PDF extraction finds 180 token occurrences, 180 unique token numbers in exact order, with page ranges 001–044, 045–096, 097–148, and 149–180; the sentinel occurs once. |
| R08 | met | P03 input text explicitly calls the first table an author-information layout container rather than a scientific data table, and its final row states `Document role | Title-page layout only`. The log classifies it as not applicable, identifies the needed Word title-page/layout-table workflow, and makes no visual-PASS claim. `runs/p03-final/formatted.docx` is absent, the input hash matches the expected `e7b8…69cb`, and all recorded commands are read-only checks. |
| R09 | met | For P01, P02, and P03, independent enumeration of each `runs/*/bundle` finds exactly the four manifest-listed files, and every file hash matches its corresponding manifest. No `checklist.md`, `__pycache__`, cache/log/intermediate file, or standalone F01/F20 semantic token is present in any bundle. |
| R10 | met | P01 and P02 logs record runtime/tool versions, exact shell command blocks, input/output SHA-256 values, renderer, final page count, structural findings, and page-specific visual findings. P03’s fresh final-bundle log records its runtime and every actual command in full, the input hash, no-output reason, and renderer/page-count/visual findings as not applicable because of the safety stop. All logs expressly disclaim scientific, journal, or full-document certification. |
| R11 | met | All R01–R10 decisions were possible from the permitted raw requests, logs, DOCX/PDF outputs, manifests, independent structural/hash checks, and the nine canonical page images, without inspecting diagnosis or intended-fix material. |

## Overall status

**PASS — all eleven criteria are met.**

## Limitations

- This is an evidence review, not a re-execution of the historical P01/P02 authoring commands. Their command provenance comes from the supplied logs; current hashes, package structure, bundle state, PDF extraction, and page rendering were checked independently.
- P01 and P02 are regression evidence produced before the final command-recording clarification; the task statement says their document algorithms and already-complete logs were unchanged. P03 is the fresh execution evidence for the final bundle wording.
- Visual conclusions apply to the supplied canonical LibreOffice/Poppler renders, not to every possible Word renderer.
- P03 has no output render by design; its criterion is the documented, hash-supported safety stop and absence of `formatted.docx`.
