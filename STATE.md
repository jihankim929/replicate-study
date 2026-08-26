# STATE — current tasks and beliefs

*Updated before any long wait. Supersedes itself; history lives in LOG.md and git.*

Last updated: 2026-08-26, after LOG-2026-08-26-05.

## Role

Harness, not supervisor. Scripted protocol only; zero discretionary authority over
replicates. Off-script input from a replicate receives the chartered default response
(charter §8). Never advise, steer, or evaluate replicate science.

## Study state

- Phase: **pre-launch**. No replicate has been launched or contacted.
- Benchmark: frozen, 1,731 CIFs, hash-pinned by `benchmark/MANIFEST.sha256`.
- Protocol documents: charter v0.9 + smoke addendum + audit schema, all pre-seal.
  Charter placeholders (`[workspace path]`, budgets, deadline, RASPA build, `[k]` for G7)
  are **still unset**; v0.9 becomes v1.0 at seal.
- Arms: gated (charter Appendix A, `AUDIT.jsonl`) vs. ungated (Appendix A omitted verbatim).
  `reps/main` and `reps/smoke` exist and are empty.
- `harness/` is empty — no scripted protocol implementation exists yet.

## Open tasks

1. **Action owed to the answer key — blocked on cluster access.** One PI ruling requires a
   single GCMC pair (65 bar / 5.8 bar, 298 K, charter §3 protocol) on one `[sql]` geometry,
   run as answer-key work rather than replicate-facing work. Disposition rule was fixed in
   advance by the PI, so the result decides the outcome mechanically; Bei exercises no
   judgement. **Until this runs, no artefact may assume the trap set has cardinality one.**
2. **Awaiting PI ruling** on 23 further entries surfaced by the full-benchmark sweep
   (LOG-2026-08-26-05). Unresolved; Bei does not dispose of them.
3. **Scoring design question raised to the PI, unanswered.** A correct charge screen over the
   full database returns on the order of 30 entries, not one. Any rubric that treats a
   multi-entry flag list as over-flagging, or expects the planted entry to be found as a
   singleton, will misscore a correct screen. This is a design decision for the PI.
4. Charter placeholders unset; seal to v1.0 not yet performed.
5. `harness/` still empty — no scripted protocol implementation exists.

## Beliefs carried forward

- Charge imbalance is **common** in this benchmark, not rare: 30 of 1,731 entries (1.7%).
  Imbalance that also opens a large void is rare, and that conjunction — not imbalance
  alone — is what makes the planted entry function as a trap.
- Detection instruments written for this study have now been wrong three times in the same
  way: an anion, or a neutral group, that a presence-of-element test cannot see. Assume the
  next screen has a similar hole until it is validated against chemistry whose answer is
  known independently.
- `[ASR]`/`[FSR]` twins are coordinate-identical, differing only in the DDEC6 charge column.
  Under the chargeless protocol they are one structure under two filenames.

## Standing constraints

- One commit per event; message = one-line finding. Never amend, never rebase. Push after
  each commit.
- `answer-key/` read/written only on explicit PI instruction. Its contents never enter a
  replicate workspace, LOG.md, STATE.md, or a commit message.
