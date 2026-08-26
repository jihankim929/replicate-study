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
