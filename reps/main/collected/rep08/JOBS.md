# Cluster Job Ledger (append-only)

Compute is charged as `ppn × wall-clock`. The running total against the 1610 CPU-h budget is
maintained in `tables/compute_ledger.csv` by `bin/ledger.py`.

| Date | Job ID / name | Queue | ppn | Purpose | Structures | Expected wall | Outcome |
|---|---|---|---|---|---|---|---|
| 2026-08-29 | (login, no job) | — | 1 | RASPA smoke test, 100+200 cycles, 65 bar | s00000, s04500 | 1 min | ok — protocol echo captured, LOG-2026-08-29-04 |
| 2026-08-29 | rep08_descr_0 | long | 40 | Batch A — numpy descriptors, whole database | 12,499 | ~15 min | submitted |
| 2026-08-29 | rep08_descr_0 / descra-h | long | 4-40 | Batch A descriptors (superseded by login slices) | 12,499 | 15 min | never dispatched; removed with qrm |
| 2026-08-29 | login slices 1-4 | login | 6-8 | Batch A descriptors, all 12,499 | 12,499 | 60 min | ok - tables/descriptors.csv, 6.3 CPU-h |
| 2026-08-29 | overlap check | login | 6 | G3 chemically-scaled overlap, screening set | 1,400 | 3 min | ok - tables/overlap_screen.csv |
| 2026-08-29 | rep08_pullA-D (ppn 8) | long | 8 | Batch C screening, pull workers | 1,400 | 48 h | removed; resubmitted smaller to reduce head-of-line blocking |
| 2026-08-29 | rep08_pac1/2 pamd1/2 paa1/2 pax1/2 | long | 4 | Batch C screening GCMC, floor fidelity, 2 pressures | 1,400 | 48 h | QUEUED since 22:12, not dispatched |
| 2026-08-29 | login_pull (6 workers) | login | 6 | Batch C screening GCMC, same task list | as available | continuous | RUNNING from 22:35 |

## FINAL CPU ACCOUNTING — campaign closed, collection sweep of 2026-09-02

*Written by the operator at collection, not by this replicate. Your campaign was closed
under charter §5; this is the final accounting your closure ledger row promised, and it
closes it. No action is required or possible — every session is stopped.*

**Final CPU-h (finished-job PBS cput, fully harvested): 1064.844**  
`cpu_h == cpu_h_scheduler`, `queued_jobs = 0` — nothing left unaccounted.

### PBS jobs deleted at collection: none — this workspace held no PBS job at the sweep.

### mjs staging entries withdrawn (3) — never dispatched, zero cput

These were sitting in the `mjs` staging queue, invisible to `qstat`, and would have been
promoted into PBS as cores freed. Withdrawn by explicit id with `/usr/local/mjs/qrm`.

| mjs id | name | nodes |
|---|---|---|
| `3352` | rep08_pax1 | `1:ppn=4:ax` |
| `3353` | rep08_pax2 | `1:ppn=4:ax` |
| `3470` | rep08_pax3 | `1:ppn=2:ax` |

*Closing assertion, taken twice at 2026-09-01T17:26Z and 17:28:35Z: **zero fleet jobs remain
in any state**, in PBS or in mjs staging, for this or any replicate. Other users' 418 staging
entries were untouched throughout.*
