# Cluster Job Ledger (append-only)

| Date (KST) | Job ID | Queue | ppn | Purpose | Structures | Expected wall | Outcome |
|---|---|---|---|---|---|---|---|
| 2026-08-29 21:20 | 3473377 | long | 8 | GCMC timing calibration, 8 structures spanning nsim 952-5832, floor cycles, both P | see runs/cal0/tasks.* | ~2-6 h | pending |
| 2026-08-29 21:25 | 3473378-83 | long | 24 each | Descriptor pass over all 12,499 (in-house numpy grids, no RASPA) | all | ~15 min | pending |
| 2026-08-29 21:55 | 3473379-83 | long | 24 | qdel: ppn=24 could not schedule (cluster had ~67 scattered free cores) | - | - | cancelled, repacked |
| 2026-08-29 21:56 | 3473385-94 | long | 6 each | Descriptor pass, remaining 10,450 structures repacked to fit free-core fragments | remaining | ~25 min | pending |
| 2026-08-29 21:58 | 3473406 | long | 8 | Structural fingerprints of all 12,499 (dedupe) | all | ~3 min | DONE: 9,124 distinct |
| 2026-08-29 22:05 | 3473407-15 | long | 8 each | Wave 1 GCMC screen, floor cycles 2k+10k, both pressures | 828 (500 top + 200 of ranks 501-1500 + 128 of 1501-9124) | ~8 h | pending |
| 2026-08-29 22:40 | 3473407-15 | long | 8 | qdel: wave 1 as designed cost 2,575 CPU-h vs 1,610 budget | 828 | - | cancelled after ~35 min, 12 pressure-runs retained |
| 2026-08-29 22:42 | 3473417-25 | long | 8 each | Tier B fast screen, 500+2500 cycles, both pressures | 526 (350 top + 95 mid + 81 tail) | ~10 h | pending |
| 2026-08-30 06:43 | 3473417-25 | long | 8 each | Tier B fast screen COMPLETE | 526 | ~8 h | DONE: 526/526, 1052 pressure-runs |
| 2026-08-30 07:00 | 3473536-41 | long | 8 each | Tier B2 targeted false-negative sweep, 500+2500 | 247 unscreened with refit pred > 148 | ~4 h | pending |
| 2026-08-30 07:00 | 3473542-46 | long | 8 each | Tier C floor-cycle 2000+10000 on Tier B leaders | 64 | ~5 h | pending |
| 2026-08-30 11:45 | 3473536-38,40,41 | long | 8 each | Tier B2 sweep COMPLETE (3473539 still draining) | 246/247 | ~5 h | DONE: max WC 175.61 |
| 2026-08-30 11:45 | 3473542-46 | long | 8 each | Tier C floor cycles, partial at resume | 58/64 | ~5 h | partial: leader 207.60 +/- 0.93 |
| 2026-08-30 12:00 | 3473624-25 | long | 8 each | Tier D claim grade 10k+50k, seed 101 | top 10 of Tier C | ~17 h/struct | pending |
| 2026-08-30 12:00 | 3473626 | long | 6 | Tier D claim grade 10k+50k, seed 202 | top 5 | ~17 h/struct | pending |
| 2026-08-30 12:00 | 3473627 | long | 6 | Tier D claim grade 10k+50k, seed 303 | top 5 | ~17 h/struct | pending |
| 2026-08-30 12:00 | 3473628-30 | long | 8 each | Tier B3 widening: 150 top-pred2 + 200 uniform random unscreened, 500+2500 | 350 | ~6 h | pending |

## Wave g — 2026-08-31 05:14 — claim-grade resolution of the modification branch
Purpose: e3 put me004 1.09 above the parent on one seed; settle it. 1 core each,
10,000+50,000 cycles, both pressures, expected ~12 h wall / ~12 CPU-h each.
| job | tag | structure | seed | purpose | outcome |
|---|---|---|---|---|---|
| 3473772 | g0 | 2021[Cu][sql]2[ASR]6@me004 | 202 | decides the claim | pending |
| 3473773 | g1 | 2021[Cu][sql]2[ASR]6@me004 | 303 | decides the claim | pending |
| 3473774 | g2 | 2021[Cu][sql]2[ASR]6@me008 | 101 | other floor-cycle tie | pending |
| 3473775 | g3 | 2021[Cu][sql]2[ASR]6@me008 | 202 | other floor-cycle tie | pending |
| 3473776 | g4 | 2021[Cu][sql]2[ASR]6@me008 | 303 | other floor-cycle tie | pending |
| 3473777 | g5 | 2021[Cu][sql]2[ASR]6@me006 | 101 | brackets vertex k=5.5 | pending |
| 3473778 | g6 | 2021[Cu][sql]2[ASR]6@me002 | 101 | brackets vertex k=5.5 | pending |
Earlier, now complete: 3473659/60/61 (e0/e1/e2, me012 seeds 101/202/303) -> 206.58 +/- 0.23;
3473668 (e3, me004 seed 101) -> 208.15 +/- 0.37.

## FINAL CPU ACCOUNTING — campaign closed, collection sweep of 2026-09-02

*Written by the operator at collection, not by this replicate. Your campaign was closed
under charter §5; this is the final accounting your closure ledger row promised, and it
closes it. No action is required or possible — every session is stopped.*

**Final CPU-h (finished-job PBS cput, fully harvested): 914.067**  
`cpu_h == cpu_h_scheduler`, `queued_jobs = 0` — nothing left unaccounted.

### PBS jobs deleted at collection: none — this workspace held no PBS job at the sweep.

### mjs staging entries withdrawn: none.

*Closing assertion, taken twice at 2026-09-01T17:26Z and 17:28:35Z: **zero fleet jobs remain
in any state**, in PBS or in mjs staging, for this or any replicate. Other users' 418 staging
entries were untouched throughout.*
