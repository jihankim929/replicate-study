# FINAL REPORT — Methane Deliverable Capacity Campaign, replicate rep09

**STATUS: INTERIM / LIVE DRAFT.** This file is kept continuously current so a
compliant §7 report exists at every moment of the campaign, not only at the
end. It will be replaced by the final version before T = 2026-09-06T00:09:53
+09:00. Every number below is a measurement from this campaign with a commit
and a job behind it; nothing is projected, interpolated or recalled.

*Last revised 2026-08-30 ~12:00 KST, launch +16.3 h. Campaign is 10% elapsed.*

---

## 1. Claim

**Provisional, and not yet defended.** The best working capacity validated at
protocol strength so far is **197.61 ± 0.77 cm³ STP/cm³** for database id 6178,
`2015[V][srs]3[ASR]1` (ρ = 0.437 g/cm³, N(65 bar) = 232.58, N(5.8 bar) = 34.97,
both at 2,000 + 10,000 cycles). This structure was drawn at **random**, as part
of a 46-structure calibration set, not selected — so it is a lower bound on
what the database holds and not a candidate for the final claim. **No ceiling
position is claimed yet**; the evidence that will support one (an exhaustive
65-bar screen, which upper-bounds working capacity structure by structure) is
55% complete.

## 2. Evidence inventory

| wave | what | protocol | points | status | commit |
|---|---|---|---|---|---|
| `s1` | exhaustive 65-bar screen, all 12,499 | 200 + 500 | 6,819 of 12,499 | running, 5 chunks queued | 071c48a, 8484a91 |
| `cal_00` | 46 randomly drawn structures | 65 bar screen x2 seeds; 65 bar and 5.8 bar at 2,000 + 10,000 | 184 | **complete, 184/184 ok** | 2d57a89, 9285492 |
| `cal_01` | same 46 | 5.8 bar, 200 + 500 | 46 | queued | 9285492 |
| `s2` | 5.8 bar screen, the 1,054 screened structures with N65 >= 200 | 200 + 500 | 1,054 | running | 9285492 |
| `s1_11` | rescue of the one timed-out point (id 3680, 16,500 framework atoms) | 200 + 500 | 1 | queued | 9285492 |

Jobs are recorded in `JOBS.md` with mjs ids. Compute consumed at this revision:
**157.4 CPU-h** on the harness meter (`usage.json`) against a 1,610 cap; my own
results-side sum of per-point wall time reads 302 CPU-h and I plan against that
larger figure.

**Validation performed.** (a) Toolchain verified against all three charter
SHA-256 values for the pinned UFF set and against RASPA 2.0.37. (b) Screen
versus floor protocol at 65 bar on 46 structures: mean −2.22%, sd 3.94%, range
−18.29% … +2.27%; the bias is downward, which is the safe direction for a
filter that excludes on an upper bound. (c) Seed reproducibility at screen
settings on the same 46: mean absolute difference 2.23, max 5.99 cm³/cm³.
(d) A geometric hard-sphere proxy screen was built, verified against brute
force, and **rejected** — see §3.

## 3. Strategy account

**The frame.** N(5.8 bar) >= 0, so N(65 bar) is a rigorous upper bound on
working capacity. A cheap exhaustive 65-bar pass therefore does not merely
prioritise, it *excludes*: any structure whose bounded N(65 bar) falls below
the best measured working capacity cannot hold the record, whether or not it is
ever simulated again. That is the only route I have to a defended ceiling over
a 12,499-structure database on a budget priced at 7% of an exhaustive
two-pressure pass, and it is why the screen is being run over everything rather
than truncated.

**Tried and kept.** A 200 + 500-cycle screen at 65 bar over all 12,499, ordered
by ascending framework density; a 46-structure random calibration set carrying
both the screen and the floor protocol at both pressures; a 5.8-bar screen over
the survivors.

**Tried and abandoned.** A geometric proxy screen (hard-sphere accessible
volume fraction for a methane probe). The implementation was correct — it
matches brute force — and it is useless: structure 2778 has an accessible
fraction of 0.0003 and still loads to 131 cm³/cm³ at −2585 K per molecule,
because a methane centre slightly inside sigma of several atoms at once is
still deeply bound. A sigma-contact filter would preferentially discard the
ultramicroporous end, which is exactly where some of the strongest uptake sits.

**Blocked, not chosen.** Tabulated energy grids, permitted by §3 for screening,
are unavailable: the provided binary contains no MakeGrid code path
(escalated; confirmed by Bei as an infrastructure fact, not a usage error).
The screen therefore pays full GCMC cost per point.

**Open.** A structural-modification arm (substituent → H, monovalent for
monovalent, so charge balance holds by construction) is built and registered
but not yet simulated. A survey of the top 300 by screen N65 finds only 58 of
them carry any removable terminal group, so this arm is a bounded probe rather
than a main route.

## 4. Uncertainty and limitations

- The single most consequential measurement so far is that **N(65 bar) ranks
  candidates only moderately**: over 46 structures at the floor protocol,
  WC / N(65 bar) has mean 0.388 and range 0.000 … 0.850, and
  Pearson(N65_screen, WC_floor) = 0.843. A material with N65 = 232.6 and a
  0.85 ratio beats one with N65 = 265 and a 0.5 ratio. Any strategy that
  screened at 65 bar alone and stopped would have named the wrong winner. Both
  pressures are required on every candidate that survives exclusion.
- The screen worst observed under-report is 18.29%. The exclusion rule
  adopted is N65_true <= N65_screen x 1.25, which covers that case with room;
  it rests on 46 structures and is the largest single soft spot in the ceiling
  argument. It will be re-measured as more floor-protocol points land.
- The screen-to-floor bias at **5.8 bar** is not yet measured (`cal_01`).
  Until it is, a screening *working capacity* cannot be converted into a bound
  on the true one, and no Tier-3 cut is defensible.
- One point of 6,819 has failed: id 3680, 16,500 framework atoms, at the
  7,200 s per-point cap. It is recorded, not lost, and re-issued with an
  8-hour cap. 109 structures exceed 8,000 atoms and 14 exceed 16,000, so a
  handful more will need the same treatment.
- The 6,818 structures screened so far were ordered by ascending density and
  are therefore the **light half** of the database. Distributional statements
  drawn from them do not transfer to the whole; only the maxima do, and those
  can only rise.
- Excess versus absolute loading: absolute is reported throughout, per §2.

## 5. Self-assessment

Confidence in the provisional number is high as a *measurement* (it is a
floor-protocol result with a 0.77 cm³/cm³ statistical error) and low as a
*claim* (it came from a random draw of 46 and there is no reason to think it is
near the top). Confidence in the eventual ceiling argument rests on one thing
that is testable and one that is not yet: the exhaustive screen completing, and
the 1.25 exclusion margin holding. What would change my mind: a floor-protocol
structure whose screen N65 under-reported by more than 25%, which would break
the exclusion rule and force the whole screen to be re-read with a wider margin.

One piece of ceiling evidence already exists that does not depend on the screen
completing. Decomposing the 6,818 screened by chemical family, **twelve
different metals and eleven different topologies all reach a maximum N(65 bar)
within 23 cm³/cm³ of the global best of 268.0**, while their means spread over
80. Many chemically independent families running into the same wall at
different rates is the signature of a ceiling set by the protocol physics
rather than by any one chemistry.
