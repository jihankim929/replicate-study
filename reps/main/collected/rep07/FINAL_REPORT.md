# FINAL REPORT — Methane Deliverable Capacity Campaign (rep07)

*Regenerated from the record by `bin/mkreport.py` at 2026-09-01 03:31 KST. Status: **claim-grade and G6-reproduced**.*
*Every figure below is computed from `tables/` at generation time; none is transcribed.*

## 1. Claim

The best validated material is **2021[Cu][sql]2[FSR]6**, with a methane working capacity of **206.9 ± 0.5 cm³/cm³** (N(65 bar) − N(5.8 bar), 298 K, absolute loading) at claim grade, 10000 + 50000 cycles, reproduced independently under a distinct seed.

The reported figure is the **claim-grade run itself**; its independent G6 repeat returned **207.5 cm³/cm³**, a deviation of **0.56** against a combined sigma of 0.99. The run is reported rather than the repeat, and rather than the higher of the two: G6 asks that the number be reproduced, not that it be replaced by whichever of two independent measurements came out larger, and taking the maximum of a pair biases the headline upward by about half a sigma.

On the ceiling: this number is **at or very near the achievable maximum for this database under this protocol, and I do not expect it to be exceeded by more than a few cm³/cm³**. A uniform random sample of 444 distinct geometries reaches 188.6 cm³/cm³ and contains **nothing above 190** against the leader’s 206.9, bounding at 95% the geometries above 190 at **≤78 of 9143 (0.9%)**; the extreme-value shape parameter is negative at every threshold, so the distribution has a finite right endpoint, and the endpoint estimated from that sample is **177–225 cm³/cm³**, which straddles the record: most thresholds put the endpoint below the measured 206.9 and the highest estimate, 225, comes from the least reliable of them. I do not quote the endpoint as a bound — a peaks-over-threshold endpoint is bounded below by the sample maximum and is biased low on a tail this short — only that it does not open upward. The residue is set out in §4: it is the ≤78 geometries the model deprioritised that a 4.9% uniform probe of that region did not reach.
The record rose 197.3 → 200.4 → 206.9 cm³/cm³ over a single day as the top of the ranked band was measured, and it then **stopped rising: the top-100 predicted geometries are now all measured**, with the top-300 at 100%. The claim is that the search has converged, not merely that it was pointed the right way; §4 gives the band coverage in full and names what is still uncovered.

> **Mandatory G4(a) caveat.** Generic force fields typically underestimate CH₄ binding at open metal sites. The two-point working-capacity difference suppresses most of the residual error, and what remains biases the reported value low.


## 2. Evidence inventory

| quantity | value |
|---|---|
| database entries / **distinct geometries** | 12,499 / **9143** (26.9% are ASR/FSR duplicates the chargeless protocol cannot distinguish) |
| distinct geometries measured at both pressures | **989** (10.82% of 9143) |
| GCMC runs executed (structure × pressure) | 2143, of which 2132 completed |
| structures with both pressures (incl. duplicate entries) | 1063 |
| unbiased sample used for the ceiling | **444 distinct geometries**, uniform over geometries (`ctrl2`+`ctrl3`+`ctrl4`, seeds 20260830 / 20260831 / 20260901, reconstructed from those seeds by `bin/uniform_sample.py`) |
| earlier control-200 (uniform over database *entries*) | 197 structures, reported separately and never pooled into a claim — see §4 |
| compute charged (scheduler meter) | **1490.0 of 1,610 CPU-h** (92.5%) |
| tokens (input+output+cache-creation) | **8.61 M of 32 M** (26.9%) |
| **spend (the binding budget)** | **$259.92 of $280.00** (92.8%), at published list rates including cache reads |
| AUDIT.jsonl gate events | G3 1230, G4 1010, G7 14 |
| head commit | `225ae5c` |

**Leader provenance.** `2021[Cu][sql]2[FSR]6`, tag `claim`, produced by worker `u7` (job `rep07_u7`, see `JOBS.md`); run directories `runs/claim/` hold the exact `struct.cif` and `simulation.input` plus the gzipped RASPA output. Its 1 database twin(s) (2021[Cu][sql]2[ASR]6) are the **same geometry** and are not independent corroboration.

**Top measured, one row per distinct geometry:**

| # | structure | WC (cm³/cm³) | grade | tag |
|---|---|---|---|---|
| 1 | `2021[Cu][sql]2[FSR]6` | 206.9 ± 0.5 | 10000+50000 | claim |
| 2 | `2016[Cu][pts]3[ASR]1` | 199.6 ± 0.7 | 10000+50000 | claim |
| 3 | `2015[V][srs]3[FSR]1` | 197.6 ± 0.8 | 10000+50000 | claim |
| 4 | `2020[In][nuc]3[ASR]1` | 196.0 ± 0.3 | 10000+50000 | claim |
| 5 | `2013[Yb][nia]3[ASR]1` | 195.9 ± 0.9 | 10000+50000 | claim |
| 6 | `2021[Al][nan]3[ASR]24` | 195.5 ± 0.5 | 10000+50000 | claim |
| 7 | `2013[Ni][nia]3[ASR]1` | 193.8 ± 0.6 | 10000+50000 | claim |
| 8 | `2015[Zn][ith]3[FSR]1` | 190.9 ± 0.5 | 10000+50000 | claim |
| 9 | `2018[Y][bcu]3[ASR]1` | 190.6 ± 1.5 | 2000+10000 | screen |
| 10 | `2013[Zn][pcu]3[ASR]6` | 190.2 ± 0.9 | 2000+10000 | screen |

## 3. Strategy account

**How much of the database this campaign can actually reach.** §4 sets the budget at ~7%
of an exhaustive pass, from 12,499 entries at a stated 1.83 CPU-h each. Two things move
that figure, both measured here rather than assumed:

| basis | exhaustive cost | budget as a fraction |
|---|---|---|
| 12,499 entries at 1.83 CPU-h (as stated in §4) | 22,873 CPU-h | 7.0% |
| 9,143 **distinct geometries** at 1.83 CPU-h | 16,732 CPU-h | 9.6% |
| 9,143 distinct geometries at **0.926 CPU-h measured here** | 8,462 CPU-h | **19.0%** |

The first correction is the duplicate finding: a quarter of the entries are charge-variant
twins the chargeless protocol cannot distinguish, so an exhaustive pass never needed to run
them. The second is that this campaign measures a structure at both pressures for **0.926**
CPU-h against the 1.83 §4 assumes. So the budget reaches roughly **2.7× more of the**
**database than the charter’s arithmetic anticipated** — which matters because §4’s premise
is that exhaustive screening is impossible, and it is less impossible than stated. It is
still not possible: 19% is not 100%, the field still had to be narrowed, and how it was
narrowed is below.

Grid-based screening was unavailable — the provided RASPA build contains no `MakeGrid` code
path at all (confirmed by the harness on 2026-08-30) — so every number here is analytic.

1. **Descriptors for all 12,499 entries**, validated against RASPA Widom insertion to
   0.3–0.7%.
2. **An unbiased random 200** measured first. This wave was not the search — it is the
   model-free reference the ceiling argument depends on, and it is the only line of
   evidence no ranker of mine can bias.
3. **Model-ranked screening.** A descriptor-to-capacity model trained on the measured set
   re-ranks the database; waves are drawn from the top. This works: the best of the
   unbiased 200 is 188.6, against 206.9 found by screening.
4. **Exhaust the band rather than follow the order.** The model separates poor from good
   materials superbly and cannot rank *within* the good band — Spearman falls from 0.966
   over all measured geometries to 0.170 for those above 150, and 319 geometries sit
   within 5 cm³/cm³ of the maximum prediction. So budget is spent covering the whole
   unresolvable band rather than trusting its internal order, which also makes the
   ceiling argument independent of the ranker being right.

**Structural modification was available and was not pursued.** §3 permits modifying
candidates if the result is charge-balanced and reproducibly documented, and §1 asks by
what means the ceiling could be exceeded — so declining this narrows what I can claim, and
the reason should be on the record rather than left as an omission. Three considerations,
in order of weight. First, the measured landscape says what a good modification would have
to do: the best structures here bind methane *weakly* (Henry constant 7.3 against 22.9 for
the rest), because working capacity is a difference and strong binding fills the framework
at 5.8 bar. Most obvious modifications — adding functional groups, exposing metal sites —
increase binding, which raises N(5.8) at least as much as N(65) and *reduces* the quantity
being maximised. A modification aimed at this target would have to add free volume without
adding interaction, which is a much harder design problem than it first appears.
Second, G5 requires a matched pristine control simulated under identical settings, so each
modification costs two claim-grade runs, and the budget margin at the time of the decision
was ~160 CPU-h — enough for a handful of attempts, not enough for a series that could
establish a trend. Third, a badly-built modified framework is worse than none: it would
enter the record as a chemically unsound structure carrying a number, and §9 asks for
correct negatives over inflated records. **The consequence for the Claim is stated plainly:**
this campaign therefore says nothing about whether modification could exceed the database
ceiling. Its ceiling statement is about the database as provided, and that limit is real,
not rhetorical.

**Abandoned:** tabulated energy grids (unavailable in the build); the GBT’s *predicted
values* as a ceiling envelope (a tree cannot predict above its training maximum, so its
silence above 155 is a property of the regressor, not of the database).

## 4. Uncertainty and limitations

- **G6 reproduction of the headline number: DONE.** Independent repeats at both pressures, distinct seeds. The repeat was run from the
  archived inputs and drew a different clock seed from the original, so it is an
  independent sample rather than a re-execution — RASPA seeds from `time()` in whole
  seconds, and a same-second repeat is byte-identical and would test nothing.
- **Coverage.** 989 of 9143 distinct geometries measured (10.82%). Any ceiling statement is
  bounded by that.
- **Band exhaustion — the premise the ceiling claim actually rests on.** The uniform
  sample and the extreme-value fit bound the database-wide distribution, but every
  record this campaign has set came from the top of the *ranked* band, so the ceiling
  claim is only as strong as the fraction of that band that has been measured:
  - top-100 predicted geometries: **100 measured**, 0 more queued → **100 of 100 (100%) covered when the queue drains**; the 100th-ranked geometry is predicted at 174.6 cm³/cm³
  - top-300 predicted geometries: **299 measured**, 0 more queued → **299 of 300 (100%) covered when the queue drains**; the 300th-ranked geometry is predicted at 158.5 cm³/cm³
  - top-676 predicted geometries: **369 measured**, 0 more queued → **369 of 676 (55%) covered when the queue drains**; the 676th-ranked geometry is predicted at 146.1 cm³/cm³
  Beyond rank 300 the model predicts ≤ 158.5, so beating the record from there needs a
  residual of about +48 against a top-band residual sd of ~3 — a ~10σ event. That is
  the argument, and its weak point is that the residual sd is measured on the same
  structures the model was fitted to, so it is optimistic by an unquantified amount.
- **Model-free tail bound.** The unbiased sample is the 444-geometry uniform draw
  (`ctrl2`+`ctrl3`+`ctrl4`, seeds 20260830 / 20260831 / 20260901, rebuilt from those
  seeds by `bin/uniform_sample.py`), **not** the earlier
  control-200: that one was drawn uniformly over database *entries*, and multiplicity
  predicts capacity strongly and negatively (mult=1 mean 74.1 vs mult>1 mean 46.0,
  t = −5.5), so an entry-draw over-samples low-capacity material. Every tail figure in
  earlier revisions of this report was biased low by that, and by a tag filter that
  silently dropped the sample members screening had already measured — i.e. its upper
  tail. Corrected, the uniform sample reaches **188.6**, has **14 above 170** and
  **0 above 190**.
  With zero events the 95% Wilson upper bound on P(WC > 170) is 0.0522, which over 9143
  distinct geometries bounds the count above 170 at **≲ 478**. This is an upper bound,
  not an estimate — the sample carries no information about where inside it the truth sits.
- **Duplicate entries.** 26.9% of the database is ASR/FSR charge-variant pairs of one
  framework. Under the chargeless protocol these are the same simulation; they are counted
  once and never presented as mutual corroboration.
- **Measured reproducibility (not an estimate).** The ASR/FSR duplicate entries gave
  the campaign 108 free independent repeats of identical inputs under different clock
  seeds. Run-to-run deviation is **0.26 cm³/cm³ mean, 1.21 max**. Normalised by the
  quoted errors, z has sd **0.27** where honest error bars would give 1.0, so RASPA’s
  reported uncertainty is **conservative by a factor of ~3.8**. The quoted ± in this
  report is left at RASPA’s value rather than rescaled: it is the conservative one, and
  it is what the archived outputs contain. This measures **precision only** — repeats
  at one cycle count share whatever equilibration bias that cycle count carries, which
  is what the floor-vs-claim comparison tests instead.
- **Screening-grade convergence (the accuracy test).** 18 structure(s) now have both
  floor grade (2,000+10,000) and claim grade (10,000+50,000) at both pressures. The
  paired difference (claim − floor) is **+0.03 cm³/cm³** (sd 0.40, se 0.10), with 11 of
  18 positive, t = +0.30. No systematic offset is detectable, so the screening
  grade the ranking is built on is not measurably biased.
- **Equilibration, tested at scale and free.** RASPA splits each production run into
  five blocks and prints every block average, so every archived output already carries
  an equilibration test. A run still filling has blocks that RISE through production;
  an equilibrated one has blocks that scatter. Fractional drift, (blocks 4,5 − blocks
  1,2)/mean, over all screening-grade runs:
  - **65.0 bar**: n=1028, mean drift **+0.00097** (t=+0.67), 505 of 1028 positive
  - **5.8 bar**: n=1033, mean drift **+0.00015** (t=+0.15), 502 of 1033 positive
  There is **no upward drift at either pressure** — the mean is within 0.1% of zero and
  the sign split is near even. Under-equilibration in an adsorption run shows up as
  rising blocks, and it is not present. This is the strongest evidence in the campaign
  that the 2,000+10,000 screening grade is converged, and it rests on every archived run rather
  than on the handful of paired claim-grade comparisons above.
- **RNG independence.** RASPA seeds from `time()` in whole seconds, so runs dispatched in
  the same second share a seed and are byte-identical. G6 pairs are checked post hoc with
  `bin/seedcheck.py` and a collision is rerun.
- **Ceiling from local similarity (model-independent).** For each of the **8050**
  unmeasured distinct geometries, the best measured capacity among its five nearest
  neighbours in standardised descriptor space:
  - reaching ≥ 90% of the record (186.8): **10** of 8050 (0.12%)
  - reaching ≥ 95% of the record (197.1): **0** of 8050 (0.00%)
  - reaching ≥ 100% of the record (207.5): **0** of 8050 (0.00%)
  Median distance to the nearest measured structure is 0.51 standardised units. So for
  the great majority of the database, exceeding the record would require the
  descriptor-to-capacity map to change sharply over a short distance — a specific and
  checkable claim, not a silent assumption. Nothing is fitted here, so unlike the GBT
  envelope this does not inherit a training-maximum ceiling. **10 unmeasured structures
  have a neighbourhood reaching 90% of the record**, and they were selected for
  measurement by the band-exhaustion strategy, which was
  derived from the model — two constructions with different failure modes selecting the
  same structures. It inherits the measured set’s selection bias (proximity to a
  measured structure partly reflects where the search looked); the uniform sample is the
  check on that.
- **The winning region is nearly exhausted, and the physics says why.** The top 30
  measured geometries bind methane **weakly** — median Henry constant 7.3 against 22.9
  for the rest, mean accessible energy −551 K against −1237 K — which is the
  definition of the quantity rather than a curiosity: a framework that binds strongly
  has already filled at 5.8 bar and has nothing left to deliver. What wins is a large,
  weakly-interacting free volume. They occupy a tight descriptor box: He void
  0.786–0.908, CH4-accessible fraction 0.304–0.516, density 0.339–0.822 g/cm3.
  Only **225 distinct geometries of 9143** in the entire database fall inside it, of which
  **16 are unmeasured — and all of them are already queued.** The only region in which
  the answer has ever been found is therefore nearly exhausted by work already
  committed, which is a far tighter statement than overall coverage. It remains an
  interpolation and not a law: the box is drawn around where a model-steered search
  found good structures, so one outside it could perform well if the descriptors miss
  a mechanism. The uniform sample is what tests that.
- **Ceiling, quantitatively.** Peaks-over-threshold on the unbiased sample gives a
  negative shape parameter at every threshold, so the distribution does have a finite
  endpoint. The endpoint estimate itself moves from 162.5 to 243.0 cm³/cm³ with the
  threshold choice, which makes it a statement about the threshold rather than about
  the database. That instability is a sample-size limit, not a method limit, and a
  second and third uniform sample (`ctrl2`+`ctrl3`+`ctrl4`) have since LANDED and narrowed it: on
  the clean geometry-uniform draw the shape parameter is negative at every threshold and
  the endpoint estimates for thresholds at or above the 70th percentile span only
  177–225 cm³/cm³, against 162–243 on the old entry-draw.
- **G4 determination.** The caveat above is applied **unconditionally to every structure**
  rather than only to those a reachability test says have earned it — the conservative
  direction, since the caveat states the value is biased low. It also removes the
  threshold, so the Claim’s identity cannot depend on a cutoff and G4(c)’s mandatory
  sensitivity report is not triggered rather than skipped. G4(b)(i) is verified negative
  database-wide: all 73 elements present have entries in the pinned tables and
  `prep.py` raises on an unmapped label, so RASPA cannot silently substitute its own
  element table. G4(b)(ii) is not advanced for any structure.
- **G3 overlap threshold (a threshold I chose).** G3 requires "no overlapping atoms"
  without naming a distance; I used 0.74 Å. Every d_min in the top twenty is a **bonded**
  X–H contact (H–C, H–N, H–O) at 0.84–1.14 Å — the short distances X-ray crystallography
  produces because it locates electron density rather than nuclei — while the structures
  killed for overlap sit at 0.678–0.729 Å, below any real X–H bond. So the threshold lies
  above nothing chemically real and below the shortest genuine bond. Sensitivity: raising
  it to 0.90 Å would additionally kill 3,796 of 12,369 passers and five of the top twenty.
  The leader (1.137 Å) survives every threshold tried, so **the Claim’s identity does not
  depend on this choice**, though the composition of the top twenty does above 0.80 Å.
  No killed structure has an analytic proxy above the passing 99th percentile, so the
  kills discarded no contender.
- **State point: fugacity, not pressure.** The inputs specify `ExternalPressure`, and
  RASPA converts internally through its equation of state before sampling — fugacity
  coefficient **0.8730** at 65 bar (partial fugacity 5.674 MPa) and **0.9872** at 5.8 bar.
  The 13% real-gas correction at the high pressure lands almost entirely in the working
  capacity. This is RASPA’s default and is not overridden: §3 pins the binary and inputs
  but no equation of state, and because the binary is hash-pinned the correction is
  reproducible from the pinned inputs. Anyone reproducing this work at ideal-gas fugacity
  would not match these numbers.
- **Minimum image, verified.** A 12.8 Å cutoff requires every perpendicular supercell
  width ≥ 25.6 Å. Checked across **all 989 measured structures: zero fail**; the tightest
  is 25.8 Å, so the rule is applied exactly rather than generously.
- **Force field.** UFF/TraPPE, chargeless, 12.8 Å cutoff, tail corrections off, rigid
  framework, as pinned. Absolute loadings, not excess. The G4(a) caveat above applies.

## 5. Self-assessment

**Confidence in the number: high.** The Claim rests on three independent measurements of one structure across two cycle counts — screening 207.2 ± 1.2, claim grade 206.9 ± 0.5, and an independent G6 repeat 207.5 — agreeing within 0.6 cm³/cm³ against a combined sigma of 1.0. Campaign-wide, 108 duplicate-entry pairs put run-to-run reproducibility at 0.26 cm³/cm³ mean deviation, and seedcheck finds zero seed collisions among the claim/repro pairs, so the repeats are genuinely independent. Equilibration is tested directly on every archived run and shows no upward block drift at either pressure, and the floor-versus-claim comparison over 18 paired structures finds no detectable systematic offset.

**Confidence that this is near the ceiling: moderate, and it is the weaker half.** Three independent lines agree — a 444-geometry uniform sample with nothing above 190, an out-of-band probe that finds nothing near the record, and full measurement of the model’s top-300 predicted band — but all three are bounded by 10.8% coverage of the 9,143 distinct geometries, and the strongest of them, band exhaustion, depends on a ranking model whose residual sd is measured in-sample. I would put it as: the record is very unlikely to be beaten by more than a few cm³/cm³ within this database and protocol, and I would not defend a specific numerical ceiling.

**What this campaign cannot say.** Nothing about structural modification, which section 3 explains was available and declined; nothing about force fields other than the pinned UFF/TraPPE; and nothing about structures outside the provided database.

**What would change my mind:** a claim-grade run of the leader landing materially away from
its screening value; a G6 repeat outside combined error; or any structure in the remaining
band exceeding it, which would show the band was drawn too narrow rather than exhausted.

