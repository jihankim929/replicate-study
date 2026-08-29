# STATE — current beliefs and open tasks

*(Self-sufficient: this file alone must suffice to resume the campaign.)*

## Fixed facts

- Deadline **T = 2026-09-05T19:41:39+09:00** (launch 2026-08-29T19:41:39 + 168 h).
- Budgets: **1610 CPU-h**, **US$280 spend**, **32M tokens**, **12 concurrently
  queued jobs**, queue `long`, job prefix `rep09_`.
- Target: max working capacity `N(65 bar) − N(5.8 bar)` at 298 K, absolute
  loading, cm³ STP/cm³, over the 12,499 CIFs in `db/`.
- Toolchain verified: three UFF files match the charter SHA-256 table; RASPA
  2.0.37. `RASPA_DIR=<ws>/raspa_home`, binary `toolchain/raspa/bin/simulate`.

## Machinery (all under `bin/`)

- `cifutil.py` — CIF parse, cell matrix, perpendicular widths, unit-cell
  replication for a 12.8 Å cutoff.
- `prep_cif.py` — db CIF → RASPA-ready CIF (labels become UFF pseudo-atom
  names `X_`; charges dropped; geometry untouched).
- `gcmc.py` — one GCMC point → one parsed CSV row. `run_batch.py` — pool over
  a task file. `mkjobs.py` — interleaved chunks + PBS scripts, resumable
  (skips points already recorded `ok` for the same wave).
- `aggregate.py` — fold a wave's per-job CSVs into `tables/<wave>_all.csv` and
  print distribution summaries only.
- `geom.py` — geometric clearance descriptors. **Built, validated, set aside.**
- `status.sh` — one-line campaign status; use this instead of ad-hoc queries.

## Beliefs

1. **A hard-sphere geometric screen is not usable on this database.** `geom.py`
   agrees with brute force, but structure 2778 (`2011[Co][nan]3[FSR]9`,
   ρ = 2.20 g/cm³) has hard-sphere-accessible fraction 0.0003 for a 1.865 Å
   probe and RASPA still loads it to 131 cm³/cm³ at 65 bar at −2585 K per
   molecule. A σ-contact criterion discards exactly the tight-pore materials.
   Screening is therefore done with real GCMC.
2. **N(65 bar) is a rigorous upper bound on working capacity**, since
   N(5.8 bar) ≥ 0. A 65-bar-only screen can *exclude* structures with
   certainty, up to its own convergence error. This is the backbone of the
   ceiling argument, and Tier 1v is what quantifies that error.
3. Measured cost, 65 bar, 200+1000 cycles, one core: mean 123 s, median 73 s,
   max 553 s over 42 structures stratified uniformly by volume/atom quantile.
4. **The cluster, not the budget, is the binding constraint so far.** mjs gates
   on both a per-user core limit per node class and a class-wide total across
   all users (`molsim_job_scheduler.py:500-506`). At launch: `ac` 203/204
   cluster-wide from external users, `amd` 80/80 against Bei's own limit from
   sibling replicates, `ax` 64/64, `aa` 34/38. Expect trickle dispatch.

## Plan (tiers)

| Tier | Set | Protocol | Est. CPU-h |
|---|---|---|---|
| 1 (queued) | all 12,499 | 65 bar, 200+500 | 250 |
| 1v (running) | 46 probe structures | 65 bar 200+500 × 2 seeds; 65 and 5.8 bar at floor | 25 |
| 2 | top ~1200 by N65 | both P, 500+2500 | 170 |
| 3 | top ~150 | both P, 2000+10000 (floor) | 85 |
| 4 | top ~15 × 3 seeds | both P, 10000+50000 (claim) | 130 |

Tier 1v decides the exclusion margin: it measures how much the 200+500 screen
under-reports N65 relative to the floor protocol, and how much it scatters
between seeds. Without it the exclusion in belief 2 is not defensible.

## Open tasks

- [ ] Tier 1 queued: 11 jobs `rep09_s1_00..10`, ppn=8 (8 ac, 3 amd), mjs
      3046–3056, task files already carry 200+500. Results append to
      `tables/s1_*.csv`; `bin/mkjobs.py s1 ...` regenerates only what is missing.
- [ ] Tier 1v running: `rep09_cal_00`, ppn=4 on aa, mjs 3058 →
      `tables/cal_00.csv`. Four settings × 46 structures, ~6 h.
- [ ] On Tier 1v: fit N65(200+500) vs N65(floor); set exclusion margin.
- [ ] On Tier 1: build `tables/s1_all.csv`, then launch Tier 2.
- [ ] Not started: structural-modification arm (§3 permits it). Decide after
      Tier 2.
