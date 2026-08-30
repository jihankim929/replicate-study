
## 2026-08-29 23:25 — protocol verification against RASPA's own echo
Before building a campaign on it, I checked that what RASPA actually applied is what §3
pins, by reading the parameter echo in the S03977 65 bar output rather than trusting the
input file I wrote:

- `CutOff VDW : 12.800000` — matches §3.
- `shift/k_B: 0.00000000 [K]` on **every** pair — potentials unshifted, as §3 requires.
- `tailcorrection: no` on **every** pair — tail corrections off. §3 is explicit that this
  comes from the force-field file's header rather than from `simulation.input`, and the
  echo confirms the file is the operative source.
- `CH4_sp3` is `148.0 K / 3.73 A` — TraPPE united-atom methane.
- Mixing is Lorentz-Berthelot as the file declares: CH4_sp3-Zn_ came out at
  `96.09995 K / 3.09500 A`, against sqrt(148 x 62.4) = 96.0999 and (3.73+2.46)/2 = 3.095.
- `Fugacity coefficient: 0.8729725844` — RASPA converted 65 bar to fugacity through
  Peng-Robinson using the critical constants in `methane.def`. This is RASPA's default
  behaviour and is what the reference numbers for this protocol were measured with.
- Volumetric conversion: RASPA printed `molecules/unit cell -> cm^3 STP/cm^3 = 12.7375209585`.
  Reproducing it independently, 22414 x 1e24 / (6.022e23 x 2922 A^3) = 12.738. The
  reported 16.7535750 molecules/unit cell x 12.7375 = 213.399 cm3/cm3, which is the number
  I recorded. Loading is reported **per unit cell** even though the simulation ran a
  2x2x2 supercell, so the conversion uses the primitive cell volume and no factor of 8
  is hiding anywhere.

The same Lorentz-Berthelot rules and the same 12.8 A truncated/unshifted/no-tail
treatment are what `bin/descriptors.py` implements, so the screening surrogate and the
production simulations are at least evaluating the same potential. That does not make the
surrogate accurate — it is not — but it removes one class of explanation for any
disagreement.

## 2026-08-29 23:20 — the starvation is a cap, not a shortage
Two hours in with zero cores. `quse` shows the amd partition at 80/160 and aa at 44/76
cluster-wide: roughly 110 cores sit idle that this account cannot touch, because Bei is
at its per-account cap on both. The pending list confirms the ordering is working as
designed rather than failing — for `aa` alone there are eighteen sibling jobs
(rep06, rep07, rep02, rep16, rep12, rep13, rep15) queued ahead of my 3322, and siblings
are being dispatched steadily (rep17 started nine jobs 38 minutes ago; rep09 started
eight just now). I am simply behind them, and I am behind them partly because I forfeited
my original position by resubmitting at 21:17.

Total work now queued is bounded and affordable: 21 bench + 144 calibration + 500 tier-1
cases, roughly 190 CPU-h against 1610 remaining. Even if all eleven jobs started at once
there is no budget risk, so the correct action is to leave the queue alone and wait.
