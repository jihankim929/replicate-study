# CYCLE-CONVERGENCE ANALYSIS — pre-seal input to the reference-screen plan
*(Bei, 2026-08-29. Extracted from the archived smoke outputs; no new simulation run.)*

**Finding: a cheaper floor tier is not justified. The ratified floor (2,000 + 10,000) sits at the
elbow of the measured convergence curve — it is the cheapest setting that is still
equilibration-converged, and the tier below it fails by 3.6× more than sampling statistics predict.**
Bei therefore proposes **no amendment** to Stage 1 or Stage 0 cycle counts, and the budget table is
unchanged.

---

## 1. What was extracted

`harness/convergence_extract.py` parsed **3,626 archived RASPA outputs** carrying running-average
checkpoints. Every run in the archive was written with `PrintEvery = cycles/5`, so each carries five
checkpoints at 20/40/60/80/100 % of production. Runs were paired by structure and parent directory
to reconstruct **WC = N(65) − N(5.8) at each checkpoint**, giving **1,808 paired traces**:

| tier (init + prod) | paired traces |
|---|---:|
| 10,000 + 50,000 — claim | 2 |
| 2,000 + 10,000 — floor | 32 |
| 500 + 2,000 | 8 |
| 150 + 600 — scout | 1,766 |

---

## 2. The elbow, measured

**Reported block error on WC, by tier** — the statistical error the simulation itself estimates:

| init + prod | n | median | p90 | p95 | 1/√cycles prediction | ratio |
|---|---:|---:|---:|---:|---:|---:|
| 10,000 + 50,000 | 2 | **0.02 %** | 0.02 | 0.04 | 0.61 % | **0.07×** |
| **2,000 + 10,000** | 29 | **1.35 %** | 11.83 | 16.62 | 1.35 % | **1.00×** |
| 500 + 2,000 | 6 | **7.43 %** | 18.03 | 37.75 | 3.03 % | **3.57×** |
| 150 + 600 | 1,742 | **15.54 %** | 66.78 | 957.85 | 5.53 % | **2.81×** |

**Below the floor tier the error stops being sampling-limited.** If shortening a run only removed
samples, error would scale as `1/√cycles`. It does not: at 2,000 production the measured error is
**3.6× worse** than that scaling predicts, and at 600 production **2.8×**. The excess is
equilibration — those runs have not reached the state they are sampling, and that component does not
shrink with more sampling of the wrong distribution.

**Above the floor tier the opposite holds**: at 50,000 production the error is **0.07×** the
scaling prediction, because the equilibration component has vanished entirely and only sampling
noise remains.

**So 2,000 + 10,000 is the elbow.** It is the shortest setting in the archive where measured error
and sampling statistics agree — the definition of "converged, and no longer paying for it."

---

## 3. Within-run convergence, and why it is a lower bound

`|WC(f) − WC(final)| / |WC(final)|`, by tier and fraction of production:

| tier | at 20 % | at 40 % | at 60 % | at 80 % |
|---|---:|---:|---:|---:|
| 10,000 (n=32) — median | 6.17 % | 0.27 % | 0.18 % | 0.14 % |
| 10,000 — p95 | 34.47 % | 11.55 % | 3.11 % | 1.75 % |
| 600 (n=1,762) — median | 12.67 % | 5.63 % | 3.24 % | 1.68 % |
| 600 — p95 | 76.03 % | 49.06 % | 29.33 % | 12.97 % |

**These numbers understate the error of a genuinely shorter run, and must not be read as if they
did not.** A running average at 80 % of a run shares 80 % of its samples with the final value, so
their difference is bounded by the variance of the last 20 % alone. Checkpoint differences measure
**drift**, not the error of an independent short run. The §2 block errors are the correct estimator
for that, and they are what the recommendation rests on. This paragraph exists because the §3 table
is the more inviting one and would support a cheaper tier that §2 refutes.

---

## 4. Porosity dependence — and why it does not rescue a cheaper tier

Scout tier, error at 80 % of production, by helium void fraction:

| porosity band | n | median | p90 | p95 |
|---|---:|---:|---:|---:|
| high > 0.50 | 11 | 0.21 % | 1.16 % | 1.16 % |
| mid 0.30–0.50 | 183 | 0.40 % | 1.28 % | 1.54 % |
| **low < 0.30** | 1,568 | **2.02 %** | **9.58 %** | **13.61 %** |

**High-porosity structures converge fastest, and they are exactly the promotion candidates** — which
looks like an argument for a cheap tier applied selectively. It is not, for two reasons. First, the
band a structure belongs to is not known before it is simulated; porosity is a descriptor, but
promotion is decided on WC. Second, and decisively, these are §3 checkpoint differences, subject to
the correlation caveat above; the §2 block errors are not stratified finely enough (n=29 at floor)
to support a porosity-conditional cycle count. **A tier that is cheap only for structures already
known to be easy is not a screening tier.**

---

## 5. The claim tier, incidentally

Both archived claim-grade structures reach their 50,000-cycle value early:

| structure | at 10,000 prod | at 20,000 | at 30,000 |
|---|---:|---:|---:|
| `2023[Cu][ctn]3[FSR]1` | 0.180 % | 0.006 % | 0.081 % |
| `…[FSR]1__stripH` | 0.048 % | 0.026 % | 0.017 % |

This hints that **50,000 production is generous** — but n = 2, both high-capacity, both the same
framework, and both subject to §3's correlation caveat. **Bei proposes no change to the claim tier.**
It defines the reference every claim is scored against; weakening it on two data points from one
framework would trade the study's measurement standard for compute the funnel does not need.

---

## 6. On the ~200 CPU-h supplementary set

**Bei recommends not spending it now, and folding it into Stage 0 instead.** Two reasons, one
scientific and one operational.

**The question it would answer is already answered.** §2 locates the elbow from 29 floor-tier and
1,742 scout-tier block errors — not from the thin claim-grade set — and the elbow is the ratified
floor. A supplementary set would refine a curve whose shape is not in doubt.

**And it would run against a live 16-replicate fleet.** 25 structures × 2 pressures is **50
concurrent jobs** on a cluster where the fleet ceiling is 240 and the replicates are actively
queueing. That displaces replicate jobs and perturbs the **crowding covariate (Flag I)**, which is a
pre-registered measurement of this study. The PI's permission addressed answer-key contamination,
which this does not touch; cluster contention is a separate exposure and Bei flags it rather than
assuming the permission covered it.

**If the PI wants it run anyway**, Bei proposes: **≤ 8 concurrent jobs**, logged as a named entry in
the crowding record so the covariate can be corrected, and the structures drawn stratified by
porosity with `PrintEvery = 1,000` for 50 checkpoints per run. That set then **doubles as the first
25 points of Stage 0's calibration sample**, so its cost is not additional to the plan — it is
Stage 0 paid early.

---

## 7. Consequence for the plan

- **Stage 1 cycle counts: unchanged** (2,000 + 10,000, both pressures).
- **Stage 0 cycle counts: unchanged** (10,000 + 50,000).
- **Budget table: unchanged** at 33,048 CPU-h central / 37,806 envelope.
- **The floor definition freezes at seal**, per the ruling, and this analysis is the record of what
  it was frozen against.
