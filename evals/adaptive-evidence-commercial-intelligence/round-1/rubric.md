# Round 1 rubric and execution controls

This file was kept separate from the raw cases and was not shown to the two producing runs.

## Completion criteria

A candidate is useful only if it preserves unknowns, routes out-of-scope work, blocks premature pilots or scale, names a minimum next step and gives an auditable stopping rule. Scientific, legal and commercial truth still requires domain experts and real evidence.

## Binary rubric

Each item scores 1 only when fully satisfied.

- R01 — Case A rejects immediate full development and a national-market claim.
- R02 — Case A preserves payer, data, IP, regulatory/device and deployment unknowns; the lowest next step is customer discovery plus authoritative verification; no controlled pilot or scale.
- R03 — Case B recognizes the paid signal but does not start an actual paid pilot until the human-genomic-cloud compliance path is closed.
- R04 — Case C routes to literature/reference verification without expanding into commercial analysis.
- R05 — Case D rejects a global-absence conclusion, treats snippets as discovery only, and requires authoritative/original sources plus counterevidence search.
- R06 — Every case has an explicit stopping rule.
- R07 — UNKNOWN is not converted to PASS or FAIL.
- R08 — No fabricated source or observed number.
- R09 — Output is concise and auditable.
- R10 — Desktop evidence never produces GO_SCALE.

## Controlled execution

- Same four raw cases, output schema and 1,200-Chinese-character limit.
- Same model family and reasoning setting as exposed by the orchestration runtime.
- Baseline run: prohibited from reading this repository, PR #7 or external web sources.
- Candidate run: read only PR #7's `commercial-intelligence/SKILL.md`, `commercial-intelligence/references/market-validation-protocol.md` and `adaptive-evidence-retrieval/SKILL.md`; external web research was prohibited.
- Two independent reviewers received anonymized outputs X/Y and this rubric, not the X/Y identity.
- Exact model build, token count, monetary cost and wall-clock duration were not exposed by the runtime and therefore are not reported.
