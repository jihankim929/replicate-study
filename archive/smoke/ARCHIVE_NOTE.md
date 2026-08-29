# Smoke campaign — off-cluster archive — 2026-08-29

Archived and removed from the cluster under PI ruling 2026-08-29 (gate-halt rulings, item 6):
*"accept procedural isolation with the audit as detector … and remove the contamination surface
before waves."* Under one Unix account there is no permission-based isolation between replicates;
removing the material is the only mechanical part of the fix available this week. Separate cluster
accounts are recorded as the correct future fix, not achievable this week.

## What is held, and the difference between the two copies

**1. `reps/smoke/s01`, `reps/smoke/s02` — the collection.** The tree pulled at the 09:00 KST
deadline. This is the scientific record.

- **50,598 / 50,598** files verified against `reps/smoke/PULLED_MANIFEST.sha256`, zero mismatches.
- **17 / 17** record files match `reps/smoke/BELL_FINGERPRINT_0900KST.log` — the independent remote
  fingerprint taken at 09:00:03 KST — with **zero divergence**.

**2. `archive/smoke/s01.tar.gz`, `s02.tar.gz` — the raw snapshot at removal.** The cluster state as
it stood at deletion, hashed on the cluster and re-hashed after transfer.

| | entries | record files | toolchain | sha256 |
|---|---:|---:|---:|---|
| `s01.tar.gz` | 45,587 | 10 | 549 | `s01.tar.gz.sha256` |
| `s02.tar.gz` | 28,918 | 8 | 549 | `s02.tar.gz.sha256` |

**These two copies are not expected to be identical, and that is not a fault.** The snapshot was
taken ~10 h after the bell, so files the harness itself keeps writing — `usage.json`, the
divergence cache — have moved on, and `s01/runs/ticker.log` grew for three days after collection.
**The collection is authoritative for the record; the snapshot is authoritative for what was
deleted.**

## Orphan processes killed before archiving

Two background processes started by s01 outlived the campaign, the collection, and the retirement
of its session — the local `screen` kill did not reach a process running on the cluster.

| PID | started (KST) | elapsed at kill | command |
|---|---|---|---|
| 3048626 | 2026-08-26 16:30:02 | 3 d 02:05:21 | `bash -c cd /home1/users/Bei/ws/s01 && nohup bash bin/ticker.sh > runs/ticker.log` |
| 3048628 | 2026-08-26 16:30:02 | 3 d 02:05:21 | `bash bin/ticker.sh` |

Killed 2026-08-29 ~18:35 KST. A third PID appeared in the same listing and was **Bei's own kill
command matching its own arguments** — it killed its own shell, which is why the count first read
three. Not a replicate process.

## Two defects this exposed in Bei's own tooling

**The first archive attempt exited 0 having copied nothing.** An ad-hoc `tar`/`scp`/`ls` pipeline:
`scp` failed on the network outage, the trailing `ls` succeeded, and the shell returned 0. This is
the same silent-success shape filed against RASPA the same hour. Replaced by
`harness/archive_smoke.sh`, which asserts every step and orders them so the destructive one runs
last — verify what is held → snapshot → pull → verify the pull → only then delete.

**The first removal pass stripped s01 to its toolchain and stopped.** The toolchain is provisioned
read-only (`dr-xr-xr-x`), and `rm` cannot unlink inside a directory it has no write bit on: 494
permission-denied files. Because the ordering put verification before deletion, **the verified
archive already existed when this happened** and nothing was at risk. The script now `chmod -R u+w`
before removing.
