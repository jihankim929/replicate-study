# STATE — current tasks and beliefs

## FILED 2026-09-01 03:50 KST — campaign closed early under charter section 5

**CLAIM (final): 2021[Cu][sql]2[FSR]6 = 206.9 +/- 0.5 cm3/cm3** methane working capacity,
N(65 bar) - N(5.8 bar), 298 K, absolute loading. Claim grade 10,000 + 50,000 cycles, G6-reproduced
under a distinct seed (repeat 207.5, deviation 0.56 vs combined sigma 0.99). Screening first found
it at 207.17 +/- 1.23: three independent measurements, two cycle counts.

**CEILING (final):** at or very near the achievable maximum for this database and protocol. A
444-geometry uniform sample reaches 188.6 with nothing above 190 => <=78 of 9,143 (0.9%) exceed 190
at 95%; the out-of-band probe finds nothing near the record; the model top-300 predicted band is
100% measured; EVT shape parameter negative at every threshold. The endpoint estimate is NOT quoted
as a bound. No specific numerical ceiling is defended.

**Why filed early rather than run to the 09-06 deadline.** Both deliverables are complete and
verified; all queued compute finished (2,143 runs, 989 distinct geometries, 1,490 of 1,610 CPU-h);
enforce_budget leaves only ~23 CPU-h of usable discretionary headroom, which buys ~25 more uniform
draws and moves the 190-bound from 78 to ~74; and spend stands at 92.8% with ~$20, which cannot
fund anything material. Further turns would burn budget and produce nothing. Charter section 5 permits
early filing when the mandate is complete, and section 9 prefers a correct filed result to an ambitious
unfiled one.

**Closing actions taken:** autopilot stopped so the verified REPORT.md is frozen rather than
regenerated after review; idle worker jobs released back to the shared queue (the harness reported
other replicates starving for queue positions, and my queue is drained).

**If this session is resumed:** the campaign is FILED. Do not queue new work. REPORT.md at the
workspace root is the deliverable and has been read end to end, section by section, against live
numbers. Every figure in it is computed at generation time; none is transcribed.


## MANDATE ANSWERED 2026-09-01 01:30 — both halves. Report is final-quality.

**CLAIM: 2021[Cu][sql]2[FSR]6 = 206.9 +/- 0.5 cm3/cm3**, claim grade 10,000+50,000, G6-reproduced
(repeat 207.5 +/- 0.9, deviation 0.56 vs combined sigma 0.99). Screening first found it at
207.17 +/- 1.23, so three independent measurements agree across two cycle counts. seedcheck: 30
claim/repro pairs campaign-wide, **0 seed collisions**. REPORT.md status: claim-grade and
G6-reproduced (no longer PROVISIONAL). Runner-up 2016[Cu][pts]3[ASR]1 199.6 +/- 0.7 (repro 199.8).

**CEILING:** at or very near the achievable maximum. 403-geometry uniform sample (ctrl2+ctrl3)
reaches 188.6 with nothing above 190 => <=~86 of 9,143 (0.9%) exceed 190 at 95%; out-of-band probe
puts <=124 of 8,363 above the record; EVT xi negative at every threshold with endpoints 173-198
for thresholds >= the 70th percentile. Top-100 predicted band fully measured, top-300 ~99.7%.

**Three report defects found and fixed in the last hours — all the same shape, a sentence
rendered for the state the code EXPECTED rather than the state it was IN:**
1. section 1 said "the best validated material is" on cycle count alone while the header said
   PROVISIONAL and section 4 said G6 NOT DONE. Branch keyed on claim_grade, ignoring repro_ok.
2. `collect()` broke ties with (prod, wc), so between a claim run and its own G6 repeat it took
   whichever came out HIGHER — selection on outcome, biasing every repeated geometry up by ~0.5
   sigma. Now ranks (prod, tag rank, wc) with claim outranking repro: the RUN is reported, the
   repeat is the check.
3. Evidence table still said the spend meter "does not exist" (true when written, false since
   2026-08-30) and used a token proxy that understated 24.6% against 87% actual.
=> **Before filing, re-read section 1 and the evidence table against the live numbers.** Auto-generated
prose goes stale silently.

**Budget: spend 87.7% ($245 of $280) is what will end this campaign, not the 09-06 deadline.**
Compute 1,461/1,610 (90.8%), queue drained. enforce_budget cuts discretionary rows at 1,513.
Remaining useful compute ~40 CPU-h -> queued as ctrl4 to tighten the ceiling bound.


## POSITION 2026-08-31 18:10 — claim grade is landing; ceiling sample being enlarged

- **14+ structures complete at claim grade**, 8+ G6-reproduced, agreement excellent:
  srs 197.56 / repro 197.38 | nia 193.81 / 194.08 | ith 190.92 / 190.68 | pcu 190.01 / 189.85 |
  lvt 186.89 / 187.13 | nts 185.46 / 185.44 | ith2 182.30 / 182.44 | nan 182.22 / 182.25.
- **Best VALIDATED (claim grade + G6): 2015[V][srs]3[FSR]1 = 197.56 +/- 0.84** (repro 197.38).
  REPORT.md names this and says it is the claim if the campaign stops first.
- **2016[Cu][pts]3[ASR]1 claim grade = 199.61 +/- 0.71** (floor 200.43); G6 repeat queued.
- **The 207.2 leader 2021[Cu][sql]2[FSR]6 is still running its 65 bar claim leg.** At 13:30 it
  was cycle 20,000/50,000 having started 05:40, so ~15.6 h total, landing ~21:15 today. It is
  slow because cost scales with loading and this is the highest-uptake structure in the campaign
  — the 8.37x claim/floor factor in STATE above is a fleet average, not a per-structure law.
  Its 5.8 bar leg already landed at 36.83.
- **REPRO_CAP was full at exactly 10 when I checked (13:38).** Same flat-cap trap as the claim
  cap — the leader would have been permanently denied its G6 repeat with the gate showing a
  complete reproduction wave. Fixed with the same N_MUST exemption; verified 10 -> 12. **This is
  the FOURTH defect of this family.** Any remaining cap or one-shot: assume the leaderboard moves.
- **ctrl3 queued (108 draws, 101 fresh, 93.5 CPU-h)** to spend idle compute on the ceiling bound,
  which is limited only by sample size. Uniform sample goes 288 -> 408 geometries; expected to
  take the 95% bound on geometries above 190 from <=120 to roughly <=85. Pools with ctrl2 (both
  geometry-uniform, successive draws without replacement); ctrl200 stays separate and unpooled.
- Compute 1,304 / 1,610 with ~200 CPU-h now pending. Spend **80.5%**. screen_ok permanently False.
- Turn cost is holding at ~$0.13-0.40 with the lean pattern (one ssh call, one line of prose).


## COMPUTE METER — prediction CONFIRMED and closed out 2026-09-01 04:01
- The 08-31 entry below predicted that `cpu_h` (finished-job basis) would stay at 0.0 while the
  72 h workers ran and would jump once they ended, and that either meter read alone would badly
  under-read at some point. Both happened: on releasing the workers at 03:55, `cpu_h` went
  0.0 -> 726 -> 862 -> **1,490.0**, landing exactly on `cpu_h_scheduler`'s 1,490.0. The two
  meters reconcile; neither is safe alone mid-campaign. Recorded as observed, not inferred.

## COMPUTE METER: `cpu_h` is now present and reads 0.0 — that is CORRECT, not a fault (05:56)
- usage.json now carries BOTH: `cpu_h_scheduler` = 893.77 (cput of jobs CURRENTLY in the
  scheduler) and the restored validated `cpu_h` = **0.0**, basis "finished-job PBS cput".
  It reads zero because **none of my 11 jobs has finished** — they hold 72 h walltimes.
  `cpu_h_runs_accounted: 0` confirms it.
- **They are complementary, not competing: true total ~= cpu_h (finished) + cpu_h_scheduler
  (running).** Today that is 0 + 894. When the jobs expire 09-01/02, cpu_h_scheduler collapses
  toward zero and cpu_h jumps. **A tool reading either one alone will badly under-read at some
  point in the campaign** — cpu_h now, cpu_h_scheduler later.
- My `cpu_ledger` (high-water cput PER JOB ID, never forgotten) reads 905.6 and is the safe
  basis. autopilot cpu_h_used() takes max(internal, usage.json, ledger), so a 0.0 cannot pull it
  down. Verified — no change needed. Do NOT "fix" anything here.
- Escalation answered: the login-node abuse I reported was confirmed and measured — bnode0 at
  load 85.5/96 with 75 unscheduled `simulate`, longest 3.9 h against a 30 min limit. Mine were
  none of them. Unscheduled execution reaches NEITHER meter, so it is invisible to the cap.
- usage.json also publishes `transcript_mb` 1.04 against `compaction_guideline_mb` 1.5. Context
  is the cost driver; keep tool output tiny and prose short.


## ENDGAME CONFIGURATION SET 2026-08-31 05:30 (Rev 24 triggered early, at 72% spend)

The binding budget is SPEND and it is 72%. The campaign is now arranged so that the Claim is
secured first and everything else fills the gaps behind it.

1. **Claim rows are ordered by measured capacity, descending.** `prioritize()` previously kept
   append order within the claim class, so the current record — queued 04:41, AFTER the wave —
   sat behind sixteen older claim rows. A claim-grade 65 bar run costs 8.37x its floor twin,
   about **5.7 h of wall-clock on one core**, so this ordering decides whether the leader is
   verified hours before the budget stops or hours after. Leader is now row 1.
2. **838 unclaimed screening rows outside the top-100 band were cut** (~388 CPU-h) so the claim
   runs take cores immediately instead of queueing behind discretionary work.
3. **That flipped `screen_ok` back to True** — pending fell to 100 and the guard's only test was
   CPU headroom, so the next cycle would have refilled the queue with exactly what was just cut.
   `screen_ok` now additionally requires **zero outstanding claim/repro rows**.
4. **Then 274 rows (137 structures, ~127 CPU-h) of band ranks 101-300 were restored BELOW the
   claim rows.** Workers take the file top-down and the claim rows are already claimed, so this
   cannot delay them; without it ~43 cores would idle for hours while one 5.7 h claim run
   finishes. This also restores the top-300 band coverage the ceiling argument uses.
   Net pending 236 CPU-h; projection ~1,129 / 1,610 (70%).

**Compute will finish well under budget and that is the correct trade.** Unspent compute is not a
failure; an unverified Claim is. Rev 24 says so explicitly.

**Critical path: ~5.7 h from 05:12 for the leader's 65 bar claim run, then a G6 repeat behind it.**
Until that lands the Claim rests on 2015[V][srs]3[FSR]1 at 197.56 claim-grade, and REPORT.md
correctly labels the 207.2 leader as screening grade and not yet validated.


## GATES: G1/G2 disposition path built 2026-08-31 05:10 (it did not exist)
- The autopilot flagged banded values `flagged_pending` but NOTHING wrote the disposition
  Appendix A requires before promotion. `bin/gate_audit.py` now does, wired into the loop at
  0.25 s: four legs (structure integrity, charge balance, protocol compliance, convergence),
  `unverified` is never a pass, `upheld` only when all four pass. Nothing is in the band yet.
- Two bugs caught by testing it OUT of band: structure names contain literal `[` `]` which glob
  reads as a character class, and run dirs are separately name-sanitised by gcmc_worker.run_one.
  Both made the protocol leg say `unverified` for structures whose outputs were all present.
  It now reads the `rundir` COLUMN from the result rows. Never re-derive a path you already store.
- Gate counts: G3 1100 pass / 130 kill, G4 680 pass, **G7 9 of 9 pass**, G1/G2 none (record 207.2).
- /tmp contamination notice: checked, CLEAN. No foreign workspace path or job prefix in
  STATE.md/REPORT.md or their git history. My writes never staged through the agent host /tmp.

## TURN ECONOMY (the thing that will end this campaign if anything does)
- Spend is 69.2% and rises ~$2-3 per turn regardless of how much wall-clock the turn covers,
  because context is re-read every turn. Turns have been arriving MINUTES apart.
- => Every check-in should carry a long in-turn `sleep` on the cluster side (up to ~540 s inside
  a 600 s tool timeout) so one billed turn advances real time. Do NOT chain short polling turns.
- ~$85 left at ~$2.5/turn is ~30 turns. Reserve ~8 for the endgame (claim-grade leader lands,
  G6 repeat, final REPORT.md read-through). The autopilot regenerates REPORT.md every cycle, so
  a hard stop at any moment still leaves a complete, compliant section 7 report on disk.


## NEW RECORD 207.2, and the cap nearly locked it out (2026-08-31 04:45)

- **Record: 2021[Cu][sql]2[FSR]6 = 207.17 +/- 1.23 cm3/cm3, floor grade, tag screen.**
  Sequence in one day: 197.3 -> 200.4 -> 207.2. Still below G1 (>230) and below the G2 band
  (210-230) even at +1sigma (208.4), so no gate action beyond routine — but the NEXT record
  probably enters the G2 band, so be ready to audit before promoting it.
- **NEAR MISS, now fixed.** The claim wave filled to CLAIM_CAP=16 at 04:16; the new record landed
  at ~04:31 from screening still in flight; `room = CLAIM_CAP - len(havegeo)` was 0, so the best
  structure in the campaign would have stayed screening grade and been **inadmissible as a Claim
  while the gate looked satisfied**. Fixed: `N_MUST=6` top geometries are queued unconditionally
  and only the remainder is capped. A budget guard may bound the TAIL of the leaderboard, never
  its HEAD. Verified 04:41: `claim queued (1)`, the leader is in.
- Lesson that generalises: every cap and every one-shot in this autopilot must be re-checked
  against "what if the leaderboard changes after this fires". That is now three defects of the
  same family (one-shot G6, one-shot claim wave, flat claim cap).

## BAND EXHAUSTION is the real premise of the ceiling claim (2026-08-31 04:45)
- The uniform sample and EVT bound the DATABASE-WIDE distribution, but every record came from the
  top of the RANKED band. So the ceiling claim is only as strong as the band's coverage:
    top-100: 68 measured + 32 queued = **100% covered when the queue drains**
    top-300: ~126 measured + ~173 queued = **99.7% covered**;  rank 300 predicted 158.5
    top-676: ~189 + ~344 = **79% covered**;  rank 676 predicted 146.1
- Beyond rank 300 the model predicts <=158.5, so beating 207.2 from there needs a residual of
  ~+49 against a top-band residual sd of ~3 — a ~10-sigma event.
  **Weak point, stated in the report:** that residual sd is measured on structures the model was
  FITTED to, so it is optimistic by an unquantified amount. Do not present it as a CV number.
- REPORT.md section 1 now says plainly that the record is still rising and that this is a claim about
  where the search CONVERGES, not that it has converged. Section 4 carries the coverage table.
- **The ceiling claim will only be safe once the top-100 band is fully measured.** That is the
  single most valuable remaining compute. It is already queued and at the head of the file.


## G6 CLEAN, and floor grade is biased LOW by ~0.26 (2026-08-31 04:30)

- **Login-node compliance verified** after the harness notice: of the 75 `simulate` processes on
  bnode0, **0 are mine** (they are rep05/rep10 and others; cwd-attributed via /proc). My only
  login-node process is the autopilot decision loop, seconds per cycle. All GCMC is scheduled.
- **G6 independence: 6 claim/repro pairs, 0 seed collisions**, deviations 0.004-0.312 cm3/cm3,
  all within 0.42 combined sigma. `bin/seedcheck.py claim repro`. Reproduction is clean.
- **floor-vs-claim: a real, small, CONSERVATIVE offset.** n=6 geometries with both grades:
  paired mean (claim - floor) **+0.264 cm3/cm3**, sd 0.300, se 0.122, **5 of 6 positive,
  t = +2.15** (two-sided p ~ 0.08 — suggestive, NOT established at n=6).
  Decomposes as 65 bar **+0.142** (5/6 positive) and 5.8 bar **-0.122** (2/6 positive): better
  sampling raises the high-P loading and lowers the low-P loading, and WC is their difference,
  so the two add. Physically the right shape for an equilibration effect.
  **Consequences, all benign:** (i) common-mode, so the floor-grade RANKING is unaffected;
  (ii) floor grade reads LOW, so the uniform-sample tail bounds behind the ceiling claim are
  conservative by ~0.26; (iii) the headline is claim grade + G6, so it does not inherit it.
- mkreport.py used to print "too few structures to rule out a systematic offset" in exactly the
  case where one had appeared. Corrected: it now states the sign, the size, the honest p, the
  decomposition and the three consequences. 10 more claim-grade structures are queued and will
  settle whether t=2.15 survives.


## CEILING: ANSWERED 2026-08-31 05:00 — and the old numbers were WRONG, biased LOW

The ceiling half of the mandate now has a defended answer. Getting it required correcting the
unbiased sample, which two separate defects had been corrupting in the same direction.

**Defect 1 — the sample was drawn over ENTRIES, not GEOMETRIES.** ctrl200 was 200 draws from the
12,499 database entries; ctrl2 was 300 draws from the 9,143 distinct geometries. 3,356 entries are
ASR/FSR charge-assignment twins, so an entry-draw over-weights a geometry by its multiplicity. That
would be harmless if multiplicity were unrelated to capacity. **It is not:** on the clean ctrl2
draw, multiplicity-1 geometries mean **74.07** and multiplicity>1 geometries mean **45.95**,
difference **-28.1 +/- 5.1, t = -5.5** (and -35.8, t = -8.1 over all measured). The entry-draw
therefore over-samples low-capacity material and **biased every tail figure in the campaign low**.
=> ctrl2 alone is the uniform sample over materials. Never pool it with ctrl200 in a claim.

**Defect 2 — ctrl2 could not be recovered by `tag`.** ctrl2.py deliberately does not re-run a drawn
structure screening had already measured (correct: a measurement does not depend on why the
structure was selected). Those members carry tag 'screen'. Every tool selected the sample with
`tag=='ctrl2'` or `tag=='ctrl200'`, so it **silently deleted exactly the members the model had
ranked highly — the upper tail**. It reported the best unbiased draw as 151.9 when the correct
value is **186.7**. A sample with its top cut off makes the ceiling look further away than it is,
which is the flattering direction, which is why it needed finding.

**Fix:** `bin/uniform_sample.py` rebuilds the sample from the seeded draw (ctrl2.SEED=20260830,
deterministic) and looks each drawn geometry up under ANY tag. ceiling.py, evt.py and mkreport.py
all now go through it. Corrections are on the record in LOG.md and in REPORT.md section 4 itself.

**The answer (all from n=288 uniform over geometries):**
- max of the uniform draw **186.7**; **0 above 190**; 2 above 180; 8 above 170.
- 95% Wilson upper bound: **<=120 of 9,143 geometries (1.3%) exceed 190**; <=228 exceed 180.
- Out-of-band probe (the 8,363 geometries the model deprioritised): 256 sampled (3.1%), best draw
  **144.2**, zero exceeding the record => **<=124 of 8,363** could beat 200.4 at 95%.
- EVT on the clean draw is now STABLE where it was not: shape xi negative at every threshold
  (finite right endpoint), and for thresholds >= the 70th percentile the endpoint estimates span
  only **172.7-197.7** against 162-243 on the old entry-draw. P(max > record) = 0 at every one of
  those thresholds; only q=0.60, the least trustworthy, dissents at 220.8.
- Read honestly: an EVT endpoint BELOW the observed record (200.4) does not mean the record is
  wrong — the estimator is bounded below by the sample max and is clearly biased low here. What is
  informative is that it does not OPEN UP: no defensible threshold puts the endpoint far above the
  record. State it that way in the report; do not quote the endpoint as a bound.
- => **Ceiling position: 200.4 is at or very near the achievable maximum. Residual risk is the
  <=124 out-of-band geometries.** REPORT.md now claims this rather than declining to.


## CHECK-IN 2026-08-31 04:20 KST — SUPERSEDES the budget, in-flight and science sections below

### What happened while I was gone
- My session was killed by a harness defect at 2026-08-30 ~13:38 KST and restarted 04:04 on
  08-31. **Deadline extended 14.4324 h to 2026-09-06T14:35:19 KST** (WORKSPACE.json). Cluster
  jobs were never touched and kept producing throughout.
- **Charter Rev 24** (section 5, "Endgame and the spend warning"): budget exhaustion ends the campaign
  exactly as the deadline does; at the 75% SPEND warning, securing a claim-grade verified leader
  outranks further exploration, and REPORT.md must be continuously filable.
- **usage.json now publishes spend** (`spend_usd`, `spend_cap_usd`, `spend_fraction`). The
  "THERE IS NO SPEND METER" note below is obsolete; bin/s.sh now prints the real figure.

### THE 12-HOUR STALL — root cause, fixed
- The login autopilot was ALIVE the whole time (pgrep read 1) but did nothing from 08-30 15:51
  to 08-31 04:10. Cause: it takes `tables/autopilot2.lock` with O_CREAT|O_EXCL and, on EEXIST,
  **silently skipped the cycle and printed nothing**. At 15:51 a worker-hosted copy inside
  rep07_v1 (pid 33103, on v1's node) took the lock and never released it. A pid in a lock is not
  checkable across hosts, so the login copy could never tell.
- Cost: 12 h 14 min with no claim-grade queueing, no G6, no G7, no REPORT.md regeneration.
- **Fixed** in bin/autopilot.py: staleness judged by AGE (LOCK_STALE_S=1200; a cycle takes
  seconds), lock now records `pid host time`, and **a skipped cycle is logged** — the silence is
  what made this expensive. `ap=1` is NOT a liveness check; check that the log ADVANCED.

### Two further defects found and fixed at the same time
1. **Workers take tasks in FILE ORDER** (bin/gcmc_worker.gen reads top-down). append_tasks wrote
   to the END, so every claim-grade / G6 row queued behind all unrun screening. Fixed:
   `prioritize()` now re-sorts the file on every append (claim/repro < g7 < risk < ctrl < screen),
   atomically via os.rename. Screening rows are additionally ordered by the refitted model
   prediction, so workers take the best first and any budget cut falls on the worst.
2. **The claim stage was a one-shot** gated on `'claim' not in waves`, with a trigger
   (measured>=750, or screening drained) that had not fired at 677 measured. It would have spent
   claim grade on an obsolete leaderboard — the record moved 197.3 -> 200.4 while I was down.
   Now **continuous**, like the G6 block: every cycle the top N_CLAIM=12 measured geometries are
   ensured claim-grade, CLAIM_CAP=16, CLAIM_MIN=600. Fired 04:16, queued 10.

### Science position 2026-08-31 04:20 (T+... 6.4 days left)
- **677 structures measured at both pressures** (was 306). ctrl2 essentially complete (287 of
  300 uniform draws), so the model-free ceiling sample is now n~490 uniform.
- **NEW RECORD: 2016[Cu][pts]3[ASR]1 = 200.43 +/- 1.11 cm3/cm3, floor grade.** Claim-grade run
  queued 04:16. Below G1 (>230) and below the G2 band (210-230), so no gate action beyond routine.
- Runners-up (floor): 196.11 2013[Yb][nia]3[ASR]1, 196.03 2020[In][nuc]3[ASR]1,
  193.36 2013[Ni][nia]3[ASR]1, 191.16 2015[Zn][ith]3[FSR]1, 190.68 2007[Zn][pcu]3[ASR]3.
- **Claim grade so far (6 geometries):** 2015[V][srs]3[FSR]1 197.56 +/- 0.84 (floor twin 197.26
  — floor and claim agree to 0.30, which is the floor-vs-claim accuracy check passing on the
  leader itself), 2021[Cu][lvt]3[ASR]1 185.98, 2014[Cu][nts]3[ASR]2 185.46, 2018[Zn][ith]3[FSR]2
  182.30, 2014[Fe][nan]3[ASR]6 182.22, 2013[In][acs]3[ASR]1 182.07.
- **G6 repeats landed for 3** and all agree: nts 185.46/185.44, ith 182.30/182.44,
  nan 182.22/182.25. The leader still needs its claim run AND its G6 repeat.
- Refitted model (n=677) now predicts up to 194.6 for UNRUN structures — it no longer saturates
  at 160 as the first fit did. Screening is still productive: keep it running.

### Budget 2026-08-31 04:20
- **SPEND $177.62 / $280 = 63.4%** <- THE BINDING BUDGET. Warning fires at $210.
  It moved $172.98 -> $177.62 during a single 25-minute check-in. At that rate the remaining
  $102 is ~5 h of active session against 6.4 days of calendar.
  **=> CHECK-INS MUST BE RARE AND TINY: one `bash bin/s.sh` call, act only on a problem.**
  Everything routine is the autopilot's job, including REPORT.md.
- Compute 847 / 1610 = 52.6%. Tokens 4.77 M / 32 M = 14.9% (understates cost; ignore it).
- Unrun after the trim: 450 screening structures (~417 CPU-h) + 33 in flight + claim 10 x 7.75
  + repro ~7 x 7.75 + G7 ~25. **Projection ~1,430 / 1,610 (89%).**
- **Trim executed 04:16:** the 70 lowest-model-ranked unclaimed screening structures
  (pred_wc <= 138.2) were removed, 140 rows, ~65 CPU-h. Reversible by re-appending.
- Worker replacement is AUTONOMOUS (`ensure_workers`, tops up to 12 when the 08-29 generation
  expires 09-01/02). No action needed from me.

### What I must still make sure of before the deadline
1. Leader 2016[Cu][pts]3[ASR]1 claim-grade AND G6-reproduced under a distinct seed
   (`bin/seedcheck.py`). Until then the Claim rests on 2015[V][srs]3[FSR]1 197.56.
2. Ceiling: rerun `bin/evt.py` and `bin/ceiling.py` once ctrl2's last 12 rows land.
3. REPORT.md is regenerated by the autopilot every cycle — verify it is current, do not rewrite
   it by hand.

_(updated 2026-08-30 12:00 KST, after the fleet pause)_

## Fixed facts
- **Deadline 2026-09-06T00:09:22 KST** (launch + 168 h + the 4.4704 h fleet pause; the pre-pause
  value 2026-09-05T19:41 is superseded — WORKSPACE.json `deadline_kst` is authoritative).
- Budgets 1,610 CPU-h / 32 M tokens / US$280. Spend is the budget most likely to bind and it
  counts cache reads; the token figure understates cost.
- **Compute meter.** `usage.json:cpu_h_scheduler` is the harness-ratified basis (ruling
  2026-08-30) BUT it sums cput over jobs CURRENTLY in the scheduler only — verified: it equals
  the sum of .cput_snapshot.json, which holds exactly the running jobs, and the killed 08-29
  descriptor jobs appear in neither. **It would fall toward zero as the 09-01 walltimes expire**,
  relaxing the guard when most budget had been spent.
- `bin/autopilot.py cpu_ledger()` records the high-water cput PER JOB ID in tables/cpu_ledger.json
  and never forgets. cpu_h_used() = max(internal wall_s sum, usage.json, ledger). Ledger is built
  from the same scheduler cput values, so it does not override the ratified basis — it sums it
  over the campaign instead of over the instant.
- Live 404.0 CPU-h vs usage.json 390.1 at 13:28; the gap is the snapshot's ~26 min refresh lag.
- Queue `long`, prefix `rep07_`, max 12 jobs in system. Submit `/usr/local/mjs/qas <script>`,
  remove `/usr/local/mjs/qrm <mjs_id>`, list `/usr/local/mjs/qinfo` (queued) and
  `qstat -u Bei` (running — the two use different id spaces).
- Cluster is shared; every replicate is user Bei (aa 38 / amd 80 / ac 102 / ax 32 cores TOTAL
  across all sixteen). ax is one node (bnode11, 64 cores) and is normally full: do not queue
  large ax jobs, they never dispatch and they head-of-line-block the class for everyone.
- RASPA toolchain/raspa/bin/simulate with RASPA_DIR=<ws>/raspa_home. Verified 2.0.37,
  unshifted, tailcorrection no, 91 pinned pseudo atoms bound, no type invented.
- NEVER feed a raw db CIF to RASPA — bin/prep.py rewrites labels to pinned UFF names.
- Energy grids unusable: the provided binary contains no MakeGrid code path at all (harness
  confirmed 2026-08-30). All GCMC is analytic. This is settled, do not retry.
- G3: 12,369 / 12,499 pass. Kills: 4 density, 126 overlap (d_min < 0.74 A).

## Architecture (all work queues are atomic-claim, so any subset of jobs finishes the work)
- Descriptors: bin/run_desc.py / bin/worker.py -> tables/desc/*.csv  [COMPLETE, 12,499]
- GCMC: append rows to tables/gcmc_tasks.csv (name,pressure_pa,init,prod,tag,timeout_s);
  workers bin/worker.py claim via tables/gclaims/ keyed by sha1(tag,name,P,init,prod), write
  tables/gcmc/res_*.csv, run dirs runs/<tag>/<name>__<P>/ with struct.cif + simulation.input
  + output.data.gz. Pruning unclaimed rows from gcmc_tasks.csv is SAFE and is the budget lever.
- Merge/rank bin/merge_rank.py; audit lines bin/audit.py; status `bash bin/s.sh`.
- SSH quoting: always `ssh dirac-bei 'bash -s' << 'OUTER'` for anything with quotes.

## Database is 9,143 distinct geometries, not 12,499  (found 2026-08-30 12:00)
- ASR / FSR are charge-assignment variants of ONE framework; §3 is chargeless, so the prepared
  struct.cif is bit-identical and they are one simulation. 3,356 of 12,499 entries (26.9%) are
  duplicates. Canonical hash: bin/geohash.py -> tables/geohash.csv.
- **Run `python3 bin/dedup_queue.py` at EVERY check-in.** The autopilot copies running inside
  compute jobs hold pre-patch code and will queue twins; the sweep is idempotent and cheap.
- Never present an ASR/FSR pair as two materials or as mutual corroboration. One material.
- Ceiling-argument denominator is 9,143 distinct geometries. The §1 mandate set is still 12,499.

## RASPA RNG (found 2026-08-30 12:00)
- RASPA seeds from time() in WHOLE SECONDS and prints `Random number seed:` in the output.
  Runs dispatched in the same second share a seed and are byte-identical, NOT independent.
- Verified: same input twice in one second -> 132.2796048033 both times; the archived run of the
  same input at another second -> 131.8475437313, i.e. 0.43 apart against a quoted error of 2.55.
  That pair is the campaign's evidence that the MC error bars are honest.
- G6: independence is checked POST HOC with `bin/seedcheck.py claim repro` — reads the seed back
  out of both archived outputs, flags collisions, reports deviation in units of combined sigma.
  Do NOT edit mkinput.py to set RandomSeed: live workers hold the old module and the repro wave
  will be run by them.

## RANKING: exhaust the band, do not follow the order (found 2026-08-30 12:20)
- Spearman(pred, measured): ALL 297 geometries 0.966 GBT / 0.866 proxy. But for the 71 with
  WC>=150: **GBT 0.170, proxy -0.266**. The model separates bad from good and CANNOT rank
  within the good band. (Range restriction attenuates this; direction is not in doubt.)
- 319 geometries within 5 of the max prediction, 676 within 20 -> the model expresses no
  preference among them. Do not spend budget on rank order inside the band.
- STRATEGY: define the band the model cannot resolve and measure ALL of it. The ceiling claim
  then does not depend on the ranker being right. Queue already covers the top-20 band with
  **0 uncovered**; 195 of the top-30 band are left for the screen3 refit.
- The GBT CANNOT extrapolate (leaf = mean of training targets, max 160.2), so its VALUES are
  unusable as a ceiling envelope: top-decile residual bias +24.0 vs +1.5 overall, and the
  best-predicted unmeasured geometry is 155.5 against a measured record of 197.3.
  Build the envelope from the physics proxy at the refit, NOT from the GBT.
- Ceiling evidence tools: `bin/ceiling.py`, `bin/evt.py`, and `bin/knn_ceiling.py`
  (MODEL-INDEPENDENT nearest-measured-neighbour argument: 199 of 8,705 unmeasured geometries have
  a neighbourhood reaching 90% of the record, 198 already queued, 1 gap queued as tag `risk`).
- Model-free bound so far: control-197 has nothing above 170 -> 95% Wilson bounds structures
  above 170 at <=175 of 9,143. This is the one line no regressor can bias.

## Science position at 2026-08-30 12:00 (T+16.3 h)
- 306 structures measured at both pressures (ctrl200 + first model-ranked screen).
- **Best measured: 2015[V][srs]3[ASR]1 / [FSR]1 = 197.3 +/- 1.2 cm3/cm3, floor grade.**
  Runners-up 185.4 (2014[Cu][nts]3[ASR]2), 185.3 (2021[Cu][lvt]3[ASR]1), 182.7, 182.2, 181.9.
- Best of the unbiased control-200: 160.2. The model buys ~37 cm3/cm3 over random draw.
- Nothing has entered the G2 band (210-230) yet; no G1 event.
- Ranking quality: analytic proxy Spearman 0.809; GBT 5-fold CV Spearman 0.919 (119 train).
- Descriptor engine validated vs RASPA Widom insertion to 0.3-0.7% (LOG 2026-08-29 22:05).

## G7 outcomes are logged, not just queued (2026-08-30 12:50)
- `bin/g7log.py` (in the autopilot loop, 0.23 s) writes the OUTCOME of each random audit, not
  merely that one ran. Without outcomes the pass rate is 0/0 and the gate's whole purpose — it
  is the only gate that yields a DENOMINATOR — is lost.
- Tolerance (mine, stated in every line): |dev| <= max(4*combined sigma, 2.0 cm3/cm3). The
  4-sigma leg is generous because repro_stats measured the error bars ~4x CONSERVATIVE, which
  would otherwise make genuine agreement look like failure; the 2.0 floor covers near-zero-uptake
  structures where combined sigma collapses.
- SEED COLLISION => `audit_void`, NOT a pass. A repeat dispatched in the same second as its
  original is byte-identical and tested nothing; counting it would inflate the pass rate.
  Voided audits are re-queued under tag `g7r` (a new tag is required: the worker claim key
  hashes the tag). Collisions ran 4 of 35 cells earlier, so this is a real rate.

## EQUILIBRATION: ANSWERED, free, n~700 (2026-08-30 13:00)
- `python3 bin/blockdrift.py` — RASPA prints 5 production block averages per run, so every
  archived output carries its own equilibration test. Cached in tables/blockdrift.csv; in the
  autopilot loop (~0.16 s warm, 21.9 s one-off backfill of 706 runs).
- Fractional drift (blocks 4,5 minus blocks 1,2, over the mean):
    65 bar  n=346  mean **-0.00007**  t=-0.04  155/346 positive
    5.8 bar n=358  mean **-0.00103**  t=-0.73  178/358 positive
- **No upward drift at either pressure.** Under-equilibration shows up specifically as RISING
  blocks, so this is a directional test, not merely a null. Floor grade IS converged.
- Do NOT quote the 65 bar sign-test z of -1.94 without the mean beside it: the mean drift it
  accompanies is 7 parts per 100,000 against a per-run spread of 0.036. Significant sign,
  meaningless magnitude.
- Does NOT settle: a run trapped in a metastable state from the start (nor does floor-vs-claim),
  or whether the force field is right — only that sampling converged under it.

## Floor-vs-claim convergence — the paired check (2026-08-30 12:45)
- Claim-grade runs are RUNNING (4 structures x 2 pressures in runs/claim/ as of 12:44). The
  priority reorder worked; they were previously last in a 1,900-row queue.
- `python3 bin/floorclaim.py` compares floor (2,000+10,000) to claim (10,000+50,000) per
  geometry: per-structure z, paired mean with se, and a SIGN TEST (the sign test is the one
  that does not assume the error bars are right, and repro_stats found them ~4x conservative).
- WHY IT MATTERS BEYOND THE HEADLINE: the ranking, the band-exhaustion strategy and the control
  tail are ALL built on floor-grade values. A systematic offset would shift every one of them.
  A per-structure difference within noise is fine; a consistent SIGN is not, however small.
- REPORT.md now states plainly that this is untested until data lands. Wired in (0.19 s).

## Uncertainty: MEASURED, not estimated (2026-08-30 12:25)
- 31 independent repeat pairs (ASR/FSR twins run under different clock seeds, 4 same-seed pairs
  excluded): deviation mean 0.314, max 1.208 cm3/cm3; z=(a-b)/hypot(ea,eb) has sd **0.246**.
- => RASPA's quoted error bars are **conservative by ~4x**; true run-to-run reproducibility of a
  floor-grade number is ~0.3 cm3/cm3. Tool: `python3 bin/repro_stats.py`, wired into REPORT.md.
- **Do NOT rescale the reported +/-.** Keep RASPA's value: it is conservative and it is what the
  archived outputs contain.
- This is PRECISION only. Repeats at one cycle count share that cycle count's equilibration bias.
  The floor-vs-claim comparison is the accuracy test; claim rows are first in the queue for it.

## Protocol verified from the archive (2026-08-30 12:30)
- Parsed quantity IS `Average loading absolute [cm^3 (STP)/cm^3 framework]` = section 2's ask.
- Cross-check: 530.7219 cm3STP/g x 0.43731 g/cm3 = 232.08 cm3STP/cm3 exactly, so RASPA and my
  cifio/prep agree on cell contents and volume. A silent cell/supercell error is excluded.
- RASPA reports excess == absolute here (void fraction unset), exactly as section 2 anticipates.
- tailcorrection no on all 4,186 pairs, unshifted, 2.0.37.

## Binding constraint is CPU-h, NOT time (checked 2026-08-30 12:35)
- Pending work ~748 CPU-h + later waves ~300 = ~29 h wall at the fleet's ~36 effective cores.
- Deadline is 2026-09-06T00:09, i.e. ~5.5 days. Time slack is large; CPU-h is what binds.
- Projection: ~1,450 of 1,610 CPU-h. Spend accordingly: prefer measurements that buy a
  deliverable over measurements that add precision to one already answered.

## Budget position (2026-08-30 12:58) — PRICING IS NOW EMPIRICAL
- Used **374** CPU-h (scheduler meter). Committed but unrun **882**. Total **1,257 / 1,610**.
- Measured unit costs (bin/autopilot.py unit_costs(), n>=5 required): floor grade 0.249 CPU-h
  at 5.8 bar, 0.676 at 65 bar => **0.926 CPU-h per structure at both pressures**.
- **Claim grade cost 8.37x its floor twin, not the 5.00x the cycle ratio implies** (54 s vs
  453 s, one pair; most likely node heterogeneity, arithmetic rules out fixed overhead).
  => ~7.75 CPU-h per claim-grade structure. REFINE THIS as more claim runs land.
- Projection: 1,257 + claim 16x7.75=124 + G6 repro 6x7.75=46 + G7 ~25 => **~1,452 / 1,610**,
  margin 158 CPU-h (9.8%).
- N_CLAIM 24->16 and N_REPRO 10->6: section 7 makes the Claim three sentences, so what must be
  claim-grade and G6-reproduced is the leader plus enough rivals to be sure it IS the leader,
  not a claim-grade survey. Top-16 spans 197.3 to ~180 against 0.3 reproducibility, so the true
  best is essentially certainly inside it.
- `screen_ok=False` — screening is at its cap; screen3's WAVE will not queue. Its model REFIT
  still runs (split out 12:55) because model_pred_final.csv feeds the ceiling argument.
  Not queueing screen3 is right, not merely forced: it would re-rank inside the band the model
  cannot resolve, and the band already has 0 uncovered.
- **enforce_budget()**: at 94% of 1,610 it cuts unrun DISCRETIONARY rows and keeps claim/repro/
  G7; at 99% it cuts everything unrun. This is the hard stop — the screening guard only ever
  controlled queueing, never execution.
- Tokens **4.58 M of 32 M (14.3%)**. Compute **405 of 1,610 (25.2%)**.
- **MY OWN SESSION COST IS NOW MATERIAL.** Tokens went 3.26 M -> 4.58 M across ~5 turns, i.e.
  ~300 k/turn, because the conversation context is re-read every turn — exactly the mechanic
  section 4 warns about. The campaign is instrumented and now mostly WAITING ON DATA, so the
  marginal value of another check-in is low while its marginal cost is not.
  => Keep check-ins LEAN: one compact status call, act only if something is wrong or a result
  has landed. Do not re-derive what STATE.md already records. Do not re-read large outputs.
- ~~THERE IS NO SPEND METER~~ (OBSOLETE 2026-08-30: usage.json publishes spend; see check-in above).** Charter section 4 says one is in the workspace; usage.json has
  only cpu_h_scheduler / queued_jobs / tokens. Escalated 13:05, no reply expected.
  Proxy in use: token fraction ~= spend fraction, valid only if my cache-read share matches the
  59%-of-cost calibration the charter cites. NOT a bound in either direction — if my cache-read
  share is higher, spend is further along than tokens show. Manage conservatively regardless.
- Guard (bin/autopilot.py): CPU_CAP=1450 on used+pending, RESERVE=160. It gates SCREENING ONLY.
  Claim grade, G6 and G7 are charter obligations and must never be blocked by it.

## In flight
- 10 workers running (u0..u9, 42 cores, ~28 effective), 72 h walltime, started 08-29 23:23-08-30 01:52
  => **they expire 2026-09-01 23:23 through 2026-09-02 01:52. A replacement generation is needed
  if any work remains after that.** Deadline is 09-06, so this is a live scheduling item.
- 2 workers queued: rep07_v0 (amd ppn6), rep07_v1 (ac ppn3), 24 h idle-exit, 72 h walltime.
- Task queue: 1,976 rows after dedup; 624 CPU-h of it unrun.

## Plan
1. [DONE] Descriptors for all 12,499 -> master.csv.
2. [DONE] Control-200 floor-grade GCMC -> unbiased landscape + model training set.
3. [RUNNING] screen1 (500) + screen2 (400) floor grade, model-ranked.
4. At 600 measured: screen3 refits the model and adds the top 200 unmeasured.
5. Claim-grade wave (10,000+50,000) on the top 24 BY GEOMETRY. Trigger is `measured>=750`
   **OR** `no screening rows left unrun and measured>=250` — the second leg exists because a
   count-only trigger can never fire if screening stops early, which would reach the deadline
   with nothing admissible in the Claim. Selection dry-run verified 2026-08-30 12:51: 24
   distinct geometries, zero overlap with the 6 already queued by name or geometry, 98 CPU-h.
   Still verify it fired rather than assuming.
6. G6 reproduction is CONTINUOUS, not a wave (fixed 13:20). Each cycle the autopilot ensures the
   current top N_REPRO=6 claim-grade GEOMETRIES each have a repro queued, capped at REPRO_CAP=10.
   As a one-shot it would have reproduced the 6 early claim structures, recorded itself done, and
   never reproduced the actual finalists — leaving the headline number inadmissible under G6 with
   the gate marked complete. G7 every 40th passer at frozen order, outcomes logged by g7log.py.
   REPORT.md stays PROVISIONAL until the leader is claim-grade AND has an independent repeat at
   both pressures under DISTINCT seeds (same-second repeats are byte-identical and prove nothing).
6b. CEILING PLAN — the half of the mandate not yet answerable. STATUS: ctrl2 QUEUED 12:35.
   - Rare-event bound (bin/ceiling.py): 188 of 8,259 out-of-band sampled, best draw 151.8 vs
     record 197.3, 0 exceedances, 95% bound <=165. Too loose to claim on.
   - EVT peaks-over-threshold (bin/evt.py) on control-197: shape xi NEGATIVE at every threshold
     (so a finite ceiling does exist), but the endpoint estimate swings **162.5 to 243.0** and
     P(max>record) swings 0 to 1 with the threshold. NOT a result. Sample-size failure.
   - => ctrl2 queued: 300 uniform draws (295 fresh, ~242 CPU-h), fixed seed 20260830 over one
     representative per distinct geometry, ctrl200 geometries excluded. Combined uniform n~497.
     Procedure is reproducible from `bin/ctrl2.py`. RERUN bin/evt.py when ctrl2 lands; if the
     endpoint is still threshold-unstable, a ctrl3 of similar size is the next step and there
     is ample TIME for it (see below) though CPU-h is the binding constraint.
   - Structures in the draw already measured keep their values; reusing them is unbiased because
     a measurement does not depend on why the structure was selected.
7. Ceiling argument: measured landscape + model envelope over the 12,499 + coverage of the
   unsimulated region; G5 modifications only if headroom is indicated.
8. REPORT.md at workspace root.

## Known traps (do not re-learn these)
- Status: `bash bin/s.sh` -> `ap=<autopilot count, must be 1> run= queued= desc= gcmc= cpu= tok=`.
- Health-check the autopilot with `pgrep -c -f "autopilot[.]py"`. Plain `pgrep -f autopilot.py`
  also matches the shell running the check and reads 2 when one is alive; a `ps -eo comm=,args=`
  filter was tried and this cluster's ps does not support that form (returns 0, i.e. would report
  the autopilot dead while it runs).
- VERIFY string-replacement patches actually matched. Two edits this session silently did nothing
  because the anchor text differed, and one earlier edit matched MID-LINE and inserted code at the
  wrong indentation, leaving mkreport.py unparseable. Assert on the match, then check the artefact.
- This cluster ships an OLD git: `git -C` is NOT supported. Use cwd= instead.
- `ps` on the login node (bnode0) works fine and shows bnode0's OWN processes — corrected
  2026-08-30, the old note said they were invisible and that stops you looking. What is true:
  MY workers run on other nodes, so ps cannot check MY fleet. Use `qstat -u Bei` for liveness
  and the mtimes of tables/gcmc/res_<wid>.csv for per-worker progress.
- bnode0 is shared and routinely SATURATED by other replicates running RASPA outside the
  scheduler (load 92/96, 76 simulate processes, none mine, on 2026-08-30 12:27). Keep login-node
  work at nice -19. Wall-clock measured on bnode0 is inflated; results are not affected.
- **A running Python process holds every module it has imported.** This bit me twice: the ten
  worker-hosted autopilots (solved by parking them) and then the login autopilot itself, which
  kept generating REPORT.md from a cached mkreport while the repo showed the fix. The login
  autopilot now RE-EXECS itself whenever any bin/*.py mtime changes, so edits land at the next
  cycle boundary. Worker-hosted copies still cannot be patched — they are parked.
- **Verify a patch actually took effect** rather than assuming: check logs/autopilot_local.log
  advanced AND the artefact changed (e.g. REPORT.md mtime and content).
- Background ssh from the agent side does not survive between turns; the in-job autopilot is
  what actually keeps the campaign moving.
- IDLE POLLING <= 1/hour. Context is re-read every turn, so cost scales with context x turns.
