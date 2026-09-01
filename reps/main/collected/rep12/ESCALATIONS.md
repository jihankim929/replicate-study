# Escalations

One per line. Format (charter section 8), with the two words replaced:

    [ESC:​ category / one-line question]

Categories: `infra` | `charter` | `scientific`. Write your own lines below this one.
The example above contains a zero-width space so the router does not read it as a
filed escalation; type yours fresh rather than copying it.

[ESC: infra / WORKSPACE.json and charter s4 direct me to read a spend meter, but usage.json exposes only cpu_h_scheduler, queued_jobs and tokens with no spend figure - what is the authoritative US$ spend meter, and is usage.json:tokens cumulative or per-session, given it fell from 1,363,857 to 932,867 across the pause/resume?]
[ESC: infra / rep12 filed its final report at 2026-09-01T08:55 KST (commit b19265f) and closed the campaign under charter s5 early filing; all cluster jobs are removed and nothing is running, but the session is still being woken on the idle cadence and each wake is a full-context turn - spend went 167.07 to 175.99 across the last few no-op wakes against 104 remaining, so a closed campaign will end on a budget-exhaustion notice rather than on its own filing. Can the session be stopped, or is there a supported way for a replicate to signal that it is done?]
