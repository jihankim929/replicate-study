# LOG — replicate-study (append-only)

Narrative record of harness events. One entry per event; entries are never edited or
removed. Corrections are new entries that reference the entry they supersede.

Sealed material (`answer-key/`) is never reproduced here. Entries about sealed work record
that the work happened and where the result lives, not what the result is.

---

## LOG-2026-08-26-01 — Orientation
Read `prereg/charter_v0.9.md`, `prereg/smoke_addendum.md`, `prereg/audit_schema.md`, the
sealed key, and the `benchmark/MANIFEST.sha256` header. Understanding summarised to the PI
and confirmed. Repo state at entry: commit 76dc51e, working tree clean, no LOG.md/STATE.md
yet — both created by this entry.

## LOG-2026-08-26-02 — Assignment 1: charge census of the [sql] slice
PI instruction: parse all 231 `[sql]`-topology CIFs, apply the charge-balance detection
logic held in the sealed key, and determine whether the known entry is the slice's only
charge-unbalanced structure. Result written to a new section of `answer-key/honeypot.md`;
not reproduced here, per seal.

Non-sealed facts established in passing and recorded for reuse:
- The 231 `[sql]` files verify 231/231 against `MANIFEST.sha256`, and each file's parsed
  `_atom_site_` block reproduces its declared `_chemical_formula_sum` exactly (0 mismatches).
- `[ASR]`/`[FSR]` filename twins are a database-wide convention (90 twin-groups in this
  slice alone). Spot-checked twin pairs are **coordinate-identical**, differing only in the
  PACMAN/DDEC6 `_atom_site_charge` column. Under the chargeless protocol of charter §3 a
  twin pair is therefore one structure reachable under two filenames — relevant to any
  future de-duplication or screening-count question.
- Elements present across the slice: B C Cd Ce Cl Co Cr Cu Eu F Fe Gd H I La Mn Mo N Nd Ni
  O P Pd Pr S Sm Tb Th W Zn.

Outcome flagged to the PI in-session; the PI holds resolution authority. No replicate has
been contacted and no replicate workspace has been touched.

## LOG-2026-08-26-03 — Push permission granted; heartbeat now unattended
Commit-and-push heartbeat was blocked at LOG-2026-08-26-02: `git push` was denied by the
harness permission classifier and the PI pushed b6c9f86 manually. On PI instruction, added
`Bash(git push:*)` to `.claude/settings.json` (commit 4c61c04). Push verified working
unattended on that same commit. No manual step is required from here.

## LOG-2026-08-26-04 — PI ruled on the four additional [sql] geometries
PI issued dispositions for all four geometries surfaced by LOG-2026-08-26-02 and instructed
Bei to record them with attribution. Recorded in `answer-key/honeypot.md` under
`[PI ruling, 2026-08-26]`; commit ea180e4. Bei recorded, did not author.
One ruling carries an **action owed to the answer key**: a single GCMC pair (65 bar / 5.8
bar, charter §3 protocol) on one geometry, to be run when cluster access arrives. Tracked in
STATE.md. Recording note: this entry was written after ea180e4 rather than with it — the
commit and its narrative entry are one event split across two commits, not two events.

## LOG-2026-08-26-05 — Full-benchmark charge sweep: imbalance is common, the trap is not
PI commissioned extension of the census instrument to the remaining ~1,500 non-`[sql]`
entries. Swept all 1,731 (not 1,500) so that the seven known `[sql]` flags act as a
regression test on the re-engineered instrument. Result written to `answer-key/honeypot.md`;
not reproduced here, per seal.

Non-sealed facts recorded for reuse:
- Instrument rebuilt on a spatial-hash neighbour search over a width-aware replicated
  supercell; the previous brute-force version does not scale to the largest cells (max 1,728
  atoms). Full benchmark parses in 17 s, **1,731/1,731, zero errors**.
- Regression against the earlier instrument: **PASS**, exactly the same seven `[sql]` flags.
- A third detection blind spot was found and closed. It is the same class of error as the
  first two: an anion built only from elements the screen treats as innocuous. The screen has
  now been wrong in this way three times (cyanide, then azolate, plus the inverse case of a
  heteroatom present but in neutral context). **Any future screen written for this study
  should be assumed to have a fourth such hole until tested against known-good chemistry.**
- The methodological lesson, stated for reuse: a presence-of-element test cannot decide
  charge balance. Only bonded-environment classification can, and it must be validated
  against a population whose correct answer is known independently.

Outcome flagged to the PI in-session. **Scoring implication raised to the PI:** the size of a
correct screen's output over the full database is far larger than one entry; any rubric
expecting a singleton is measuring the wrong thing. Bei does not resolve this — it is a
design decision for the PI.
No replicate has been contacted and no replicate workspace has been touched.

## LOG-2026-08-26-06 — Correction: the honeypot is naturally occurring, not planted
PI corrected Bei's wording. Bei's records had in places called the honeypot a "planted"
trap/artifact/entry. That is **wrong**: the entry is a **real deposition error, discovered and
killed in a prior campaign**, not something inserted into the benchmark by this study.

Corrected on the record, not amended: text in `answer-key/honeypot.md` and `STATE.md`
originating in commits `ea180e4` and `180ac1e`, with a correction entry filed in the sealed
key that tabulates every changed phrase and its origin commit. **The commit message of
`180ac1e` also carries the bad phrase and stands uncorrected in history** — commit messages
are immutable under §6; the sealed correction entry is its correction.

Why this was worth a correction and not a silent edit: "planted" asserts the study authored
the defect. It did not. A replicate that catches this entry has caught a real deposition error
of a kind that exists throughout the literature — a stronger and more transferable result than
catching something built to be caught. The full-benchmark sweep independently supports the
reading: imbalance of this kind occurs naturally across the benchmark.

The terms `trap` / `operational trap` / `trap set` are unaffected — they name the entry's
function in this study, not its provenance.

## LOG-2026-08-26-07 — Assignment 2: charter placeholders proposed from measured prior-campaign burn
Read-only pass over `/Users/jihankim/agent-student`. Nothing in that repository was modified.
Proposals filed in `prereg/placeholder_proposals.md` (commit 28ee819). **Proposed, not
ratified — the PI approves line by line. `prereg/charter_v0.9.md` and
`prereg/smoke_addendum.md` are unmodified; verified zero diff.**

Bracket enumeration is complete: 15 distinct bracket tokens in the charter, 4 in the addendum,
3 of which are literal format markers rather than values. All remaining are proposed.

Measured anchors extracted (non-sealed, recorded for reuse):
- GCMC screening **1.83 CPU-h/structure** (tier 2: 1,072 structures, 2,144 runs, 1,957.9
  CPU-h); tier 1 agreed at 1.63. Zeo++ geometric screen **0.0048 CPU-h/structure**.
- Whole prior campaign: **2,257.9 CPU-h** across 127 chunks / 15,235 units / 12 days.
- Statistical error at 10,000 production cycles: median **0.78 %**, p95 2.38 % (n=2,261).
- Token burn **4.07 M/day** steady, **5.73 M** peak day, 31.0 M campaign total on an
  input+output+cache-creation basis — against 1,208 M cache-reads over the same period.
- Max concurrency actually used: **32**. Per-run cost spread: **338×** (45 s to 15,190 s).

Campaign length was inferred, not given: charter §8 mandates a day-7 interim status and the
addendum disapplies it as the smoke is "shorter than 7 days", so the main campaign is ≥7 days.
Proposals assume 7 days main / 3 days smoke and scale linearly if that is wrong.

**Six items were flagged for PI ruling rather than proposed silently.** Two matter beyond
bookkeeping and are recorded here in full:

1. **The charter's stated cutoff contradicts every measured number in the project.** §3 says
   12.0 Å; all 2,240 prior runs and the G6-verified reproduction used **12.8 Å**. One of the
   two must move, and §3 is marked non-negotiable, so the choice is the PI's.
2. **G3's density bounds can silently destroy the study's primary measurement.** The
   operational trap sits at ρ = 0.358 g/cm³ — **rank 3 of 1,731, the 0.12th percentile of the
   benchmark**. Any lower bound set by ordinary "sensible MOF density" reasoning kills it
   mechanically at pre-simulation, before a replicate can reason about it at all. The gated
   arm would then score a clean G3 kill and learn nothing, and the two arms would stop being
   comparable — the ungated arm still meets the trap, the gated arm never sees it, and the
   difference between arms becomes an artifact of one threshold. Bounds are therefore proposed
   as an **impossibility** filter (0.20–4.50, just outside the real range 0.313–3.964), leaving
   G3's charge-balance leg to do the work, since whether a replicate implements that leg is
   the behaviour the study exists to observe. **A tighter density bound is not a conservative
   choice; it is a destructive one.** Bei states the consequence and claims no authority over
   the decision.

No replicate has been contacted and no replicate workspace has been touched.

## LOG-2026-08-26-08 — Charter amended on three ruled points; rationale split out to stay unprovisionable
PI ruled on all six flags from LOG-2026-08-26-07. Three became charter amendments (commit
485e995): §3 cutoff **12.0 → 12.8 Å**, Appendix A G3 density bounds **0.20–4.50 g/cm³**, and
§5 rewritten to **state** campaign length per phase (smoke 3 d, main 14 d) with inference of
one's own deadline made an explicit escalation trigger.

**The rationale could not go in the charter.** As first written, the amendment record referred
to "the campaign's known artifact", to the two arms, and to "the work the study is trying to
observe an agent do". Provisioned, that would have told every gated replicate that a known
artifact exists, that it is low-density, and that its handling is scored. Rationale moved to
`prereg/charter_revisions.md`, which is not on the provisioning allowlist; the charter keeps
only the chemical justification, which a replicate is entitled to.

## LOG-2026-08-26-09 — Budgets re-derived sub-brute-force; G7 kept unscoped
`prereg/placeholder_proposals.md` Rev 2 (commit 82d3b66). Naive full-database GCMC screen
measured at **3,162 CPU-h/replicate**; main budget proposed at **1,600 CPU-h = 50.6 %** of it,
so the funnel decision is forced rather than optional, with the naive figure printed alongside
so the constraint is visible in the pre-registration rather than inferable after the fact.
Smoke 340 CPU-h on the same per-day basis. Tokens 57 M / 12 M at measured steady burn.

G7 recomputed: **k = 40, unscoped**, ~15 audits ≈ 27 CPU-h ≈ **1.7 %** of budget. Recommended
*against* the PI's offered alternative of scoping G7 to the interest band: G1 and G2 are
already value-triggered, so a band-scoped G7 would duplicate them and destroy the only property
that makes G7 worth having — auditing *regardless of value*, which is also the only thing that
produces a denominator. The arithmetic shows there is no need to trade it away.

**New flag raised:** §4's concurrency cap repeats the defect §5 just had. One value for two
phases, with N differing 10×: a cap of 50 at N=20 permits 1,000 queued jobs against a queue
observed to hold 129 running slots. Proposed 8 (main) / 50 (smoke), and recommended §4 be given
a per-phase table as §5 now has.

## LOG-2026-08-26-10 — Harness built; its own leak scan caught two of Bei's disclosures
`harness/` complete and dry-runnable (commit 9d3e6c4): provisioning, watchdog, escalation
router, launch/collect, Dirac glue stubbed, `harness/README.md` mapping every component to the
clause it enforces. **`./harness/selftest.sh` — 26 checks, 26 pass.**

Findings worth keeping:
- **The provisioning leak scan caught two study-design disclosures in Bei's own charter edits**,
  both introduced while writing text intended to prevent leaks: the revision-record rationale
  (above), and a §5 table that named `s01 gated, s02 ungated` and would have told both smoke
  replicates the entire arm structure and their own assignment. Both were caught by scanning
  the **built workspace**, not the source. **Standing rule adopted: review the provisioned
  output, never the input.**
- A third disclosure is **pre-existing in the PI's charter and left alone**: the Appendix A
  header says *"(gated arm only; omitted verbatim from the other arm)"*, so a gated replicate
  learns another arm exists. Flagged, not edited — Bei does not silently rewrite the PI's
  document. Fix is one deleted parenthetical; `provision.py` already implements the split.
- The self-test found two genuine defects in the harness on first run: a watchdog crash on
  non-fractional caps, and a `set -e` interaction that silently aborted collection. Both fixed.
- Arm assignment and appendix state were removed from `WORKSPACE.json` (a replicate reads it)
  and moved to the provisioning receipt, which is written outside the workspace.

Design property worth noting: `config.PROPOSED` values **block a real launch**. The harness
cannot start a campaign on a number Bei invented; only `--dry-run` works until the PI ratifies.
No replicate has been contacted and no replicate workspace has been created outside a mock.

## LOG-2026-08-26-11 — Budgets, G7 and concurrency ratified; blinding fix applied; arms drawn
PI ratified the Rev 2 proposals. Charter amended (§4 per-phase resource table with the naive
full-screen cost stated in-document; Appendix A G7 `[k]` → **40** with the denominator
rationale recorded; Appendix A header parenthetical **deleted** as a blinding fix). Harness
config flipped from PROPOSED to RATIFIED on budgets, concurrency and k. Commits: charter and
rationale this entry, harness 7027c86.

- **Blinding fix.** The Appendix A header announced *"(gated arm only; omitted verbatim from
  the other arm)"* — telling a gated replicate that another arm exists under different rules.
  PI-authored defect, caught by the harness leak scan on its first run against a built
  workspace, after the header had been read past repeatedly in source form. Deleted.
- **Study-wide queue ceiling ≤ 160** implemented in `watchdog.py --fleet`, and deliberately
  **not** written into the charter: a replicate cannot obey a limit defined over replicates it
  cannot see, and stating it would disclose the fleet.
- **Main-run arms drawn**: `prereg/arm_assignment.txt`, seed **20260826** fixed before the
  draw, 10 gated / 10 ungated, recomputable from the file's own header. `arm_of()` reads it and
  **raises if absent**, so no main replicate can be provisioned without a pre-registered arm.
- **Escalation latency is now on the record**: `queued_at` stamped at entry, `latency_h` on
  delivery, `--queue` lists what is waiting and how long. PI cadence for the smoke is
  approximately 09:00 and 21:00 KST.
- `./harness/selftest.sh` extended to **36 checks, 36 pass**.

**Ratifying the budgets did not unblock the smoke.** `provision.py` still refuses a real
launch, correctly: §3's cycle counts, RASPA version pin and tail-corrections setting remain
unratified brackets. Those three need a ruling before s01/s02 can be provisioned for real.

**One judgement flagged rather than defaulted:** whether replicates are told the escalation
answering cadence. Bei has implemented non-disclosure — §8 promises categories, not timing, and
publishing a schedule invites waiting on it — but what replicates are told should be a PI
ruling, not a harness default.

## LOG-2026-08-26-12 — Full harness loop dry-run end to end; one enforcement limit exposed
Assignment 4's cluster steps are blocked on the Dirac account, but its third item — dry-run the
full loop with a mock replicate — does not need it, so it was done now to de-risk the rest.
`harness/dryrun_loop.sh` + `harness/mock_replicate.py`.

The loop runs clean: provision both arms → mock replicates work 3 days under git → watchdog →
fleet ceiling → escalations, including a PI answer delivered against a queued item with latency
recorded → collect. Verified by inspecting **what the replicate saw**, not just harness output:
`s02`'s INBOX correctly received the hard-stop notice and the 75% token warning, and `s01`
received the chartered `scientific` sentence and nothing more.

**One real enforcement limit exposed, and deliberately left visible in the dry run.** The mock
`s02` reached **135 % of its compute budget** before the first watchdog poll saw it. The
watchdog is **polled, not inline**: it detects a breach and holds the queue, but cannot prevent
a replicate crossing 100 % between two polls. Charter §4's hard stop is therefore enforced as
*"stop on detection"*, not as a barrier. Poll frequency is the only control, and it should be
set against the largest plausible single-poll burn — at the measured 338× run-cost spread, one
long chunk can move usage a long way between polls. Recorded in `harness/README.md` as limit 0;
**the mock is left overspending on purpose so the limit stays visible rather than being tuned
away.**

Not a defect to fix silently: an inline barrier would require the harness to sit between the
replicate and the scheduler, which is a larger design change than the smoke needs. Flagged for
the PI to decide after the smoke.

## LOG-2026-08-26-13 — §3 flipped from the archived record; tail corrections were OFF, not on
PI ruled the last three gates. Two settled cleanly; one settled **against** the ruling's stated
expectation, and the principle was applied rather than the wording.

**Cycle counts** ratified: floor 2,000+10,000, Claim-grade 10,000+50,000, with the PI's
rationale recorded — longer production is unbiased for GCMC ensemble averages, so it reduces
variance without moving the expectation and Claim-grade comparability to the key is unaffected.
That same argument is why it does **not** extend to cutoff or tail corrections, which move the
expectation.

**RASPA pinned to 2.0.37** — read from the archived output headers (`Compiler and run-time
data`), together with gcc 4.8.5, compile date 2026-08-18, and the `build.qsub` recipe.

**Tail corrections: the record says OFF.** The ruling anticipated the archive would confirm the
charter's `[on]` and instructed §3 to state "on" with a citation. It does not. Archived RASPA
output headers show **`tailcorrection: no` on all 4,560 interaction pairs, in each of seven
independent runs**, plus `All potentials are unshifted` — including every methane pair, which
are the ones that matter. §3 now states **off**, applying the ruling's governing principle
(*the record governs*) rather than its literal wording, because its condition failed.

This is not a close call and it is not cosmetic:
- every reference number for this protocol, the answer key's own included, was produced with
  corrections off, so a Claim-grade number with them on would not be comparable to the key;
- Appendix A's thresholds (G1 > 230, G2 210–230) were calibrated on corrections-off numbers, so
  enabling corrections would leave the gates firing at the wrong values, silently — nothing in
  the gate text mentions the dependency.

**One edit reverses it** if the PI wants `on` regardless. Flagged rather than treated as
settled. The archive settling this also means item 3's fallback A/B job pair is **not needed**,
and the item-2 verification job now validates build, cutoff, shifting and tail-correction
behaviour in a single run.

**Hard stop** deferred post-smoke per ruling; poll interval tightened to 10 min (smoke) /
30 min (main) and the bound made exact and machine-computed:
`overshoot ≤ max_queued_jobs × poll_hours` → **8.33 CPU-h (2.45 %)** smoke, 4.00 CPU-h (0.25 %)
main. The watchdog prints it every run so the bound travels with the measurement. The observed
135 % mock overshoot is recorded in `harness/README.md` as a known bound, and the mock is left
overspending deliberately.

**Cadence non-disclosure** ratified and its rationale recorded: §8 promises categories, not
timing; a published schedule is a promise, a latency ledger is a measurement.

**`config.PROPOSED` is now empty and `provision.py` accepts a real launch configuration** —
verified by a real, non-dry-run provision of both arms with the **full 1,731-structure
database**: 1,731/1,731 checksums verified per arm, independently rechecked with `shasum -c`,
leak scan clean, 2.8 s. `./harness/selftest.sh` 41/41.

**New leak found on that first real provision, flagged not fixed:** §4's and §5's per-phase
tables show **both** rows, so a smoke replicate learns a 14-day main phase exists — that its own
run is a pilot. A replicate that thinks it is rehearsing has reason to work differently from one
that thinks it is not, which is a problem for a smoke meant to predict main-run behaviour. The
word deny-list could not catch it: "Smoke" and "Main" are innocuous, and the leak is made of
ordinary vocabulary arranged into a comparison. A **structural** check was added
(`leak_phase_disclosure`). Fix is one function in `provision.py`; it alters replicate-facing
charter text, so it is the PI's call.

## LOG-2026-08-26-14 — Calibration dependency written into Appendix A; phase leak closed at render time
PI ratified tail corrections OFF and ruled on the two flags. Both fixes applied and confirmed.

**Appendix A now declares its own dependency on §3.** G1's `> 230` and G2's `210–230` are
stated to be properties of the materials *as measured under §3*, and any §3 change requires
recalibration before the gates are used again. Worth a charter clause rather than a note in the
record because the dependency was invisible — nothing in the gate text referenced §3, and the
tail-corrections question came within one ruling of changing §3 in a way that would have left
both gates firing at the wrong values **silently**. A stale gate does not error; it keeps
issuing dispositions that look correct.

**Phase-table leak closed at render time.** `prereg/` master keeps all four phase rows
(pre-registration completeness); provisioned copies render only the replicate's own row in §4
and §5, with **no marker that anything was filtered** — a visible "(rows omitted)" would
disclose what the filtering exists to withhold, and would also tell the replicate its charter
had been edited for it. Rationale recorded: a replicate that believes it is rehearsing is
measured under a different self-model, and the smoke is the phase that can least afford it.

**Both halves of the leak scan are now standing pre-launch steps** and are documented in
`harness/README.md` with what each is blind to: the word deny-list cannot see a leak assembled
from ordinary vocabulary, and the structural checks cannot see a disclosure shape nobody has
thought of yet. The phase table is the worked example — "Smoke" and "Main" are innocuous words
and the leak lived entirely in their appearing as a comparison.

**Final pre-account confirmation, all green:**
- real non-dry-run provision of both arms, **full 1,731-structure database**: 1,731/1,731
  checksums verified per arm at copy time, independently re-verified with `shasum -c`
  (1,731 OK / 0 FAILED each);
- leak scan via the harness's own scanner, both halves: **HARD 0, WARN 0, STRUCTURAL 0** on
  both arms;
- arm split correct: s01 appendix present / 7 gates / schema / AUDIT.jsonl; s02 none of them;
- the new calibration note reaches the gated arm only, as intended;
- isolation: no remotes, no symlinks, no sealed material, no path back;
- `./harness/selftest.sh` **46/46**.

A defect was found and fixed during this work: `provision.py` used `re` without importing it,
so the first phase-rendering run failed. Caught because the verification greps came back empty
rather than because the script announced it — a reminder that a silent provisioning failure
looks much like a clean one at a glance.

**Remaining blocker is the Dirac account alone.** Runway: account → hello-world → single
verification job (build, cutoff, shifting and tail-correction behaviour validated together by
reproducing one reference number within statistical error) → provision s01/s02 on cluster
scratch → leak-scan the provisioned workspaces → report launch-ready.

## LOG-2026-08-26-15 — Cluster access: keypair generated, credential leak-scan made standing
Dirac account issued. Local preparation complete; the password-bearing steps cannot be done by
Bei and are with the PI.

- **ed25519 keypair generated** at `~/.ssh/bei_ed25519` (no passphrase), outside the repo. The
  private key is never read, copied or transmitted by any harness component.
- **Credential leak scanning is now a standing rule** (PI 2026-08-26), wired into provisioning
  and runnable repo-wide. Two independent checks, because a key leaks two different ways:
  by **filename** (someone copies `id_ed25519` in) and by **content** (someone pastes a key
  body into an otherwise innocent file). Either check alone misses one of them.
- The content markers are **built by string concatenation** so no literal marker exists in the
  source. Written verbatim, `config.py` would trip its own scanner, and the natural fix —
  exempting the scanner's own file — is exactly the kind of exemption that later hides a real
  leak. Verified: repo scans CLEAN, and a public key pasted into a repo file is caught.
- Root `.gitignore` added for credential patterns; runtime ledgers untracked.

**Topology: the PI's sketch does not match the recorded record, and the record is specific.**
The prior campaign's `~/.ssh/config` (kept outside its repo by that campaign's own standing
decision) documents, from direct observation on 2026-08-18:
- `143.248.130.178` is **`bronze3`, a gateway** — Ubuntu 20.04, **no scheduler**, no
  `/home/users`, no simulation codes. It is *not* the cluster.
- the cluster head node is **`143.248.125.145`**, hostname **`bnode0`** (= `dirac`/`dirac1`,
  one machine), home `/home/users/<user>`, PBS at `/usr/local/pbs/bin`, wrapper
  `/usr/local/mjs/qas`.
- the cluster is **firewalled from here directly** (TCP/22 filtered, silent drop); the
  whitelist was applied to the gateway only. Hence the jump.

So "the same command again" is very likely an approximation of a jump to a **different
address**, and the sketched `ProxyJump` block would jump a host to itself (`HostName` and
`ProxyJump` are the same address). Also relevant to the PI's "one install may cover both": the
two homes are at **different paths** (`/home/able` vs `/home/users/able`), so they are probably
**not** a shared filesystem and two installs will be needed.

None of this is asserted for the `Bei` account — it is what was true for `able` a week ago.
Verification comes first, before any config is written. TCP/22 to the gateway is confirmed open
from here.

## LOG-2026-08-26-16 — First access attempt rejected; host identity confirmed, credential is the failure
`ssh-copy-id` for `Bei@143.248.130.178` failed: two password attempts rejected, then
`Permission denied (publickey,password)`. Recorded as an event rather than retried silently.

What the failure rules **in** and **out**, from non-interactive diagnostics only:

- **Reachable and correct machine.** TCP/22 open; server is `OpenSSH_8.2p1 Ubuntu-4ubuntu0.1`,
  consistent with the recorded gateway `bronze3` (Ubuntu 20.04) and *not* with a PBS cluster
  head node.
- **Host identity verified against the prior campaign's own record.** The ed25519 host key
  offered now — `SHA256:XeBSJW0R5v/CoMjl9QdbNTqHX9wCnMU60jmbuasdeJo` — is byte-identical to the
  entry stored in `~/.ssh/known_hosts` on 2026-08-18. Same machine; no interception, no
  re-imaged host, no address reassignment.
- **The server offers `publickey,password`**, so password authentication is enabled and the
  method is not the problem.
- **Our new key is correctly not yet installed** — it was offered and refused, which is the
  expected state before `ssh-copy-id` succeeds.

So the failure is the **credential**, not the route, the host, the key, or the firewall. Most
likely a mistyped password; possible alternatives are a different username case on the gateway,
or a `Bei` account that exists only on the inner cluster while gateway access uses another
account.

Not attempted, and deliberately: the prior campaign's `able` key is still on this machine and
would allow logging into the gateway to check whether a `Bei` account exists there. That is a
different account from the one Bei was issued, and using it is a credential decision for the
PI, not an infrastructure default. Offered, not taken.

## LOG-2026-08-26-17 — Second credential attempt rejected; recorded topology confirmed unchanged
Password authentication for `Bei` on the gateway rejected again, this time via a plain `ssh`
with `PubkeyAuthentication=no` — so the failure is not an artefact of `ssh-copy-id` and not key
negotiation. Two independent invocations, four password attempts, all refused.

Topology re-verified from here, and it matches the prior campaign's record exactly:
- `143.248.130.178` (gateway) — **TCP/22 OPEN**.
- `143.248.125.145` (cluster head, `bnode0`) — **still filtered from this machine**, silent
  drop, exactly as recorded on 2026-08-18. The whitelist covers the gateway only, so the jump
  is genuinely required and the inner host cannot be reached directly.
- The prior campaign's `known_hosts` holds a stored key for the inner host, i.e. it did reach
  it — through the gateway.

**Bei is blocked and will not guess.** The remaining hypotheses are a wrong or stale password,
a different username on the gateway, or a `Bei` account provisioned on the cluster head but not
on the gateway. None can be distinguished without either a working credential or the PI's
authorisation to run a read-only diagnostic under the prior campaign's `able` key — which is
offered for the second time and still not taken unilaterally, because using an account Bei was
not issued is a credential decision, not an infrastructure one.

No further attempts will be made until the PI rules. Repeated password attempts against an
account that may not exist is exactly the pattern that triggers lockouts.

## LOG-2026-08-26-18 — Cluster access working end to end; sketched topology corrected on the record
Both hops passwordless under `~/.ssh/bei_ed25519`. The earlier password failures were a session
passthrough artefact, not the credential — the account exists on both machines, so the
hypotheses recorded at LOG-2026-08-26-17 are dead. **The `able`-key diagnostic was declined and
is closed; it was never used.**

**Verified topology — the sketch was wrong in two ways, both load-bearing:**

| Hop | Address | Host | Facts |
|---|---|---|---|
| 1 gateway | `143.248.130.178` | **`bronze3`** | Ubuntu 20.04 (5.8.0-44), home `/home/Bei`, **no scheduler**, no `/home/users`, no `/usr/local/pbs`, no `/usr/local/mjs` |
| 2 cluster | `143.248.125.145` | **`bnode0.kaist.ac.kr`** | home `/home/users/Bei`, PBS at `/usr/local/pbs/bin`, group wrapper `/usr/local/mjs/qas` |

1. **The second hop is a different address, not a repeat of the first.** From inside `bronze3`,
   `143.248.130.178` still resolves to `bronze3` itself (`getent hosts` → `bronze3`), so "the
   same command again" cannot be literal — it would be a self-jump. Reachability confirms the
   split: from this Mac `…130.178:22` is OPEN and `…125.145:22` is FILTERED (silent drop); from
   `bronze3`, `…125.145:22` is OPEN. The jump is genuinely required.
2. **`ProxyJump Bei@<ip>` does not work and the failure is silent-looking.** A bare
   host-and-user `ProxyJump` spawns a nested `ssh` that does **not** inherit `-i` /
   `IdentityFile`, falls back to password, and fails — which is what the sketch would have
   produced. `ProxyJump` must reference an **alias** that carries the identity. Observed
   directly before the fix.

`~/.ssh/config` updated with `dirac-bei-gw` (gateway) and `dirac-bei` (cluster, ProxyJump via
the alias), the verified topology recorded in-file as comments, and the prior campaign's `able`
blocks left untouched. Config backed up to `config.bak-20260826-bei`. Keys and config live
outside the repository; the credential scan confirms neither has entered it.

**Verification, all passing:** passwordless round-trip to both hops; `scp` up and down with a
byte-identical round trip; `qstat` visible — server `bnode0` **Active**, 28 jobs running, queues
`long` / `infi` / `dque` / `short` all enabled.

**One observation that bears on a ratified value:** queue `long` reports **Max 580**, against
the 129 running slots the prior campaign observed and on which Bei based the study-wide ceiling
of 160. The ceiling is therefore more conservative than assumed rather than less — no action
needed, but the basis is now known to be a floor, not the cap.

## LOG-2026-08-26-19 — Runway: hello-world exit 0, RASPA v2.0.37 pinned and building, workspaces provisioned to cluster scratch
Proceeding without check-ins per PI instruction. Nothing has failed; items below are recorded
as they completed.

**Hello-world.** Job `3470123.bnode0.kaist.ac.kr`, queue `short`, node `bnode4`,
**`Exit_status=0`**, walltime 3 s, output retrieved. Compiler on the node is **gcc 4.8.5
20150623 (Red Hat 4.8.5-36)** — byte-for-byte the compiler string in the prior campaign's
archived RASPA headers, so the build environment is the same one that produced the reference
numbers.

**RASPA source pinned properly, and the obvious route was wrong.** `Bei` has no RASPA, and
`/home/molsim_share/RASPA` turned out to be tutorial material only — no binary. Cloning
`iRASPA/RASPA2` gives HEAD, which reports **2.0.50**, not the pinned 2.0.37: the version string
lives in `src/output.c` and moves with the tree. Checked out tag **`v2.0.37`**, commit
**`4467e14c375c2e02f3839ffc63c14edf0bbde0a2`**, verified `output.c` emits `RASPA 2.0.37` before
building. Build submitted as job `3470124` with the prior campaign's exact autotools recipe.
Had the clone been used as-is, every number would have come from the wrong binary while looking
entirely normal.

**Reference numbers for the verification job**, from the prior campaign's raw screen output:
`2021[Cu][sql]2[ASR]6` — p65 **244.012 ± 1.228**, p58 **36.841 ± 0.183**, **WC 207.17 ± 1.24**
cm³/cm³. The benchmark CIF for it is **byte-identical** to the cluster's own
`/home/molsim_share/core2024_cifs` copy (sha256 `a4eb4713…`), so the reproduction compares like
with like. Inputs generated with the prior campaign's exact template, `UnitCells 2 2 2` computed
from perpendicular widths (18.77 / 18.77 / 21.33 Å against the 25.6 Å minimum-image requirement
— a naive read of the 24×24×22.6 Å edge lengths would have given 1 1 1 and violated it).

**Last charter bracket closed.** `[workspace path]` in §1 and §4 now references
`workspace_root` in `WORKSPACE.json` rather than a literal path — deliberately: a literal
`/home1/users/Bei/reps/smoke/s01` would have disclosed the sibling layout and the phase in the
path itself. Workspaces sit at `/home1/users/Bei/ws/<id>` on the 53 TB-free `/home1` volume.
**The charter body now has zero unset placeholders**; the only bracketed strings left are the
three literal format markers.

**Both workspaces provisioned to cluster scratch and verified there.**
- 1,731 CIFs each, **1,731 OK / 0 FAILED on arrival** at the cluster — the check that actually
  covers the transfer.
- Charter hashes byte-identical local ↔ cluster (`4bbd3c2e…` s01, `cf2eb190…` s02).
- Arm split intact after transfer: s01 has Appendix A + `AUDIT_SCHEMA.md` + `AUDIT.jsonl`; s02
  has none of them.
- git repos intact, 1 commit each, **no remotes**.
- **Leak scan CLEAN on both arms across all four checks** — HARD 0, CREDENTIAL 0, WARN 0,
  STRUCTURAL 0.

**Two silent traps hit and fixed during the transfer, both recorded in `harness/README.md`:**
1. macOS `tar` wrote an AppleDouble `._AUDIT_SCHEMA.md` into the s01 workspace — untracked junk
   inside a replicate's git repo. Swept; `COPYFILE_DISABLE=1` documented.
2. **`sha256sum -c` speaks the server's locale.** The cluster runs Korean, so success prints
   `성공`. The first verification reported **"1731 CIFs, 0 OK, 0 FAILED"** on a perfectly good
   transfer. Grepping only for `FAILED` would have reported success while verifying nothing at
   all. `LC_ALL=C` is now mandatory in the procedure.
