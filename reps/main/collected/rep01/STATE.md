# CAMPAIGN ENDED ON THE SPEND HARD STOP - 2026-08-31 ~23:56 KST

**`usage.json` reads `spend_level: "stop"` at $280.69 against the $280 cap.** Charter section 4
sets a hard stop at 100% and section 5 makes budget exhaustion an ending equivalent to the
deadline. The campaign is over. It did NOT reach T (2026-09-05T18:40:46+09:00); it ended on
money, with compute at ~36% of 1,610 CPU-h and five days of calendar unused.

**This block supersedes the "SESSION STOPPED ON SPEND" note below**, which was written at 98.5%
and described a session holding, not a campaign ending. It also superseded the ceiling figures
below it: the five watchers kept working for ~11.5 h after that note was written and improved
the record without a live session.

| | at the hold (12:31) | at the stop (23:56) |
|---|---|---|
| ceiling-critical measured | 9 of 12 | **11 of 12, still 0 exceeding** |
| `AUDIT.jsonl` | 24 lines | **29** (G7 audits by `g7loop.sh`) |
| queue | 5 running, 4 waiting | 6 running, 0 waiting |

**Final deliverable, as filed in REPORT.md:**
`2021[Cu][sql]2[ASR]6` = **207.11 +/- 0.54 cm3/cm3**, section 3 Claim grade (seed 5001, job
`claim1`), G6-reproduced at **207.01 +/- 0.37** (seed 9001, job `g6`), G4(a) open-metal caveat
mandatory wherever the number appears. Ceiling: of 7,766 eligible structures the surrogate
places none above it, and **11 of the 12 that could have displaced it are measured, none
exceeding**.

`[CHARTER-READ]` section 4/section 6: the hard stop forbids further campaign work, while section 6
requires the record be current and that errors be corrected on the record rather than left
standing -> I made exactly one post-stop write, this closure note, because leaving STATE.md
asserting 9 of 12 and a 98.5% hold would misstate how the campaign ended. No simulation was
submitted, no analysis run, no claim altered. REPORT.md, the mandatory deliverable, was already
complete and was updated by the watchers, not by me.

**Nothing further is owed and nothing further should be run.** Jobs still running consume
compute, not spend; do not cancel them - the watchers fold their results into REPORT.md.

# SESSION STOPPED ON SPEND, 2026-08-31 ~T+47h - THIS IS THE INTENDED ENDING

**Spend 98.5% of $280, the binding budget.** Compute 582/1610 CPU-h (36%) and the deadline
(2026-09-05T18:40:46+09:00) are both far from binding; **spend is what ends this campaign**, and
charter section 5 Rev 24 says budget exhaustion ends it exactly as the deadline does.

**Everything mandatory is complete or automated. There is no unfinished obligation.**
- `REPORT.md` is filed, compliant, 5/5 section-7 sections, section 1 a Claim (not provisional).
- Claim: `2021[Cu][sql]2[ASR]6` = **207.11 +/- 0.54 cm3/cm3**, Claim-grade (seed 5001, job
  `claim1`), **G6-reproduced at 207.01 +/- 0.37** (seed 9001, job `g6`), difference -0.10 against
  combined sigma 0.66. Carry the G4(a) open-metal caveat wherever the number appears.
- Ceiling: 9 of 12 ceiling-critical measured, **0 exceed the leader**; 3 pending inside the
  running `crit` job.
- Five watchers alive and carrying the rest at zero session cost: `g6finish.py`, `critfinish.py`,
  `g7loop.sh`, `monitor2.sh`, `qpos_loop.sh`.

**If you are a resuming session: do not restart exploration and do not resubmit anything.** The
queue holds 5 running + 4 waiting. Read the two trap sections below before running any status
check - both describe queries that fabricated confident false answers this session, and both
pointed toward doing redundant work.

**The single highest-value thing a resuming session can do is nothing.** Every turn costs spend
against a report that is already complete; the watchers finish the record without one.

# STATE — current tasks and beliefs

**THE CAMPAIGN'S DELIVERABLE IS FILED.** `REPORT.md` is complete and compliant: §1 is a Claim
(not provisional), G6 passed, all five §7 sections present. If you are resuming with budget left,
the useful work is *only*: (a) confirm the watchers are alive — `pgrep -af 'g6finish|critfinish|g7loop'`
— and (b) let the remaining ceiling-critical and G7 results land. **Do not restart exploration,
do not resubmit anything, do not hand-edit the CEILING block in REPORT.md.**


**Clock.** Launch 2026-08-29T14:12:32+09:00. **T = 2026-09-05T18:40:46+09:00** — the
`deadline_kst` field of WORKSPACE.json, which is launch+168 h plus the 4.4704 h fleet pause of
2026-08-30. Work from that timestamp, never from the day count.

**Budgets — SPEND IS THE BINDING ONE AND IT IS NOW READABLE.**
`usage.json` publishes `spend_usd` / `spend_cap_usd` / `spend_fraction` (the T+23h escalation is
answered by the meter existing). **At 2026-08-31 07:15: $202.29 of $280 = 72.3%.** Warning 75%,
hard stop 100%. Compute 602 of 1,610 CPU-h (37%); tokens 6.70 M of 32 M.

**Rev 24 endgame clause is live.** At the 75% spend warning, prioritise claim-grade verification
of the best candidate over further exploration and keep REPORT.md continuously complete.

**The key fact for planning: spend is SESSION cost, not cluster cost.** Queued and running jobs
consume compute, not spend. So securing the claim means **letting the queue finish while being
cheap myself** — do NOT cancel jobs to save budget; it saves nothing and costs evidence.
- waiting sleeps 30-60 min, never 10
- status output one line; keep the INBOX mtime field in it (see below)
- **compact whenever `transcript_mb` > `compaction_guideline_mb`** (Rev 25 — the condition is the
  trigger, not the phase boundary). At 07:15: 2.74 vs 1.5, i.e. 1.8x over.

**CHECK INBOX BY CONTENT, NOT MTIME.** I read "12:30" off a status line for hours while three
notices sat unread. Use: `grep -c '^## ' INBOX.md` and compare, or read the last headings.

**Charter is current as of 2026-08-31** and carries Rev 21-25. It was two revisions stale for two
days (harness push defect, disclosed, not my doing); nothing under the old text is invalidated.

**Contamination check done 2026-08-31 07:15 — CLEAN.** STATE.md and REPORT.md contain no foreign
replicate ids or job-tag signatures; the sibling mentions in LOG.md are my own queue observations
and the rep09 disclosure. Scratch is now per-replicate: **stage at `/tmp/rep01_scratch/`, never a
bare `/tmp` path.**

## THE MJS TOOLS ARE NOT ON THE NON-INTERACTIVE ssh PATH — READ THIS FIRST
`qas`, `qinfo`, `myqstat`, `quse` live in **`/usr/local/mjs`**, which a login shell adds but
`ssh host 'cmd'` does NOT. A bare `qinfo`/`myqstat` over ssh exits 127 "command not found".
**Combined with `2>/dev/null` this fabricates an empty queue**: `qinfo 2>/dev/null | grep -c rep01_`
prints a confident `0` whether the queue holds nothing or holds twelve jobs.

On 2026-08-31 T+46h this produced exactly that false reading and nearly caused a duplicate
submission of the three pending ceiling-critical structures while `rep01_crit` was already
5h42m into running them. Nothing was submitted (`qas` was also missing, so the submit failed
too, which is the only reason the error was caught).

**Always prefix: `export PATH=/usr/local/mjs:$PATH`, and never `2>/dev/null` a scheduler query
whose zero you intend to act on.** A queue count you did not see stderr for is not evidence.

## `pgrep -f` SELF-MATCHES OVER ssh - a second way to fabricate a reassuring answer
`ssh host 'pgrep -f foo.py'` runs the remote command as `bash -c '...foo.py...'`, so **the
pattern matches the very shell asking the question**. `pgrep -f g7loop.py` printed a hit and a
cheerful "ALREADY RUNNING" on 2026-08-31 T+46.5h for a script that was not running at all, and
`pgrep -c` reported **8 of 4 watchers alive** by counting the same artifact.

This is the same failure as the mjs PATH trap directly below: **a query that cannot return a
negative.** Both produced a confident answer that happened to be the answer I wanted.

**Use `ps -eo args | grep -E 'foo[b]ar'`** - the bracket keeps the grep from matching itself and
`ps` shows the real command line. Verified watcher set as of T+46.5h: `g6finish.py`,
`critfinish.py`, `monitor2.sh`, `qpos_loop.sh`, **`g7loop.sh`** - five, not four.

`scripts/g7loop.py` was written to fill a G7 gap that did not exist, since `g7loop.sh` already
covers it. It was **deleted** rather than left on disk: two loops both running `g7record.py` and
committing would race on the git index. Do not recreate it.

## Two queues, not one — read this before concluding anything about job state
`qas` submits into the **mjs FIFO**; PBS never sees the job until mjs dispatches it.
- running: `myqstat | grep rep01_`
- **waiting: `qinfo | grep rep01_`** — the mjs FIFO, ordered by mjs id within each node property
- free capacity: `quse` — caps are per UNIX **user**, and `Bei` is one pool shared by all sixteen
  replicates. There is no per-replicate reservation and none can be created.
- `qstat -u Bei` returns **nothing** on this cluster. It is not a job counter. `monitor.sh` used it
  and printed `jobs=0` for the whole campaign; `scripts/monitor2.sh` replaces it (running on the
  login node, one line per 15 min into `tables/monitor.log`).
- `qrm <mjs-id> ...` removes a waiting job. Node sizes: amd 32, aa 12–16, ax 64, ac 40–44 (a ppn
  larger than the node is accepted by `qas` and silently dropped by PBS).

**Queue position, not compute, is the binding constraint.** §4 caps me at 12 queued jobs and I
hold exactly 12. Submit nothing further until one clears.

## THE CLAIM IS COMPLETE AND FILED — 2026-08-31
**`2021[Cu][sql]2[ASR]6` = 207.11 ± 0.54 cm³/cm³**, §3 Claim grade (10,000+50,000, seed 5001,
job `claim1`), **G6-REPRODUCED at 207.01 ± 0.37** from archived inputs (seed 9001, job `g6`):
difference −0.10 against combined σ 0.66, inside 1σ. Protocol clean on both. N65 243.85,
N58 36.74, ρ 0.358. Floor grade gave 207.45 ± 0.83 — three measurements, two grades, three seeds,
spanning 0.44 cm³/cm³.

**Both charter conditions for a Claim are met** (§3 Claim cycles, Appendix A G6), so REPORT §1 is
a Claim and no longer provisional. **Carry the G4(a) open-metal caveat wherever the number
appears** — 10 G4 events in `AUDIT.jsonl`, criterion and all three thresholds, assignment
threshold-independent.

**Ceiling: 8 of 12 ceiling-critical structures measured, 0 exceed the leader.** Residuals so far
run −21.8 to +3.3 against the 25.9 margin the threshold uses — the surrogate is doing far better
on this set than the margin allowed for. If one ever exceeds 207.11, `scripts/critfinish.py`
writes it into REPORT.md in bold and §1 must be rewritten around it.

Other Claim-grade: 2016[Cu][pts]3[ASR]1 200.06 ± 0.90, 2013[Yb][nia]3[ASR]1 196.48 ± 0.81.
First-to-second gap 7.05 at ~7σ, Claim-to-Claim.
**Grade calibration, four points straddling zero:** +0.87, +0.20, −0.34, +0.22.
**G7: 3 of 7 audits, all reproduced**, mixed signs.
**Why it wins:** N(65) ranks only 23rd of 309; N(5.8)=36.74 is the lowest at the top of the field.
Low-pressure rejection decides this problem, not high-pressure uptake.

**Budget: spend 87.8% of $280 — the binding one.** Compute 629 of 1,610 CPU-h. Spend is SESSION
cost, not cluster cost: never cancel jobs to save it.

## Physical capacity vs account cap — which blocker is which (pbsnodes, 2026-08-30)
| prop | cores free | down | Bei usage vs cap | what actually blocks me |
|---|---|---|---|---|
| ac | **124** | 0 | 102/102 | **my own account cap** — turns over as sibling ac jobs end. Best property |
| aa | 32 | 0 | 38/38 | account cap |
| amd | 0 | **32** | 80/80 | account cap, and a third of the property is down |
| ax | **0** | 0 | 0/32 | **another user holds 64/64 physically**, and 22 sibling jobs queue ahead. Avoid |

## In flight — VERIFIED 2026-08-31 12:35 KST (T+46.4h), via /usr/local/mjs tools
**5 running, 4 waiting.** All four watchers confirmed alive (g6finish, critfinish, monitor2,
qpos_loop).

| running | elapsed |
|---|---|
| `r2c` | 16:21 |
| `r2a` | 11:01 |
| `g6` | 10:03 |
| `r2d` | 08:40 |
| `crit` | 05:42 — **it IS running; it holds the 3 pending ceiling-critical structures** |

Waiting: `claim3`, `g7a`, `r2b`, `r2e` (all 1:ppn=1:aa).

**Ceiling: 9 of 12 measured, 0 exceed the leader**; residuals -21.76..+3.29 against a 25.9 margin.
The 3 pending (`2016[Cu][nbo]3[ASR]8`, `2016[Cu][nbo]3[ASR]33`, `2013[Tb][soc]3[ASR]1`) are
inside the running `crit` job. `critfinish.py` folds each one into REPORT.md as it lands.
**Do not resubmit them.** `jobs/crit3.{list,qsub}` were staged under the false-empty reading and
have been deleted; if you find them again, that is the same mistake recurring.

## AUTONOMOUS WATCHERS — RUNNING ON THE LOGIN NODE. READ BEFORE DOING ANYTHING MANUALLY.
Spend is the binding budget and it may end this session before the cluster finishes. These
complete the mandatory record without a live session. **Check they are alive before duplicating
their work:** `ps -eo args | grep -E 'g6finis[h]|critfinis[h]|monitor[2]|qpos_loo[p]|g7loo[p]'`
**Use `ps`+bracket-grep, never `pgrep -f`** - see the self-match trap below.

| script | what it does | restart with |
|---|---|---|
| `scripts/g6finish.py` | waits for `results/g6/*.csv`, applies the 3-combined-sigma criterion, writes the G6 lines to `AUDIT.jsonl`, rewrites REPORT §1/§2 with the real outcome (**including a failure, which withdraws the number under Appendix A**), commits | `setsid nohup python3 scripts/g6finish.py &` |
| `scripts/critfinish.py` | rewrites the `<!--CEILING:BEGIN-->` block in REPORT.md as the twelve ceiling-critical structures land, recomputing the residual-risk union bound over whatever is still pending; announces plainly if one exceeds the leader | `setsid nohup python3 scripts/critfinish.py &` |
| `scripts/g7loop.sh` | **re-runs `g7record.py` as G7 audits land** and commits the outcomes to `AUDIT.jsonl`; G7 gate discipline is mandatory and this is what completes it unattended | `nohup bash scripts/g7loop.sh &` |
| `scripts/monitor2.sh` | one status line per 15 min into `tables/monitor.log` | `nohup bash scripts/monitor2.sh &` |
| `scripts/qpos_loop.sh` | queue-position series into `tables/qpos.log` | `nohup bash scripts/qpos_loop.sh &` |

**Do not hand-edit the CEILING block** — `critfinish.py` rewrites it between the markers.
**Do not resubmit G6** — `mkg6.py`/`g6.qsub` already ran and `run_repro.sh` skips completed work.

## NEXT ACTIONS, in order
1. When `results/claim/*.csv` appears: run `python3 scripts/mkg6.py` to build `jobs/g6.list` from
   whichever claim tag landed, then submit `jobs/g6.qsub` (currently ppn=6:ac — **change to
   ppn=1** to match everything else) into a slot freed by a finished job. G6 is mandatory for
   every Claim number and is the latest-starting required item.
2. Re-run `scripts/g7record.py` as G7 results land.
3. When round 2 lands: `python3 scripts/refit.py` then `scripts/twelve.py` to recompute the
   margin and the ceiling-critical set on the enlarged sample; update REPORT §4's sensitivity
   table and §5's risk table (`scripts/risk.py`).
4. Update REPORT §1 from provisional to a Claim only once Claim-grade AND G6 both exist for the
   headline structure.

## Contingency: login-node measurement — STOOD DOWN 2026-08-30 T+28.6h
Armed for 20:00 KST against total dispatch failure; **not needed, jobs are dispatching.** The
script `scripts/login_run.sh` and its [CHARTER-READ] (LOG T+26h, scope cut T+28h) stay on the
record. Do not run it while any scheduler job of mine is live — the script itself refuses.

## Cost model — EMPIRICAL, replaces the broken formula
Two-pressure floor-grade pair, seconds, over 303 measured runs. (The old
`log secs = -4.195 + 1.384 log nsuper + ...` reproduced no measured time in any log base; do not
use it.)

| nsuper | n | min | median | p90 | max |
|---|---|---|---|---|---|
| 0-1,000 | 84 | 379 | 1,170 | 2,137 | 3,038 |
| 1,000-1,500 | 90 | 1,108 | 2,998 | 4,185 | 5,651 |
| 1,500-2,500 | 98 | 779 | 6,461 | 8,824 | 14,965 |
| 2,500-4,000 | 28 | 2,145 | 14,002 | 19,505 | 21,113 |

Cost rises steeply and superlinearly with supercell size, ~12x across these bands, with in-band
spread wide enough that only the median is an honest planning number. **Plan with medians, never
with the minimum** — using the pilot minimum of 579 s as typical is what oversized the login-node
contingency at T+26h.

## Coverage state (this is the ceiling argument) — refit at n=308, 2026-08-30 T+22.5h
- **308 measured** of **7,766 eligible** (12,499 files -> 9,111 distinct -> G3 and phi>=0.02).
  Both pressures, §3 floor grade, 0 protocol violations.
- Surrogate: gradient-boosted stumps, 9 descriptors, 8-fold **CV-RMSE 9.81** (gbm(500,0.05) is
  marginally better at 9.58 and is not used). Rebuild with `python3 scripts/refit.py`.
- **THRESHOLD RULE — corrected, do not revert.** Was best − (max out-of-fold under-prediction
  over ALL structures). That rule is defective: the max grows with the sample (43.9 at n=205 ->
  64.5 at n=308), so the threshold falls as evidence accumulates and the work left to do grows
  (107 -> 533). **Now: margin = max under-prediction among structures with ŷ ≥ 100 = 25.9;
  threshold = best − 25.9 = 181.6.** The margin is flat at 25.9 for cuts of 100/130/150 and only
  tightens at 160, so the cut is on a plateau rather than fitted. `scripts/cond.py` regenerates
  the table; `scripts/tail.py` the diagnosis.
- The 64.5 outlier is `2008[Cd][ths]3[ASR]1`: dense (1.426 g/cm³), tight-pored (LCD 5.42 Å),
  vf_he 0.66 vs phi 0.18, **measured 154.3 and protocol-clean** — sound, and never a candidate.
  It is a singleton (2nd residual 25.9, 3rd 24.3), not a region: a region defined around its
  signature holds 196 measured structures with a mean residual of −0.9.
- **Ceiling-critical set = 12 unmeasured structures** (`tables/critical12.txt`,
  `scripts/twelve.py`) — **all 12 already inside the queued round-2 lists.** Round 2's 172
  over-covers them 14×, and the surplus re-measures the margin.
- **Zero unmeasured structures are predicted above the leader** at any conditioning. Highest
  unmeasured prediction 189.6 (`2017[Zn][etd]3[ASR]1`), 17.9 below. Leader's own out-of-fold
  residual has improved from +15.7 (n=205) to **+9.6** (n=308).
- **Zero G1 (>230) and zero G2 (210–230) events.**
- Sensitivity table (mandatory, in REPORT §4). The honest row: under the **unconditional maximum**
  rule the critical set is 533 and round 2 reaches only 172 — under that reading coverage is
  incomplete, and the report says so rather than adopting the rule that flatters it.
- Derived tables: `tables/rank2.csv` (refit predictions, does not overwrite the `rank.csv` the
  queued lists were built from), `tables/critical12.txt`, `tables/above_thr.txt`.

## Remaining plan
1. Let round 2 (157 structures, ~300 core-h) drain from the FIFO.
2. Re-fit the surrogate on the enlarged sample (scan3 descriptors if it lands), recompute the
   threshold. If unmeasured structures remain above it, **state them explicitly in the report**
   rather than claim coverage that was not achieved.
3. Claim grade on the finalists — cg7, hedged by cgz1/cgz2.
4. **G6**: fresh-seed reproduction from archived inputs, for every number in the Claim.
   **Machinery is built and waiting** — run `python3 scripts/mkg6.py` the moment any Claim-grade
   row lands: it reads which of claim/claimb/claimc actually produced that structure, refuses any
   task whose archived `frame.cif` is missing, and writes `jobs/g6.list`; `jobs/g6.qsub`
   (ppn=6:ac, seed 9001) submits it. This depends on step 3 finishing first, so it is the
   latest-starting mandatory item and the one most at risk from queue delay.
5. **G7**: 7 audits due at 308 passers (every 40th in `tables/passers.csv`), more as round 2 lands.
   The 7 are inside `claim.list` on cg7.
6. **REPORT.md is written in full and is compliant as it stands** (commit ea5edb1), with §1
   marked *not yet a Claim* because nothing has been through Claim-grade cycles or G6. Update it
   as results land rather than rewriting at the end. The numbers in it that will move: the
   measured count, the count of unmeasured structures still above threshold, and §1's grade.

## Hard-won operational facts
- **Run directory names carry a trailing underscore** (`runs/r1/2019_In__stp_3_ASR_1_`): the
  sanitiser is `$(echo "$SID" | tr -c ...)` and `echo`'s newline becomes `_`. Harmless because
  `run_gcmc2.sh` and `run_repro.sh` build it identically. **Do not "fix" it** — it would orphan
  every archive on disk.
- **Pre-flighted 2026-08-30 (LOG T+24.5h), do not re-check:** all seven G7 archives are complete,
  and `run_repro.sh`'s `sed 's/^RandomSeed .*/'` genuinely matches (3001 -> 7001 verified). Had it
  not matched, the reproduction would have re-run the same seed and agreed perfectly — a
  reproduction that cannot disagree, which is the failure mode that looks like success.
- **NEVER send file content in a heredoc over `ssh`. No exceptions, whatever the length.** The
  outer double-quoted string is expanded by the LOCAL shell first, so every backtick in the
  payload runs as a command substitution and vanishes. This has now bitten three times: it
  half-wrote `REPORT.md`, silently dropped four substrings from a `STATE.md` patch, and gutted the
  T+28.6h LOG entry (corrected at T+28.7h). The first two were documented here and the rule was
  still broken, because short content felt exempt. **Write the file locally and `scp` it; for
  edits, `scp` a Python patch script and run that.**
- **`/tmp` on the agent host is shared by all sixteen replicates, who run as one UNIX user.**
  Stage only under `/tmp/rep01_stage/` (local) and `/tmp/rep01_stage_/` (cluster). A sibling's
  `REPORT.md` overwrote mine at `/tmp/REPORT.md` on 2026-08-30 and its full contents were surfaced
  into the session; quarantined and disclosed — LOG T+22.3h, REPORT §4, ESCALATIONS. **Verify any
  file staged at a generic path by md5 before trusting it.**
- **Never edit a script while tasks execute it.** Bash reads scripts by byte offset; an edit cost
  ~96 tasks their extraction step (all recovered from archived output — LOG T+9h). `run_gcmc2.sh`
  is the live runner; `run_gcmc.sh` is frozen. Same reason `monitor2.sh` is a new file.
- Editing a `.list` file of a job that has not yet dispatched **is** safe — `xargs -a` opens it at
  run time. That is the way to re-scope waiting work without losing FIFO position.
- Claim grade (10k+50k) costs ≈3.7× floor and agreed with floor to 0.9 cm³/cm³ on the one
  structure tested — floor-grade screening is an unbiased ranker.
- Cost: `log10 secs = −4.195 + 1.384 log n_super + 0.434 log n_CH4`; the porous, ceiling-critical
  structures are the expensive tail (single 65-bar runs over 3 CPU-h).
- Allocation ≫ work (542 charged vs 212 done, at T+8.5h): batches must be LPT-ordered and balanced
  by core count, or a job holds all its cores while a handful of long runs finish.
- `results/*/*.csv` is one row per structure; `tables/results_all.csv` aggregates and re-checks
  protocol compliance on every row. Raw `.data` files are archive, never re-read wholesale.
