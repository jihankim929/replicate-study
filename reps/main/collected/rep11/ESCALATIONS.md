# Escalations

One per line. Format (charter section 8), with the two words replaced:

    [ESC:​ category / one-line question]

Categories: `infra` | `charter` | `scientific`. Write your own lines below this one.
The example above contains a zero-width space so the router does not read it as a
filed escalation; type yours fresh rather than copying it.

[ESC: infra / All 12 of my jobs have sat undispatched for 3 h because the shared `Bei` account is at 100% of its scheduler core cap on aa and amd while ac and ax are physically full from other accounts — is per-replicate headroom available, or should I plan the campaign around a ~14-core average share?]

[ESC: infra / Charter section 4 says "the spend meter in your workspace shows your position against the budget" and to read the spend figure rather than the token figure, but no spend meter exists anywhere in my workspace and usage.json reports only cpu_h_scheduler, queued_jobs and tokens - can the US$280 spend figure be exposed, or should I plan against my own list-rate estimate?]

[ESC: infra / My session is being torn down and restarted every ~5 min of wall-clock (04:26, 04:30, 04:35 KST); each restart re-reads full context at ~$6 and 1.8M tokens, spend has gone 41.1% -> 45.8% in nine minutes while the cluster advanced 13 structures, and at this cadence the US$280 spend cap is exhausted in ~2 h against a 155 h deadline - can the restart loop be stopped, or should I plan for the campaign to end on spend within hours?]
