# REFERENCE SCREEN — EXECUTION PLAN — **SEALED**
*(Sealed 2026-08-29 by PI ruling. Executes post-collection only. No cycle count, stage
definition, sample size or decision rule in this document changes after this line.)*

**Rulings applied at seal:** Δ is the sealed estimator derived from Stage 0, not a number fixed in
advance; **Stage 0 exists and is drawn independently of Stage 3**; Stage 2 runs **2 independent
seeds** per promoted structure; **the concavity prune and the Langmuir pre-filter are withdrawn**,
with the evaluation retained as Appendix A — evaluated, not activated; the cycle-convergence
analysis (`prereg/convergence_analysis_2026-08-29.md`) is filed as **the floor definition's freezing
record**; cycle tiers unchanged at 2,000 + 10,000 (floor) and 10,000 + 50,000 (claim); concurrency
ceiling revised to **480** post-collection.

The reference screen produces the **independent capacity landscape** the leaderboard derives from:
the number each replicate's claim is scored against, computed by the harness under the same pinned
protocol, with no knowledge of what any replicate did.

---

## 0. The finding that changes the design, stated first

**Δ cannot be pre-registered as a number, because the data to derive it does not exist.**

The ruling specifies Δ *"derived from the measured floor-to-claim error model (smoke archive, twin
pairs, rep-gate data)."* Bei searched all 1,805 runs in the smoke archive carrying cycle metadata.
What exists:

| cycles (init + prod) | grade | runs |
|---|---|---:|
| 150 + 600 | scout | 1,766 |
| 2,000 + 10,000 | **floor** | 30 |
| 500 + 2,000 | triage | 7 |
| 10,000 + 50,000 | **claim** | **2** |

**Structures with both a floor and a claim value: two — and they are the same framework**
(`2023[Cu][ctn]3[FSR]1` and its stripped-hydrogen modification). Their differences are
**−0.10 %** and **+0.06 %**. s02 states the position outright in its own log: *"no run at
10,000 + 50,000 exists, so no number in this campaign is claim-grade under §3."*

Two points on one framework cannot support a promotion margin for 12,499 structures. **Twin pairs
do not fill the gap either**: an ASR/FSR twin run twice at the same fidelity measures run-to-run
noise, not the floor→claim shift, and under the chargeless protocol the twins are the same
structure. The rep-gate data is claim-grade *reproduction* (G6), floor-vs-claim on the same
structure only incidentally, and it will be a handful of structures at most.

**A second finding compounds it.** The smoke's full 1,731-structure landscape was run at **scout**
cycles, not floor. Its relative error is **median 15.4 %, p95 89.5 %** — so it cannot be used to
size the promotion set either. The floor-grade error model from the prior campaign is the usable
one: **median 0.78 %, p95 2.38 %, max 5.10 %, 8.7 % of runs above 2 %** (n = 2,261).

**Bei's proposal: pre-register the estimator and the decision rule, not the number.** A Stage 0
calibration measures the floor→claim distribution on a stratified sample, and Δ is then fixed by a
rule written down in advance. That keeps the pre-registration honest — the rule is fixed before the
data, the value is determined by it — instead of inventing a margin and calling it measured.

---

## 1. Stage 0 — floor→claim calibration *(new; required by §0)*

| | |
|---|---|
| **Cycles** | claim grade, **10,000 init + 50,000 production**, both pressures |
| **Population** | 300 structures drawn from the Stage 1 output, **stratified by floor-value decile**, 30 per decile, with the top decile drawn at random from the top 5 % rather than the top 30 |
| **Replication** | 1 claim-grade run per structure per pressure; the Stage 1 floor value is the paired measurement |
| **Cost** | 300 × 9.13 = **2,739 CPU-h** (12.0 % of the naive basis) |
| **Output** | `stage0_calibration.csv` — one row per structure: floor value, claim value, both errors, decile |

**Pre-registered decision rule for Δ, fixed now:**

> Fit the signed difference `d = claim − floor` over the calibration sample. **Δ = max( p99(|d|),
> 3 × σ(d) )**, evaluated on the pooled sample, and reported per decile so any capacity dependence
> is visible. If the top-decile |d| distribution is materially wider than the pooled one — p99
> exceeding pooled p99 by more than 50 % — **Δ is taken from the top decile alone**, since that is
> the regime promotion decisions are made in.

**Stated limit of this rule.** It is a tolerance for the floor measurement's *disagreement with*
claim grade, which folds bias and noise together. It does not separate them, and with 300 points it
will not resolve a bias below roughly 0.2 %. That is adequate for a promotion margin and inadequate
for a claim about systematic offset; the plan makes no such claim.

---

## 2. Stage 1 — full-census floor screen

| | |
|---|---|
| **Cycles** | **2,000 init + 10,000 production**, both pressures (5.8 and 65 bar), in one pass |
| **Population** | all **12,499** structures; membership = the published SHA-256 manifest |
| **Replication** | 1 run per structure per pressure |
| **Cost** | 12,499 × 1.830 = **22,873 CPU-h** |
| **Basis** | measured: 1,072 structures / 2,144 runs / 1,957.9 CPU-h → 0.913 CPU-h per run |

**The pressure-ordered restructure and its concavity prune are withdrawn** (PI ruling, 2026-08-29).
The evaluation is retained in **Appendix A** because it is a measured negative result: the bound is
sound, and it removes 3.2 % of the 65 bar runs for 366 CPU-h while its own audit costs 915 and it
serialises Stage 1 behind a full-census barrier. Stage 1 therefore runs as a single pass and retires
each structure's two pressures together, with no barrier.

**Stage 1 is the naive basis exactly.** The charter's 22,873 CPU-h figure is a **floor-grade**
exhaustive pass, not a claim-grade one — worth stating because "1.83 CPU-h per structure" appears in
§4 beside the word *exhaustive*. Claim grade is **9.15 CPU-h per structure**; an exhaustive
claim-grade pass would be **114,365 CPU-h**, which is what the funnel exists to avoid.

## 3. Stage 2 — claim-grade promotion

Two disjoint populations, unioned:

**(a) Margin promotions.** Every structure whose Stage 1 floor value satisfies
`floor ≥ (provisional band top) − Δ`, with Δ from Stage 0 and the band top being the highest
Stage 1 floor value in the census.

**(b) Claimed structures, unconditionally.** Every structure named in the Claim of any replicate's
final report, at any value, whether or not it is anywhere near the band. **This population is not
knowable until collection completes**, and it is the one place the screen's scope depends on
trajectory content — see §7 for how that is kept blind.

| | |
|---|---|
| **Cycles** | **10,000 + 50,000**, both pressures |
| **Replication** | **2 independent runs per structure**, distinct seeds, for population (a); the pair is a G6-grade reproduction and both values are reported. Population (b) also 2 runs, so a replicate's claim is checked against a reproduced number, not a single one |
| **Cost, central** | (a) ~60 structures + (b) ≤ 80 claimed = 140 × 2 × 9.13 ≈ **2,556 CPU-h** |
| **Cost, envelope** | 400 structures × 2 × 9.13 = **7,304 CPU-h** |

**Why the count is an estimate and not a number.** Promotion depends on Δ, which does not exist
yet, and on the *floor-grade* density near the band top, which has never been measured — the only
full landscape is scout grade at 15.4 % median error. Extrapolating that landscape gives ~14
structures within 10 cm³/cm³ of the top when scaled to 12,499, but at 15.4 % error near a top value
of ~190 cm³/cm³ the scout ranking cannot resolve a 10 cm³/cm³ band at all. **The envelope is sized
at 400 structures — roughly 30× the naive extrapolation — because the honest statement is that the
promotion count is unknown until Stage 1 finishes.**

---

## 4. Stage 3 — random audit of the non-promoted set

Two populations, reported as two separate rates.

### 4.1 False-exclusion audit — non-promoted, unpruned

| | |
|---|---|
| **Cycles** | **10,000 + 50,000**, both pressures |
| **Population** | **300** drawn at random from the non-promoted set that received both floor runs |
| **Stratification** | 150 from the band immediately below the promotion threshold (threshold − 3Δ to threshold), where a false exclusion is plausible; 150 uniformly from the remainder, so the design can detect a surprise rather than assuming where it lives |
| **Replication** | 1 claim-grade run per structure per pressure |
| **Cost** | 300 × 9.13 = **2,739 CPU-h** |

With zero false exclusions in 300 draws, the rule of three gives a **95 % upper bound of 1.0 %** on
the false-exclusion rate. If any are found, the empirical rate is reported with a Wilson interval,
**Δ is re-derived at the larger value implied, and Stage 2 is re-run over the newly promoted set** —
pre-registered here so it cannot become a judgment call later.

### 4.2 Bound-violation audit — withdrawn

Withdrawn with the prune it audited (PI ruling, 2026-08-29). With no pruned set there is no
bound to violate. Retained in Appendix A as part of the evaluated-not-activated record.

## 5. Compute budget against the naive basis

| stage | structures | grade | runs each | CPU-h | vs 22,873 naive |
|---|---:|---|---:|---:|---:|
| 0 — calibration | 300 | claim | 1 | 2,745 | 12.0 % |
| **1 — full census** | **12,499** | floor | 1 | **22,873** | 100.0 % |
| 2 — promotion, central | ~140 | claim | 2 | 2,562 | 11.2 % |
| 3 — false-exclusion audit | 300 | claim | 1 | 2,745 | 12.0 % |
| retries @ 5 % | — | — | — | 1,546 | 6.8 % |
| **total, central** | | | | **32,471** | **1.42 ×** |
| **total, envelope** (Stage 2 at 400) | | | | **37,229** | **1.63 ×** |

*Costed at the naive basis's own arithmetic — 22,873 / 12,499 = **1.830 CPU-h per structure**,
**0.915 per run**, **9.150 at claim grade** (5× cycles), so the rows sum to the naive figure exactly.
Separately measured figures elsewhere in this study are 1.83 and 9.13; the 0.2 % difference is
rounding in the source.*

**This table reflects the withdrawal exactly.** Against the pruned variant it is **577 CPU-h
lower**: the prune's 366 CPU-h saving is given up and its 915 CPU-h audit is not incurred, with the
balance in the retry base. The screen costs **1.42–1.63× a naive floor pass** and **28.4–32.6 % of
an exhaustive claim-grade pass** (114,365 CPU-h).

## 6. Wave sizing and concurrency

**Measured ceilings.** PBS per-user running-job limit **580** (measured 2026-08-28, not assumed).
The harness fleet ceiling of **240** was a courtesy limit set from measured displacement of other
users *during the campaign week*.

**Post-collection revision (PI ruling, 2026-08-29):** the 240 ceiling existed to protect group
members while the fleet ran; from the last collection onward the PI coordinates directly with the
group, and the screen may run at **up to 480 concurrent**.

| | central (32,471) | envelope (37,229) |
|---|---:|---:|
| at **240** — perfect packing | 135.3 h | 155.1 h |
| at **240** — 70 % packing | 193.3 h (**8.1 d**) | 221.6 h (9.2 d) |
| at **480** — perfect packing | **67.6 h** | 77.6 h |
| at **480** — 70 % packing | **96.6 h (4.0 d)** | 110.8 h (4.6 d) |

**The revision halves the screen's wall clock: 8.1 days → 4.0 days at the central budget.**

**Standing contention rules, kept in force at the higher ceiling:**

1. **Whole-queue depth is logged at every poll** — total running and queued across all users, not
   just this study's share, as the smoke's crowding covariate already records.
2. **Automatic back-off to 240 on sustained third-party queueing.** "Sustained" is defined
   mechanically so it is not a judgment: any third-party job queued and not running across **three
   consecutive polls**. Back-off holds until two consecutive polls are clear.
3. **Every excursion above 240 is logged** with its start, end, peak concurrency and the queue
   state that justified it, so the 480 window is auditable rather than assumed.

**Packing efficiency is the risk, and it is measured.** Per-structure cost spans **45 s to 15,190 s
(338×)** in the prior campaign and **p99/median = 18.3×** in the smoke's own screen. A batch
finishes when its slowest member finishes, so **waves are sized by predicted cost, not by count**:
structures are ordered by a cost proxy (atoms × simulation-cell replication, both computable before
any run), binned into quartiles, and batched within a quartile. Batch sizes 40 for the cheapest
quartile, 8 for the most expensive.

## 7. Blindness, ordering, and the write barrier

**Ratified constraints, restated as mechanism rather than intention:**

1. **No screen output is written to the cluster before the last collection completes.** Enforced by
   the screen refusing to start: its first action reads `reps/main/collected/COLLECTION.md` for all
   16 replicates and exits non-zero if any is missing. It cannot write a byte before that check
   passes, because the check precedes workspace creation.
2. **The screen runs in `/home1/users/Bei/screen/`, created at start**, never inside any replicate
   workspace, and no replicate workspace is readable by it — they are archived off-cluster at
   collection, as the smoke workspaces already are.
3. **Stages 0–1 and 3 are blind by construction** — their populations are the manifest and a random
   draw, neither of which can encode trajectory content.
4. **Stage 2(b) is the single point where trajectory content enters.** It is confined to a list of
   structure identifiers extracted mechanically from the Claim section of each final report by a
   parser, with **no capacity values read** — the identifier list is the only thing that crosses.
   The parser's output is committed before Stage 2 runs, so what crossed is auditable.

---

## 8. Failure, retry, and completeness accounting for the full census

**Completeness is asserted against the manifest, not against a count of successes.** The failure the
accounting exists to catch is the one this study has already met three times: a stage that reports
success on a subset and looks complete.

- Every stage writes one ledger row per **manifest entry attempted**, including failures, with an
  explicit `status` of `ok | failed | retried_ok | abandoned`.
- **Retry policy:** up to **3 attempts** per run. Attempt 2 resubmits unchanged (transient
  scheduler and node failures dominated the smoke). Attempt 3 resubmits with the simulation cell
  re-derived, which is the one input the smoke found capable of failing deterministically.
- **A run that exits 0 having written no output is a failure, not a success.** RASPA on this build
  returns 0 whether or not it succeeds — measured both ways on 2026-08-29 — so status is decided by
  the presence and parseability of the output file, never by exit code.
- **Abandoned runs are reported by name.** The final ledger states `12,499 = ok + retried_ok +
  abandoned` as an identity that must hold exactly, and the leaderboard states the abandoned count
  beside it. A screen that silently covered 12,400 structures and called itself the landscape would
  reproduce SI-020's shape at study scale.

---

## 9. Output ledger format — what the leaderboard derives from

`screen_ledger.csv`, one row per structure per stage, append-only:

```
stem, stage, grade, init_cycles, prod_cycles, seed, n_05bar, err_05bar, n_65bar, err_65bar,
wc, wc_err, cpu_s, attempt, status, node, started_utc, finished_utc, raspa_sha256, uff_sha256
```

`screen_landscape.csv`, one row per structure, the leaderboard's direct input:

```
stem, floor_n05, floor_n05_err, pruned, prune_bound_wc, floor_wc, floor_err, promoted,
promotion_reason, claim_wc_1, claim_wc_2, claim_wc_mean, claim_wc_spread, reference_wc,
reference_grade, audit_sampled, audit_class, bound_violated, status
```

**A pruned structure carries no `floor_wc` and must never be given one.** Its row records
`floor_n05`, `pruned = true`, and `prune_bound_wc = 10.2069 × floor_n05` — the *upper bound* that
justified skipping its 65 bar run, explicitly labelled as a bound and not a measurement. Writing a
bound into the `floor_wc` column would put a number in the landscape that no simulation produced,
which is the failure the two-column rule in the paragraph below exists to prevent.
`bound_violated` is populated only for audited pruned structures and is the §4.2 rate's source.

`reference_wc` is the number a claim is scored against: the mean of the two claim-grade runs where
they exist, the floor value otherwise, with `reference_grade` naming which. **The two columns are
never merged**, so no reader can mistake a floor number for a claim-grade one — which is the
mistake the smoke made in the other direction when it reported a scout-grade landscape without the
error column that would have shown 15.4 % median error.

---

## 10. Ruling record

All items are ruled. Retained as the record of what was decided and on what basis.

| # | item | ruling |
|---|---|---|
| 1 | Δ as a rule rather than a number | **Sealed estimator from Stage 0.** No number was invented; the archive holds two paired floor↔claim points, both the same framework. |
| 2 | Stage 0 exists at all | **Yes, and drawn independently of Stage 3.** Adds 2,745 CPU-h; the alternative was a Δ with no empirical basis. |
| 3 | Stage 2 replication at 2 runs | **Ratified.** The reference number is a reproduced one. |
| 4 | 240 vs 580 concurrent | **Superseded**: 480 post-collection, contention rules kept (§6). |
| 5 | Stage 3 contingency | **Ratified.** False exclusions re-derive Δ and re-run Stage 2 — fixed in advance so it cannot become a judgment call. |
| 6 | the prune | **Withdrawn**, appendix retained. Budget reflects the withdrawal: **577 CPU-h lower** than the pruned variant. |
| 7 | bound-violation audit size | **Moot** — withdrawn with the prune. |
| 8 | 3σ noise allowance | **Moot** — withdrawn with the prune. |
| 9 | cheaper floor tier | **Refused on measurement.** The floor sits at the elbow: below it error runs 3.6× worse than 1/√cycles predicts. |

## Appendix A — the concavity prune: evaluated, not activated

### 2.1 The bound and its derivation

For an isotherm `N(P)` that passes through the origin and is **concave** on `[0, 65]` bar, the
chord slope `N(P)/P` is non-increasing in `P`. Therefore

```
N(65)/65  ≤  N(5.8)/5.8        ⇒        N(65) ≤ (65/5.8) · N(5.8) = 11.2069 · N(5.8)
WC = N(65) − N(5.8)            ⇒        WC    ≤ (65/5.8 − 1) · N(5.8) = 10.2069 · N(5.8)
```

The bound is the **pressure ratio itself**, attained only in the Henry limit (`b → 0`) and
approached from below as saturation sets in. Concavity through the origin is the whole requirement;
Langmuir is a sufficient special case, not a necessary one.

**Premises, stated because they are what could fail:**

1. **`N(0) = 0`.** Trivially true.
2. **Rigid framework.** Gate-opening, breathing and structural transitions produce stepped
   isotherms with locally *convex* segments, which break concavity. **This is protocol-guaranteed,
   not assumed about the materials**: charter §3 pins `framework rigid`, so no simulation in this
   study can produce a stepped isotherm even if the real material has one. The bound therefore
   holds for the quantity the screen actually computes.
3. **Supercritical adsorbate.** Methane at 298 K against `T_c` = 190.56 K gives a reduced
   temperature of 1.56, so there is no capillary condensation and no pore-filling step — the other
   two sources of convexity in this pressure range.
4. **Single component.** Pure CH₄; no mixture effects.

The residual physical risk is a strongly bimodal pore system whose second population fills only at
high pressure, which can give a locally convex segment. For supercritical methane in a rigid
framework over 5.8–65 bar this is not an observed regime, and §2.3 tests it empirically rather than
resting on the argument.

### 2.2 Execution

| | |
|---|---|
| **Stage 1a** | **5.8 bar only**, floor cycles (2,000 + 10,000), all **12,499** structures |
| **Prune** | skip 65 bar where `(N(5.8) + 3σ) · 10.2069 < (provisional band top) − Δ` |
| **Stage 1b** | **65 bar**, floor cycles, survivors only |
| **Replication** | 1 run per structure per pressure |
| **Cost** | 12,499 × 0.913 = **11,411 CPU-h** (1a) + survivors × 0.913 (1b) |

**The prune is applied to the upper confidence bound on `N(5.8)`, not to the point estimate.** A
structure is pruned only if it would remain outside the promotion zone even if its 5.8 bar
measurement were understated by 3σ. §2.3 shows why that allowance is not optional.

### 2.3 What the bound does empirically — measured, not asserted

Tested against **all 1,792 smoke runs** carrying both pressure points with `N(5.8) > 0`:

| | |
|---|---|
| measured `N(65)/N(5.8)` | median **1.536**, p95 4.453, p99 8.238, max 18.788 |
| runs exceeding 11.2069 | **6 of 1,792 (0.335 %)** |

**All six violations are noise, and identifiably so.** Every one is at **scout cycles (150 + 600)**,
the noisiest fidelity, and every one has `N(5.8)` between **0.0017 and 0.259** — where a small
absolute error produces an enormous ratio. Their working capacities are **0.019 to 2.76 cm³/cm³**
against a band top near 190. **None is within three orders of magnitude of the promotion zone.**
No violation occurs at floor grade or above, and none at any loading where the prune operates.

That is the case for the 3σ allowance rather than a bare comparison: the bound is physically sound,
but a *measurement* of it can exceed it at near-zero loading, and the prune must be robust to the
measurement rather than to the physics.

### 2.4 The prune is sound and nearly inert — stated before ratification, not after

**It removes 3.2 % of the 65 bar runs and saves ~365 CPU-h, 1.6 % of the naive basis.**

The reason is arithmetic, not implementation. The prune threshold is
`(band top − Δ)/10.2069 ≈ 19.4 cm³/cm³` at 5.8 bar, and the measured median `N(5.8)` across the
screened set is **84.7 cm³/cm³** with p5 = 15.7. **Roughly 94 % of structures clear the threshold
comfortably**, because the concavity bound is **19× looser than the median structure's actual
`WC/N(5.8)` ratio of 0.534**. A rigorous bound must accommodate the Henry limit; almost nothing in
this database is near it.

| prune variant | multiplier | pruned | CPU-h saved | provable? |
|---|---:|---:|---:|---|
| **rigorous concavity, 3σ allowance** | 10.207 | **3.2 %** | **~365** | **yes** |
| rigorous concavity, point estimate | 10.207 | 5.8 % | ~664 | yes, but not noise-robust |
| empirical p99.9 of measured ratio | 14.935 | 3.9 % | ~445 | no — and *looser* than the rigorous bound |
| empirical multiplier 3.0 | 3.000 | 31.6 % | ~3,600 | **no — 1 % of measured structures exceed it** |

Two things worth the PI's attention in that table. **The empirical p99.9 multiplier is larger than
the rigorous bound**, so tuning on the smoke data would produce a *weaker* prune than the theory —
a consequence of the same near-zero-loading noise. And **the multiplier that would actually save
real compute (3.0) is violated by 1 % of measured structures**, so it would false-exclude, which is
the one failure mode this screen exists to prevent.

**And the amendment does not pay for itself in compute.** The bound-violation audit it requires
(§4) costs **~913 CPU-h** against the **~365 CPU-h** the prune saves — **net +548 CPU-h**. That is
not an argument against it: what the amendment buys is a landscape whose completeness is *verified*
rather than argued, and 548 CPU-h is a cheap price for that. But it should be ratified for that
reason and not on the expectation of a saving.

### 2.5 Basis

Stage 1 remains the naive basis. The charter's 22,873 CPU-h figure is a **floor-grade** exhaustive
pass, not a claim-grade one — worth stating because "1.83 CPU-h per structure" appears in §4 beside
the word *exhaustive* and is easily read as the cost of a definitive number. It is not. Claim grade
is **9.13 CPU-h per structure**; an exhaustive claim-grade pass would be **114,116 CPU-h**, which is
what the funnel exists to avoid.

