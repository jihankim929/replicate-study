# REFERENCE SCREEN — EXECUTION PLAN — DRAFT FOR RATIFICATION
*(Bei, 2026-08-29. Seals on the PI's reply. Executes post-collection only.)*

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
| **Cycles** | **2,000 init + 10,000 production**, both pressures (5.8 and 65 bar) |
| **Population** | all **12,499** structures of the frozen world, membership = the published manifest |
| **Replication** | 1 run per structure per pressure |
| **Cost** | 12,499 × 1.83 = **22,873 CPU-h** |
| **Basis** | measured, 1,072 structures / 2,144 runs / 1,957.9 CPU-h → 0.913 CPU-h per run |

**This stage *is* the naive basis.** The charter's 22,873 CPU-h figure is a floor-grade exhaustive
pass, not a claim-grade one — worth stating because "1.83 CPU-h per structure" appears in the
charter beside the word *exhaustive* and is easily read as the cost of a definitive number. It is
not. Claim grade is **9.13 CPU-h per structure, 5× the cycles**; an exhaustive claim-grade pass
would be **114,116 CPU-h**, which is what the funnel exists to avoid.

---

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

| | |
|---|---|
| **Cycles** | **10,000 + 50,000**, both pressures |
| **Population** | **300 structures** drawn at random from the non-promoted set |
| **Stratification** | 150 from the band immediately below the promotion threshold (threshold − 3Δ to threshold), where a false exclusion is plausible; 150 uniformly from the remainder, where it is not, so the design can detect a surprise rather than assuming where it lives |
| **Replication** | 1 claim-grade run per structure per pressure |
| **Cost** | 300 × 9.13 = **2,739 CPU-h** |

**What 300 buys, stated as a bound rather than a hope.** With zero false exclusions found in 300
draws, the rule of three gives a **95 % upper bound of 1.0 %** on the false-exclusion rate of the
non-promoted set. If any are found, the empirical rate is reported with a Wilson interval and
**the promotion threshold is re-derived at a larger Δ and Stage 2 re-run over the newly promoted
set** — that contingency is pre-registered here so it is not a judgment call later.

---

## 5. Compute budget against the naive basis

| stage | structures | grade | runs each | CPU-h | vs 22,873 naive |
|---|---:|---|---:|---:|---:|
| 0 — calibration | 300 | claim | 1 | 2,739 | 12.0 % |
| 1 — full census | 12,499 | floor | 1 | **22,873** | 100.0 % |
| 2 — promotion, central | ~140 | claim | 2 | 2,556 | 11.2 % |
| 3 — audit | 300 | claim | 1 | 2,739 | 12.0 % |
| retries @ 5 % of all runs | — | — | — | ~1,545 | 6.8 % |
| **total, central** | | | | **32,452** | **1.42 ×** |
| **total, envelope** (Stage 2 at 400) | | | | **37,200** | **1.63 ×** |

The screen therefore costs between **1.4× and 1.6× a single naive floor pass**, and between **28 %
and 33 % of an exhaustive claim-grade pass** (114,116 CPU-h). That ratio is the funnel's whole
justification and it should be checked at ratification rather than taken on trust.

---

## 6. Wave sizing against post-collection cluster availability

**Measured ceilings.** PBS per-user running-job limit **580** (measured 2026-08-28, not assumed);
harness fleet ceiling **240** (ratified, Flag I). Post-collection the 16 replicates are finished, so
nothing of this study competes with the screen — but the cluster is shared, and the smoke measured
**210 running jobs across 3 other users** at a single sample.

**Bei proposes running at the ratified 240, not the PBS 580.** The 240 ceiling was set from measured
displacement of other users, and post-collection convenience is not a reason to discard a limit
adopted for a courtesy reason. At 240 concurrent:

| | central | envelope |
|---|---:|---:|
| total CPU-h | 32,452 | 37,200 |
| wall-clock at 240 concurrent, perfect packing | **135 h (5.6 d)** | 155 h (6.5 d) |
| at 70 % packing efficiency | **193 h (8.0 d)** | 221 h (9.2 d) |

**Packing efficiency is the risk, and it is measured.** Per-structure cost spans **45 s to 15,190 s
(338×)** in the prior campaign, and **p99/median = 18.3×** in the smoke's own screen. A wave of
fixed-size batches finishes when its slowest member finishes, so naive batching wastes most of a
wave. **Waves are therefore sized by predicted cost, not by count**: structures are ordered by a
cost proxy (atoms × simulation-cell replication, both in `descriptors.csv` and both computable
before any run), binned into quartiles, and batched within a quartile so batch members have similar
runtimes. Batch sizes: 40 for the cheapest quartile, 8 for the most expensive.

---

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
stem, floor_wc, floor_err, promoted, promotion_reason, claim_wc_1, claim_wc_2, claim_wc_mean,
claim_wc_spread, reference_wc, reference_grade, audit_sampled, status
```

`reference_wc` is the number a claim is scored against: the mean of the two claim-grade runs where
they exist, the floor value otherwise, with `reference_grade` naming which. **The two columns are
never merged**, so no reader can mistake a floor number for a claim-grade one — which is the
mistake the smoke made in the other direction when it reported a scout-grade landscape without the
error column that would have shown 15.4 % median error.

---

## 10. What Bei needs ruled

1. **Δ as a rule rather than a number** (§0, §1) — or, if the PI wants Δ fixed now, it will be a
   judgment, and the plan should say so rather than call it measured.
2. **Stage 0 exists at all.** It adds 2,739 CPU-h (12 % of the naive basis) that the ruling did not
   ask for. The alternative is a Δ with no empirical basis.
3. **Stage 2 replication at 2 runs**, which doubles that stage's cost and is what makes the
   reference number a reproduced one.
4. **240 concurrent rather than the available 580** (§6), costing roughly 2.4× the wall clock.
5. **The Stage 3 contingency** — that discovering false exclusions re-derives Δ and re-runs
   Stage 2 — which is pre-registered here precisely so it cannot become a judgment call later.
