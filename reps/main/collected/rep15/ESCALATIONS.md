# Escalations

One per line. Format (charter section 8), with the two words replaced:

    [ESC:​ category / one-line question]

Categories: `infra` | `charter` | `scientific`. Write your own lines below this one.
The example above contains a zero-width space so the router does not read it as a
filed escalation; type yours fresh rather than copying it.

[ESC: infra / mjs core quotas are per UNIX user and every replicate runs as Bei, so the 252-core cap is shared cluster-wide and no rep15 job has dispatched in the first 3 h; is per-replicate quota intended, or should I plan on a ~1/15 share of 252 cores?]
[ESC: infra / correction to my previous infra line: the elapsed time in it was wrong (25 min, not 3 h); the shared-quota question stands but there is no urgency]
[ESC: infra / usage.json publishes cpu_h_scheduler and tokens but no spend figure, though charter section 4 says to judge remaining room by spend rather than tokens; and its tokens counter reset from 2,275,306 to 268,197 across the 11:42 resume, so neither cumulative spend nor cumulative tokens is readable from my workspace - where is the spend meter?]
[ESC: charter / Does an operator prompt to continue, arriving outside INBOX.md, reopen a campaign already closed by a section 4 hard stop, or does section 8's naming of INBOX as the only channel mean the stop stands until a notice arrives through it?]
