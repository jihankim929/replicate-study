
## 2026-08-29 21:12 — descriptor sweep complete, all 12,499 structures
`rep04_desc` finished in 76 min on 16 cores (~19 CPU-h, 1.2% of the compute budget).
Zero structures failed. `manifest/desc_all.csv` now holds one row per structure.

Surrogate working-capacity distribution (cm3/cm3): p50 9.1, p90 62.5, p99 90.1,
p99.9 98.0, max 107.1. 409 structures score above 80, 982 above 70, 1844 above 50.
The head is exactly what the physics predicts it should be: low-density frameworks
(0.36-0.77 g/cm3) with high hard-sphere accessible fraction. Nothing about the shape of
this distribution is surprising, which is mildly reassuring about the surrogate but is
not evidence for it — that comes from the calibration set.

## 2026-08-29 21:17 — contention forced a resubmission strategy
All six of my jobs sat pending with Bei at its per-partition caps (amd 80/80, aa 38/38)
and the `ac` partition 200/204 full from users outside this campaign. The moment
`rep04_desc` released its 16 amd cores, sibling replicates took them.

A ppn=16 request cannot fit the fragments that open when a sibling job ends; a ppn=4
request can. I therefore withdrew the ppn=16 `calib` (qrm 3316) and the queued ppn=16
`bench` (qdel 3473395) and resubmitted the same work as six ppn=4 jobs spread across
amd, ac and aa, so that whichever partition frees first can start doing my work. Total
requested is 24 cores against a sustainable average of ~10, which is deliberate for a
one-off screening burst and will be throttled once tier-1 begins.

## 2026-08-29 21:20 — the database contains systematic near-duplicates
Every one of the 12,499 names parses as `<year>[<metal>][<topology>]<n>[<ASR|FSR|ION>]<i>`.
Grouping on everything except the ASR/FSR field gives **4,349 groups covering 8,847
structures** — i.e. roughly a third of the database is twinned. The median surrogate
working-capacity difference within a pair is **0.34 cm3/cm3**, far below the spread that
distinguishes candidates.

Consequence for strategy: tier-1 will carry **one representative per ASR/FSR pair**,
recovering the twin only if its representative scores well. This cuts tier-1 by about
35% at negligible risk of losing a distinct material, and it is a much better use of a
compute budget set at 7% of an exhaustive pass than simulating the same framework twice.
The twins also serve a second purpose: a matched pair that I *do* run at claim grade is a
free reproducibility check on the whole pipeline.

Enrichment in the surrogate top 500, as a share of each group's database membership:
topologies `nts` 76%, `nbo` 32%, `tbo` 25%, `scu` 25%; metals `Zr` 32%, `Fe` 13%,
`Cu` 10%. `ASR` variants are four times likelier to reach the head than `FSR` (6.1% vs
1.5%). This is a map of where the head of the database lives, and it will be part of the
ceiling argument: if the best material sits inside a family that is already densely
sampled, that is evidence the ceiling is near.
