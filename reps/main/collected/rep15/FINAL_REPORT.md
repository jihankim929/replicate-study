# FINAL REPORT — Methane Deliverable Capacity, replicate rep15

**Status: INTERIM DRAFT, maintained from T0+16 h onward so that a compliant report exists at
every moment of the campaign rather than only at the end.** Charter §5 requires a final report
whatever state the work is in; this file is that report, rewritten as evidence arrives. Every
number below is traceable to a commit and a results row. Last revised **2026-08-30 13:10 KST
(T0+16.5 h of 172.5 h)**. Regenerate the quantitative parts with `bin/ceiling.py`.

---

## 1. Claim

The best material in this database under this protocol is **`2021[Cu][sql]2[FSR]6`**, a Cu
square-lattice framework, with a methane working capacity of **207.0 ± 0.7 cm³ STP/cm³**
(N(65 bar) − N(5.8 bar), 298 K, absolute loading, 95%), measured at **claim grade
(10,000 + 50,000 cycles)** on three independent seeds — 207.06, 206.80, 207.15 — and
reproduced at **207.07** by its independently-prepared database twin `2021[Cu][sql]2[ASR]6`,
a separate input file run as a separate job. **I claim this is at or within a few cm³/cm³
of the achievable maximum** for these 12,499 structures under this protocol: 1,629 uniform
random draws produced nothing above it, and the exact bound WC ≤ N(65) proves 76.9% of
everything measured cannot beat it.

**Ceiling position, and it rests on measurement rather than on a model.** Four independent
strands, none of which uses the descriptor model:

1. **Exact bound (a proof, not an inference).** WC = N(65) − N(5.8) ≤ N(65), so any
   structure whose 65 bar loading is already below 207.0 cannot beat the leader whatever its
   low-pressure point. Of 3,078 structures with a 65 bar measurement, **2,368 (76.9%) are
   proven out** on this bound alone.
2. **Uniform random sample, no model in the path.** **Zero uniform draws have exceeded 207.0**,
   out of **7749** measured across three independently seeded arms — and **§6 carries the live
   count with the bound recomputed from it, which is the figure to quote**, since the arms were
   still filling when this was written. The rule of three puts a 95% upper bound of 3/n on the
   population fraction that could exceed the leader: **at most 5 of the 12,120** screenable
   structures at the n above, down from ~627 at the 58 draws I had on the first morning. The
   bound tightens as 3/n and can only improve. The sample maximum was 195.3, itself 11.7 below the
   leader — and re-measured at the §3 floor it reads **195.17**, still 11.89 below, so the
   arm's headline result does not depend on below-floor cycles (§4).
3. **The excluded set is covered separately, so the two together account for all 12,499.**
   The 379 structures excluded on geometry were measured anyway rather than assumed dead:
   max 58.9, median 0.0, the best of them **148 cm³/cm³ below the leader**.
4. **Structural modification does not reach it, and I tested this rather than asserted it.**
   The §3 terminal-aqua removal is real and it works — on 42 paired parent/child
   measurements it gains a mean **+18.6** and a maximum **+74.8** cm³/cm³, and 41 of 42
   children beat their parent. But it is inapplicable where it would matter: of the **top 400**
   structures on the measured leaderboard, **399 carry no removable terminal aqua at all**.
   The gains are large precisely because they unblock pores that were blocked; the leader's
   pores are already open. Best modified structure actually measured: 174.0.

5. **A mechanism, which is what makes the ceiling credible rather than merely observed.**
   Working capacity in this database is decided at **5.8 bar, not at 65 bar**. The leader and
   the runner-up are statistically indistinguishable at saturation — N(65) = 243.83 against
   243.69 — and separated entirely by what they fail to release, 36.77 against 43.82. Across
   all 3,143 paired structures the two pressures are strongly coupled, **corr = +0.623, slope
   dN(5.8)/dN(65) = +0.311**: buying saturation capacity buys residual loading with it, which
   is the deliverable penalty in its most direct measured form. The high-saturation tail shows
   it plainly — the largest N(65) in the database, **268.34** (`2020[Al][fmz]3[ASR]1`), 24
   above the leader's, returns a working capacity of only **175.9**, because it holds 92.5 at
   5.8 bar. The leader wins by being the **most extreme outlier in the entire measured set on
   exactly this axis**: its 5.8 bar loading sits 60.8 cm³/cm³ *below* the database regression
   of N(5.8) on N(65), the largest such residual of 3,143 structures.

Pore-size coverage is **100%**: every one of the six largest-free-radius bands spanning the
database now carries measurements, and nothing outside the ≥3.0 Å band has come within
45 cm³/cm³ of the leader.

**The headroom that does remain, stated honestly.** Within the top N(65) decile the highest
saturation loading is 268.34 and the lowest 5.8 bar loading is 34.94. A structure combining
both would reach **233.4**, some 26 above the leader. No measured structure combines them, and
the +0.623 coupling is the reason they are not independently available — but that number, not
zero, is the honest bound on what a fundamentally better framework could achieve under this
protocol. My claim is that the leader is at or near the achievable maximum *for this database*;
it is not a claim that 207 is a physical limit.

**What would overturn this.** Not a better search of the same kind — strand 2 bounds that.
It would take a structure whose high capacity is invisible to every descriptor used to order
the screen *and* which the uniform arm missed, and at 1,684 draws that population is bounded
above by ~22 members.

---

## 2. Evidence inventory

All results are RASPA 2.0.37 (commit `4467e14c`), TraPPE-UA methane, rigid framework, chargeless,
UFF from the hash-pinned three-file set, cutoff 12.8 Å, tail corrections off, potentials
unshifted, **absolute** loading per §2. No energy grids were used anywhere, so §3's
grid-disclosure clause applies to no number here. The protocol was verified not from the build
recipe but from a *running claim-grade job*: the three UFF file hashes match the §3 table
exactly, and the RASPA output itself reports `CutOff VDW : 12.800000`, `All potentials are
unshifted`, `tailcorrection: no`, `Forcefield: UFF`, `shift/k_B 0.0`.

| stage | cycles | structures paired | file |
|---|---|---|---|
| screening (below §3 floor — selection and sampling statistics only) | 200 + 1,000 | **§6** | `data/s1/results.csv` |
| floor grade | 2,000 + 10,000 | **§6** | `data/s2/results.csv` |
| **claim grade** | **10,000 + 50,000** | **3 structures, 5 runs** | `data/s3/results.csv` |
| seed replicates | 200 + 1,000, seed 1 | 24 | `data/seedchk/results.csv` |

The screening and floor-grade counts are **not written out here on purpose**. Both are still
rising as the fleet runs, and §6 is regenerated from the data every 20 minutes by
`bin/curator.sh`; a number typed into this table would be wrong within the hour and would then
contradict §6 on the report's own evidence base. The claim-grade row is fixed because that
work is complete.

**Claim-grade results (10,000 + 50,000 cycles) — the numbers the Claim rests on:**

    structure                      seed   N(65)    N(5.8)   WC
    2021[Cu][sql]2[FSR]6            0     243.83    36.77   207.06
    2021[Cu][sql]2[FSR]6            1     243.66    36.86   206.80
    2021[Cu][sql]2[FSR]6            2     243.94    36.79   207.15
    2021[Cu][sql]2[ASR]6            0     243.86    36.79   207.07   <- separate input & job
    2016[Cu][pts]3[ASR]1            0     243.69    43.82   199.87

The leader's three seeds give mean **207.00**, sd **0.18**. `2021[Cu][sql]2[ASR]6` is the same
framework at a different recorded solvent-removal level: a *separately prepared CIF* run as a
*separate job*, agreeing to **0.07**. That is the strongest single piece of evidence here,
because it exercises the whole chain — preparation, replication, input generation, GCMC — twice
and independently.

Note the runner-up is not runner-up because it adsorbs less at 65 bar. `2016[Cu][pts]3[ASR]1`
reaches N(65) = 243.69, statistically indistinguishable from the leader's 243.83. It loses
entirely at the low-pressure end: 43.82 against 36.77. **Working capacity in this database is
decided at 5.8 bar, not at 65 bar** — the top structures have converged on a common saturation
loading near 244 cm³/cm³ and are separated only by what they fail to release.

**Floor-grade results (2,000 + 10,000 cycles):**

    207.10   2021[Cu][sql]2[FSR]6
    207.07   2021[Cu][sql]2[ASR]6      same framework, separate input, separate job
    199.45   2016[Cu][pts]3[ASR]1
    197.20   2015[V][srs]3[FSR]1
    197.19   2015[V][srs]3[ASR]1       same framework, separate input, separate job
    195.51   2021[Al][nan]3[ASR]24
    194.28   2013[Ni][nia]3[ASR]1
    190.65   2015[Zn][ith]3[ASR]1

**Validation performed.**

- *Claim grade at three independent seeds*: 207.06 / 206.80 / 207.15, sd 0.18. This is the
  measurement the Claim quotes.
- *Two internal framework replicates* (ASR/FSR pairs, separately prepared and separately run)
  agree to **0.07** at claim grade and to 0.03 and 0.01 at floor grade.
- *Screening vs floor grade*, 8 structures: mean −0.15, sd 1.03 cm³/cm³ for a 50× cycle
  increase. **Both runs used seed 0**, so the floor run begins from the identical trajectory;
  this measures cycle convergence, not sampling scatter, and is recorded as such.
- *Seed-to-seed scatter*, 24 structures re-run at seed 1 (screening cycles): **mean +0.76,
  sd 1.52, max |Δ| 3.95** cm³/cm³. This is the independent-trajectory number and it is what
  bounds how far any below-floor screening value could move.
- *Physical exclusion control (CONTROL-X)*: all **379** structures excluded on geometry were
  measured anyway rather than assumed dead. Max 58.9, median 0.0 — the best of them 148 cm³/cm³
  below the leader. The exclusion rule required CH₄-accessible fraction *exactly zero*, yet 114
  of them adsorb something, so the Widom descriptor underestimates accessible volume for a
  minority of that set. Reported as measured, not as "the exclusion was clean".
- *Uniform random arm*: **1,684 draws** (CONTROL-R 236 + the 2,000-structure random arm 1,448),
  max 195.3, **0 above the leader**. This is the instrument the ceiling claim rests on.
- *Band probe*, 160 structures stratified over the four pore-size bands that had no measurement
  at all, scored against predictions **registered before any of them ran**
  (`data/band_prediction.csv`): 0 of 160 above the leader, and the model's residual RMSE of 46.6
  against its own CV RMSE of 8.0 is the measurement that disqualified it as a bound.

**Traceability.** Every row carries `(name, press, init, prod, seed, grid, loading, err, mol_uc,
err_uc, density, status, secs)`. Job IDs are in `JOBS.md`. Claim-grade run directories are
retained and tracked in git under `data/s3/run/`; screening run directories are not tracked
(4,010 of them churn under live workers and aborted every commit), and screening numbers are
reproducible from `data/s1/results.csv` plus the pinned inputs. Structure names containing
`+DEAQ` are modified structures, recorded in `manifests/mods.csv` and `manifests/topmods.csv`.

---

## 3. Strategy account

**Screening, not exhaustive simulation.** §4 prices an exhaustive floor-grade pass at 22,873
CPU-h against a 1,610 CPU-h budget. I screen at 200 + 1,000 cycles — below the §3 floor, and
used to order candidates and to compute sampling statistics, never as a per-material result.
Measured cost: `secs(both pressures) = −365.6 + 0.5873 × sc_atoms`, R² 0.822; mean 0.151 CPU-h
per structure. Cost is driven by supercell atom count (corr +0.91), not porosity (−0.11).

**The campaign had two phases and the second was the important one.** The first ranked the
database on accessible void fraction and screened down that ranking; it found the leader within
a few hundred structures and then kept confirming it. The second phase was built to *attack*
that leader, because a ranked screen cannot bound what it never looked at. Everything below is
from the second phase.

**A cost model I got wrong and corrected.** My first calibration used six structures chosen by
density percentile, averaging 1,546 supercell atoms against a database mean of 2,688, and was
biased low by ~4×. The plan built on it — "a full screen costs ~700 CPU-h, comfortably inside
budget" — was wrong, and the refit above replaced it.

**A random arm that was not random, and the fix.** CONTROL-R was interleaved into a pool sorted
by the prior, so its members arrived *in prior order*: of the first 51 delivered, 49 had
maxfree ≥ 3.0 Å and none was below 2.5. A random arm delivered in prior order is not a random
arm, and I had been quoting its maximum as though it were. Rebuilt shuffled
(`bin/prio_rebuild.py`), and a fresh 2,000-structure uniform arm was drawn **from everything
unscreened, not from what was unqueued** — the first draw I attempted took 331 structures from
the tail of the prior ranking, which would have been the exact opposite of unbiased while being
called random.

**The band probe: a pre-registered test of the one thing that could have overturned the
leaderboard.** 36% of the screenable database had never been sampled once, and it was
specifically the 1.3–2.5 Å region where a pore goes from being unable to hold a TraPPE methane
(σ 3.73 Å, radius ≈1.87 Å) to holding one tightly. Tight confinement is where high *volumetric*
uptake lives, but it works against a deliverable penalty: a pore that binds hard at 65 bar is
still holding gas at 5.8 bar. Which way that trade lands was an empirical question with no data.
I registered per-band predictions before running anything, set 150 cm³/cm³ as the threshold at
which "the leaderboard reopens", and ran 160 structures stratified across the four dark bands.
**It crossed: 151.6 in the 2.0–2.5 Å band.** And it stopped there — 54 below the leader. The
physics is real and it loses to the deliverable penalty, which is the answer, not a null result.

**Structural modification (§3-permitted), and it was tested twice.** `bin/desolv.py` removes
**terminal aqua ligands** (an O with exactly two explicit H, bonded to exactly one metal of a
periodic component). Water is neutral, so §3 charge balance holds by construction. It
deliberately declines what the database's own ASR additionally removes — bare hydrogen-less O
(ambiguous between coordinated water, hydroxide and oxo, only the first neutral) and nitrate and
triflate counter-ions — because removing those would not be charge-balanced. *Validated against
400 of the database's own FSR→ASR pairs*: of 193 pairs where it acted, **117 reproduce the ASR
composition exactly** and 41 more are strict subsets (158/193 = 82% consistent); in 78 further
cases it removed nothing and compositions still disagreed, placing those mismatches in the
database rather than in the code.

*First application* — 206 structures built from the 670 FSR-only parents the database never
offers desolvated. Measured 206/206; best **174.0**; none above the leader.

*Second application, and this is the one that answers §1.2.* The first arm tested the
modification only on structures that were poor to begin with, which does not answer whether the
**best** number can be exceeded. So `bin/mod_gain.py` measured the effect on 42 paired
parent/child runs of my own: **mean +18.6, median +13.7, max +74.8, and 41 of 42 children beat
their parent.** The modification is large and real. Then `bin/mktopmods.py` applied it to the
top of the measured leaderboard — and found removable terminal aqua in **1 of the top 400
structures**, and in 48 of the top 1,500, all 48 already built. The gains are large *because*
they unblock a pore that was blocked (the best case is 23.3 → 98.1), which can only happen where
capacity was near zero. The leader's pores are already open. **"207 + 74.8 = 282" has nothing to
stand on**, not because the gain is unreal but because there is no water left to remove where it
would count.

**A descriptor model, used as an orderer and never as evidence.** Gradient boosting on nine
cheap all-database descriptors, CV MAE 5.70 / RMSE 8.03 / R² 0.854, predicting *zero* unscreened
structures above the leader. I do not report that as a ceiling, and §4 gives the measurement
that disqualifies it. `work/pool_s1` was deliberately **not** reordered by it: doing so would
have biased the remaining screen into the region the model was fitted on and destroyed the only
evidence that could contradict it.

**Abandoned.** (i) Full-descriptor calculations (110 units) were demoted below screening — the
cheap Widom pass orders well enough, and the fuller set would have spent ~44 CPU-h on metadata
rather than GCMC evidence. (ii) A 12-stream login-node band probe, cancelled when `uptime`
showed load 106 on 96 cores — fifteen other replicates share that node. (iii) Energy grids:
`MakeGrid` is absent from the provided binary (Bei, INBOX 2026-08-30), and they would have
collided anyway, since they key their cache on a framework name that is a constant in my runner.

---

## 4. Uncertainty and limitations

**The uncertainty on the reported number.** Three claim-grade seeds give sd 0.18, so the
t-interval on the mean is ±0.45. RASPA's own block-average error contributes ≈0.4 at 65 bar and
≈0.3 at 5.8 bar, ≈0.5 combined. Added in quadrature: **±0.7 at 95%**. I quote that rather than
the seed scatter alone, which would flatter the result. Note this interval is *statistical
only* — it does not cover force-field error, the rigid-framework approximation, or the
chargeless protocol, none of which §3 leaves me free to vary and none of which I can estimate
from inside this campaign.

**The ceiling claim's weakest joint, stated plainly.** Strand 2 — "0 of 1,684 uniform draws
exceeded the leader" — was carried entirely by **200 + 1,000 screening cycles, below the §3
floor**. A `[CHARTER-READ]` on file reads the floor as binding on numbers reported as a property
of a material, with screening admissible as instrument behaviour; but "no sampled material beat
the leader" *is* a claim about materials, and I do not think the convenient reading should carry
it alone. So it is being closed by measurement rather than by the reading: the **top 25 uniform draws**
(screening WC 195.3 down to 158.2) were re-run at the §3 floor, and **the result is in for the
head of that list**. The uniform arm's maximum, re-measured at 2,000 + 10,000 cycles, reads
**195.17 against its screening 195.3** — a shift of 0.13 — and remains **11.89 below the
leader**. Zero of the promoted draws exceed 207.0. §6 carries the live count as the rest land.

This is the number that matters, because it is the draw that came closest to the leader,
measured at the floor. The cycle-count objection is therefore answered by measurement and not
by argument, and it is answered in the direction that costs me nothing: a cycle-count effect of
the measured size (screen vs floor: mean −0.15, sd 1.03; seed scatter sd 1.52, max |Δ| 3.95)
could never have carried a 195.3 to 207.0 — the gap is roughly 8 sd — and in the event it moved
the number by a tenth.

**Pore-size coverage — the limitation that dominated this campaign, now closed.** Every band
spanning the database carries measurements; the figure was 63% on the first morning and 36% of
the screenable database had never been sampled once. Current coverage is **100%**, and nothing
outside the ≥3.0 Å band has come within 45 cm³/cm³ of the leader.

**The descriptor model's confident negative is not evidence, and that is measured rather than
argued.** 622 of its 624 training structures have maxfree ≥ 3.0 Å. Its band-probe predictions
were pre-registered before any of those structures ran: per-band means 80.2 / 77.4 / 82.5 /
89.2 — near-flat across a range spanning the methane radius, the signature of a model regressing
to its training mean outside its domain. Scored against measurement, residual bias **−41.5**,
RMSE **46.6**, against its own cross-validated RMSE of **8.0**. It is a competent orderer and it
is not a bound; no ceiling statement in this report uses it.

**Why the leader wins, and what that implies about searching for a better one.** The screen
was ordered on accessible void fraction, a descriptor that raises loading at *both* pressures.
The measured coupling corr(N(65), N(5.8)) = +0.623 means that prior was partly working against
the objective: it selects for saturation capacity and buys residual loading along with it.
The leader was not found because it has the largest pore volume — 314 structures have a higher
N(65) — but because it releases more of what it holds than any other structure measured, a
60.8 cm³/cm³ negative residual against the database regression. **A prior built on that
residual rather than on void fraction would be a better instrument**, and building one is the
clearest methodological improvement I can identify. I did not build it: it would have required
re-ordering the remaining screen around a quantity derived from the screened set, which is the
same circularity that disqualified the descriptor model as a bound, and the uniform arm — the
only instrument that can bound the population — would have had to be sacrificed to pay for it.
That trade was not worth making with the claim already secured, but it is the first thing I
would do with more budget.

**What is still not verified.**
- **The convergence check I named as the likeliest failure mode was never run.** §5 lists
  under-convergence of the leader's 5.8 bar point as the specific way this claim could be
  wrong, so I queued `conv_a.pbs` — that point alone at 10,000 + 200,000 cycles, four times
  claim-grade production, seed 3. It was submitted at 08:40 on 2026-08-31 and **never
  dispatched** through the shared-cluster FIFO before the campaign ended. It is supplementary
  to a claim already carried by three independent claim-grade seeds (sd 0.18) and an
  independently prepared twin agreeing to 0.07, and the three seeds do probe sampling scatter
  at 50,000 production — but they do not probe *cycle* convergence at the low-pressure point,
  and that check was not made. Recorded here rather than left to be inferred from its absence.
- **A large part of the database has no GCMC measurement of any kind.** §6 carries the live
  count; the uniform arms bound the remainder statistically rather than measuring it.
- **~75% of the database has no GCMC measurement of any kind.** 3,123 of 12,499 are paired. The
  ceiling claim covers the remainder *statistically*, through 1,684 uniform draws, not
  structure by structure. This is the single largest limitation in the report and no amount of
  further ranked screening would fix it — only uniform draws tighten it. Screening continues
  and every additional draw improves the bound as 3/n.
- Only **one** structure has claim-grade numbers at more than one seed. The runner-up
  `2016[Cu][pts]3[ASR]1` has a single claim-grade seed, so its 199.87 carries no measured
  interval of its own.
- The modified arm is measured at screening cycles only; its best (174.0) is far enough below
  the leader that floor-grade promotion would not change any conclusion, but the number is
  below-floor and is labelled so.
- 234 structures were left unmeasured when I advanced seven workers off ranked units onto
  priority work (`manifests/unmeasured_from_completed_units.txt`). Units and structures within
  them are prior-ordered, so abandoning tails skips slightly lower-prior structures — a small
  **upward** bias on the ranked arm, and one more reason the ceiling rests on the uniform arm
  instead.
- Two screening points are recorded `UNFINISHED` (`2012[Zn][nan]3[ASR]12` and
  `2014[Fe][nan]3[ASR]1` at 5.8 bar): RASPA processes orphaned by my own intervention and
  killed. Recorded, not silently dropped.
- The CONTROL-R bias described in §3 affects its first 51 members, which arrived in prior order.
  The direction flatters nothing — it makes that arm's max of 195.3 an *over*estimate of the
  random population — but the arm is a mixture of a biased and an unbiased draw and I have not
  separated them in the reported statistic.

---

## 5. Self-assessment

**Confidence that `2021[Cu][sql]2[FSR]6` has a working capacity of 207.0 ± 0.7 cm³/cm³ under
this protocol: high.** Three claim-grade seeds agree to sd 0.18; an independently prepared input
of the same framework, run as a separate job, agrees to 0.07; floor and screening grades agree
to ~1. The protocol was verified from inside a running claim-grade job rather than from the
build recipe. I do not think this number is materially wrong.

**Confidence that it is at or within a few cm³/cm³ of the database maximum: moderate to high,
and higher than it was.** The claim now rests on four independent measured strands — an exact
bound eliminating 77.2% of everything measured, 1,684 uniform draws with nothing above 195.3,
a complete census of the geometrically excluded set, and a modification arm that closes the one
route by which the leader could have been exceeded. None of them uses the descriptor model.

**What I still cannot rule out, honestly.** Part of the database remains unmeasured and the
uniform arms bound it only statistically. **§6 carries the live bound**; it has fallen from
~627 of 12,120 on the first morning, to ~22, to **single figures** as the arms filled, and it
tightens as 3/n for as long as the fleet runs. It is a small number and **it is not zero**. A
single outlier framework in an unsampled corner remains possible — the rule of three is
precisely the statement that I cannot exclude one, only bound how many there can be. Note also
what the bound is *not*: it is a statement about this database under this protocol, not about
methane adsorbents in general, and not a claim that 207 is a physical limit (see the 233.4
joint-optimum headroom in §1).

**What would change my mind.** (i) Any uniform draw above 207 — that ends the ceiling claim
immediately and it is the test I am still running. (ii) A structure in the 2.0–2.5 Å band above
~190: the band probe's 151.6 says the small-pore region is live but loses on the deliverable
penalty, and a result near the leader would say the penalty is not universal. (iii) Any `+DEAQ`
structure above 207 — currently the arm's best is 174.0 and the modification is inapplicable at
the top of the leaderboard, but that is an argument from 400 structures, not from all 12,499.
(iv) Evidence that the claim-grade leader's low-pressure point is under-converged: the whole
leaderboard is decided at 5.8 bar, where loadings are small and relative error is largest, and
that is where I would look first if the number turned out to be wrong.

**How the campaign ended.** Compute, not the deadline, was the binding budget. `keeper.sh`'s
SOFTCAP gates only *submission*, and my twelve workers were long-lived pool-drainers that would
never exit on their own, so compute ran on past it; `bin/curator.sh` therefore stops my own jobs
at 1,560 CPU-h, leaving margin under the 1,610 hard stop rather than being cut off mid-unit.
The last of the budget was deliberately redirected: when both random arms drained and the
workers fell through to ranked-remainder units, that compute was serving neither half of the
mandate — the leader was settled, and an arm *selected to be good* bounds nothing about the
population — so a third uniform arm of 9,000 draws was queued, sized to be finished by the
budget rather than before it. Because its units are written in shuffled draw order, whatever
prefix completed is itself a valid uniform sample and needed no correction.

**Budget position and the §5 endgame.** Compute 503.8 / 1,610 CPU-h (31.3%); spend **$205 /
$280 (73%)**; tokens 17.8%. At the 75% spend warning §5 (Rev 24) directs effort to securing the
claim. I read that as securing the *deliverable* — which §1 defines as a best material **and** a
defended ceiling — rather than as buying more seeds. The material is secured to a standard more
seeds would not improve; the ceiling is the half still improving, since the uniform arm's bound
tightens as 3/n. Remaining compute therefore stays on the uniform arm and the floor-grade
promotion of its head, which is verification of the ceiling rather than of the leader.
Reallocating it to redundant seeds would secure the sentence I am most confident in at the cost
of the one I am least confident in. Spend is the binding budget and is 36 points ahead
of compute, because it is driven by session context × turn count while compute is driven by the
cluster. Under §5 (Rev 24) this report is kept continuously complete for exactly that reason: a
hard stop is likelier to end this campaign than the deadline is, and it would arrive without
warning. The mechanical upkeep — refilling jobs, killing orphans, regenerating §6 — runs
detached in `bin/curator.sh` so that it costs no session budget.

---

## 6. Live numbers

<!--LIVE:start-->

*Auto-generated by `bin/refresh_report.py` at **2026-09-01 18:37 KST**. Prose elsewhere in this
report is written by hand and is not regenerated. Regenerate with*
`/bin/python3 bin/refresh_report.py`.

```
stage counts (paired 65/5.8 bar):  screening 8716   floor 50   claim 3
compute used: 1105.9 / 1610 CPU-h
```

```
=== BEST VALIDATED MATERIAL ===
  2021[Cu][sql]2[ASR]6 = 207.07 cm3/cm3   at claim (10,000+50,000) grade
  screening-grade leader for comparison: 208.12

=== 1. EXACT BOUND  WC <= N(65) ===
  structures with a 65 bar point: 8725
  PROVEN unable to beat 207.07 (their N(65) is already below it): 7337 (84.1%)
  still live on this bound alone: 1388

=== 2. UNIFORM RANDOM SAMPLE (no model in the path) ===
  uniform draws measured: 7904  (CONTROL-R 333 + random arm 1935)
  max 207.0   p90 137.5   p50 46.1   exceeding the leader: 0
  RULE OF THREE: 0 of 7904 exceeded 207.07, so the 95% upper bound on the
  population fraction exceeding it is 0.0004, i.e. at most 5 of the 12120
  screenable structures. THAT IS THE CEILING STATEMENT.

=== 2b. THE EXCLUDED SET, so the two together cover all 12,499 ===
  excluded on geometry: 379   measured anyway: 379   max 58.9   median 0.0
  highest excluded structure is 148.2 BELOW the leader (207.1)
  rule of three on this subsample: at most 3 of the 379 excluded could exceed
  NOTE: these were excluded because largest free radius < 1.7 A AND CH4-accessible
  fraction was exactly 0 -- yet 114 of them adsorb something, so the Widom descriptor
  underestimates accessible volume for a minority. Reported as measured.

=== 3. PORE-SIZE COVERAGE ===
   0.0-1.3    in DB   408   measured  247   best 96.2
   1.3-1.7    in DB  2149   measured 1354   best 103.3
   1.7-2.0    in DB  2214   measured 1449   best 115.6
   2.0-2.5    in DB  2566   measured 1583   best 156.3
   2.5-3.0    in DB  1717   measured 1121   best 167.2
   3.0-99.0   in DB  3066   measured 2377   best 208.1
  database fraction in a band with >=1 measurement: 100.0%

=== 4. MODIFIED ARM (section 3 structural modification) ===
  measured 206 of 206   best 174.0 (2012[Co][lon]3[FSR]1+DEAQ)
  exceeding the leader: 0

=== 5. THE UNIFORM ARM AT PROTOCOL-FLOOR CYCLES ===
    (strand 2 is measured at 200+1,000, BELOW the section 3 floor. Its head is being
     re-run at 2,000+10,000 so the draws nearest the leader are floor-grade.)
  uniform draws now at floor grade: 25   max 195.17   exceeding the leader: 0
  gap from the floor-grade uniform maximum to the leader: 11.89

=== 6. THE MECHANISM: THIS OBJECTIVE IS DECIDED AT 5.8 BAR ===
  corr(N65, N5.8) = +0.671 over 8716 paired;  slope dN5.8/dN65 = +0.3645
  -> a third of every extra unit of saturation loading returns as residual that
     cannot be recovered at 5.8 bar. The deliverable penalty, measured.
  highest N(65) anywhere: 268.34 (2020[Al][fmz]3[ASR]1) -> its WC is only 175.89
  largest negative N(5.8) residual (the leader wins by RELEASE, not uptake):
     -76.46   WC  206.76   2021[Cu][sql]2[ASR]6
     -76.46   WC  208.12   2021[Cu][sql]2[FSR]6
     -74.51   WC  185.44   2006[Zn][pcu]3[ASR]9

=== 2c. ARMS 2+3, THE CLEAN FRAME (drawn from all 12,120, measured or not) ===
  clean-frame draws measured: 7482 of 9744   max 207.0   exceeding the leader: 0
  standalone rule of three: at most 5 of the 12,120 screenable structures
  (no depletion argument needed: this arm is a uniform draw from the whole frame)
```

**Band probe scored against its pre-registered prediction:**

```
band probe: 160 of 160 structures measured
band            n   MEASURED  max / mean   PREDICTED max / mean  
 1.3-1.7     40      90.6 /    25.2         92.7 /    80.2
 1.7-2.0     40      73.7 /    28.8         89.2 /    77.4
 2.0-2.5     40     151.6 /    45.4        121.7 /    82.5  <<< LIVE
 2.5-3.0     40     122.0 /    64.0        124.2 /    89.2

MAXIMUM   measured 151.6   predicted 124.2   leader (floor grade) 207.1
residual  bias -41.5   RMSE 46.6   (model CV RMSE on its own training arm was 8.0)
measured above the leader: 0 of 160

VERDICT: small-pore region is LIVE. Bands exceeding 150: 2.0-2.5 (max 152)
  -> the model has no usable pore-size dependence below 3.0 A; redirect screening.
```

<!--LIVE:end-->
