<!-- closes: 2026-08-30T13:30:40.272964+09:00 -->

## {STAMP} — harness notice (answer to your escalation)

You wrote that §4 tells you to judge your remaining room by spend, that no spend figure existed
anywhere in your workspace, and that you were proceeding on the token meter as a proxy and
logging it as a CHARTER-READ.

- **You were right, and it is fixed.** `usage.json` now carries **`spend_usd`** — US dollars spent
  to date on the same published-rate basis `WORKSPACE.json` describes — together with
  `spend_cap_usd` and `spend_fraction`. It is refreshed every two minutes. The instrument §4
  names now exists; read it there.
- **Note the two uses of the same name.** In `WORKSPACE.json`, `spend_usd` is your **cap**. In
  `usage.json` it is what you have **spent**. `usage.json` holds what has been used, as it
  already did for `cpu_h_scheduler` and `tokens`; `spend_cap_usd` is carried alongside so the
  comparison needs no lookup.
- Your proxy reading was a reasonable response to a missing instrument and your CHARTER-READ log
  entry is correct as written. Nothing needs to be retracted.
- Your budgets and deadline are unchanged by this.
