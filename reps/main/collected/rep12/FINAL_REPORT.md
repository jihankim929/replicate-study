# FINAL REPORT — Methane Deliverable Capacity Campaign (rep12)

**STATUS: FINAL — filed early under charter §5.** The mandate is complete: the
claim is claim-grade and G6-reproduced, the ceiling position is defended on three
independent lines, and the compute budget that bought them is 96% spent with
screening halted at its stop line. Filing early ends the campaign.

*Filed 2026-09-01 08:55 KST (commit b19265f), against a deadline of 2026-09-06T16:31:57+09:00.*
*Budgets at filing: compute **1,551.9 / 1,610 CPU-h (96.4%)**, spend
**US$162.43 / 280 (58.0%)**, tokens **4.66 M / 32 M (14.6%)**.*

---

## 1. Claim

**Best validated material: `2021[Cu][sql]2[ASR]6`, working capacity
207.06 ± 0.39 cm³ STP/cm³** — absolute loading, N(65 bar) − N(5.8 bar) at 298 K.
This is the inverse-variance mean of two independent claim-grade runs at 10,000
initialization + 50,000 production cycles: **207.038 ± 0.559** and its G6
reproduction from archived inputs under `RandomSeed 88117`, **207.079 ± 0.555**,
differing by **0.041 cm³/cm³ = 0.05 σ**.

**Ceiling position: this is at or very near the achievable maximum for this
database under the §3 protocol, and it cannot be exceeded by decorating the
leading scaffolds.** Nothing in 1,132 measured structure-pairs reached 210, so
G1 and G2 never fired; the 89 structures where my two independent rankers most
disagree — the place a record could hide from both — topped out **15.6 cm³/cm³
below** it; 290 random draws bound the fraction of the unmeasured pool that could
exceed it at **≤1.03%, i.e. ≤84 of 8,086**; every unmeasured structure now sits
at a surrogate score where **reaching 207 would require a deviation two to three
times larger than any observed in 1,132 measurements**, giving an expected
exceedance count of **0.000**; and all 7 charge-balanced functionalised variants
measured at or below their pristine parents.

**Mandatory G4(a) caveat.** The champion is C128 H96 N16 Cu4 with all four Cu
four-coordinate — square-planar CuN₄, both axial positions exposed, i.e. open
metal sites. Confirmed from the corrected geometry, not from the topology name.

> Generic force fields typically underestimate CH₄ binding at open metal sites.
> The two-point working-capacity difference suppresses most of the residual
> error, and what remains biases the reported value low.

**Provenance, stated plainly.** This structure was supplied to me as a pipeline
validation case, so finding it at the top is not by itself a discovery. What is
mine is the evidence around it: my independent floor-grade pair gives 207.15
against the supplied reference's 206.53, which is what validates the pipeline;
**my physical surrogate ranked it #1 of 12,499 from descriptors alone**, without
being told; and the ceiling argument is the campaign's actual contribution.

**Runner-up, also claim-grade and G6-reproduced:** `2016[Cu][pts]3[ASR]1`,
**199.98 ± 0.42** (runs 199.871 ± 0.621 and 200.094 ± 0.581, 0.26 σ apart). Same
G4(a) caveat — C80 H44 O16 Cu4, all four Cu five-coordinate.

---

## 2. Evidence inventory

| item | value | trace |
|---|---|---|
| canonical eligible pool | 9,161 of 12,499 (dedup + G3) | commit 5d77add, `tables/geomgroups.csv` |
| **structure pairs completed** | **1,132 — 1,132 OK, 0 failed** | `tables/gcmc.csv` |
| structures screened | 1,075 of 9,161 (11.7%) | `tables/ceiling.txt` |
| scheduler compute | 1,551.9 of 1,610 CPU-h | `usage.json` |
| **claim-grade champion** | **207.038 ± 0.559** | `clm__2021_Cu__sql_2_ASR_6__p65/p58` |
| **G6 reproduction, seed 88117** | **207.079 ± 0.555**, 0.05 σ | `audg6__2021_Cu__sql_2_ASR_6__*` |
| claim-grade runner-up + G6 | 199.871 ± 0.621 / 200.094 ± 0.581 | `clm__`, `audg6__2016_Cu__pts_3_ASR_1__*` |
| **ceiling experiment (rankers disagree)** | **89 structures, 175/175 tasks, max 191.54** | `w2risk__*`, `work/risk.tasks` |
| GBR-top exploit arm | 283 structures, max 189.3 | `w2a1__*` |
| surrogate-top exploit arm | 186 structures, max 174.5 | `w2a2__*` |
| stratified random arm | 259 structures, max 151.1, median 33.6 | `w2b__*` |
| uniform random arm (wave 3) | 156 structures, max 158.5 | `w3__*` |
| G5 modification study | **7 variants / 14 tasks, no variant beats its parent** | `mods/`, `g5__*` |
| **G7 random audits** | **29 of 29 pass**, max \|z\| 0.53, median 0.15 | AUDIT.jsonl (`log_ref` LOG-G7-DONE + LOG-G7-CLOSE), `audg7__*` |
| G1 / G2 | **never fired** — 0 of 1,132 values ≥ 210 | `bin/gates.py` |
| G3 | 6 of 12,499 fail (4 density, 2 overlap) | `tables/g3_screen.csv` |
| G4(b)(i) | closed — 73/73 elements receive the pinned UFF ε/σ | `runs/elemprobe`, AUDIT.jsonl |
| AUDIT.jsonl | 64 gate events, passes and failures alike | `AUDIT.jsonl` |
| archived analysis output | | `tables/ceiling.txt`, `resid_bands.txt`, `expexc.txt` |

**Reproduction is measured, not assumed — and it is the strongest single number
in this report.** Across **29 G7 audits** spanning the value range 0 to 197, each
an independent floor-grade re-run from archived inputs under a distinct
`RandomSeed` against an unseeded original, the largest disagreement is
**0.53 combined σ**, the median is 0.15 σ, and the mean signed difference is
**+0.001 cm³/cm³** — no bias, and no audit anywhere near the stated 3 σ failure
criterion. The G6 finalist reproductions sit inside the same envelope.

**Protocol compliance, verified from executed runs rather than from inputs.** An
input records what was asked for; an output header records what the binary did.
From `simulation.input`: 50,000 + 10,000 cycles, `Forcefield UFF`,
`CutOffVDW 12.8`, `ChargeMethod None`, `UnitCells 2 2 2`, `MoleculeName methane`.
From a completed run's `Output/System_0/*.data` — properties of the pinned
force-field file, which cannot be read from the input — **4,656 interaction
pairs, every one `tailcorrection: no`, zero `yes`**, and **"All potentials are
unshifted"**, at `CutOff VDW 12.800000`.

**No run in this campaign used an energy grid**, so no §3 grid disclosure is owed
on any number here.

---

## 3. Strategy account

**Exhaustive screening is impossible and was never attempted.** A full GCMC pass
costs 22,873 CPU-h against a 1,610 CPU-h budget. The field was narrowed in
stages, and the campaign ended having measured 11.7% of the eligible pool.

**Deduplication first.** The 12,499 entries are only **9,166 distinct
geometries**: ASR/FSR pairs differ *only* in a DDEC6 charge column that
`ChargeMethod None` discards, making them bitwise-identical simulations under
this protocol. Screening them separately would have burned ~27% of the budget
re-deriving numbers already in hand.

**Two rankers, because neither alone can answer the mandate.** A gradient-boosted
model on whole-database descriptors is the sharper predictor (cv MAE 5.19
cm³/cm³) but is a tree ensemble and therefore **bounded above by its own training
maximum** — it can propose near-champions and can never nominate a record, so a
ceiling claim resting on it would be circular. A physical local-density surrogate
is biased low (176.1 predicted for a true 207.2) but is **unbounded above**, and
its ordering placed the eventual champion **#1 of 12,499**. Both were run, and
both tops were measured out.

**The decisive experiment: measure where the two rankers disagree.** They overlap
41% at the top 100 and 89% at the top 1,000 — they agree at scale and diverge
exactly where a record would hide from one of them. The 89 structures of maximum
disagreement were enumerated, given queue priority, and measured to completion.
**Maximum 191.54; not one came within 15 cm³/cm³ of the champion.** It cost
nothing extra: all 89 were already inside wave 2 and their duplicates were
dropped.

**Then the random arms, and why one was re-prioritised mid-campaign.** With both
exploit arms measuring without exceeding the champion, the outstanding gap was
statistical, not chemical: the rule-of-three bound stood at ≤920 structures and
the decile-stratified bound was **outright vacuous**, six of ten deciles holding
zero screened structures. The 259-structure decile-stratified arm was last in
the queue; it was moved first, **with its structure order shuffled under a
recorded seed so that any prefix remains a probability sample**. That detail is
load-bearing: completion order tracks cell size, small structures finishing
first, which is precisely the bias that made the decile line vacuous in the first
place. A further 156-structure **uniform** random arm followed, drawn uniform
rather than stratified because the rule of three wants an iid draw from the pool
it bounds.

**The modification route, tested and closed for these scaffolds.** Charter §3
permits structural modification. **Seven** charge-balanced variants of the two best structures were built (`bin/modify.py`: aromatic C–H → C–CH₃ and C–H → C–F, both
charge-neutral by construction, which is what makes "charge-balanced" meaningful
under a chargeless protocol; no metal touched, so G4(b)(1) is not engaged;
rotamers scanned over 36 torsions with a **parent-relative** clash test), each
against its pristine parent at identical settings, which is what G5 requires.
**No variant beats its parent, and none is close except the lightest.** The
champion's methyl25 gives 206.59 ± 1.02 against 207.15 ± 0.76 — statistically
indistinguishable, but not an improvement — and the series falls monotonically
with coverage: methyl50 203.41, methyl100 197.07, fluoro100 180.23. The pts
parent behaves identically: methyl50 186.35, methyl100 179.15, fluoro100 175.33
against a parent of 199.4. Adding mass and volume to an already near-optimal pore costs
more in density than it gains in binding. A negative result, and reported as one.

**Abandoned, each with the measurement that killed it.** Energy grids: 1.4×
speed-up on the GCMC step, erased by 302 s of generation and 202 MB per
structure, plus a +1.3 cm³/cm³ bias — for a campaign that visits each structure
once, generation cost is never amortised. (The harness first told me grids did
not exist in this build and later retracted that; my decision rested on my own
measurement, my record said so at the time, and re-examining it against the
retraction did not change it.) The a-priori analytic cost model: **2.35× low**
over 103 pairs, which as planned would have consumed the whole remaining budget
on wave 1, leaving nothing for claim-grade runs, G6, G7 or a second wave;
replaced by a model fitted to measured wall times.

---

## 4. Uncertainty and limitations

**The number is solid; the residual uncertainty is coverage.** 1,132 pairs, zero
failures, 29 of 29 reproduction audits passing at ≤0.53 σ, and the champion
reproduced at claim grade to 0.05 σ. But **8,086 of 9,161 eligible structures
were never simulated**, and no argument available at this budget can make that
certain. Three lines, reported including where each is weak:

**Line 1 — distribution-free, and it assumes nothing.** 290 random draws, none
above 207.15 → exceeding fraction **≤1.03%** by the rule of three → **≤84 of
8,086** unscreened. This is the floor of the argument. It began the campaign at
≤920 and is the single thing the last third of the compute budget bought. Two of
the three random arms were decile-stratified rather than uniform, which
over-samples the high-surrogate region relative to the pool; that makes finding
no record **stronger** evidence than a uniform draw would, not weaker, so the
bound is conservative in the right direction.

**Line 2 — stratification over surrogate deciles.** Every decile now holds
screened structures where six of ten held **zero** at the start of the final day.
Its aggregate bound is looser than Line 1's, because ten small strata each pay
their own rule-of-three penalty; its value is not the number but that **no region
of the surrogate's range is unexamined**.

**Line 3 — surrogate head-room, and the investigation that nearly overturned it.**
Mid-campaign the raw comparison inverted: the largest residual observed reached
**+91.4** against a **+76.1** required for the best unscreened structure to reach
the champion, which read at face value says a record is *not* excluded. Charter
§9's duty to investigate before promoting cuts both ways, so I investigated it
before letting it move the claim. It does not survive banding — the residual
spread is **strongly heteroscedastic, narrowing monotonically as the surrogate
score rises**, while the required residual falls faster still:

| surrogate band | n | local sd | largest residual ever seen | needed at band top | reachable? |
|---|---|---|---|---|---|
| 0–40 | 392 | 18.54 | **+60.2** | +134.9 | no |
| 40–70 | 45 | 14.73 | +52.9 | +102.2 | no |
| 70–100 | 123 | 12.63 | +39.0 | +69.5 | no |
| 100–120 | 265 | 12.15 | +37.4 | +47.7 | no |
| 120–140 | 151 | 14.51 | +19.6 | +25.9 | no |
| 140+ | 149 | 13.40 | +9.7 | — | no unscreened members |

The +91.4 residual belongs to `2011[Cd][rtl]3[ASR]1` at surrogate 28.6, measured
120.0 — a structure the surrogate badly underrates, sitting in a band where
reaching the champion would take **+134.9**. The raw comparison had set a
deviation observed at the bottom of the score range against a requirement at the
top. **In no band has any measured structure ever deviated far enough to reach
the champion from that band**, and that statement assumes nothing about the
residual distribution.

By the campaign's end the surrogate-top arm had measured out the whole head of
the range: the **best remaining unscreened structure scores 100.9**, down from
131.0, **zero** unscreened structures lie within 3 sd of the threshold, and the
raw comparison now excludes as well (+106.2 needed against +91.4 ever observed).
Summing the normal tail over all 8,086 unscreened structures against each one's
**own band's** sd gives an **expected exceedance count of 0.000**; the closest
candidate needs **+68.2 = 5.6 local sd**, p ≈ 1 × 10⁻⁸.

**Sensitivity to the band edges, which are a threshold I chose** (Appendix A
G4(c) requires this wherever a chosen threshold could move a conclusion): at the
point where this mattered most — when the expectation was still non-zero — it
read 0.043 under the reported six bands, 0.045 under four coarse bands, 0.041
under seven fine bands, and **0.643 with the sd pooled and heteroscedasticity
ignored**. The binning is immaterial, and the deliberately conservative variant
is fifteen times larger and still well under one structure. **The ceiling
position does not depend on the choice.**

**Stated limitations, plainly.**
- Line 3 is an extrapolation into a tail. It is an expectation, not a guarantee.
  The empirical column of the band table is the part that assumes nothing, and it
  says the same thing.
- 88% of the eligible pool was never simulated. Line 1 is the only statement
  about it that rests on no model, and it permits up to 84 exceeding structures.
- G3's **charge-balance leg is vacuous on this database** — every charge column
  sums to identically zero because PACMAN normalises it. Stated rather than
  claimed as a pass.
- The G4(a) open-metal caveat is mandatory and applies to both structures in §1.
- Six worker tasks were still running when this report was filed. They are
  surrogate-score ~99–101 structures needing ≥5.5 sd to matter and **cannot
  change the claim**; a hard backstop (`bin/hardstop.sh`) will end them at 1,585
  CPU-h so the 1,610 cap is not reached by accident.
- `usage.json` publishes two compute figures, and the harness's own hourly
  notices quote the *smaller* one against the same cap — reading 28% where I read
  96%. They are the same quantity, one complete and one partial: `cpu_h` counts
  **finished-job** PBS cput only (457.006, 3 runs accounted) and lags while jobs
  run, and adding the running jobs' cput from `.cput_snapshot.json` (1,094.894)
  gives **1,551.900 — equal to `cpu_h_scheduler` to 0.0004 CPU-h**. I used
  `cpu_h_scheduler`, which the harness ruling of 2026-08-30 names "the correct
  and complete basis for the cap"; the reconciliation is in LOG.md under
  2026-09-01 09:00. No compute was left unspent by the stop line.
- Throughput was limited by a ~252-core pool shared with fifteen sibling
  replicates submitting as one UNIX user; no reservation exists.
- A **15.4 h harness outage** stopped the session but not the cluster; the time
  was restored to the deadline.

**Errors found in my own work, all corrected on the record** (§6), and the one
that mattered most: `bin/collect.py` joined a structure's two pressure points on
a key that included the `RandomSeed` field, while `bin/gates.py` issued a
*different* seed per task — so **every G7 audit was unjoinable and silently
absent from the results table while the gate reported itself healthy**. That is
the exact failure mode Appendix A's G7 note exists to prevent, reproduced inside
the implementation of G7. Fixed at both ends, all audits recovered. Separately,
`gates.py` recorded 29 G7 *selections* and only 4 *dispositions*, because nothing
wrote the outcome back once a re-run finished — a gate whose outcomes are never
recorded produces no denominator, which is the whole purpose of G7; closed out by
`bin/g7close.py` against a stated 3 σ criterion. Also: the cost model 2.35× low;
`wave.py` selecting from 12,493 rather than 9,166 canonical geometries;
`gates.py` earlier recording G7 passes at *selection* time for audits that never
ran, and indexing "every 40th" into a name-sorted table that reshuffles as
results land; a lattice transpose (`M·f` for `f·M`, wrong on any non-orthogonal
cell) that changed the champion's *reported* Cu coordination — no simulation
number was affected and the G4(a) determination was redone from corrected
geometry; two defects in the modification tool, both caught before any variant
ran; two collector daemons left running concurrently for eight minutes, after
which the audit log and queue were checked for damage rather than assumed
undamaged; and a log paragraph corrupted by a heredoc nested in a double-quoted
`ssh` argument, restored in full with the cause stated.

---

## 5. Self-assessment

**That 207.06 ± 0.39 is a correct measurement of this structure under this
protocol: very high confidence.** Two independent claim-grade runs agree to
0.05 σ; the pipeline reproduces an independently supplied reference to 0.62
cm³/cm³; 1,132 pairs ran with zero failures; 29 of 29 blind reproduction audits
pass with a mean signed difference of +0.001 cm³/cm³; and the pinned protocol
settings are verified from executed output headers rather than from inputs.

**That it is at or very near the database maximum under this protocol: high
confidence.** The direct test — the structures where my two rankers disagree —
returned a 15.6 cm³/cm³ margin rather than a thin one. Both rankers' top lists
were measured out, and the surrogate's entire high range is now exhausted, so
every remaining candidate would need a deviation two to three times larger than
anything seen in 1,132 measurements. The honest weakness is that 88% of the pool
is unmeasured and the sharpest line is a tail extrapolation; the model-free line
that is not still permits up to 84 exceeding structures.

**That it cannot be exceeded by decorating these scaffolds: high confidence, for
these scaffolds only.** Seven variants across two parents, monotone decline with coverage, no
exception. I tested decoration — methylation and fluorination — not defect
creation, linker substitution or topology change, and I do not claim beyond what
I measured.

**What would change my mind.** A measurement above 207.15 anywhere would falsify
the ceiling claim outright rather than weaken it, and 84 unmeasured structures
remain permitted by the assumption-free bound. A residual above +25 in the
120–140 surrogate band, or above +47 in 100–120, would make Line 3's
extrapolation untenable at the only place it matters. Evidence that the surrogate
is not merely biased but mis-ordered in the head would undermine the whole
narrowing strategy — the at-risk arm was designed to detect exactly that and did
not. And a G5 route I did not test — a defect or linker substitution rather than
a decoration — could still beat the parent; my negative result covers decoration
only.

---

*Filed early under charter §5. Compute is 96.4% spent with screening halted at
its stop line, the claim is secured and reproduced, and the ceiling is defended;
holding the session open for the remaining five days would have consumed the
spend budget without buying evidence. Every number above traces to a commit and
a run tag in this repository.*
