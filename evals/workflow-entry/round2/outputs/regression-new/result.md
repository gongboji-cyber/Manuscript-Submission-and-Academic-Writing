# Revised submission text

## Results sentence

> In the paired analysis with patients weighted equally, the mean difference between Method A and Method B (A−B) was 0.020 (95% CI, −0.005 to 0.045).

This replaces the v1 sentence and does not claim superiority: the reported interval includes zero. It also does not imply equivalence or no difference.

## Cover-letter contribution

> Our study evaluates the difference between Methods A and B using a paired analysis in which patients are weighted equally. The estimated mean difference (A−B) was 0.020 (95% CI, −0.005 to 0.045), quantifying the comparison while retaining the uncertainty in the direction and magnitude of the difference. Accordingly, we do not claim that Method A is superior or that it improves clinical outcomes.

## Materials requiring synchronization

### Known stale

1. **Figure2.pdf** — it is known to use analysis-v1. Regenerate it from the authorized v2 output, then verify the A−B direction, estimate, CI, analysis unit, patient-equal weighting, labels/legend, and final rendered appearance. No figure was generated or inspected here.
2. **Supplement-v1** — it is known to use analysis-v1. Update every affected method description, result, table/figure, caption, and cross-reference to v2; then cross-check the revised supplement against the main text. Its contents were unavailable, so affected locations and post-update consistency could not be verified.

### Dependency scan required

The following submission components must be searched and revised **if** they contain `0.035`, `0.010–0.060`, analysis-v1, the former analysis unit/weighting, or claims of superiority or improved clinical outcomes:

- Abstract and any structured abstract fields.
- Statistical Methods, including the paired analysis unit and equal-patient weighting.
- Other Results text, tables, figure legends, and any source files used to create Figure 2.
- Discussion and Conclusion.
- Title/subtitle, highlights, key points, significance or impact statements, graphical-abstract text, and plain-language summary.
- Submission-system metadata and any response/rebuttal letter that repeats the result or contribution claim.

These materials were not provided, so their present status is **unknown**, not verified or presumed incorrect.

## Change-impact record

| Change source | Affected artifact and freshness | Check required on the updated artifact | Actual status |
| --- | --- | --- | --- |
| analysis-v1: A−B 0.035 (95% CI, 0.010 to 0.060) → author-designated analysis-v2: A−B 0.020 (95% CI, −0.005 to 0.045), with the paired unit fixed and patients weighted equally | Revised Results sentence — **current for alignment with the supplied v2 summary** | Verify direction, estimate, interval, analysis identity/weighting, and claim strength | **Completed on the revised sentence** against the supplied summary; no source-data or code verification performed |
| Same change | Revised cover-letter contribution — **current for alignment with the revised Results sentence** | Verify numbers, method description, and absence of unsupported superiority/clinical-benefit claims | **Completed on the revised paragraph** against the supplied summary |
| Same change | Figure2.pdf — **stale** | Regenerate from v2; numerical, technical, caption, and visual QA on the new file | **Not performed**; source/output unavailable and figure generation was outside scope |
| Same change | Supplement-v1 — **stale** | Update from v2; verify methods, numbers, claims, figures/tables, and cross-references | **Not performed**; supplement unavailable |
| Same change | Other potentially dependent submission materials listed above — **unknown pending dependency scan** | Search for v1 numbers/method/claims, update affected items, and cross-check the resulting submission package | **Not performed**; materials unavailable |

Unchanged work that may continue: authorship and affiliations, acknowledgments, funding/conflict disclosures, references unrelated to the changed analysis, and purely stylistic formatting are not made stale by this numerical/method change because no dependency on the analysis was identified. They were not otherwise audited here.

## Verification boundary

Only the supplied summary values and the author's statement about the paired-unit fix were available. The v2 analysis itself was **not independently verified**: no source data, code, or run logs were provided, and no analysis was rerun. The edits are therefore wording- and consistency-level revisions to the author-designated current analysis, not certification of its statistical validity or clinical meaning.
