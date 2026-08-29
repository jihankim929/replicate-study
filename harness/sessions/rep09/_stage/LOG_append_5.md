
## 2026-08-29 20:40 (launch +1.0h) — screen calibrated against a longer run; tasks reordered by promise

- DONE **Screen calibration, 46 paired structures, seed 1 both sides.**
  N(65 bar) at 200+500 cycles against the same structures at 200+1000 cycles:
  mean difference **−1.19 cm³/cm³**, median −0.72, largest single deviation
  5.3 cm³/cm³; in relative terms **−1.2% mean with 2.1% standard deviation**
  over the 45 structures loading above 5 cm³/cm³. RASPA's own reported error
  on the 200+500 runs averages 5.2% relative. So halving the production cycles
  costs ~1% of accuracy and buys ~40% of the cost: the screen ranks reliably,
  and the residual bias is *downward*, which is the safe direction for a filter
  that excludes on an upper bound.
- Node speed differs from the login node used for the cost probe by ~1.7×:
  200+500 cycles average 141.6 s on an `aa` compute node against 146.6 s for
  200+1000 on the login node. Full-database screen therefore costs ~490 CPU-h
  (30% of budget) at `aa` speed, not the 250 CPU-h projected from login-node
  timings. Accepted; the revised tier plan below still fits.
- DONE **Framework density computed for all 12,499 structures**
  (`manifests/density.csv`): min 0.164, p10 0.843, median 1.255, p90 1.803,
  max 3.963 g/cm³.
- DONE **Tier-1 task files reordered by ascending density**, interleaved over
  the 11 chunks. Across the 48 probe structures, Pearson correlation between
  density and N(65 bar) is **−0.669**, with mean N65 falling monotonically
  from 186.6 (ρ < 1.1) to 90.3 (1.4 ≤ ρ < 1.8). Density is a free prior from
  the manifest and costs nothing to exploit. Note it is only a prior, not a
  filter: the ρ ≥ 1.8 bin still reaches N65 = 170, which is why the screen
  remains exhaustive rather than density-truncated. The point of the reordering
  is that if the queue starves the screen, what ran is the part that mattered,
  and the report can say exactly which part that was.
- DECISION Tier 2 restructured. Rather than a mid-precision pass at both
  pressures, run **5.8 bar at the same 200+500 settings** on the top ~2,500 by
  N65. That yields a screening working capacity for every plausible candidate
  for ~60 CPU-h instead of ~325, because the 2.1% screen scatter is already
  well below the spread between candidates.

Revised budget: Tier 1 ~490, Tier 2 ~60, Tier 3 (floor, top ~200) ~215,
Tier 4 (claim, top ~12 × 3 seeds) ~194, calibration ~25. Total ~985 CPU-h,
61% of 1610, leaving room for the structural-modification arm and for
reproduction runs.
