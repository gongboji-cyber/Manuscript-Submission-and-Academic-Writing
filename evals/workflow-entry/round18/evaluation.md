# Round 18 evaluation

## Defect and completion condition

`main@90f43f2` merged two new professional modules—`adaptive-evidence-retrieval` and `commercial-intelligence`—but the existing unified controller PR still described twelve professional modules and had no routes to either stable skill. A user entering through the controller could therefore miss the new unfamiliar-problem protocol and commercial gate workflow.

Completion required: merge the current main without rewriting history; add exactly one bounded route to each stable skill; preserve reference-matching and downstream scientific-judgment boundaries; update the module/version snapshot; pass structure/link checks; and run frozen normal, boundary and not-applicable cases with independent review.

## Minimal change

- Merged `main@90f43f21a58a67686cd7dae75dc8e857641900c2` into the existing `optimize/workflow-entry` branch with a two-parent commit.
- Routed unfamiliar scientific/technical evidence problems to `adaptive-evidence-retrieval`.
- Routed commercial research to `commercial-intelligence`, with adaptive retrieval first when source/query/adversarial-search logs are needed.
- Kept narrow DOI/claim matching in `retrieve-and-match-references` and sentence polishing in `audit-and-polish-manuscript`.
- Added explicit boundaries: desktop research cannot pass commercial G6 or imply `GO_SCALE`; a no-find result is not proof of nonexistence; adaptive retrieval does not replace downstream scientific judgment.
- Updated the source snapshot to 14 professional modules and excluded deleted historical evaluation fixtures from runtime inputs.

## Verification

Static checks found 15/15 runtime skill entries including the root controller, 15/15 present and unique frontmatter names, zero missing relative links, and exactly one new route for each added module. Before this evaluation-only commit the branch was 25 commits ahead and 0 behind main.

Four frozen public-synthetic cases covered unfamiliar parser diagnosis, commercial pilot readiness, narrow DOI claim matching, and narrow numeric-preserving polish. Each baseline and candidate condition was executed twice. Executors saw only raw prompts; the rubric was separate. Two fresh reviewers regraded verbatim anonymized outputs after an initial compressed review, and confirmed that scores did not change.

Both reviewers conservatively scored both systems 9/10 at system level. The candidate did not improve pass rate, so no general reliability or efficiency gain is claimed. It did make stable routing, evidence/contradiction logs, evidence status and gate labels more explicit. The common failure was criterion 4: commercial role/economics completeness. One reviewer found candidate replication 2 sufficient; the stricter reviewer required an explicit unit-economics/cost model. The baseline also failed to separate payer from user/buyer.

## Limits and next decision

The test assessed written plans only: no live retrieval, code execution, full-text reading, interviews, private data, or paid services. Model deployment ID, tokens, costs and comparable latency were unavailable. The result does not certify scientific, regulatory, privacy, IP, or commercial correctness.

The controller PR remains draft because this is a cross-module architecture change. Do not merge it automatically. Human review should decide whether the commercial entry contract should require unit economics explicitly or whether the existing `bottom_up_market`, `business_model` and G3/G6 outputs already cover the intended boundary; add a runtime rule only after that decision and a failing case, not merely to raise this rubric score.
