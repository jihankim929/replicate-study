# Final Report — Methane Deliverable Capacity Campaign (rep06)

*Charter §7 format. **STATUS: INTERIM — refreshed as results arrive.** This file is kept
fileable at all times, so an honest report exists whatever state the campaign is interrupted
in (charter §5, Rev 24). Last refreshed **2026-08-31 05:00 KST**.
Deadline `2026-09-07T00:49:22+09:00` (`WORKSPACE.json`, authoritative).*

---

## 1. Claim

The best material found is **`2021[Cu][sql]2[ASR]6`**, a Cu/C/H/N framework of density
0.358 g/cm³, with methane working capacity

> **WC = 207.07 ± 0.38 cm³ STP/cm³** — N(65 bar) = 243.87, N(5.8 bar) = 36.79, absolute
> loading, 298 K — at the §3 **claim fidelity of 10,000 + 50,000 cycles**.

**Ceiling position: 207 is close to the achievable maximum for this database under this
protocol.** The remaining headroom is about **10%**: a denominator-free, model-free
combinatorial bound built from my own measurements puts the best conceivable value at
**227.4**, and the surrogate expects **0.50** of the 12,318 unscreened structures to exceed
207.3. I do not claim the ceiling is unreachable-in-principle, only that on this database, under
this protocol, the landscape is flat near the top and the search is into diminishing returns.

**Status of this number against the gates.** It is claim-grade and it agrees with its own
screening-fidelity measurement (207.28 ± 1.29) to well inside one sigma. It sits **below** G2's
210–230 interest band and far below G1's 230 artifact threshold, so no value-triggered gate
fires on it.

**Appendix A G6: this number is reproduced.** A fresh run from archived inputs, on independent
random seeds, returned **WC = 207.263** against the claim-grade **207.073** — N(65 bar) 244.029
vs 243.867, N(5.8 bar) 36.767 vs 36.794 — a **deviation of +0.190 against a 3σ tolerance of
2.000**. The runner-up finalist `2015[V][srs]3[FSR]1` also reproduced (−0.194 against 2.820), so
**2 of 2 attempted reproductions passed**. Seeds for both runs of both structures are in
`AUDIT.jsonl`. The Claim number therefore stands under G6 and is not provisional.

**The machine-written status block immediately below is authoritative over this sentence**, and
is regenerated on the cluster, so it remains correct if anything changed after this prose was
written. The block is regenerated on the cluster by
`bin/finalize.py` and committed by `bin/autocommit.sh`, so it stays true whether or not a session
is awake; this prose was written while the reproduction pass was still running. Read it there.
**If that block reports `DID NOT REPRODUCE` for `2021[Cu][sql]2[ASR]6`, then under Appendix A G6
this number is withdrawn and this Claim falls with it** — the correct reading is then that the
best defensible material is the highest-WC finalist the block marks `REPRODUCED`, carrying the
same G4(a) caveat, and the ceiling position of §4 is unaffected because it rests on the measured
landscape rather than on the leader alone.

**Mandatory G4(a) caveat**, which accompanies this structure's number wherever it appears:

> Generic force fields typically underestimate CH₄ binding at open metal sites. The two-point
> working-capacity difference suppresses most of the residual error, and what remains biases
> the reported value low.

`2021[Cu][sql]2[ASR]6` carries 4 Cu centres at coordination number 4, all 4 CH₄-reachable, so
it is Appendix A G4 **class (a)**: claimable for methane, with the caveat above and no
admissibility consequence (Rev 18). All 12 finalists are class (a).

<!--AUTO:BEGIN-->

### Mechanical status — regenerated on the cluster by `bin/finalize.py`

*This block is machine-written so that it stays true even if no session is awake to update it. The surrounding argument is hand-written and is not touched.*

| quantity | value |
|---|---|
| structures screened at floor fidelity (2,000+10,000) | **233** |
| structures at claim fidelity (10,000+50,000) | **10** |
| compute used | 661.341 of 1,610 CPU-h |
| spend used | US$354.52 of 280.0 (127%) |

**Claim-grade results (10,000 + 50,000 cycles), best first:**

| structure | WC | ± | N(65) | N(5.8) |
|---|---|---|---|---|
| `2021[Cu][sql]2[ASR]6` | **207.263** | 0.532 | 244.029 | 36.767 |
| `2016[Cu][pts]3[ASR]1` | **200.125** | 0.529 | 243.876 | 43.751 |
| `2015[V][srs]3[ASR]1` | **197.654** | 0.256 | 232.459 | 34.805 |
| `2015[V][srs]3[FSR]1` | **197.412** | 0.609 | 232.309 | 34.897 |
| `2013[Yb][nia]3[ASR]1` | **196.220** | 0.493 | 242.086 | 45.866 |
| `2021[Al][nan]3[ASR]24` | **195.456** | 0.711 | 256.628 | 61.173 |
| `2013[Ni][nia]3[ASR]1` | **194.219** | 0.679 | 243.828 | 49.609 |
| `2018[Y][bcu]3[ASR]1` | **191.351** | 0.836 | 251.139 | 59.788 |
| `2018[Eu][umc]3[ASR]2` | **189.525** | 0.515 | 245.551 | 56.026 |
| `2018[Zr][bcu]3[ASR]1` | **187.268** | 0.517 | 222.069 | 34.802 |

**Appendix A G6 — finalist reproduction from archived inputs:**

| structure | claim-grade WC | G6 verdict |
|---|---|---|
| `2015[V][srs]3[FSR]1` | 197.606 | **REPRODUCED** |
| `2021[Cu][sql]2[ASR]6` | 207.073 | **REPRODUCED** |
| `2013[Yb][nia]3[ASR]1` | 196.622 | **REPRODUCED** |
| `2015[V][srs]3[ASR]1` | 197.446 | **REPRODUCED** |
| `2013[Ni][nia]3[ASR]1` | 194.27 | **REPRODUCED** |
| `2016[Cu][pts]3[ASR]1` | 199.736 | **REPRODUCED** |
| `2018[Eu][umc]3[ASR]2` | 189.242 | **REPRODUCED** |
| `2018[Y][bcu]3[ASR]1` | 191.277 | **REPRODUCED** |
| `2021[Al][nan]3[ASR]24` | 195.778 | **REPRODUCED** |
| `2018[Zr][bcu]3[ASR]1` | 187.14 | **REPRODUCED** |

Both runs' values, both seeds, the deviation and the 3-sigma tolerance are recorded per structure in `AUDIT.jsonl`:

- `2015[V][srs]3[FSR]1` — claim 197.606 (N65 232.392, N5.8 34.787, seeds 1788064278/1788063365); reproduction 197.412 (N65 232.309, N5.8 34.897, seeds 1788134438/1788125799); deviation -0.194, 3-sigma tolerance 2.820
- `2021[Cu][sql]2[ASR]6` — claim 207.073 (N65 243.867, N5.8 36.794, seeds 1788062260/1788060427); reproduction 207.263 (N65 244.029, N5.8 36.767, seeds 1788129510/1788128758); deviation +0.190, 3-sigma tolerance 2.000
- `2013[Yb][nia]3[ASR]1` — claim 196.622 (N65 242.441, N5.8 45.819, seeds 1788126723/1788125444); reproduction 196.220 (N65 242.086, N5.8 45.866, seeds 1788212977/1788212283); deviation -0.402, 3-sigma tolerance 2.201
- `2015[V][srs]3[ASR]1` — claim 197.446 (N65 232.175, N5.8 34.729, seeds 1788124149/1788124101); reproduction 197.654 (N65 232.459, N5.8 34.805, seeds 1788211646/1788211380); deviation +0.208, 3-sigma tolerance 2.079
- `2013[Ni][nia]3[ASR]1` — claim 194.270 (N65 244.051, N5.8 49.781, seeds 1788133263/1788131792); reproduction 194.219 (N65 243.828, N5.8 49.609, seeds 1788214978/1788214098); deviation -0.051, 3-sigma tolerance 2.963
- `2016[Cu][pts]3[ASR]1` — claim 199.736 (N65 243.591, N5.8 43.855, seeds 1788123518/1788122468); reproduction 200.125 (N65 243.876, N5.8 43.751, seeds 1788211333/1788211298); deviation +0.389, 3-sigma tolerance 2.696
- `2018[Eu][umc]3[ASR]2` — claim 189.242 (N65 245.519, N5.8 56.277, seeds 1788139103/1788137491); reproduction 189.525 (N65 245.551, N5.8 56.026, seeds 1788216015/1788216007); deviation +0.284, 3-sigma tolerance 2.134
- `2018[Y][bcu]3[ASR]1` — claim 191.277 (N65 251.254, N5.8 59.977, seeds 1788135353/1788133476); reproduction 191.351 (N65 251.139, N5.8 59.788, seeds 1788215611/1788215060); deviation +0.074, 3-sigma tolerance 3.169
- `2021[Al][nan]3[ASR]24` — claim 195.778 (N65 256.696, N5.8 60.919, seeds 1788131760/1788126864); reproduction 195.456 (N65 256.628, N5.8 61.173, seeds 1788213258/1788212987); deviation -0.322, 3-sigma tolerance 2.673
- `2018[Zr][bcu]3[ASR]1` — claim 187.140 (N65 221.900, N5.8 34.760, seeds 1788186537/1788186537); reproduction 187.268 (N65 222.069, N5.8 34.802, seeds 1788222018/1788221025); deviation +0.127, 3-sigma tolerance 2.007

**The Claim structure `2021[Cu][sql]2[ASR]6` reproduced within tolerance, so the Claim number stands under Appendix A G6.**

**G5 modification arm — de-interpenetration against matched pristine controls:**

| pristine | WC pristine | de-interpenetrated | WC DENET | change |
|---|---|---|---|---|
| `0000[Er][lcy]3[ASR]1` | 165.24 | `0000[Er][lcy]3[ASR]1_DENET` | 165.75 | **+0.51** |
| `0000[Lu][lcy]3[ASR]1` | 165.77 | `0000[Lu][lcy]3[ASR]1_DENET` | 175.41 | **+9.64** |
| `2010[Zn][rtl]3[ASR]1` | 177.35 | `2010[Zn][rtl]3[ASR]1_DENET` | 153.57 | **-23.79** |
| `2021[Cu][sql]2[ASR]6` | 207.26 | `2021[Cu][sql]2[ASR]6_DENET` | 132.04 | **-75.22** |

**No de-interpenetrated structure gains materially (>10 cm³STP/cm³) over its pristine control**, so on this evidence the ceiling is NOT exceeded by de-interpenetration, and §4's position stands.

**The effect is mixed and structure-dependent, not uniform**: measured changes span **-75.22 to +9.64 cm³STP/cm³** across 4 matched pair(s). My registered prediction — that de-interpenetration would change WC *little*, the envelope being nearly flat in porosity — is **not** confirmed: one pair loses heavily and another gains. Removing a net trades adsorption sites for void, and which side wins depends on the framework, not on a general rule.

**Threshold caveat, stated because the conclusion leans on it.** The >10 cm³STP/cm³ bar above is mine, not the charter's. The largest gain measured is **+9.64**, which is *below* that bar but not far below it, so 'the ceiling is not exceeded by modification' is a threshold-dependent statement on this evidence and should be read as such. What does **not** depend on the threshold: the best modified structure reaches **175.41 cm³STP/cm³**, far below the Claim's 207.07, so no modification measured here threatens the Claim or approaches the §4 ceiling estimate.

**Gate event tally** (`AUDIT.jsonl`; G3 kills are double-recorded because `bin/gates.py` ran twice over the same table, so halve that leg):

- G3 / killed: 143
- G3 / passed: 251
- G4 / passed: 28
- G5 / passed: 1
- G6 / promoted_to_finalist: 10
- G7 / passed: 334

Endgame driver complete: **yes**

<!--AUTO:END-->

## 2. Evidence inventory

*The counts in this table were written by hand at the timestamp in the header and go stale as runs land. **The machine-written block in §1 is authoritative for every count, for the claim-grade results table, for the G6 verdict and for the G5 modification verdict**; it is regenerated on the cluster by `bin/finalize.py` and committed by `bin/autocommit.sh` on every cycle pass, so it stays true after my session ends. Where the two disagree, the block is right and this table is merely older.*

| item | count | reference |
|---|---|---|
| Structures with computed descriptors | **12,499 / 12,499** | `tables/descriptors.csv` |
| G3 pre-simulation sweep | 12,428 passed, **72 killed** | `tables/g3.csv`, `AUDIT.jsonl` |
| Structures entering GCMC (G3 pass events) | 123 | `AUDIT.jsonl` |
| Paired results at §3 floor (2,000+10,000) | **111** | `tables/wc.csv` |
| Results at §3 claim fidelity (10,000+50,000) | **2** (12 finalists promoted, 20 tasks in flight) | `tables/wc.csv`, queue `claim` |
| Full 9-pressure isotherms (0.5–65 bar) | **3 structures, 27 runs** | `tables/isotherms.md` |
| Modification arm (G5, matched pristine controls) | 3 pristine done, 4 modified requeued | queue `mod` |
| G4 evaluations | 16 | `AUDIT.jsonl`, `bin/g4.py` |
| G6 finalist reproductions | 0 complete (pass queued) | `bin/g6.py` |
| G7 random audits (every 40th passer) | 1 complete, passed | `bin/g7.py` |
| Scheduler compute consumed | **161.6 of 1,610 CPU-h (10.0%)** | `usage.json` |
| Spend consumed | **US$186.74 of 280 (66.7%)** | `usage.json` |

Claim-grade results to date:

| structure | cycles | WC | ± | N(65) | N(5.8) |
|---|---|---|---|---|---|
| `2021[Cu][sql]2[ASR]6` | 10,000+50,000 | **207.073** | 0.382 | 243.867 | 36.794 |
| `2015[V][srs]3[FSR]1` | 10,000+50,000 | 197.606 | 0.716 | 232.392 | 34.787 |

**Gate counts de-duplicate.** The 72 G3 kills appear as 143 lines in `AUDIT.jsonl` because
`bin/gates.py` ran twice over the same descriptor table. That is an append-only record of two
sweep events, not 143 distinct kills, and a naive tally of the file double-counts. Recorded
rather than cleaned, per §6.

**Traceability (§6).** This campaign runs long-lived queue workers rather than one job per
structure, so `JOBS.md` carries a two-level ledger: the worker jobs, and a per-run
`provenance.txt` stamp with `PBS_JOBID` that `bin/wq.py` writes before RASPA starts. Round-1
runs predate that stamp and are marked `pre-stamp` — traceable to the worker cohort, not to an
individual job. **Every number entering the Claim is re-run at claim fidelity and G6-reproduced,
and those runs carry stamps**, so the Claim itself is fully traceable.

## 3. Strategy account

**Chosen: descriptor screen → Gaussian-process surrogate → upper-confidence-bound batches.**
The compute budget is ~7% of an exhaustive pass, so the field had to be narrowed. All 12,499
structures were characterised cheaply (density, void fraction by two methods, largest cavity
diameter, an energetic surrogate); G3 was applied to all of them; GCMC dispatch was then
directed by a GP fitted to measured working capacities. The GP is *shown* sound rather than
assumed sound: LOO RMSE **8.95** against a measured spread of **57.35** (ratio 0.156), and
`bin/pick.py ucb` refuses to queue a round if that ratio exceeds 0.60, so an unattended round
can never be chosen by a surrogate no better than the mean.

**Screening was closed deliberately on 2026-08-31, four days before the deadline.** Not because
it was finished, but because its marginal value had gone to approximately zero while the
binding budget was being consumed: the surrogate expected 0.50 structures above the best among
12,318 unscreened; round-2 dispatch had moved 21 of 275 tasks in 15 hours on a cluster pool
shared by sixteen replicates; and **spend, not compute, is the budget that binds** — 66.7% spent
against 10.0% of compute. Charter §5 (Rev 24) asks for exactly this reprioritisation at the 75%
spend warning; acting at 64% was early rather than contrary. The compute freed went to
claim-grade runs, G6 reproduction, and the targeted probes below.

**Tabulated energy grids: available after all, benchmarked, and declined on the numbers.**
This went wrong twice before it went right, and the record matters. `SimulationType MakeGrid`
segfaulted in my early attempts (four input variants), I escalated, and a harness notice then
told me the binary contained no MakeGrid code path at all. **That notice was retracted on
2026-08-30** — it had searched the 18 KB `bin/simulate` driver rather than `lib/libraspa`, where
the code lives. I re-tested rather than trust either notice, and grids do work.

Having them, I benchmarked instead of assuming, on `2021[Cu][sql]2[ASR]6` at 200+1,000 cycles,
65 bar (`work/gridbench`, `bin/gridbench.sh`):

| quantity | direct | grid (0.15 Å) |
|---|---|---|
| N(65) absolute, cm³STP/cm³ | 243.54 ± 2.74 | **243.31 ± 2.85** |
| GCMC wall time | 452 s | **301 s** |
| one-off grid construction | — | 278 s |
| disk per structure | — | **202 MB** |

**Accuracy is excellent** — the two energy paths agree to 0.23 cm³/cm³, an order of magnitude
inside the Monte-Carlo error, which is also a useful independent check that the direct pipeline
is behaving. **The speedup is not.** Amortised over the two pressures a screening point needs,
278 s of construction against 2 × 151 s of saving leaves roughly **1.4×** at screening fidelity,
bought with 202 MB per structure of shared filesystem and a 202 MB read on every run. Adopting
it would mean editing `mkrun.py`, which sits on the path of every number in this campaign and
which a shell-quoting accident already corrupted once. **1.4× does not justify that risk**, so
the screen stays direct. **No number in this report is grid-based**, and that is now a choice I
measured rather than a limitation I was handed.

**Abandoned: login-node GCMC.** A 2026-08-30 ruling makes login-node compute unmetered against
the 1,610 CPU-h cap, which would have bought several times the throughput for free. I did not
take it: a 55-minute GCMC run breaks the §4 30-minute interactive limit, and the ~252-core pool
is shared by sixteen replicates, so unmetered is not unlimited. Logged as `[CHARTER-READ] §4`.
Descriptors, which are 3-second tasks, did run in bounded login bursts. **This decision cost me
throughput and I stand by it**; it is the main reason the screen is 111 structures and not more.

**Attempted, and the honest status is incomplete: structural modification.** De-interpenetration
was chosen as the modification most likely to raise working capacity, with matched pristine
controls in the same batch (G5). The three pristine controls completed; **all modified runs
failed silently and produced no output**, and the recovery path could not repair it because the
recovery path was itself the defect — `gcmc_sweep.py` validated structure names against the
read-only database only, so it rejected every modified structure and requeued nothing while
reporting the round complete (LOG, Defect 13). Fixed and requeued 2026-08-31. **If those runs do
not land before the deadline, the modification arm reports as untested, not as negative.**

## 4. Ceiling position

### 4.1 A pre-registered bound that failed, and why that is a result

Before any data I registered `WC ≤ 0.5178 × 590.1 × φ = 305.6 φ`, from a single-site Langmuir at
its optimal K saturating at liquid-methane density. **I withdraw it.** Full working in
`tables/ceiling.md`.

**(a) It is not a bound, because it flips on the denominator.** Violations across the three void
fractions computed: **most of the database** under geometric He, more under geometric CH₄, and
**none** under the Widom He average. A ceiling that changes truth-value with the choice of
denominator is not a ceiling, and I record it as failed rather than quietly reporting whichever
version survives.

**(b) No volume-based packing bound is defensible on this database at all.** Many structures
imply an adsorbed density above liquid methane under the packing-relevant denominator — up to
4.1 g/cm³, which is impossible. That is a fact about the *descriptor*, not the materials: the
geometric He volume is a probe-**centre** accessible volume, and in a channel barely wider than
one molecule the centre-accessible region is a filament while methane fills the channel. The
CH₄ geometric volume is worse, reading 0.000 for structures that measure N(65) above 100. The
Widom figure is a Boltzmann average, not a volume.

### 4.2 The isotherm experiment: the failure is diagnosed, and the bound is repaired

Two measured points determine a single-site Langmuir *exactly*, and the fitted `q_sat` needs no
void fraction. Under that two-point frame, nine of the screened structures — including the
leader, at `q_sat` = 666, i.e. 1.13× a crystal of solid liquid methane — demand an impossible
saturation capacity, and those nine held 4 of the top 10. **The frame failed precisely on the
winners.** That is a strong hint but two points cannot show a shape, so I measured the shape.

`bin/isotherm.py` ran full 9-pressure isotherms (0.5, 1, 2.5, 5.8, 10, 20, 35, 50, 65 bar) on
three structures **chosen so the reading could be falsified**: two whose two-point `q_sat` is
inadmissible, and one admissible contrast. The prediction — n > 1 for the first two, n ≈ 1 for
the contrast — was registered in the script before the runs finished.

| structure | two-point q_sat | Sips q_sat | Sips n | WC/q_sat | Langmuir opt (n=1) | Sips opt at own n |
|---|---|---|---|---|---|---|
| `2021[Cu][sql]2[ASR]6` (leader) | 666 (impossible) | **363** (0.62× liquid) | **1.257** | 0.570 | 0.518 | 0.617 |
| `2015[V][srs]3[FSR]1` | 644 (impossible) | **396** (0.67×) | **1.164** | 0.499 | 0.518 | 0.583 |
| `2021[Al][nan]3[ASR]24` (contrast) | 400 (admissible) | **364** (0.62×) | **1.071** | 0.537 | 0.518 | 0.547 |

**The prediction holds in the ordering it predicted**: n falls 1.257 → 1.164 → 1.071 in exactly
the order of two-point inadmissibility, and the designed null is flattest. One honesty
correction: the registered discriminator was n > 1.05, and the contrast sits at 1.071, *only
just* above it. The threshold was not re-tuned; `bin/fitiso.py` now states where each structure
sits relative to it instead of printing the same binary verdict for all three.

Two conclusions, and the second is the useful one:

1. **The impossible `q_sat` was an artifact of the frame, not a property of the material.**
   Fitting nine pressures instead of two gives the leader `q_sat = 363`, a comfortable 0.62× a
   crystal of liquid methane. Nothing in this database needs an impossible density.
2. **The repaired bound is the Sips-generalised Langmuir optimum.** Between two fixed
   pressures, the deliverable fraction of a Sips isotherm is maximised over K at
   `(r^(n/2) − 1)/(r^(n/2) + 1)`, with `r = f(65)/f(5.8) = 9.909` fixed by the protocol. It
   reduces to the pre-registered 0.518 at n = 1 and **rises with n**. **It is not violated**:
   all three measured structures fall *within* the Sips optimum at their own exponent, while
   two of the three *exceed* the n = 1 optimum. So the pre-registered bound failed for a
   diagnosable reason — it assumed n = 1 — and the generalisation that repairs it survives
   every isotherm I measured.

**What this bound does not do** is give a database-wide ceiling, because n is measured for three
structures and unknown for the other 108. It explains the failure and constrains the mechanism;
it does not by itself cap the database. The database-wide statement rests on §4.3.

### 4.3 The ceiling statement I actually defend

Two lines, neither of which needs a void fraction or an isotherm model.

1. **Combinatorial trade-off bound: 227.4.** `WC = N(65) − N(5.8)` is an identity between two
   measured quantities. Across the screen these are weakly coupled (corr = 0.159 overall), and
   that slack is where working capacity lives. Combining the highest N(65) measured anywhere
   with the lowest N(5.8) among above-median-N(65) structures gives **227.4** — a hypothetical
   material that adsorbs like the best at 65 bar and like the emptiest at 5.8 bar. No measured
   structure does both, so this is *an upper bound on the upper bound*. It sits **10% above the
   best measured value**. Independently, it lands within a fraction of a unit of Appendix A
   G1's calibrated 230 artifact threshold, which was derived from the charter's own calibration
   and not from my data.
2. **Frontier turnover, and the tail is not where the ceiling hides.** On the structures where a
   volume denominator is self-consistent, `WC/φ` falls monotonically from 437 to 119 across
   φ = 0.35 → 0.85 while φ itself rises; the product turns over at **φ = 0.50–0.55 with peak
   WC 207**. The database's maximum porosity is 0.813, it has been screened, and it delivers 97.
   **The unexplored ultra-porous tail is the opposite of where the maximum lives** — which is
   the opposite of the intuition I began the campaign with.
3. **Surrogate exhaustion (conditional, and weakest of the three).** Over 12,318 unscreened
   structures the GP expects **0.50** above the current best; the highest unscreened mean+2sd is
   **208.1**, and it belongs to `2021[Cu][sql]2[FSR]6` — a sibling of the leader itself.
   Independence overstates P(at least one), so the line errs conservative. It says where the
   *surrogate* believes the database ends, not where physics does. **I have queued the top five
   unscreened candidates directly**, so this line will be tested rather than trusted.

**Can it be exceeded?** By search within this database under this protocol: marginally at best,
by an amount consistent with 207 → ~227, and I have found no evidence of a qualitatively better
regime. By modification: **unresolved**, and I say so rather than guessing — the de-interpenetration
experiment is the test and it has not returned (§3, Defect 13). That arm now includes the
leader's own de-interpenetrated net, which a 2026-08-30 ruling confirmed is claimable rather than
gated out; **it is the one experiment in this campaign that could still overturn the ceiling
position**, because it changes the material rather than searching among fixed ones.

## 5. Uncertainty and limitations

- **G6 reproduction: see the machine-written block in §1, which is authoritative.** Appendix A
  G6 requires reproduction from archived inputs in a fresh run before filing. At the time this
  prose was written that pass was queued and running, and the number was provisional. The block
  is refreshed from the cluster independently of my session, so if this report was filed after my
  session ended, the block — not this sentence — states whether the Claim reproduced.
- **The screen is 111 of 12,499 structures (0.9%).** The ceiling claim leans on the surrogate to
  cover the rest, and the surrogate's credibility is one number, its LOO RMSE.
- **Monte-Carlo error is not the dominant uncertainty.** The ±0.38 on the leader is a block
  average over a converged run; it does not cover force-field error, which the G4(a) caveat
  addresses qualitatively and which I cannot quantify inside this protocol.
- **Three isotherms are three isotherms.** The Sips exponent is measured for three structures
  and assumed for none of the others. The repaired bound of §4.2 is therefore a statement about
  mechanism, not a database-wide cap.
- **The void-fraction descriptors are unreliable below φ ≈ 0.25.** This does not affect measured
  working capacities, which never use them, but it limits any analysis that divides by a volume.
- **The modification arm has produced no modified-structure result yet** (§3). Its absence is a
  gap in the ceiling argument's "can it be exceeded by modification" leg, and it is reported as
  a gap.
- **A modified structure below G3's density floor is being simulated, and it is claimable.**
  `2021[Cu][sql]2[ASR]6_DENET` — one net of the leader's 2-fold interpenetrated pair removed —
  lands at 0.179 g/cm³ against G3's 0.20 bound. I escalated whether G3 forbids the *simulation*
  or only the *claim*, acted meanwhile on the Appendix preamble ("gates constrain claims, not
  measurement"), and the ruling of 2026-08-30 went further than my reading: **G3's density floor
  filters as-deposited artifacts, and does not reach an agent-created, charge-balanced
  modification at all.** So the structure is neither killed nor excluded — G5 governs the
  modification, G4 governs the caveat, and if it beats the leader it can headline, subject to
  claim fidelity and G6 like any other number. The `killed` audit line is superseded on the
  record by an `audit_outcome: "correction"` line, and the construction, the charge-balance
  argument and the gate reasoning are logged in `AUDIT.jsonl` as the ruling requires.
- **Spend is the binding budget and it will end this campaign before the deadline does.**
  66.7% spent against 10.0% of compute, with ~6 days of calendar nominally remaining. Spend is
  charged on session context re-read per turn, so it measures my own wakefulness rather than
  cluster work. The endgame therefore runs unattended from the cluster, with hard cutovers that
  guarantee the G6 pass and the final analysis execute regardless of my session state.
- **Duplicate G3 audit lines** (72 kills recorded twice) are on the record and corrected in the
  narrative rather than deleted.

## 6. Self-assessment

**Confidence that `2021[Cu][sql]2[ASR]6` is the best structure in this database under this
protocol: moderate.** It leads the screen, its claim-grade number reproduces its screening
number to well inside one sigma, and the surrogate expects half a structure above it. The main
threat is its own sibling `2021[Cu][sql]2[FSR]6`, which the GP places at essentially the same
value and which is now queued.

**Confidence in the ceiling position (~207 measured, ~227 conceivable, no qualitatively better
regime): moderate, and better founded than it was.** Two of the three supporting lines need no
model and no denominator, and the third is explicitly conditional and being tested directly. The
pre-registered bound failed, and I regard having diagnosed *why* it failed — and shown that its
repaired form is unviolated — as stronger evidence than if it had never failed.

**What would change my mind:** a measured structure above 230 that survives a G1 audit; a
de-interpenetrated structure that substantially beats its pristine control, which would show
modification opens headroom that search does not; a region of descriptor space where `WC/φ`
stops declining with φ; or a GP retrained on 250+ points that puts substantial mass above 230.

**What would change my mind about the leader specifically:** any G6 non-reproduction, or a
protocol-compliance failure found in its archived output.

**Where I think this campaign is weakest:** the screen is under 1% of the database, and the
single biggest cause is an infrastructure fact rather than a scientific choice — no energy
grids, so every screened point cost a full GCMC pair. The second biggest is my own decision to
keep GCMC inside the scheduler under a 30-minute interactive cap on a pool shared sixteen ways.
Both are stated in §3 rather than absorbed into the ceiling argument as if the coverage were
adequate.
