# STATE — rep10 methane deliverable-capacity campaign

**Deadline (hard):** **2026-09-06T16:20:49+09:00** — `deadline_kst` in `WORKSPACE.json`
is authoritative and has now moved twice: launch 2026-08-29T20:42:28 + 168 h, + 4.4704 h
recorded fleet pause, + **15.1688 h restored** for the harness fault that held this session
down 2026-08-30T03:54:21Z → 2026-08-31T04:04:28 (INBOX, same timestamp). Never hardcode it;
`bin/status.sh` printed a stale literal through both extensions until it was fixed.
**At 2026-08-31 04:13 KST: ~141.0 h left.**
**Target:** max N(65 bar) − N(5.8 bar), 298 K, **absolute**, cm³ STP/cm³, over `db/`.

## ⚠ SPEND IS THE BINDING BUDGET AND IT IS OVER HALF GONE
A spend meter now exists. Harness notice 2026-08-30T18:59Z added `spend_usd`,
`spend_cap_usd`, `spend_fraction` to `usage.json`, and charter §5 gained **Rev 24
(Endgame and the spend warning)** — read it. `bin/meter.py` meters spend with the same
reset-banking as tokens and prints it first.

**2026-08-31 04:13: $144.74 / $280 = 51.7%.** Tokens 18.9%, compute 12.7%. Spend rose
**$3.14 in ~12 min** of active session ≈ **$15 per active hour**, so $135 of headroom is
about **9 hours of active session against 141 hours of wall clock**. The 75% warning
($210) arrives after roughly 4 more active hours.

**Therefore the default between check-ins is to do nothing.** The campaign is autonomous
(`bin/supervise2.sh`) and REPORT.md regenerates hourly. Check in with **one** call —
`ssh dirac-bei 'bash /home1/users/Bei/ws/rep10/bin/status.sh'` — act only on something new
or wrong, then end the turn. Do not re-derive what `data/*.txt` already carries. Space
check-ins hours apart, not minutes.

## Charter Rev 25 + 45-min cadence (INBOX 2026-08-30T20:09Z) — READ BEFORE PLANNING
- **Compaction is now required on a CONDITION, not at phase boundaries.** Charter §4
  "Context hygiene" amended: compact whenever accumulated context materially exceeds
  current needs; working guideline **`transcript_mb` >= 1.5**. `usage.json` now publishes
  `transcript_mb` (this live session), `transcript_mb_all_sessions`, and
  `compaction_guideline_mb`. **At 05:51 I stood at 1.47 of 1.5 — at the threshold.**
- **Compaction costs nothing that the file record already carries.** The session loop
  starts each session from the initial prompt, not a resumed conversation, so a restart
  re-orients from `CHARTER.md`, `STATE.md`, `LOG.md` and git history. That is ratified
  design. **The standard those files must meet is exactly that they suffice alone** — which
  is why this file is written the way it is. If you are a fresh session: everything you
  need is here, in `LOG.md`, and in `REPORT.md`. Nothing important lives only in a
  transcript.
- **Idle re-invocation cadence lengthened 10 min -> 45 min**, effective when the loop next
  starts. This materially extends the runway: holding turns cost ~$0.15 each and 51 min of
  holding cost $5.16 total, versus ~$2.50 for a full check. **Hold by default; check on a
  ~10-45 min rhythm, not every turn.**

### Both escalations answered (same notice)
- **MakeGrid: I was right, retracted fleet-wide.** The harness test searched the small
  driver binary; the code path is in the linked RASPA library. The lesson I had already
  written into REPORT.md §5 — that the failure is deferring to a derived summary or an
  authoritative claim over a direct observation already in hand — was confirmed, with the
  note that it applied to the harness before it applied to me.
- **The burn-rate arithmetic was right**, and it is why the cadence and Rev 25 were made.

### A THIRD compute figure now exists — do not quote it yet
`usage.json` gained `cpu_h: 18.487` with `cpu_h_basis: finished-job PBS cput` and
`cpu_h_runs_accounted: 1`. That is actual CPU time from *one* harvested job, so it is
radically incomplete; `cpu_h_scheduler` (217.2) is wall-clock-based and is what REPORT.md
quotes. Both are still lower bounds on true campaign compute because head-node work was
never metered at all. Do not swap the report onto `cpu_h` while `runs_accounted` is 1.

## ⚠ THE SPEND CAP, NOT THE DEADLINE, WILL END THIS CAMPAIGN
Measured 2026-08-31: $140.52 at 04:04 → $148.61 at 04:19 → $155.08 at 04:22 (55.4%).
That is **~$3 per turn**, and the cost is per-turn context re-read, not work: an idle
check-in costs about the same as a working one. ~$125 of headroom is therefore **~39
turns**, and the 75% warning is ~17 turns away. The deadline is 141 h out and irrelevant
by comparison. Filed as `[ESC: infra / ...]`; nothing in the charter lets me change the
re-invocation cadence from inside the session.

**The only lever is fewer and shorter turns.** Do not re-arm background waiters — they do
not survive session teardown here and each attempt costs a turn. Do not re-read REPORT.md
or LOG.md to admire them. One bounded `bin/status.sh`, act only if something is wrong,
end the turn.

## Critical path, 2026-08-31 04:23 — verify the leader before the money runs out
`2021[Cu][sql]2[ASR]6` measured **207.12** at screen cycles, 9.5 above the claim-grade
best. Verification queued, and ordered so the *fast* evidence lands first, because a
claim-grade run needs ~2.5 h and the spend cap may be closer than that:

| tasks | tier | cycles | ~wall | status at 04:34 |
|---|---|---|---|---|
| `AA0000/AA0001` | floor | 2,000+10,000 | ~30-40 min | queued, sorts FIRST, **not yet claimed** |
| `AZ10000/1, AZ20000/1, AZ30000/1` | claim | 10,000+50,000 | ~2.5 h | queued, unclaimed |

**`AZ10000` is no longer running.** It was claimed by a head-node worker at 04:12 and was
13 min in when I killed all head-node workers for charter §4 compliance (see LOG). Its
orphaned claim directory and stub result file were removed by hand, because `reap.py`
would not have released them for 3 h. The task is back in the queue for a *scheduler*
worker. **All simulation now runs through the scheduler only** — there is no head-node
fallback any more, by design.

To free a slot I cancelled one running worker (`3473595`) and topped up; its replacement
is pending in the shared 252-core pool. We sit at the 12-job cap, so nothing further can
be pushed: `AA` gets claimed the moment any worker finishes its current task.

`pull.py` claims alphabetically, so tier `AA` was minted specifically to sort ahead of
`AZ`; the equivalent `FZ` floor tasks were deleted to avoid running the same work twice.
A floor-tier confirmation near 207 would upgrade the finding from screen-only to charter
§3 floor evidence, which is the best return per minute available right now.

**REPORT.md is already safe against a stop at any moment**: `bin/mkreport.py` generates a
*Pending verification* block under the Claim listing every material measured above the
claim-grade best at a lighter tier, recomputed hourly, self-emptying when the runs land.
So if the cap fires first, the filed report is honest and complete — it claims
`2015[V][srs]3[FSR]1` at 197.64 and discloses 207.12 as pending. **Do not let a desire to
promote 207.12 push a screen-grade number into the Claim; charter §3 forbids it.**

## Budgets — read `bin/meter.py`, NEVER `usage.json` directly
`usage.json` meters the **current session, not the campaign**: its `tokens` field reset
from 2,492,029 to ~290,000 at the 2026-08-30 pause. Read straight it understates usage
silently and in the unsafe direction. `bin/meter.py` keeps a monotone reset-corrected
total in `data/meter.json` and the supervisor runs it every 10 min.

**At T+18.8 h: tokens 4.55 M / 32 M = 14.2%** · compute 65.5 / 1,610 CPU-h (4.1%) ·
≤12 queued jobs. Compute counts **scheduler jobs only**; head-node work is unmetered.

### CADENCE WARNING — tokens are the binding budget, not compute
Compute is at 4% with 156 h left; **tokens went 2.78 M -> 4.55 M in under an hour of
active turns.** At that rate the 32 M cap binds long before the deadline, and charter §4
warns spend (unmetered here) runs *higher* than the token basis because cache reads are
charged but excluded from it. The campaign is fully autonomous and `REPORT.md` regenerates
hourly, so **the correct default between check-ins is to do nothing**. Check in with
`bash bin/status.sh` (one bounded summary), act only if it shows something wrong or new
results that change a conclusion, and end the turn. Heavy analysis passes are largely
done; do not re-derive what `data/*.txt` already carries.

**Superseded:** this file previously recorded that no spend meter existed and that
planning had to run off reset-corrected tokens as a lower bound. That was true until
2026-08-30T18:59Z and is no longer. Spend is now read directly; see the block at the top.

## THE LEADER CHANGED — `2021[Cu][sql]2[ASR]6` at **207.12** (screen cycles only)
Tier `B` did its job. The refutation queue measures structures the model ranks *above* the
incumbent, and one of them beat it by 9.5:

| structure | tier | wc | ±err |
|---|---|---|---|
| **`2021[Cu][sql]2[ASR]6`** | screen 500+2,500 | **207.12** | 1.66 |
| `2016[Cu][pts]3[ASR]1` | screen 500+2,500 | 199.26 | 2.65 |

**This is not yet claim-grade and cannot be quoted as the Claim until it is.** Queued
2026-08-31 04:10 as tiers `AZ1/AZ2/AZ3` (10,000+50,000, one seed per task so the three run
in parallel) and `FZ` (floor, for the cross-tier check). ~17 CPU-h. Expect ~206.7 at
claim-grade if the measured screen→claim bias (−0.46 ± 0.45, n=5) holds.

**Until those land, the defensible claim is still `2015[V][srs]3[FSR]1`.**

## Best claim-grade results (10,000 + 50,000 cycles, direct summation)
| structure | seeds | wc | ±err |
|---|---|---|---|
| `2015[V][srs]3[FSR]1`  | 1,2,3 | **197.64 / 197.57 / 197.28** | 0.32 / 0.69 / 0.80 |
| `2013[Yb][nia]3[ASR]1` | 1,2,3 | 196.26 / 196.24 / 196.21 | 0.68 / 0.36 / 0.90 |
| `2013[Ni][nia]3[ASR]1` | 1,2,3 | 194.43 / 194.35 / 193.94 | 0.91 / 0.82 / 1.02 |
| `2015[Zn][ith]3[FSR]1` | 1,2,3 | 190.56 / 190.46 / 190.43 | 0.92 / 1.41 / 0.56 |

V-srs and Yb-nia are separated by ~1.35 against combined error ~0.7 — close, not tied.
Screen → floor → claim agree closely, so the screen is an unbiased selector.

## ⚠ THE DATABASE IS 26.8% REDUNDANT — `dupes.py` WAS WRONG, USE `dupes2.py`
`bin/dupes2.py` → `data/dupes2.csv`. Content key = cell + sorted multiset of
(element, wrapped fractional x,y,z) at 5 dp — exactly what the chargeless protocol feeds
RASPA. Over all 12,499 entries:

    distinct materials 9,144 · duplicate groups 3,245 · redundant entries 3,355 (26.84%)
    group sizes  2: 3,178   3: 24   4: 43   ·  unparsed: 1

Found because the new leader appeared as both `[ASR]6` and `[FSR]6` with **byte-identical**
output (207.1175 ± 1.6598, both pressures, every field) — impossible for independent
stochastic runs. Same cell, same 244 atoms, same order; they differ only in the `data_`
name and the partial-charge column, which this protocol ignores. RASPA is deterministic
given the same input and seed.

**This file previously said the opposite** — that `2015[V][srs]3[ASR]1` and `[FSR]1` "are
not one file counted twice", on the strength of `dupes.py` reporting zero duplicate groups.
They *are* one material (identical screen values, 197.8879 ± 1.8242); the 0.32 gap cited
was a screen value against a claim-grade value of the same material. `dupes.py` grouped on
a *descriptor* signature, which only compares structures that both carry descriptor rows
and is weaker than the structure itself. **Do not use `dupes.py`.**

**Open consequence for the ceiling — not yet done.** The population is 9,144 distinct
materials, not 12,499. The hypergeometric model-free bound and the E[unscreened beats best]
table are both stated over entries and must be restated over distinct materials.
Deduplication shrinks the unscreened remainder as well as the screened set, so coverage
should *improve*; the leaderboard must name one material per group.

## THE CAMPAIGN RUNS ITSELF — do not hand-drive it
`bin/supervise2.sh` runs detached until **2026-09-05 23:55 KST**. Check the whole
campaign with **`ssh dirac-bei 'bash /home1/users/Bei/ws/rep10/bin/status.sh'`** — it
prints budgets, tier counts, claim-grade table, supervisor health, ceiling and coverage
in ~20 lines. Restart with **`bash bin/resup.sh`**, which kills any running instance and
starts exactly one, and always prints the surviving PID list.

**Detection hazards, all hit for real on 2026-08-30 — see LOG:**
- `ps -u Bei` **silently omits processes**; `ps -eo pid,user,args` does not. A false
  supervisor is dead made me launch a duplicate. Use `bin/suppids.sh`, which scans
  with `ps -eo` and confirms ownership from `/proc/<pid>/cwd`.
- Sixteen replicates run as the **same UNIX user `Bei`** and sibling supervisors are
  visible in `ps`. Never kill by command-name match; cwd is the only safe test.
- `pkill -f` here is not procps `pkill` and matches nothing silently.
- Editing `supervise2.sh` while it runs does nothing until restart (bash reads by byte
  offset). Always edit, then `bin/resup.sh`.
- Before believing an alarming reading, corroborate from an independent source. The
  supervisor death I chased was disproved by its own heartbeat log, which ran
  continuously through the 4.47 h pause with no ssh session open.

Every 10 min it tops the cluster up to 12 jobs (under the compute-budget guard), holds 4
`nice -19` head-node workers (2 above load 80, 0 above 110), reaps claims orphaned by
killed workers, refreshes `data/wc.csv` and runs `bin/meter.py`. Every hour it refits
the predictor, promotes the funnel, widens the screen, recomputes the ceiling and
`data/tiercheck.txt`, and regenerates `REPORT.md`.

**`bin/topup.sh` carries a compute-budget guard** (added T+15 h). It reads
`usage.json:cpu_h_scheduler`, keeps a 40 CPU-h reserve, sets each new worker's walltime
guard to `remaining/12` hours (capped 40 h) so 12 concurrent workers cannot collectively
overrun, and `qdel`s our own workers at the ceiling. Without it, 12 workers held to the
deadline projected to ~1,940 CPU-h against a 1,610 hard stop.

## The funnel
| tier | cycles | selection | task prefix |
|---|---|---|---|
| screen | 500 + 2,500 | ranked band + uniform-random, both pressures | `m`,`n`,`s`,`v` |
| floor | 2,000 + 10,000 | top 60 measured within 30 cm³/cm³ of best | `F` |
| claim-grade | 10,000 + 50,000 | top 8 by floor measurement, 3 seeds | `A` |
`pull.py` claims alphabetically and uppercase sorts first, so claim-grade pre-empts
everything. Promotion (`bin/promote.py`) uses **measured** values only, never predicted,
and is idempotent. Widening (`bin/extend.py`) stops at 1,250 CPU-h, floor work at 1,350.

Counts at T+17.6 h: **195 screened · 26 floor · 7 claim-grade runs / 5 structures**
(226 rows in `data/wc.csv`).
**205 pending tasks covering 651 distinct structures** are queued and unclaimed.

## Ceiling argument — the machinery is built and the queue already covers it
`bin/ceiling2.py` → `data/ceiling.txt`, refreshed hourly. Residual spread is modelled as
prediction-dependent (`sd = max(2, 13.114 − 0.0533·pred)·√(π/2)`, rescaled ×1.58 to unit
standardised variance); the Gaussian tail is selected over t8/t4 on observed exceedances
(obs 8/6/4/3/2 beyond +10/15/20/25/30 vs Gaussian 34/19/11/6/4 — the model is
**conservative**, over-predicting the tail). Expected number of unscreened structures
that beat the best, as a function of how deep we screen:

| screen down to wc_pred ≥ | structures in set | E[beat best] |
|---|---|---|
| 185 | 64 | 0.468 |
| 180 | 106 | 0.116 |
| 175 | 152 | 0.039 |
| 170 | 214 | **0.010** |
| 165 | 288 | 0.003 |

**Verified T+15 h:** the 205 pending tasks cover **100% of the still-unscreened set down
to wc_pred ≥ 160** (313 structures) — so no new queueing is needed to reach E ≈ 0.001.
Re-verify with `python3 bin/qgap.py` after any refit (the refit reorders predictions, so
coverage must be rechecked, not assumed).

## Ceiling argument, physical leg — the maximum is INTERIOR in both physical axes
`bin/optimum.py` (quantile bins — equal-width bins gave the OPPOSITE conclusion once,
see LOG) + `bin/vfedge.py`. Working capacity is a difference, penalised at both ends, so
it has an optimum in binding strength bounded above by accessible volume.
- **Henry constant: clearly interior.** Best at log10Kh +0.83…+1.16; capacity falls to
  184.6 on the weak-binding side and 144.2 on the strong side. Bracketed by measurement.
- **Void fraction: interior but thinly sampled.** Fine bands, top-3 measured:
  0.85–0.87 → 195.5 · 0.87–0.89 → 194.4 · **0.89–0.91 → 197.9** · 0.91–0.93 → 182.3 ·
  0.93+ → 97.2. The turnover rests on only n=11 and n=1.

The peak near vf ≈ 0.90 is **the thinnest part of the database and the model's blind
spot**: only 75 structures reach vf ≥ 0.90, 14 of the 36 at vf ≥ 0.90 were unmeasured,
and none of the 5 at vf ≥ 0.94. The ridge model has almost no training points there, so
the statistical bound — which is conditional on that model — is weakest exactly where the
physics says the answer lives. `bin/vfset.py` queued **48 unscreened structures with
vf ≥ 0.86 as tier `G`** (sorts behind `A` claim and `F` floor, ahead of the bulk
screen), highest-vf first, ~25 CPU-h. **This is the key outstanding measurement for the
ceiling claim.** If the turnover survives, the claim rests on mechanism as well as
statistics; if capacity instead keeps climbing to vf 0.96, the ceiling is higher than
measured and the report must say so.

## RUN THE REFUTATIONS FIRST — tier `B` (T+18.5 h)
The bulk screen is ordered by tier letter, so everything the model ranked highest sat in
*lowercase* tiers behind hundreds of ordinary structures. Most screening tightens a bound
around an answer I already have; **the only structures whose measurement can change the
answer are those predicted at or above the best measured value.**

`bin/topqueue.py 190` queues every unmeasured structure with `wc_pred >= 190` as tier `B`
(sorts after `A` claim-grade, ahead of all else), in 2-structure tasks so they land fast.
It runs **hourly from the supervisor** and is idempotent: structures already named in an
existing `work/set_top_*.txt` are skipped, and tags come from a clock, not a file count.
**Never tag from a count of files** — deleting one lets the counter reuse a tag, and
`plan.py` derives task ids from the tag, so a reused tag overwrites a live task and
orphans the rest of its tier. That happened at T+18.9 h; see LOG.

At T+18.9 h, 12 are outstanding (the hourly promotion added two) and **three are
predicted above the best measured 197.9**:
`2016[Cu][pts]3[ASR]1` 206.0 · `2021[Cu][sql]2[ASR]6` 201.0 · `2021[Cu][sql]2[FSR]6` 200.2.
If any measures above 197.9 **the leader changes** — the report follows the data
automatically.

**Coverage is not count.** A bound at threshold T is earned only when every structure
predicted above T has been measured. Comparing T's set size against the total number
screened is a different and wrong test: the screen was steered by earlier rankings and each
refit reorders the head of the list. `REPORT.md` §1 now checks this structure by structure
and labels the sharp bound a *projection* while any gap remains.

## Ceiling argument, robustness leg — the screening set is a UNION, not an argmin
`bin/robustset.py` -> `data/robustset.txt`, hourly (analysis only; **queue manually**).
`fitmodel.py` picks ridge λ by argmin of a nearly flat CV curve. At n=224:
10.94 / 11.37 / 11.35 / 10.94 / **10.76** / 11.39 / 13.21 / 16.66 over λ = 0.1…300. The
winner beats λ=0.1 by 0.18 against a s.e. of ~0.50 — a coin-flip that moved as the
calibration set grew, taking the ceiling set with it (count above 185 swung 16 ↔ 64).

Fix: keep every λ within 1 s.e. of the minimum (the data cannot reject them) and take the
**union** of the sets they nominate. At threshold 175, n=228: λ ∈ {0.1, 3, 10} survive,
nominating 155 / 126 / 97 structures; **union 158, intersection 94, 64 disputed**. The
argmin's 97 omitted 61 structures an equally supported model ranks above threshold.
Those 130 unscreened union members are queued as **tier `H00`** (~65 CPU-h).
Screening extra can only strengthen a ceiling bound — it spends surplus compute to remove
an assumption.

`fitmodel.py` now takes optional `[lam] [outpath]`; with no args it is byte-identical to
before. **Do not put `robustset.py --queue` in the hourly loop** — it would mint a new
tier every hour as the union drifts (same hazard removed from `vfset.py`).

## Ceiling argument, model-free leg — the number that owes the model nothing
`bin/freebound.py` -> `data/freebound.txt`, hourly. Both other legs lean on the same fit.
The uniform-random sample does not: **61 of the 100 uniform-random draws are measured and
none exceeds B = 197.89.** The hypergeometric upper confidence bound on how many of the
12,499 could exceed B:

| confidence | K <= | % of db |
|---|---|---|
| 95% | **597** | 4.78% |
| 90% | 461 | 3.69% |
| 68% | 230 | 1.84% |

Deliberately weak, and reported as such. The model-conditional bound says E[unscreened
structure beats B] ~ 0.015; these differ by four orders of magnitude and are **not in
conflict** — one assumes the model is sound, the other assumes it is worthless. The
honest claim lives between them and the report carries both, model-free first.

**Incidental result that may matter more than the bound:** the best structure in the
uniform-random sample measures **186.2** (it read 177.9 when the sample had 61 measured; it now has 98), which is 20.9 below B=207.12 and still below the claim-grade best of 197.64. An unbiased sample of the
database contains nothing close, which is direct evidence the top band is genuinely
exceptional rather than an artefact of having looked there hardest.

**This is the campaign's live falsifier.** `freebound.py` is written so that a single
random draw exceeding B prints an instruction to withdraw the ceiling claim and deepen the
screen, rather than quietly folding the exceedance into a wider interval. It has not
fired. Check it every session.

## Model (refit hourly; figures at n=214)
- `wc_lda` (local-density physical baseline) alone: Pearson 0.944, Spearman 0.819.
- Ridge on LDA + Widom descriptors, λ=0.1: **CV RMSE 10.55**, residual p50 +0.1,
  p95 +14.2, p97.5 +17.0, p99 +20.8.
- CV RMSE rose from 6.37 (n=154) to 10.55 (n=214) because widening keeps buying
  **uniform-random** points. That is the honest population figure; the earlier one was
  flattered by a top-band-heavy calibration set. Do not quote the 6.37.
- Guards: features clamped to the training box (touched 999 of 12,499); no prediction may
  exceed the LDA physical baseline by more than 3 affine-RMSEs (active on 128). Both were
  added after the first fit put essentially non-porous structures in its top 20.

## Structural-modification arm — negative so far, and physically expected
25%-methylation (`bin/methylate.py`, `MOD:*_f25`) was screened on the three best
frameworks. **All three lost capacity:**
| framework | unmodified | f25-methylated | Δ |
|---|---|---|---|
| `2020[In][nuc]3[ASR]1` | 196.19 | 191.48 | −4.7 |
| `2013[Yb][nia]3[ASR]1` | 198.33 | 187.08 | −11.3 |
| `2013[Ni][nia]3[ASR]1` | 194.71 | 183.87 | −10.8 |
Mechanism is the expected one: added CH₃ groups both *reduce* pore volume (lowering the
65-bar plateau) and *strengthen* binding (raising the 5.8-bar residual), and working
capacity is a difference that penalises both. The best frameworks already sit at void
fraction 0.87–0.93, i.e. near the optimum, so adding mass moves away from it.
**Open question:** whether the opposite direction (linker-vacancy defects, raising void
fraction) helps. Untested. See open tasks.

## Duplicate check (T+18.2 h) — the leaderboard is distinct materials
`bin/dupes.py`. Names carry ASR/FSR tags, so a parent framework can appear twice; the top
two hits `2015[V][srs]3[ASR]1` (197.89) and `[FSR]1` (197.57) differ by 0.32 and look like
one file counted twice. They are not. Signature = density + void fraction + free radius +
Henry constant to 4 s.f. simultaneously. **Zero duplicate groups across all 12,499
entries**; no two measured structures share a signature. The ceiling argument's
independence assumption survives.
- `MOD:` structures have **no descriptor row** (built from parent CIFs, never went through
  Widom). Verified that `fitmodel.py` and `ceiling2.py` both gate on descriptor
  membership, so modification measurements are excluded from the predictor and from the
  residual model. Correct — a modified structure is not in the population the bound covers.
- Bug fixed here: `dict.get` returned `None` for all MOD structures and the grouping read a
  shared *absence* as a shared signature, announcing four distinct methylated frameworks
  were one material. A missing value is not a matching value.

## Audited end-to-end against raw RASPA output (T+17.9 h) — do not redo
The three things that fail *silently* were checked against the raw claim-grade `.data`
for the headline structure. All pass; see LOG for the full block.
- Parser reads `Average loading absolute [cm^3 (STP)/cm^3 framework]` (the §2 field, not
  the mol/kg or per-gram variants). Pattern occurs **exactly once** per file, so the
  last-match indexing is unambiguous.
- **Excess prints identically to absolute** (232.5042489821 both) — §2's own reasoning
  confirmed: excess is defined against a helium void fraction §3 does not pin, so it is
  unset and the correction is zero.
- Arithmetic reproduces: 232.5042 − 34.9367 = 197.5675, √(0.5077²+0.4738²) = 0.6945,
  matching `data/wc.csv` to the last digit on all six fields; file confirms 50,000
  production cycles.
- Supercell uses RASPA's own criterion `ceil(2×12.8/perp width)` per axis (not a lattice
  constant rule — matters for non-orthogonal cells): 17.766 Å widths → UnitCells (2,2,2)
  → 35.53 Å vs the 25.6 Å minimum-image requirement. Filename `2.2.2` confirms.

**Traceability limit:** `worker.py` deletes its scratch dir after parsing. 519 raw
`.data` files survive under `runs/` for claim-grade (`runs/A`) and floor (`runs/F`) —
everything that can enter the Claim. Bulk-screen values exist only as parsed rows in
`work/res/*.csv`.

## Grid vs direct
`MakeGrid` **works in this build.** The harness notice claiming the binary contained no
MakeGrid code path was **RETRACTED** (INBOX 2026-08-30T19:23:45Z): it had searched
`bin/simulate`, an ~18 KB driver, while the logic lives in `lib/libraspa2.so`. Our own
measurement had already contradicted it and the report said so at the time — `MakeGrid`
occurs four times in the library, and the grid/direct comparison below agreed to 0.18.
**Lesson worth carrying into the report's self-assessment: our own data was right and an
authoritative-sounding infrastructure notice was wrong.** Deferring to it over a
measurement we had already taken was the mistake, and it is the same failure mode as
trusting `dupes.py` over the byte-identical outputs.

**This does not change strategy, and the reason is specific:** grids buy *compute*, and
compute was never the binding budget (12.7% used). **Spend** binds. So the retraction
restores an option that would accelerate a resource we are not short of. Our own comparison before that notice: floor cycles,
`2021[V][nan]3[FSR]12`, 5.8 bar, direct 140.91 ± 2.20 vs tabular 141.09 ± 1.90.
**Everything reported uses direct summation**, so no charter §3 grid disclosure is needed.

## Data files (all regenerable from `bin/` + `db/`)
`data/manifest.csv` · `data/descriptors.csv` (Widom scalars) · `data/hist_all.csv`
(82-bin adsorption-energy histogram, all 12,499) · `data/lda.csv` · `data/pred.csv`
(fitted prediction, best first) · `data/wc.csv` (**every measured working capacity**) ·
`data/ceiling.txt` · `data/model.npy` · `work/res/*.csv` (raw parsed points).
Helper: `bin/gap.py` (unscreened count per threshold), `bin/qgap.py` (queue coverage).

## Operating facts
- `export PATH=$PATH:/usr/local/mjs`. PBS spec `nodes=1:ppn=1:<ac|aa|amd|ax>`.
- mjs quotas are **per UNIX user**; all sixteen replicates submit as `Bei` and share one
  ~252-core pool. No per-replicate reservation exists or can be created (INBOX ruling).
  Escalated; the reply was the standard "logged, no answer guaranteed".
- **Never use `/tmp` on the cluster** — shared between replicates.
- Task scripts self-check binary + pinned force field before working; `worker.py` exits 3
  if most points fail to parse.
- Head-node workers: 4 × `nice -19` on a 96-core box at load ~20. Reading logged at
  LOG.md `[CHARTER-READ] §4`.

## Open tasks — endgame, rewritten 2026-08-31 04:45 KST

### WARNING — AT 91% SPEND, YOUR OWN CHECKING IS THE MAIN THREAT TO THE CAMPAIGN
The hard-stop guard in `bin/supervise2.sh` ends the campaign at 100% spend -- correctly,
per charter section 5. But the deadline is 2026-09-06 and the detached supervisor would
otherwise keep screening, promoting and tightening the ceiling argument for five more
days. **Every turn you take pushes toward 100% and buys nothing the supervisor is not
already doing.** A full check costs about USD 2.50; pure holding costs about USD 0.15. At
91.6% (about USD 23 left) the difference between checking hourly and holding is the
difference between the campaign ending tonight and running to the deadline.

The deliverable is COMPLETE: Claim 207.1 +/- 0.46 on two claim-grade seeds, all five
section 7 sections present, falsifier unfired, report self-regenerating hourly. There is
nothing left that a check can improve. **Hold. Do not check unless you have specific
reason to think something has broken.**

*(Written twice. The first attempt was sent inside a double-quoted `ssh "..."` string, so
the LOCAL shell expanded the backticks and the dollar signs before ssh ever saw them:
`bin/supervise2.sh` vanished, USD 2.50 became ".50", USD 0.15 became "/bin/bash.15". That
is the same class of error as the 04:45 incident logged in LOG.md, committed with a
message that read correctly, and I made it again after diagnosing it. The lesson is not
"be careful with quoting" -- it is that the only method proven safe here is writing the
patch to a file and piping it over ssh stdin, and I should stop hand-rolling shell
heredocs for record text at all.)*


**Read this first.** Spend is at 66% and rises ~$2.5-3 per turn whatever the turn does,
because the cost is per-turn context re-read. The deadline (2026-09-06T16:20:49) is ~140 h
away and is *not* what will stop this session; the spend cap is. Charter §5 Rev 24 governs
from the 75% warning (~$210, roughly 8-9 turns away): stop exploring, secure the claim,
keep REPORT.md filed and current. **Treat exploration as closed. Do not start new
analysis. Do not re-read REPORT.md or LOG.md to admire them.**

### The handoff, which is the important thing to understand
My session and the campaign are separate. `bin/supervise2.sh` runs detached until 16:10:49
on 2026-09-06 (ten minutes before the deadline — it previously stopped 16.4 h early on a
hardcoded literal; fixed 04:40). Every 10 min it tops the scheduler to 12 jobs and runs
`collect.py` + `meter.py`; every hour it refits, promotes the funnel on **measured** values
only, and regenerates `REPORT.md`. So:

- The six verification runs on the new leader will complete **whether or not I am
  attached**. `pull.py` is sound (sorted glob, atomic `mkdir` claim); `task_AA0000.sh`
  sorts first among unclaimed and is taken by the next worker to finish. Workers are
  simply mid-task on long screening jobs — this is not a bug and needs no intervention.
- When claim-grade rows for `2021[Cu][sql]2[ASR]6` land, `mkreport.py` replaces the Claim
  with it and empties the pending-verification block **automatically**.
- A frozen REPORT.md showing a pending verification therefore means my session stopped,
  not that verification was abandoned. REPORT.md says this to its reader.

### CONFIRMED AT FLOOR TIER 07:11 — the challenger is real
The floor verification landed and it holds. `task_AA0000`, 2,000+10,000 cycles, seed 1:

| material | tier | N(5.8 bar) | N(65 bar) | working capacity |
|---|---|---|---|---|
| `2021[Cu][sql]2[ASR]6` | floor | 36.7634 ± 0.8160 | 244.2163 ± 1.0744 | **207.45 ± 1.35** |
| `2016[Cu][pts]3[ASR]1` | floor | — | — | **199.57 ± 1.03** |

Screen → floor agreement is 207.12 → 207.45 (+0.33) and 199.26 → 199.57 (+0.31): both
slightly positive, both far inside error, consistent with the small measured cross-tier
bias. The screening result was not a fluke.

**Two materials now exceed the claim-grade incumbent** (`2015[V][srs]3[FSR]1`, 197.64).
207.45 is an *admissible* §3 number — floor is the charter's minimum for any reported
number — but the **Claim still requires 10,000+50,000 and must not change until that
lands.** REPORT.md handles this automatically and correctly; do not hand-edit it.

**Claim-grade runs are in flight.** `AZ10000/AZ10001/AZ20000/AZ20001` (seeds 1 and 2, both
structures) were claimed by scheduler workers; `AZ30000/AZ30001` (seed 3) remain queued.
Timing, measured rather than guessed: floor high-pressure took ~134 min for 12,000 cycles,
so claim-grade at 60,000 cycles is roughly **11-12 h per seed**, running in parallel —
expect completion late 2026-08-31. That is inside the deadline (2026-09-06T16:20) with
enormous margin, and at the current holding burn (~$1-2/h) inside the spend budget too.

### ✅ CLAIM IS 207.2 — `2021[Cu][sql]2[ASR]6` (claim-grade, 14:48)
Seed 2, 10,000+50,000: **207.1529 +/- 0.4311**. N(65)=243.9, N(5.8)=36.8.
Screen 207.1175 -> floor 207.4529 -> claim 207.1529: spread 0.34 across a 20x cycle
increase, error shrinking 1.66 -> 0.43. REPORT.md moved its own headline and emptied the
pending block. **Do not hand-edit it.**

Beats the long-standing incumbent `2015[V][srs]3[FSR]1` (197.6, 3 seeds) by **9.6 (4.9%)**.
Second best now `2016[Cu][pts]3[ASR]1` at 199.9 (2 claim-grade seeds).

**THREE claim-grade seeds, complete (2026-09-01 01:10):** 206.7971 +/- 0.6310,
207.1529 +/- 0.4311, 207.1415 +/- 0.4841. Mean 207.03, seed-to-seed sd 0.20.
**Claim reads 207.0 +/- 0.52** -- the LARGER of block-average error and seed sd. Keep it
that way: the seed sd measures chain reproducibility, not how well the number is known.

Seed 1 is the low one and is also the seed the old 3 h reaper restarted. Do not over-read
that: a restart re-runs deterministically from the same seed, so it cost wall-clock and
not accuracy, and 0.35 sits inside every one of the three block errors.

**The campaign's scientific objectives are met.** Nothing further is required of a session.

### ⚠ REAPER BUG — fixed 09:19, do not reintroduce
`bin/reap.py <hours>` releases claims older than the threshold as orphaned. The supervisor
called it with **3 h**, but claim-grade runs take **~11-12 h**, so every claim-grade task
was reaped mid-run, re-claimed and restarted from zero — an unbreakable loop that can
never yield a result. It looked healthy: the log said "reaped N stale claims" and fresh
`work/res/AZ*.csv` timestamps looked like progress when they were restarts. Now **24 h**
(`bin/supervise2.sh`), verified live. **If you change task cycle counts, check this
threshold against the longest task.**

### If a session is still alive, in priority order
- [ ] **Nothing, by default.** One `bin/status.sh`, act only on something wrong, end turn.
- [ ] Check the falsifier: `data/freebound.txt`. 0 of 98 uniform-random draws exceed
      B=207.12; best draw 186.2. A single draw above B withdraws the ceiling claim.
- [ ] If claim-grade rows for the leader appear: confirm REPORT.md §1 names **one**
      material (`[ASR]6` and `[FSR]6` are the same material — see the dedup section) and
      that the screen→floor→claim consistency row for it looks sane.
- [ ] **Never promote a sub-floor number into the Claim.** 207.12 is a 500+2,500 screening
      value, below the §3 floor of 2,000+10,000 for *any reported number* and far below
      the 10,000+50,000 the Claim requires. The temptation at the end is to headline the
      bigger number. §3 forbids it and the report already handles it correctly.
- [ ] Do not restate the hypergeometric bound over 9,144 distinct materials without
      correcting for size-bias; it is valid over the 12,499 entries and that is on-mandate.

### Closed, do not reopen
Modification arm (methylation lost capacity on all parents; uphill direction untested and
now out of budget) · tier `G` void-fraction edge · tier `H00` λ-robust union · grids
(retracted notice; declined on cost, compute was never the binding budget).
