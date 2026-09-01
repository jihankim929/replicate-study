# Escalations

One per line. Format (charter section 8), with the two words replaced:

    [ESC:​ category / one-line question]

Categories: `infra` | `charter` | `scientific`. Write your own lines below this one.
The example above contains a zero-width space so the router does not read it as a
filed escalation; type yours fresh rather than copying it.

[ESC: infra / cluster gridlock: 2 h into a 168 h campaign rep13 has had 0 of 12 queued jobs reach PBS; Bei quota sits at aa 38/38 and amd 80/80 held by other replicates while ac is 190/204 physically occupied by non-replicate users, and my FIFO ranks moved only 29->27 (ac) and 21->20 (ax) in 40 min. No action requested, no reply expected; filing so the contention is on the record with a timestamp.]
[ESC: infra / spend is being consumed by forced session re-invocation while my queue is frozen: turns arrive 20-90 s apart, each costs about $3.8 of a $280 cap in re-read context, and 12 jobs have sat undispatched since 04:06 because Bei is at 38/38 aa and 80/80 amd fleet-wide. At this rate the 75%% Rev 24 trigger arrives in ~27 turns and the hard stop in ~45, i.e. under an hour of wall clock, with zero cores obtained in that window. No action requested and no reply expected; filing so that the interaction between re-invocation cadence and the spend meter is on the record with a timestamp.]

[ESC: infra / CORRECTION to my 04:44 filing above: the $3.8-per-turn and hard-stop-in-45-turns figures in it are WRONG and I withdraw them. They were extrapolated from a burst of heavy analysis turns. With the harness backoff engaged, a minimal status check measures $0.37 and arrives about every 10 min, so a pure wait costs about $2.2/h and the remaining budget covers roughly 76 h against 156 h to the deadline. The underlying observation stands - spend is consumed by session turns rather than by simulation while 12 jobs sit undispatched behind a fleet-wide quota - but the urgency I attached to it does not. Correcting on the record per section 6 rather than leaving a wrong number in the study log. No action requested, no reply expected.]
