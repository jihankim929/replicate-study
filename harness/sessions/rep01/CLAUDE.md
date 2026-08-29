# Operating conventions

## Output handling
- Never re-read raw simulation output files wholesale. Extract the needed
  quantities once, immediately, into compact tables (CSV or markdown) in
  your workspace; consult the tables thereafter. Raw outputs are archive,
  not working memory.

## Working context
- STATE.md is your working memory. Keep it current and self-sufficient:
  after any long wait or context compaction, STATE.md alone must suffice
  to resume correctly. Prefer updating STATE.md over re-deriving from
  history.

## Session rhythm
- Do not poll the scheduler on a timer from your reasoning loop. Submit,
  record expected completion in JOBS.md, and check results in batches
  when jobs are expected to finish. Waiting is not working: between
  batches, either do analysis you have inputs for, or end the turn.

## Reports
- Status entries use the fixed form: DONE / RUNNING / BLOCKED / DECISION
  / NEXT, one line each. Detail lives in LOG.md, referenced not inlined.
