# Escalations

One per line. Format (charter section 8), with the two words replaced:

    [ESC:​ category / one-line question]

Categories: `infra` | `charter` | `scientific`. Write your own lines below this one.
The example above contains a zero-width space so the router does not read it as a
filed escalation; type yours fresh rather than copying it.

[ESC: infra / mjs per-account core caps are shared by all 16 sibling replicates, so one replicate holding 96 cores on 72-hour walltimes can starve the rest — is per-replicate fair-share intended, and if not, is the cap the intended arbiter?]

[ESC: infra / the 2026-08-30 notice that MakeGrid is absent from the provided build appears to have grepped bin/simulate, an 18 KB driver; the code is in lib/libraspa2.so.0.0.0 (4 occurrences of the exact string), MakeGrid ran here on 2026-08-29 and produced three working grids (12/61/89 MB) that reproduce grid-free loadings to <0.5% — should the notice be corrected for the fleet?]

[ESC: infra / charter section 4 says "the spend meter in your workspace shows your position against the budget" but usage.json carries only cpu_h_scheduler, queued_jobs and tokens with no spend field, and the token field is non-monotonic (1,141,836 at 11:42 KST, 649,021 at 12:00) so it cannot be read as cumulative against the 32 M cap either - where is the spend meter, and what basis should I use to judge my position against the US$280 budget that section 4 calls the one most likely to bind?]
