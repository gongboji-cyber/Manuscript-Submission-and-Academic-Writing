# Citation-chain audit: reusable failure-aware research workflow

Status: **field-tested on one exploratory project; NOT externally validated**. Date: 2026-10-19.

## Purpose
Reusable procedures for tracking quantities from primary data to downstream citations. Do not present the workflow as a novel validated instrument, a systematic-review replacement, or proof of numerical citation drift prevalence.

## Case history and verdict
JRSM manuscript `From annual incidence to diagnostic probability: preserving the meaning of childhood pneumonia estimates` was desk-rejected. Follow-up Phases 1–4 explored UNICEF childhood-pneumonia estimate reuse.

* Source provenance: UNICEF reported global ~1,400/100k, South Asia ~2,500/100k, West/Central Africa ~1,620/100k; work traced the underlying metric to Wahl et al. 2018, 2015 annual pneumonia incidence in children aged 1–59 months. Regional denominators remained unresolved and must not be reconstructed from unjustified unweighted means.
* Discovery: OpenAlex citation, numerical and textual channels; Frame A included 1,098 Wahl citations, Frame B 1,792 deduplicated candidates.
* Closed validation cohort: 92 numerical-reuse candidates; 37 full-text checked, 26 nonrelevant full texts, 26 paywalled, 3 extraction failures. Of the 37 checked, one relevant numerical reuse was P0 (preserved). Along with two earlier independent P0 publications, independent verified outcomes were **3 P0, 0 verified drift**.
* Four prior hand-selected known examples were tagged `PRIOR_KNOWN_CASE` and excluded from independent inference. Do not report their observed positive fraction as a population rate.
* No second independent human rater: `HUMAN_RELIABILITY_PENDING`.
* Empirical-prevalence work closed as `PIVOT_TO_METHODS_COMMENTARY`; conceptual work judged `REVISE_CONCEPTUAL_CONTRIBUTION`. Further conceptual publication is not presumed worthwhile.

The reported counts are derived from previous local Codex phase summaries and must be reverified against the original CSVs before independent reuse.

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
- Local Codex workspace was reported as `citation_estimand_drift_empirical/`; it is **not automatically accessible from GitHub**. Copy no data from unverified paths.
- Suggested evaluation: blind human annotations on independent records, compare against baseline number+DOI checking, count additional correctly identified meaning mismatches and false positives, cost and human time. Do not claim an improvement unless empirically shown.

## Reusable lesson
A large discovery graph (1,098 and 1,792 candidate records) did not yield a large eligible evidence corpus. The bottleneck was validated source-dependent numerical reuse, not search volume. Independent negative or inconclusive checks are valuable for stopping bad projects, not evidence that a phenomenon never occurs.
