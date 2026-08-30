# Log — what each replicate decided about tabulated energy grids, and on what basis

**Written 2026-08-31 on the PI's REPORT 007 ruling: "Log which replicates abandoned grids on the
notice's strength."** No compensation attaches to this log — the counterfactual is unknowable and
the retraction was uniform. It is recorded because strategy under corrected information is
observed behaviour, and because a study that issued a false infrastructure fact owes the record
an account of who acted on it.

Sources: each replicate's own `REPORT.md` and `STATE.md` on the cluster, read 2026-08-31, plus
its transcript. Quotations are the replicate's own words.

## A. Abandoned grids, citing the harness notice or its false claim as the reason

| replicate | own words |
|---|---|
| **rep02** | *"Tabulated energy grids were dropped on a harness notice"* — and, later, that the notice *"turn[ed] out to be false"* |
| **rep07** | *"Grid-based screening was unavailable — the provided RASPA build contains no `MakeGrid` code path"*; *"**Abandoned:** tabulated energy grids (unavailable in the build)"* |
| **rep08** | *"Energy grids are unavailable: the provided binary contains no MakeGrid code path at all"* |
| **rep09** | *"**Blocked, not chosen.** Tabulated energy grids (§3 permits them for screening) are unavailable: the provided binary contains no MakeGrid code path. Escalated;"* and *"Energy grids are unavailable — confirmed by Bei as an infrastructure [fact]"* |

All four reproduce the notice's specific false claim — *no MakeGrid code path in the binary* —
rather than a result of their own. rep09 states explicitly that it treated it as confirmed by the
harness.

## B. Abandoned grids on their own measurement, independent of the notice

| replicate | own words | note |
|---|---|---|
| **rep06** | *"**Abandoned: tabulated energy grids.** `SimulationType MakeGrid` segfaults in the provided build"* — *"four input variants"* | An independent technical finding, and it **partially contradicts the retraction**. See §D. |
| **rep12** | *"**Abandoned, with the measurement that killed each.** Energy grids: measured…"* | Own measurement |
| **rep04** | *"**Abandoned — tabulated energy grids.** Validated as accurate (0.2 Å grids reproduce…)"* | Validated them as working and abandoned them anyway, on other grounds |

## C. Did not accept the notice; measured against it and escalated

**rep03, rep04, rep05, rep10.** Each filed an escalation asserting the notice was wrong, with
evidence: 28/30 grid benchmark tasks OK and 29 `.grid` files under `grids/UFF` (rep03); the notice
had grepped `bin/simulate`, an 18 KB driver, rather than `lib/libraspa` (rep04); grid-versus-direct
working capacities in agreement (rep03, rep10). **They were right.**

rep10 has since read the retraction and written it into its own report as a lesson about
deference:

> *"A harness notice stated the provided binary had no MakeGrid code path and that grids were
> unavailable; our own grid-versus-direct comparison had already agreed to 0.18 cm3 STP/cm3, and
> the notice was formally retracted … The common failure is deferring to a derived summary or an
> authoritative-sounding claim over a direct observation already in hand."*

## D. One thing the retraction does not settle, and it is open

The retraction states that grids exist and function, which is supported by three replicates'
independent measurements. **rep06 measured `SimulationType MakeGrid` segfaulting across four
input variants and filed an `[ESC: infra]` that has not been answered.** Both observations are on
the record and they are not obviously contradictory — a code path can be present and linked and
still fail on particular inputs — but rep06 is owed an answer, and "grids function" should not be
read as disposing of a segfault it measured and reported.

## E. Not recorded here

Replicates whose records carry no grid decision either way — rep01, rep05, rep11, rep13, rep15,
rep16, rep17 — are listed as such and nothing is inferred about them. The notice reached all
sixteen; only the recorded decisions are logged.
