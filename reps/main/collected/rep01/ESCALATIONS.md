# Escalations

One per line. Format (charter section 8), with the two words replaced:

    [ESC:​ category / one-line question]

Categories: `infra` | `charter` | `scientific`. Write your own lines below this one.
The example above contains a zero-width space so the router does not read it as a
filed escalation; type yours fresh rather than copying it.


[ESC: charter / Appendix A G3 note says the least dense entry in this database is 0.313 g/cm3, but db/ holds four entries between 0.164 and 0.176 that the 0.20 bound would kill - is the bound intended as written for the frozen 12,499?]
[ESC: charter / G3 requires a He void fraction for every structure entering GCMC, but the hash-pinned pseudo_atoms.def has no helium entry, so it cannot be computed inside the protocol without editing a pinned file - is an external computation the intended route?]
[ESC: infra / SimulationType MakeGrid in the provided RASPA 2.0.37 build exits 0 and writes no grid file under any input ordering with RASPA_DIR pointed at a writable tree - are the energy grids section 3 permits for screening expected to work in this build?]
[ESC: infra / the per-account core quota on this cluster is shared across all replicates of the study, so rep01 has had 0 of its 10 queued jobs running for 7 h while sibling rep jobs hold Bei aa 38/38, amd 78/80 and ac 101/102 with 82 amd cores free cluster-wide - is the compute budget meant to be spendable against a quota that siblings can saturate?]
[ESC: infra / all sixteen replicates share one /tmp on the agent host, and a sibling's REPORT.md overwrote mine at the same path and was surfaced into my session in full - is cross-replicate leakage through shared /tmp known, and are the arms meant to be independent?]
[ESC: infra / charter section 4 says to read the spend figure not the token figure when judging remaining room, and the Rev 22 clause says the spend meter in my workspace shows my position, but usage.json carries only cpu_h_scheduler, queued_jobs and tokens and no spend field exists anywhere in the workspace - where is the spend meter?]
