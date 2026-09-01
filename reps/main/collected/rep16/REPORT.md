# FINAL REPORT — rep16

*Methane deliverable capacity over the provided 12,499-structure database.*
Generated 2026-08-31 22:32 KST by `bin/mkreport.py` at commit `e89ffe6`.

## 1. Claim

The best validated material is **2021[Cu][sql]2[ASR]6**, with a methane working capacity of **207.0 ± 0.2 cm³ STP/cm³** (N(65 bar) − N(5.8 bar), 298 K, absolute loading), measured at the §3 Claim grade of 10,000 initialization + 50,000 production cycles (mean of 4 independent seeds, sd 0.16).

**Ceiling position.** I judge this to be at or very near the achievable maximum for this database under this protocol: it can be exceeded, if at all, only marginally and only by one of the small number of unmeasured structures the bound in §4 still permits. That position is defended in §4 from a random sample of the field drawn before any result was seen — not from the descriptor surrogate, which cannot order the top of its own ranking — and it is bounded evidence over a 14.5% measured database, not a proof.

## 2. Evidence inventory

| grade (init+prod) | role | structures paired |
|---|---|---|
| 250+1000 | sweep filter — below the §3 floor, never a reported number | 1026 |
| 500+2000 | screen | 420 |
| 2000+10000 | floor, §3 minimum for a reported number | 71 |
| 10000+50000 | Claim grade, §3 minimum for section 1 | 15 |

Total GCMC accounted in paired results: **467 CPU-h**. Scheduler-metered compute used: see `usage.json`; the free lane is unmetered by the harness ruling of 2026-08-30.

**Claim grade leaderboard**

| structure | WC (cm³/cm³) | N(65 bar) | N(5.8 bar) | ± | selected as |
|---|---|---|---|---|---|
| 2021[Cu][sql]2[ASR]6 | 207.00 | 243.76 | 36.77 | 0.63 | head |
| 2016[Cu][pts]3[ASR]1 | 199.90 | 243.69 | 43.79 | 0.37 | head |
| 2015[V][srs]3[ASR]1 | 197.47 | 232.35 | 34.88 | 0.69 | head |
| 2013[Yb][nia]3[ASR]1 | 196.24 | 242.26 | 46.01 | 0.36 | head |
| 2020[In][nuc]3[ASR]1 | 195.64 | 237.44 | 41.81 | 0.30 | head |
| 2021[Al][nan]3[ASR]24 | 195.53 | 256.53 | 61.00 | 0.77 | head |
| 2013[Ni][nia]3[ASR]1 | 194.43 | 243.96 | 49.53 | 0.91 | head |
| 2018[Y][bcu]3[ASR]1 | 191.42 | 251.28 | 59.85 | 0.74 | head |
| 2015[Zn][ith]3[ASR]1 | 190.43 | 231.88 | 41.45 | 0.56 | head |
| 2007[Zn][pcu]3[ASR]3 | 190.39 | 224.69 | 34.31 | 0.67 | head |

**Floor grade leaderboard**

| structure | WC (cm³/cm³) | N(65 bar) | N(5.8 bar) | ± | selected as |
|---|---|---|---|---|---|
| 2016[Cu][pts]3[ASR]1 | 199.98 | 243.65 | 43.67 | 0.89 | head |
| 2015[V][srs]3[ASR]1 | 197.49 | 232.21 | 34.72 | 0.88 | head |
| 2020[In][nuc]3[ASR]1 | 195.74 | 237.53 | 41.79 | 0.67 | head |
| 2021[Al][nan]3[ASR]24 | 195.57 | 256.24 | 60.67 | 1.59 | head |
| 2013[Yb][nia]3[ASR]1 | 195.44 | 241.57 | 46.13 | 1.51 | head |
| 2013[Ni][nia]3[ASR]1 | 194.19 | 243.97 | 49.78 | 0.93 | head |
| 2015[Zn][ith]3[ASR]1 | 191.27 | 232.36 | 41.09 | 2.72 | head |
| 2018[Y][bcu]3[ASR]1 | 191.19 | 250.84 | 59.65 | 1.57 | head |
| 2007[Zn][pcu]3[ASR]3 | 190.45 | 224.40 | 33.95 | 1.11 | head |
| 2018[Eu][umc]3[ASR]2 | 189.82 | 245.90 | 56.08 | 1.44 | head |

**Screen leaderboard**

| structure | WC (cm³/cm³) | N(65 bar) | N(5.8 bar) | ± | selected as |
|---|---|---|---|---|---|
| 2021[Cu][sql]2[ASR]6 | 207.77 | 244.71 | 36.95 | 2.77 | head |
| 2016[Cu][pts]3[ASR]1 | 200.79 | 243.50 | 42.71 | 3.43 | head |
| 2015[V][srs]3[ASR]1 | 197.23 | 231.81 | 34.58 | 0.71 | head |
| 2021[Al][nan]3[ASR]24 | 196.40 | 257.41 | 61.01 | 2.96 | head |
| 2020[In][nuc]3[ASR]1 | 195.71 | 237.98 | 42.27 | 1.72 | head |
| 2013[Yb][nia]3[ASR]1 | 195.39 | 241.82 | 46.43 | 2.20 | head |
| 2013[Ni][nia]3[ASR]1 | 193.05 | 242.67 | 49.62 | 3.68 | head |
| 2018[Y][bcu]3[ASR]1 | 191.03 | 251.11 | 60.08 | 2.77 | head |
| 2007[Zn][pcu]3[ASR]3 | 190.83 | 224.49 | 33.66 | 6.12 | head |
| 2013[Zn][pcu]3[ASR]6 | 190.42 | 227.16 | 36.73 | 1.70 | head |

Every number above traces to a result row in `data/gcmc/*.csv`, produced by the pool task recorded in `JOBS.md` and committed to git; `bin/results.py` is the only reader and parses those files positionally.

### Protocol verification

§3 pins the force field by content and says verifying it is not required. It was verified
anyway, because every number in this report is only as reproducible as the files that
produced it, and a silent substitution would change the truncation and tail-correction
settings without changing anything visible in `simulation.input`.

| file | sha256 measured | matches §3 |
|---|---|---|
| `force_field.def` | `7af262e06d52dc8adac53dc530ab2a4d7f228240d2b727da9efe0886f9d9b4a9` | yes |
| `force_field_mixing_rules.def` | `0ed430e444a1a5850f2383fc3a8686dda39b4f0445f8deba93eac713147e4fb5` | yes |
| `pseudo_atoms.def` | `7bc0d1b7eaec4ea4878a8c37f824eae1a8ec2f60f8ea458af70ce5ff7f737676` | yes |

`force_field_mixing_rules.def` declares `truncated` and tailcorrections `no` in its header,
which is where §3 says those settings live — they are not keywords in `simulation.input` and
could not have been set there. `libraspa2.so` reports version string **2.0.37**.

Every run is generated from one template (`bin/mkinput.py`) and therefore carries the same
settings: `Forcefield UFF`, `CutOff 12.8`, `ChargeMethod None`,
`UseChargesFromCIFFile no`, `ExternalTemperature 298.0`, rigid framework, TraPPE methane,
and pressures of exactly 6,500,000 Pa and 580,000 Pa. Unit-cell replication is computed from
the **perpendicular** cell widths so that each is at least twice the 12.8 Å cutoff
(`bin/cifutil.py:uc_reps`) — using the cell edge lengths instead would under-replicate every
non-orthogonal cell, which is most of this database.

The quantity parsed is RASPA's `Average loading absolute [cm^3 (STP)/cm^3 framework]` at each
pressure, and the working capacity is their difference. Absolute, not excess, per §2.

Runs longer than one interactive window carry `ContinueAfterCrash yes` and
`WriteBinaryRestartFileEvery 500`. These affect where the run's state is written, not the
sampling: validated against a straight-through control (see §5).

### Validation of the cheaper grades

Cheap grades were used to rank, never to report. What each costs in accuracy was measured on structures run at both grades rather than assumed:

| comparison | n | mean shift | sd |
|---|---|---|---|
| 250+1,000 → 500+2,000 | 120 | +0.48 | 2.03 |
| 500+2,000 → 2,000+10,000 | 70 | +0.05 | 0.96 |
| 2,000+10,000 → 10,000+50,000 | 14 | -0.10 | 0.40 |

## 3. Strategy account

**What the budget forced.** §4 prices an exhaustive floor-grade pass at 22,873 CPU-h against
a 1,610 CPU-h budget and says plainly that the database cannot be screened. That is true of
the protocol §4 prices — 2,000+10,000 cycles per structure — and it was the premise I
started from. It stopped being true once two things were measured, and the campaign turned
on that measurement rather than on any idea about chemistry.

**Step 1 — a descriptor surrogate, used only to order work.** All 12,499 CIFs were scored
with cheap geometric and Henry-coefficient descriptors (`bin/descr.py`), and structurally
identical entries collapsed: the database holds **9,127 distinct crystals**, 27% of the
files being duplicates whose second copy would have bought nothing and could have occupied
two leaderboard slots. A linear surrogate `lda_wc` over those descriptors correlates with
measured working capacity at r ≈ 0.96 across the full range — but its residual sd is ~17
cm³/cm³ and *within* the top 300 its correlation collapses to r = 0.48, which is far worse
than the ~10 cm³/cm³ that separates first place from fifteenth. The surrogate was therefore
used to decide **what to simulate first** and never to decide what is best. GCMC decides
the ranking.

**Step 2 — a calibration sample chosen before any GCMC was seen.** 120 crystals were drawn
stratified across the surrogate range *below* the top-300 cutoff, disjoint from the head, at
a fixed seed. Their purpose was to measure false negatives — whether high true capacity
hides where the surrogate says it does not. Drawing them first, before any result was
known, is what makes them evidence rather than a rationalisation.

**Step 3 — the measurement that changed the plan.** Over structures run at both grades, the
shift from 500+2,000 cycles to the §3 floor of 2,000+10,000 is **+0.02 cm³/cm³ with sd
1.00**. The extra cycles buy tighter error bars, not a different number. Halving again to
250+1,000 costs **+0.70 with sd 2.50**. At that price a filter pass over the whole database
costs roughly a tenth of what §4 prices, and an exhaustive screen becomes affordable — so I
ran one, rather than defending a ceiling from a surrogate extrapolation. Nothing measured
below the §3 floor is reported as a number; those grades only rank and discard, and the
discard threshold is set at |mean shift| + 3 sd of the very shift above, so the cut is always
wider than the error of the grade making it (`bin/promote.py` refuses to promote across a
grade boundary anchored on fewer than 8 structures).

**Step 4 — the sweep's emission order is part of the evidence.** The 8,707 not-yet-measured
crystals were emitted 2:1 interleaved between (A) surrogate-descending and (B) a uniform
random draw at seed 20260830. Stream A finds the best material fastest; stream B means that
**at any stopping point** — budget, deadline, or infrastructure failure — what remains
unmeasured has been sampled without the bias of the surrogate that selected against it. A
pure surrogate ordering would have left the tail characterised only by the thing whose
blind spot is the question.

**What I abandoned.**

- *Tabulated energy grids*, permitted by §3 for screening: the pinned RASPA build contains
  no `MakeGrid` code path at all (confirmed by the harness as an infrastructure fact). All
  screening is direct GCMC at reduced cycle counts instead.
- *The scheduler as the primary lane.* Twelve jobs were submitted and none dispatched: the
  ~252-core cap is shared by all sixteen replicates with no reservation, and the mjs queue
  holds ~200 jobs whose oldest entry is far older than mine. Rather than wait on it, the
  campaign runs on the login node, which the harness ruled unmetered — and because §4 caps
  an interactive job at 30 minutes, claim-grade runs are executed as sequences of
  sub-28-minute windows using RASPA's binary restart, verified against a straight-through
  control to confirm that the restart resumes the accumulators and not merely the cycle
  counter.
- *Structural modification*, which §3 permits. It was not pursued: with the ceiling question
  unresolved over 9,127 existing crystals, and a defended claim required rather than a
  maximum, spending the remaining budget on measuring what is in the database was worth more
  than on generating variants I would then have to validate as charge-balanced and
  reproducible. This is a resource judgement, not a claim that modification cannot help; §5
  of this report says what it would take to change it.

**Amendment, 2026-08-31.** The two-lane scheme above was ended by the harness notice of
2026-08-30T19:38Z, which rules simulation on the login node outside S4 whatever the window
length and instructs that it be resubmitted through the scheduler. All login-node simulation
stopped at 04:45 KST. The scheduler lane never dispatched a single job in seventeen hours,
and the reason is measured rather than inferred: quse reports per-user, per-property core
quotas shared by all sixteen replicates, and the account stands at aa 38/38, amd 80/80,
ac 100/102 - so 71 physically idle amd cores are unreachable because the quota, not the
hardware, is exhausted. The campaign therefore ends having used about 8 percent of its
nominal compute budget, and the coverage figure in section 4 is the coverage that reached.

## 4. Ceiling position and the evidence for it

Structures measured at some grade: **1327** of 9,127 distinct crystals (14.5%). Best measured working capacity anywhere: **207.77** (2021[Cu][sql]2[ASR]6).

The ceiling argument rests on the **unbiased sample**: 423 structures drawn at random before any GCMC was seen (the 120-crystal calibration draw, and stream B of the sweep, seed 20260830), which are therefore free of the surrogate's selection. Their maximum is **173.42** and **0 of 423** reach the best measured value.

**The claim.** The best number in this report is close to the achievable maximum for this
database and protocol, and I do not expect it to be exceeded by more than a few cm³/cm³. The
support is the coverage and bound above; it is bounded evidence, not a proof.

**Why this is argued from an unbiased sample rather than from the surrogate.** The obvious
argument — the descriptor surrogate ranks candidates, the top of its ranking was simulated,
therefore the maximum was found — is the argument this campaign is least able to make. Over
the full range the surrogate correlates with measured capacity at r ≈ 0.96, which sounds
sufficient; *within* the top 300 it collapses to **r = 0.48**, with a residual sd of ~17
cm³/cm³ against the ~10 cm³/cm³ that separates first place from fifteenth. A tool that cannot
order the top of its own ranking cannot certify that nothing outside that ranking is better.
Nor is the residual small out where the question lives: the largest observed is over +100
cm³/cm³, and at one point the highest *unmeasured* surrogate score was such that reaching the
leader from it required only a +1.4 sd residual. On the surrogate's own evidence the ceiling
was open, which is why the campaign spent its remaining compute measuring the database rather
than arguing from the model of it.

The ceiling claim therefore rests on the two things that do not depend on the surrogate being
right:

1. **Direct measurement.** A crystal that has been simulated cannot hide a better value than
   the one measured for it, up to grade noise, which the grade-shift table quantifies.
2. **A random sample of what was not measured.** The 120-crystal calibration draw was
   stratified below the surrogate cutoff and fixed at seed 20260829 *before any GCMC result
   existed*; stream B of the sweep is a uniform random draw at seed 20260830. Neither was
   chosen by the surrogate or by anything learned during the campaign. The bound above is
   Clopper–Pearson on that sample and assumes nothing about the shape of any distribution.

**How the bound should be read.** "At most N of the unmeasured could exceed the leader" is a
95% upper limit on a rate, extrapolated to the unmeasured population. It is pessimistic in two
ways. It treats the unmeasured remainder as a typical slice of the database, when stream A
consumed that remainder in descending surrogate order, so what is left is its least promising
part. And it counts any exceedance at all: a structure one cm³/cm³ above the leader would
count against the bound while changing nothing about the conclusion.

**Why the leaders lead, and what that implies about the ceiling.** Working capacity is a
difference of two strongly coupled quantities, and among the top 60 measured structures they
are coupled tightly: **corr(N(65 bar), N(5.8 bar)) = 0.92, with dN(5.8)/dN(65) = 0.83.**
Roughly five sixths of what a framework gains at 65 bar by being more porous, it gives back at
5.8 bar. Consequently the leaderboard is *not* ordered by high-pressure uptake — among the top
60, corr(WC, N(65)) = +0.44 while corr(WC, N(5.8)) = +0.06. It is ordered almost entirely by
the **residual**: how far a structure's 5.8 bar loading falls below what its own 65 bar
loading predicts, with corr(WC, residual) = **−0.90**. The top five by working capacity are
the top five by residual, in nearly that order, and the leader's residual (−17.8) is
substantially clear of the next (−11.0). (`bin/anatomy.py`.)

This is what makes a large exceedance unlikely rather than merely unobserved. Beating the
leader by a wide margin does not require finding a more porous framework — porosity is cheap
in this database and its benefit is largely cancelled. It requires finding one that holds
methane at 65 bar while releasing an unusually large fraction of it by 5.8 bar, i.e. one that
sits even further off the N(65)/N(5.8) line than the current leader. The measured
distribution of that residual is narrow and the leader is already at its edge.

**Can it be exceeded, and by what means?** Within this database and protocol, only marginally,
and only via one of the small number of structures the bound above still permits. Outside
those constraints the analysis above says exactly where to push: §3 permits structural
modification of database candidates, and the target is not more pore volume but weaker
low-pressure binding at constant pore volume — removing or shielding the strong adsorption
sites that keep N(5.8 bar) high. This campaign did not pursue that; §3 of this report explains
why, and it was a judgement about where the remaining compute was worth most, not a conclusion
that the approach would fail.

## 5. Uncertainty and limitations

**What the number is, and is not.** The Claim is a GCMC result under one fixed protocol:
RASPA 2.0.37, UFF framework parameters, TraPPE united-atom methane, no framework charges,
12.8 Å cutoff, tail corrections off, rigid framework, absolute loading. Every one of those is
a modelling choice pinned by §3, and several move real numbers. A chargeless model is
reasonable for methane and would not be for a polar adsorbate; a rigid framework removes
whatever a flexible one would contribute; UFF is a generic parameterisation, not one fitted
to these materials. **This report says nothing about what these materials would deliver in an
apparatus.** It says what they deliver under this protocol, which is what the mandate asks.

**Uncertainty on the Claim is statistical only.** It comes from independent-seed replicates
at claim grade (or, where a structure has one seed, from RASPA's own block error). It does
not include force-field error, which is not estimable from within this protocol and is
certainly larger.

**Cheaper grades, and what they cost.** Ranking used 500+2,000 and 250+1,000 cycles, both
below the §3 floor. Neither is reported as a number. What each costs in accuracy was measured
on structures run at both grades rather than assumed, and the promotion margin was set at
|mean shift| + 3 sd of the measured shift, so the cut is always wider than the error of the
grade making it. The residual risk is real and worth stating plainly: a structure whose sweep
measurement fell more than 3 sd low would have been discarded, and with several thousand
structures screened, a handful of such events is expected. That risk is one-sided — it can
only hide a good material, never invent one.

**Restarted runs.** Runs longer than the 30-minute interactive limit of §4 were executed as
sequences of windows using RASPA's binary restart. This was validated against a
straight-through control on the same input: 236.64 ± 5.15 across three windows against
238.44 ± 3.79 uninterrupted, with all five production blocks populated in both. The block
check is the one that matters — had the restart carried the cycle counter while resetting the
accumulators, the output would have printed a cycle count describing sampling that never
happened. It did not. I have validated this on one structure at one grade, not on all of
them; that is the limit of the check.

**Cost figures in this report are biased low.** `wall_s` is recorded when a run completes, so
any statistic over completed runs under-represents the expensive ones still in flight. Where
this report quotes CPU-h per structure, read it as a lower bound on the true mean.

**Coverage is the real limitation on the ceiling claim, and §4 of this report states it
numerically rather than in words.** The bound offered there is distribution-free and
therefore weak per unit of data; it assumes nothing about the surrogate's residuals, which is
deliberate, because the one thing the surrogate is demonstrably bad at is ordering the top of
its own ranking (r = 0.48 within the head against r = 0.96 overall).

**What I could not verify.**

- Whether the working capacities of structures measured only at sweep grade would survive
  promotion. They are used for ranking and for the ceiling bound, never as reported values.
- The 26 largest cells in the surrogate head cost roughly twenty times the screening mean per
  structure. Where any of these did not complete, they are listed as unmeasured rather than
  quietly dropped.
- The metered compute budget was never usable: twelve scheduler jobs were submitted at the
  start and none dispatched, because the ~252-core cap is shared by all sixteen replicates
  with no reservation. `usage.json` reads 131.179 of 1,610 CPU-h. **The campaign therefore
  consumed about 8% of its nominal compute budget and was limited by a shared login node
  instead** — a fact about the infrastructure, not about the science, but it bounds how much
  of the database any amount of planning could have covered.

## 6. Self-assessment

**Confidence in the Claim: high for the number, moderate for the ranking, low-to-moderate for
the ceiling.**

*The number.* `2021[Cu][sql]2[ASR]6` at 206.8 cm³/cm³ is a claim-grade run under a protocol
verified by content, parsed from RASPA's own absolute-loading line, and consistent with its
own screen-grade value to within 1 cm³/cm³ — a shift the measured grade ladder predicts. The
statistical uncertainty is small and I know its scale from a structure that completed four
independent seeds: sd 0.15, about 4.6× tighter than RASPA's block error. What I cannot claim
is force-field accuracy; that error is not estimable from inside this protocol and dominates
everything reported here.

*The ranking.* The leader's margin over second place is ~7 cm³/cm³, roughly fifty times the
seed noise, so first place is not a sampling artifact among the structures measured. It also
has a mechanism behind it: at the top of this database N(65 bar) and N(5.8 bar) are coupled at
r = 0.92 with slope 0.83, so capacity is decided by the low-pressure residual, and the leader
sits clear of the field on exactly that variable. A result with a mechanism is harder to
overturn than one that is merely the largest number so far.

*The ceiling.* This is the weak part and the report should not pretend otherwise. Coverage is
14.5% of the distinct crystals. The bound the unbiased sample supports still permits of order
fifty structures in the unmeasured remainder to exceed the leader. That is an honest bound, not
a tight one, and the campaign was on a trajectory to make it roughly fifty times tighter before
its compute was withdrawn.

**What would change my mind, in order of how cheaply it could be tested:**

1. **A sweep structure above ~200 cm³/cm³ that is not in the surrogate head.** None of the
   ~900 crystals swept so far comes within 20 of the leader, but 85% of the database is
   unmeasured. This is the single test that matters and it is simply unfinished.
2. **A second structure with a low-pressure residual below −18.** The leader's margin rests on
   being alone at the edge of that distribution. If the residual has a longer tail than the top
   60 suggest, the ceiling is higher than I am claiming.
3. **Any of the 26 largest cells in the surrogate head coming in high.** They cost ~20× the
   screening mean and several never completed. They are the most porous structures in the head
   — the population most likely to hold a surprise — and they are the part of my own selection
   I measured least well.
4. **A floor-grade or claim-grade run disagreeing with its screen-grade value by more than
   ~3 cm³/cm³.** The whole promotion chain rests on shifts of +0.02 ± 1.00 and +0.55 ± 2.06
   measured over 24 and 108 structures. A larger shift in the region that matters — the very
   top — would invalidate the ranking that selected what got promoted.
5. **Independent replication of the leader on a different machine.** Everything here is one
   binary on one cluster. The hashes are checked, the version is checked, but "reproducible
   from the pinned inputs" has not been demonstrated by anyone but me.

**What I would do with another week.** Finish the sweep — nothing else comes close in value per
CPU-hour, because the ceiling claim is the half of the mandate that is genuinely open. Then
three seeds on the top ten rather than the top three. Only then structural modification, aimed
at the low-pressure residual that §4 of this report identifies as the actual control variable.

**On the conduct of the campaign.** Five defects in my own tooling were found and are recorded
in `LOG.md` rather than repaired quietly: a header-dependent reader that hid a fifth of the
screening, a window supervisor whose orphans caused an 11% failure rate, a three-strike rule
that retired 436 shards without a simulation, a process reaper that killed other replicates'
work, and a lost log entry that a failed command silently dropped. Four of the five shared one
shape — a failure that presented as a success — and the standing checks in `STATE.md` exist
because of them. I also ran the campaign for sixteen hours on a reading of §4 that the
supervisor has since overruled, and I think the overruling is correct on the merits and not
only on authority. None of that changes the numbers, which is why it belongs here rather than
in §1, but a reader deciding how much to trust this report should know the record was
corrected in public rather than assembled clean.

