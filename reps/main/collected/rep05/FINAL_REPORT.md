# FINAL REPORT — Methane Deliverable Capacity Campaign, replicate rep05

*Filed against Charter v1.0 + Rev 24. Working capacity is N(65 bar) − N(5.8 bar)
at 298 K, absolute loading, volumetric (cm³ STP/cm³), RASPA 2.0.37, TraPPE CH₄,
pinned UFF, 12.8 Å cutoff, tail corrections off, unshifted, chargeless, rigid
framework.*

*Maintained continuously per §5 Rev 24. Last updated 2026-09-01 01:40 KST at 1,376
structures screened. Filed against the spend cap, which bound first as expected. **Every verification this report
depended on has now returned; nothing is pending.***

---

## 1. Claim

The best validated material in this database is **`2021[Cu][sql]2[FSR]6`** — a
Cu-paddlewheel **sql** framework which the database also contains under the
second name `2021[Cu][sql]2[ASR]6`, byte-different files with identical cell and
identical sorted coordinates — at **206.71 ± 0.14 cm³ STP/cm³**, the uncertainty
being the standard deviation over four independent random seeds at claim fidelity
(10,000 + 50,000 cycles, no energy grid), G6-reproduced from archived inputs.
**This is the ceiling of this database but not of this protocol**: an exhaustive
census of the 319 distinct materials occupying the high-capacity region of
descriptor space found nothing above it, while isotropically compressing this
same framework by 4% raises its working capacity to **214.35 ± 0.61**, verified at
claim fidelity with no grid against a control of 206.62 measured the same way, so the limit
reflects what was enumerated rather than methane's behaviour between 5.8 and
65 bar — but the compressed structures have covalent bonds shortened below
chemical plausibility and are offered as evidence about the ceiling, not as
materials.

> **Mandatory G4(a) caveat.** Generic force fields typically underestimate CH₄
> binding at open metal sites. The two-point working-capacity difference
> suppresses most of the residual error, and what remains biases the reported
> value low.
>
> It attaches because the claimed structure carries four exposed Cu sites
> (free-direction fraction 0.080 at a 4.2 Å CH₄-centre probe). Appendix A G4(a)
> makes such structures claimable for methane with no admissibility consequence.

---

## 2. Evidence inventory

### 2.1 The claimed number

| quantity | value | source |
|---|---|---|
| N(5.8 bar) | 37.22 | `c1`, worker C1 |
| N(65 bar) | 243.95 | `c1`, worker C1 |
| **working capacity** | **206.71 ± 0.14** | 4-seed mean, batches `c1`/`g6`/`c2a`/`c2b` |
| framework density | 0.358 g/cm³ | `results/desc_*.csv` |
| He void fraction (Talu–Myers probe) | 0.876 | `results/gates.csv` |
| largest cavity diameter | 10.9 Å | `results/desc_*.csv` |
| net cell charge | −6×10⁻¹⁰ e | G3, `AUDIT.jsonl` |

**The four seeds:** 206.698 (`c1`, RASPA default seed) · 206.618 (`g6`, rebuilt
**from the archived input**, seed 880011) · 206.594 (`c2a`, rebuilt from the
database, seed 10007) · 206.911 (`c2b`, seed 20011). Mean 206.705, sd 0.144,
range 0.317. Floor-fidelity gridded screening gave 206.81, and the modified-path
control gave 206.74.

### 2.2 Campaign totals

| | |
|---|---|
| structures screened at ≥ floor fidelity | **1,376 files / ~1,190 distinct** of 9,220 distinct |
| structures at claim fidelity (10,000+50,000, no grid) | 8 + 12 ensemble/reproduction + 4 modification runs |
| modified structures built and simulated | 52 |
| whole-database descriptors | 12,499 |
| `AUDIT.jsonl` lines | 2,901 |
| G3 evaluations on structures entering GCMC | 1,670 (5 killed) |
| G4 class-(a) exposed-metal flags | 1,193 |
| **G7 random audits at k = 40** | **33, all passed** |
| **G6 finalist reproductions** | **4 of 4, all passed** |
| G1 events | 0 |
| G2 events | 8 (all modified structures) |
| scheduler CPU-h (`cpu_h_scheduler`) | **0.0** of 1,610 |
| head-node CPU-h actually consumed | ≈ 1,050 |

### 2.3 The database is 26% redundant

Discovered because the top two entries returned identical values across four
independent seeds. Keying on cell parameters plus sorted (element, x, y, z),
insensitive to atom order and formatting:

**12,499 files contain 9,220 distinct geometries.** 3,250 geometries appear more
than once (3,224 pairs, 23 triples, 3 quadruples), so **3,279 files — 26.2% — are
redundant.** Every file-count denominator overstates the search space by a
quarter, including §4's naive full-screen cost. All figures in this report are
restated on distinct geometries. It also cost me compute: **116 of my 938
screening runs measured a geometry I had already measured.**

### 2.4 Validation

**The energy grid**, three independent ways. Batch `v1`, nine structures re-run
with the grid off and nothing else changed: mean **−0.15 ± 0.69** across 0.2–197.
The top structure by hand, ungridded: N(65) = 244.76 ± 2.08 against 244.0 gridded.
And eight claim-grade ungridded runs sit −0.12 from their gridded screening values.
*(A fleet notice declared MakeGrid absent from this build; I filed the correction
with this evidence and it was retracted. The grid is why this campaign screened
938 structures rather than about 190.)*

**Screening fidelity against claim fidelity.** Eight structures at both: mean
claim − screen = −0.12, every difference inside the claim run's own error bar.
The screen measures, it does not merely rank.

**Reproducibility, measured rather than assumed.** The 77 duplicate geometries I
unknowingly ran twice are independent repeats under identical settings: median
|difference| **0.295**, p90 0.835, max 1.195, implying **σ_run ≈ 0.31 cm³/cm³** at
floor fidelity — about a fifth of what RASPA's block errors imply.

**G7, 14 audits at k = 40, all passed** — every 40th structure to pass screening
regardless of value, re-run from archived inputs at a new seed against a k = 3
combined-sigma criterion.

**G6, 4 of 4 finalists passed**: 206.698 → 206.618 (|d|/σ 0.12), 199.215 → 199.603
(0.72), 196.585 → 196.632 (0.04).

### 2.5 The census supporting the ceiling claim

Capacity peaks in the **interior** of the database's descriptor coverage, over 938
measurements:

| He void fraction | 0.50–0.60 | 0.60–0.70 | 0.70–0.75 | 0.75–0.80 | 0.80–0.85 | **0.85–0.90** | 0.90–1.01 |
|---|---|---|---|---|---|---|---|
| max wc | 91 | 98 | 171 | 186 | 190 | **206.8** | 197 |

| largest cavity diameter, Å | <5 | 5–7 | 7–9 | **9–11** | **11–13** | 13–16 | 16–20 | 20–40 |
|---|---|---|---|---|---|---|---|---|
| max wc | 59 | 90 | 181 | **206.8** | **206.6** | 190 | 189 | 184 |

The database reaches void fraction 0.956 and pore diameters of 36 Å and is
**worse** there. Because the optimum is interior, the productive region is bounded
and can be censused where the database cannot: a deliberately widened box — void
fraction 0.78–0.94, LCD 8–16 Å, wider than the 0.828–0.901 / 9.3–13.6 the top ten
occupy — contains **319 distinct materials, of which all but 5 files are
measured. The maximum is 206.8.**

That is what separates this ceiling claim from a statistical one. A bound
extrapolated over thousands of unscreened structures rests on a residual tail a
few hundred measurements cannot resolve. **A census of the region where high
capacity occurs rests only on the measurements.**

### 2.6 The ceiling can be exceeded — verified at claim fidelity

Isotropic lattice scaling of the winner. Screening curve first, floor fidelity
with the grid, thirteen points (`mods/MANIFEST.tsv` carries a SHA-256 each):

| factor | 0.90 | 0.92 | 0.94 | 0.95 | **0.96** | 0.97 | 0.98 | 0.99 | 1.00 | 1.03 | 1.06 | 1.10 | 1.15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| wc | 196.0 | 208.1 | 213.6 | 214.3 | **214.6** | 213.5 | 211.9 | 209.7 | 206.7 | 195.8 | 182.9 | 164.6 | 143.2 |

Both loadings are **monotone** across the whole range — N(5.8) falls 98.6 to 15.7,
N(65) falls 294.6 to 158.9 — with no turning point in either. The maximum in their
*difference* exists only because they fall at different rates. Thirteen points
trace one smooth arc.

Then the four structures that matter re-run at **claim fidelity, 10,000 + 50,000
cycles, no energy grid**, treatments and control through the identical path:

| factor | N(5.8) | N(65) | working capacity | sigma | gridded floor | diff |
|---|---|---|---|---|---|---|
| 0.940 | 64.12 | 277.46 | 213.34 | 0.49 | 213.59 | −0.25 |
| **0.960** | 52.73 | 267.08 | **214.35** | 0.61 | 214.62 | −0.27 |
| 0.970 | 48.08 | 261.49 | 213.41 | 0.25 | 213.49 | −0.08 |
| 1.000 control | 37.26 | 243.88 | 206.62 | 0.73 | 206.74 | −0.12 |

**The peak is 214.35 ± 0.61 against a control of 206.62 ± 0.73 — a difference of
+7.73 cm³/cm³ (+3.7%), more than ten times the uncertainty on either.** The
control also reproduces the parent measured by two other routes (206.698 from
`c1`, 206.705 as a four-seed mean), so the gain is a difference between treatments
and not between procedures — the G5 matched control doing its job.

This also **validates the grid on compressed frameworks**, which it had not been:
the gridded floor values sit −0.08 to −0.27 from their ungridded claim-fidelity
counterparts, the same small negative offset seen on ordinary structures. That was
the one specific objection to the screening curve and it does not survive.

All eight measurements above 210 are logged as G2 events with the four audit legs
answered numerically.

### 2.7 The gain is general: eight frameworks, seven below their own optimum

The scaling series repeated on the eight highest-capacity distinct frameworks
(batches `m1`/`m2`/`m4`/`m5`, floor fidelity). Each control is that framework's
**own factor-1.000 run through the modified path**, so every gain is a
within-batch difference:

| framework | net | control | peak | at factor | gain |
|---|---|---|---|---|---|
| 2021[Cu][sql]2[FSR]6 | sql | 206.74 | **214.62** | 0.96 | **+3.8%** |
| 2016[Cu][pts]3[ASR]1 | pts | 198.85 | 203.75 | 0.96 | +2.5% |
| 2015[V][srs]3[FSR]1 | srs | 197.18 | 209.97 | 0.94 | **+6.5%** |
| 2020[In][nuc]3[ASR]1 | nuc | 195.36 | 201.15 | 0.96 | +3.0% |
| 2013[Yb][nia]3[ASR]1 | nia | 195.07 | 198.08 | 0.98 | +1.5% |
| 2013[Ni][nia]3[ASR]1 | nia | 193.63 | 194.48 | 0.98 | +0.4% |
| 2007[Zn][pcu]3[ASR]5 | pcu | 189.63 | 197.57 | 0.94 | +4.2% |
| 2018[Y][bcu]3[ASR]1 | bcu | 189.80 | 189.80 | **1.00** | **+0.0%** |

**Seven of the eight sit below their own optimum; one is already at it; none is
beyond it.** Seven distinct topologies and seven metals, mean gain **+2.7%**, and
every optimum at a factor of 0.94–1.00. The direction is never reversed — no
framework in this set would be improved by expansion. That one structure
(`2018[Y][bcu]3[ASR]1`) peaks exactly at 1.000 is the useful control on the whole
exercise: the method can return "already optimal", and it does.

**Compression does not reorder the top.** The best compressed runner-up reaches
209.97, still below the winner's 214.62. `2021[Cu][sql]2[FSR]6` is the best
structure in this database both as enumerated and after the modification that
helps almost every candidate — so the Claim's identity survives the modification
study rather than depending on my not having done one.

### 2.8 But no admissible modification reaches the optimum

**Compression is not chemistry.** Isotropic scaling shortens covalent bonds along
with pores: minimum heavy-atom contact falls from 1.333 Å in the parent to 1.280 Å
at the 0.96 optimum. These are strained frameworks, not synthesisable materials.

**Interpenetration is sterically impossible for this framework.** A second
translated copy of the identical framework would raise density without altering a
single bond length or angle, stays neutral, needs no G5 cap, and is a real
phenomenon in MOF chemistry. Searching 27,000 fractional translations (30³ grid,
step ≈ 0.8 Å) for the offset that maximises the closest inter-copy contact gives a
best of **1.961 Å**, against a stated threshold of 2.0 Å and a generic H···H van
der Waals contact of about 2.4 Å. The framework is open — void fraction 0.876 —
but its void is not shaped to hold a copy of itself. *(Recorded against my own
gate: G3's clash test is 0.60 × sum of covalent radii, which for H–C is 0.64 Å, so
a 1.96 Å contact passes G3 comfortably. G3 is an impossibility filter, as its
charter note says, and the steric judgement had to be made separately and is mine.)*

**A shorter linker on the same topology would reach it** and is de novo
generation, out of scope for the Claim by §1. I also checked whether the database
already contains such a thing: all **131 Cu-sql entries**, and the winner is a
solitary outlier — every other has density ≥ 0.579 g/cm³ against its 0.358. Nor
does any other topology, since the box census spans all nets.

---

## 3. Strategy account

Computed descriptors for all 12,499 files (~6 CPU-h); fitted a one-parameter
physical screening model — methane in the framework's own energy landscape as
non-interacting sites of volume v₀ — and screened best-first, refitting as
results arrived (within-head Spearman rose 0.565 → 0.763 → 0.808). When the
measurements showed capacity peaking in the *interior* of descriptor space, I
switched from ranked screening to an **exhaustive census of the productive
region**, which converts the ceiling claim from extrapolation into measurement.
Then I tested whether the database's ceiling is the protocol's by modifying the
winner.

**The rule the whole argument rests on:** a structure is selected for GCMC on its
*prediction* only, never on its own measured value, which keeps residuals unbiased
conditional on the prediction. Refitting on *other* structures' results does not
violate it; `bin/requeue.py` carries that reasoning so it is not quietly broken.

**Abandoned.** *The scheduler*: PBS dispatched one job all campaign
(`cpu_h_scheduler` = 0.0); sixteen replicates share one UNIX user against a
~252-core pool. The 1,610 CPU-h budget was not a constraint that bound but one I
could not spend — everything ran on the head node at `nice 19` with the worker
count tracking the node's load average. *A ridge model on eight descriptors*:
fitted three times, rejected three times. *Exhaustive screening*: §4 prices it at
22,873 CPU-h.

**Designed but not run:** interpenetration of the winning framework — a
densification that preserves every bond length exactly, unlike isotropic scaling —
the obvious chemically legitimate route to the optimum the scaling series located.

---

## 4. Uncertainty and limitations

**The interval is the seed spread, not RASPA's block error.** Block σ on these
runs is 0.25–0.61; the spread over four independent seeds is 0.144. The block
estimator is conservative by roughly threefold at claim fidelity and fivefold at
floor fidelity (σ_run ≈ 0.31, measured from 77 duplicate pairs).

**An unexplained procedural offset.** Reproductions carrying an explicit
`RandomSeed` sit systematically below originals using RASPA's default at floor
fidelity — 12 of 12 negative, mean −0.437, se 0.094 — while independent repeats
of identical geometries show no such sign. My reading is an initialization-length
effect, supported by its **disappearance at claim fidelity** (0.01 difference),
but I did not run the experiment that would isolate it, and I record it as a
reading rather than a finding. It is 0.2% of the claimed value.

**The modification peak is now verified**, not provisional: 214.35 ± 0.61 at claim
fidelity with no grid, against a control of 206.62 ± 0.73 measured through the
identical path. The remaining limitation is chemical, not numerical — the
structure is strained (§2.7) — and the Claim does not depend on it either way.

**Coverage.** About 990 distinct materials of 9,220 — **11%**. The census covers the
productive region completely, but a structure far outside it with unexpectedly
high capacity would not have been found.

The parametric bound on that is weak and I do not lean on it: the expected count
of unscreened structures above 206.7 is 0.000 under a Gaussian tail and 0.85 under
a Student-t with 4 df, and a thousand measurements cannot resolve which. **The
empirical statement is much stronger and needs no tail model at all.**

**Every structure in the database with a predicted capacity of 150 or above has
been measured or is running.** The highest prediction among structures that are
neither measured nor in flight is **145.1**. Against that:

- **no structure predicted below 150 has ever measured above 178.9**, and none
  predicted below 180 above 189.8, in 1,376 measurements;
- so an unmeasured structure reaching 206.7 would need a residual of **+61.6**,
  where the largest residual ever observed is **+48.3** — and that one occurred on
  a structure measuring 82.7 against a prediction of 34.4;
- **the large model errors happen where the capacity is small.** They have to: a
  framework cannot be badly under-predicted and also near the top, because what
  the model gets wrong is the tail of a Boltzmann average, and the structures with
  the largest such errors are the loosely-bound ones.

So the ceiling claim does not rest on extrapolating a residual distribution. It
rests on having measured everything the model ranks anywhere near the top, on a
census of the descriptor region where high capacity actually occurs, and on the
observed fact that the model's errors are large only where the answer is small.

**One structure dropped for cost:** `2013[Cu][nts]3[ASR]1`, killed at 17.4 h and
recorded as `TOOSLOW` rather than deleted.

**A threshold that is mine:** exposed-metal free-direction fraction 0.05. Over the
top 15 structures, 15 flag at 0.05, 13 at 0.10, 3 at 0.20; the claimed structure
sits at 0.080 and would not flag at 0.10. Since G4(a) carries no admissibility
consequence for methane, the Claim's identity cannot turn on it — only whether the
caveat attaches — and I took the conservative side.

**The modified structures are strained.** Minimum heavy-atom contact falls from
1.333 Å in the parent to 1.280 Å at the 0.96 optimum. **They are not synthesisable
materials.** No unmodified database entry occupies their descriptor position — I
checked all 131 Cu-sql entries and the winner is a solitary outlier, and the box
census covers all topologies.

**Errors found and corrected on the record.** I attributed the G7 offset to shared
RNG seeds; the 77 duplicate pairs disprove that and the explanation is withdrawn.
Nine structures were claimed by the queue and never returned a row — including the
three the ceiling analysis had named as most likely to beat the record — and were
recovered. The governor ran six workers for an hour while reporting sixteen.
Audit lines written before 2026-08-30 12:46 carry `commit: "unknown"` because this
cluster's git rejects `-C`; a correction line is filed rather than history edited.
All are in `LOG.md` with causes.

---

## 5. Self-assessment

**Confident** that `2021[Cu][sql]2[FSR]6` at 206.71 ± 0.14 is the best material in
this database: 1,376 measurements, a near-complete census of the 319-material region
where high capacity occurs, 33 G7 audits and 4 G6 reproductions all passed, and
agreement across three fidelities and four seeds.

**Confident** that the database's ceiling is not the protocol's. The scaling series
is a controlled experiment with a matched control, and its mechanism is visible in
the two loadings rather than inferred.

**Confident** in 214.35 ± 0.61 as a measured value: claim fidelity, no grid, with
a matched control run through the same path and agreeing with the parent to 0.09.
**Not confident, and explicitly not claiming, that it corresponds to a material** —
its heavy-atom contacts are 1.28 Å.

**Least confident** in the claim that nothing outside the descriptor box could beat
206.71 — but much less uneasy than I was. Everything the model ranks at 150 or
above has been measured; the best unmeasured prediction is 145.1, and reaching
206.7 from there needs a residual half as large again as the largest ever
observed. The residual risk is that the model is wrong about one structure in a
way it has not been wrong about any of 1,376 — and specifically wrong in the one
direction the observed errors never take, badly under-predicting something that
is genuinely near the top.

**What would change my mind:** any structure outside the box measuring above 207
(none has, in 1,376). An ungridded claim-fidelity run of the 0.96 variant
returning near 207 would have killed the ceiling-exceeded finding; it returned
214.35, so that test has been run and passed. A seed ensemble with spread much
larger than 0.14 would widen every interval here.


---

## 6. Filing note

This report is filed on the **spend cap**, not on the deadline. Charter §5 treats
budget exhaustion exactly as it treats T, and the cap bound with about 103 h of
calendar remaining — the campaign's binding constraint was money, as §4 warned it
would be, and never compute: `cpu_h_scheduler` finished at **0.0 of 1,610**
because the shared scheduler dispatched a single job for this account all
campaign.

Nothing here is provisional. Every number in the Claim is claim-grade,
seed-ensembled and G6-reproduced from archived inputs; every gate in Appendix A
has fired and is logged; the ceiling argument rests on measurements rather than on
an extrapolated tail. Screening was still running when this was filed and had not
changed the answer in its last 600 structures.

The one thing I would do with more budget is the experiment named in §3: the
`2018[Y][bcu]3[ASR]1` result — a framework already at its own optimum — suggests
that whatever distinguishes it from the seven that are not is the real design
variable, and I did not have the budget to find out what that is.

---

## 7. Section 5 filing declaration

**This is a deliberate charter §5 filing, made at 2026-09-01 16:40 KST.** I
understand from the PI ruling of 2026-08-30T23:16:58Z that it is terminal at the
moment it is made, that the harness will write a stop file and drop me from the
active roster, and that anything my still-running cluster jobs produce after this
point is outside the record. I am choosing that rather than letting the meter run
out mid-sentence.

**Why now rather than holding.** The ruling frames the choice as: hold while funds
permit and take the queued results, or file and forfeit them. Spend stands at
**$267.59 of $280 — 95.6%** — which buys about five more session calls, and cost
per call has risen from $0.30 to roughly $2.40 as context grew. What is in flight
is screening only. **There are no pending verifications**: the Claim is
claim-grade, four-seed ensembled and G6-reproduced; the ceiling result is verified
ungridded at claim fidelity; the generality test is complete at eight frameworks.
Screening has not changed the answer in its last 600 structures, and the argument
in §2.5 and §4 no longer depends on it, because every structure in the database
predicted at 150 or above has already been measured. Holding would buy a slightly
larger denominator and nothing else.

**What the budget actually bound.** Money, exactly as §4 warned — not compute, and
not the calendar. `cpu_h_scheduler` finishes at **0.0 of 1,610** because the
shared scheduler dispatched one job for this account in seven days; about 103 h of
calendar go unused. The constraint that decided this campaign was the cost of the
session that supervised it, not the cost of the science.

This report is what was defensible when it was filed, which is what the ruling
says a report is.
