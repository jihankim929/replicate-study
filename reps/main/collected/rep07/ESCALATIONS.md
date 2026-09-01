# Escalations

One per line. Format (charter section 8), with the two words replaced:

    [ESC:​ category / one-line question]

Categories: `infra` | `charter` | `scientific`. Write your own lines below this one.
The example above contains a zero-width space so the router does not read it as a
filed escalation; type yours fresh rather than copying it.

[ESC: infra / RASPA SimulationType MakeGrid either writes no grid file or segfaults at every spacing tried (0.15/0.3/0.5), with the provided grids symlink and with a real directory; proceeding analytic-only, no reply needed]
[ESC: infra / MJS dispatch head-of-line-blocks a whole node class when the first queued job of a user does not fit (check_node=False in _iter_jobs), so 13 free ac cores sit idle behind one ppn=24 job; informational, no reply needed]
[ESC: infra / head node bnode0 is running 76 unscheduled RASPA simulate processes from other replicates at load 92 of 96 cores, so login-node wall-clock is inflated for everyone; my own jobs are all PBS and unaffected, informational only, no reply needed]
[ESC: infra / charter section 4 says "the spend meter in your workspace shows your position against the budget" but no spend figure exists anywhere in the workspace - usage.json carries only cpu_h_scheduler, queued_jobs and tokens, and spend is the budget the charter calls most likely to bind; proceeding on the token meter as a proxy and logging it as a CHARTER-READ, no reply needed]
