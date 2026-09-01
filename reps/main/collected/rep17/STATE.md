# STATE - CAMPAIGN REOPENED 2026-08-31 05:10 KST: the filed claim was contradicted

**Read this first. The report was filed early at 04:20 and is no longer the final word.**

At 05:09 the last outstanding job, e3 (job 3473668), returned the claim-grade value for the
four-methyl variant of the leader:

    2021[Cu][sql]2[ASR]6         parent, 3 seeds   207.07 +/- 0.37
    2021[Cu][sql]2[ASR]6@me004   1 seed            208.15 +/- 0.37   <-- ABOVE by 1.09 +/- 0.53
    2021[Cu][sql]2[ASR]6@me012   3 seeds           206.58 +/- 0.23

me004 is 2.1 sigma above the parent on propagated block errors (2.7 sigma using the parent's
seed sem 0.153). The report I filed claimed the best number "cannot be exceeded by modifying
its best member". That is withdrawn in REPORT.md sections 1, 3, 4 and 6, with the withdrawn
sentences stated in place rather than deleted. **REPORT.md is current and honest as of now:
if this session stops at any moment it reads as a parent claim with an open modification
branch, not as a false ceiling.**

Why the floor series missed it: floor-cycle error bars are +/-0.9 to +/-1.2, three times the
effect. The k=4 and k=8 points (207.82, 207.40) were never separable from the parent's 207.60.
Claim grade (+/-0.37) is the first resolution that can see a ~1 cm3/cm3 bump. Refit on the
three claim-grade points k = 0, 4, 12: vertex k = 5.5, predicted max 208.2.

## WAVE G - the only thing that matters now (submitted 05:14, jobs 3473772-78)
Each is one structure, 1 core, 10,000+50,000 cycles, both pressures, ~12 h wall / ~12 CPU-h.

    g0 3473772  me004 seed 202   <-- these two decide the claim
    g1 3473773  me004 seed 303   <--
    g2 3473774  me008 seed 101   the other floor-cycle tie, 3 seeds
    g3 3473775  me008 seed 202
    g4 3473776  me008 seed 303
    g5 3473777  me006 seed 101   newly built, brackets the fitted vertex k=5.5
    g6 3473778  me002 seed 101   newly built

Collect with: python3 scripts/collect.py g0   (etc; one task per tag)
Expected landing ~17:15 KST 2026-08-31. Deadline 2026-09-06T01:22 - ample.

**DECISION RULE, fixed in advance so the result is not read after the fact.**
- If mean(me004, 3 seeds) - 207.07 > 0.4 and the 3 seeds are mutually consistent:
  the claim material becomes 2021[Cu][sql]2[ASR]6@me004 and REPORT.md section 1 is rewritten.
- If within +/-0.4: single-seed fluctuation; parent stands; say so plainly and restore the
  modification-ceiling sentence as earned rather than assumed.
- If me008 or me006 beats me004, that structure needs its own 3 seeds before it can be
  claimed; there is time for one more round (~12 h) but not two.
- me002/me006/me008 single seeds are curve shape, NOT claim material on their own.

## What I actually hold: a 2.41 sigma DISAGREEMENT, not a confirmed improvement
Re-analysing the floor series properly (fit n58 and n65 separately - RMS 0.271 and 0.359 -
instead of fitting their difference, whose error bars are 0.89-1.22) makes it PRECISE, and it
then disagrees with the new seed:

    dWC/dk at k=0, floor, variance-reduced : -0.0655 +/- 0.0468   (1.40 sigma BELOW zero)
    dWC/dk over k=0->4, claim grade        : +0.2715 +/- 0.1316   (2.06 sigma ABOVE zero)
    tension                                 +0.3370 +/- 0.1397 = 2.41 sigma
                                            = 1.35 +/- 0.56 cm3/cm3 over 4 sites

The separate-fit floor model predicts WC(4) = 207.66 and a monotone decline from k=0; the
claim-grade seed says 208.15. The gap is almost all in n65 (floor 244.34/247.09 at k=0/4 vs
claim grade 243.92/247.57 - both shifts push the same way, each inside a single-run loading
error). **So do not tell anyone methylation helps.** Two more me004 seeds cut the claim-grade
slope error by sqrt(3) and separate the hypotheses at better than 3 sigma either way.

Mechanism is common ground: dWC/site = +0.271 over k=0->4 and -0.196 over k=4->12, because
n65 saturates (0.912 -> 0.498 per site) while n58 stays linear (0.641 -> 0.694). A turnover
exists; the dispute is only whether it sits just above or just below k=0.

## Budget position at reopening (2026-08-31 05:14)
- Spend **156.96 of 280.00 (56.1%)** - the binding budget. usage.json now HAS spend_usd
  (the earlier STATE note saying no spend meter exists is superseded; the meter arrived
  2026-08-30T19:10Z and is a true running total carrying pre-migration spend forward).
- Compute 912.1 of 1610 (56.7%). Wave g adds ~84 CPU-h -> ~62%. Not binding.
- Tokens 7.25M of 32M.
- Cost is per invocation, not per unit of waiting: use ONE long blocking cluster wait per
  turn, never repeated short polls. At ~-6 a turn there is room for roughly 20 more turns.

## Still running from before the reopening
w70 (3473677), w71 (3473681), w83 (3473732) - screening tail, already fully collected at
448/450 and 499/500; they change nothing. blindbound.py: 0 exceedances in 998 uniform random
draws -> at most 26 of 8352. That part of the report is settled and needs no further work.

---
(historical working notes below)

# STATE - current beliefs and open tasks
_(working memory; must be sufficient to resume alone)_

## Fixed facts
- **Deadline T = 2026-09-06T01:11:02+09:00.** Launch 2026-08-29T20:42:48 + 168 h, plus
  the 4.4704 h fleet pause of 2026-08-30 (INBOX notice 02:42:33Z). The earlier value
  2026-09-05T20:42:48 in this file was pre-pause and is superseded. Read cluster time
  with date(1); never estimate timestamps from session pacing.
- Budgets: 1610 CPU-h, 32M tokens, USD 280. Max 12 queued jobs. Queue long. Prefix rep17_.
  **There is no spend meter in the workspace** (usage.json has cpu_h_scheduler,
  queued_jobs, tokens only). Escalated; proxying spend from tokens x ~2.4 for cache reads.
- Objective WC = N_abs(65 bar) - N_abs(5.8 bar), 298 K, cm3 STP/cm3. Absolute, not excess.
- Toolchain verified by content: UFF 3 files match the charter SHA-256 table; RASPA 2.0.37.
- **Framework atom typing, verified from RASPA's own output.** RASPA does NOT match the
  pinned type names (C_, H_, N_, F_) to the CIFs; it creates pseudo-atoms from the bare
  CIF labels (97 vs the 91 declared) and resolves them BY ELEMENT to the pinned values:
  C 88.43257 K/3.58 A, H 57.24264/3.15, N 71.68375/3.495, F 61.02560/3.363, Cu 19.293/3.4215.
  So modified structures containing F get the pinned UFF fluorine. The same output reports
  Forcefield UFF, CutOff 12.8, "All potentials are unshifted", tailcorrection no - the three
  section 3 settings confirmed from the simulator rather than from my input file.
  RASPA_DIR = ws/raspa_home. Binary ws/toolchain/raspa/bin/simulate.
- Submission: `qas` DOES exist, at /usr/local/mjs/qas, absent from the non-interactive
  PATH. Everything so far went through PBS qsub (same scheduler); either is fine.
- RASPA MakeGrid is non-functional fleet-wide. Irrelevant here: no number of mine is
  grid-based, so section 3's grid-disclosure clause never applies.
- The ~252-core scheduler cap is shared by all 16 replicates submitting as user Bei.
  There is no private allocation; plan throughput against a contended pool.

## Established results
- All 12,499 CIFs parse; every element has a UFF type. analysis/manifest.csv.
- The database is **9,124 DISTINCT structures**; 3,375 names are charge-only duplicates
  (ASR/FSR pairs identical but for the DDEC6 column, which the chargeless protocol
  ignores). analysis/fingerprints.csv, analysis/canon.csv. Screening runs on canonical
  representatives only.
- Tier A descriptor screen (in-house numpy grids, NOT RASPA): all 12,499, analysis/screen.csv.
- Tier B (w2, 500+2500 cycles): 526 structures. Tier B2 (w3, same): 246 more.
  **772 distinct structures measured by GCMC.** Sub-floor cycles validated against floor
  cycles on 10 structure-pressure points: mean diff -0.13, RMS 0.44 cm3/cm3, 4x cheaper.
  These are a ranking instrument only; no sub-floor number is reported as a capacity.
- Tier C (w4, floor 2,000+10,000): 58 of 64 done.
  **Leader 2021[Cu][sql]2[ASR]6, WC = 207.60 +/- 0.93** (n58 36.74, n65 244.34).
  Runner-up 2016[Cu][pts]3[ASR]1 at 200.07 +/- 0.99. Then 197.43, 196.50, 195.84.
  Independently corroborated: Bei's archived run on the same structure gives 206.53.
- **Ceiling evidence, current form (supersedes the earlier version of this block).**
  * 907+ distinct structures measured by GCMC; 79+ at the section 3 floor or above.
  * Gate A (ridge regression refit on 772) admitted everything predicted above
    207.60-58.76=148.30. One structure, 2021[ZnIn][nan]3[ASR]1: measured **136.53**.
  * Gate B (thermodynamic, no regression): optimal single-site Langmuir fixes the swing
    efficiency at eta=0.5178 from the 5.8/65 bar fugacity ratio; pore volume x liquid
    methane packing bounds n_sat; the best efficiency any real material reaches (0.810)
    scales it. 15 structures, 8 unscreened, all measured (w6), **max 144.05**. The most
    dangerous, 2015[Zr][spn]3[ASR]1 (vf 0.932, allowance 230.5), gave **97.24**.
  * The gates were nearly DISJOINT, so each was checked where the other said it was most
    likely to fail. Closest approach of anything either flagged: **63.55 below 207.60**.
  * **What actually carries the claim is block P's depth, not gate A's threshold.** Block P
    covers every unscreened structure with pred2 >= 138.48, tolerating an underprediction
    of 69.12. Measured worst underprediction on the unbiased block R sample (n=145):
    +54.39 overall, +23.26 in the pred>80 band that a ceiling claim is actually exposed to.
    Gate A's own margin is only 1.08x the unbiased worst - do NOT lean on it alone.
  * Block R (uniform random unscreened, n=145 of 200): max measured **135.33**, 72.27 below
    the leader; 0 exceedances -> 95% Clopper-Pearson bound of 2.04%, at most 171 of 8352.
  * Model error by band (block R, fixed cuts, pred<0 excluded as out-of-domain):
    pred 0-40 RMS 13.49 / 40-80 RMS 15.27 / 80-200 RMS 8.50. Worst in the MIDDLE, best at
    the top. An earlier STATE/LOG claim that errors are worst at the bottom was wrong; see
    LOG 16:35 correction.
- Proxy bias, measured: the raw wc_lda proxy overestimates 5.8 bar loading by ~41%, so it
  penalises strongly-binding frameworks. Raw Spearman vs GCMC only 0.788; the refit is
  what makes the gate usable.
- **Thermodynamic ceiling (scripts/ceiling.py), model-independent.** Single-site Langmuir
  optimised over affinity gives WC <= n_sat*eta with eta = (sqrt(r)-1)/(sqrt(r)+1),
  r = f65/f58 = 9.910 from Peng-Robinson at 298 K, so **eta = 0.5178**; site heterogeneity
  only lowers it. With n_sat <= vf_he * 590.1 (liquid-methane packing), reaching 207.6
  requires vf_he > 0.680. Above that void fraction the bound holds over all 676 measured
  structures and the best efficiency any real material reaches is **0.810**; the leader
  is at 0.770. Applying 0.810 to all 8,352 unscreened leaves **15** able to reach 207.6,
  max attainable 230.5. The bound fails (efficiency 1.263) only at vf ~ 0.11, where a
  Widom-averaged helium void fraction is not a geometric volume - a regime that cannot
  reach 207.6 regardless.
- The two gates are nearly disjoint: the model gate keeps 1 structure, the thermodynamic
  gate keeps 15 (eight Zr-csq/spn frameworks the model scores only 109-137). Union 16;
  8 already in w5 block P, 8 submitted as w6. analysis/w6_selection.csv.
- The leader is an outlier inside its own family: the other 11 structures sharing its
  year/metal/topology/catenation have density 0.83-1.74 and vf 0.27-0.73. There is no
  gradient to climb by screening its neighbours.
- Cost model, calibrated: seconds = 1.46e-6 x nsim x cycles x max(20, N_molecules),
  scatter 7e-7 to 2.6e-6. scripts/cost.py. Loading, not framework size, drives cost.
  High-capacity candidates ~3.4 CPU-h at floor cycles, ~17 CPU-h at claim grade.

## Running (submitted 2026-08-30 12:00)
- d0 (3473624-25): Tier D claim grade 10k+50k, top 10 of Tier C, seed 101. ~17 h/struct.
- d1 (3473626) seed 202, d2 (3473627) seed 303: top 5 repeated. Separate tags because run
  dirs are keyed on structure+pressure and would otherwise collide.
- w5 (3473628-30): Tier B3 widening, 350 at 500+2500. block P = 150 highest-pred2
  unscreened (takes the measured band down to prediction 138.5); block R = 200 uniformly
  random unscreened (the only model-blind false-negative test in the campaign).
  Block membership in analysis/w5_selection.csv.
- w3 (3473539) and w4 (3473542-45) still draining their last few tasks.
- m1 (3473635, submitted by the watcher 12:14): FIVE tasks at floor cycles - methyl
  variants me012/me025/me100 (me100 = 32 sites, the saturation limit) and fluorine
  variants f025/f050 (f050 = 44 sites, saturated). Methyl and F saturate at different
  counts so the series are not nested; an equal-site comparison exists at 24.
- w6 (3473646, submitted by the watcher 13:06): the 8 thermodynamic-gate survivors not
  already in w5, at floor cycles. The watcher has now finished; nothing is held.
- Modified structures live in mods/ and prep.py falls back to that directory; their names
  carry '@'. scripts/methylate.py rebuilds them deterministically from the parent CIF.
- Collect any wave with: python3 scripts/collect.py <tag>

## Modification branch: CLOSED for real this time (m1+m2 complete, floor cycles)
Seven methyl counts on the leader 2021[Cu][sql]2[ASR]6 (parent WC 207.60 +/- 0.93):

    k methyls:   0      4      8     12     16     24     32
    WC:      207.60 207.82 207.40 206.27 205.61 203.50 199.73
    +/-        0.93   1.22   1.14   0.89   1.14   0.95   0.51

Inverse-variance-weighted quadratic: WC(k) = 207.672 + 0.0014 k - 0.00777 k^2, all seven
residuals inside their own error bars, **vertex at k = 0.09, i.e. 0.000 above WC(0)**.
The methylation optimum IS the unmodified parent. k=4 and k=8 are ties (+0.22, -0.20).
Fluorine: linear, -0.385 and -0.396 per site at k=24 and 44. No interior maximum either.
=> The leader is at a stationary point of the only modification axis section 3 allows
(decorating the pore wall; rewiring topology makes it a new structure, out of scope per
section 1).
NOT doing: more seeds on me004. No sampling resolves a 0.22 gap between numbers whose own
block errors are 4-5x larger.
History: LOG 13:12, 14:48 and 16:45 each closed or characterised this branch prematurely;
corrected at 15:20, 17:15 and 17:31. Cite only the 17:31 entry.

## w6 result: the loose gate's candidates all miss badly (floor cycles, reportable)
Six of eight in. Max 144.05 (2017[Zr][csq]3[FSR]2). The most dangerous structure in the
campaign, 2015[Zr][spn]3[ASR]1 - largest void fraction in the database at 0.932, volumetric
allowance 230.5 - delivers **97.24**. Biggest pore measured, nearly the worst capacity:
a pore that large has too little surface per unit volume to approach the packing density
the bound assumes. The regression held where the independent argument said it would break
(largest underprediction 6.6 vs the +15.23 out-of-sample margin). Two still running.

## Tier D CLOSED - THE CLAIM
2021[Cu][sql]2[ASR]6, three claim-grade seeds 206.77 / 207.28 / 207.15.
**CLAIM = 207.07 +/- 0.37 cm3/cm3** (10,000+50,000 cycles, jobs 3473624-27).
Error bar rule: seed sem is 0.153, propagated block errors give 0.374, QUOTE THE LARGER.
The seed spread only measures how much converged chains differ from each other, not
whether they converged to the right distribution. See LOG 16:10 and 23:26.
Runner-up 2016[Cu][pts]3[ASR]1 = 199.90 +/- 0.38 (3 seeds). Margin 7.17 +/- 0.53.
Then 197.39, 196.30, 195.97 (all 3 seeds); 195.55, 193.91, 191.19, 190.79, 190.50 (1 seed).
Ordering identical at floor and claim cycles for all ten; shifts in [-0.53, +0.46].
Floor value was 207.60 +/- 0.93; claim-grade is 0.53 lower, the wave's largest shift and
still inside the floor error bar.
me004 comparison: parent claim-grade 207.07 vs me004 FLOOR 207.82 - NOT comparable.
e3 (me004 claim grade) is the only valid comparison and is still running.

## w5 COMPLETE (331 of 350) and w7 RUNNING
w5 block P: 133/150, max 178.35, none above 207.60. Block R: 198/200 uniform random draws,
max **143.58** (64.02 below the leader), zero exceedances -> 95% bound 1.50%, at most 126 of
8352. Residual bias -0.03, RMS 14.33; by band, pred 0-40 RMS 13.18 worst under +38.59 /
40-80 RMS 16.11 worst +54.39 / 80-300 RMS 12.08 worst +23.26.

**THE CEILING, IN THE ORDER THE REPORT SHOULD STATE IT.** Recompute with
scripts/blindbound.py; never quote these by hand.
1. MODEL-BLIND (leads the report; depends on neither gate). 484 uniform random draws from
   the unscreened remainder (w5 block R 198 + w7 block R2 286), zero above 207.60, max
   measured 154.29. 95% Clopper-Pearson: at most **0.62%, i.e. 52 of 8352**.
2. COVERAGE INEQUALITY. Coverage is complete only above the HIGHEST-PREDICTED STRUCTURE
   STILL UNMEASURED - not the selected depth (a queued task screens nothing), not the lowest
   measured prediction (unmeasured ones can sit anywhere in the block). Both were used and
   both were wrong; LOG 19:10. Currently pred2 > **140.69**; a counterexample needs
   pred2 < 140.69 AND an underprediction > **66.91**. When the 156 queued P-block structures
   land: > 128.95 and 78.65.
3. RESIDUALS, distributional NOT extremal. n=477 unbiased, mean -1.65, sd 13.26; tail counts
   above 20/30/40/50/60/66.91 = 30/15/5/2/0/0. The requirement is 5.17 sd out.
   **DO NOT quote the sample maximum as a margin.** It grew +11.69 (n=12) -> +23.26 (n=57)
   -> +43.80 (n=88) in the pred>80 band. LOG 20:42 withdraws the earlier "three times the
   worst observed" claim for exactly this reason.
   Also excluded: +54.89 from 2016[Cd][nan]3[ASR]34, predicted -54.9 and measured 0.0 - the
   model out of domain, not an error.

w7 (3473677, + up to 4 more jobs added by scripts/addjobs.sh as slots free): 450 structures,
519 CPU-h. block R2 = 300 more uniform random (queued FIRST) -> combined n=498 -> bound
0.60%, at most 50. block P2 = pred2 ranks 151-300 -> coverage depth 129.02 -> required
underprediction rises to 78.58. Selection in analysis/w7_selection.csv.

## Open tasks
- [ ] collect d0/d1/d2; report WC as mean over seeds with run-to-run spread as uncertainty
- [ ] collect w5; refit including block P+R; recompute the gate; report block R's
      false-negative rate as the model-blind bound
- [ ] collect m1 and w6; if any methylated variant beats the parent, extend the series
      and take the winner to claim grade
- [ ] status at a glance: scripts/status.sh (cluster time, jobs, usage, per-wave counts)
- [ ] write REPORT.md in the section 7 format; it also satisfies the day-7 interim (A1)

## Session-restart notes
- usage.json `tokens` is a PER-SESSION counter (it reset 0.73M -> 0.34M across a restart),
  so it cannot be read as a campaign total. `cpu_h_scheduler` IS cumulative.
- Session-side background waits do not survive a restart; the setsid'd login-node watcher
  scripts/slotwatch.sh does. Put anything that must happen unattended in the watcher.
- **Do not arm session-side background waits.** Two restarts inside ten cluster-minutes
  killed two of them. Instead each invocation runs ONE blocking foreground wait on the
  cluster - a loop that sleeps 30 s up to ~17 times and breaks early on a threshold - then
  scripts/status.sh. That buys ~8.5 min of cluster time per turn instead of ~40 s, which is
  the charter section 4 instruction to wait with sleeps rather than polling turns.
  Set the break thresholds ABOVE the current counts or the loop returns immediately.

## Budget position (update each check)
- 2026-08-31 01:08: cpu_h_scheduler **845.7 of 1610 (52.5%)**. Deadline is 5 days out.
  Still running: w8 (500 random, ~209 CPU-h total, about half done) and the four
  claim-grade modification runs e0-e3. Expect to finish the campaign near 1,050-1,100
  CPU-h, i.e. ~68% of the compute budget, with the remainder deliberately unspent:
  every argument the report leads with is already measured, and the alternatives priced
  at LOG 21:24 buy less than the reserve is worth against a cost model that scatters 1.8x.
- Tokens 3.40M of 32M this session (PER-SESSION counter, not a campaign total).
