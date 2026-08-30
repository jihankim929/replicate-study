# STATE — current beliefs and open tasks

*(Self-sufficient: this file alone must suffice to resume the campaign.)*
*(Last updated 2026-08-30 12:05 KST, launch +16.4 h.)*

## Fixed facts

- Deadline **T = 2026-09-06T00:09:53+09:00** (launch 2026-08-29T19:41:39 +168 h
  + 4.4704 h of recorded fleet pause). ~156 h remain. **This supersedes the
  19:41 figure that STATE and `bin/status.sh` carried before the pause.**
- Budgets: **1610 CPU-h**, **US$280 spend**, **32M tokens**, **12 live jobs**,
  queue `long`, prefix `rep09_`.
- Usage at this stamp (`usage.json`, the authoritative meter):
  **157.4 CPU-h scheduler**, 1.42M tokens. My own results-side accounting
  (sum of per-point wall) reads 302 CPU-h; the harness meter is lower and is
  the one the cap is judged on. I plan against the conservative (higher) figure.
- Target: max working capacity `N(65 bar) − N(5.8 bar)`, 298 K, **absolute**
  loading, cm³ STP/cm³, over the 12,499 CIFs in `db/`.
- Toolchain verified against all three charter SHA-256 values; RASPA 2.0.37.
  `RASPA_DIR=<ws>/raspa_home`, binary `toolchain/raspa/bin/simulate`.
- Login-node interactive compute is **not** metered (INBOX ruling 2026-08-30).
- `qas` lives at `/usr/local/mjs/qas`; it is not on the non-interactive PATH.

## The cluster, and why it is the binding constraint

`mjs` gates on a per-user core limit per node class **and** a class total over
all users (`molsim_job_scheduler.py:500-506`; limits in
`/usr/local/mjs/config.txt`). All sixteen replicates submit as UNIX user `Bei`,
so the caps are one shared pool: ax 32, aa 38, amd 80, ac 102 = **252 cores for
the whole fleet**. At this stamp `quse` shows Bei at 38/38 aa, 78/80 amd,
102/102 ac, and **0/32 ax** — ax is unreachable because another user is at
64/64 of the ax class total. Dispatch order is (node class, that user usage,
submission time); with one user it is FIFO. Practical consequences:

- Keep all 12 slots occupied at all times; a free slot is throughput lost.
- A queued job position is its submission time. Do not churn submissions.
- Small `ppn` fits through the per-user limit check when the class is nearly
  full (that check `continue`s rather than blocking the class), so a ppn=1/2
  job dispatches when a ppn=8 one cannot.

## Machinery (`bin/`)

`cifutil.py` (CIF parse, cell matrix, unit-cell replication for 12.8 Å) ·
`prep_cif.py` (db CIF → RASPA CIF, labels → `X_`, charges dropped, geometry
untouched) · `gcmc.py` (one point → one CSV row) · `run_batch.py` (pool over a
task file; idempotent, skips points already ok in the output CSV) ·
`mkjobs.py` (chunks + PBS, resumable) · `remaining.py` · `census.sh` (live
rep09 jobs: mjs queue union `qstat -f` names) · `autopilot.sh` (submits from
`jobs/autopilot.plan`, capped at 12 live; **running as pid 2865800**, survives
session loss) · `aggregate.py` · `cal_report.py` (calibration analysis →
`tables/cal_wc.csv`) · `rank.py` · `select.py` · `modify.py`
(defunctionalisation) · `geom.py` (set aside, see Belief 1) ·
`status.sh` (**use this, not ad-hoc queries**).

## Beliefs

1. **No geometric proxy screen.** `geom.py` matches brute force and is still
   useless: structure 2778, ρ = 2.20 g/cm³, has hard-sphere accessible fraction
   0.0003 for a methane probe and still loads to 131 cm³/cm³ at −2585 K per
   molecule. A σ-contact filter would preferentially discard ultramicroporous
   winners.
2. **N(65 bar) rigorously upper-bounds working capacity** (N(5.8 bar) ≥ 0), so
   the 65-bar screen *excludes* rather than merely deprioritises. This is the
   backbone of the ceiling argument: an exhaustive 65-bar screen plus a
   calibrated margin turns "I did not test everything" into "everything I did
   not test cannot beat the winner".
3. **The screen bias is measured and downward.** 46 structures with both the
   200+500 screen and the 2,000+10,000 floor at 65 bar: mean −2.22%, sd 3.94%,
   range −18.29% … +2.27%. Seed-pair scatter at screen settings: mean 2.23,
   max 5.99 cm³/cm³. Adopted exclusion rule:
   **N65_true ≤ N65_screen × 1.25**; exclude only when
   N65_screen × 1.25 < WC\*.
4. **N65 predicts WC only moderately.** Over the same 46, WC/N65 has mean
   0.388, sd 0.191, range 0.000 … 0.850, and Pearson(N65_screen, WC_floor)
   = 0.843. Ranking on N65 alone would pick the wrong winner: N65 = 232.6 with
   ratio 0.85 (WC 197.6) beats N65 = 265 with ratio 0.5. **Both pressures are
   needed on every candidate that survives the exclusion.** Weak binding, not
   high uptake, is what makes a material good here.
5. **Density is a real but weak prior.** Pearson(ρ, WC_floor) = −0.599 over the
   46. N65 by density band peaks at an interior optimum near ρ = 0.5–0.6, but
   band *maxima* fall far more slowly than band means (268.0, 264.8, 250.6,
   247.9, 227.1 against means 223.5, 211.1, 187.0, 165.3, 148.7), which is the
   empirical case against truncating the screen at any density threshold.
   Tasks still run in ascending-ρ order so partial completion covers the
   promising end.
6. **Energy grids are unavailable** — confirmed by Bei as an infrastructure
   fact: the provided binary contains no MakeGrid code path. Not a usage error,
   will not be fixed this campaign. Screening runs without them.
7. Screen cost falls steeply with density (292 s per point at ρ = 0.5–0.7 down
   to 117 s at 1.1–1.2) and the database median is ρ = 1.255, so the expensive
   part of the screen is the part already done. Whole-database Tier 1
   projection: **285–447 CPU-h**.
8. **A handful of structures will time out, not more.** Framework atoms after
   replication: p50 2,424, p99 7,488, p100 23,166; 109 structures exceed 8,000
   and 14 exceed 16,000. Exactly one point has timed out in 6,819 (id 3680,
   16,500 atoms, 7,200 s cap). Cost scales roughly as atoms times molecules, so
   the heavy tail needs a longer cap, not a different protocol.

## Current best numbers

| | value |
|---|---|
| Best **floor-protocol** WC measured so far | **197.61 ± 0.77** cm³/cm³, id 6178 `2015[V][srs]3[ASR]1`, ρ = 0.437, N65 = 232.58, N5.8 = 34.97, ratio 0.850 |
| Best screen N65 seen (6,818 structures) | 268.0, id 9930 `2020[Al][fmz]3[ASR]1`, ρ = 0.526 |
| Screen N65 quantiles (6,818, density-biased sample) | p50 128.8, p90 214.6, p99 244.7, p100 268.0 |

6178 came out of a **random** sample of 46. That a random 46 already contains a
197.6 says the top of this database is high, and it sets the bar the claim has
to clear.

## Tier plan and budget

| Tier | Set | Protocol | Est. CPU-h | Status |
|---|---|---|---|---|
| 1 | all 12,499 | 65 bar, 200+500 | 285–447 | **54.6% done**, 5 chunks queued |
| 1v | 46 probe | 65 bar screen x2 seeds; both P at floor | 25 | **done** |
| 1w | same 46 | **5.8 bar at screen settings** | 2 | queued as `cal_01` |
| 2 | N65_screen >= 158 | 5.8 bar, 200+500 | ~150 | 1,054 queued (threshold 200); **widen to 158** |
| 3 | top ~200 by screening WC | both P, 2,000+10,000 (floor) | ~210 | not started |
| 4 | top ~10 x 3 seeds | both P, 10,000+50,000 (claim) | ~190 | not started |
| M | modification arm | as Tier 3 | ~80 | not started |

Total ≈ 900–1,100 CPU-h against 1,610.

**Why Tier 2 must widen from N65 >= 200 to >= 158.** The exclusion rule is
N65_screen × 1.25 < WC\*. With WC\* = 197.6 that is N65_screen < 158.1. The
threshold of 200 used for the first Tier-2 wave was set before the floor
calibration landed and is not defensible as an exclusion; it is a
prioritisation. Tier 2 gets extended to 158 as Tier 1 completes. If the eventual
best WC rises, the threshold rises with it and the extension shrinks.

## Open tasks

- [ ] **Tier 1**: chunks `s1_04,05,06,07,10` queued; `s1_11` is a one-point
      rescue of id 3680 at ppn=2 with a 28,800 s cap. `s1_02` was retired
      (job 3443 `qrm`ed): it was complete but for 3680 and the watchdog was
      re-queueing an 8-core job to retry one point.
- [ ] **Tier 2** `s2_00..04` queued (1,054 ids, `manifests/s2_ids.txt`).
      Extend to N65_screen >= 158 once Tier 1 finishes.
- [ ] **cal_01** queued: 5.8 bar at screen settings on the 46 calibration
      structures. This is the missing calibration — it measures
      WC_screen vs WC_floor directly, which is what the Tier 2 → Tier 3
      exclusion margin has to rest on. Until it lands, no Tier-3 cut is
      defensible.
- [ ] Tier 3 and 4 not started. Trigger: Tier 2 coverage of the N65 >= 158 set.
- [ ] Modification arm not started (`bin/modify.py` built and tested):
      H-capping of terminal monovalent substituents on high-N65 structures that
      sit *denser* than the ρ ≈ 0.5–0.6 optimum, monovalent-for-monovalent so
      charge balance holds by construction. Decide after Tier 2.

## Errors on the record

- 20:44 2026-08-29 watchdog double-submitted `s1_00`/`s1_01` (live count 14 >
  cap 12) because it read only the mjs queue listing, which drops dispatched
  jobs. Withdrawn before dispatch, no GCMC work duplicated. Fixed via
  `census.sh`.
- A log entry was stamped 23:00 when it was written at 22:38; corrected on the
  record in commit 5d44a98.
- `bin/status.sh` carried the pre-pause deadline (19:41) for 4.4 h after the
  harness extended it. Corrected here and in the script.
