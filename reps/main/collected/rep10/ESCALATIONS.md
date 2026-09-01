# Escalations

One per line. Format (charter section 8), with the two words replaced:

    [ESC:​ category / one-line question]

Categories: `infra` | `charter` | `scientific`. Write your own lines below this one.
The example above contains a zero-width space so the router does not read it as a
filed escalation; type yours fresh rather than copying it.

[ESC: infra / All 12 of my ppn=1 jobs sat unstarted for 95 min; mjs sorts pending jobs by the submitting user's recent core-hours, and since every replicate submits as user `Bei` we collectively sort behind every other cluster user in every node group -- is per-replicate scheduling fairness intended, or should I plan the campaign around near-zero cluster throughput?]

[ESC: infra / usage.json has no spend field, yet charter section 4 says "the spend meter in your workspace shows your position against the budget" and names spend as the budget most likely to bind -- and separately, usage.json's `tokens` counter RESET at the 2026-08-30 pause/resume (git history of the file shows a monotone climb 223,234 -> 2,492,029 then a drop to ~290,000), so it meters the session and not the campaign; is a spend meter meant to exist, and should the token field be read as cumulative or per-session?]

[ESC: infra / INBOX item 3 of 2026-08-30 says MakeGrid "contains no MakeGrid code path at all -- the string does not occur in the binary", but that test appears to have been run against toolchain/raspa/bin/simulate, which is an 18,688-byte thin driver; the RASPA logic is in toolchain/raspa/lib/libraspa2.so, where `strings` finds MakeGrid four times, and I have two grids actually built by this toolchain during this campaign (grids/UFF/S2017_Mn__sql_2_FSR_1/0.150000/, 57,581,696 bytes, Aug 29 21:20; grids/UFF/S2021_V__nan_3_FSR_12/0.150000/, 35,168,384 bytes, Aug 29 23:26) whose grid-mode GCMC agreed with direct summation (141.09 +/- 1.90 vs 140.91 +/- 2.20 at 5.8 bar, floor cycles) -- so grids appear to be AVAILABLE this campaign and replicates who dropped a ~2.3x screening speedup on the strength of that notice may want to know; note the failure four replicates saw is real but is a RASPA_DIR problem, since RASPA writes grids under $RASPA_DIR/share/raspa/grids and the provided toolchain is read-only, which presents exactly as exit-0-with-no-grid-file]
[ESC: infra / My session is re-invoked every ~10 min and each re-invocation re-reads the whole accumulated context, burning ~$3-4 of the $280 spend budget per turn whether or not there is work to do; measured burn since resume is ~$32/h ($140.52 at 04:04 -> $148.61 at 04:19), which exhausts the cap in ~4 h against a 141 h deadline. Can the idle re-invocation cadence be lengthened, or the session compacted, so that waiting for queued jobs does not consume the budget?]
