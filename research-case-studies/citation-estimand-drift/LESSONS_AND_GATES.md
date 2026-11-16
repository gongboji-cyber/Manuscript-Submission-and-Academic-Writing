# Citation-chain audit: reusable failure-aware research workflow

Status: **field-tested on one exploratory project; NOT externally validated**. Date: 2026-10-19.

## Purpose
Reusable procedures for tracking quantities from primary data to downstream citations. Do not present the workflow as a novel validated instrument, a systematic-review replacement, or proof of numerical citation drift prevalence.

## Private origin and public validation boundary

This workflow was adapted from a closed private exploratory project. The public repository intentionally omits
the manuscript title, journal and submission history, disease-specific records, local workspace names, private
file hashes, source-specific counts and unpublished empirical estimates.

Only the synthetic fixtures in this directory are public runnable examples. They can test software behaviour and
record-keeping contracts, but they cannot establish prevalence, workflow accuracy, clinical importance or
publication value. Any reuse of private project findings requires fresh authorization and re-verification against
the frozen private records.

## Mandatory gates for future citation/quantity audits
1. **Source reconstruction**: identify the original numerator, denominator, units, population, period, case definition, estimate year, uncertainty, and source lineage. Explicitly flag unknown information.
2. **Research-question/denominator freeze**: differentiate candidate records, eligible publications, full-text-interpretable publications, verified numerical reuse, and individual numerical occurrences. Never merge rates across frames with different ascertainment methods.
3. **Independent discovery**: use complementary direct-citation and numerical/textual searches; log query, API, date, pagination, return count, de-duplication and retrieval errors.
4. **Evidence-grounded extraction**: preserve exact text, reference match, page/section, surrounding context, document version, DOI, and access status. An extracted number alone is not proof of source dependence.
5. **Case coding**: distinguish P0 (meaning preserved), D1 statistical measure, D2 population, D3 time horizon, D4 numerator/denominator/observation unit, D5 probability transport, D6 analytical use, U uncertain. These are provisional, possibly overlapping dimensions, NOT a validated measurement scale.
6. **Human adjudication**: AI can triage, not impersonate a human reviewer. Preserve independent first-pass judgments and pre-adjudication disagreement; do not compute fake inter-rater reliability.
7. **Negative controls**: include clearly correct reproductions, valid mathematical transformations, harmless abbreviations, changed-source equivalents and unavailable source definitions. Do not label all differently worded quantities errors.
8. **Inference discipline**: distinguish publication-level from instance-level denominators; account for clustering and missing full text; do not assign statistical confidence to convenience searches or selected examples.
9. **Adversarial audit**: challenge source provenance, mathematical conversion assumptions, detection false positives, novelty, selection bias and any alleged clinical consequences.
10. **Hard stopping**: if source definition, sampling frame, retrieval coverage, validation or conceptual novelty remains deficient after a bounded pilot, archive the assets and issue STOP/PIVOT rather than launching open-ended searches.

## Programmatic workflow
`discovery -> metadata_normalization -> fulltext_access -> extraction -> citation_matching -> source_target_quantity_comparison -> human_review -> frozen_analysis -> red_team -> decision`

Keep a record registry (one row per publication), occurrence table (one row per instance), query log, retrieval status table, evidence ledger, independent annotation sheet, SHA256 manifest and a reproducibility README. Required states for inaccessible or nonrelevant records must remain distinct. Never relabel retrieval failure as scientific P0.

## Suggested source-to-target quantity review
Fields: source measure; target measure; population; numerator/observation unit; denominator; time horizon; case definition; source provenance; assumptions for transformation. Results: preserved, justified transformation, assumptions needed, unsupported transformation, insufficient information. A rate may inform a risk under explicit assumptions, but an annual event incidence is not automatically a point prevalence or clinical pre-test probability.

## Integration guidance for the repository
- Treat this file as a **case-derived quality gate** for existing literature-review, citation-checking, methodology, statistics, and manuscript pre-submission skills.
- Avoid duplicating or replacing existing skills before inspecting their entrypoints.
- Add executable regression fixtures from local raw CSVs **only after** checking licensing, de-identification, accuracy and provenance.
- Keep full papers and any restricted sources outside the public repository.
- The originating private workspace is not identified or accessible from this public repository. Copy no data from unverified paths.
- Suggested evaluation: blind human annotations on independent records, compare against baseline number+DOI checking, count additional correctly identified meaning mismatches and false positives, cost and human time. Do not claim an improvement unless empirically shown.

## Reusable lesson
A large candidate discovery graph did not necessarily yield a large validated evidence corpus. The bottleneck was validated source-dependent numerical reuse, not search volume. Independent negative or inconclusive checks are valuable for stopping bad projects, not evidence that a phenomenon never occurs.
