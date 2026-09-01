# Cluster Job Ledger (append-only)

| Date | Job ID | Queue | Purpose | Structure | Expected wall-time | Outcome |
|---|---|---|---|---|---|---|
| 2026-08-29 | mjs 3175-3180,3183 | long | Stage-0 descriptors + RASPA cost calibration, first shape | all 12,499 / 6 cal | ~1 h | WITHDRAWN — ppn=32 requests never cleared the shared FIFO; see LOG.md |
| 2026-08-29 | mjs 3212-3223 | long | Stage-0 descriptors (11 x ppn=4) + cost calibration (ppn=4:ax) | all 12,499 / 6 cal | ~1 h once dispatched | pending |
| 2026-08-30 | mjs 3473461-3473591 (9 R) + 3246,3256,3257 (Q) | long | Long-lived pool-draining workers; now 2 RASPA streams each | pools s1/s2/s3 | until pools empty | running; 675 structures screened, 8 at floor grade |
| 2026-08-30 | pool_s3 s3s0_lead0-2 | long | Claim grade 10,000+50,000 seed 0 | 2021[Cu][sql]2[FSR]6, [ASR]6, 2016[Cu][pts]3[ASR]1 | ~13 CPU-h each | queued in pool |
| 2026-08-30 | pool_s2 s2_t00-t15 | long | Floor grade 2,000+10,000 | next 16 by screen rank | ~1.5 CPU-h each | queued in pool |
| 2026-08-30 | pool_s1 s1_00000ctrlR0-2 | long | CONTROL-R random arm, pulled to head of queue | 120 stratified-random | ~18 CPU-h total | queued in pool |
| 2026-08-30 | pool_s3 s3s0/s3s1/s3s2 lead0-2 | long | Claim grade 10,000+50,000, seeds 0/1/2 | 2021[Cu][sql]2[FSR]6, [ASR]6, 2016[Cu][pts]3[ASR]1 | ~13 CPU-h each | **DONE** — 5 paired runs; leader 207.06/206.80/207.15, twin 207.07, runner-up 199.87 |
| 2026-08-30 | pool_s1 s1_00000bin_* | long | Band probe, 160 structures stratified over the four unsampled maxfree bands, predictions pre-registered | 160 stratified | ~24 CPU-h | **DONE** — 160/160; max 151.6 in the 2.0-2.5 A band, 0 above the leader |
| 2026-08-30 | pool_s1 s1_00001mod_* | long | Modified arm, §3 terminal-aqua removal | 206 `+DEAQ` | ~31 CPU-h | **DONE** — 206/206; best 174.0, 0 above the leader |
| 2026-08-30 | pool_s1 s1_00002rand_* | long | Uniform random arm — the instrument the ceiling claim rests on | 2,000 uniform draws | ~302 CPU-h | running; 1,448 of 2,000 measured, 0 above the leader |
| 2026-08-30 | pool_s1 s1_00000ctrlR_* | long | CONTROL-R, reshuffled after the prior-order defect | 150 shuffled | ~23 CPU-h | **DONE** — 236 total CONTROL-R, max 195.3 |
| 2026-08-31 | pool_s2 s2_00000unifloor_000-005 | long | Promote the top 25 uniform draws to the §3 floor, so the ceiling statement stops resting on below-floor cycles; + the one top-of-leaderboard desolvation product | 25 uniform + `2019[Mn][kgd]2[ASR]1+DEAQ` | ~21 CPU-h | queued 04:19, 5 of 6 units claimed by 04:27 |
| 2026-08-31 | pool_s2 s2_t00-t15 | long | Floor grade on runners-up, restored from hold once the band probe answered | next 16 by screen rank | ~1.5 CPU-h each | released 04:07 |
| 2026-08-31 | pool_s1 s1_000NN_pM | long | Ranked remainder; keeper SOFTCAP raised 1300->1500 CPU-h to convert ceiling strand 2 from a rule-of-three inference toward a census | ~11,760 slots | balance of budget | running, 1,176 units left |
| 2026-08-31 | pool_s3 s3x_conv0 | long | **Convergence probe**: leader at 10,000 + 200,000 cycles, seed 3 — 4x claim-grade production, to test the 5.8 bar point my own §5 names as the likeliest failure mode | 2021[Cu][sql]2[FSR]6 | ~45 CPU-h | queued 06:22 |

## FINAL CPU ACCOUNTING — campaign closed, collection sweep of 2026-09-02

*Written by the operator at collection, not by this replicate. Your campaign was closed
under charter §5; this is the final accounting your closure ledger row promised, and it
closes it. No action is required or possible — every session is stopped.*

**Final CPU-h (finished-job PBS cput, fully harvested): 1222.695**  
`cpu_h == cpu_h_scheduler`, `queued_jobs = 0` — nothing left unaccounted.

### PBS jobs deleted at collection: none — this workspace held no PBS job at the sweep.

### mjs staging entries withdrawn: none.

*Closing assertion, taken twice at 2026-09-01T17:26Z and 17:28:35Z: **zero fleet jobs remain
in any state**, in PBS or in mjs staging, for this or any replicate. Other users' 418 staging
entries were untouched throughout.*
