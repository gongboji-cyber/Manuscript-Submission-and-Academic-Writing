# Round 19 evaluation — optional-module fail-closed contract

## Defect and acceptance rule

The eight-skill personal installation does not include `research-topic-selection`, `research-flow-diagrams`, or the coordinator. Three installed core skills nevertheless used hard handoffs to those unavailable modules. The candidate must:

1. name the missing dependency and never imply that it ran;
2. use `NOT_RUN/HOLD` for decisions or graphics that require it;
3. continue only independently valid work;
4. keep already authorized methods/statistical-plot tasks unblocked;
5. not present fallback output as equivalent to the unavailable specialist module.

Candidate acceptance was frozen at R01–R10 = 10/10 with no T2/T3 regression.

## Versions

- Baseline: `main@90f43f21a58a67686cd7dae75dc8e857641900c2`
- Candidate runtime: `optimize/workflow-entry@ef35f814e0cd6d0d0ec74861417f2c1e2a4e669a`
- Python used for static validation: 3.12.14
- Validator: `/root/.codex/skills/.system/skill-creator/scripts/quick_validate.py`
- Exact model deployment, token counts, fees, and comparable end-to-end latency were not exposed.

## Runs and integrity

- Inputs are four public synthetic tasks in `cases.md`; the rubric was stored separately and not shown to producers.
- Baseline and candidate producers received the same four tasks and the same list of installed/unavailable modules.
- The first candidate run read the repository coordinator even though it was not installed. It was rejected before scoring and is not archived as a scored output.
- The scored candidate rerun was restricted to the same three professional entrypoints used by the baseline and explicitly prohibited reading the coordinator or missing modules.
- Raw scored outputs are preserved without summarization in `baseline-output.md` and `candidate-output.md`.
- A fresh reviewer read only the cases, frozen rubric, and two raw outputs. It did not inspect branch identity or implementation history.

## Results

| Version | R01–R10 | T2/T3 regression | Acceptance |
|---|---:|---|---|
| Baseline | 8/10 | no | no |
| Candidate | 10/10 | no | yes for this task set |

Baseline failed R03 because T1 used only `HOLD`, and R07 because T4 supplied Mermaid source rather than marking graphical generation `NOT_RUN/HOLD`. Candidate passed all ten items, preserved a usable unexecuted SAP for the already-authorized study, and preserved the statistical-plot plan.

## Static checks

- All three modified SKILL directories returned `Skill is valid!` from `quick_validate.py`.
- Comparing this round's starting head `abb929a66d702af9b66481fc69fe8f19e8a5c1f5` with candidate `ef35f814e0cd6d0d0ec74861417f2c1e2a4e669a`: ahead 3, behind 0, exactly three expected SKILL files modified, each as one replacement line.
- No personal installed skill was changed.

## Boundary

This is one run per scored version on four synthetic tasks and one independent textual review. It supports the stated fail-closed delivery contract only in this task set. It does not validate real manuscript novelty, statistical analysis, figure rendering, scientific correctness, or general success rates. T1 lacked a manuscript; T2 lacked data and full design parameters; T3 did not render files; T4 verified only supplied arithmetic. Human/module-owner review remains required before merging the architectural PR or synchronizing personal skills.
