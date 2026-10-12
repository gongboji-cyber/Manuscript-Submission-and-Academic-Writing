# Round 12 evaluation — patent handoff readiness and per-reference state

## Verified defect

A recent workflow pattern combined a positive handoff label with mandatory prior-art verification still open. Four frozen synthetic tasks therefore tested whether the current system distinguishes:

1. a package blocked by one potentially claim-changing unverified reference;
2. a technical draft whose stated internal handoff conditions are complete;
3. a local claim-editing request that must not become a filing-readiness audit; and
4. a commercial search summary that lacks primary claim evidence.

The baseline correctly held P1, preserved D2 as unverified, and gave a precise next action. However, both independent reviewers found that it omitted the supplied positive state that D1 had been read in full and charted. Because the frozen R02 required preserving D1 and D2 independently, the baseline failed the 9/9 acceptance rule. This state loss can create duplicate work or turn a partially verified evidence set into an undifferentiated “unverified” batch during handoff.

## Minimal change

Only `专利书写规范/SKILL.md` changed. Its delivery section now requires:

- separating current action permission from verification status and authority to file;
- preserving identity, verification state, and actual reading scope for each key comparison document;
- preventing an unverified D2 from erasing a verified D1 or a verified D1 from implying anything about D2;
- reserving “技术稿可交代理师” for the existing audit-template conditions; and
- labeling earlier professional assistance as `review-only`, not filing-ready or completed prior-art review.

No patent-law rule, scientific claim, legal threshold, search result, or patentability decision was added.

## Same-condition forward test

One fresh executor per version received the same four raw tasks and the relevant skill collection. The suspected defect, rubric, prior output, and expected answers were withheld. Two fresh blind reviewers per version received only that output and the frozen rubric.

- Baseline: R01 and R03–R09 were MET; R02 was `NOT_MET` by one reviewer and `INSUFFICIENT` by the other. Acceptance failed.
- Candidate: both reviewers scored R01–R09 as 9/9 MET.

The candidate preserved D1's completed verification, kept D2 unable to verify, used `review-only` for early assistance, allowed technical handoff in the complete positive control, kept the local edit scoped, and refused to treat a commercial summary as primary evidence.

## Sources and actual reading scope

- Repository and PR state: `main@5af337b3d8cdf530aa382ad9cf0f33de03cc046e`, candidate baseline `f4a7fb87b9d72daea43b419202ba63bf5d5c8be8`; draft PR #3 was open, mergeable, with no comments, reviews, or review threads at the start of this run.
- `work-skill-creator` package version `0.1.0`: read in full.
- `专利书写规范/SKILL.md`: read in full (265 newline-terminated baseline lines before the patch; the file lacked a final newline).
- `专利书写规范/assets/audit-report-template.md`: read in full (87 lines), including the seven “技术稿可交代理师” conditions.
- `专利书写规范/references/checklist.md`: read in full (175 lines).
- `专利书写规范/references/prior-art-and-inventiveness.md`: lines 1–180 read, covering source hierarchy, per-reference claim chart states, and inventive-step workflow.
- Root coordinator, handoff reference, and workflow record template: read in full.

No official legal source was newly interpreted because the change is a process-state contract, not a legal rule. Existing legal content and source versions remain unchanged.

## Regression and measurement boundaries

- Patent skill structure validation: PASS.
- Root/11-module structural regression: 11/11 checks passed; zero missing links.
- Topic-selection tests: 10/10 passed.
- Gate-ledger example: 18 rows / 3 topics passed.
- All skill entrypoints: 12/12 passed structure validation.
- Three local regression commands completed in 103,263,988 ns; this excludes model calls, review, cloning, and structure validation and is not an end-to-end efficiency comparison.

This is one execution per version on public synthetic inputs. Exact model ID, tokens, cost, and comparable model runtime were unavailable. Independent review establishes rubric compliance, not legal or scientific correctness. No real patent draft, unpublished invention, patient data, private communication, or proprietary search result is stored here.

## Recheck trigger

Reopen only if a future run again loses a verified source's state, uses an ambiguous “GO_TO_AGENT” while mandatory preconditions remain, or the patent audit template changes its readiness conditions. Any substantive legal threshold or patentability rule still requires authoritative source review and human patent-professional judgment.
