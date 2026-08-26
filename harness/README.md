# harness/ — what each component enforces, and which charter clause it enforces

The harness is **infrastructure, not supervision** (charter §8: *"It handles infrastructure and
administers this charter. It will not answer scientific questions."*). Every component below
either mechanises a clause the charter already states, or reports a fact. None of them exercise
judgement over a replicate's science, and the one place discretion could creep in — the
escalation router — is deliberately built so that it cannot.

Run `./harness/selftest.sh` before any launch. **26 checks, all must pass.**

---

## Component → clause map

| Component | Enforces | Clause |
|---|---|---|
| `provision.py` | database delivered at `<workspace>/db/`, 1,731 structures | §1 |
| | checksums verified **on arrival** against the frozen manifest | §1 (integrity of "the provided database") |
| | Appendix A present for the gated arm, **omitted verbatim** for the other | Appendix A header |
| | `AUDIT_SCHEMA.md` + empty `AUDIT.jsonl` seeded for the gated arm only | Appendix A |
| | workspace is self-contained: files copied not symlinked, git repo with **no remote** | §4 "you operate exclusively inside [workspace path]" |
| | reads only from an explicit allowlist — `answer-key/` is structurally unreachable | study constitution (sealed material) |
| | leak scan of the built workspace, hard-fail + warn lists | see *Leak control* below |
| | seeds `LOG.md`, `STATE.md`, `JOBS.md` | §6 record-keeping |
| `watchdog.py` | usage warning at **75 %**, hard stop at **100 %**, compute and tokens alike | §4 |
| | hard stop **holds** the queue, never deletes jobs | §4 + §6 (evidence must survive) |
| | queued-job cap | §4 cluster etiquette |
| | workspace isolation audit: symlink escapes, git remotes, sealed material, paths back | §4 "prohibited and audited" |
| | liveness + `STATE.md` staleness, **reported not punished** | §6 "updated before any long wait" |
| `escalate.py` | the §8 category table, transcribed verbatim into `config.ESC_TABLE` | §8 |
| | `scientific` → the exact chartered sentence, auto-replied | §8 |
| | `infra` → queued for repair; `charter` → queued for the PI | §8 (see *Why two are queued*) |
| | malformed → the format returned, never a guess at intent | §8 "There is no other channel" |
| | every escalation and response logged to `escalations.jsonl` | §6 |
| `launch.sh` | provisions both smoke replicates, verifies, prints an arm/charter-hash registry | §5 phase table, Appendix A |
| `collect.sh` | harvests the record; **absence of a final report is a finding, not an error** | §5 "mandatory at end, whatever state you are in" |
| | checks git history for amend/rebase | §6 "Never amend or rebase history" |
| | flags an empty `AUDIT.jsonl` alongside a filed report | Appendix A closing clause |
| `dirac.py` | PBS glue — `qas` not `qsub`, node group mandatory, `qhold` not `qdel` | cluster facts, prior campaign |
| `config.py` | refuses to launch on **unratified** placeholder values | study governance |

---

## Scheduling requirement — dynamic work-stealing, never even chunking

**PI ruling, 2026-08-26**, adopted from a measured finding: GCMC cost per run spans
**45 s to 15,190 s — a 338× spread — and is not predictable from structure size.**

Any scheme that divides N structures into K equal-count chunks will therefore have chunks
finishing hours apart, with most cores idle while one chunk grinds. Under a budget deliberately
set below the cost of a full screen (`prereg/placeholder_proposals.md` §R2.2), wasted
wall-clock is wasted science.

**Requirement on any submission wrapper written for this study:** workers pull the next unit
from a shared queue as they free up. No worker is assigned a fixed slice in advance.
`dirac.submit()` is the per-unit primitive this is built from; the puller itself is stubbed with
the rest of the Dirac glue until the account lands.

*Note this is a harness requirement, not a charter clause.* It binds the infrastructure. It is
not imposed on replicates — how a replicate schedules its own work is its business, and the
choice is itself observable.

---

## Leak control

Two-list scan, run against the **built workspace**, not the source:

- **HARD** (`config.LEAK_DENY_HARD`) — provisioning aborts. Study-design vocabulary and any
  file byte-identical to sealed material.
- **WARN** (`config.LEAK_DENY_WARN`) — printed, provisioning continues. These sit in documents
  Bei does not own; auto-editing the PI's charter would be worse than reporting it.

**One WARN is currently outstanding and needs a PI decision.** The Appendix A header reads
*"(gated arm only; omitted verbatim from the other arm)"*, so a gated replicate reading its own
charter learns that another arm exists under different rules. Suggested fix: drop the
parenthetical — `provision.py` already implements the arm split, so the instruction does not
need to live in the replicate-facing text. Rationale and the full leak history are in
`prereg/charter_revisions.md`.

Why this scan exists at all: **two of the three leaks found so far were introduced by Bei while
writing text whose purpose was to prevent leaks**, and both were caught by scanning the built
workspace rather than by reading the source. Review the output, not the input.

---

## Limits — what this harness does not do

Stated because a monitoring component that overstates its reach is worse than none.

1. **Read-auditing is partial.** `watchdog.audit_isolation()` catches escapes that leave a
   trace: symlinks, git remotes, sealed content, absolute paths in files. It **cannot** detect a
   read that left no artifact. Genuine read-auditing needs OS-level mediation — a read-only bind
   mount, or an audit subsystem. Until then §4's "reading ... outside your workspace is
   prohibited and audited" is enforced for *writing* and for *traces of reading*, not for
   reading as such.
2. **Budget metering trusts the replicate's ledger.** `usage.json` is written by the job
   wrapper. Once the cluster account lands this should be reconciled against `tracejob`
   `resources_used.cput`, which is authoritative. Until then a replicate that under-reports is
   not caught.
3. **Token metering has no source yet.** The basis is fixed (input + output + cache-creation,
   cache-reads excluded) but nothing populates it. It needs wiring to whatever meters the
   replicate's sessions.
4. **All Dirac glue is stubbed.** Every function in `dirac.py` prints what it would do and
   returns `DIRAC-STUB`. Nothing pretends to have succeeded.
5. **Main-phase arms are unassigned.** `config.RATIFIED["arms"]` covers `s01`/`s02` only;
   `arm_of()` raises for main-phase ids. The 20-replicate split is not yet ruled.
6. **Budgets are unratified.** `config.PROPOSED` values block a real launch by design. The
   smoke cannot start until the PI ratifies them.

---

## Everything is dry-runnable

```bash
./harness/selftest.sh                              # 26 checks against a throwaway mock
./harness/launch.sh --dry-run --dest /tmp/mock     # both arms, 25-structure db, no cluster
python3 harness/watchdog.py /tmp/mock/s01 --dry-run
python3 harness/escalate.py /tmp/mock/s01 --dry-run
./harness/collect.sh --dest /tmp/mock --out /tmp/mock/collected
```

A real run differs only in dropping `--dry-run` and `--db-limit` — and will refuse to start
while the budgets remain unratified.
