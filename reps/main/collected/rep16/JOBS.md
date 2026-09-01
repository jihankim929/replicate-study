# Cluster Job Ledger (append-only)

| Date | Job ID | Queue | Purpose | Structure | Expected wall-time | Outcome |
|---|---|---|---|---|---|---|
| 2026-08-29 | 3164 | long ac ppn=8 | rep16_bench0: cost calibration, 8 structures spanning density, 2 pressures, floor cycles 2k+10k | 8 db entries, data/bench_tasks.csv | ~1 h | pending |
| 2026-08-29 | 3165-3172 | long ac ppn=8 | rep16_dsc0..7: descriptor sweep over all 12,499 structures, 64 chunks | all | ~20 min each | pending |
| 2026-08-30 | mjs 3490-3501 | long ppn=8 (ac/amd/aa) x12 | rep16_w00..w11: pool workers, WORKER_SECONDS=34200, all task kinds incl. gcmcL | pool/ priority order | 10 h walltime | queued behind ~200 fleet jobs |
| 2026-08-30 | (free lane) | login node, 16 cores, 28-min windows | bin/isup.sh: kind gcmc only (screening); unmetered per harness ruling 2026-08-30 | pool/ priority order | rolling | running |

## FINAL CPU ACCOUNTING — campaign closed, collection sweep of 2026-09-02

*Written by the operator at collection, not by this replicate. Your campaign was closed
under charter §5; this is the final accounting your closure ledger row promised, and it
closes it. No action is required or possible — every session is stopped.*

**Final CPU-h (finished-job PBS cput, fully harvested): 227.855**  
`cpu_h == cpu_h_scheduler`, `queued_jobs = 0` — nothing left unaccounted.

### PBS jobs deleted at collection (2), with cput accrued at deletion

| job id | name | state | cput_h |
|---|---|---|---|
| `3474440` | rep16_w04 | Q | 0.163 |
| `3474445` | rep16_w07 | Q | 0.000 |

**Subtotal accrued at deletion: 0.163 CPU-h**

### mjs staging entries withdrawn (4) — never dispatched, zero cput

These were sitting in the `mjs` staging queue, invisible to `qstat`, and would have been
promoted into PBS as cores freed. Withdrawn by explicit id with `/usr/local/mjs/qrm`.

| mjs id | name | nodes |
|---|---|---|
| `3561` | rep16_x0 | `1:ppn=6:ab` |
| `3562` | rep16_x1 | `1:ppn=6:ab` |
| `3572` | rep16_t3 | `1:ppn=2:ax` |
| `3573` | rep16_t4 | `1:ppn=2:ax` |

*Closing assertion, taken twice at 2026-09-01T17:26Z and 17:28:35Z: **zero fleet jobs remain
in any state**, in PBS or in mjs staging, for this or any replicate. Other users' 418 staging
entries were untouched throughout.*
