# Independent blind review — grader 4

Scope: only `version-a.md`, `version-c.md`, and `rubric.json` were read. Version identity was not inferred. R10 is intentionally not assessed. A pass below is limited to the rubric criterion and does not certify scientific correctness.

## Version A

| Criterion | Decision | Precise location | Basis |
|---|---|---|---|
| R01 | **fail** | `version-a.md:5-10,23` | T01 provides a bounded topic-triage workflow and disclaims completed search/experiments, but never names `research-topic-selection` as the first-choice module. The rubric expressly requires that named routing. |
| R02 | **pass** | `version-a.md:3,16-23` | The sole current decision is `EXPLORE_ONLY`; explicit STOP, HOLD, minimal-pilot, and later full-study transitions are tied to evidence gates. |
| R03 | **fail** | `version-a.md:27-28` | T02 respects the approved scope and moves to SAP, but never explicitly selects the required named module `guide-research-methods-statistics`. |
| R04 | **pass** | `version-a.md:35-41,43-53,55-65,67-80` | Estimand, independent units, A01, and sensitivity analyses are all present. Missing inputs block signoff, and no analysis execution or validation is claimed. |
| R05 | **pass** | `version-a.md:84,88-96,98` | T03 explicitly routes originality/redo value first to `research-topic-selection`; literature, methods, and manuscript work are conditional downstream steps. Code/polish is not used as an originality fix. |
| R06 | **pass** | `version-a.md:91-100` | STOP/HOLD/unlock rules are explicit, and without new experiments the answer refuses GO_FULL_STUDY or a claim that feasibility is established. |
| R07 | **pass** | `version-a.md:102-106` | T04 stays at one-sentence language/typography scope, does not call topic selection, and explicitly avoids broader review. |
| R08 | **pass** | `version-a.md:104-106` | It preserves 12%, 95% CI 2%–20%, association-only wording, `observed risk`, and terminal [12]. The dash change is scientific-meaning neutral. |
| R09 | **pass** | `version-a.md:3,8-10,21-23,27,32,53,80,84,92-100,106` | The response separates plans and local edits from unverified or unexecuted work; no completed search, experiment, SAP execution, novelty validation, or broad audit is fabricated. |
| R10 | **not_assessed** | `rubric.json:R10` | Reserved for parent static checking. |

## Version C

| Criterion | Decision | Precise location | Basis |
|---|---|---|---|
| R01 | **pass** | `version-c.md:3,7-14` | T01 explicitly names `research-topic-selection` first, makes other work conditional, and says no search, download, or experiment was executed. |
| R02 | **pass** | `version-c.md:3,14` | It gives the sole current decision `EXPLORE_ONLY` and evidence-specific unlock, HOLD, and STOP branches. |
| R03 | **pass** | `version-c.md:18-20,39` | T02 explicitly hands the approved scope to `guide-research-methods-statistics`, refuses renewed topic/novelty review, and limits unresolved items to targeted confirmation. |
| R04 | **pass** | `version-c.md:28-39,41-49,51-57` | It covers estimand, independent units, A01, and sensitivity analyses, while requiring approved inputs and disclaiming all execution/results. |
| R05 | **pass** | `version-c.md:61,65-73` | T03 starts with `research-topic-selection`, then conditionally routes evidence, methods, and only later manuscript work; code or prose is not treated as a novelty repair. |
| R06 | **pass** | `version-c.md:67-75` | It provides STOP/unlock conditions, denies GO_FULL_STUDY now, and permits at most GO_MINIMAL_PILOT after the specified gates. |
| R07 | **pass** | `version-c.md:77-81` | T04 remains a local fidelity/language check and expressly excludes topic, methods, full-manuscript, and citation-support review. |
| R08 | **pass** | `version-c.md:79-81` | It preserves 12%, 95% CI 2% to 20%, associative wording, `observed risk`, and terminal [12], without causal or numerical drift. |
| R09 | **pass** | `version-c.md:3,7-14,18,25-26,39,57,61,67-75,81` | All cases distinguish completed, pending, and unexecuted work; no search, experiment, result, validation, or broad-review completion is invented. |
| R10 | **not_assessed** | `rubric.json:R10` | Reserved for parent static checking. |

## Focused cross-checks

- **Named module routing:** Version A omits the required explicit module names in T01 and T02; Version C names both. Both correctly name and stage the key T03 modules.
- **T02 scope boundary:** Both versions honor the already-approved scope. Neither restarts topic/novelty review nor equates project approval with validated methodology.
- **T04 scope and scientific fidelity:** Both remain local and preserve the numerical estimate, interval, epistemic strength, `observed risk` qualifier, and citation placement.
- **Fabricated completion:** None found in either version.
- **Certification limit:** No total or collection of passes should be read as certification of scientific correctness.
