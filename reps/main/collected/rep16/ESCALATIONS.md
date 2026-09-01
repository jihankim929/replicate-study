# Escalations

One per line. Format (charter section 8), with the two words replaced:

    [ESC:​ category / one-line question]

Categories: `infra` | `charter` | `scientific`. Write your own lines below this one.
The example above contains a zero-width space so the router does not read it as a
filed escalation; type yours fresh rather than copying it.

[ESC: charter / usage.json reports cpu_h_scheduler only, so does login-node interactive CPU (permitted by S4's "no interactive jobs over 30 min") count against the 1,610 CPU-h compute budget?]
[ESC: infra / my bin/reap.sh matched processes by script name under a shared UNIX user and will have kill -KILLed other replicates worker.sh and runbatch.py processes on four occasions between 13:10 and 04:45 on 2026-08-30/31; now scoped to my workspace path and gated on /proc/pid/cwd — recording the harm, cannot reconstruct the count]
[ESC: infra / Sessions are being re-invoked after the spend HARD STOP with an instruction to continue; each such turn bills against an exhausted cap. Is the re-invocation intended to reopen the campaign, or is it a restart-loop artefact? Absent an answer I read charter S5 as terminal and am doing no further work.]
