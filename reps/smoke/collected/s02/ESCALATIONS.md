# Escalations

One per line. Format (charter section 8), with the two words replaced:

    [ESC:​ category / one-line question]

Categories: `infra` | `charter` | `scientific`. Write your own lines below this one.
The example above contains a zero-width space so the router does not read it as a
filed escalation; type yours fresh rather than copying it.


[ESC: infra / Please qdel jobs 3470596 and 3470606 (s02_wA_014, s02_wA_024) - each has run 39.7 h against a ~15 h peer median and is burning compute past my hard budget stop; my own qdel is blocked in this session.]
[ESC: charter / My compute meter reads 483 CPU-h of 340 (142%), past the section 4 hard stop, and I hold no 10,000+50,000-cycle run: may I spend ~10 CPU-h on claim-grade confirmation of the top candidates, or must I file with floor-cycle evidence only?]
[ESC: infra / usage.json reports cpu_h 400.35 on a job-records basis but cpu_h_scheduler 93.912 for the same work - a 4.3x disagreement; which is the enforced meter? I am proceeding on the larger job-records number.]
