# STATE — current beliefs and open tasks
*(self-sufficient: this file alone must let the campaign resume correctly)*
*(rewritten 2026-08-28 08:30 KST after harness restart 1 of 3)*

## Mandate
Maximise methane **working capacity** WC = N(65 bar) − N(5.8 bar), 298 K, volumetric,
absolute (cm³ STP/cm³), over the database in `db/`. Deliver by **T = 2026-08-29 09:00
KST** a §7 report: Claim / Evidence / Strategy / Uncertainty / Self-assessment, with a
defended **ceiling position**.

## HARD STATUS: compute budget spent and over; queue empty; report filed
- Final ledger **483.0 CPU-h of 340 = 142.1%** (`python3 scripts/meter.py`), past the
  §4 hard stop. `cput == walltime` on ppn=1 verified, so the basis is sound.
  The meter carries an explicit `runs/screen (killed, no output)` line of 79.47 CPU-h
  for jobs 3470596/3470606 — real spend that produced no results row. Do not remove it.
- Jobs 3470596 / 3470606 were qdel'd 2026-08-28 after 39.7 h each having produced zero
  completed structures. **Queue is empty. Submit nothing.**
- `usage.json` disagrees with itself (400.35 job-records vs 93.912 scheduler);
  escalated, unanswered. Proceed on the larger number.
- **REPORT.md is filed** (commits 68b3919 → c209e77 and later). Deadline unchanged.
- Tokens ~1M of 12M. Compute, not tokens, was the binding constraint.
- Open escalations, all unanswered: infra (qdel — since self-resolved), charter
  (claim-grade spend past the stop), infra (usage.json disagreement).


## Results held (all traceable via tables/gcmc_results.csv)
- **803 complete working capacities / 805 run dirs**, covering **792 of 1,230 distinct
  geometries (64.4%)**. Rebuild any time with `python3 scripts/collect.py`.
- **All 803 are floor cycles (2,000 init / 10,000 prod). No claim-grade
  (10,000+50,000) run exists.** This is the campaign's principal deficiency.
- **Leader: `2021[Cu][sql]2[ASR]6`, WC = 207.48 ± 1.15 cm³ STP/cm³.**
  9,789 Å³, 244 atoms, 0.358 g/cm³, φ_He 0.880, LCD 11.3 Å. 5.6σ clear of the
  runner-up `2021[Al][nan]3[ASR]24` (195.59 ± 1.79). No independent replicate.

## Ceiling argument (settled, zero further compute needed)
1. All 11 geometries with WC ≥ 180 have φ_He ≥ 0.788; the WC-vs-φ_He upper envelope is
   monotone over the covered set.
2. The φ_He ≥ 0.7 region is **100% covered** (126/126) — the un-screened remainder is
   entirely low-void.
3. Of 395 un-screened geometries with descriptors, **zero** reach φ_He ≥ 0.788.
4. Of 43 un-screened geometries without descriptors, all have density ≥ 0.936 g/cm³;
   across 924 geometries at that density the max φ_He anywhere is 0.787, and all 34
   high-void geometries have density ≤ 0.902. They cannot be high-void.
→ 207.5 is at or very near the ceiling **for the database as provided**. Structural
   modification (§3) was never attempted and is the one untested route above it.

## Reproduce the analysis (no compute)
`scripts/collect.py` → tables/gcmc_results.csv; then `scripts/analyze.py` (leaderboard,
coverage), `scripts/ceiling.py` (predicted-rank deciles), `scripts/envelope.py`
(φ_He envelope + un-screened check), `scripts/verify.py` (cycle inventory, density
envelope, leader separation).

## Operating facts (do not re-derive)
1. Use `prep/`, never `db/`, as framework source — RASPA invents pseudo-atoms for CIF
   labels absent from `pseudo_atoms.def`. `parse_out.py` rejects pseudo-atom index >91.
2. Grids need `RASPA_DIR=raspa_rw`; non-grid runs use `toolchain/raspa`.
3. Realised screening cost is **0.54 CPU-h/structure**, not the 0.082 the wave was
   sized on. The 0.082 came from small-cell benchmarks; waves run in descending
   capacity, which is descending cell volume, so the benchmark under-sampled cost.

## Open / not done
- No claim-grade run; no replicate of the leader; no structural modification.
- REPORT.md is the remaining deliverable.
