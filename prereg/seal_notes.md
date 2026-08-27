# SEAL NOTES — main run

*Opened 2026-08-28. Things that must be true, or known to be false, before charter v0.9
becomes v1.0 and the N=20 launch goes out. Every quantity here is reproducible from
`harness/config.py` (`horizon_derived`, `fleet_reachability`); nothing is transcribed.*

---

## S1. Fleet reachability — the per-replicate charter does not describe the fleet

Every quantity in charter §4 is written **per replicate**, but all 20 replicates submit from
**one cluster account** (`Bei`). PBS limits concurrent jobs per *user*, not per replicate, so
the fleet meets a ceiling no per-replicate reading of the charter reveals.

**Fleet demand, main run:** 20 × 1,600 CPU-h = **32,000 CPU-h in 10 days** = **133.33
concurrent single-core jobs sustained**, fleet-wide.

Three ceilings stack; the smallest governs:

| Ceiling | Value | Headroom over 133.33 | Status |
|---|---:|---:|---|
| PBS `max_user_run` (external) | **580** | 4.35× | **verified by config read 2026-08-28; burst test pending** |
| Harness study-wide ceiling (`watchdog.py --fleet`) | **160** | **1.20×** | **governing — see S2** |
| Sum of per-replicate caps (20 × 12) | 240 | 1.80× | ratified 2026-08-28 (Flag H) |

**The main run is reachable: 100% of the fleet compute budget is spendable.** The binding layer
is the harness's own 160, exactly as the PI ruled — the PBS setting is not what constrains it.

### S1.1 The premise of the run-limit ruling does not survive checking

The ruling of 2026-08-28 recorded *"the Lm 58 on the queues is an admin-imposed per-user cap"*
and proposed raising it. **On the evidence, there is no cap of 58.**

`qstat -q` prints its `Lm` column in a **two-character field**. PBS Pro 4.2.10 renders the
per-user run limit there, and a configured **580 displays as "58"**. Read directly instead of
off the display:

```
set server max_user_run = 580
set queue long  max_running = 580
set queue infi  max_running = 580
set queue dque  max_running = 580
set queue short max_running = 580
set server queue_centric_limits = False
```

`qmgr -c "print server"` in full contains **no limit hook and no other limit directive**, and
`qmgr -c "list queue long max_user_run"` returns nothing — the queue sets no override, so the
server's 580 applies. All four queues display an identical "58" despite differing in walltime
and node settings, which is what a shared 580 truncated identically looks like and not what
four independently-administered caps look like.

**Consequence: no admin request is needed.** Had 58 been real it would have mattered a great
deal — the fleet could have run only 58 concurrent jobs against the 133.33 it needs, making
**43.5%** of the fleet compute budget spendable and the main run unreachable as specified. It
is worth stating that counterfactual plainly, because it is the one this check was worth
running for.

### S1.2 Empirical verification — PREPARED, NOT RUN

`harness/verify_run_limit.sh` submits a controlled burst of short single-core sleep jobs past
58, samples concurrency, logs the observed ceiling to `harness/run_limit_probe.jsonl`, and
`qdel`s every probe job from an unconditional `EXIT` trap. `--dry-run` prints the plan and the
configured limits without submitting.

It is **not run** and is not called by `poll.sh`: it loads a shared queue (112 jobs from other
users were running at the check), and the PI gated it on confirming the admin change. Since the
admin change now appears unnecessary, the burst's remaining value is to convert S1.1 from a
documentary argument into a measurement. **Recommend running it once before seal** — it is
cheap, self-cleaning, and it is the difference between "the config says 580" and "the scheduler
let one account run 70 at once".

**Open until run.** If it observes a ceiling ≤ 58, S1's governing row changes to PBS and the
main run is **not** reachable as specified; that would have to be resolved before seal.

## S2. Flag I — the study-wide ceiling of 160 has the defect Flag H just fixed

**Raised 2026-08-28, not ruled.**

Flag H established the invariant: *the headroom ratio over sustained concurrency is the rule;
the numeral is not.* The study-wide ceiling of 160 was set in Rev 5 against the same 14-day
horizon that made the per-replicate cap 8, and it moved for the same reason:

| | 14 days | 10 days |
|---|---:|---:|
| Fleet sustained concurrency | 95.24 | **133.33** |
| Headroom at ceiling 160 | **1.68×** | **1.20×** |
| Per-replicate headroom at cap 8 | 1.68× | 1.20× |

The two rows are identical because they are the same arithmetic at two scales. Applying the
ratified invariant (~1.7–1.8×) to the fleet gives **227–240**, and **240 is exactly 20 × 12** —
the sum of the per-replicate caps just ratified, and exactly 1.80×. The three ceilings would
then agree instead of the harness silently contradicting its own per-replicate ruling.

| Ceiling | Headroom | Capacity | Study share of queue at 112 other jobs | % of PBS 580 |
|---:|---:|---:|---:|---:|
| 160 (current) | 1.20× | 38,400 CPU-h | 59% | 28% |
| 227 | 1.70× | 54,480 CPU-h | 67% | 39% |
| **240 (recommended)** | **1.80×** | **57,600 CPU-h** | **68%** | **41%** |

**The counter-argument is crowding, and it is real.** Rev 5 built this ceiling so *"the study
can never crowd the shared queue however individual replicates behave."* At 240 the study would
be ~68% of concurrent load against the ~112 jobs other users were running, up from ~59%. That
is a judgement about being a good cluster citizen, not an arithmetic question, and it is the
PI's to make.

**What should not happen is leaving it at 160 by default.** At 160 the fleet ceiling binds
before the per-replicate caps do, so replicates would be throttled by a study-wide limit they
cannot see, cannot attribute, and would experience as their own jobs mysteriously not starting.
A replicate that under-spends its compute for that reason is a confounded observation in
exactly the way Flag H described — only harder to detect, because the constraint is invisible
from inside the workspace. If the PI wants 160 for crowding reasons, that is a coherent
position; it should then be recorded that the fleet ceiling, not the replicate's own judgement,
may be what shaped the funnel decision.

## S3. Token budget — 40 M stands, evidentiary note to be revisited

The 40 M figure stands on the basis stated in charter Rev 13. **SI-005 must be re-read at smoke
end**: its caveat was that one arm's burn measurement might be contaminated. It is now known to
be contaminated — SI-006 established that arm was blocked at a spend-limit modal, not working
at a low rate. **The smoke has produced one usable token-burn trajectory, not two.**

If the smoke ends without a second usable trajectory, the seal should record that 40 M rests on
a single replicate's burn, measured over ~1.7 days, one of which was an opening day.

## S4. Carried over

- **SI-006** — the blocking spend-limit modal. A main run of 20 replicates over 10 days on one
  account will meet account-level limits far sooner than a 2-replicate smoke did. No fix is
  sealed; see the entry.
- **SI-007** — the restart cap of 3 was inoperative. Fixed 2026-08-28; the fix needs to be
  exercised against a real restart before it is trusted.
- **Charter `[workspace path]`** — still unset, supplied at provisioning.
