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
