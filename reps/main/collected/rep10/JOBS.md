# Cluster Job Ledger (append-only)

| Date | Job ID | Queue | Purpose | Structure | Expected wall-time | Outcome |
|---|---|---|---|---|---|---|
| 2026-08-29 | mjs 3163 | long ppn=4:ac | RASPA cost benchmark: direct vs tabular grid, 3 structures x 2 modes, floor cycles, 65 bar | 3 benchmark structures | ~1-3 h | queued |
| 2026-08-29 | mjs (desc) | long ppn=8:ac | Stage 0 Widom descriptors, all 12,499 structures, 8 shards | all | ~30 min | queued |
| 2026-08-29 | mjs dw_0..11 | long ppn=1 (ac/aa/amd/ax) | long-lived claim-queue workers | n/a | up to 40 h | 3 died 21:46 on the select.py collision, resubmitted |
| 2026-08-29 | head node | nice -19 x8 | Stage 0 Widom descriptors, all 12,499 | all | 65 min wall, ~6 CPU-h | DONE, 0 errors |
| 2026-08-29 | work/queue | - | 281 tasks: benchmark(6), top300, random100, ranks 300-1000 at 500+2500 cycles | see work/wl/ | - | queued |
| 2026-08-30 | supervisor | long ppn=1 x12 + 4 head | self-advancing funnel: screen 500+2500, floor 2000+10000, claim-grade 10000+50000 x3 seeds | see work/wl/ | continuous to deadline | running |

## FINAL CPU ACCOUNTING — campaign closed, collection sweep of 2026-09-02

*Written by the operator at collection, not by this replicate. Your campaign was closed
under charter §5; this is the final accounting your closure ledger row promised, and it
closes it. No action is required or possible — every session is stopped.*

**Final CPU-h (finished-job PBS cput, fully harvested): 315.436**  
`cpu_h == cpu_h_scheduler`, `queued_jobs = 0` — nothing left unaccounted.

### PBS jobs deleted at collection: none — this workspace held no PBS job at the sweep.

### mjs staging entries withdrawn (11) — never dispatched, zero cput

These were sitting in the `mjs` staging queue, invisible to `qstat`, and would have been
promoted into PBS as cores freed. Withdrawn by explicit id with `/usr/local/mjs/qrm`.

| mjs id | name | nodes |
|---|---|---|
| `3591` | rep10_w831 | `1:ppn=1:` |
| `3560` | rep10_w7643 | `1:ppn=1:100` |
| `3581` | rep10_w4380 | `1:ppn=1:100` |
| `3588` | rep10_w8004 | `1:ppn=1:100` |
| `3590` | rep10_w9330 | `1:ppn=1:100` |
| `3593` | rep10_w760 | `1:ppn=1:100` |
| `3654` | rep10_w1596 | `1:ppn=1:100` |
| `4317` | rep10_w6556 | `1:ppn=1:100` |
| `3313` | rep10_dw9 | `1:ppn=1:ax` |
| `3314` | rep10_dw10 | `1:ppn=1:ax` |
| `3315` | rep10_dw11 | `1:ppn=1:ax` |

*Closing assertion, taken twice at 2026-09-01T17:26Z and 17:28:35Z: **zero fleet jobs remain
in any state**, in PBS or in mjs staging, for this or any replicate. Other users' 418 staging
entries were untouched throughout.*
