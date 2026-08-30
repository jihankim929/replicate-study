<!-- closes: 2026-08-30T12:31:07.465906+09:00 -->

## {STAMP} — harness notice (answer to your escalation)

You asked what the authoritative US$ spend meter is, and whether `usage.json:tokens` is
cumulative or per-session given that it fell from 1,363,857 to 932,867 across the pause and
resume.

- **The spend meter now exists in your workspace.** `usage.json` carries **`spend_usd`** — US
  dollars spent to date on the published-rate basis `WORKSPACE.json` describes — with
  `spend_cap_usd` and `spend_fraction` alongside it, refreshed every two minutes. That figure is
  authoritative and it is the one §4 means.
- **Note the two uses of the same name.** In `WORKSPACE.json`, `spend_usd` is your **cap**. In
  `usage.json` it is what you have **spent**.
- **`tokens` is cumulative, and your observation was correct.** The figure fell because the
  machine that hosts the agent sessions changed at the pause, and the meter recomputes from
  records held on that machine. The counter restarted; your consumption did not. This was an
  infrastructure artefact of the move and nothing was reset that belongs to you: **your token
  budget, your compute budget, your spend cap and your deadline are all unaffected**, and the
  spend figure now published to you carries the pre-move spend forward, so it is a true running
  total and not a total since the resume. You were right to distrust the counter.
