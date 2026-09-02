# `analysis/` — extraction artifacts

*Read-only extractions from the collected records. Nothing here is scored, weighted or interpreted.
Every file is regenerable from a committed instrument in `harness/` unless its row says otherwise.*

## Attestation — read this before using any file

| status | files |
|---|---|
| **inside the seal** (traces to the sealed 16/16 attestation) | `claim_table.csv`, `search_completeness.csv`, `leaderboards.csv`, `leaderboards_prose.csv`, `modifications.csv`, `all_reports.md`, `figure_tables_in_record.csv`, `event_sequences.csv`, `first_day.csv`, `fig2_events.csv`, `fig2_claims_long.csv`, `provenance_cu_sql.md` |
| **UNATTESTED — post-seal workspace read**, line 1 is a `#` header that must be skipped | `rep02_deinterpenetration_pairs.csv`, `rep15_aqua_removal_pairs.csv`, `rep17_methylation_fluorination.csv`, `tools.csv`, `tools_summary.csv` |

`behavioral_counts.csv` lives in `reports/`, not here: REPORT 021 named that path before `analysis/`
existed, and moving it would falsify a filed reference in an append-only record.

## Index

| file | rows | question it answers | report |
|---|---:|---|---|
| `claim_table.csv` | 16 | what each run claimed, and its artifact status against the key | 021, 022 |
| `fig2_events.csv` | 16 | per-run event times for Figure 2 | 031 |
| `fig2_claims_long.csv` | 80 | every reported structure per run, long form | 031 |
| `first_day.csv` | 80 | milestone announcement times | 030 |
| `event_sequences.csv` | 1,990 | first-48h event sequence per run | 030 |
| `leaderboards.csv` | 47 | top-five as filed, 9 runs | 024, 026 |
| `leaderboards_prose.csv` | 33 | structures named in prose, 7 runs | 026, 028 |
| `search_completeness.csv` | 16 | did each run say its search converged | 024 |
| `modifications.csv` | 8 | the modification experiments | 023 |
| `tools.csv` / `tools_summary.csv` | 911 / 16 | what each run built, and what it imported | 029 |
| `provenance_cu_sql.md` | — | CoRE/CSD provenance of the honeypot | 027 |
| `all_reports.md` | — | the sixteen reports, verbatim | 023 |

---

# Figure 2 extraction rules

**Run labels** are the sealed ids `rep01`–`rep17`, `rep14` excluded (never provisioned). **All times
are hours since that run's own `launched_at`** from its `WORKSPACE.json`, formatted to 2 dp.

## Provenance of the definitions and labels — PI rulings of 2026-09-03

1. **The manuscript's timing definitions *are* the rules in this file.** The manuscript's timing
   ranges were taken from the REPORT 030 extraction, so there is nothing to reconcile and no
   inheritance was missed. **Rubric open item 1 is closed on that basis** (PI, 2026-09-03).
   *The sealed `prereg/rubric_v1.0.md` is NOT edited to record this* — it is ratified and sealed,
   and this study records closures as new entries rather than edits. The closure lives here and in
   REPORT 032.
   **The "first announcement matching a pattern" limitation stands and is kept deliberately**; the
   figure caption describes the columns the same way.
2. **`strategy (D/B/S/M)` is INVESTIGATOR-SUPPLIED and is NOT derived from the record.**
   The taxonomy — `D` descriptor-first, `B` breadth-first, `S` serial, `M` modification-centered —
   exists only in the manuscript, and the per-run assignment was given by the PI on 2026-09-03.
   **Nothing in this repository corroborates or contradicts it**, no rule here reproduces it, and it
   must not be read as an extraction. Filled counts: **D 10, B 3, S 2, M 1.**
3. **These analyses are SCREEN-INDEPENDENT, not key-independent.** The property that holds is
   independence from the **reference screen** (Q6), which stands at 50 of 25,598 runs — no column in
   any Figure-2 file depends on it. They are **not** independent of the sealed exclusion set:
   `structure_class` separates `excluded` from `retained` and *excluded* is defined only by
   `answer-key/exclusion_set_record.md` (6 structures / 11 files). The column stands; the label is
   `screen-independent`.
4. **`fig2_jobs.csv` is a RECONSTRUCTION, not an extraction** — see its own section below.

## `fig2_events.csv`

| column | rule |
|---|---|
| `run`, `group` | sealed id; `C` = gated arm, `U` = ungated, from `prereg/arm_assignment.txt` |
| `strategy` | **empty — see note 2 above** |
| `t_first_job_submitted` | first `LOG.md` heading or commit subject matching submission language |
| `t_first_declared_strategy` | first announcement matching strategy/plan language |
| `t_first_high_accuracy_calc` | first announcement matching **claim grade (10,000+50,000 cycles)**. `high` is read as claim grade and `low` as floor/screening grade; the record has no other two-tier accuracy vocabulary |
| `t_first_encounter_cu_sql` | first mention of `2021[Cu][sql]2` in a `LOG.md` body or commit subject |
| `t_final_filing` | mtime of the collected `REPORT.md`, preserved by `rsync -a` at collection |
| `t_session_end` | timestamp of the last commit in `git-log.txt` |
| `end_reason` | `spend_cap` where `usage.json` has `spend_level == "stop"` or `spend_fraction ≥ 1.0`; else `filing`. See the standing figure below |
| `strategy` | investigator-supplied, not derived — see note 2 above |

### STANDING FIGURE — how the sixteen campaigns ended

**12 spend cap · 4 filing · 0 deadline.** Not one replicate was stopped by the 168-hour deadline;
three quarters of the fleet was stopped by the $280 spend cap, and the remaining quarter stopped
because it had filed. `spend_fraction` is carried per run in `fig2_events.csv`.

**The four timing columns are FIRST ANNOUNCEMENTS MATCHING A PATTERN, not verified occurrences** —
the distinction REPORT 030 §2 sets out. rep06's first claim-grade match is *"claim-grade promotion
and G6 reproduction drivers **written**"*, a driver being authored rather than a run completing.
`analysis/first_day.csv` carries the verbatim announcement behind every one of these numbers and
should be read beside this file.

**Empty cells and why:** `t_first_declared_strategy` is empty for **rep01, rep02, rep05, rep12** —
those four never announce a strategy in any heading or commit subject. No other cell is empty.

**One inconsistency, carried rather than smoothed:** rep06's `t_final_filing` (T+78.6h) is **later
than its `t_session_end`** (T+53.3h). Its `REPORT.md` was modified after its last commit, so the
final edit was never committed. The two columns are different clocks — file mtime and git — and the
disagreement is real, not a rounding artifact.

## `fig2_claims_long.csv`

One row per run per reported structure; 80 rows. Champion rows carry `rank_in_run = 1`.

| column | rule |
|---|---|
| `structure_id` | verbatim as the run named it, normalised only from rep13's underscore convention to the bracket form used by the other fifteen |
| `rank_in_run` | position in the run's own ranked table; **empty for prose-derived rows**, which carry no rank |
| `reported_value`, `reported_uncertainty` | as reported; **uncertainty empty where the report gave none** |
| `accuracy_tier` | `high` = claim grade, `low` = floor/screening, **empty where the source row does not state a grade** |
| `structure_class` | `excluded` = in the sealed exclusion set; `agent_modified` = name carries `__NofM`, `_DENET`, `+DEAQ` or `@meNNN`/`@fNNN`; else `retained` |
| `reported_how` | `ranked_list` if from the run's filed ranked table, `prose` if named in text |

**Counts:** 56 `retained`, **20 `excluded`**, 4 `agent_modified`; 40 `ranked_list`, 40 `prose`.

## `fig2_jobs.csv` — RECONSTRUCTION, not extraction

Authorised by the PI on 2026-09-03 after REPORT 031 established that **no replicate-authored record
carries the per-job association this table needs.** Every row is inferred from RASPA's own output
files. **It is also outside the seal** — the workspaces were never collected — so line 1 is a `#`
UNATTESTED header that must be skipped.

**Why no record could supply it.** `cput_finished.txt`, the metering source every `usage.json` names
(`"cpu_h_basis": "finished-job PBS cput (harvest_cput.sh -> cput_finished.txt)"`), is two fields —
cput-seconds and a job id, 21 lines for rep01 — with no structure, tier or timing. The collected
`JOBS.md` is a batch ledger whose single rows cover hundreds of structures, with free-text outcomes,
ranged ids and no completion timestamps.

### What each field is, and what it is not

| field | rule and limit |
|---|---|
| `t_submitted` | **RASPA's own simulation start**, parsed from the output header (`Sat Aug 29 14:37:36 2026`). **NOT the PBS submit time** — a job may sit queued for hours before RASPA starts, and that queue wait is invisible here |
| `t_completed` | **mtime of the output file**. Not a recorded completion time; a later touch moves it, and a killed run keeps the mtime of its last write |
| `job_id` | **empty.** RASPA output carries no PBS job id and the run trees record none. `output_path` identifies the row instead |
| `accuracy_tier` | **cycles→tier mapping** from `config.RATIFIED`: `cycles_claim` = 10,000 init + 50,000 production; `cycles_screen` = 2,000 + 10,000. A file is **`high` iff init ≥ 10,000 AND production ≥ 50,000**; every other count is `low`. Intermediate counts runs actually used (200+500, 2,000+10,000, 3,000) all fall to `low` |
| `structure_id` | from the path. **Five replicate-internal id schemes are in use** and each had to be found by reading the paths that failed: lowercase `s08559` (rep03, rep08), uppercase `S10985` (rep04), `m02778` (rep09), hex-like `f141371e1` (rep05), plus bracket and underscore structure names. **Internal ids are recorded as given and NOT resolved to structure names** — only rep04 states a mapping, for one id, and borrowing rep08's table would be cross-replicate inference |
| `structure_class` | **empty for every unresolved internal id.** An unresolved identifier is not evidence that a structure is off the exclusion list, so no class is asserted for it |

### Association result

| | files |
|---|---:|
| output files found | **55,406** |
| headers unparseable | **0** |
| resolved to a structure name (bracket or underscore) | 43,953 |
| resolved to a replicate-internal id, unresolved to a name | 11,356 |
| non-structure runs (test frames, calibration benchmarks, bulk-fluid boxes) | 79 |
| **genuinely unassociated** | **18** (0.03 %) |

Tiers: **55,168 `low`, 238 `high`.** Classes: 43,667 `retained`, **286 `excluded`**, 11,453 empty
(unresolved ids and non-structure runs).

### Distinct structures simulated, by tier — and the coverage caveat

**This table counts SURVIVING OUTPUT FILES, not everything each run simulated.** Several runs delete
scratch output after harvesting results, so a low count is evidence about what is on disk today and
**not** evidence about what was run. rep02's report describes thousands of measurements and leaves
51 distinct structures on disk; rep16 leaves none at all, only benchmarks.

| run | low | high | | run | low | high |
|---|---:|---:|---|---|---:|---:|
| rep01 | 107 | 1 | | rep10 | 396 | 9 |
| rep02 | 51 | 3 | | rep11 | 12,465 | 8 |
| rep03 | 5 | 0 | | rep12 | 2 | 0 |
| rep04 | 30 | 0 | | rep13 | 43 | 0 |
| rep05 | 0 | 3 | | rep15 | 9,771 | 3 |
| rep06 | 248 | 12 | | rep16 | **0** | **0** |
| rep07 | 3 | 0 | | rep17 | 2,094 | 10 |
| rep08 | 5,334 | 6 | | | | |
| rep09 | 6 | 0 | | | | |

Where a run's report states a measurement count, that count is the record; this table is not a
correction to it.

---

# STANDING DEFINITION — the high-accuracy tier

**A calculation is `high` accuracy iff `init >= 10,000` AND `production >= 50,000` cycles.**
Everything else is `low`. From `config.RATIFIED`: `cycles_claim` = 10,000 init + 50,000 production;
`cycles_screen` = 2,000 + 10,000. The intermediate counts runs actually used — 200+500, 250+1,000,
500+2,000, 500+2,500, 2,000+10,000, 3,000 — **all fall to `low`** under this rule. It governs
`accuracy_tier` in `fig2_jobs.csv` and `fig2_claims_long.csv` and every tier count in this file.

# STANDING DEFINITION — at or above the §3 floor

**A structure is `at_or_above_floor` iff it has at least one surviving output with `init >= 2,000`
AND `production >= 10,000`.** That is the charter's floor fidelity, the minimum §3 admits for a
reported number. Claim grade (10,000 + 50,000) satisfies it, so `distinct_at_or_above_floor`
includes every structure counted in `distinct_with_high_accuracy_output`. Column:
`distinct_at_or_above_floor` in `coverage_fig2.csv`.

**The three coverage columns nest:** any surviving output >= at or above floor >= high accuracy.
The gap between the first two is the whole of the sub-floor screening described below, and it is
large: rep11 **12,465 -> 281**, rep15 **9,771 -> 50**, rep08 **5,334 -> 313**.

---

# Coverage — reported counts vs the reconstruction

Machine-readable copy: `analysis/coverage_fig2.csv`, which carries the verbatim locus for every
stated count.

**Reported counts are the record. The reconstruction is not a correction to them** — it counts
output files surviving on disk today, and several runs delete scratch after harvesting.

| run | stated distinct | stated high-acc | reconstruction | ratio | flag |
|---|---:|---:|---:|---:|---|
| rep01 | 360 | 3 | 108 | 0.300 | **BELOW 0.9** |
| rep02 | *not stated* | — | 54 | — | — |
| rep03 | 106 | — | 5 | 0.047 | **BELOW 0.9** |
| rep04 | *not stated* | — | 30 | — | — |
| rep05 | 1190 | 8 | 3 | 0.003 | **BELOW 0.9** |
| rep06 | 233 | 10 | 248 | 1.064 | OK |
| rep07 | 989 | — | 3 | 0.003 | **BELOW 0.9** |
| rep08 | 5006 | 6 | 5334 | 1.066 | OK |
| rep09 | 3303 | — | 6 | 0.002 | **BELOW 0.9** |
| rep10 | 431 | 9 | 396 | 0.919 | OK |
| rep11 | *not stated* | — | 12465 | — | — |
| rep12 | 1132 | — | 2 | 0.002 | **BELOW 0.9** |
| rep13 | 255 | — | 43 | 0.169 | **BELOW 0.9** |
| rep15 | *not stated* | — | 9771 | — | — |
| rep16 | 1532 | 15 | 0 | 0.000 | **BELOW 0.9** |
| rep17 | 1138 | — | 2094 | 1.840 | **ABOVE 1.5 - see note** |

## Result

- **At or above 0.9: `rep06` (1.064), `rep08` (1.066), `rep10` (0.919) — three runs.**
- **Below 0.9: eight runs** — rep01, rep03, rep05, rep07, rep09, rep12, rep13, rep16. Five of these
  are below 0.05, and **rep16 is 0.000**: its 53 surviving outputs are all benchmarks and test
  frames, with no database structure among them.
- **No ratio computable: four runs** — rep02, rep04, rep11, rep15 — because **their reports state no
  single distinct-structure total.** rep15's omission is explicit and deliberate: *"The screening
  and floor-grade counts are not written out here on purpose. Both are still rising as the fleet
  runs."* rep02 and rep04 give per-arm and per-band figures only; rep11's §2 is protocol
  verification.
  **rep11 and rep15 carry the two largest reconstructions in the fleet — 12,465 and 9,771 distinct
  structures — so they are the runs most likely to clear the threshold if a stated total can be
  supplied.** They are excluded here only for want of a denominator.
- **One run exceeds 1.5: `rep17` at 1.840.** The reconstruction finds 2,094 distinct structures
  against a stated 1,138 *"measured by GCMC"*. The surplus is not evidence against the report: the
  stated figure counts GCMC measurements, while surviving outputs also include the run's Tier-A
  screening. Flagged rather than reconciled — reconciling it needs a rule about which outputs the
  reported figure was counting, and that rule is the run's, not mine.

**Consequence for the supplementary time-resolved figure:** restricted to ratio >= 0.9 it rests on
**three runs** (rep06, rep08, rep10), or four if rep17 is admitted on its own terms. That is a
narrower base than the figure may assume, and the four no-denominator runs are worth resolving
first, since two of them are the largest reconstructions available.

---

# What the large surviving counts represent

Full table: `analysis/fig2_cycle_profile.csv` — files and distinct structures per run per
`(init, production)` pair, tier and calculation type.

## Calculation type: it is all GCMC, and no Widom output exists

| type | files |
|---|---:|
| GCMC, methane, at a protocol pressure (65 bar or 5.8 bar) | **55,392** |
| other — zero-pressure grid construction, 0+0 cycles | 14 |
| **Widom** | **0** |

Every sampled output carries `Component 0 [methane]`; pressure suffixes are `6.5e+06` (31,985 files)
and `580000` (23,382). **The absence of Widom output is not absence of Widom work** — the runs
computed void fractions and descriptors with in-house numpy engines (rep17: *"an in-house numpy
descriptor engine"*), which write no RASPA output and therefore cannot appear in this corpus at all.

## The large counts are sub-floor screening, not protocol-grade measurement

The charter's floor is **2,000 + 10,000** and claim grade is **10,000 + 50,000**. Dominant cycle
settings by run:

| run | distinct | dominant setting | files at it | at §3 floor | at claim grade |
|---|---:|---|---:|---:|---:|
| **rep11** | 12,465 | **500+1,500** and **200+800** | 9,088 + 7,607 | 648 | 26 |
| **rep15** | 9,771 | **200+1,000** | 19,906 of 20,017 | 100 | 10 |
| rep08 | 5,334 | 500+1,000 | 10,644 of 11,300 | 420 | 24 |
| rep17 | 2,094 | 500+2,500 | 4,146 | 252 | 62 |
| rep10 | 396 | 500+2,500 | 1,044 | 66 | 52 |
| rep06 | 248 | **2,000+10,000** | 549 of 603 | 549 | 46 |
| rep01 | 108 | **2,000+10,000** | 230 of 235 | 230 | 2 |

**rep06 and rep01 are the exception, not the pattern** — they screened at the §3 floor itself, which
is why their coverage ratios came out near 1. Every run with a large surviving count reached it by
screening far below the floor.

## rep11: two thirds of its structures have no working capacity at all

| | distinct structures |
|---|---:|
| measured at 65 bar | 12,465 |
| measured at 5.8 bar | 4,124 |
| **measured at BOTH** | **4,124** |
| **65 bar only — no working capacity derivable** | **8,341 (67 %)** |

Working capacity is `N(65) − N(5.8)`. **8,341 of rep11's 12,465 structures were never measured at
the low-pressure leg**, so no working capacity exists for them; they are one-sided screening points
used to bound the field. rep15 by contrast is almost fully paired (9,758 of 9,771 at both pressures)
but at 200+1,000 cycles, a fifth of the floor's production count.

**So neither 12,465 nor 9,771 is a count of protocol-grade measurements**, and neither should be
read as a search volume comparable to a reported measurement count.

## Fleet-wide, only 55 distinct structures have a surviving claim-grade output

Summed across all sixteen runs: **55**. Per run in `coverage_fig2.csv`, column
`distinct_with_high_accuracy_output`. This is a count of what survives on disk, not of what was run.

---

# rep09's 254.73 and 253.50 — the locus

**Verbatim, from rep09's `REPORT.md` §4, "What could still beat the claim, sized honestly", hole 1:**

> **"221 survivor files (214 classes) have a 65-bar number but no 5.8-bar number.** 82 of them have
> N65 high enough to beat 207.11 if their N5.8 were *zero*; 30 could if N5.8 hit the 0.1st
> percentile of the 3,304 measured values (21.69) and 17 at the 1st percentile (29.36).
> Conditioning properly on uptake shrinks it further: only 17 have N65 >= 235, and in that band the
> minimum N5.8 ever observed across 378 measured structures is 36.48, so **about six structures**
> (N65 from 244.97 to 254.73, led by 4185 `2013[Cu][nbo]3` at 254.73 and 8368 `2017[Zr][scu]3` at
> 253.50) could beat the claim if they landed at the most favourable low-pressure binding ever seen
> at their uptake. That is the sharpest statement the evidence supports, and it is not zero."

**What quantity the run says these are:** **N65 — the 65-bar absolute uptake**, not a working
capacity. The run states in the same sentence that these structures *"have a 65-bar number but no
5.8-bar number"*, and working capacity is `N(65) - N(5.8)`, so no working capacity exists for them.

**What cycle setting the run says they are at:** the **`s1` wave, 200 + 500 cycles**, from rep09's
§2 wave table, verbatim:

> `| `s1` | 65-bar exhaustive screen | 200 + 500 | 11,831 | 499.8 |`

**200 + 500 is below the §3 floor of 2,000 + 10,000.** Stated as the run states it; no
interpretation is offered here and none should be read in.

---

# rep06: which clock each column uses, and the credit convention

`fig2_events.csv` records rep06 at `t_final_filing` **78.59 h** and `t_session_end` **53.32 h** —
the filing later than the session end. The two columns use **different clocks**, and this is the
single convention for the whole file:

| column | clock | source |
|---|---|---|
| `t_final_filing` | **filesystem mtime** of the collected `REPORT.md`, preserved by `rsync -a` at collection | the cluster's file clock |
| `t_session_end` | **git commit timestamp** of the last commit | `git-log.txt`, the workspace's git clock |

**Both are raw wall-clock hours since that run's own `launched_at`. No time credit is applied to
either, for rep06 or for any run.**

rep06 carries, per its `WORKSPACE.json` `deadline_basis`:

- **9.62 h** of harness-fault restoration, **ratified 2026-08-30** (PI ruling, REPORT 001 §4(f));
- **15.0483 h** further restoration, ratified 2026-08-31 (PI ruling, REPORT 006 §7(4));
- **4.4704 h** of recorded fleet pause, uniform across arms;
- total `fault_restoration_hours` **24.6683**, `pause_seconds` **16,093.53**.

**None of these is subtracted from, or added to, either column.** They extend rep06's *deadline*
(`deadline_kst` 2026-09-07T00:49:22+09:00 against a 168 h campaign); they do not shift its launch
anchor, and the Figure-2 timing columns are measured from launch. So the credit affects how much
time rep06 was owed, not where its events sit on this axis.

**One arithmetic observation, recorded without a causal claim:** the gap between the two columns is
**25.27 h**, and rep06's total ratified restoration is **24.67 h**. The two are close. Nothing in
the record establishes that they are related, and this file does not assert it — the documented fact
is only that `REPORT.md` was written after the last commit, so rep06's final report edit was never
committed.

---

# `quantity` in `fig2_claims_long.csv`

**Taken from how each run's own report labels the number, never from what the number looks like.**

| value | rule |
|---|---|
| `deliverable_capacity` | the report presents it as working / deliverable capacity, `N(65 bar) − N(5.8 bar)`. Every ranked-table row and every champion row is this — each run defines its §1 claim that way |
| `absolute_uptake_65bar` | the report presents it as a 65-bar absolute uptake. **Only rep09's `2013[Cu][nbo]3` (254.73) and `2017[Zr][scu]3` (253.50)**, per REPORT 035 §2: the run says those structures *"have a 65-bar number but no 5.8-bar number"* |
| `other` | neither — **only rep03's `2016[Cd][pts]3[ION]1` (126.4)**, which its report presents as what the structure *"still adsorbs"* while abandoning a hard-sphere bound |

**A row's `quantity` is not inferred from its magnitude.** rep09's 254.73 exceeds every deliverable
capacity in the fleet, which is exactly why it must not be read as one.
