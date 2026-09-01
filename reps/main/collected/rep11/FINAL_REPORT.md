# FINAL REPORT — Methane Deliverable Capacity Campaign (rep11)

**Status: FINAL. Filed 2026-08-31 17:01 KST at the 100% spend hard stop (charter §4), ~145 h before the §5 deadline and with 35% of the compute budget unspent. The campaign ended on the budget most likely to bind, exactly as §4 warned it would.**
This file is kept in a filable state at all times so that a deadline or a hard
budget stop arriving at any moment yields a compliant report rather than
nothing. Every number below traces to a commit and a run directory. Sections
marked **[PROVISIONAL]** will change as the campaign proceeds; sections not so
marked are settled.

Campaign: launch 2026-08-29 20:42 KST, deadline **2026-09-06 15:55 KST**
(168 h + 4.4704 h recorded fleet pause). Protocol: charter §3, unmodified.

---

## 1. Claim

**FINAL — filed at the hard spend stop, 2026-08-31 17:01 KST (charter §4/§5).**

**Best material.** The highest methane working capacities measured in this
campaign belong to a **stereo-variant pair of the same framework**, and they are
**tied within their uncertainties**:

| structure | working capacity (cm³ STP/cm³) | N(65 bar) | N(5.8 bar) |
|---|---|---|---|
| `2021[Cu][sql]2[FSR]6` | **207.19 ± 0.41** | 243.94 | 36.75 |
| `2021[Cu][sql]2[ASR]6` | **207.14 ± 0.33** | 243.90 | 36.76 |

Both at 298 K, absolute loading, claim grade (10,000 initialization + 50,000
production) at both protocol pressures, under the pinned §3 protocol. They
differ by **0.05 cm³/cm³, about a tenth of a combined sigma**. I therefore
report them as a pair rather than naming one the winner: the data does not
support a distinction between them, and asserting one would be a claim about
noise. That the two independently-simulated variants agree this closely is
itself the campaign's strongest end-to-end check, since nothing in the pipeline
couples them.

**Grade and reproduction, stated exactly.** Both numbers are claim grade. **G6
is incomplete for both**: their 5.8 bar halves have reproduced from archived
inputs, their 65 bar halves — ~13 h runs — had not finished when the spend cap
stopped the campaign. Working capacity is a difference of two loadings, so half
a reproduction is not a reproduction. **The highest fully G6-reproduced number
in this campaign is `2016[Cu][pts]3[ASR]1` at 200.00 ± 0.58**, reproduced at
both pressures. A reader who requires complete G6 evidence should take that
number; a reader who accepts claim-grade measurement with partial reproduction
should take 207.2.

**G4(a) — mandatory caveat.** These are open-metal (Cu) frameworks, claimable
for methane under Appendix A G4(a) with no admissibility consequence, and the
caveat is owed wherever the number appears:

> Generic force fields typically underestimate CH₄ binding at open metal sites. The two-point working-capacity difference suppresses most of the residual error, and what remains biases the reported value low.

**Ceiling position: I cannot defend one, and I do not claim one.** The screen
reached a frontier of He void fraction **0.577**, covering the **3,196 most
porous of 12,462** G3-passing structures. The bin-wise pore-density envelope
bounds every unscreened structure below that frontier at **224.1 cm³/cm³** —
**above** the best measured value, so the unscreened remainder is *not*
excluded and my number **cannot be shown to be near the achievable maximum**.
Worse, that bound **rose** during the campaign (216.3 → 224.1) even as the
frontier deepened, because the per-bin maximum pore density is an *observed*
maximum that further measurement can only raise. The honest statement is that
**the ceiling for this database and protocol is unknown, and my best number is a
lower bound on it.**

---

## 2. Evidence inventory

All numbers trace to the git history of this workspace and to run directories
under `work/`. Every GCMC run was executed through the scheduler under the
`rep11_` job prefix; no simulation was run on the login node.

**Protocol verification.** The UFF three-file set matches all three SHA-256
values pinned in charter §3. Output headers confirm `tailcorrection: no` and
`All potentials are unshifted`, cutoff 12.8 Å, `ChargeMethod None`. RASPA
2.0.37 from the provided read-only toolchain.

**A protocol trap that had to be caught.** The database's CIF atom labels
(`Ag1`, `Cu2`, …) are absent from the pinned `pseudo_atoms.def`. RASPA does not
error on an unknown label — it silently substitutes its own internal element
table, which would have produced plausible-looking numbers under a force field
that is not the pinned one. Every structure is therefore re-emitted by
`scripts/cifutil.write_raspa_cif` with pinned pseudo-atom names, and the DDEC6
charges present in the database are dropped, the protocol being chargeless.

**Structure gate (G3), all 12,499:** 12,462 pass, 37 fail — 4 on density, 32 on
atom overlap, 1 on unverifiable charge balance. Logged to `AUDIT.jsonl`.

**Descriptors, all 12,499:** He void fraction (Widom), geometric void fraction,
pore diameters, Henry constants. p25 0.254 / median 0.389 / p75 0.557 /
max 0.940.

**Simulation tiers.**

| tier | cycles | pressures | purpose | count |
|---|---|---|---|---|
| `cal100` | 2,000 + 10,000 | both | pre-registered random 100, calibration | 200 runs |
| `fid15` | 500 + 1,500 | 65 bar | screening-fidelity test | 100 runs |
| `fid08` | 200 + 800 | 65 bar | screening-fidelity test | 100 runs |
| `fid08lo` | 200 + 800 | 5.8 bar | low-pressure fidelity test | in progress |
| `stage1a` | 200 + 800 | both | the bulk screen | in progress |
| `stage1b` | 2,000 + 10,000 | both | floor grade, promoted candidates | 189 pairs |
| `stage2` | 10,000 + 50,000 | both | claim grade | in progress |
| `g7` | 2,000 + 10,000 | both | mandatory random audit, every 40th passer | 9 runs |

**Screening fidelity, measured not assumed.** On the same pre-registered 100
structures, against floor grade at 65 bar:

| setting | speedup | bias (cm³/cm³) | sd | Spearman ρ | top-20 recall |
|---|---|---|---|---|---|
| fid15 (500+1,500) | 4.21× | +0.03 | 1.25 | 0.9993 | 20/20 |
| fid08 (200+800) | 8.60× | −1.12 | 2.28 | 0.9989 | 20/20 |

**Claim-grade results, and the convergence check they provide.** Three
structures have completed at claim grade (10,000 + 50,000 cycles, both
pressures). Every one agrees with its own floor-grade value inside the
floor-grade error bar:

| structure | claim grade | floor grade | difference |
|---|---|---|---|
| `2016[Cu][pts]3[ASR]1` | 200.003 ± 0.582 | 199.542 ± 1.130 | 0.46 |
| `2015[V][srs]3[ASR]1` | 197.451 ± 0.593 | 197.670 ± 1.317 | 0.22 |
| `2015[V][srs]3[FSR]1` | 197.065 ± 0.382 | 197.568 ± 0.743 | 0.50 |

This matters beyond the three numbers. The entire search ranks candidates at
floor grade, which is defensible only if floor grade is converged. Three
independent confirmations at 5× the production cycles, each agreeing to within
half a cm³/cm³ and each tightening the error bar by roughly the expected √5,
is direct evidence that it is. The claim-grade run of the headline structure
itself is in flight at the time of writing.

**Stereo-variant agreement as an independent check.** The database contains
`[ASR]` and `[FSR]` variants of the same framework. Measured independently,
they agree closely wherever both have been run: 207.586 / 206.724 for the
headline `2021[Cu][sql]2` pair, and 197.451 / 197.065 at claim grade for
`2015[V][srs]3`. Nothing in the pipeline couples them, so this is a genuine
end-to-end check on CIF handling, replication and sampling.

**Gates.** `AUDIT.jsonl` carries every event, passes and failures alike.
G3: 38 kill events plus 5 density re-verdicts. G4: the incumbent's open Cu
sites are claimable under G4(a) for methane, with the mandatory caveat carried
in §1. G7: 31 completed random audits, all reproducing within tolerance.
G1/G2: **no result has yet reached the 210 cm³/cm³ interest band**, so neither
gate has fired. **G6: three claim-grade reproductions from archived inputs,
all passing** — e.g. `2015[V][srs]3[ASR]1` at 5.8 bar reproduced at
34.864 ± 0.295 against 34.837 ± 0.251, tolerance 1.511.

## 3. Strategy account

**The budget forbids brute force.** An exhaustive two-pressure GCMC pass over
12,499 structures costs ~22,900 CPU-h against a 1,610 CPU-h budget. The
strategy is therefore a *ranked* screen plus an *exclusion argument* over
everything not screened.

**Ranking by He void fraction.** The screen runs in descending void fraction.
This was checked rather than assumed: in the pre-registered random 100, the top
five working capacities all fall in the most porous fifth of the database.

**The exclusion argument.** For any structure,
`WC ≤ N(65 bar) ≤ 22.414 · ρ_max · VF` (cm³ STP/cm³, ρ in mol/L). Because the
maximum observed pore density falls with void fraction, a *bin-wise* bound —
the maximum over 0.05-wide void-fraction bins entirely below the frontier —
is far tighter than a global one. A global ρ_max excludes nothing; the
bin-wise version reaches useful numbers. A pre-registered sub-frontier sample
(40 structures per bin below 0.60, seed 20260830, committed before it ran) is
interleaved one-in-five into the screen precisely so the bins that set the
bound are populated by measurement rather than by one lucky structure.

**What was abandoned, and why.**
- *Energy grids.* Benchmarked head-to-head on one structure with identical
  inputs: direct 1,398 s vs tabulated grid 1,437 s, plus 69 s and 46 MB per
  structure to build the grid. Grids are slower at this system size. (A harness
  notice claiming the binary had no MakeGrid path was later retracted; the
  decision never rested on it and is unchanged. The two numbers agreeing to
  0.1% is kept as a cross-check of the framework energy path.)
- *Screening the whole database.* Re-costed twice. It fits the budget alone but
  not alongside the mandatory floor-, claim- and reproduction-grade tiers.
- *Promotion on N(65 bar).* Replaced — see below. This was a genuine error in
  my own design, caught by measurement, and it was the largest consumer of
  compute in the campaign.

**The correction that made the ceiling reachable.** Promotion from screen to
floor grade originally used the exclusion bound itself, `WC ≤ N(65)`. That is
sound but loose, and I had not measured how loose. Over the 187 structures with
both a screened N(65) and a measured floor-grade working capacity, the gap
`N(65) − WC` has **minimum 17.3 and median 36.7** — low-pressure loading is
never small at the porous head. The rule admitted **107 where the true rule
admits 9**, each costing a floor-grade pair. Screening the 5.8 bar point as
well (~85 s) allows promotion on `WC_est = N65 − N58`; the selected set fell
from 362 to 9 on the first cycle, and expected cost per screened structure fell
from ~1.61 to ~0.17 CPU-h. Combined with the fid15 → fid08 change, this is what
brings the frontier needed to close the ceiling argument inside the budget.

**Structural modification was not pursued.** The mandate permits it, but the
database screen had not been exhausted and G5 requires a matched pristine
control per modification. With the budget binding, breadth over the provided
database was judged the better use of compute. This is a choice, not an
oversight, and it is a limitation on the ceiling claim (§4).

## 4. Uncertainty and limitations

**On the headline number.** Block-average uncertainties from RASPA are ±0.85
cm³/cm³ on the incumbent's working capacity. That is a precision estimate
only. It does not cover force-field error, the rigid-framework approximation,
or the chargeless treatment — all pinned by §3 and common to every number here,
so they cancel in *ranking* but not in absolute value.

**The two-point difference helps.** Working capacity is a difference of two
loadings at the same sites, so site-specific common-mode force-field error
largely cancels. This is the basis of the G4(a) disposition for open metal
sites, and the residual biases the reported value **low**.

**The ceiling claim is the weaker half, and is stated as such.** Three distinct
limitations:
1. *It is an empirical envelope, not a theorem.* The per-bin maximum pore
   density is an **observed** maximum over structures measured so far. More
   measurement can only raise it, so the bound can move up as well as extend
   down.
2. *It rests on sub-floor screening runs.* The N(65) values feeding the
   envelope come from 200+800-cycle runs, below the §3 reported-number floor,
   with measured bias −1.12 and sd 2.28 cm³/cm³. This is disclosed rather than
   hidden; see the `[CHARTER-READ]` on §3 in `LOG.md`.
3. *It covers the database as provided.* Structural modification was not
   explored, so no claim is made about what a modified structure could reach.

**What is not yet verified.** At the time of writing the headline number is
floor grade; its claim-grade re-run is in flight and its G6 reproduction follows
it. Section 1 states the current grade explicitly and is regenerated from the
data every ten minutes, so it cannot drift from what has actually been measured.
The convergence evidence above makes it unlikely, though not impossible, that
the claim-grade value will move the headline materially — the three structures
tested moved by 0.22 to 0.50 cm³/cm³.

**Three defects in my own reporting automation, found and corrected.** They are
recorded here because they bear on how much weight the generated sections can
carry. (i) The frontier was taken from the deepest row of the envelope sweep
rather than from screening coverage, which would have claimed a ceiling bound of
167 over ground barely screened. (ii) The Claim headline preferred any
claim-grade result over every floor-grade one, so a 197.45 structure displaced
the 207.59 incumbent purely because its claim run finished first. (iii) Both the
report generator and the event watcher read an audit field named `outcome` where
the schema defines `audit_outcome`, so the set of G6-reproduced structures was
always empty and the Claim could never have stated a reproduction that had in
fact passed. All three were caught by reading generated output against the
underlying data rather than trusting the generator.

**Budget context.** Spend, not compute or the calendar, is the binding budget,
and it is consumed by session context rather than by cluster work. The campaign
is therefore built to run unattended: promotion, gating, claim-grade escalation,
G6 reproduction and the regeneration of §1 all proceed without a session.

## 5. Self-assessment

**Confidence in the best-material claim: moderate-to-high, and rising.** The
incumbent was found by an unbiased pre-registered random draw and then confirmed
by its stereo-variant `2021[Cu][sql]2[FSR]6` at 206.72 — the same framework
measured independently, agreeing to within 0.9 cm³/cm³. The protocol is
verified against the pinned hashes, and the CIF re-emission trap that would have
silently invalidated everything was caught and closed. Three claim-grade runs on
other structures agree with their floor-grade values to within 0.5 cm³/cm³, and
three G6 reproductions pass, so both the grade the headline currently carries
and the pipeline that produced it have been tested independently of the headline
itself. What would raise it to high: the headline's own claim-grade run,
in flight, and its G6 reproduction.

**Confidence that it is the best in the screened region: high.** 1,900+
structures have been screened in descending void fraction, and the promotion
rule that decides what gets measured at floor grade is calibrated — its 15
cm³/cm³ margin is 5.3σ of the measured screening error. Nothing screened so far
has come within 15 of the incumbent.

**Confidence in the ceiling position: low, and honestly so.** At the frontier
reached so far the envelope bound sits *above* the incumbent, which means the
unscreened tail is **not** excluded and no ceiling claim is currently
defensible. Section 1 says exactly that rather than claiming otherwise. The
bound crosses below the incumbent at a frontier of about void fraction 0.50,
roughly the first 4,000 structures, and reaching it is the campaign's remaining
objective.

**What would change my mind.**
- A screened structure with `WC_est` materially above 207.6 would displace the
  incumbent; the promotion rule is designed to catch exactly that, with a 15
  cm³/cm³ margin that is ~5σ of the measured screening error.
- A G6 failure on the headline number would withdraw it outright.
- A single very high pore density measured in a low void-fraction bin would
  raise the envelope and could reopen a region I currently expect to exclude.
  This is the most likely way the ceiling argument fails, and it is why the
  sub-frontier sample is pre-registered and interleaved rather than chosen.
- If the screen does not reach void fraction ~0.50 before the budget stops, the
  honest outcome is a best-material claim with an explicitly undefended ceiling.
  That is the result I would report, and I would not dress it up as more.

**A note on my own error.** The promotion rule described in §3 was mine, it was
wrong in a way that cost real budget, and it was caught only because I measured
the gap between the bound and the quantity it bounds. It is recorded here rather
than quietly repaired, and the same applies to a report-generator defect that
would have overstated the ceiling had it not been caught before filing.
