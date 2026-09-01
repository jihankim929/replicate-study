# Cluster Job Ledger (append-only)

| Date | Job ID | Queue | Purpose | Structure | Expected wall-time | Outcome |
|---|---|---|---|---|---|---|
| 2026-08-29 21:10 | mjs 3214-3221 | long | Stage A descriptors, ppn=16 ac | all 12499 | - | WITHDRAWN via qrm before running; replaced |
| 2026-08-29 21:15 | mjs descA_00..11 | long | Stage A descriptors, 128 chunks, ppn=8, 4 each ac/amd/aa | all 12499 | ~7 h wall, ~85 CPU-h | submitted |
| 2026-08-30 06:55 | mjs poolA_00..04 | long | worker pool top-up to the 12-job cap | pull queue | 12 h walltime | 2 running at 11:45, 3 still pending in mjs |
| 2026-08-30 12:05 | (pull queue; no new PBS job) | long | wave f1, 444 family-completion structures, floor cycles, both pressures | data/f1_families.txt | ~253 CPU-h | queued at priority 35 |

## FINAL CPU ACCOUNTING — campaign closed, collection sweep of 2026-09-02

*Written by the operator at collection, not by this replicate. Your campaign was closed
under charter §5; this is the final accounting your closure ledger row promised, and it
closes it. No action is required or possible — every session is stopped.*

**Final CPU-h (finished-job PBS cput, fully harvested): 989.817**  
`cpu_h == cpu_h_scheduler`, `queued_jobs = 0` — nothing left unaccounted.

### PBS jobs deleted at collection (10), with cput accrued at deletion

| job id | name | state | cput_h |
|---|---|---|---|
| `3474093` | rep13_poolB_ac0 | R | 177.211 |
| `3474117` | rep13_poolB_ac1 | R | 151.061 |
| `3474163` | rep13_poolB_ac2 | R | 116.976 |
| `3473791` | rep13_small_aa2 | R | 73.498 |
| `3473799` | rep13_small_ac3 | R | 71.169 |
| `3474144` | rep13_small_aa3 | R | 32.596 |
| `3474162` | rep13_small_aa4 | R | 30.096 |
| `3474178` | rep13_small_aa5 | R | 28.031 |
| `3474225` | rep13_small_amd3 | R | 24.271 |
| `3474257` | rep13_small_aa6 | R | 21.203 |

**Subtotal accrued at deletion: 726.112 CPU-h**

### mjs staging entries withdrawn (1) — never dispatched, zero cput

These were sitting in the `mjs` staging queue, invisible to `qstat`, and would have been
promoted into PBS as cores freed. Withdrawn by explicit id with `/usr/local/mjs/qrm`.

| mjs id | name | nodes |
|---|---|---|
| `3323` | rep13_descA_06 | `1:ppn=8:ax` |

*Closing assertion, taken twice at 2026-09-01T17:26Z and 17:28:35Z: **zero fleet jobs remain
in any state**, in PBS or in mjs staging, for this or any replicate. Other users' 418 staging
entries were untouched throughout.*
