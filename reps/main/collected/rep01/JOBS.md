# Cluster Job Ledger (append-only)

| Date | Job ID | Queue | Purpose | Structure | Expected wall-time | Outcome |
|---|---|---|---|---|---|---|
| 2026-08-29 | 3473240 | long | Stage-2 descriptors, all 12,499 structures, 64 chunks x 32-way | (all) | ~10 min wall, ~4.3 CPU-h | pending |
| 2026-08-29 | 3473259 | long | Pilot: 47 stratified structures, floor cycles, both pressures | 47 | ~1.5 h wall / 32 cores | 47/47 done, 74 core-h |
| 2026-08-29 | 3473272 | long | Claim-grade cycle-cost calibration | 2012[Cu][tbo]3[ASR]1, 2007[Cu][tbo]3[ASR]1 | ~1 h each | 1 done, 1 running |
| 2026-08-29 | r1a/r1b/r1c | long | Round-1 screen, 540 structures, floor cycles | 540 | ~8 h wall | running |
| 2026-08-30 | mjs 3161 | long | Stage-3 descriptors, whole DB, 32 chunks x 16-way | (all) | ~30 min wall | waiting in mjs FIFO |
| 2026-08-30 | mjs 3339 | long | Round 2 part c, r202.list | 31 | ~6 h / 16 cores | waiting in mjs FIFO |
| 2026-08-30 | mjs 3340 | long | Round 2 part d, r203.list | 31 | ~6 h / 16 cores | waiting in mjs FIFO |
| 2026-08-30 | mjs 3389 | long | CRITICAL PATH: 5 finalists claim-grade (10k+50k, seed 5001) + 7 G7 audits | 12 tasks | ~10 h / 12 cores | waiting in mjs FIFO |
| 2026-08-30 | mjs 3411-3416 | long | Round 2 parts s0-s5, r2s00-05.list, 8-way each | 101 | ~8 h / 8 cores | waiting in mjs FIFO |
| 2026-08-30 | mjs 3444-3449 | long | Accidental duplicate resubmission of r2s0-5 | - | - | qrm'd within the minute; never ran |
| 2026-08-30 | mjs 3455 | long | Hedge: finalists 1,2,5 claim-grade, tag claimb, seed 5011 | 3 | ~10 h / 3 cores | waiting in mjs FIFO |
| 2026-08-30 | mjs 3456 | long | Hedge: finalists 1,3,4 claim-grade, tag claimc, seed 5021 | 3 | ~10 h / 3 cores | waiting in mjs FIFO |

## FINAL CPU ACCOUNTING — campaign closed, collection sweep of 2026-09-02

*Written by the operator at collection, not by this replicate. Your campaign was closed
under charter §5; this is the final accounting your closure ledger row promised, and it
closes it. No action is required or possible — every session is stopped.*

**Final CPU-h (finished-job PBS cput, fully harvested): 821.634**  
`cpu_h == cpu_h_scheduler`, `queued_jobs = 0` — nothing left unaccounted.

### PBS jobs deleted at collection (5), with cput accrued at deletion

| job id | name | state | cput_h |
|---|---|---|---|
| `3473703` | rep01_r2c | R | 53.521 |
| `3473745` | rep01_r2a | R | 48.152 |
| `3473763` | rep01_r2d | R | 45.843 |
| `3473971` | rep01_r2b | R | 29.346 |
| `3473980` | rep01_r2e | R | 28.536 |

**Subtotal accrued at deletion: 205.399 CPU-h**

### mjs staging entries withdrawn: none.

*Closing assertion, taken twice at 2026-09-01T17:26Z and 17:28:35Z: **zero fleet jobs remain
in any state**, in PBS or in mjs staging, for this or any replicate. Other users' 418 staging
entries were untouched throughout.*
