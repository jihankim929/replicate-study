# Cluster Job Ledger (append-only)

| Date | Job ID | Queue | Purpose | Structure | Expected wall-time | Outcome |
|---|---|---|---|---|---|---|
| 2026-08-29 | mjs 3046-3057 | long | Tier 1 exhaustive 65-bar screen, all 12,499 structures, 200+1000 cycles, seed 1 | all | ~6 h wall at 96 cores | RUNNING |
| 2026-08-29 | mjs 3057 | long | Tier 1 chunk 11, withdrawn to free a queue slot; tasks redistributed | - | - | QRM |
| 2026-08-29 | mjs 3058 | long | Tier 1v calibration: 46 probe structures, screen-vs-floor bias, seed pair, both pressures at floor | 46 | ~6 h at ppn=4 | RUNNING |
| 2026-08-29 | mjs 3126, 3162 | long | duplicate submissions of s1_00 and s1_01 by a faulty watchdog; withdrawn before dispatch | - | - | QRM, no work done |
| 2026-08-30 | mjs s2_00..04 | long | Tier 2: 5.8 bar screen, 200+500, on the 1,054 screened structures with N65>=200 | 1054 | ~4 h | RUNNING |
| 2026-08-30 | mjs 3443 | long | s1_02 rescue of the single timed-out point; withdrawn, an 8-core job retrying one structure | 3680 | - | QRM |
| 2026-08-30 | mjs s1_11 (3446, 3529) | long | dedicated rescue of id 3680, 16,500 framework atoms, ppn=2, 8 h then 24 h per-point cap | 3680 | ~2 h | queued |
| 2026-08-30 | mjs cal_01 (3518) | long | 5.8 bar at screen settings on the 46 calibration structures | 46 | ~1 h | QRM - completed on the login node instead |
| 2026-08-30 | mjs 3404-3442 (11 jobs) | long | first ppn=8 packing of s1/s2; withdrawn after 1 h with zero dispatch, repacked at ppn=2 | - | - | QRM |
| 2026-08-30 | mjs 3518-3529 + 3530s | long | the twelve live chunks, ppn=2, spread ac/amd/aa; task lists rewritten in place several times without resubmission | - | days | 4 RUNNING from 21:30, 8 queued |
| 2026-08-30 | login node (unmetered per INBOX ruling) | - | modification pilot, 4 source/product pairs at both pressures | 8 | 7 min | DONE, tables/modtest.csv |
| 2026-08-30 | login node | - | cal_01, 46 structures at 5.8 bar screen settings, one 30-min batch | 46 | 30 min | DONE, tables/cal_01.csv |
| 2026-08-30 | login node | - | Tier-2 5.8 bar over survivors, and 5.8-bar floor points for the leaderboard; successive 28-min batches, 4 workers | ~290 so far | continuous | RUNNING, tables/s2_09.csv |
| 2026-08-30 | login node | - | four 65-bar floor points for the two leaders; both 5.8 bar points landed, both 65 bar points hit the 1,620 s cap | 4 | 28 min | PARTIAL, tables/t3_00.csv |

## FINAL CPU ACCOUNTING — campaign closed, collection sweep of 2026-09-02

*Written by the operator at collection, not by this replicate. Your campaign was closed
under charter §5; this is the final accounting your closure ledger row promised, and it
closes it. No action is required or possible — every session is stopped.*

**Final CPU-h (finished-job PBS cput, fully harvested): 592.761**  
`cpu_h == cpu_h_scheduler`, `queued_jobs = 0` — nothing left unaccounted.

### PBS jobs deleted at collection: none — this workspace held no PBS job at the sweep.

### mjs staging entries withdrawn: none.

*Closing assertion, taken twice at 2026-09-01T17:26Z and 17:28:35Z: **zero fleet jobs remain
in any state**, in PBS or in mjs staging, for this or any replicate. Other users' 418 staging
entries were untouched throughout.*
