# Round 2 evaluation

## Defect and completion rule

The candidate required an RNG inventory but did not explicitly require those fields to survive into the user-visible delivery. The planned completion rule was:

1. each applicable case exposes RNG source, control status, injection point or unavailable control, and software/model version;
2. deterministic work is marked not applicable without inventing a seed;
3. hosted nondeterminism reports repeat count, observed range and decision flips as count/denominator;
4. decision-changing drift remains HOLD;
5. no other rubric item regresses.

Only item 4 showed a consistent expression improvement. Items 1 and 3 remain incomplete.

## Minimal runtime change

Commit `2718af3df5391f738e6589d7c32e281ca7e3d62f` added one delivery-contract paragraph to `references/computational-audit.md`. It added no numerical threshold or scientific decision rule. It requires per-task RNG provenance and asks repeat reports to include run count, range and decision flips/total, with missing repetition kept descriptive.

## Independent blind review

Producing outputs were anonymized before grading. Reviewers were fresh same-model agents, not human domain experts.

### Baseline versus candidate v1

Reviewer 1:

- baseline X: 9/10
- candidate Y1: 9/10
- common failure: R08, because A and B did not explicitly expose software/model versions and a complete per-case RNG ledger
- conclusion: no scoreable behavior difference; Y1 was more explicit about HOLD, single-factor comparison and observed range

Reviewer 2:

- baseline X: 7/10
- candidate Y1: 8/10
- common failures: R06 and R08
- score difference: Y1 explicitly preserved the predeclared-threshold condition for D
- conclusion: both versions made the same stop decisions; Y1 improved audit phrasing, not demonstrated scientific correctness

The disagreement on R06/R07 reflects the strictness of interpreting “range/frequency” and whether the predeclared status must be repeated verbatim. It was not resolved by averaging scores.

### Baseline versus candidate v2

Reviewer 3:

- baseline X: 7/10
- candidate Y2: 8/10
- candidate gain: R03, because Y2 explicitly kept the main comparison on HOLD until layered drift was quantified
- common failures: R06 and R08
- Y2 still omitted explicit software/estimator versions for A and B and did not report D's threshold flip as an explicit count/denominator

## Verdict

`PARTIAL_BEHAVIORAL_SUPPORT — DO_NOT_MERGE_YET`

The candidate consistently gives conservative decisions for the four synthetic cases and does not regress the deterministic not-applicable case. However, main already handled most of the cases correctly. The runtime edit did not satisfy its own completion rule, so this round does not establish a reliable improvement in the full delivery contract.

Do not add further wording solely to optimize this four-case rubric. Reopen the runtime rule only after a natural task again omits a required RNG/version field, or after a human methods reviewer decides that explicit `NOT PROVIDED` fields and flip count/denominator should be mandatory in concise answers.

## Measurement boundary

- Four public-safe synthetic cases.
- One producing run per version.
- Same exposed model family and reasoning setting.
- Same-model agent reviewers; no human methods expert.
- No numerical experiment, model training, hosted-API call, document rendering or scientific validity assessment.
- No exposed token, cost or comparable timing data.
- Scores are descriptive for these fixed outputs and are not a validated reliability metric.
