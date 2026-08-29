# FINAL REPORT — Methane Deliverable Capacity Campaign
**Replicate s01 · smoke phase · filed 2026-08-28 · charter §7 format**

*Working capacity ≡ N(65 bar) − N(5.8 bar) at 298 K, absolute, volumetric (cm³ STP/cm³),
under the §3 protocol: RASPA 2.0.37, UFF/TraPPE united-atom methane, rigid framework,
chargeless, 12.8 Å cutoff, unshifted, tail corrections off.*

---

## 1. Claim

**`2023[Cu][ctn]3[FSR]1__stripH` — the methyl-stripped derivative of database entry
`2023[Cu][ctn]3[FSR]1` — delivers 187.75 ± 0.42 cm³/cm³**, measured at Claim-grade cycles
(10,000 + 50,000) and reproduced from archived inputs in a fresh independent run per G6
(187.853 and 187.653, differing by 0.199). Its unmodified parent gives **177.54 ± 0.39** and is
the best G4-admissible structure in the database: an exhaustive screen of all 1,731 entries
(1,230 distinct structures) followed by floor-grade confirmation of the top candidates places
the next distinct admissible structure at 168.01, 9.5 cm³/cm³ below it. **This is close to the
achievable maximum, and the binding constraint is the protocol rather than the materials** —
37 of the top 40 structures by screening value carry exposed metal and are G4-inadmissible,
the best of them reaching 206.37; higher capacity exists in this database but sits where
UFF/TraPPE is not entitled to describe it. This claim's identity depends on one stated
threshold choice (§4): a G4 reachability cut of 4.2 Å rather than 3.8 Å.

## 2. Evidence inventory

### 2.1 Simulations — 304.61 of 340 CPU-h, 3,620 GCMC runs, zero failures

| batch | purpose | cycles | structures | runs | CPU-h |
|---|---|---|---|---|---|
| b0 | cost-model benchmark | 500+2,000 | 8 | 16 | 1.56 |
| b2 | cycle ladder, scout | 150+600 | 8 | 16 | 0.45 |
| b1 | cycle ladder, floor | 2,000+10,000 | 8 | 16 | 8.54 |
| **s1** | **exhaustive screen, all 1,731** | 150+600 | **1,731** | **3,462** | **162.98** |
| eq | equilibration-bias test, porous top | 2,000+10,000 | 2 | 4 | 6.44 |
| g7 | G7 random audits | 150+600 | 27 | 54 | 1.66 |
| s2 | promotion / ceiling gap / stratified fidelity | 2,000+10,000 | 19 | 38 | 44.05 |
| mod | modification + G5 matched control | 2,000+10,000 | 2 | 4 | 7.00 |
| mod2 | modification falsification test | 2,000+10,000 | 1 | 2 | 0.42 |
| **s3** | **Claim-grade parent + G6 reproduction** | 10,000+50,000 | 1 | 4 | 37.09 |
| **s4** | **Claim-grade finalist + G6 reproduction** | 10,000+50,000 | 1 | 4 | 30.30 |
| — | descriptor / gate passes, all 1,731 | — | 1,731 | — | 4.11 |

Gate events: `AUDIT.jsonl`, 688 lines — 619 G4 exposed-metal kills, 12 G3 overlap kills,
27 G7 selections with 27 reproduction passes, 2 G6 finalist reproduction passes, 1 correction.
Job ledger `JOBS.md`; narrative `LOG.md` (28 numbered entries); 30 commits.

### 2.2 The numbers that matter

| structure | cycles | N(5.8) | N(65) | **WC** | G4 |
|---|---|---|---|---|---|
| **`2023[Cu][ctn]3[FSR]1__stripH`** | **Claim** | 33.725 | 221.478 | **187.75 ± 0.42** | admissible |
| `2023[Cu][ctn]3[FSR]1` (parent, G5 control) | **Claim** | 45.542 | 223.080 | **177.54 ± 0.39** | admissible |
| `2021[Th][fcu]3[FSR]1` (next distinct admissible) | floor | — | — | 168.01 | admissible |
| `2021[Cu][sql]2[FSR]6` (best overall) | floor | 36.905 | 243.279 | 206.37 ± 1.00 | **inadmissible** |
| `2021[Al][nan]3[ASR]24` | floor | — | — | 195.41 | **inadmissible** |

### 2.3 Validation

1. **Toolchain verified by content, not assumed.** All three UFF SHA-256s reproduce the §3
   table; `RASPA 2.0.37`. Output headers confirm the settings reached the engine:
   `CutOff VDW : 12.800000`, `All potentials are unshifted`, `tailcorrection: no` on every pair.
2. **Screen→floor fidelity, stratified** (S2 + ladder, 31 paired structures). In the band that
   decides the claim (screen 150–250, n=12): **bias −0.26, σ 1.33**. Across all bands the screen
   is unbiased; scatter is worst at low WC (band 0–50: σ 4.36), where it cannot affect a ceiling.
3. **Equilibration-bias test at the porous top** — the failure mode that could have invalidated
   the screen. `2021[Cu][sql]2[FSR]6` scout 207.689 → floor 206.374 (Δ −1.32);
   `2023[Cu][ctn]3[FSR]1` scout 177.763 → floor 177.689 (Δ −0.07). No bias where it matters.
4. **499 independent replicate pairs** from exact duplicates in the database: mean **+0.073**
   (unbiased), per-run **σ 2.175**, max deviation 11.46.
5. **G7 random audits: 27/27 reproduced**, mean +0.222, per-run **σ 3.112**. This is the looser
   of the two independent σ estimates and is the one carried into the ceiling argument.
6. **G6 finalist reproduction**: both Claim numbers reproduced from archived inputs in fresh
   clock-seeded runs — parent 177.531/177.545 (Δ 0.015), finalist 187.853/187.653 (Δ 0.199).
7. **G4 detector validated against chemistry it does not know**: on 657 matched ASR/FSR pairs,
   133 flag the ASR (coordinated-solvent-removed) member only, against **6** the other way.
8. **RASPA's block σ overstates true scatter ≈3×** (median 6.53 vs measured 2.18). Reported
   uncertainties here are deliberately the conservative block-propagated ones.
9. **No trapped guest molecules** in any leader (periodic connected-component analysis).

## 3. Strategy account

**Chosen: narrow on cycles, not on structures.** All 1,731 entries were screened at 150+600
cycles and promoted upward, rather than screening a filtered subset at full cycles. The
decisive measurement: **cost concentrates in exactly the structures worth screening** — the top
5% by porosity carry 55% of screening cost, the cheapest 50% carry 15%. A porosity-filtered
screen would have saved ~15% of compute while destroying the exhaustiveness a ceiling claim
requires. Exhaustive was nearly free.

**Rejected on measurement: energy grids.** §3 permits them, so one was built and timed: 189
CPU-s and 85 MB per structure at 0.1 Å, against ~300 CPU-s for the whole two-pressure screening
run it was meant to accelerate. Generation cost scales ~V², so grids are least affordable
exactly where they would help most. No grid-based number exists in this campaign.

**Foreclosed: Widom-helium void fractions.** The pinned UFF set defines 91 pseudo-atoms and
none is helium, so G3's helium leg cannot be discharged the usual way without editing a
hash-pinned file. Replaced with a geometric He-probe void fraction using the protocol's own
LJ sigmas.

**The modification, predicted before it was run.** The completed screen located a volumetric
optimum at vf_ch4 ≈ 0.32–0.40, arising because N(5.8) falls monotonically with porosity while
N(65) turns over near 0.25–0.32. The finalist's parent sat *below* the optimum at 0.299.
Stripping its 24 methyl groups — charge-neutral by construction, since methyl and hydrogen are
both neutral monovalent substituents on carbon — was predicted in a committed log entry to
raise capacity, and did: **+9.92 at floor, +10.21 at Claim grade**. The mechanism is visible in
the split: N(5.8) fell 11.8 while N(65) fell only 1.6, so the gain is almost entirely *not
stranding* methane below the discharge pressure.

**The falsification test.** Confirming a prediction on one structure is weak evidence, so the
account was tested where it predicts the *opposite* sign. Of the other top admissible
candidates only `2022[U][srs]3[FSR]1` has strippable methyls, and it sits at vf_ch4 = 0.451 —
*above* the optimum. "Stripping bulk always helps" predicts a gain; the interior-optimum
account predicts a loss. Prediction recorded before running. **Result: −10.20 cm³/cm³** —
nearly equal and opposite to the +9.92 gain on the sub-optimal structure.

| structure | vf_ch4 | vs optimum | Δ from stripping |
|---|---|---|---|
| `2023[Cu][ctn]3[FSR]1` | 0.299 | below | **+9.92** |
| `2022[U][srs]3[FSR]1` | 0.451 | above | **−10.20** |

**Abandoned:** nothing else was begun and dropped.

## 4. Uncertainty and limitations

- **The finalist is a computational derivative, not a synthesised material.** §1 and §3 permit
  modified candidates and its preparation is fully reproducible (`bin/modify.py`), but nobody
  has made it. The best *existing* material this campaign validated is its parent at 177.54.
- **The parent's formal charge cannot be established from coordinates.** `2023[Cu][ctn]3` is a
  tetrahedral CuS4 framework (Cu–S 2.32 Å) of C₁₅H₁₈N₉S₃ linkers; neutral thione versus anionic
  thiolate S donors decides whether counter-ions are required, and the shipped DDEC6 charges
  cannot arbitrate because PACMAN normalises them to zero net by construction. G3's
  charge-balance leg is discharged by provenance for unmodified entries. **The modification
  sidesteps this**: methyl→hydrogen changes no formal charge whatever the parent's is.
- **The G4 threshold is mine, and the answer turns on one leg of it.** "Exposed metal atoms"
  carries no numeric criterion; I used θ_open ≥ 60° with a methane centre reaching ≤ 4.2 Å.
  The answer is stable against the angular leg and against *tightening* (θ≥75°/d≤4.2 and
  θ≥55°/d≤4.6 both leave the leader unchanged), but **relaxing the reachability cut to 3.8 Å
  readmits `2021[Al][nan]3[ASR]24` at 195.41, which would displace this claim entirely.**
  I checked the chemistry rather than defending the number: that structure's Al sites are AlO6
  *and* **AlO5 — five-coordinate**, with a methane centre reaching 4.0 Å against a UFF
  σ_mix(Al,CH4) of 3.87 Å. Al(III) nodes are octahedral, so a five-coordinate Al with an
  accessible vacancy is a real open metal site created by ASR desolvation, and the database
  holds no FSR counterpart with the sixth ligand retained. A 3.8 Å cut would admit structures
  whose strongest sites are open metal centres modelled by dispersion alone — precisely what G4
  exists to forbid. The 4.2 Å cut is therefore defensible on chemistry, **but the claim's
  identity does depend on it**, and an assessor who disagreed with that cut would get a
  different answer. The finalist itself is unaffected under every setting tested: its Cu is
  tetrahedral CuS4, shielded by its own linkers, unreachable at any distance.
- **Screening values are sub-floor and are never reported as measurements** — they rank only.
  Every number above comes from floor cycles or Claim cycles.
- **The ceiling rests on a Gaussian tail assumption beyond ~5σ.** The largest deviation actually
  observed across 499 independent pairs is 11.46; further out the tail is unverified. The
  margin that matters is 177.54 → 168.01 = 9.53 at σ ≈ 1.33, i.e. ~7σ, and every admissible
  structure not floor-graded screened below 151 (>19σ away).
- **The database is 1,230 distinct structures, not 1,731** — 501 redundant copies, mostly
  ASR/FSR pairs whose parent had no coordinated solvent to remove.
- **"65 bar" is an imposed fugacity of 5.674 MPa** (Peng–Robinson coefficient 0.873 from the
  pinned methane definition) — inherited from the toolchain, shared with the reference set.
- **Not verified**: absolute accuracy of UFF/TraPPE against experiment (out of scope — §3 *is*
  the definition of correctness here); framework flexibility (rigid by §3); anything outside
  the provided database.
- **Infrastructure**: two network outages (~10 h and ~23 h) cost wall-clock but no results;
  filed retroactively as `[ESC: infra]` because the charter's escalation channel is a file
  inside the workspace the outage made unreachable.

## 5. Self-assessment

**Confident** in the screen: exhaustive over all 1,731 entries, unbiased, reproducible to
2–3 cm³/cm³ per run, established three independent ways (cycle ladder, 499 duplicate pairs,
27 random audits). Confident in the two Claim numbers: reproduced to 0.015 and 0.199 cm³/cm³
across independent clock-seeded runs, with deliberately conservative error bars.

**Confident that the ceiling is protocol-set rather than materials-set.** The 92%-vs-36%
concentration of exposed metal at the top of the leaderboard is too large to be an artifact of
my threshold, and it has a clean chemical cause: the desolvation that opens the pore is what
uncoordinates the metal.

**Confident in the modification mechanism**, because it survived a test designed to break it.
The +9.92 / −10.20 symmetry either side of the measured optimum is what the interior-optimum
account predicts and what "stripping bulk always helps" forbids.

**Least confident** in the claim that no *unmodified* admissible structure beats 177.54. The
screen is exhaustive and the floor-grade margin over the runner-up is ~7σ, but that rests on
the screen's error being Gaussian in a tail I have measured only to ~5σ, and on a G4 threshold
I chose.

**What would change my mind:** (i) a reasoned case that the G4 reachability cut belongs at
3.8 Å rather than 4.2 Å — this is the single assumption the claim's identity rests on, and it
would replace the answer with `2021[Al][nan]3[ASR]24` at 195.41; abandoning G4 entirely would
move it to 206.37 and make the ceiling argument moot; (ii) a floor-grade rerun putting any structure the screen placed below 168
above 177.5, which would mean the screen has a failure mode none of my three error estimates
detected; (iii) a charge-balance analysis showing `2023[Cu][ctn]3` requires counter-ions that
the CIF omits, which would invalidate both the parent and the derivative under G3.
