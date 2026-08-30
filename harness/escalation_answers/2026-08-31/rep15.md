<!-- closes: 2026-08-30T12:31:12.055472+09:00 -->

## {STAMP} — harness notice (answer to your escalation)

You wrote that `usage.json` published compute and tokens but no spend figure, that §4 says to
judge remaining room by spend rather than tokens, and that its token counter had reset from
2,275,306 to 268,197 across the 11:42 resume — so neither cumulative spend nor cumulative tokens
was readable from your workspace.

- **The spend meter now exists in your workspace.** `usage.json` carries **`spend_usd`** — US
  dollars spent to date on the published-rate basis `WORKSPACE.json` describes — with
  `spend_cap_usd` and `spend_fraction` alongside, refreshed every two minutes.
- **Note the two uses of the same name.** In `WORKSPACE.json`, `spend_usd` is your **cap**. In
  `usage.json` it is what you have **spent**.
- **The token counter reset was an infrastructure artefact, and your reading of it was correct.**
  The machine hosting the agent sessions changed at the pause and the meter recomputes from
  records held on that machine, so the counter restarted while your consumption did not.
  **Your token budget, compute budget, spend cap and deadline are all unaffected.** The spend
  figure now published to you carries the pre-move spend forward, so it is a true running total.
