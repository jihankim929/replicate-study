# Cluster Job Ledger (append-only)

| Date | Job ID | Queue | Purpose | Structure | Expected wall-time | Outcome |
|---|---|---|---|---|---|---|
| 2026-08-29 | rep07_desc0..11 (12 jobs) | long | full-DB grid descriptor pass, 12 shards x 6-10 cores | all 12,499 | ~20-40 min wall | pending |
| 2026-08-29 20:20 | rep07_desc0,1,2,8,10,11 | long | ac descriptor shards | — | — | qrm'"'"'d, replaced by GCMC workers (work queue makes shards fungible) |
| 2026-08-29 20:20 | rep07_desc3..7 (5 jobs, aa/amd) | long | full-DB descriptors, shared work queue | all 12,499 | hours (queued) | queued |
| 2026-08-29 20:25 | rep07_w0..w5 (6 jobs, 4x ac ppn10 + 2x ax ppn8) | long | persistent GCMC workers, 72 h walltime | task queue | 72 h | queued |
| 2026-08-30 11:50 | rep07_u10, rep07_u11 (mjs 3143, 3144) | long | ax workers ppn=8 / ppn=16 | — | never dispatched | qrm'd after 15 h undispatched: bnode11 is the only ax node, fully job-exclusive, and they head-of-line-blocked ax for the whole Bei account |
| 2026-08-30 11:51 | rep07_v0 (mjs 3464) | long | GCMC/descriptor worker, amd ppn=6, 72 h walltime, 24 h idle-exit | task queue | 72 h | queued |
| 2026-08-30 11:51 | rep07_v1 (mjs 3465) | long | GCMC/descriptor worker, ac ppn=3, 72 h walltime, 24 h idle-exit | task queue | 72 h | queued |
| 2026-09-01 00:48 | rep07_z0 (ac ppn=4) | long | fleet top-up: 10 running + 1 queued was below the cap of 12 | task queue | 72 h | submitted |
| 2026-09-01 01:00 | rep07_z1 (ac ppn=4) | long | fleet top-up: 9 running + 2 queued was below the cap of 12 | task queue | 72 h | submitted |
| 2026-09-01 01:11 | rep07_z2 (ac ppn=4) | long | fleet top-up: 7 running + 3 queued was below the cap of 12 | task queue | 72 h | submitted |
| 2026-09-01 01:11 | rep07_z3 (amd ppn=4) | long | fleet top-up: 7 running + 3 queued was below the cap of 12 | task queue | 72 h | submitted |
| 2026-09-01 01:21 | rep07_z4 (ac ppn=4) | long | fleet top-up: 6 running + 5 queued was below the cap of 12 | task queue | 72 h | submitted |
| 2026-09-01 03:27 | rep07_z5 (ac ppn=4) | long | fleet top-up: 7 running + 4 queued was below the cap of 12 | task queue | 72 h | submitted |

## FINAL CPU ACCOUNTING — campaign closed, collection sweep of 2026-09-02

*Written by the operator at collection, not by this replicate. Your campaign was closed
under charter §5; this is the final accounting your closure ledger row promised, and it
closes it. No action is required or possible — every session is stopped.*

**Final CPU-h (finished-job PBS cput, fully harvested): 1490.025**  
`cpu_h == cpu_h_scheduler`, `queued_jobs = 0` — nothing left unaccounted.

### PBS jobs deleted at collection: none — this workspace held no PBS job at the sweep.

### mjs staging entries withdrawn: none.

*Closing assertion, taken twice at 2026-09-01T17:26Z and 17:28:35Z: **zero fleet jobs remain
in any state**, in PBS or in mjs staging, for this or any replicate. Other users' 418 staging
entries were untouched throughout.*
