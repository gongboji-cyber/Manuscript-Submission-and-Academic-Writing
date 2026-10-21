# Round 20 evaluation — installed personal baseline vs PR candidate

## Decision and defect

Round 19's behavioral comparison used repository-main files and mislabeled them as installed personal skills. Round 20 therefore compared the actual installed personal skill files with the PR candidate under the same task set and isolation rules.

The confirmed personal-baseline defect is fail-open cross-module handling: when the topic-selection or flow-diagram specialist is unavailable, the installed skills may omit the module name and required `NOT_RUN/HOLD` state, and the plotting skill may substitute Mermaid source as a completed deliverable.

Acceptance was frozen before either output was scored: 10/10 rubric items and no T2/T3 regression.

## Versions and actual read scope

- Installed-personal baseline repository remote HEAD before the candidate sync attempt: `08e7a7b9e5636a597d7973facfe5d3ea4d39e9c9`.
- Candidate source used by the producer: PR #3 commit `0f02a7aa473212a6c5dcd40ee9f4dc08d39a9d41`.
- Candidate files read: only the three `SKILL.md` files for manuscript audit, methods/statistics, and statistical plotting.
- Personal files read: only the corresponding three files under `/root/.codex/skills/remote-skills`.
- Producers could not inspect this evaluation, the rubric, coordinator material, or the unavailable modules.
- The four inputs in `cases.md` are public synthetic cases.

## Reproduction

Producer A received the cases with the installed personal files. Producer B received the same cases with the three candidate files. The scoring rubric was kept in a separate file and was not supplied to either producer. Two fresh reviewers then received only `cases.md`, `rubric.md`, and the two anonymous outputs.

Raw artifact hashes:

| Artifact | SHA-256 |
|---|---|
| `personal-output.md` | `ffca279026b147c470051c9602713b19b40dce99454bc398c972017deafdfbb6` |
| `candidate-output.md` | `bbfe88ab2c9ef7180232756de1f3d4e84cae593336d2384333fbbee659aa5cf3` |
| `cases.md` | `d32710eb6d9fb12eac46c6fea2ccfe334120d0220816805eaa2c66042d8e38af` |
| `rubric.md` | `3e4ecd4f90ee48a8990e45c9f80481f7b21f716bdb781546e716664f50b79f5a` |

## Results

Both independent reviewers produced the same result:

| Version | R01 | R02 | R03 | R04 | R05 | R06 | R07 | R08 | R09 | R10 | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Installed personal baseline (A) | 0 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 7/10 |
| PR candidate (B) | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 10/10 |

No T2/T3 regression was observed. The candidate names the missing module, records the dependent decision/generation as `NOT_RUN/HOLD`, continues independent work, and does not represent a generic fallback as the specialist output.

This supports the fail-closed workflow behavior only for these four synthetic cases. It does not establish scientific correctness, real-data execution quality, rendered-figure quality, or generalization to all prompts. The runtime provided no token/cost measure; elapsed-time comparisons were not used.

## Structural defect found and corrected

A direct installed-vs-candidate diff showed the intended change was small (three files: 6 insertions and 1 deletion after correction), but the plotting candidate contained a literal `\\n\\n` before a Markdown heading. That broke the section boundary even though the behavioral output passed.

The candidate branch was corrected at `9fe933fe38fc38897662c106b05721c31a4fcbc9`. After correction:

- all three candidate files are byte-identical to the local personal candidates by Git blob SHA;
- `quick_validate.py` reports `Skill is valid!` for all three folders;
- the literal escaped-section-break check returns no match;
- the corrected plotting blob is `67feb73448c8a0310c10442e135794f01730701c`.

The formatting correction does not change the tested handoff semantics. It restores the intended Markdown blank line and heading.

## Personal save status

The validated three-file update is preserved locally in personal-skills commit `73d441476369af0416278b6b0ec4f62c12b1bc76`. Two push attempts returned HTTP 422. Read-only verification showed the remote still at `08e7a7b9e5636a597d7973facfe5d3ea4d39e9c9` and the local branch ahead by one commit.

Therefore the personal Skills page is **not confirmed updated**. Do not describe the local commit as a completed personal-skill save until the remote accepts it.
