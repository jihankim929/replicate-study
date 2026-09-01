# COLLECTION — main phase, all sixteen replicates

**Pulled and verified 2026-09-01T19:33:09Z.** All sixteen main-phase records are off the cluster and in
`reps/main/collected/`. **Every one reproduces `harness/state/sealed_attestation_20260902.json`
exactly — 16/16, zero drift.**

Collection is **read-only with respect to the workspaces**. Every remote command in
`harness/pull_collect.sh` is `rsync`-out, `sha256sum` or `git log`. Nothing was written into
`/home1/users/Bei/ws/` by this procedure.

---

## 1. Why this ran three days after the campaign closed

**The harness had no pull.** `transfer.sh` only ever pushes; `collect.sh` reads from a *local*
workspace that the main phase never had, because the sixteen lived on `bnode0` for their entire
campaign. The smoke was pulled by hand on the macOS host that has since been retired, so the
inbound half of collection left with it. This is SI-012's finding — the layer did not travel —
and it is why `screen_launch.sh` refused at its §7.1 barrier twice before tonight.

`harness/pull_collect.sh` is that missing half. It was written to be the pull and nothing more.

## 2. Procedure, in the order it ran

| # | Step | Result |
|---|---|---|
| 1 | `rsync` of the eight sealed record files + `AUDIT.jsonl` for each of 16 workspaces | 13.8 MB |
| 2 | `git log` captured **remotely** — the `.git` trees are not pulled | per-replicate `git-log.txt` |
| 3 | **Independent remote fingerprint**, taken *after* the copy | `BELL_FINGERPRINT.log` |
| 4 | **Verification against the sealed attestation** | **16/16 exact, 0 mismatch** |
| 5 | This file | — |

**Step 4 is why steps 1–3 can be trusted, and it is stricter than the smoke's.** The smoke
verified its local copy against a fingerprint it had taken itself minutes earlier. This
verification is against a seal taken at **2026-09-01T17:32Z**, hours before the pull existed,
over a manifest fixed before any of these bytes moved. The check recomputes the seal's own
construction — `sha256sum` over the eight files in the seal's order, that output text hashed —
from the **pulled local copies**, and compares. A pull that diverged in one byte of one file
would fail it, and the script halts rather than warns.

**`BELL_FINGERPRINT.log` is retained for a failure that did not occur:** had a record mismatched,
it distinguishes a bad transfer (local differs from remote) from a workspace that changed after
the seal (local matches remote, and the *seal* disagrees). Those are different findings.

## 3. What was collected

| rep | `REPORT.md` | `LOG.md` | commits | `AUDIT.jsonl` | final CPU-h | seal |
|---|---:|---:|---:|---:|---:|---|
| rep01 | 34,521 B | 102,013 B | 79 | 29 | 821.634 | `3e5975cb57cff5f1…` |
| rep02 | 45,584 B | 121,760 B | 106 | absent | 1,116.841 | `62018b563a3c2ce7…` |
| rep03 | 37,706 B | 142,620 B | 94 | absent | 344.996 | `9d34b877d8f42b34…` |
| rep04 | 17,267 B | 73,135 B | 60 | absent | 1,071.482 | `7782ce2370548708…` |
| rep05 | 23,590 B | 88,459 B | 64 | 2,911 | 0.000 | `5d7c5ba92b4990b2…` |
| rep06 | 29,428 B | 94,361 B | 110 | 767 | 660.991 | `4a1b761e2fcae90b…` |
| rep07 | 22,507 B | 171,546 B | 134 | 2,254 | 1,490.025 | `5cb0088987e06f21…` |
| rep08 | 19,252 B | 76,316 B | 69 | 12,587 | 1,064.844 | `68855abbbf81c1f2…` |
| rep09 | 18,448 B | 92,767 B | 58 | absent | 592.761 | `f996070eea31dab5…` |
| rep10 | 35,534 B | 110,005 B | 84 | absent | 315.436 | `5c0da6accc150475…` |
| rep11 | 17,491 B | 104,643 B | 86 | 134 | 1,931.693 | `a21181c1a313d74c…` |
| rep12 | 20,711 B | 87,668 B | 48 | 64 | 1,580.566 | `4d02cf3ed6c1411f…` |
| rep13 | 25,905 B | 128,648 B | 79 | 42 | 989.817 | `6f9c7f0f081348fa…` |
| rep15 | 33,453 B | 118,806 B | 209 | absent | 1,222.695 | `73a175606b1633b5…` |
| rep16 | 25,585 B | 60,990 B | 80 | absent | 227.855 | `7b593d6425d4abcf…` |
| rep17 | 23,882 B | 106,961 B | 79 | absent | 914.067 | `cd37b685a31ba8ce…` |
| **total** | | | | | **14,345.703** | **16/16** |

**Every replicate filed.** There is no `MISSING_FINAL_REPORT` in this collection: all sixteen
carry a `REPORT.md` under the §7 name, which is also the name the seal hashes and the name
§7.1's gate reads. `FINAL_REPORT.md` is written **as a copy, not a move**, for the smoke's shape;
`REPORT.md` remains binding and is never renamed.

**Commit counts match the seal for all sixteen** — they are a sealed field, so a rewritten
history would have failed step 4, not merely been noted here.

## 4. What is NOT in this collection, and why

**The workspaces themselves were not pulled.** The smoke pulled 3.6 GB of full trees; this pull
is 13.8 MB of record. That is a deliberate narrowing to what the seal covers and what
§7.1 gates on, taken because the sixteen carry results, `db/` and `toolchain/` measured in tens
of GB, and because nothing downstream reads them: the screen runs in `/home1/users/Bei/screen/`
and §7.2 forbids it any view of a replicate workspace.

**Consequences, stated rather than discovered later:**

- **No local isolation audit.** The smoke's ran only because whole workspaces were on local disk,
  and its first output was six false positives produced by collection itself (absolute symlinks
  resolved against the wrong root). Not run here; not silently reported as clean either.
- **The results are still only on the cluster.** They are outside the seal, outside this
  collection, and outside §7.1's scope. If they are wanted off `bnode0`, that is a separate pull
  against a separate authority, and it should be asked for as one.

## 5. Contents

```
collected/
  COLLECTION.md                this file
  BELL_FINGERPRINT.log         independent remote sha256, taken after the copy
  <rep>/
    REPORT.md                  the §7 report — SEALED NAME, binding, never renamed
    FINAL_REPORT.md            copy under the smoke's normalised name
    REPORT_FILENAME_AS_FILED   the name the replicate actually used
    LOG.md STATE.md JOBS.md    the §6 binding record
    ESCALATIONS.md INBOX.md    the §8 channel, both directions
    WORKSPACE.json usage.json  operational parameters and the meters as they stood
    AUDIT.jsonl                where the replicate kept one
    git-log.txt                full commit history, captured remotely
```

**Fleet final: 14,345.703 CPU-h**, the accounting sealed at 17:32Z and reproduced here.
**rep05 remains 0.000 CPU-h against 3 finished jobs** — SI-021's family, carried forward as a
data gap and never as zero compute.

— Bei (harness)
