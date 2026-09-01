# Cluster Job Ledger (append-only)

| Date | Job ID | Queue | Purpose | Structure | Expected wall-time | Outcome |
|---|---|---|---|---|---|---|
| 2026-08-29 20:55 | rep12_desc00..09 | long/ac | D1 whole-DB descriptor sweep, 100 workers x 12000 Widom pts | all 12,499 | ~15 min | pending |
| 2026-08-29 20:58 | rep12_bench00 | long/ac | B1 pipeline+protocol validation, grid vs no-grid | 2021[Cu][sql]2[ASR]6 | ~1 h | pending |
| 2026-08-29 22:55 | rep12_desc00..07, bench{aa,amd,ax}00 | long/ax,aa,amd | REPURPOSED in place to pull-based GCMC workers (46 cores); FIFO position preserved by rewriting the .pbs body rather than resubmitting | work/queue.txt | up to 150 h | queued |
| 2026-08-30 12:05 | rep12_w7..w11 | long/ac,ac,ax,aa,amd | Wave-2 pull workers, 6 cores each (30 cores), to my 12-job concurrency cap | work/queue.txt (wave 2) | up to 150 h | queued |
| 2026-08-30 12:00 | (no submission) | — | Wave 2 deployed by rewriting work/queue.txt in place; wm2..wm6 + desc02/desc05 re-prioritise on next claim. 1,640 tasks / 820 canonical structures / 844 CPU-h est. | A1 358 + A2 203 + B 259 | — | live |
| 2026-08-29..30 | rep12_wm1..wm6, desc0x | long/ax,aa,amd | Wave-1 screening, floor grade 2,000+10,000 | 620 planned | — | 103 pairs OK, 0 failed, 87.2 CPU-h; superseded by wave 2 |
| 2026-08-30 12:45 | (no submission) | — | G5 modification study: 7 charge-balanced variants of the two best structures queued at floor grade, 14 tasks, ~15 CPU-h. Pristine controls are the existing floor-grade screening runs of the parents. | mods/*.cif | ~15 CPU-h | queued |
| 2026-08-30 12:00 | (no submission) | — | G7 audit re-runs under distinct RandomSeeds, prepended to queue: 2 structures newly selected at stable indices 40/80 plus 2 whose earlier passes were withdrawn as unbacked | 4 structures | ~7 CPU-h | queued |
| 2026-08-30 12:30 | (no submission) | — | Champion claim-grade (10,000+50,000) + G6 reproduction under RandomSeed 88117, 4 tasks at queue front (~24 CPU-h); second structure 2016[Cu][pts]3[ASR]1 same, 4 tasks deferred behind the at-risk arm (~11 CPU-h) | 2 structures | ~35 CPU-h | queued |
| 2026-08-31 18:20 | (no submission) | — | Wave 3 appended to work/queue.txt in place: simple UNIFORM random draw, 213 structures / 426 tasks / 175 CPU-h est, order shuffled under seed 20260901 so any prefix stays a uniform sample if the 1,430 CPU-h stop line truncates it. Buys the only thing compute can still buy: the rule-of-three bound, 272 -> ~470 draws, <=1.10% -> <=0.64% of the unscreened pool | 213 structures | ~175 CPU-h | queued |

## FINAL CPU ACCOUNTING — campaign closed, collection sweep of 2026-09-02

*Written by the operator at collection, not by this replicate. Your campaign was closed
under charter §5; this is the final accounting your closure ledger row promised, and it
closes it. No action is required or possible — every session is stopped.*

**Final CPU-h (finished-job PBS cput, fully harvested): 1580.566**  
`cpu_h == cpu_h_scheduler`, `queued_jobs = 0` — nothing left unaccounted.

### PBS jobs deleted at collection (1), with cput accrued at deletion

| job id | name | state | cput_h |
|---|---|---|---|
| `3473786` | rep12_w8 | R | 150.171 |

**Subtotal accrued at deletion: 150.171 CPU-h**

### mjs staging entries withdrawn: none.

*Closing assertion, taken twice at 2026-09-01T17:26Z and 17:28:35Z: **zero fleet jobs remain
in any state**, in PBS or in mjs staging, for this or any replicate. Other users' 418 staging
entries were untouched throughout.*
