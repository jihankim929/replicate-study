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

## Four things about the request, stated before the rules

1. **No definitions could be inherited.** The request specifies *"the same definitions already used
   for the timing ranges in the manuscript"*. **There is no manuscript in this repository** — the
   rubric (`prereg/rubric_v1.0.md` §14, §220), `prereg/seal_notes.md` and `STATE.md` each record its
   absence independently. Every rule below is therefore **declared here, not reproduced from
   anywhere.** If the manuscript's definitions differ, these columns must be rebuilt against them.
2. **`strategy (D/B/S/M)` is empty for all sixteen runs.** No D/B/S/M taxonomy exists anywhere in
   this repository — not in `prereg/`, the charter, the rubric, `STATE.md` or any replicate record.
   Assigning sixteen runs to four unseen categories would be interpretation, which this request
   excludes. **The column is present and empty**, awaiting the definitions.
3. **These extractions are not key-independent.** `structure_class` distinguishes `excluded` from
   `retained`, and *excluded* is defined **only** by the sealed exclusion set in
   `answer-key/exclusion_set_record.md` (6 structures / 11 files). `fig2_claims_long.csv` therefore
   depends on the answer key. `fig2_events.csv` does not.
4. **`fig2_jobs.csv` is not built.** Reason and evidence in its own section below.

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
| `end_reason` | `spend_cap` where `usage.json` has `spend_level == "stop"` or `spend_fraction ≥ 1.0`; else `filing`. **12 of 16 ended at the spend cap, 4 by filing.** No run ended on the deadline, so `deadline` and `other` are unused |

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

## `fig2_jobs.csv` — NOT BUILT

The specification asks for one row per **completed simulation job** with `t_submitted`,
`t_completed`, `accuracy_tier` and `structure_id`, sourced from *"the completed job records used
for compute metering, not scheduler-only accounting"*. **Those records do not carry those fields.**

- **The metering source is `cput_finished.txt`**, named in every `usage.json` as
  `"cpu_h_basis": "finished-job PBS cput (harvest_cput.sh -> cput_finished.txt)"`. Its format is
  **two fields — cput-seconds and job id** (`8971 3473240.bnode0.kaist.ac.kr`), **21 lines for
  rep01**. No submit time, no completion time, no tier, no structure. It is also **not in the
  collected record**.
- **`JOBS.md` is collected but is a batch ledger, not a job record** — 21 table lines for rep01,
  where a single row covers 540 structures (*"Round-1 screen, 540 structures, floor cycles"*), the
  outcome column is free text (*"waiting in mjs FIFO"*), several ids are ranges (*"mjs 3411-3416"*),
  and there are **no completion timestamps**.

So the file cannot be produced from the collected record, and cannot be produced from the metering
source the request names, because the per-job structure/tier/timing association was never written
down. Producing it would require re-deriving job→structure mapping from the workspace run trees —
a different and much larger read, against data outside the seal — and it is **held rather than
attempted**.
