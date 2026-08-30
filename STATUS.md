# STATUS — live view of the running smoke campaign

*Machine-generated. Refreshed by `harness/poll.sh` each watchdog cycle.*

<!-- DIVERGENCE-PANEL:BEGIN -->
## Mechanical divergence panel — **RETIRED 2026-08-29T22:24:19Z**

The A/B panel compared the two **smoke** arms. Those arms are finished and archived
(`harness/state/SMOKE_ARCHIVED.json`), so the panel had no live subject: it was carrying figures
forward from a last successful collection and correctly refusing its own comparison, which is a
dashboard reporting on a fleet that no longer exists.

It is retired rather than repaired. The main phase is N = 16 and its comparison is not this
panel's two-arm shape; a main-phase divergence view is a separate instrument and is not
pre-registered yet. The sealed arm mapping in `harness/divergence_map.SEALED.json` is
**unopened and stays sealed** — retiring the display does not unseal anything.

Historical panels remain in git history. The smoke's own record is in `reps/smoke/` and
`archive/smoke/`.
<!-- DIVERGENCE-PANEL:END -->
