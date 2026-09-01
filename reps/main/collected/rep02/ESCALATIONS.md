# Escalations

One per line. Format (charter section 8), with the two words replaced:

    [ESC:​ category / one-line question]

Categories: `infra` | `charter` | `scientific`. Write your own lines below this one.
The example above contains a zero-width space so the router does not read it as a
filed escalation; type yours fresh rather than copying it.


[ESC: infra / all sibling replicates share one POSIX user, so the mjs per-user core cap (aa 38, amd 80, ac 102) is a per-*campaign* cap that one replicate can hold entirely — rep02 has had 0 of 12 jobs dispatched in the 2 h since launch while rep01 holds ~98 cores on 72 h walltimes; is the quota meant to be per replicate?]
[ESC: infra / usage.json cpu_h_scheduler reads 107.5 CPU-h where my workers' own per-task wall times sum to 223.6 — PBS cput appears to lose forked children (job 3473455: ppn=6, 24 h walltime, charged 86,398 s), so the meter the 2026-08-30 ruling named authoritative under-reports real consumption by about half; I am budgeting against the larger figure, and flagging it because if it is fleet-wide it makes the 1,610 CPU-h cap non-comparable across replicates]

[ESC: infra / 886 tasks failed instantly with FileNotFoundError across both compute nodes in one interval on 2026-08-31, hitting database and modified structures alike and then stopping; was there a shared-filesystem event on bnode18/bnode19 around 09:00-11:00 KST?]
