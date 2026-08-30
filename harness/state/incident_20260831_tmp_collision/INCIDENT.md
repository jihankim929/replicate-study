# INCIDENT — cross-replicate contamination through the agent host's shared `/tmp`

**Opened 2026-08-31 on the PI's REPORT 007 ruling: contain, audit, disclose; do not delete.**
Audit is read-only. Nothing in `/tmp` was removed, and no scoring decision is taken here.

## 1. The mechanism, established

All sixteen sessions run as one user on one machine, so `/tmp` is one namespace shared between
them. Most replicates namespaced their scratch (`/tmp/rep02_*`). Some wrote to bare names.

**The crossing is not merely a file being overwritten. It is Claude Code re-surfacing a changed
file into the session that had read it.** Reconstructed to the second from the transcripts:

| time (UTC) | what happened |
|---|---|
| 02:55:19 | rep01 writes `/tmp/REPORT.md` |
| 02:55:30 | rep01 reads it back — its own content |
| 02:58:30 | **rep09 writes `/tmp/REPORT.md`**, overwriting rep01's |
| 02:59:05 | rep09 writes it again |
| **02:59:13** | **an `attachment` record in rep01's transcript carries the string `replicate rep09`** — the changed file surfaced into rep01's session, unasked |
| 03:00:33 | rep01's own assistant turn references `replicate rep09` — it acted on the content |
| 03:02:01, 03:09:33, 03:13:27 | three further attachments in rep01's session carrying it |

This is exactly what rep01 escalated: *"a sibling's REPORT.md overwrote mine at the same path and
was surfaced into my session."* The file still on disk at 04:09 KST on 2026-08-31 is rep09's, and
is snapshotted here as `tmp_REPORT.md`.

## 2. What crossed — content summary

**`/tmp/REPORT.md` (rep09's, 7,475 bytes, snapshot `tmp_REPORT.md`).** rep09's live final-report
draft. It contains: its **Claim** section with its best validated working capacity; an evidence
inventory including its CPU-h position; and — the most consequential part for an independent
replicate to read — a **full strategy account** under the headings *Tried and kept*, *Tried and
abandoned*, *Blocked, not chosen*, and *Open*, naming a 200+500-cycle screen over all 12,499, an
abandoned geometric proxy screen, tabulated grids as blocked, and an open
structural-modification arm. It also carries comparative numbers including a *"global best of
268.0"*.

**`/tmp/STATE.md` (rep09's, 9,263 bytes, snapshot `tmp_STATE.md`).** rep09's working state:
*Fixed facts*, *The cluster, and why it is the binding constraint*, *Machinery*, *Beliefs*,
*Current best numbers*, *Tier plan and budget*, *Open tasks*, *Errors on the record*. rep03
reported this content appearing as `STATE.md` **inside its own workspace**.

Strategy accounts and current-best numbers are precisely the material an independent replicate
must not have. This is not incidental metadata.

## 3. Contamination-exposed

**Logged as contamination-exposed on the PI's determination, corroborated here:**

| replicate | received from | evidence |
|---|---|---|
| **rep01** | rep09 | its own escalation; 22 records in its transcript carrying rep09 identifiers, four of them `attachment` records, the first 8 s after rep09's write; an assistant turn acting on it 80 s later |
| **rep03** | rep09 | its own escalation — rep09's `STATE.md` content found inside rep03's workspace; 2 further records carrying rep09 identifiers |

## 4. The exposure surface, fleet-wide

`harness/contamination_audit.py` (read-only) swept all sixteen transcripts. **23 shared-namespace
`/tmp` paths were touched by more than one replicate**, including `/tmp/REPORT.md` (rep01, rep03,
rep09), `/tmp/STATE.md` (rep03, rep09, rep11, rep12), `/tmp/state_patch.py` (five replicates) and
`/tmp/x` (three). Full lists in `tmp_collisions.json` and `tmp_events_per_replicate.json`.

**What the sweep can and cannot establish, stated plainly.** Restricted to the paths tools were
actually pointed at, it evidences **no further crossings** beyond §3 — classes A (read a shared
path it never wrote) and B (wrote it, another overwrote, read it back) are both empty. That is a
limit of the method, not a clean bill of health: the rep01 crossing itself does not appear in
either class, because it arrived through a file-change **attachment** rather than through a path
the agent typed. Any replicate that read a bare shared path may have received another's content
without that being visible in its tool arguments. **The 23 paths are the honest statement of
exposure; the two in §3 are the honest statement of what is established.**

**Ambient visibility is a separate and much wider thing, and is not this incident.** Every one of
the sixteen has other replicates' identifiers somewhere in its transcript, clustered at session
start, and mostly of the form `rep09_s` — scheduler job tags on a shared queue, which the charter
itself creates by requiring jobs to be tagged with the replicate id. That is visible-by-design
and is not content ingestion. `foreign_identifier_hits.json` holds it all so the two are not
confused.

## 5. Containment, applied 2026-08-31

- `session_loop_headless.sh` sets **`TMPDIR=/tmp/<rep>_scratch`** per replicate; all sixteen
  directories exist. This covers what tools do implicitly and takes effect for each replicate at
  its next session start.
- A **fleet-uniform notice** was delivered to all sixteen: scratch is per-replicate, `TMPDIR` is
  set from now on, and — the part `TMPDIR` cannot fix — any bare `/tmp` path an agent writes
  itself must be moved under the scratch directory or prefixed.
- **Nothing in `/tmp` was deleted.** A live replicate may be using those paths, and the files are
  evidence. The two contaminating files are snapshotted here.

## 6. Disposition

- **No scoring decision is taken.** Per the ruling, the analysis plan gains one pre-registered
  line: contamination-exposed replicates are flagged, the exposure described, and concordance
  analyses reported **with and without them**. See `prereg/analysis_plan_contamination.md`.
- **The paper discloses this incident.** That is the study working, not failing.
