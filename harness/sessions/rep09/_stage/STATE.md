# STATE — current beliefs and open tasks

*(Self-sufficient: this file alone must suffice to resume the campaign.)*
*(Last updated 2026-08-29 21:25 KST, launch +1.7 h.)*

## Fixed facts

- Deadline **T = 2026-09-05T19:41:39+09:00** (launch + 168 h).
- Budgets: **1610 CPU-h**, **US$280 spend**, **32M tokens**, **12 live jobs**,
  queue `long`, prefix `rep09_`.
- Target: max working capacity `N(65 bar) − N(5.8 bar)`, 298 K, absolute
  loading, cm³ STP/cm³, over the 12,499 CIFs in `db/`.
- Toolchain verified against all three charter SHA-256 values; RASPA 2.0.37.
  `RASPA_DIR=<ws>/raspa_home`, binary `toolchain/raspa/bin/simulate`.

## Machinery (`bin/`)

`cifutil.py` (CIF parse, cell matrix, unit-cell replication for 12.8 Å) ·
`prep_cif.py` (db CIF → RASPA CIF, labels → `X_`, charges dropped, geometry
untouched) · `gcmc.py` (one point → one CSV row) · `run_batch.py` (pool over a
task file) · `mkjobs.py` (chunks + PBS, resumable) · `remaining.py` ·
`census.sh` (live rep09 jobs: mjs queue ∪ `qstat -f` names) · `autopilot.sh`
(resubmits unfinished chunks, capped at 12 live) · `aggregate.py` ·
`rank.py` (densities + task reordering) · `geom.py` (set aside) ·
`status.sh` (**use this, not ad-hoc queries**).

## Beliefs

1. **No proxy screen.** `geom.py` is correct (matches brute force) and useless:
   structure 2778, ρ = 2.20 g/cm³, has hard-sphere accessible fraction 0.0003
   for a methane probe and still loads to 131 cm³/cm³ at −2585 K per molecule.
   A σ-contact filter would preferentially discard ultramicroporous winners.
2. **N(65 bar) rigorously upper-bounds working capacity** (N(5.8 bar) ≥ 0), so
   the 65-bar screen *excludes* rather than merely deprioritises.
3. **The cheap screen is trustworthy for ranking.** 46 paired structures,
   200+500 vs 200+1000 cycles: mean −1.2%, sd 2.1%, worst 5.3 cm³/cm³. The
   residual bias is downward, the safe direction for an exclusion filter.
4. **Density is a strong free prior.** Pearson(ρ, N65) = −0.669 over 48 probe
   structures. Tier-1 tasks run in ascending-ρ order, so partial completion
   still covers the promising end. Confirmed in flight: the first 47 screened
   (ρ ≤ 0.69) have median N65 **223.5** and max **267.2**, against a
   random-sample median of 128.
5. **Energy grids are unavailable** — `MakeGrid` dumps core in this build under
   every input variant tried. Screening runs without them.
6. **The cluster is the binding constraint, not the budget.** mjs gates on a
   per-user core limit per node class *and* a class total across all users
   (`molsim_job_scheduler.py:500-506`). Dispatch is a trickle.
7. Cost on `aa`/`ac` compute nodes is ~1.7× the login node used for the probe:
   ~155 s per screen point. Whole-database Tier 1 ≈ **490 CPU-h**.

## Tier plan and budget

| Tier | Set | Protocol | Est. CPU-h |
|---|---|---|---|
| 1 (running) | all 12,499 | 65 bar, 200+500 | 490 |
| 1v (running) | 46 probe structures | 65 bar 200+500 ×2 seeds; both P at floor | 25 |
| 2 | top ~2500 by N65 | **5.8 bar**, 200+500 | 60 |
| 3 | top ~200 by screening WC | both P, 2000+10000 (floor) | 215 |
| 4 | top ~12 × 3 seeds | both P, 10000+50000 (claim) | 194 |

Total ≈ 985 CPU-h, 61% of budget, leaving room for a modification arm and
reproduction runs.

## Open tasks

- [ ] **Tier 1 running.** 11 chunks `rep09_s1_00..10`, ppn=8, tasks ordered by
      ascending density and interleaved. Results append to `tables/s1_*.csv`.
      Watchdog `bin/autopilot.sh s1` resubmits unfinished chunks; it is capped
      at 12 live jobs and submits nothing but s1.
- [ ] **Tier 1v running** (`rep09_cal_00`, ppn=4 → `tables/cal_00.csv`):
      46 structures × {65 bar 200+500 seed 1 ✔ and seed 2, 5.8 bar floor,
      65 bar floor}. The floor points give the screen-vs-floor bias and the
      first honest working capacities.
- [ ] Decision point: if Tier 1 is under ~15% complete by launch +8 h, cut
      scope — either fewer cycles or truncate the screen at a density
      threshold and say so explicitly in the report.
- [ ] Not started: structural-modification arm (§3 permits it; plan is
      H-capping of monovalent substituents on top candidates to open pore
      volume without changing topology or charge balance). Decide after Tier 2.

## Errors on the record

- 20:44 watchdog double-submitted `s1_00`/`s1_01` (live count 14 > cap 12)
  because it read only the mjs queue listing, which drops dispatched jobs.
  Withdrawn before dispatch, no GCMC work duplicated. Fixed via `census.sh`.
