# STATE — current tasks and beliefs

*Updated before any long wait. Supersedes itself; history lives in LOG.md and git.*

Last updated: 2026-08-26, after LOG-2026-08-26-02.

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

1. **Awaiting PI ruling** on the entries flagged out of Assignment 1. Bei does not resolve
   their status. Until ruled on, no downstream artefact should assume the slice contains
   exactly one defective structure.
2. Census scope was the `[sql]` slice only (231 of 1,731). Whether the same defect class
   occurs in the other ~1,500 entries is **open and unswept**. The two-pass procedure in the
   sealed section is directly reusable if the PI wants the full sweep.
3. Charter placeholders unset; seal to v1.0 not yet performed.

## Standing constraints

- One commit per event; message = one-line finding. Never amend, never rebase. Push after
  each commit.
- `answer-key/` read/written only on explicit PI instruction. Its contents never enter a
  replicate workspace, LOG.md, STATE.md, or a commit message.
