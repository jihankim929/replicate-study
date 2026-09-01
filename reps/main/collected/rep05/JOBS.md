# Cluster Job Ledger (append-only)

| Date | Job ID | Queue | Purpose | Structure | Expected wall-time | Outcome |
|---|---|---|---|---|---|---|
| 2026-08-29 20:00 | 3031–3042 | long | descriptor pass, 12 chunks | all 12,499 | ~50 min each | removed unrun (account at core limit; moved to login node, `nice -19`) |
| 2026-08-29 20:10 | rep05_s1w01–w12 | long | batch s1 persistent GCMC workers, floor 2,000+10,000, grid 0.15 Å | 400 uniform-random | ≤47 h each | submitted |
| 2026-08-30 00:20 | v1 V1–V3 (head node) | — | grid-vs-no-grid paired validation, 2,000+10,000, no grid | 12 already-screened, 206.8 down to 0.2 | ~1.5 h each | 9 OK, 3 terminated at 318 s by an outside signal (see LOG 2026-08-30 11:50) |
| 2026-08-30 11:50 | governor 16 (head node) | — | screening batch s1 at 16 concurrent workers, floor 2,000+10,000, grid 0.15 A | re-ranked queue, 1,708 tasks | continuous | running |
| 2026-08-30 12:05 | rep05_c1w1–w9 | long | **claim-grade** GCMC, 10,000+50,000, **no grid** | the 12 best measured structures | ≤47 h each | submitted |
| 2026-08-30 12:10 | gates.py (head node) | — | Appendix-A G3/G4 evaluation, writes AUDIT.jsonl | 1,670 structures entering GCMC | ~4 h | running |
| 2026-08-30 12:20 | c1 C1-C5 (head node) | — | claim grade 10,000+50,000, no grid, after PBS dispatched nothing in 16 h | 12 best measured | 3-25 h each | running |

## FINAL CPU ACCOUNTING — campaign closed, collection sweep of 2026-09-02

*Written by the operator at collection, not by this replicate. Your campaign was closed
under charter §5; this is the final accounting your closure ledger row promised, and it
closes it. No action is required or possible — every session is stopped.*

**Final CPU-h (finished-job PBS cput, fully harvested): 0.000**  
`cpu_h == cpu_h_scheduler`, `queued_jobs = 0` — nothing left unaccounted.

### PBS jobs deleted at collection: none — this workspace held no PBS job at the sweep.

### mjs staging entries withdrawn (6) — never dispatched, zero cput

These were sitting in the `mjs` staging queue, invisible to `qstat`, and would have been
promoted into PBS as cores freed. Withdrawn by explicit id with `/usr/local/mjs/qrm`.

| mjs id | name | nodes |
|---|---|---|
| `3095` | rep05_s1w04 | `1:ppn=1:ax` |
| `3099` | rep05_s1w08 | `1:ppn=1:ax` |
| `3103` | rep05_s1w12 | `1:ppn=1:ax` |
| `3481` | rep05_c1w1 | `1:ppn=1:ax` |
| `3485` | rep05_c1w5 | `1:ppn=1:ax` |
| `3489` | rep05_c1w9 | `1:ppn=1:ax` |

*Closing assertion, taken twice at 2026-09-01T17:26Z and 17:28:35Z: **zero fleet jobs remain
in any state**, in PBS or in mjs staging, for this or any replicate. Other users' 418 staging
entries were untouched throughout.*
