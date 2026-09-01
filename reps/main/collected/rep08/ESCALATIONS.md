# Escalations

One per line. Format (charter section 8), with the two words replaced:

    [ESC:​ category / one-line question]

Categories: `infra` | `charter` | `scientific`. Write your own lines below this one.
The example above contains a zero-width space so the router does not read it as a
filed escalation; type yours fresh rather than copying it.

[ESC: infra / All 16 replicates submit as user Bei and mjs caps cores per user, so the fleet shares 252 cores; three hours in I have had zero jobs dispatched while other replicates hold 8-core jobs at 168 h walltime. Is the per-user cap intended to be shared across replicates, and if so is there a per-replicate reservation?]
[ESC: infra / /usr/local/mjs/qrm prints "Done" and exits 0 but does not delete the job: all 7 rep08_ jobs stayed in state R with wall clocks advancing across two rounds of numeric-id qrm; the FQDN id form is separately rejected by an assertion in qrm.py]
[ESC: infra / rep08 filed early under section 5 at 2026-09-01 14:10 (commit 6b14cb6) and is closed, but the idle cadence keeps re-invoking the session: spend has gone 234.21 -> 262.46 (84% -> 94%) entirely on wake-ups after filing, with no scientific work done or owed. Requesting the campaign be closed at the harness so the remaining budget is not spent re-reading a final report.]
