# PROPOSED — restoring a writer to the compute meter

**Status: PROPOSED, not applied.** Written 2026-08-31 on the PI's REPORT 007 ruling: *"Compute
meter: investigate and propose — reconcile PBS cput against per-job wall×cores on finished jobs;
if the undercount is real, propose a corrected basis for ratification. Enforcement continues on
the current meter meanwhile."* Enforcement is unchanged by this document.

## 1. What rep02 reported

> *"usage.json cpu_h_scheduler reads 107.5 CPU-h where my workers' own per-task wall times sum to
> 223.6 — PBS cput appears to lose forked children."*

The **observation** is right. The **diagnosis** is not, and the real defect is worse.

## 2. The reconciliation the ruling asked for

Measured 2026-08-30T19:2xZ over every running fleet job that reports both quantities in
`qstat -f` — 75 jobs across thirteen replicates:

| | |
|---|---|
| Σ `resources_used.cput` | **14,384 CPU-h** |
| Σ `resources_used.walltime × ncpus` | **4,758 CPU-h** |
| ratio wall×ncpus / cput | **0.33** |

**cput is roughly three times wall×ncpus, not a third of it.** Per replicate the ratio runs 0.13
to 1.00 and never exceeds 1 except where the sample is tiny (rep03, three jobs). PBS is therefore
not losing forked children — it is capturing processes *beyond* the job's `ncpus` allocation,
which a wall×cores estimate would miss entirely. The hypothesis in rep02's escalation is not
supported by the scheduler's own numbers.

## 3. What is actually wrong, and it is not a rate

`cpu_h_scheduler` undercounts for the reason the record already established (SI-021, PI ruling
2026-08-27): PBS drops a finished job from `qstat` within seconds, and this account cannot read
the accounting log, so a 30-minute poller sees only what is still alive. It is a **sampling**
undercount, not an accounting one, and it is exactly why the recorded meter was changed away from
it. `cpu_h_scheduler` is an estimate the record already classifies as non-authoritative.

**The authoritative meter is `usage.json:cpu_h` — "finished-job CPU-h (validated)" — and it has
had no writer since the smoke was archived.**

- `watchdog.py:110` takes the hard stop from `u["cpu_h"]`.
- The only non-mock writer of `cpu_h` in the repository is `divergence_collect.py:305`, inside the
  A/B divergence collector.
- That panel was **retired at the smoke purge**. Nothing replaced its `--write-usage` path.
- Consequence, verified: `cpu_h` is **absent from every workspace's `usage.json`**, so
  `meter_has_data` is false for all sixteen, every compute row reads `unaccounted`, and the
  1,610 CPU-h cap has no data behind it at all.

STATE records this as *"SI-021 working as fixed — a meter with no data says so instead of saying
0.0 OK — and it will resolve itself as jobs land."* **It will not resolve itself.** Jobs have
landed and it has not resolved, because the absence is a missing writer and not a missing job.

## 4. The data exists and is being collected

`harvest_cput.sh` banks each finished job's cput into `<ws>/cput_finished.txt` on its way out of
the queue, and has been doing so correctly. Read 2026-08-31:

| replicate | finished jobs banked | Σ CPU-h |
|---|---|---|
| rep01 | 10 | **567.89** |
| rep02 | 3 | **74.73** |
| rep07, rep15 | file absent — nothing harvested yet | — |

rep01 has 567.89 validated CPU-h of its 1,610 cap — **35 %** — and the panel has been reporting
`unaccounted` throughout.

## 5. The proposal

**Do not change the basis. Restore its writer.**

The ratified basis — finished-job CPU-h, validated — is correct and is already being collected.
One line of plumbing is missing:

> `meter_compute.sh` (which already writes `cpu_h_scheduler` and `queued_jobs` into the same
> file, over the same ssh, on the same poll) additionally writes
> **`cpu_h = Σ cput_finished.txt / 3600`**, rounded, into `usage.json`.

Properties, stated so the ratification is on the record:

1. **The definition of the meter does not move.** It remains finished-job CPU-h from PBS
   accounting, which is what was ratified. Only the writer changes.
2. **`cpu_h_scheduler` is kept and unchanged**, as SI-021 requires: the gap between the two is
   the evidence for why the basis changed, and a study that discards it cannot show its work.
3. **The direction of error while unfixed favours replicates**, as the ruling notes — a cap with
   no data never falsely stops anyone. It also never truly stops anyone, which is the risk on the
   other side: rep01 could pass 1,610 CPU-h with the panel still reading `unaccounted`.
4. **It should be applied to all sixteen at once or to none**, since a compute cap that binds for
   some replicates and not others is a treatment difference.

## 6. What this proposal does not cover

Unscheduled execution on the login node reaches neither meter — not `cpu_h`, not
`cpu_h_scheduler` — because it never enters PBS accounting at all. Restoring the writer does not
capture it. See `harness/state/observed_behavior/2026-08-31_login_node_execution.md`; rep05 was
running 25 concurrent simulations at a metered 0.0 CPU-h.
