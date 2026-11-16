# Citation estimand drift: reusable audit toolkit

This directory contains the reusable engineering assets from a closed exploratory project. It is a
case-derived quality gate, not a new standalone skill.

## What this project established

- Multi-channel citation discovery (source-citation and numerical/textual frames).
- Source quantity provenance checks.
- Full-text citation-context extraction and evidence ledgers.
- Independent annotation templates and disagreement tracking.
- Denominator, missing-full-text, selection-bias, and inference gates.
- Adversarial red-team checks and GO/PIVOT/STOP decision rules.

## What this project does not establish

- Drift prevalence in any population.
- That the quantity-verification checklist is a validated instrument.
- That machine coding is equivalent to independent human review.

## Repository call relationships

Route decision-level work through existing skills before using this toolkit:

| Need | Existing skill to call |
|---|---|
| Evidence-first retrieval and coverage logging | `adaptive-evidence-retrieval` |
| Literature identity, reading, claim matching | `retrieve-and-match-references` |
| Methodology and estimand/statistics audit | `guide-research-methods-statistics` |
| Novelty, feasibility and GO/HOLD/STOP gates | `research-topic-selection` |
| Pre-submission evidence and language audit | `audit-and-polish-manuscript` |

This directory is a concrete implementation for one case. Do not duplicate those entrypoints.

## Commands

The scripts use only the Python standard library. Run from the repository root:

```bash
python -B research-case-studies/citation-estimand-drift/scripts/discovery.py --help
python -B research-case-studies/citation-estimand-drift/scripts/extraction.py --help
python -B research-case-studies/citation-estimand-drift/scripts/gates.py --help
python -m pytest research-case-studies/citation-estimand-drift/tests -q
```

## Fixtures

`fixtures/` contains synthetic, non-copyrighted examples only. No full-text papers or restricted sources are
stored in this repository.
