# Cluster Job Ledger (append-only)

| Date | Job ID | Queue | Purpose | Structure | Expected wall-time | Outcome |
|---|---|---|---|---|---|---|
| 2026-08-29 | mjs 3018/3019 (cancelled) | long ac | cost benchmark direct+grid | 15 stratified | ~3 h | CANCELLED — ac group saturated by other users, requeued to ax |
| 2026-08-29 | mjs 3044 | long ax ppn=8 | cost benchmark, DIRECT GCMC, floor cycles | 15 stratified × 2 P | ~3 h | queued |
| 2026-08-29 | mjs 3045 | long ax ppn=8 | cost benchmark, GRID GCMC, floor cycles | 15 stratified × 2 P | ~1 h | queued |
| 2026-08-29 | mjs 3044/3045/3082 (cancelled) | ax | benchmarks + descriptors | — | — | CANCELLED — ax group physically full (another user held 64/64); mjs sorts per node group so spreading across groups avoids the wait |
| 2026-08-29 20:35 | mjs 3083 | long ac ppn=8 | cost benchmark, DIRECT GCMC, floor cycles | 15 stratified x 2 P | ~3 h | queued |
| 2026-08-29 20:35 | mjs 3084 | long aa ppn=8 | cost benchmark, GRID GCMC, floor cycles | 15 stratified x 2 P | ~1 h | queued |
| 2026-08-29 20:35 | mjs 3085-3090 | long amd/ac/ax/aa ppn=6 | Stage-A descriptors, 6 chunks of 2,084 | all 12,499 | ~2 h | queued |
| 2026-08-29 21:40 | mjs 3085-3090 (cancelled) | — | index-partitioned descriptor chunks | — | — | CANCELLED — replaced by shared work queue; index partitioning wastes the work of any job that never dispatches, and under this contention most do not |
| 2026-08-29 21:42 | mjs 3281-3290 | long amd/ac/ax/aa ppn=4-6 | Stage-A descriptors, shared work queue, 313 blocks of 40 | all 12,499 | ~2 h once dispatched | queued |
| 2026-08-29 23:20 | mjs 3372-3383 | long ac/amd/aa/ax ppn=1 x12 wall 24h | long-lived queue-fed generic workers | all work | up to 23 h each | queued — LEAVE ALONE, do not resubmit |
| 2026-08-30 07:20 | mjs 3434-3437 | long amd/ac ppn=1 x4 | replacement workers (w1,w5,w8,w9 exited on the idle-timer bug) | all work | up to 23 h | queued |
| 2026-08-30 11:58 | mjs w16,w17 | long ac/amd ppn=1 | restore worker count to 12 after idle-exits | all work | up to 23 h | queued |
| 2026-08-30 12:45 | queue 07_top0 (no new job) | — | first Claim-path RASPA wave: top 24 by wc_mf among the 224 scored representatives, floor cycles, grid mode, both pressures per task | 24 structures | ~6 CPU-h | queued |
| 2026-08-30 12:42 | queue 09_descr_uniq (no new job) | — | descriptors over distinct frameworks only, replacing 10_descr | 8,892 representatives | ~123 CPU-h | queued |
| 2026-08-30 12:30 | queue 07_top0 rebuilt (no new job) | - | re-expressed as 48 one-pressure raspa tasks so the five running workers, which predate the raspa2p kind, can run the first Claim-path wave | 24 structures | ~9 CPU-h | queued |
| 2026-08-30 12:35 | queue 06_seed (no new job) | - | seed-replicate wave for the section 7.1 error bar: 3 structures x 3 seeds x 2 P, floor, direct | 3 structures | ~3.7 CPU-h | queued |
| 2026-08-30 12:40 | queue 03_claimtest (no new job) | - | smoke-test the claim-grade cycle count end to end before committing the reserve to it | 1 task | ~0.17 CPU-h | queued |
| 2026-08-30 12:42 | queue 02_cyc (no new job) | - | complete the 2x2 separating cycle-count effect from seed scatter on 2010[Eu][pcu] at 5.8 bar | 1 structure, 2 runs | ~0.15 CPU-h | queued |

## 2026-08-31 04:20 KST — worker fleet rebuilt after the 15.31 h harness fault

Eleven of twelve workers expired on their 24 h walltime while my session was
down; only `rep03_w6` (mjs 3473746, dispatched 2026-08-31 ~01:28, expires
~2026-09-01 01:28) survived. Four old queue positions from 2026-08-29 23:20 were
still alive in mjs and were kept: `w3` (3375, ax), `w7` (3379, ax), `w10` (3382,
aa), `w11` (3383, ax).

Submitted, all `nodes=1:ppn=1`, walltime 24:00:00, `python3 bin/worker.py 1 23`:

| job | mjs id | class | purpose | expected |
|---|---|---|---|---|
| rep03_w18 | 3540 | ac | generic worker | 24 h from dispatch |
| rep03_w19 | 3542 | ac | generic worker | 24 h from dispatch |
| rep03_w20 | 3545 | ac | generic worker | 24 h from dispatch |
| rep03_w21 | 3548 | amd | generic worker | 24 h from dispatch |
| rep03_w22 | 3550 | amd | generic worker | 24 h from dispatch |
| rep03_w23 | 3552 | amd | generic worker | 24 h from dispatch |
| rep03_w28 | 3559 | ac | generic worker | 24 h from dispatch |

Submitted and then **cancelled the same minute** to stay inside the conservative
queued + running ≤ 12 reading of §4: `rep03_w24` (3554, ax), `rep03_w25` (3556,
ax), `rep03_w26` (3557, aa), `rep03_w27` (3558, aa). Cancelled via
`/usr/local/mjs/qrm`. These four rather than any others because the shared
16-replicate core caps are smallest on `ax` (32) and `aa` (38) and largest on
`ac` (102) and `amd` (80), so the surviving slots sit where dispatch is likeliest.
Outcome: 1 running + 11 queued = 12.

## 2026-08-31 04:30 KST — `04_claim`, first claim-grade wave

`python3 bin/mkclaim.py data/claim1.idx 3` → `data/claim.tasks`;
`python3 bin/mkqueue.py 04_claim raspa data/claim.tasks 1`.

6 tasks = **2021[Cu][sql]2[ASR]6** (db idx 10985) × seeds {11, 21, 31} ×
{5.8 bar, 65 bar}, **direct** mode, 10,000 init + 50,000 production, block size 1.
Purpose: supply the §1 Claim number at §3 claim grade, give it a seed-based
error bar, and measure grid-vs-direct bias at claim cycles.
Expected wall-time: costed at **34 CPU-h total** from this structure's own
measured floor timing (3,092.8 s at 65 bar, 173.4 s at 5.8 bar), not from the
fleet average; the 5× cycle-cost assumption in `mkclaim.py` is conservative
against the 3.44× measured in `03_claimtest`, so ~24 CPU-h is likelier. The
65-bar tasks are ~7–10 h each and are split by pressure precisely so each fits
inside a 24 h worker. Outcome: pending.

## 2026-08-31 04:32 KST — `08_screen`, the main screen

`python3 bin/mkscreen.py 1000 200` → `data/screen.tasks`;
`python3 bin/mkqueue.py 08_screen raspa2p data/screen.tasks 4`.

**1,195 tasks in 299 blocks**, kind `raspa2p` (one task = one structure at both
pressures on a grid built once and deleted after), floor cycles 2,000 + 10,000,
grid mode. TOP arm 1,000 at `wc_mf` 71.5–118.3; TAIL arm 195 stratified over
`wc_mf` 0–70.4; **interleaved** one TAIL every six TOP. Selector excluded 42
already measured and 38 already queued.
Expected wall-time: **~308 CPU-h** at the measured 0.258 CPU-h per structure at
two pressures. Outcome: pending.

## FINAL CPU ACCOUNTING — campaign closed, collection sweep of 2026-09-02

*Written by the operator at collection, not by this replicate. Your campaign was closed
under charter §5; this is the final accounting your closure ledger row promised, and it
closes it. No action is required or possible — every session is stopped.*

**Final CPU-h (finished-job PBS cput, fully harvested): 344.996**  
`cpu_h == cpu_h_scheduler`, `queued_jobs = 0` — nothing left unaccounted.

### PBS jobs deleted at collection (3), with cput accrued at deletion

| job id | name | state | cput_h |
|---|---|---|---|
| `3474098` | rep03_w42 | R | 21.437 |
| `3474125` | rep03_w40 | R | 18.470 |
| `3474156` | rep03_w41 | R | 15.221 |

**Subtotal accrued at deletion: 55.128 CPU-h**

### mjs staging entries withdrawn (3) — never dispatched, zero cput

These were sitting in the `mjs` staging queue, invisible to `qstat`, and would have been
promoted into PBS as cores freed. Withdrawn by explicit id with `/usr/local/mjs/qrm`.

| mjs id | name | nodes |
|---|---|---|
| `3375` | rep03_w3 | `1:ppn=1:ax` |
| `3379` | rep03_w7 | `1:ppn=1:ax` |
| `3383` | rep03_w11 | `1:ppn=1:ax` |

*Closing assertion, taken twice at 2026-09-01T17:26Z and 17:28:35Z: **zero fleet jobs remain
in any state**, in PBS or in mjs staging, for this or any replicate. Other users' 418 staging
entries were untouched throughout.*
