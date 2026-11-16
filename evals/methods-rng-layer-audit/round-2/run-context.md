# Round 2 execution context

## Fixed versions

- Baseline repository commit: `90f43f21a58a67686cd7dae75dc8e857641900c2`
- Candidate v1 commit: `c4b93d0205a0cfe3b7dbb1f111cc645a429fde39`
- Candidate v2 commit under test: `2718af3df5391f738e6589d7c32e281ca7e3d62f`
- Skill entry: `方法学/统计学指导/SKILL.md`
- Changed runtime reference: `方法学/统计学指导/references/computational-audit.md`
- Raw inputs: `../round-1/cases.md`
- Frozen rubric: `../round-1/rubric.md`

## Producing-run controls

- Model family exposed by the runner: `gpt-6.1-sol`
- Reasoning setting: `high`
- One producing run per version.
- Producers were placed in fresh isolated contexts.
- Producers received the same four raw cases and the same four-field output schema: 裁决、依据、最小下一步、可报告边界.
- Producers were told to read only the fixed skill commit and directly relevant references.
- Producers were told not to read `evals/`, PR descriptions, rubrics or other branches.
- No expected answer, suspected defect or scoring hint was supplied.
- No repository or personal-skill writes were allowed in producing runs.

## Review controls

- Outputs were anonymized as X and Y before review.
- Reviewers received the frozen rubric only after generation.
- Two fresh same-model reviewers assessed baseline versus candidate v1.
- One fresh same-model reviewer assessed baseline versus candidate v2 after the minimal runtime edit.
- Reviewer prompts did not disclose version identities.

## Unavailable measurements

The runner did not expose stable deployment build identifiers, token counts, monetary cost or comparable wall-clock duration. These fields are therefore recorded as unavailable rather than estimated. No numerical experiment, model training or real hosted-API call was executed; the test evaluates workflow responses to synthetic inputs only.
