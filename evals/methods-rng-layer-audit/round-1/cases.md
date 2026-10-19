# Round 1 raw cases

All data and entities below are synthetic and public-safe. These inputs contain no diagnosis, expected answer or scoring hint.

## Case A — nested estimator

A benchmark fixes data generation and train/test split with outer seed 20261020. It fits a random-forest regressor with `random_state=None`, repeats five different outer seeds once each, and reports the between-seed SD as the full uncertainty. An exact rerun of outer seed 20261020 produces a different top-20 ranking and changes which method is declared best. Audit whether the numerical comparison is ready for a main conclusion and specify the minimum next check.

## Case B — repeatable but seed-sensitive

A simulation fixes the splitter and estimator with documented integer seeds. Exact reruns produce identical output hashes. Across the predeclared 20 estimator seeds, however, the preferred method changes in 7 runs. The author asks whether exact repeatability alone is sufficient to claim robust superiority.

## Case C — not applicable

A script computes a closed-form mean difference from a frozen CSV. It contains no random sampling, randomized estimator, stochastic optimization, concurrency or hardware-dependent reduction. Two exact reruns have the same input and output hashes. The author asks whether a new random seed must be invented before reporting the descriptive result.

## Case D — unsupported nondeterminism

A hosted model API exposes model/version identifiers but no seed control. Frozen inputs and settings give three different scores; one result crosses the predeclared deployment threshold. The author cannot replace the service during this audit. Decide what can be reported now and what stops the deployment conclusion.
