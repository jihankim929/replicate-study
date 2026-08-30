# Analysis plan — contamination exposure

**Pre-registered 2026-08-31, by PI ruling on REPORT 007, before any outcome analysis has been
run.** Added while the campaign is live and before collection, so this is a pre-registration and
not a post-hoc adjustment.

## The line

> **Contamination-exposed replicates are flagged, their exposure described, and every concordance
> analysis is reported both with and without them.**

## What "contamination-exposed" means here

A replicate is contamination-exposed if another replicate's working material — state, strategy
account, current-best numbers, or report text — entered its session or its workspace, by any
route, at any time during the campaign.

It is a statement about the **apparatus**, not about the replicate. Exposure is something that
happened to a replicate; it is not conduct, it is not a finding about the quality of its work,
and it carries no penalty.

## The register

`harness/state/incident_20260831_tmp_collision/contamination_exposed.json` is the authoritative
list, with the content that crossed, the vector and the timestamps. As of 2026-08-31 it holds:

- **rep01** — received rep09's live report draft, including rep09's strategy account and
  comparative best numbers, surfaced into its session at 02:59:13Z on 2026-08-30 and referenced
  in its own next turn.
- **rep03** — received rep09's STATE.md content into its workspace.

The register is append-only in effect: an entry is added if further exposure is established, and
an entry is never removed. If the list changes before collection, this file is not rewritten —
the register is the list.

## How it is reported

1. Every concordance analysis is run twice: over all replicates, and over the non-exposed subset.
2. Both results are reported, together, with the n of each. Neither is the headline; the
   difference between them is itself a result.
3. The exposure is described in the text — what crossed, to whom, when, and by what route — not
   summarised as a flag.
4. If the two analyses disagree materially, that disagreement is reported as a finding about the
   study's apparatus and not resolved by choosing one.

## Disclosure

The incident is disclosed in the paper, with its mechanism and this plan.
