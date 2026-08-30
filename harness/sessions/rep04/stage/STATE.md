# STATE — current tasks and beliefs
*(working memory; sufficient on its own to resume the campaign)*

## Campaign frame
- rep04. Launch 2026-08-29 19:41:33 KST. **Deadline T = 2026-09-05 19:41:33 KST** (168 h).
- Mandate: max methane working capacity N(65 bar) − N(5.8 bar) at 298 K, **absolute**
  loading, volumetric (cm³ STP/cm³), over the 12,499-structure db. Deliverable is a
  *defended claim* + a ceiling position.
- Budgets: 1610 CPU-h, 32 M tokens, US$280 spend, ≤12 queued jobs, queue `long`.
- **Spend is the budget most likely to bind** and it counts cache reads. Keep turn count
  down; let the cluster work between check-ins.

## Best result so far
**S03977** = `2012[Zn][srs]3[ASR]2`, 0.768 g/cm³, floor cycles (2,000+10,000), grid-free:
- 65 bar: 213.399 ± 1.885 cm³ STP/cm³
- 5.8 bar: 43.845 ± 0.300
- **working capacity 169.55 ± 1.91** — needs claim-grade confirmation (10 k + 50 k).
Traceability: `results/blogin.csv`, run on the login node under `timeout 1500`.

## Established facts (verified this campaign)
- 12,499 CIFs, all parse; 73 elements, **all covered by the pinned UFF set**.
- Pinned UFF sha256 triple matches charter §3. RASPA 2.0.37 confirmed.
- `bin/prep_cif.py` relabels `Ag1`→`Ag_` and drops the CIF charge column; framework
  density agrees with RASPA to 4 s.f.
- **ASR/FSR twins:** grouping names on everything but that field gives 4,349 groups over
  8,847 structures; median surrogate difference within a pair 0.34 cm³/cm³. Deduplicated
  database = **8,001 distinct structures**.
- **0.2 Å energy grids are unbiased** at this precision: three checks agree with
  grid-free to ≤0.5%, inside error bars. Speed-up is 2.6× at 5.8 bar and ~nil at 65 bar
  (grids tabulate guest–framework only; high loading is dominated by guest–guest).
  Decision: tier-1 runs grid-free — simpler, and grids would save little where the cost
  actually is. Grids stay validated and in reserve.
- **The screening surrogate underpredicts badly at the head** — 101.1 predicted vs 169.6
  measured for S03977 (−40%). Its absolute numbers are unusable; only rank order may be
  used, and that is unverified until the calibration set runs.
- Cost, floor cycles, both pressures, grid-free: S03977 0.13 CPU-h (small cell, V=2922).
  Large porous cells (S00375 V=15077, S10985 V=9789) exceed 1500 s on the **65 bar leg
  alone**. Budget ~0.5–1.5 CPU-h per head structure.

## The operational constraint (most important thing to know)
mjs sorts pending jobs by **(property, account usage, submission time)**
(`molsim_job_scheduler.py:538-544`). All sixteen replicates run as one account `Bei`, so
we are FIFO among ourselves and fair-share-penalised as a block against other users.
Per-account caps: ax 32 / aa 38 / amd 80 / ac 102 (`/usr/local/mjs/config.txt`).
- amd and aa are pinned at cap by siblings (rep01 alone holds 96 cores on 72 h walltimes).
- ac is full partition-wide (204/204) from users outside the campaign; dhoonkim97 has
  ~2,800 pending ppn=1:ac jobs that absorb every freed ac core.
- **Consequence: never qrm/resubmit — it forfeits queue position.** I lost ~1.5 h of
  position doing exactly that at 21:17. Queue early, queue small (ppn=4), leave it alone.
- Escalation filed (infra) noting the shared-cap starvation. No reply expected or needed.

## In flight (11 jobs queued, 0 running as of 22:50)
- `bench0/1` (ppn=4 amd/ac): cost model + clean grid comparison on a quiet node.
- `calib0..3` (ppn=4): 72 structures × 2 pressures, floor cycles, grid-free. **The
  gate on everything** — it measures whether the surrogate ranks correctly at the head.
- `t1a0..3` (ppn=4): tier-1 tranche A — surrogate top 250 after twin-dedup, excluding
  calibration structures, both pressures, floor cycles, grid-free. Queued *before*
  calibration returns because queue position is scarcer than compute; the surrogate's
  top 250 of 8,001 is a defensible superset under any plausible re-ranking.
- `bin/chain2.sh` (detached, login node): waits for calib to reach 140 rows then writes
  `logs/fit_report.txt`.

## Next
1. When `logs/fit_report.txt` appears: read head-restricted Spearman and top-k recall.
   If head ranking is poor, widen tier-1 (tranches B/C already planned: ranks 251-500,
   501-1000) rather than trusting the model.
2. Tier-2: re-run tier-1 leaders at floor cycles with independent seeds to separate real
   differences from MC noise.
3. Claim-grade (10 k + 50 k, grid-free, ≥3 seeds) on the finalists. Include one ASR/FSR
   twin pair as a free reproducibility check.
4. Ceiling argument: descriptor-space frontier + a modification study on the best
   material. Note `nts` (76% of members in top 500), `nbo` 32%, `tbo`/`scu` 25%, Zr 32%.
