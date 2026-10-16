# Round 8 Revised Independent Review

## Reviewer scope

Independent document and workflow validation against the frozen `grading/criteria.json` rubric. The review used only the revised staged requests, inputs, formatted outputs, execution logs, canonical PDFs and page PNGs, bundle manifests, matching bundle directories, and `parent-verification-revised.json`. No candidate source outside the staged bundles, prior reviews or rounds, diagnosis, or intended fix was inspected. Run-log PASS statements were treated as unverified claims and checked independently where the staged evidence allowed.

This review assesses document preservation, OOXML table structure, pagination, rendered appearance, bundle purity, and execution-record completeness. It does not certify scientific correctness, statistical validity, accessibility, journal compliance, or Microsoft Word rendering parity.

## Pages inspected

All canonical output pages were opened and inspected at original image resolution:

- P01: `runs/p01-revised/qa-render/page-1.png` through `page-5.png` (5 pages). Visually observed data ranges were R001–R013, R014–R028, R029–R043, R044–R058, and R059–R072.
- P02: `runs/p02-revised/qa-formatted-v2/page-1.png` through `page-4.png` (4 pages). Visually observed token ranges were TOKEN-001–044, TOKEN-045–096, TOKEN-097–148, and TOKEN-149–180.
- P03: no output pages were expected or inspected because `formatted.docx` is absent by the required safe-stop path.

## Criterion decisions

| ID | Status | Evidence |
| --- | --- | --- |
| R01 | met | Independent DOCX comparison found identical ordered `w:t` sequences (P01: 299 text nodes; P02: 188), identical document-level paragraph text/order, byte-identical canonical XML for all table-external body elements (6 per case), identical `sectPr`, identical table counts/dimensions (P01 74×4; P02 2×2), identical physical-cell counts, and identical merge signatures. P03 has no formatted output and its input SHA-256 remains `e7b80c318e311100a20a3314dc3fd92141ba41a44ba03aad575d15efb96269cb`. |
| R02 | met | P01 renders to 5 Letter pages. PDF extraction independently found the complete header terms on every page and continuous, nonduplicated row IDs: pages 1–5 contain R001–013, R014–028, R029–043, R044–058, and R059–072. Visual inspection confirmed the complete two-row `Record` / `Measurement` / `Estimate` then `Variable` / `Value` / `95% interval` header block on every page. OOXML has `tblHeader` on rows 1 and 2 only. |
| R03 | met | P01 visual inspection shows the full-width top and header-bottom rules on each fragment, the final bottom rule after R072, and no visible vertical borders, internal body grid, diagonal/double rules, or shading. Independent OOXML audit found only 11 non-nil cell rules: three 1 pt top rules on physical row 1, four 0.5 pt bottom rules on header row 2, and four 1 pt bottom rules on row 74; all audited shading is `clear`/`FFFFFF`. |
| R04 | met | All five P01 PNGs were inspected. No clipping, overlap, missing glyphs, blank continuation page, or excessive pagination gap was visible. Pages 2–4 are full continuation pages; page 5 ends normally with R072, the note, and sentinel. The extracted row sequence is complete, and the 73 body rows are normal-height rows kept intact rather than one over-page row. |
| R05 | met | On P01 page 1 the caption is directly above the table start; on page 5 the note and `NORMAL-END-88421` sentinel follow the final rule. On P02 page 1 the caption is directly above the table start; on page 4 the note and `OVERPAGE-END-33017` sentinel follow TOKEN-180 and the final rule. Ownership is visually clear in both outputs. |
| R06 | met | P02 contains one body row with 180 narrative paragraphs. Independent OOXML inspection found `cantSplit` on the one-row header but not on the over-page body row, implementing the justified row-splitting exception documented in the log. All four pages render completely; the sequence ends at TOKEN-180 with the note and sentinel visible. |
| R07 | met | Every canonical P02 PNG was independently inspected at original resolution. Visible ranges are continuous across pages (001–044, 045–096, 097–148, 149–180). Input and output DOCX independently contain exactly 180 unique tokens in exact numeric order, and PDF extraction yields 180 unique tokens, each once, plus one `OVERPAGE-END-33017` sentinel. The execution log limits visual PASS to the four inspected pages. |
| R08 | met | P03 input text explicitly identifies the only 3×2 table as an author-information layout container, with rows for corresponding author, institution, and document role. The log classifies it as outside the data-table scope, specifies a title-page/author-information layout workflow instead, and records a safe stop. Independent filesystem and hash checks confirm `runs/p03-revised/formatted.docx` is absent and the input hash matches the recorded value. |
| R09 | met | For P01, P02, and P03, both `bundles/*-revised/bundle` and `runs/*-revised/bundle` contain exactly the four manifest-listed files: `SKILL.md`, two reference files, and `scripts/word_format_helpers.py`. All file hashes match each manifest; no extras, missing files, cache/log/intermediate files, `checklist.md`, or `F01`/`F20` text were found. |
| R10 | not_met | P01 and P02 record runtimes, concrete commands/exit results, input/output hashes, renderer/page counts, separate structural and page-by-page visual findings, and explicit non-certification boundaries. P03 likewise records versions, input hash, justified output/renderer/page-count N/A states, and separate structure/render sections, but its key read-only DOCX/XML inspection is recorded only as ``"$CODEX_PRIMARY_RUNTIME_PYTHON" -B - <<'PY' ... PY``. Because the executed here-document body is omitted, the log does not record that actual command; the frozen criterion is therefore not fully met. |
| R11 | met | The staged evidence was sufficient to decide every criterion without diagnosis or intended-fix material: raw requests established scope, DOCX/PDF/PNG evidence established preservation and rendering, manifests plus bundle trees established bundle purity, and logs established or failed recordkeeping requirements. The R10 defect is itself directly decidable from the P03 log. |

## Overall status

**not_met** — 10 of 11 criteria are met; R10 is not met because P03 does not record the actual body of its key inspection command.

## Limitations

- Visual findings are specific to the supplied LibreOffice/Poppler canonical renders and do not guarantee identical pagination in every Microsoft Word version.
- The review is limited to document/workflow behavior and the frozen rubric; it does not assess scientific meaning, statistical correctness, accessibility, or journal-specific compliance.
- Bundle purity was verified from the manifest-matched final trees and recorded `-B`/post-run checks; an already-deleted transient file cannot be reconstructed from the staged evidence.
