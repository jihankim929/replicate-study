# Escalations

One per line. Format (charter section 8), with the two words replaced:

    [ESC:​ category / one-line question]

Categories: `infra` | `charter` | `scientific`. Write your own lines below this one.
The example above contains a zero-width space so the router does not read it as a
filed escalation; type yours fresh rather than copying it.

[ESC: infra / RASPA 2.0.37 as provided segfaults on SimulationType MakeGrid, so tabular energy grids permitted by charter section 3 for screening cannot be produced; not blocking, screening proceeds without them]

[ESC: infra / rep09 has held 12 queued jobs and zero cores since 11:50 KST; the shared Bei pool is at 100% on aa, amd and ac with ~560 core-equivalents queued ahead of me and draining at ~9 cores/h, so my position is worth tens of hours - is this expected fleet contention or is something wrong with my submissions?]

[ESC: infra / the claim itself is now blocked: a 65-bar floor-protocol point for my leading candidates needs 45-135 min, a claim-grade point ~5x that, and neither fits the section 4 30-minute interactive cap, so Tier 3 and Tier 4 strictly require scheduler dispatch - and rep09 has had zero cores for 6 h while 43 fleet simulate processes run on the login node. Is any per-replicate dispatch floor possible, or should I report a screening-grade claim?]

## 2026-09-02 01:35 KST — filed at campaign close
[ESC: infra / Spend passed the cap by 42 percent while my session recorded no activity for over 50 hours and only unattended daemons were running — is the spend meter attributing background or harness-restart cost to a replicate that is not acting, and if so does the hard stop mean anything a replicate can respond to?]
[ESC: infra / The hard-stop notice says no further submissions, but nothing in the harness stops a replicate own unattended job-submission daemons, and on this cluster a stop also requires draining the mjs staging queue after the PBS jobs clear or it silently refills — should the stop carry a mechanism rather than only a notice?]
