# Round 1 rubric and execution controls

This rubric is separate from the raw cases. It must not be shown to producing runs. Scientific correctness still requires independent review; this file does not certify its own author.

## Completion criteria

A candidate is useful only if it inventories stochastic layers, tests exact repeatability on frozen inputs, distinguishes repeatability from robustness, routes deterministic work to not applicable, and stops a decision when unexplained drift changes that decision or exceeds a predeclared tolerance.

## Binary rubric

Each item scores 1 only when fully satisfied.

- R01 — Case A identifies the uncontrolled nested estimator RNG rather than accepting the outer seed.
- R02 — Case A requires an exact same-input/same-environment repeat and a single-factor check that explicitly controls the estimator RNG.
- R03 — Case A is HOLD for the main comparison until the decision-changing drift is explained and quantified.
- R04 — Case B distinguishes exact repeatability from robustness across estimator seeds and does not infer validity from identical hashes.
- R05 — Case C marks the RNG gate not applicable and does not invent a seed.
- R06 — Case D records model/version/settings, repeats frozen calls, reports the observed range/frequency, and does not promise determinism the API cannot provide.
- R07 — Case D is HOLD for deployment because the unexplained spread crosses the predeclared decision threshold.
- R08 — Every applicable case names RNG source, seed/control status, injection point or missing control, and software/model version.
- R09 — Fixed seeds are never presented as proof of scientific validity, unbiasedness or generalization.
- R10 — No fabricated run, source, variance component or universal numeric threshold.

## Controlled execution

- Use the same four raw cases and the same concise output schema for baseline and candidate.
- Baseline reads the main-branch methods skill; candidate reads only the candidate-branch methods skill and directly linked references.
- Keep model family, reasoning setting, tool availability and per-case output budget identical.
- Producing runs receive `cases.md` only. Reviewers receive anonymized outputs and this rubric only after generation.
- Record exact model/runtime build, prompts, calls, duration and cost only when exposed.
- Status for this change: independent baseline/candidate model runs and expert scientific review are pending; do not record PASS from static checks alone.
