# STATUS — live view of the running smoke campaign

*Machine-generated. Refreshed by `harness/poll.sh` each watchdog cycle.*

<!-- DIVERGENCE-PANEL:BEGIN -->
## Mechanical divergence panel

Refreshed 2026-08-26 22:27:13Z (07:27 KST) — every watchdog cycle.

Arms are relabelled **A** / **B** in randomized order. The mapping was drawn once from
OS randomness and sealed in `harness/divergence_map.SEALED.json`
(sha256 `dd49fc9492a876f56de2804d0250d362`). It is not to be opened until collection.

| Quantity | A | B |
|---|---:|---:|
| First submission (UTC) | 2026-08-26 06:36Z | 2026-08-26 06:38Z |
| Elapsed since first submission | 15.8 h | 15.8 h |
| Jobs submitted | 183 | 108 |
| Jobs completed | 144 | 100 |
| Jobs running | 39 | 8 |
| Jobs queued | 0 | 0 |
| Distinct structures touched | 1,731 | 765 |
| — collapsed over charge-variant twins | 1,055 | 649 |
| Tasks across all jobs | 3,614 | 2,584 |
| Batch size — median / max | 39 / 39 | 21 / 73 |
| Batch-size distribution (size×jobs) | 1×50, 2×8, 4×8, 13×2, 14×2, 38×9, 39×80, unresolved×24 | 1×40, 9×7, 10×5, 21×4, 22×28, 72×21, 73×3 |
| Cumulative CPU-h — from run records | 183.1 | 381.6 |
| Cumulative CPU-h — from scheduler | 9.3 | 121.0 |
| Token burn (billable) | 4,182,977 | 646,274 |
| Token:CPU (tokens per CPU-h) | 22,848 | 1,694 |
| Resubmissions | 0 | 0 |

**Definitions.** *Jobs submitted* = job scripts carrying a `#PBS -N` line; *completed* = submitted − running − queued. *Distinct structures touched* = benchmark structures whose run directory holds simulation output; the collapsed row merges the coordinate-identical charge-variant pairs. *Batch size* = simulation tasks carried by one submitted job. *Resubmissions* = one job name submitted under more than one job id.

**Blind spots, stated rather than implied.** The scheduler drops a finished job from `qstat` and this account cannot read the PBS accounting log, so the scheduler CPU figure accounts only for jobs alive at a poll plus those the harvester caught leaving; the run-records figure is the more complete of the two and is single-core elapsed time per finished run. The resubmission ledger starts at its first poll — resubmissions earlier than that are not recoverable and are not counted. A job script written but never submitted would count as submitted, and therefore as completed.

**The blind is procedural, not cryptographic.** Per-replicate ledgers elsewhere in this repo carry some of the same quantities under their real ids, so the mapping is recoverable by anyone who goes looking. It holds because it is not looked at.
<!-- DIVERGENCE-PANEL:END -->
