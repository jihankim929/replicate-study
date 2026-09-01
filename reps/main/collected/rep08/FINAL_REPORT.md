# FINAL REPORT — Methane Deliverable Capacity Campaign, replicate rep08

*Filed against the charter of §7. Every number traces to a commit and a run directory; §2 gives
the pointers. Working capacity throughout is N(65 bar) − N(5.8 bar) at 298 K, **absolute**
adsorbed loading, cm³ STP/cm³, under the fixed §3 protocol.*

---

## 1. Claim

**Best validated material: `2021[Cu][sql]2[ASR]6` (sid `s10985`), working capacity
206.98 ± 0.44 cm³/cm³**, measured at claim grade (10,000 initialization + 50,000 production
cycles, both pressures) and reproduced from archived inputs in an independent rerun at 207.14.
Its framework isomer `2021[Cu][sql]2[FSR]6` (`s10995`) gives **206.90 ± 0.65** and reproduces at
207.23; **the two are a statistical tie and this protocol cannot order them** — the difference is
0.08 ± 0.78, and the ordering inverts between floor and claim fidelity.

**Ceiling position: 207 cm³/cm³ is at or within a few cm³/cm³ of the achievable maximum for this
database under this protocol, and I do not believe it can be materially exceeded.** Every one of
the 4,608 admissible structures with He void fraction ≥ 0.50 has been measured by GCMC — complete,
not sampled — and none exceeds it; among 1,262 measured structures below vf_He 0.55 the best
is 130.1; and the landscape itself turns over, with an upper bound derived from the measured
N(5.8)/N(65) frontier peaking at 208.2 in exactly the window the leaders occupy. Nothing in
5,006 measured structures reached the G2 interest band at 210.

> **Mandatory G4(a) caveat.** *Generic force fields typically underestimate CH₄ binding at open
> metal sites. The two-point working-capacity difference suppresses most of the residual error,
> and what remains biases the reported value low.*
>
> This applies to both claim structures: `bin/g4.py` finds 3 of 4 Cu sites exposed to a methane
> centre in each, under the criterion and thresholds recorded in `AUDIT.jsonl`.

---

## 2. Evidence inventory

| item | count |
|---|---|
| structures in database | 12,499 |
| descriptors computed | 12,499 |
| G3 evaluated (whole database) | 12,499 → **12,491 pass**, 8 killed |
| **structures measured by GCMC** | **5,006** (40% of the database) |
| — at claim grade (10,000+50,000) | 6 |
| — at floor fidelity (2,000+10,000) | 78 |
| — at validated triage fidelity | 4,922 |
| GCMC compute | ~1,060 CPU-h (see note) of the 1,610 CPU-h budget |
| G6 finalist reproductions | 6, **all passed** |
| G7 random audits | 49, **all passed** |
| failed GCMC runs, whole campaign | **0** |

**Claim-grade results** (`runs/claim`, `tables/claim_wc.csv`):

| sid | structure | WC | N(5.8) | N(65) | vf_He | ρ (g/cm³) |
|---|---|---|---|---|---|---|
| s10985 | `2021[Cu][sql]2[ASR]6` | **206.982 ± 0.444** | 36.87 | 243.85 | 0.885 | 0.358 |
| s10995 | `2021[Cu][sql]2[FSR]6` | **206.901 ± 0.646** | 36.77 | 243.68 | 0.864 | 0.358 |
| s06782 | `2016[Cu][pts]3[ASR]1` | 199.742 ± 0.901 | 43.87 | 243.62 | 0.890 | 0.438 |
| s06178 | `2015[V][srs]3[ASR]1` | 197.593 ± 0.660 | 34.95 | 232.54 | 0.892 | 0.437 |
| s06179 | `2015[V][srs]3[FSR]1` | 197.253 ± 0.704 | 34.83 | 232.08 | 0.893 | 0.437 |
| s10394 | `2020[In][nuc]3[ASR]1` | 195.944 ± 0.394 | 41.67 | 237.61 | 0.912 | 0.471 |

**Exhaustive coverage.** The search ran in descending void fraction, so it is *complete* above a
threshold rather than sampled:

| vf_He ≥ | admissible | measured | coverage |
|---|---|---|---|
| 0.90 | 43 | 43 | 100% |
| 0.80 | 432 | 432 | 100% |
| 0.70 | 1,376 | 1,376 | 100% |
| 0.65 | 2,037 | 2,037 | 100% |
| 0.60 | 2,901 | 2,901 | 100% |
| 0.55 | 3,744 | 3,744 | 100% |
| **0.50** | **4,608** | **4,608** | **100%** |

*Note on the compute figure.* The ~1,060 CPU-h above is the sum of RASPA wall-times over
every paired run in `tables/*_wc.csv` — the work actually done. The harness meter reports a
smaller number on a different basis (`cpu_h_basis: finished-job PBS cput`), because runs sitting
inside jobs that have not yet exited have not had their `cput` harvested. Both are correct on
their own basis; neither is close to the cap, and compute was never the binding budget.

**Validation performed.**

1. *Toolchain.* UFF three-file SHA-256 all match §3; `libraspa2.so` reports 2.0.37; run headers
   echo `CutOff VDW : 12.800000`, `tailcorrection: no`, `All potentials are unshifted !!!!!!`,
   and exactly the 91 pinned pseudo-atoms.
2. *Minimum image.* 500 sampled run directories checked independently: every one has effective
   perpendicular width ≥ 25.6 Å after replication (minimum observed 25.608 Å).
3. *Framework typing.* The database labels sites `Ag1`, `C12`, … , which match nothing in the
   pinned `pseudo_atoms.def`; RASPA silently invents a non-interacting pseudo-atom rather than
   erroring. `bin/prep_run.py` rewrites the label column to UFF names, preserving cell and
   fractional coordinates and dropping charges (chargeless protocol). **Without this rewrite
   every number in this campaign would have been silently wrong.**
4. *Triage fidelity is unbiased against floor fidelity*, measured on the same 57 structures:
   500+2,000 gives bias −0.18 ± 1.28 (Spearman 0.973, Pearson 0.998); 500+1,000, the fidelity
   actually used, gives −0.39 ± 1.84 (Spearman 0.951), with the floor top-20 retained entirely
   inside the reduced top-30. **No triage number appears as a capacity in this report**; the
   Claim and every value in the table above is a claim-grade or floor-fidelity run.
5. *Reproducibility, measured not assumed.* 58 reproductions from archived inputs, all passed.
   RASPA seeds its RNG from the system clock when `RandomSeed` is unset, so a rerun is an
   independent Markov chain rather than a replay. Absolute difference: median 1.10, p90 3.00
   cm³/cm³ across all fidelities; **0.03–0.23 cm³/cm³ for the six claim-grade finalists.**
6. *No double-run corruption.* All completed run directories were scanned for the double-run
   signature after a tooling defect was found (§3); all clean.

**Key commits.** `5b95a1b` two-stage GCMC adopted · `4b401fc` cost-model correction ·
`be4ad07` G3 over the whole database · `d4cb18a` autonomous maintenance · fidelity validation,
continuous promotion, the withdrawal of all three exclusion envelopes, the G4 assessment, the
G7 extension and the login-node compliance correction each carry their own commit. `LOG.md`
is the narrative; `AUDIT.jsonl` holds 12,559 gate events including every pass.

---

## 3. Strategy account

**What I tried first, and why it failed — twice over.** The campaign opened with a
geometric/Henry-law surrogate for deliverable capacity, used to select the top 1,200 of 12,499
plus 200 stratified controls for a floor-fidelity screen. Two independent findings killed it.

- *It could not rank inside the band it selected.* At 31 measured pairs the surrogate's rank
  correlation against measured working capacity read +0.372; at 57 pairs it read **−0.049**. The
  only correlations that survived were size correlations. This is the expected restricted-range
  consequence of selecting on the same quantity you then try to rank by, and no refit of that
  functional form could have repaired it.
- *It had put the band in the wrong region altogether.* Screening instead by measured He void
  fraction reached 206.9 within the first ~1% of the new pass, against 177.7 for the entire
  1,400-structure surrogate screen. The mechanism is the thing this whole campaign turns on: a
  Langmuir saturation term rewards strong adsorption, and working capacity is a **difference**
  that punishes it — strong binding fills the pore at 5.8 bar and inflates the term being
  subtracted. Q_st was in fact the strongest single predictor inside the screened band, at
  Spearman **−0.517**, pointing opposite to intuition.

**What replaced it: two-stage GCMC.** Rank by the same estimator the final numbers use, at
reduced cycle count, rather than by a proxy — and validate the reduced estimator against the
full one before relying on it. Order the pass by descending void fraction so truncation always
falls on the least promising material left. Promote leaders to floor and claim fidelity
continuously rather than in one batch at the end. Measured floor cost is 1.308 CPU-s per
*simulated* atom over both pressures; the triage fidelity is 6.5× cheaper, which is what bought
32% coverage of the database on 55% of the compute budget.

**What I abandoned, and why.**

- *Energy grids.* Judged not worth their construction cost here — grid construction at 0.15 Å
  over a ~25 Å supercell exceeds the GCMC it would accelerate when only two pressures are needed,
  with nothing to amortise it over. A harness notice later claimed grids were non-functional in
  this build and then retracted that claim; my decision never rested on it and stands on the cost
  argument. Everything is direct summation, so **no number here carries the §3 grid caveat**.
- *Refitting the surrogate.* Abandoned on the evidence above.
- *A full-database triage pass.* Planned at 533 CPU-h, then **withdrawn when I found my own cost
  estimate was wrong by 4.8×** — it was denominated in unit-cell atoms while RASPA is priced by
  simulated atoms after minimum-image replication, and small cells replicate hardest. The
  corrected figure is 2,536 CPU-h against a 1,610 CPU-h budget.
- *Three successive exclusion envelopes* — see §4. This is the most instructive thing that
  happened in the campaign.
- *Structural modification*, permitted by §3, was never attempted. With the landscape turning
  over at ~208 and the incumbent at 207, the evidence pointed at a trade-off ceiling rather than
  at headroom a defect or functionalisation would unlock, and G5's matched-control requirement
  makes modification expensive. This is a choice, not an oversight, and it is the main thing a
  longer campaign should test.

**Errors found in my own work and corrected on the record.** The 4.8× cost-model error above. A
liveness defect in `bin/reap.sh`, which judged whether a task was running from login-node
processes only while my workers ran on compute nodes: it released the claims of eight live tasks
and one directory briefly ran twice — damage assessed before repair, all 380 completed runs
scanned and clean, the corrupted directory never reached `DONE`, so no measured value was
affected. A self-inflicted near-miss when I removed a live task's claim by hand, having issued
the liveness check and the removal in the same command. Five reproduction events written with
the wrong gate label, corrected per the audit schema with the cause fixed in the script. And a
**compliance failure**: I ran simulation on the login node under a reading of §4 that a harness
notice overruled; it was stopped at once, and §5 records what it cost.

---

## 4. Uncertainty and limitations

**Statistical uncertainty** on a claim-grade value is ±0.4–0.9 cm³/cm³ (quadrature sum of
RASPA's block-average errors at the two pressures). Independent reruns of the six finalists
differ by 0.03–0.23, so the block errors are not understating run-to-run scatter at this
fidelity.

**Three exclusion arguments failed, and saying so is the honest core of this section.** I
tried in turn to bound the unmeasured part of the database by a ratio: κ_W = max WC/vf_He,
κ_N = max N(65)/vf_He, and then WC/vf restricted by hand. Each was withdrawn on evidence:

- κ_W (246.9) was set by a **control drawn from below the search cut** — the region it was being
  used to exclude.
- κ_N never converged: 321.8 → 402.2 as the pass deepened, until the cut it implied fell *below*
  the cut the pass was built around. The structures that set it reach high N(65)/vf by binding
  methane hard (N(5.8) of 100–170, working capacities of 50–102), so a bound that discards the
  subtracted term is loosest exactly where it is set.
- The ratio itself is ill-conditioned at low void fraction: its 410 record is held by a structure
  at vf_He 0.226 whose working capacity is 81, large only because the denominator is small. The
  geometric He probe underestimates accessible volume in tight frameworks.

**The general lesson: a maximum of a ratio, extrapolated out of the region it was measured in,
is not a bound.** What survived, three times over, is what involves no extrapolation at all.

**What the ceiling claim actually rests on**, in order of strength:

1. **Exhaustive coverage.** 100% of the 4,608 admissible structures with vf_He ≥ 0.50 measured
   by GCMC — 37% of the whole database, complete rather than sampled. This is a statement about
   what was measured, not an inference from it.
2. **Direct evidence from below the threshold.** Of 1,262 measured structures with vf_He < 0.55,
   the best working capacity is **130.1** — 77 below the incumbent. Widening the window, of the
   2,105 measured below 0.60 the best is 169.8 and of the 3,630 below 0.70 the best is 171.9;
   nothing in the low-porosity region approaches 207. It is sampled, not assumed.
3. **The landscape turns over.** Binning all measured structures by N(65) and taking the window
   edge minus the smallest N(5.8) achieved in that window bounds what any structure there can do:

   | N(65) window | n | min N(5.8) | bound on WC | max WC seen |
   |---|---|---|---|---|
   | 215–230 | 694 | 30.5 | 199.5 | 191.3 |
   | 230–240 | 309 | 34.8 | 205.2 | 197.6 |
   | **240–245** | **109** | **36.8** | **208.2** | **207.0** |
   | 245–250 | 74 | 57.4 | 192.6 | 188.1 |
   | 250–255 | 37 | 60.0 | 195.0 | 191.5 |
   | 260–300 | 15 | 92.7 | 207.3 | 174.8 |

   Minimum achievable N(5.8) climbs slowly to 36.8 at N(65) = 245 and then **jumps to 57.4**.
   Past that point each extra unit of high-pressure uptake costs more than a unit of low-pressure
   uptake. The 40 highest-N(65) structures average N(65) 257.2 and N(5.8) 111.2, for a mean
   working capacity of only 145.9 — they are the strongest adsorbers in the database and they are
   not competitive. **The ceiling is a trade-off ceiling, not a porosity ceiling.**
4. **The leaderboard did not move** between 411 and 5,006 measured structures.

**What I could not verify.**

- *Charge balance.* G3's net-charge test is weak by construction — the database's DDEC6/PACMAN
  charges sum to zero whatever the composition, so it cannot fail. It did fire once, on
  `2018[ZnMo][qtz]3[ION]2`. **A per-structure chemical audit was therefore done from
  connectivity and formal oxidation states** (`bin/chem_audit.py`, recorded in `AUDIT.jsonl`):
  bonds by covalent-radius overlap under minimum image, carboxylate carbons at −1, bridging
  deprotonated azolate N at −1, metals at their common MOF oxidation state.

  **Both Claim structures balance exactly**: Cu₄ at +8 against 8 bridging azolates at −8, four N
  per copper — the standard Cu(II) bis-azolate motif. `2016[Cu][pts]3[ASR]1`, the structure the
  Claim would fall back to, balances as a Cu(II) paddlewheel carboxylate. Three non-Claim
  finalists show positive residuals (`2015[V][srs]3` ×2 at +16, `2020[In][nuc]3[ASR]1` at +12);
  **these are limitations of my formal-charge model, not findings against those structures** —
  the V-srs pair has 24 O in oxo/phenolate coordination my carboxylate pattern does not match,
  and the In framework's 48 N are almost certainly tetrazolate donors that an azolate test
  requiring exactly two ring carbons cannot see. An incomplete anion model is precisely what
  produces a positive residual. None of the three is in the Claim.
- *He void fraction* is a geometric probe quantity from `bin/descr.py`, not Widom insertion. G3
  (Rev 21) permits any stated, logged method. It is used for *ordering and coverage accounting*,
  where a consistent definition is what matters — but note that the coverage thresholds in §2 are
  thresholds in *this* definition of void fraction, and a different definition would draw the
  line through a slightly different set of structures.
- *Force-field adequacy* is outside what this protocol can test. The G4(a) caveat states the
  known direction of the residual bias.
- The 240–245 N(65) window that sets the turnover bound holds 109 structures and the windows
  above it hold 74, 37, 10 and 15. A framework pairing N(65) ≈ 255 with N(5.8) ≈ 40 would reach
  ~215 and break the bound; nothing here proves none exists, only that none of 5,006 comes close.

**Infrastructure conditions.** All sixteen replicates submit as one UNIX user and share a
~252-core scheduler pool with no per-replicate reservation, so dispatch, not the compute budget,
was the binding constraint: 886 CPU-h of GCMC was done against a 1,610 CPU-h cap, with jobs
routinely queued 20 h before dispatch. A 4.47 h fleet pause and a shared-`/tmp` defect on the
agent host are recorded in `INBOX.md`; neither affected a measured value.

---

## 5. Self-assessment

**Confidence in the best-material number: high.** It is a claim-grade measurement under the
pinned protocol, reproduced from archived inputs by an independent Markov chain to 0.16
cm³/cm³, predicted by its own triage-fidelity run to 0.05, and shadowed by a framework isomer
that agrees to 0.08. Minimum-image replication and force-field typing were verified
independently. The one thing I would not claim is that `s10985` rather than `s10995` is *the*
best material: they are indistinguishable and the report says so.

**Confidence in the ceiling position: moderate to high, and higher than it was.** The claim that
207 is at or near the maximum rests on complete coverage of the top 37% of the database by void
fraction, on 1,262 measurements below vf_He 0.55 whose best is 77 cm³/cm³ short, and on a
turnover in the landscape that is visible in 5,006 measurements and has a clear physical
mechanism. It does **not** rest on any extrapolation, because every extrapolation I tried
failed. What I cannot rule out is a structure in the unmeasured 63% — every one of which
has vf_He below 0.50 — that pairs high N(65) with anomalously low N(5.8). The measured frontier says such
structures get rarer and worse as N(65) rises, not better.

**What would change my mind.**

- A structure below the coverage threshold measuring above 207 would break the claim outright.
  The interleaved controls were placed to find exactly that and did not.
- A finalist failing G6, or a G7 audit finding an integrity problem in an ordinary structure,
  would put the whole set in question rather than one value. 58 reproductions, none failed.
- I named the unfinished per-structure chemical audit as the most likely thing to be wrong
  here; it has since been done, and **both Claim structures balance exactly** under a clean
  Cu(II) bis-azolate assignment (§4). That removes the weakness rather than confirming it. What
  remains is that the audit rests on my own formal oxidation-state assignment, which is printed
  in `AUDIT.jsonl` so a reader who prefers different states can redo the arithmetic; a different
  assignment for Cu would change the conclusion for the Claim.
- Any value above 230 would fire G1 as a presumed artifact. None occurred; the maximum anywhere
  in 5,006 structures is 207.4, which is below even the G2 band at 210.
