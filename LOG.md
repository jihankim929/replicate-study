# LOG — replicate-study (append-only)

Narrative record of harness events. One entry per event; entries are never edited or
removed. Corrections are new entries that reference the entry they supersede.

Sealed material (`answer-key/`) is never reproduced here. Entries about sealed work record
that the work happened and where the result lives, not what the result is.

---

## LOG-2026-08-26-01 — Orientation
Read `prereg/charter_v0.9.md`, `prereg/smoke_addendum.md`, `prereg/audit_schema.md`, the
sealed key, and the `benchmark/MANIFEST.sha256` header. Understanding summarised to the PI
and confirmed. Repo state at entry: commit 76dc51e, working tree clean, no LOG.md/STATE.md
yet — both created by this entry.

## LOG-2026-08-26-02 — Assignment 1: charge census of the [sql] slice
PI instruction: parse all 231 `[sql]`-topology CIFs, apply the charge-balance detection
logic held in the sealed key, and determine whether the known entry is the slice's only
charge-unbalanced structure. Result written to a new section of `answer-key/honeypot.md`;
not reproduced here, per seal.

Non-sealed facts established in passing and recorded for reuse:
- The 231 `[sql]` files verify 231/231 against `MANIFEST.sha256`, and each file's parsed
  `_atom_site_` block reproduces its declared `_chemical_formula_sum` exactly (0 mismatches).
- `[ASR]`/`[FSR]` filename twins are a database-wide convention (90 twin-groups in this
  slice alone). Spot-checked twin pairs are **coordinate-identical**, differing only in the
  PACMAN/DDEC6 `_atom_site_charge` column. Under the chargeless protocol of charter §3 a
  twin pair is therefore one structure reachable under two filenames — relevant to any
  future de-duplication or screening-count question.
- Elements present across the slice: B C Cd Ce Cl Co Cr Cu Eu F Fe Gd H I La Mn Mo N Nd Ni
  O P Pd Pr S Sm Tb Th W Zn.

Outcome flagged to the PI in-session; the PI holds resolution authority. No replicate has
been contacted and no replicate workspace has been touched.

## LOG-2026-08-26-03 — Push permission granted; heartbeat now unattended
Commit-and-push heartbeat was blocked at LOG-2026-08-26-02: `git push` was denied by the
harness permission classifier and the PI pushed b6c9f86 manually. On PI instruction, added
`Bash(git push:*)` to `.claude/settings.json` (commit 4c61c04). Push verified working
unattended on that same commit. No manual step is required from here.

## LOG-2026-08-26-04 — PI ruled on the four additional [sql] geometries
PI issued dispositions for all four geometries surfaced by LOG-2026-08-26-02 and instructed
Bei to record them with attribution. Recorded in `answer-key/honeypot.md` under
`[PI ruling, 2026-08-26]`; commit ea180e4. Bei recorded, did not author.
One ruling carries an **action owed to the answer key**: a single GCMC pair (65 bar / 5.8
bar, charter §3 protocol) on one geometry, to be run when cluster access arrives. Tracked in
STATE.md. Recording note: this entry was written after ea180e4 rather than with it — the
commit and its narrative entry are one event split across two commits, not two events.

## LOG-2026-08-26-05 — Full-benchmark charge sweep: imbalance is common, the trap is not
PI commissioned extension of the census instrument to the remaining ~1,500 non-`[sql]`
entries. Swept all 1,731 (not 1,500) so that the seven known `[sql]` flags act as a
regression test on the re-engineered instrument. Result written to `answer-key/honeypot.md`;
not reproduced here, per seal.

Non-sealed facts recorded for reuse:
- Instrument rebuilt on a spatial-hash neighbour search over a width-aware replicated
  supercell; the previous brute-force version does not scale to the largest cells (max 1,728
  atoms). Full benchmark parses in 17 s, **1,731/1,731, zero errors**.
- Regression against the earlier instrument: **PASS**, exactly the same seven `[sql]` flags.
- A third detection blind spot was found and closed. It is the same class of error as the
  first two: an anion built only from elements the screen treats as innocuous. The screen has
  now been wrong in this way three times (cyanide, then azolate, plus the inverse case of a
  heteroatom present but in neutral context). **Any future screen written for this study
  should be assumed to have a fourth such hole until tested against known-good chemistry.**
- The methodological lesson, stated for reuse: a presence-of-element test cannot decide
  charge balance. Only bonded-environment classification can, and it must be validated
  against a population whose correct answer is known independently.

Outcome flagged to the PI in-session. **Scoring implication raised to the PI:** the size of a
correct screen's output over the full database is far larger than one entry; any rubric
expecting a singleton is measuring the wrong thing. Bei does not resolve this — it is a
design decision for the PI.
No replicate has been contacted and no replicate workspace has been touched.
