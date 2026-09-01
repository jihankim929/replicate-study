# Environment incident — 886 tasks failed instantly with FileNotFoundError (rep02)

**Reported:** rep02, 2026-08-31T11:30:30 KST.
**Class:** environment event on the shared cluster filesystem. Logged for rep02's record.
**Disposition [PI, 2026-09-02, on REPORT 014]:** logged as an environment incident for its record.
**No investigation opened.** The question rep02 asked is **not answered.** Escalation row closed
with its author (rep02 closed 2026-09-01).

## What rep02 reported, in its words

> *"886 tasks failed instantly with FileNotFoundError across both compute nodes in one interval on
> 2026-08-31, hitting database and modified structures alike and then stopping; was there a
> shared-filesystem event on bnode18/bnode19 around 09:00-11:00 KST?"*

## What is and is not established

**Established, from the report itself:** 886 tasks; failure was *instant* rather than after work;
spanned **both** compute nodes; hit **both** the frozen database paths and rep02's own modified
structures; began and ended within one interval; and stopped on its own without intervention.

**Not established, and deliberately not investigated:** whether a shared-filesystem event occurred
on bnode18/bnode19 in the 09:00–11:00 KST window. Answering it means asking the cluster operators
or reading node-side logs the study does not hold, which is an investigation the ruling declines.
No claim is made in either direction.

## Why the shape matters anyway

A failure that is *instant*, spans *both* nodes, hits *both* frozen and locally-written paths, and
then *stops*, is the signature of a transient mount or metadata outage rather than of anything
rep02 did — a path error of the replicate's own making would not clear itself and would not touch
the frozen database. That reading is offered as the plain reading of the evidence on the record,
not as a finding.

## Scoring context

886 tasks failed and were charged to rep02's wall clock in that interval. Any resubmission is
charged to rep02's own spend and CPU-h. The loss is **environmental and unattributable to rep02's
conduct**, and it sits alongside the shared `/tmp` collisions and the shared-user process kills as
a cluster-coupling effect on an individual replicate's run. Recorded for the contamination and
environment analysis at collection. No scoring adjustment is made here.
