# Four SI queries, answered read-only — 2026-09-06

*Companion to `charter_revisions.csv`, which was extended through Rev 25 in the same pass.
Every quantity below carries its locus. Nothing in the study record was modified to produce
this file; the only writes in this pass were `charter_revisions.csv`, this file, and the
`README.md` entries for both.*

*Amended later on 2026-09-06 with the two sub-queries the first pass did not cover: **§2.3**,
the 38.6 vs 39.16 h blocked figures (a different agent from §2.2 — s02, not s01), and **§3**,
which charter state Supplementary Text S1 actually is. §4 gained the launch-state row counts
and the fact that no delivered `CHARTER.md` was collected, so the answer is a reconstruction.*

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

## 2. Smoke phase — the two launch times, the two CPU-h figures, and the two blocked durations

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


### 2.3 38.6 versus 39.16 h blocked — **39.16 h is authoritative**

**First, a scope correction the SI should make explicitly: this pair is about a different agent
from §2.2.** The 304.61 / 300.741 figures belong to **s01** (gated), the agent that filed at
89.6 %. The blocked hours belong to **s02** (ungated), the arm that met the spend-limit modal —
`usage.json` `cpu_h 796.754`, `tokens 646,274`, against s01's `4,200,806`. Nothing in the
blocked-time accounting touches the 89.6 % filer, and a sentence that runs the two together
reads as one agent's record.

| figure | what it is | locus |
|---:|---|---|
| **~38.6 h** | SI-006's **in-flight** figure, taken while the block was still in force | `SI_LEDGER.md:355` (observation table, *"Heartbeat frozen 38.6 h"*), `:359`, `:401`, `:450`, `:683`; `LOG.md:929`, `:975`; `STATE.md:818` |
| **39.16 h** | the **closed** measurement at collection, from the two session transcripts | `SI_LEDGER.md:189` — *"\| **Freeze duration** \| **39.16 h** \|"*, in SI-004's *"Closed at collection — 2026-08-29 09:00 KST"* block |

**They share a start and differ only in where they stop.** Both run from the last transcript
write of session `32fe5673`, **2026-08-26 16:57 KST**.

- 16:57 KST **+ 38.6 h = 2026-08-28 07:33 KST**, the moment SI-006 was written. The block had
  not been cleared yet, so the figure is *how long has this been going on* — and it is written
  with a `~`.
- 16:57 KST **→ the restart at 2026-08-28 08:06:43 KST = 39.1619 h**, which is the ledger's
  **39.16**.

The 0.56 h between them is the **~33 minutes from SI-006 being written to the repair being
executed**. The later figure is not a correction of the earlier one's measurement; it is the
same measurement with an end point.

**The denominators differ too, and that is the part that was genuinely wrong.** SI-006 stated the
freeze as *"~38.6 h of a 72 h campaign"* — 53.6 %. **The smoke campaign is 65.53 h, not 72**: §5
set **T** at 09:00 KST on the third day against a 15:28 launch (§2.1), the 9.0 % silent shortfall
Rev 19 later repaired. The record issues the restatement itself, twice — *"Restated on the true
denominator, the freeze was **59.7 %** of the campaign, not 53.6 %"* (`SI_LEDGER.md:200-201`) and
*"SI-006's \"38.6 h of a 72 h campaign\" is restated as **39.16 h of 65.53 h — 59.7 %**"*
(`LOG.md:1503`). Recomputed here: 39.1619 / 65.53 = **59.76 %**.

**Use 39.16 h and 59.7 %.** 38.6 h is a live status figure already superseded by its own ledger;
quoting it — and especially quoting *53.6 % of 72 h* — reproduces a denominator the study has
retracted. What both figures agree on is the finding: **s02 worked for about 1.5 h and sat at an
unanswered modal for the rest**, so the smoke has *"one usable trajectory, not two"*
(`SI_LEDGER.md:450`).

---

## 3. Which charter state is Supplementary Text S1? — **the cumulative post-seal text, current through Rev 25. It is not the launch-state rendering.**

The charter extracts in this directory — `charter_v1_common.md` (the ungated body) and
`charter_v1_appendixA.md` — were rendered from **`prereg/charter_v0.9.md` as it stands in the
working tree**. That source is **four revisions ahead of what any replicate launched with, and
one revision ahead of anything committed to this repository.**

**The recorded source hash settles it.** `README.md` gives the extracts' source as
`205d7d8ba8f9e7a6eab6507aa63ea66ccdbd7136fe372462ba9e31cfb52d3f24`. That is the working-tree
file, and it is not any commit:

```
worktree  prereg/charter_v0.9.md   205d7d8b…   <- the extract's source, carries Rev 25
HEAD      prereg/charter_v0.9.md   1d23c48b…   <- stops at Rev 24
```

Re-rendering the working-tree source through the provisioning pipeline read-only reproduces the
extract exactly: the ungated render is **14,416 B, sha256 `1274611fcf94fe11…`** — byte-identical
to `charter_v1_common.md`'s recorded size and hash. The extract is a **re-render of today's
source**, not a copy of a delivered artefact.

**The four charter states, all rendered here through the same pipeline
(`split_charter(render_phase_prose(render_phase_rows(src,'main'),'main'), arm)`):**

| charter source | last revision | gated B | ungated B | revision-record rows (gated) |
|---|---|---:|---:|---:|
| `b1fac28` — rep01 at provisioning, 2026-08-29 14:07 KST | **Rev 20** | 25,649 | 11,487 | 33 |
| `1d39111` — rep02–rep17 at provisioning, 19:15–19:20 KST | **Rev 21** | 26,861 | 11,487 | 35 |
| `4d941e6` — HEAD | **Rev 24** | 29,959 | 13,670 | 39 |
| **working tree — the extract's source** | **Rev 25** | **31,082** | **14,416** | **40** |

**So the extract corresponds to no agent's launch state.** rep01 launched on a charter through
**Rev 20**; the fifteen wave replicates launched on one through **Rev 21**. Rev 22–25 reached
them afterwards by re-render and INBOX notice, on the schedule in `charter_revisions.csv`. The
extract is the **end state**: what the fifteen live replicates held after the 2026-08-31 Rev 25
render — and **rep17 never held it at all**, having filed and closed at 2026-08-30T19:59:34Z,
9 min 44 s before the Rev 25 notice went out.

**Two consequences for the SI.**

1. **Label S1 as the charter's final state, not as what the agents were launched with.** A
   caption reading *"the charter as delivered"* is true of fifteen replicates at the end of their
   campaigns, false of all sixteen at launch, and false of rep17 throughout. The honest caption
   is *"charter v1.0 as amended through Rev 25"*, with the launch states named separately —
   they are in `charter_revisions.csv`'s `seal_position` and `delivered_when` columns.
2. **S1 reproduces from an uncommitted working tree.** Rev 25's charter row (`:246`) and its
   narrative (`charter_revisions.md:1080`) exist only as working-tree modifications; **no commit
   in this repository carries them** (`README.md` disposition 2). The governing text the agents
   actually held is therefore *ahead of* the committed record, and anyone regenerating S1 from a
   clean checkout of HEAD will get the **Rev 24** render — 29,959 / 13,670 B, 39 rows — and will
   not be able to tell from the repository that it differs. **Commit Rev 25, or state in the SI
   that S1 was rendered from an uncommitted source and give the hash.**

---

## 4. Was a revision record appended at the foot of the delivered charter?

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

**Where it is, exactly.** In the gated render the revision record is the block headed
`# REVISION RECORD`, which opens after Appendix A ends and runs to the first `## Note on…`
heading — **7,077 B, 40 dated rows**, the last of them Rev 25. In the charter source it is
`prereg/charter_v0.9.md:201-247`, with the Rev 25 row at `:246`. It is a *table*, one row per
revision, dated and attributed, not prose.

**But the row count is the count at the END of the campaign, not at launch.** The rendering above
is made from the working-tree source, which carries Rev 25 (§3). Re-rendering the sources the
replicates were actually provisioned from gives the same structural answer and a different table:

| charter source | last rev | gated: revision record | rows | ungated: revision record |
|---|---|---|---:|---|
| `b1fac28` — rep01 at provisioning | Rev 20 | present | **33** | **absent** |
| `1d39111` — rep02–rep17 at provisioning | Rev 21 | present | **35** | **absent** |
| working tree — the extract | Rev 25 | present | **40** | **absent** |

**The ungated arm has no revision record in any state**, so the finding is not an artefact of
which snapshot is rendered. The gated arm's table grew from 33 rows to 40 across the campaign.

**One caveat on the whole of this answer: no delivered `CHARTER.md` was collected.** The sixteen
workspaces under `reps/main/collected/` carry `REPORT.md`, `LOG.md`, `STATE.md`, `INBOX.md`,
`AUDIT.jsonl`, `JOBS.md`, `usage.json`, `WORKSPACE.json`, `ESCALATIONS.md` and `git-log.txt` —
and **no charter**. `find . -name "CHARTER*.md"` returns one file in the whole repository, the
smoke's `CHARTER_READ_HARVEST.md`. So every statement here about what a replicate held is a
**re-render from the charter source through the provisioning pipeline**, not a reading of the
artefact as delivered. The re-render is the same code path `rerender_charter.py` used to write
those files and it reproduces `charter_v1_common.md` byte-for-byte, so the reconstruction is
sound — but the delivered artefacts themselves are gone, and the SI should say *reconstructed*
rather than *as delivered*. **Collecting `CHARTER.md` is a one-line change to the collector and
would have made this question a `diff`.**

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
wider than Appendix A. Nor is the byte decomposition an estimate: the four
segments close on the gap exactly — Appendix A **7,156** + revision record **7,077** + the three
notes **2,423** + a **10 B** `---`/`---` separator pair that `split_charter` trims from the
ungated arm = **16,666 B**, and the ungated render is a byte-exact prefix of the gated one up to
that point.
