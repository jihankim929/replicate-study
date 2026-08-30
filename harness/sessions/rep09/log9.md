
## 2026-08-30 (launch +~4h) — screen at 11.4%, cost projection settled

- RUNNING Tier 1 at 1,431 of 12,499 points, ~800 points/h, 86 CPU-h spent.
- Cost per point falls steeply with framework density, which is the half of the
  ordering trade-off I had not measured: mean wall time is 292 s in the
  ρ = 0.5–0.7 band, 231 s at 0.7–0.9, 200 s at 0.9–1.0, 147 s at 1.0–1.1 and
  117 s at 1.1–1.2. The database median density is 1.255 and three quarters of
  it lies above 1.056, so the expensive part of the screen is the part already
  done. Whole-database projection: **285–447 CPU-h** (18–28% of budget)
  depending on how much further the cost falls. No scope cut is needed.
- Structure of the result, 1,431 structures spanning ρ = 0.16–1.18. Mean N65
  by band: 198.2 (ρ<0.5), **223.5 (0.5–0.7)**, 211.1 (0.7–0.9), 187.0
  (0.9–1.0), 165.3 (1.0–1.1), 148.7 (1.1–1.2). The interior optimum near
  ρ ≈ 0.6 is now firm.
- **The maxima do not fall nearly as fast as the means**: 268.0, 264.8, 250.6,
  247.9, 227.1 across those same bands. A band whose *mean* has dropped 75
  cm³/cm³ still contains individual structures within 20 of the global best.
  That is the empirical case for screening exhaustively rather than truncating
  at a density threshold — the ranking is driven by structure, not density, and
  density only shifts the odds.
- Best so far: `2020[Al][fmz]3[ASR]1` (id 9930, ρ = 0.526),
  N65 = 267.96 ± 2.86 cm³/cm³ at screen settings.
