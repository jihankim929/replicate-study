# Three SI queries, answered read-only — 2026-09-06

*Companion to `charter_revisions.csv`, which was extended through Rev 25 in the same pass.
Every quantity below carries its locus. Nothing in the study record was modified to produce
this file; the only writes in this pass were `charter_revisions.csv`, this file, and the
`README.md` entries for both.*

---

## 1. Descriptor-tail accounting — **858 is AFTER deduplication**

| stage | count | locus |
|---|---:|---|
| Selected by the tail rule | **1,007** | `analysis/fig4_descriptor_tail.csv` — 1,007 data rows, `n` 1…1,007 |
| — of which by `vf_he` top-1000 | 1,000 | `selected_by = vf_he_top1000` |
| — of which by `d_max > 15 Å` | 7 | `selected_by = d_max>15` |
| Overlap with the 1,500-structure random sample | **149** | recomputed here by set intersection of `structure_id` against `analysis/fig4_sample_20260903.csv` |
| **Final tail size (queued segment)** | **858** | 1,007 − 149 |

**The rule, verbatim from the file's own header line:** *"Population = 9,167 coordinate-distinct
representatives … minus those 11; take the 1,000 highest helium void fraction (`vf_he`), then add
every remaining structure with largest cavity diameter `d_max` > 15 Ångstrom."* The second
criterion adds only 7 because **234 structures in the pool exceed `d_max` 15 Å and 227 of them
were already in the top 1,000** (`reports/REPORTS.md:6431`).

**The deduplication is a separate, later, ruled step — not part of the tail rule.** It was
proposed as *"272 CPU-h of that is pure duplication … 149 structures are in both the sample and
the descriptor tail, and both segments run them at floor grade"* (`reports/REPORTS.md:6452`),
filed **"Not applied without your word", and then applied**: *"**(1) Dedupe — applied.** Each
`(structure, grade)` runs once … **149 descriptor-tail structures were already in the sample;
removing the duplicate floor runs saves 272 CPU-h**"* (`reports/REPORTS.md:6510-6511`).

**Both numbers are in the record and they mean different things:**

- **1,007** is the descriptor tail as a *set of structures selected by the rule*. It is the
  number in `analysis/fig4_descriptor_tail.csv`, and the number REPORT 041 §2 reports against the
  file's hash (`reports/REPORTS.md:6421`). It survived the 2026-09-03 rebuild that narrowed the exclusion from every file
  sharing an excluded base name to the eleven named files: *"Tail is still 1,007 structures but
  its membership changed"* (`reports/REPORTS.md:6515`).
- **858** is the descriptor tail as a *queue segment* — 1,007 minus the 149 the sample already
  runs at the same grade. It is the number in the deduplicated queue table
  (`reports/REPORTS.md:6539`), in both Figure-4 order amendments (*"the descriptor tail's 858
  deduplicated structures"*, `prereg/fig4_order_amendment_2026-09-03.md:25` and
  `…_2026-09-04.md:30`), and in the export's per-segment completion block
  (`analysis/fig4_interim.csv:12`, *"descriptor_tail 833 / 858 (97.1%)"*).

**Arithmetic check on the whole queue:** 1,500 sample + **858** tail + 571 agent tail + 2 claims
= **2,931**, which is the `TOTAL … / 2931` denominator in `analysis/fig4_interim.csv:15`. With
1,007 in place of 858 it would not close.

**Recomputed, not quoted.** The 149 was re-derived for this note by intersecting the two files as
they stand (`4d90e37e…` tail, `78f5bbbe…` sample): 1,007 distinct ids, 1,500 distinct ids,
intersection 149, difference 858. It reproduces the ruled figure exactly.

**One caveat for anyone citing the file's hash.** REPORT 041 §2 records the rebuilt tail as
`65b475ba53309b0b60946275a4605eee78f56764375ff74a8a8b2aec312cbdda`
(`reports/REPORTS.md:6517`). The file on disk today hashes to
`4d90e37e9e645a1a72dad5f4d94ac8263f2c9569435c1119f4558a89bf60b53d`. The membership is the one
the record describes — 1,007 rows, 1,000 + 7 by the two criteria, 149 overlapping the sample —
so cite the count and the rule, or re-hash before citing a hash.

---

## 2. Smoke phase — the two launch times and the two CPU-h figures

### 2.1 14:45 versus 15:28 KST — both are real, and they are different events

`14:45` appears **once** in the repository: *"**Launched 2026-08-26 14:45 KST.** `s01` (gated) and
`s02` (ungated), screen sessions `477.rep-s01` and `533.rep-s02`"* (`LOG.md:713`). `15:28`
appears in the loop logs and in the ledger: *"From launch (2026-08-26 15:28 KST) until this
entry…"* (`SI_LEDGER.md:101`, SI-002) and *"Launch was 2026-08-26 15:28 KST, so the campaign was
**65.53 h**"* (`analysis/si_verbatim/smoke_endgame.md:7`).

**The loop log resolves it. `harness/sessions/s01.loop.log` has three `iteration 1 starting`
lines, not one:**

```
2026-08-26T05:45:11Z iteration 1 starting      <- 14:45:11 KST, the LOG.md launch
2026-08-26T06:27:11Z iteration 1 starting      <- 15:27:11 KST
2026-08-26T06:28:16Z iteration 1 starting      <- 15:28:16 KST, the one that survived
2026-08-29T05:01:21Z iteration 1 exited rc=0 after 253985s
```

`s02.loop.log` is the same shape, at 05:45:13Z / 06:27:13Z / 06:28:27Z.

**Only the third start produced work.** The first two have no matching `exited` line — they were
killed, not finished. The third ran **253,985 s**, and `06:28:16Z + 253,985 s = 2026-08-29
T05:01:21Z` **to the second**, which is the line the log carries. So the surviving session, and
the only one whose transcript exists, began **2026-08-26T06:28:16Z = 15:28:16 KST**.

**What happened in the 43 minutes between them is on the record**, in the same LOG entry that
gives 14:45 — the launch *"failed three separate ways, and every one of them looked like
success"*: a malformed deny rule that *"blocked both replicates for 40 minutes"* sitting on an
interactive Settings Warning in a detached screen; a heartbeat that advanced unconditionally so
the watchdog *"reported a perfectly healthy replicate"* throughout; and both replicates running
with transcript saving silently disabled through an inherited `CLAUDE_CODE_CHILD_SESSION`
(`LOG.md:753-768`). The log does not say which restart carried which fix, and this note does not
guess.

**Neither figure is wrong; they answer different questions.**

| question | answer | why |
|---|---|---|
| When was the launch *attempted* / the screen sessions created? | **2026-08-26 14:45 KST** | `LOG.md:713` |
| When did the campaign that produced the record *begin*? | **2026-08-26 15:28:16 KST** | the only iteration with an exit line and a transcript |

**Use 15:28 for anything measured.** It is what the derived quantities already use: campaign
length **65.53 h** to the 09:00 KST bell (66.25 h from 14:45), SI-002's statement of how long the
campaign ran with no enforcement, and SI-001's polling-gap window *"between 2026-08-26 15:30 and
2026-08-27 07:26"*. **Do not describe the smoke as a 72-hour or 66-hour campaign**: §5 set **T**
at 09:00 KST on the third day rather than launch + 72 h, which is the 9.0 % silent shortfall
Rev 19 later fixed by making **T = launch + N × 24 h exactly**.

### 2.2 304.61 versus 300.741 CPU-h — **`usage.json:cpu_h` = 300.741 is authoritative**

The agent that filed at 89.6 % is **s01** (gated). 304.61 / 340 = 89.59 %; 300.741 / 340 =
88.45 %.

| figure | what it is | locus |
|---:|---|---|
| **304.61** | s01's own final total | `reps/smoke/collected/s01/LOG.md:780` *"Final compute: **304.61 of 340 CPU-h (89.6%)**, 35.4 CPU-h unspent."*; `…/FINAL_REPORT.md:27` *"2.1 Simulations — 304.61 of 340 CPU-h, 3,620 GCMC runs, zero failures"* |
| **300.741** | the harness meter at the bell | `reps/smoke/collected/s01/usage.json` — `{"cpu_h": 300.741, "cpu_h_basis": "job-records (single-core elapsed per finished run)", "cpu_h_runs_accounted": 3620}`; `final-watchdog.json` `fraction 0.8845, level "warn"`; `COLLECTION.md:58`; `SI_LEDGER.md` SI-001 closing table |

**The gap is a scope difference, and it is fully accounted.** s01's report gives its total as a
twelve-row batch table (`FINAL_REPORT.md:29-42`). **Eleven of those rows are GCMC batches and
they carry exactly 3,620 runs — the same 3,620 the harness meter accounted — summing to 300.49
CPU-h.** The twelfth row has **no runs at all**:

> `| — | descriptor / gate passes, all 1,731 | — | 1,731 | — | 4.11 |`

Those are the `s01_geom_00..19` (G3 pre-sim screen + descriptors) and `s01_oms_0..3` (G4
exposed-metal screen) jobs in `reps/smoke/collected/s01/JOBS.md`. They are real cluster jobs, but
they are not GCMC runs, so they produce no finished-GCMC job record for the meter to sum.

    304.61  s01's total
    − 4.11  descriptor / gate passes  (not GCMC; invisible to the meter)
    = 300.50  GCMC leg, s01's own accounting
    vs 300.741  GCMC leg, harness meter        difference 0.25 CPU-h = 0.08 %

**So the two instruments agree on the GCMC leg to 0.08 %** — residual rounding across twelve
two-decimal batch figures — **and the entire 3.87 CPU-h discrepancy is the 4.11 CPU-h of
non-GCMC cluster work.** This is **not** the s02-shaped disagreement: s02's self-report and the
meter differ by **1.65×** on the same work, which SI-001 leaves *"open, deliberately"* as a
Q-item under SI-013. s01's is a difference in what is being counted, and it resolves.

**Which is authoritative, and for what.**

- **For the charter §4 cap: `usage.json:cpu_h` = 300.741.** SI-001 installed that basis as the
  recorded meter (*"The recorded meter is now the job-record basis"*); `harness/watchdog.py:110`
  reads it for the hard stop (`stop_used = u["cpu_h"]  # validated: finished jobs only`); and
  `prereg/compute_meter_RATIFIED.md` §3 states it outright: *"The authoritative meter is
  `usage.json:cpu_h` — 'finished-job CPU-h (validated)'."* It is the figure `COLLECTION.md` and
  SI-001's closing table already report, at **88.5 %, `warn`**.
- **304.61 is not wrong** — it is a wider quantity, s01's total cluster burn, and it is the
  better number if the SI wants *"compute this agent consumed"* rather than *"compute the §4 cap
  was enforced against"*. It should be labelled as such, not presented as a competing estimate of
  the same thing.
- **Nothing turns on the choice.** 88.5 % and 89.6 % are both inside the warn band and both under
  the 340 CPU-h cap, and smoke compute enforcement was **log-only** under SI-001 regardless.

**One thing the SI should state rather than leave implicit:** the authoritative meter's scope is
narrower than "compute used". On s01 it misses **4.11 CPU-h — 1.3 % of the agent's burn and
1.2 % of the cap** — because descriptor and gate work does not run as GCMC. A Methods sentence
saying the meter measures compute consumption would overstate it; it measures **finished GCMC
job records**, which is what the cap was ratified against.

---

## 3. Was a revision record appended at the foot of the delivered charter?

**Every delivered charter, both arms, carries the header line that promises one:**

> *(Revision record at the foot of this document. Bracketed values not yet listed there are
> still unset.)*

— `prereg/charter_v0.9.md:3`, in the common body, before any arm split.

**The promise is kept for one arm and broken for the other.**

| arm | agents | revision record present? | rendered size |
|---|---|---|---:|
| **gated** (checked) | rep01, rep05, rep06, rep07, rep08, rep11, rep12, rep13 — **8** | **YES**, 40 dated rows, current through Rev 25 | 31,082 B |
| **ungated** (unchecked) | rep02, rep03, rep04, rep09, rep10, rep15, rep16, rep17 — **8** | **NO — absent entirely** | 14,416 B |

Verified by running the provisioning pipeline read-only, exactly as
`harness/rerender_charter.py` does — `split_charter(render_phase_prose(render_phase_rows(src,
'main'), 'main'), arm)` — and searching the two rendered strings. Independently confirmed against
the extract already in this directory: `charter_v1_common.md` **is** the ungated render, and it
ends at §9 with `grep -c "REVISION RECORD"` returning **0**.

**The cause is structural, not a rendering bug.** `prereg/charter_v0.9.md` is ordered
§1–§9 (`:1-147`) → **`# APPENDIX A — AUDIT GATES`** (`:148`) → **`# REVISION RECORD`** (`:201`) →
three closing notes (`:248-287`). `provision.py:149` `split_charter` returns, for the ungated arm,
everything **before the appendix marker**:

> *"Gated arm gets the whole charter. Ungated gets everything before Appendix A. … The ungated
> charter simply ends at section 9."*

The revision record sits **after** Appendix A, so the cut that removes the treatment removes the
revision record with it. The header promising it sits **before** the cut and survives in both.

**Three further sections go the same way, and one of them is not gate material.** The ungated
render also loses **"Note on the G3 density bounds"** and **"Note on G7"** (both Appendix A
scoped, arguably correct to drop) and **"Note on tail corrections"** (`:277`), which is about
**§3** — the common-core protocol both arms hold. That note carries the evidentiary basis for a
pinned §3 setting: *"4,560 interaction pairs, every one `tailcorrection: no`, across seven
independent archived runs"*. Eight replicates were governed by a §3 that pins tail corrections
off without holding the paragraph that says why. **This is the same shape as the defect Rev 22
was written to repair** — a general statement about the pinned protocol reaching one arm only
because of where it happened to sit relative to the appendix cut — and it was not caught, because
Rev 22 moved a sentence *out of* the gate while these sit *after* it.

**Consequences for the SI.**

1. A statement that the delivered charter carried its own revision record is **true of eight
   agents and false of eight**. State the arm.
2. **The gated charter's larger size is not all treatment.** Rev 23 and Rev 25 both justify
   common-core placement by the byte asymmetry — *"the gated charter is 28,929 bytes against the
   ungated arm's 13,109 — 15,820 bytes of treatment text that enter context on turn one"*. At
   HEAD the two renders are 31,082 and 14,416 B, a 16,666 B gap, of which the revision record and
   the three notes are **9,500 B — 57 %** (revision record 7,077 B, notes 2,423 B). Appendix A itself is **7,156 B** in the
   current render (7,150 B as extracted to `charter_v1_appendixA.md`). Any per-arm cost decomposition that attributes the whole
   difference to Appendix A attributes **2.33×** more to the treatment than Appendix A
   accounts for.
3. The ungated arm could not verify the revision numbering it was nonetheless notified about:
   the Rev 24 and Rev 25 INBOX notices name revisions by number, and the clause text itself
   carries `(Rev 25)`, but eight agents had no table in which to look a number up.

**What is *not* claimed here.** No replicate is known to have asked for the revision record and
failed to find it, and no `[CHARTER-READ]` entry in `charter_read_entries.csv` turns on it. The
finding is that the header asserts something untrue for half the fleet, and that the omission is
wider than Appendix A.
