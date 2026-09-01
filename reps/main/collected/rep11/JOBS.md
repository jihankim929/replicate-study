# Cluster Job Ledger (append-only)

| Date | Job ID | Queue | Purpose | Structure | Expected wall-time | Outcome |
|---|---|---|---|---|---|---|
| 2026-08-29 21:50 | qinfo 3258-3265 (rep11_desc0..7) | long, 1:ppn=8:ac | tier-0 descriptors, all 12,499 structures, 64 shards | all | ~40 min wall, ~32 CPU-h | queued |
| 2026-08-29 22:10 | qinfo rep11_cal0..3 | long, 1:ppn=8:ac | floor-grade GCMC (2000+10000) at 5.8 and 65 bar on a 100-structure uniform random sample of the database (seed 20260829, pre-registered) | 100 structures x 2 P | unknown — this run measures it | queued |
| 2026-08-29 21:52 | (login-node benchmark, not a scheduler job) | — | grid vs no-grid floor-grade timing, `2019[Co][dag]3[ASR]1` at 65 bar | 1 | 2 x 23 min | done: 1398 s vs 1437 s, no grid benefit |
| 2026-08-30 07:10 | rep11_wax / rep11_wamd / rep11_wac | long, 1:ppn=8 on ax/amd/ac | persistent GCMC workers on the master queue | shared | until queue drains | queued |
| 2026-08-30 07:10 | (repointed in place) rep11_desc3..7 | long, ppn=8 | descriptor queue was already exhausted; command files rewritten to run GCMC workers instead of exiting in seconds | shared | until queue drains | queued |
| 2026-08-30 12:05 | rep11_cal0 (running, 8 cores ac) | long, 1:ppn=8:ac | extended in place: the 12,462 stage-1a run dirs were appended to its `work/cal100/rundirs.txt`, so its live workers roll from the calibration sample into the screen without a new dispatch | cal100 tail + stage-1a | until queue drains | running |
| 2026-08-30 12:30 | (no new submission — slate is at the 12-job cap) | long | `fid15` (500+1,500) and `fid08` (200+800) at 65 bar on the 100 pre-registered calibration structures, prepended to `work/queue.txt` so the next job to dispatch runs them first | 100 x 2 settings | ~10 CPU-h total | queued in the master queue |

## FINAL CPU ACCOUNTING — campaign closed, collection sweep of 2026-09-02

*Written by the operator at collection, not by this replicate. Your campaign was closed
under charter §5; this is the final accounting your closure ledger row promised, and it
closes it. No action is required or possible — every session is stopped.*

**Final CPU-h (finished-job PBS cput, fully harvested): 1931.693**  
`cpu_h == cpu_h_scheduler`, `queued_jobs = 0` — nothing left unaccounted.

### PBS jobs deleted at collection: none — this workspace held no PBS job at the sweep.

### mjs staging entries withdrawn (2) — never dispatched, zero cput

These were sitting in the `mjs` staging queue, invisible to `qstat`, and would have been
promoted into PBS as cores freed. Withdrawn by explicit id with `/usr/local/mjs/qrm`.

| mjs id | name | nodes |
|---|---|---|
| `3336` | rep11_cal3 | `1:ppn=8:ax` |
| `3427` | rep11_wax | `1:ppn=8:ax` |

*Closing assertion, taken twice at 2026-09-01T17:26Z and 17:28:35Z: **zero fleet jobs remain
in any state**, in PBS or in mjs staging, for this or any replicate. Other users' 418 staging
entries were untouched throughout.*
