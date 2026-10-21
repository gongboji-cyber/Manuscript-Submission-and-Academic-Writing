# Independent round-3 review

Input hashes:

- `cases.json`: `328337cff8d3f785cc6c6d11920ec838bc2ba5feceda876cf44782731798acd1`
- `rubric.json`: `f34418b3a27a8f3cecc3b8827cf236402506c87f437ef2666dc7863920d7c389`

## Results

| Run | Variant | Met | Not met | Unclear | Total |
|---|---:|---:|---:|---:|---:|
| old-1 | old | 13 | 1 | 0 | 14 |
| old-2 | old | 14 | 0 | 0 | 14 |
| old-3 | old | 13 | 1 | 0 | 14 |
| new-1 | new | 14 | 0 | 0 | 14 |
| new-2 | new | 14 | 0 | 0 | 14 |
| new-3 | new | 14 | 0 | 0 | 14 |

Variant totals were **40/42 met** for old and **42/42 met** for new. There were no unclear judgments.

## Criterion consistency

| Criterion | Old (3 runs) | New (3 runs) | All runs | Reading |
|---|---:|---:|---:|---|
| U01-1 | 3 met | 3 met | 6/6 met | Stable |
| U01-2 | 3 met | 3 met | 6/6 met | Stable |
| U01-3 | 3 met | 3 met | 6/6 met | Stable |
| U01-4 | 3 met | 3 met | 6/6 met | Stable |
| U01-5 | 3 met | 3 met | 6/6 met | Stable |
| U02-1 | 3 met | 3 met | 6/6 met | Stable |
| U02-2 | 3 met | 3 met | 6/6 met | Stable |
| U02-3 | 2 met, 1 not met | 3 met | 5/6 met | Old mixed; new stable |
| U02-4 | 3 met | 3 met | 6/6 met | Stable |
| U03-1 | 2 met, 1 not met | 3 met | 5/6 met | Old mixed; new stable |
| U03-2 | 3 met | 3 met | 6/6 met | Stable |
| U03-3 | 3 met | 3 met | 6/6 met | Stable |
| U03-4 | 3 met | 3 met | 6/6 met | Stable |
| U03-5 | 3 met | 3 met | 6/6 met | Stable |

The two not-met judgments were:

- **old-1, U02-3:** the response said the presentation-only changes did not require rendering (“也不需要重跑、重绘或渲染”) and did not make actual document insertion/render/style verification a condition of package-ready status. It only made full-bibliography compliance conditional on whether more titles existed.
- **old-3, U03-1:** the cover-letter sentence said the cohort included adults “eligible for screening from age 45 under G-2026.” Eligibility beyond the age threshold was not supplied, so this invented an unsupported guideline detail.

All other run/criterion judgments were met. The exact evidence for every judgment is recorded in `independent-assessment.json`.

## Regressions and stability

No frozen criterion was met less often in the new variant, so no regression was observed. The new variant was internally consistent at 14/14 in all three runs. The old variant scored 13/14, 14/14, and 13/14, with different isolated misses.

The descriptive difference favors new, but it was not repeated at every run index: the met-count differences were +1, 0, and +1. Thus the new result is stable within this small exploratory sample, while the between-variant advantage is not sufficiently replicated to establish durability. No statistical significance is claimed.

## Limitations

This review grades literal output evidence only. It does not certify medical, statistical, guideline, or journal-style correctness. The run logs are executor self-reports, not complete independent tool traces. No absent facts, unavailable-file contents, external identities, completed edits, renders, or checks were inferred. With only three runs per variant, the totals are descriptive.
