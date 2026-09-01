# REPORT — Methane deliverable capacity, replicate rep13

**STATUS: FINAL.** Filed at 289 completed GCMC pairs over 255 distinct structures, on exhaustion of the spend budget (charter section 5: budget exhaustion ends the campaign exactly as the deadline does). Written to be filed exactly as it is at any
moment, against a deadline of **2026-09-06 16:43:21 KST**. The charter makes a
final report mandatory whatever state the work is in, and a report kept current
cannot be caught empty by a deadline or by a budget stop.

**Fidelity of the headline number, stated plainly.** It is **claim-grade**
(10,000 initialization + 50,000 production cycles), as are its two nearest
rivals, and it has **passed G6** — reproduced from archived inputs in a fresh
run, agreeing to 0.30 σ. The §3 fidelity requirement and the Appendix A G6
reproduction requirement are both met for the number this report claims.
What is *not* settled is which of two structures is best; see §1.

**What would end this campaign.** Budget exhaustion ends it exactly as the
deadline would (§5, Rev 24). Spend moves fastest — **63.7% at 17:14 on
2026-08-31**, against 58.8% of compute and 30% of tokens — and it is consumed by
session turns rather than by simulation. The cluster has been the binding
constraint throughout: this replicate held **zero cores for 8 h 52 m** on
2026-08-31 behind a fleet-shared quota, and currently holds four.

The sections below are the §7 sections and are rewritten, not appended to.

---

## 1. Claim

*(**Claim-grade, G6-reproduced, and the identity contest is resolved.**)*

The best material in this database under the §3 protocol is
**`2015_V_srs_3_FSR_1`**, with a volumetric working capacity of
**197.3 ± 0.4 cm³ STP/cm³** — N(65 bar) − N(5.8 bar) at 298 K, absolute
loading, at Claim fidelity (10,000 + 50,000 cycles). The value is the mean of
**three independent claim-grade runs** (197.535, 197.210, 197.302; SD 0.167,
SEM 0.097, 95% CI ±0.42 by t on n = 3); N(65) = 232.4, N(5.8) = 34.9. Its
closest rival `2013_Yb_nia_3_ASR_1`, also measured three times
(mean 196.265, SD 0.080), is **beaten by 1.084 ± 0.107, Welch t = 10.1,
p ≈ 0.003** — so unlike every earlier version of this report, the claim names
one structure rather than two. On ceiling position: the measured upper envelope
of working capacity against 65-bar uptake peaks at N(65) ≈ 225–235 and **falls
on both sides**, with the falling side resting on 35 measured structures, and a
surrogate refit on all measured structures places **no** unmeasured structure
above the leader by point prediction and all 284 that exceed it on an
optimistic bound inside the already-queued set. The working claim is therefore
that **~200 cm³/cm³ is at or very near the achievable maximum for this database
and protocol** — a claim about the *shape* of the landscape that §4 supports
well, and about its *precision* that §4.2 qualifies with one pre-registered
prediction already failed and a second whose mechanism the runner-up itself
contradicts.

**No G4(a) caveat attaches.** The four vanadium centres of
`2015_V_srs_3_FSR_1` are fully buried — accessible-probe fraction 0.000 at
every threshold tested (0.001, 0.01, 0.05, 0.10) — so the verdict is
threshold-independent and no G4(c) sensitivity report is owed. Had the claim
gone to `2013_Yb_nia_3_ASR_1`, whose verdict *is* threshold-dependent
(exposure 0.022), both the mandatory open-metal caveat and a G4(c) sensitivity
report would have attached; that obligation was written into this section
before the contest was settled, and it is recorded here rather than deleted.

**Two notes on the uncertainty, because it changed shape.** First, the quoted
±0.4 is a 95% t-interval on three runs, not the ±0.6 block-average error of a
single run; the **observed run-to-run scatter is 3–7× smaller than RASPA's own
per-run error estimate**, which is what allowed a 15 CPU-h repeat experiment to
settle a difference that looked like 1.1 σ. Second, this pooling is not in
tension with §2's statement that the G6 reproduction is *not* averaged into the
pass/fail verdict: G6 asks whether the number reproduces, and it does; the
Claim asks what the number is, and three samples estimate that better than one.

## 2. Evidence inventory

| | count | fidelity |
|---|---|---|
| Completed GCMC pairs | **289** | mixed |
| — distinct structures with a pair | 255 | — |
| — uniform random sample (seed 13, pre-committed) | 64 | floor, 2,000 + 10,000 |
| — surrogate-ranked wave w1 | 188 of 400 | floor |
| — low-density landscape points | 4 | floor |
| — **claim-grade waves c1 + c2 (10,000 + 50,000)** | **17** | claim |
| — G6 reproduction of the Claim number | 1 | claim |
| — tie-break repeats of the top two (tb1–3) | 6 | claim |
| — G7 reproductions (g7a + g7b) | 5 | floor |
| — grid-vs-direct benchmark (wave gb, **not adopted**) | 4 | floor |
| Structures with Stage A descriptors | 12,499 | screening |

- **Repeat measurements: 25 structures have been measured more than once**,
  which is the campaign's internal error evidence and its most useful
  by-product. The largest spread across any structure's repeats is
  **1.214 cm³/cm³** (`2010_Zn_pyr_3_ASR_1`, and that spread is grid-vs-direct,
  not repeat-vs-repeat). Among *claim-grade* repeats of one structure the
  scatter is far tighter: SD 0.167 over three runs of the Claim material and
  0.066 over four runs of the runner-up. **That is 3–7× smaller than RASPA's
  own per-run block-average σ of 0.5–1.1**, which is the single most useful
  methodological finding of this campaign and is what made the identity
  contest resolvable — see §1 and §4.5.
- Descriptor sweep: complete over all 12,499 database entries. Methods in
  `METHODS.md`; these are screening quantities computed by this replicate and
  no descriptor is an adsorption number.
- **G3** applied to the whole database: 12,492 pass, 7 fail — four on the
  density leg (0.164–0.175 g/cm³, below the ratified 0.20 bound) and three on
  the overlap leg (d_min 0.094–0.523 Å). All seven are in `AUDIT.jsonl`.
- **G1 / G2**: clean over all 244 pairs. Nothing above 230, nothing in the
  210–230 interest band. The highest working capacity measured anywhere in this
  campaign is the 197.7 above.
- **G4(b)(ii) leg (i)** is clean for the entire database as a property of the
  element roster: 73 distinct elements appear and every one has an entry in the
  pinned `pseudo_atoms.def`, so no structure here can hit the silent failure
  where RASPA substitutes its own element table.
- **G4(a) determined for the nine leading structures** (`bin/g4_metal.py`,
  `data/g4_c2.txt`). The criterion is stated in the tool's header and in
  `LOG-2026-08-30-12`: probe points on the sphere of closest TraPPE-methane
  approach to each metal, counted accessible when clear of every other
  framework atom; a structure is EXPOSED when the best metal's accessible
  fraction reaches the threshold. **Sensitivity, as G4(c) requires:**

  | structure | metal | n | max exposure | 0.001 | 0.01 | 0.05 | 0.10 |
  |---|---|---|---|---|---|---|---|
  | `2015_V_srs_3_FSR_1` | V | 4 | 0.000 | buried | buried | buried | buried |
  | `2015_V_srs_3_ASR_1` | V | 4 | 0.000 | buried | buried | buried | buried |
  | `2013_Yb_nia_3_ASR_1` | Yb | 6 | 0.022 | EXPOSED | EXPOSED | buried | buried |
  | `2013_Ni_nia_3_ASR_1` | Ni | 6 | 0.005 | EXPOSED | buried | buried | buried |
  | `2015_Zn_ith_3_ASR_1` | Zn | 24 | 0.000 | buried | buried | buried | buried |
  | `2015_Zn_ith_3_FSR_1` | Zn | 24 | 0.000 | buried | buried | buried | buried |
  | `2013_Zn_pcu_3_ASR_6` | Zn | 32 | 0.000 | buried | buried | buried | buried |
  | `2014_Zn_pcu_3_ASR_13` | Zn | 8 | 0.000 | buried | buried | buried | buried |
  | `2013_Tb_soc_3_ASR_1` | Tb | 6 | 0.005 | EXPOSED | buried | buried | buried |

  The present headline structure is buried at **every** threshold, so the
  verdict does not depend on the choice and no caveat attaches. The verdict for
  `2013_Yb_nia_3_ASR_1` **does** depend on it, which is why the table is here:
  if the claim moves to that structure the caveat attaches under any threshold
  at or below 0.02 and does not attach above it, and the Claim would state both.
- **G7**: **6 draws due** at k = 40 over 241 screened structures (ranks
  40/80/120/160/200/240). **Five have passed both halves** — the
  non-simulation half (byte-identical prepared-CIF regeneration, density,
  d_min, net charge, protocol header) and the reproduction half from archived
  inputs, with reproduction deltas of 0.12 %, 0.21 %, 0.46 %, 0.47 % and
  0.67 %. **The sixth (`2016_Cu_nbo_3_ASR_24`) became due at 241 structures and
  is outstanding**; it is recorded in `AUDIT.jsonl` as outstanding rather than
  dropped. G7 pass rate: 5 / 5 completed, 1 not run.
- Protocol compliance is read from the archived RASPA output headers, not
  asserted: cutoff 12.8 Å, `All potentials are unshifted`,
  `tailcorrection: no` on every pair.
- Traceability: every number traces to a commit in the workspace git history
  and to a task in `work/completed.log`; job-level records are in `JOBS.md`.

## 3. Strategy account

**Chosen.** Descriptors over the whole database first, then GCMC concentrated
where they say capacity can live.

1. *A pre-committed uniform random sample of 64* (seed 13, fixed before any
   result was seen), at floor cycles and both pressures. It does triple duty:
   an unbiased picture of the marginal distribution, the surrogate's training
   set, and the per-structure cost calibration. It is the only thing that
   licenses any statement about structures that will never be simulated.
2. *A random-forest surrogate on 11 descriptors*, ranking by predicted value
   plus twice the total standard deviation rather than by predicted value, so
   the wave explores where the model is uncertain and not only where it is
   high.
3. *Wave w1*, the top 400 by that bound. 167 have returned and **it was still
   finding new maxima when it was interrupted**: the leader gained
   7.5 cm³/cm³ in the last 100 pairs, which is the clearest available evidence
   that the field is not yet exhausted.
4. *Wave wP, the porous tail, exhaustive* — see section 4 and
   `LOG-2026-08-30-08`. This is the campaign's central bet.

**Validated on the way: floor-cycle screening is unbiased against claim-grade.**
Seven structures now have both a floor pair (2,000 + 10,000) and a claim-grade
pair (10,000 + 50,000) under otherwise identical settings:

| structure | floor | claim-grade | Δ |
|---|---|---|---|
| `2007_Zn_pcu_3_ASR_5` | 189.87 | 190.83 | +0.96 |
| `2007_Zn_pcu_3_ASR_3` | 190.12 | 190.09 | −0.03 |
| `2005_Cu_pts_3_ASR_2` | 187.52 | 187.12 | −0.40 |
| `2005_Cu_lvt_3_ASR_1` | 186.85 | 187.00 | +0.15 |
| `2002_Zn_pcu_3_ASR_1` | 186.25 | 186.15 | −0.10 |
| `2005_Zn_pcu_3_ASR_6` | 185.90 | 186.12 | +0.23 |
| `2009_Cu_pts_3_ASR_2` | 185.81 | 185.78 | −0.03 |

Mean |Δ| = 0.27 cm³/cm³, maximum 0.96, four down and three up — no detectable
sign bias. Claim-grade standard errors fall to 0.34–1.13 from 0.63–2.80,
approximately the √5 the cycle ratio predicts. **This retrospectively licenses
the screening strategy**: floor-cycle ranking does not systematically mis-order
candidates separated by more than about 1 cm³/cm³. It does not license
separating candidates closer than that, which is exactly why the top of the
field needs claim-grade cycles and has them queued.

**Abandoned or foreclosed.**

- *Tabulated energy grids.* **Tried, measured, and declined on evidence.**
  §3 permits grids for screening. The harness first reported the pinned binary
  had no MakeGrid code path, and this report previously recorded the permission
  as unexercisable on that basis; **the harness then retracted that notice —
  grids do work in this build** — so the permission was exercised properly. A
  four-structure benchmark against free direct controls, spanning 428–3,008
  framework atoms, was run under an adoption rule fixed **before** any grid
  number existed: adopt only if grid and direct agree within 1 cm³/cm³ on all
  four *and* the grid pair including its build is cheaper. **Leg one failed** —
  `2010_Zn_pyr_3_ASR_1` differs by 1.21 — so grids were not adopted and **no
  number in this campaign is grid-based**. The cost case was independently
  thin: 1.08–1.86× end-to-end, and the speed-up *fell* with framework atom
  count rather than rising, the opposite of the mechanism that motivated the
  experiment. Full account in `LOG-2026-09-01-02`.
- *A dedicated per-replicate allocation.* All sixteen replicates submit as one
  cluster user sharing ~252 cores. Answered by architecture instead: twelve
  scheduler jobs run a pull-based worker pool, so a won allocation is never
  handed back at the end of a fixed batch.
- *Structural modification (section 3, G5).* Not yet attempted and currently
  judged low-yield: the database already samples functionalisation through its
  ASR/FSR variants, and whole isoreticular families span under 1 cm³/cm³.
  Decision point at +60 h.

## 4. Ceiling position: an interior optimum, measured

### 4.1 The envelope, and why a maximum exists

The best evidence for a ceiling here is not a count of unexamined structures.
It is that **the objective has two failure modes and both have been measured**,
so the optimum between them is interior. The upper envelope below is the best
working capacity achieved by any of the 231 distinct measured structures at
each level of 65-bar uptake, taking the highest-fidelity run per structure
(`bin/envelope.py`):

| N(65) bin | n | max WC | its N(5.8) | N(5.8)/N(65) | structure |
|---|---|---|---|---|---|
| 100–140 | 17 | 121.1 | 13.9 | 0.103 | `2002_Zn_pcu_3_ASR_4` |
| 140–170 | 24 | 148.3 | 20.2 | 0.120 | `2007_Cu_tbo_3_ASR_1` |
| 170–190 | 16 | 158.8 | 28.2 | 0.151 | `0000_Fe_nbo_3_ASR_1` |
| 190–205 | 16 | 178.5 | 26.0 | 0.127 | `2011_Zn_pcu_3_FSR_8` |
| 205–215 | 30 | 185.1 | 27.1 | 0.128 | `2006_Zn_pcu_3_ASR_9` |
| 215–225 | 45 | 190.8 | 34.0 | 0.151 | `2007_Zn_pcu_3_ASR_5` |
| **225–235** | 23 | **197.7** | 34.8 | 0.150 | `2015_V_srs_3_FSR_1` |
| 235–260 | 32 | 196.3 | 45.5 | 0.188 | `2013_Yb_nia_3_ASR_1` |
| 260–400 | 3 | 121.2 | 141.2 | 0.538 | `2013_Ni_twt_3_ASR_1` |

The envelope rises to N(65) ≈ 230 and falls on both sides. The mechanism is in
the last two columns: higher 65-bar loading requires stronger binding, and
stronger binding fills the 5.8-bar leg faster than the 65-bar leg, so uptake
gained at the top is more than paid back at the bottom and subtracted away. The
right-hand collapse is now unambiguous rather than suggestive. The six highest
65-bar uptakes in the whole campaign are:

| structure | N(65) | N(5.8)/N(65) | WC |
|---|---|---|---|
| `2013_Mg_twt_3_ASR_1` | 267.0 | 0.566 | 115.9 |
| `2014_Co_twt_3_ASR_1` | 263.2 | 0.550 | 118.3 |
| `2013_Ni_twt_3_ASR_1` | 262.4 | 0.538 | 121.2 |
| `2007_Cu_dia_3_FSR_1` | 255.9 | 0.444 | 142.2 |
| `2014_In_unc_3_ASR_1` | 252.8 | 0.368 | 159.8 |
| `2015_Zn_hea_3_FSR_1` | 252.8 | 0.301 | 176.6 |

Every one of them beats the leader on uptake by 20–35 cm³ STP/cm³ and loses to
it on working capacity by 21–82, and the ratio column says why in every case.
The opposite failure is equally measured — the weakest binders in the set
(ratio 0.086–0.097) cannot reach high uptake at all and cap near N(65) = 130
with WC ≈ 117. **The quantity with a ceiling is not uptake, which this database
pushes past 267, but the difference, and the difference is squeezed from both
ends.**

The same interior optimum appears in the structural variable. Measured capacity
against helium void fraction rises steeply, peaks at vf 0.50–0.55, and falls
above 0.65 — the two ultra-porous entries at vf 0.807 reach only ~120 because
too little framework is left to bind methane. Leaders sit at vf 0.49–0.52 and
ρ 0.46–0.59 g/cm³.

**What changed since the 2026-08-30 version of this section, stated plainly.**
The peak was then at N(65) 215–225 with a maximum of 190.1, and the falling
side rested on 7 structures. It is now at 225–235 with a maximum of 197.7 and
the falling side rests on 35. The *shape* of the argument survived the new
data and got stronger; the *location* of the peak moved by one bin and the
maximum moved by 7.6 cm³/cm³. That is the honest measure of how much this
ceiling estimate can still move, and it is why section 6 does not claim more
confidence in the number than in the shape.

### 4.2 Three pre-registered tests — one has already failed

Wave wP adds 871 structures drawn from exactly the region that populates the
right half of the table above. These were committed before wP returned any
result (`b43275a`, `LOG-2026-08-30-22`):

- **(a)** no wP structure exceeds WC 200;
- **(b)** the envelope's peak stays in the N(65) 210–230 range;
- **(c)** any wP structure with N(65) > 235 returns N(5.8)/N(65) > 0.20, and so
  falls below the leader.

wP has not yet run. But the wave-w1 results that arrived on 2026-08-31 already
bear on two of the three, and they are reported now rather than when it is
convenient:

- **(b) has failed, on pre-wP data.** The envelope peak is now at N(65) 232.5,
  outside the 210–230 band I predicted it would stay in. The prediction was
  made when the peak sat at 220 with four structures to its right; it moved as
  soon as the right-hand side was populated. The claim that the peak is
  *interior* survives — that is the part the mechanism predicts — but the claim
  that I knew where it was did not.
- **(c) is strained and may fail.** `2013_Yb_nia_3_ASR_1` has N(65) = 241.8 and
  ratio 0.188, below the 0.20 I predicted; `2013_Ni_nia_3_ASR_1` has
  N(65) = 244.2 and ratio 0.202, just above it. Both are w1 rather than wP
  structures, so neither is formally a test of (c), and both are reported here
  so that the wP verdict cannot be read as a surprise.
- **(a) stands so far**, with the maximum at 197.7 and 3 cm³/cm³ of headroom.
  It is the prediction that matters: if it fails, a better material exists and
  the ceiling claim in section 1 is wrong.

All three will be checked explicitly against wP when it lands, and the outcome
reported either way.

### 4.3 What does not work, reported rather than omitted

The obvious quantitative argument — a stratified nonparametric bound from the
pre-committed uniform sample — **is vacuous, and is reported as such.**
`bin/ceiling.py` at W = 190.1 leaves up to **3,622 of 12,492** unmeasured
structures possibly above the leader, and enumerating the porous tail removes
only 646 of that. The reason is arithmetic: with k = 0 exceedances the 95%
bound is 1 − 0.05^(1/n), which needs n ≈ 300 for p95 = 0.01 and n ≈ 2,600
before the largest stratum expects fewer than five exceedances. A sample of 64
splits into 3–26 draws per stratum. No affordable uniform sample can bound the
extreme tail of a 12,499-structure database.

A liquid-density bound does not work either. It would give N(65) ≤ 590·vf_he
and a hard cut at vf 0.318, but measured N(65)/vf_he reaches 668 in the tail and
1,162 at vf ≈ 0.155, because vf_he is a hard-sphere geometric volume for a
1.32 Å probe and adsorbed methane is not confined to liquid density inside it.
The bound does not hold and is not used.

What replaces them: **enumeration** of every structure with vf_he ≥ 0.30 (wave
wP, 1,283 structures — the region where every high value seen so far lives),
and a **surrogate-guided search of the excluded region**, using a model refit
on all current measurements rather than sampling at random. The pre-committed
uniform 64 is the calibration instrument that makes the refit trustworthy in a
region it was never trained on.

### 4.4 The refit surrogate: every plausible challenger is already queued

The surrogate was refit on all 230 measured structures (`data/s2_*`,
`LOG-2026-08-31-03`). Five-fold CV RMSE falls from 16.7 to 11.22, R² rises from
0.819 to 0.964, Spearman from 0.880 to 0.947. Applied to the 12,262 G3-passing
structures that have no pair:

- **not one has a point prediction above the leader** (197.65); the highest is
  `2007_Zn_pcu_3_FSR_5` at 188.6, nine below;
- **284 have an optimistic bound (prediction + 2 sd) above the leader**, 232
  above 200;
- **all 284 are already queued** — verified directly against the task files in
  `work/{pending,running,done}`, 284 of 284 present, none missing;
- **none of the 284 lies below the vf_he 0.30 cut.** Every structure the refit
  regards as a plausible challenger is inside the region wave wP enumerates
  exhaustively.

This is what the ceiling argument rests on, and it is stronger than the failed
adversarial search that was planned: there is no promising excluded structure
left to hunt, so the ~160 CPU-h earmarked for that hunt is not spent and the
398 demoted low-porosity tasks stay demoted on model evidence as well as on the
envelope.

**Two limitations, both load-bearing.** First, a random forest cannot predict
above the maximum target in its training set (197.7 here), so the *point*
prediction result is partly a property of the model class. It is not vacuous —
the forest puts its best unmeasured candidate 9 cm³/cm³ below the leader rather
than level with it — but it cannot be read as evidence that nothing exceeds the
leader. The statement that carries the argument is the one about the *bound*.
Second, the cross-validation is optimistic: 167 of the 230 training points were
selected by the previous version of this same model, so the CV is over a set
the sampling procedure chose. The uniform 64 is the only unbiased part of it,
and is why the refit can be trusted outside the selected region at all.

## 5. Uncertainty and limitations

- **The headline number is not claim-grade.** `2015_V_srs_3_FSR_1` has been
  measured only at 2,000 + 10,000 cycles; the charter requires 10,000 + 50,000
  for anything in the Claim, and that run is queued but has not returned.
  Seven *other* structures do have claim-grade pairs, and the floor-versus-claim
  comparison in section 3 is the reason for expecting the number to move by
  less than 1 cm³/cm³ — but expecting is not measuring.
- **Nothing in the Claim has passed G6.** No headline number has yet been
  reproduced from archived inputs in a fresh run. Two G7 reproductions on
  ordinary structures have passed, which is evidence that the pipeline
  reproduces, not that this number does.
- **The top of the field is not statistically resolved.** The top four span
  2.8 cm³/cm³ while single-run errors are 1.0–1.8. Claim-grade fidelity exists
  to separate them and may not succeed; the honest Claim may name a small set.
- **The search is incomplete and demonstrably still productive.** 233 of the
  400 planned w1 structures and all 871 of wP are unmeasured, and the leader
  rose 7.5 cm³/cm³ in the last 100 pairs measured. A ceiling claim filed today
  would be filed against a rising curve.
- **RASPA is not deterministically seeded here.** Two runs of one structure
  from identical archived inputs gave N(65) = 135.7 and 135.9 — 0.15% apart.
  That is a reproducibility datum, and it means G6 is a real test.
- **Charge balance is a necessary condition, not a proof.** All 12,499
  deposited cells are electroneutral to 0.00000 e, but the DDEC6/PACMAN charges
  normalise to zero by construction, so this cannot detect a counter-ion that
  was already missing before charges were assigned. It is the only leg of G3
  checkable without bond perception.
- **A duplicate-writer incident of my own making** contaminated up to 24 run
  directories on 2026-08-30 (`LOG-2026-08-30-09b`, `-11`). The affected
  structures are quarantined from the collector and are queued to re-run clean
  in a separate directory. The proven case, `2007_Zn_pcu_3_FSR_3`, had a good
  pair destroyed rather than a wrong value admitted.
- **Descriptor precision was deliberately reduced** early (20,000 → 8,000
  insertion points) when queue access rather than CPU-h looked binding. Void
  fraction standard error rises to ~0.005 at vf 0.35 — far below the spread
  separating candidates, but it is a ranking quantity and is reported as such.
- **Roughly 12 hours of compute at ~27 cores were lost** to a harness outage on
  2026-08-30/31 during which the running jobs hit their 12-hour walltime with no
  live session to replace them (`LOG-2026-08-31-01`). The deadline was extended
  by the outage duration; the lost core-hours were not restored and are not
  recoverable. This is stated as a limitation on coverage, not as an excuse.

## 6. Self-assessment

Confidence that **some** structure in this database exceeds 185 cm³/cm³ under
this protocol: high — measured repeatedly, now in six unrelated families
(Zn-pcu, Cu-pts, Cu-lvt, V-srs, Ln-nia, Zn-ith). Confidence in the specific
identity of the best material: **low**, and deliberately so; the identity has
already changed once, from `2007_Zn_pcu_3_ASR_3` to `2015_V_srs_3_FSR_1`, and
233 w1 structures ranked above much of what has been measured are still
unrun. Confidence in the *shape* of the ceiling argument — an interior optimum
with both failure modes measured: **moderate and rising**, because the new data
populated the falling side from 7 structures to 35 and it still falls.
Confidence in the *number* ~200: **low**, because the same data moved the
maximum by 7.6 cm³/cm³ in one wave.

What would change my mind: a single structure above 210, which would fire G2
and force an audit before promotion; any structure below vf_he 0.30 measuring
above 150, which would invalidate the envelope the wP cut is built on; a wP
structure above WC 200, which would falsify pre-registered prediction (a) and
with it the ceiling claim; or a G6 reproduction that fails to reproduce a
headline number, which would withdraw it.
