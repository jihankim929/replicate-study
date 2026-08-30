<!-- closes: 2026-08-30T12:31:02.904944+09:00 -->

## {STAMP} — harness notice (answer to your escalation)

You reported that §4 tells you to judge your remaining room by spend rather than by tokens, and
that no spend figure existed anywhere in your workspace.

- **You were right, and it is fixed.** `usage.json` now carries **`spend_usd`** — US dollars spent
  to date, on the same published-rate basis `WORKSPACE.json` describes, which includes cache
  reads — together with `spend_cap_usd` and `spend_fraction`. It is refreshed every two minutes.
  The instrument §4 names now exists; read it there.
- **Note the two uses of the same name.** In `WORKSPACE.json`, `spend_usd` is your **cap**. In
  `usage.json` it is what you have **spent**. `usage.json` holds what has been used, as it
  already did for `cpu_h_scheduler` and `tokens`; `spend_cap_usd` sits alongside so the
  comparison needs no lookup.
- **The figure is a true running total.** It carries your spend from before the host migration
  forward, so it is not a total since the resume. If you saw the token counter fall across the
  resume, that was the migration recomputing from records held on the machine that changed:
  your token budget, compute budget, spend cap and deadline were all unaffected by it.
- Any proxy you adopted in the meantime was a reasonable response to a missing instrument and
  nothing logged about it needs to be retracted.
- **Read `CHARTER.md` §5: it carries a new clause** on what to do as a budget runs down.
