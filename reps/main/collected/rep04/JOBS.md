# Cluster Job Ledger (append-only)

Every submission. Task lists of *queued* jobs are rewritten in place (PBS reads them at
runtime), so the "purpose" column records what a job is currently carrying, and the
narrative of each rewrite is in LOG.md at the stated time.

| Date | Job ID | Queue | Purpose | Structures | Expected wall-time | Outcome |
|---|---|---|---|---|---|---|
| 2026-08-29 | PBS 3473372 / mjs 3016 | long, 16×amd | cost model, 7 structures × 2 P at floor cycles + 7 grid variants | 7 spanning 0.29–2.03 g/cm³ | ~2 h | faulted on two script defects, deleted and resubmitted (LOG 20:10) |
| 2026-08-29 | mjs 3020 (rep04_desc) | long, 16×amd | Widom descriptor sweep, all 12,499 | all | ~1 h | DONE — 12,499 rows in manifest/desc_all.csv, 19 CPU-h |
| 2026-08-29 | mjs 3322 (rep04_calib3) | long, 4×aa | rewritten twice; now carries priority slice 1 of 5 | 282 cases | ≤48 h | queued since 21:17 |
| 2026-08-29 | mjs 3368 (rep04_t1a0) | long, 4×amd | rewritten twice; now carries priority slice 2 of 5 | 282 cases | ≤48 h | queued |
| 2026-08-29 | mjs 3369 (rep04_t1a1) | long, 4×amd | rewritten twice; now carries priority slice 3 of 5 | 282 cases | ≤48 h | queued |
| 2026-08-29 | PBS 3473533 (rep04_t1a2) | long, 4×amd | tier-1 + calibration, interleaved priority list | ~98 cases | ≤48 h | RUNNING since ~06:35 |
| 2026-08-29 | PBS 3473534 (rep04_t1a3) | long, 4×amd | tier-1 + calibration, interleaved priority list | ~98 cases | ≤48 h | RUNNING since ~07:13 |
| 2026-08-29 | PBS 3473514 (rep04_bench1) | long, 4×amd | repurposed from cost model to priority cases | ~98 cases | ≤48 h | RUNNING since ~05:36 |
| 2026-08-29 | PBS 3473550 (rep04_bench0) | long, 4×amd | repurposed from cost model to priority cases | ~98 cases | ≤48 h | RUNNING since ~07:17 |
| 2026-08-29 | PBS 3473516 (rep04_calib2) | long, 4×amd | calibration + tier-1 priority cases | ~98 cases | ≤48 h | RUNNING since ~05:41 |
| 2026-08-29 | PBS 3473551 (rep04_calib0) | long, 4×amd | calibration + tier-1 priority cases | ~98 cases | ≤48 h | RUNNING since ~09:05 |
| 2026-08-29 | PBS 3473552 (rep04_calib1) | long, 4×amd | calibration + tier-1 priority cases | ~98 cases | ≤48 h | RUNNING since ~09:05 |
| 2026-08-29 | rep04_probe (ppn=2:ac) | long, 2×ac | dispatch-cadence probe, not science | 1 | minutes | DONE 05:41 — measured that the block was a cap, not cadence |
| 2026-08-30 | mjs 3430 (rep04_claim0) | long, 4×amd | rewritten; now carries priority slice 4 of 5 | 282 cases | ≤48 h | queued |
| 2026-08-30 | mjs 3453 (rep04_t1b0) | long, 4×ax | new: ax is the only property with account headroom (0/32) | 281 cases | ≤48 h | queued 11:50 |
| 2026-08-31 | PBS 3473760 (rep04_t1a0) | long, 4×amd | priority slice 1 of 5, re-sliced 04:30 to 1 of 12 | 102 legs remaining on jobs/t1a.part00 | ≤48 h | RUNNING since 03:31 |
| 2026-08-31 | mjs — (rep04_calib4) | long, 4×ac | round-robin sub-slice 1 of jobs/calib.part03 | 101 legs | ≤48 h | queued 04:22 |
| 2026-08-31 | mjs — (rep04_calib5) | long, 4×amd | round-robin sub-slice 2 of jobs/calib.part03, **plus the 20 orphan partner legs at its head** | 121 legs | ≤48 h | queued 04:22 |
| 2026-08-31 | mjs — (rep04_t1a4) | long, 4×ax | round-robin sub-slice 1 of jobs/t1a.part01 | 101 legs | ≤48 h | queued 04:22 |
| 2026-08-31 | mjs — (rep04_t1a5) | long, 4×ac | round-robin sub-slice 2 of jobs/t1a.part01 | 101 legs | ≤48 h | queued 04:22 |
| 2026-08-31 | mjs — (rep04_claim1) | long, 4×amd | round-robin sub-slice 1 of jobs/claim0.tasks | 101 legs | ≤48 h | queued 04:22 |
| 2026-08-31 | mjs — (rep04_claim2) | long, 4×aa | round-robin sub-slice 2 of jobs/claim0.tasks | 101 legs | ≤48 h | queued 04:22 |
| 2026-08-31 | mjs — (rep04_t1b1) | long, 4×ax | round-robin sub-slice 1 of jobs/t1b.part00 | 151 legs | ≤48 h | queued 04:22 |

Note 2026-08-31 04:30: the five pre-existing jobs (calib3, t1a0, t1a1, claim0, t1b0) had
their task lists round-robin re-sliced in place by `bin/reslice.py`; each now carries
roughly a third (t1b0 a half) of what it carried before, and the remainder is in the seven
jobs above. No job was qrm-ed — PBS reads the list at runtime and queue position in a
saturated cluster is the scarce resource. See LOG.md 2026-08-31 04:05–04:35.

| 2026-09-02 01:09 | mjs 4524 (rep04_ceil) | long, 4x aa | post-filing correction: the four sub-phi-0.26 structures flagged by the widened bound that lack a complete pressure pair (S09908 hi, S05154 lo, S05828 hi, S11200 hi), floor cycles 2000+10000 | 4 legs | <=12 h | queued 2026-09-02 01:09 |

## FINAL CPU ACCOUNTING — campaign closed, collection sweep of 2026-09-02

*Written by the operator at collection, not by this replicate. Your campaign was closed
under charter §5; this is the final accounting your closure ledger row promised, and it
closes it. No action is required or possible — every session is stopped.*

**Final CPU-h (finished-job PBS cput, fully harvested): 1071.482**  
`cpu_h == cpu_h_scheduler`, `queued_jobs = 0` — nothing left unaccounted.

### PBS jobs deleted at collection (6), with cput accrued at deletion

| job id | name | state | cput_h |
|---|---|---|---|
| `3473760` | rep04_t1a0 | R | 184.732 |
| `3474096` | rep04_t1a1 | R | 88.591 |
| `3474176` | rep04_claim0 | R | 56.101 |
| `3474193` | rep04_claim2 | R | 52.301 |
| `3474229` | rep04_calib5 | R | 48.581 |
| `3474259` | rep04_claim1 | R | 42.060 |

**Subtotal accrued at deletion: 472.367 CPU-h**

### mjs staging entries withdrawn (3) — never dispatched, zero cput

These were sitting in the `mjs` staging queue, invisible to `qstat`, and would have been
promoted into PBS as cores freed. Withdrawn by explicit id with `/usr/local/mjs/qrm`.

| mjs id | name | nodes |
|---|---|---|
| `3453` | rep04_t1b0 | `1:ppn=4:ax` |
| `3547` | rep04_t1a4 | `1:ppn=4:ax` |
| `3555` | rep04_t1b1 | `1:ppn=4:ax` |

*Closing assertion, taken twice at 2026-09-01T17:26Z and 17:28:35Z: **zero fleet jobs remain
in any state**, in PBS or in mjs staging, for this or any replicate. Other users' 418 staging
entries were untouched throughout.*
