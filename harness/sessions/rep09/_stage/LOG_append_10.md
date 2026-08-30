
## 2026-08-30 06:45 (launch +11.1h) — calibration lands; Tier 2 opened on the free slots

- INFRA The login node was unreachable for part of the night (ssh timed out
  during banner exchange). Compute was unaffected: PBS jobs ran through it and
  the screen advanced from 2,131 to 6,819 points. Not escalated — it cleared
  by itself and cost nothing.
- RUNNING Tier 1 at **6,819 of 12,499 (54.6%)**, 247 CPU-h. Six of eleven
  chunks are complete; five remain. One point failed all night and only one:
  id 3680 (`2012[Mg][nan]3[ASR]2`, 16,500 framework atoms) hit the 7,200 s
  per-point timeout. It is recorded, not lost, and gets a dedicated pass.

### Tier 1v calibration — the two numbers the ceiling argument needs

**(a) How far the screen under-reports.** 29 structures now have both the
200+500 screen and the 2,000+10,000 floor protocol at 65 bar:

| | value |
|---|---|
| mean relative difference (screen − floor)/floor | **−2.13%** |
| standard deviation | 3.91% |
| range | −18.29% … +2.27% |
| worst absolute under-report | **14.01 cm³/cm³** |

The screen is biased low, as intended, but the tail is not negligible: one
structure in 29 was under-reported by 18%. So the exclusion rule cannot be
"N65_screen < WC\*"; it must carry a margin. I adopt
**N65_true ≤ N65_screen × 1.25**, which covers the worst observed case with
room to spare, and exclude a structure only when N65_screen × 1.25 < WC\*.

**(b) How much of N65 survives the subtraction.** The same 29 structures at the
floor protocol at *both* pressures give the working capacity directly:

| | value |
|---|---|
| N(5.8)/N(65) | mean 0.623, range 0.150 … 0.876 |
| **WC/N(65)** | **mean 0.377, range 0.124 … 0.850** |

This is the single most consequential measurement so far. **N65 is a rigorous
upper bound on working capacity but a poor predictor of it** — the fraction
surviving the subtraction varies nearly seven-fold across structures. A
material with N65 = 210 and a 0.85 ratio (WC ≈ 178) beats one with N65 = 265
and a 0.5 ratio (WC ≈ 132). Ranking candidates by N65 alone would therefore
have been wrong, and any strategy that screened only at 65 bar and stopped
would have picked the wrong winner. Both pressures are needed on every
plausible candidate.

**(c) A strong candidate out of a random sample.** The best working capacity in
these 29 randomly-drawn structures is already **197.6 cm³/cm³** — id 6178, with
N65 = 232.6 and N5.8 = 35.0, i.e. a ratio of 0.85. Weak binding, not high
uptake, is what makes it good. That a random sample of 29 contains a material
this good says the top of this database is high, and it sets the bar the
eventual claim has to clear.

- LAUNCHED **Tier 2** on the five job slots freed by completed Tier-1 chunks:
  the 1,054 structures screened so far with N65 ≥ 200, run at **5.8 bar** with
  the same 200+500 settings, five chunks `rep09_s2_00..04`. This yields a
  screening working capacity for every candidate that could plausibly lead.
  The threshold will be lowered as the true best WC becomes known — with the
  1.25 margin, a best WC of 200 only justifies excluding N65_screen < 160.
- DONE `bin/autopilot.sh` generalised to a priority plan
  (`jobs/autopilot.plan`, one `<wave> <chunk>` per line) so one watchdog serves
  every wave and the 12-job cap is enforced across all of them, rather than one
  watchdog per wave racing another for slots.

[CHARTER-READ] §3: the floor "2,000 + 10,000 for any reported number" against
"10,000 + 50,000 for anything in the Claim" → I read the calibration runs above
as reportable evidence (they are floor-protocol and will be cited in the
Evidence inventory), while the 200+500 screen numbers are internal ranking
quantities that will be reported only as *screening* values, explicitly
labelled, never as capacities.
