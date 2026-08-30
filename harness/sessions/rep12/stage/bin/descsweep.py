"""Descriptor sweep over a shard of the database.

usage: descsweep.py <shard_index> <n_shards> <npts> <out.csv>

One CSV row per structure.  Cheap Widom/geometric descriptors only -- no
RASPA, no cluster GCMC.  These feed structure selection; every number that
reaches the report comes from RASPA under the pinned protocol.
"""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mofcore as mc

WS = os.environ.get("WSROOT", "/home1/users/Bei/ws/rep12")
DB = os.path.join(WS, "db")
UFFP = os.path.join(WS, "toolchain/raspa/share/raspa/forcefield/UFF/force_field_mixing_rules.def")

R = 8.31446261815324
T = 298.0
# ideal-gas molar concentration -> cm3(STP)/cm3 conversion at the two pressures
CONV = 22413.969 / 1.0e6  # cm3STP per micromol ... see below
RHO_LIQ_CH4 = 0.4224      # g/cm3 at 111 K, used only for a saturation estimate

COLS = ["name", "natoms", "a", "b", "c", "alpha", "beta", "gamma", "V_uc",
        "mass", "density", "nx", "ny", "nz", "nrep", "mindist", "elements",
        "unknown", "vf_he", "phi_boltz", "phi_geom", "phi_half", "u_boltz",
        "qst", "lcd", "pld_proxy", "e10", "e50", "frac_neg", "sec", "npts",
        "uhist"]

# Energy-histogram bin edges in K.  The ranking model integrates a local-density
# estimate over this histogram, so the bins are fine where the Boltzmann factor
# moves fastest (-100 to 0 K) and coarse in the tails.
UBINS = [-1e9, -3000, -2400, -2000, -1700, -1450, -1250, -1100, -975, -875,
         -790, -715, -650, -590, -535, -485, -440, -400, -362, -327, -295,
         -265, -237, -211, -187, -165, -145, -126, -108, -92, -77, -63, -50,
         -38, -27, -17, -8, 0, 10, 25, 50, 100, 200, 500, 1e9]


def n_ideal(P, phi):
    """cm3(STP)/cm3 in the Henry limit at pressure P [Pa]."""
    c = P / (R * T)                    # mol/m3
    return phi * c * 22413.969e-6      # mol/m3 * cm3STP/mol / 1e6 cm3/m3


def describe(path, uff, npts):
    t0 = time.time()
    fr = mc.Frame(path, uff)
    uHe, uC, ds = fr.probe(npts, seed=12345)
    bHe = np.exp(np.clip(-uHe / T, -700, 700))
    bC = np.exp(np.clip(-uC / T, -700, 700))
    vf_he = float(bHe.mean())
    phi_b = float(bC.mean())
    phi_h = float(np.exp(np.clip(-uC / (2 * T), -700, 700)).mean())
    acc = ds > 1.865
    phi_g = float(acc.mean())
    if bC.sum() > 0:
        u_b = float((uC * bC).sum() / bC.sum())
    else:
        u_b = 0.0
    qst = (T - u_b) * R / 1000.0       # kJ/mol
    lcd = 2.0 * float(ds.max())
    pld = 2.0 * float(np.percentile(ds, 99.0))
    ua = uC[acc] if acc.any() else uC
    e10 = float(np.percentile(ua, 10))
    e50 = float(np.percentile(ua, 50))
    fneg = float((uC < 0).mean())
    hist = np.histogram(np.clip(uC, -9e8, 9e8), bins=UBINS)[0]
    els = "".join(sorted(set(fr.syms)))
    row = [fr.name, fr.natoms, fr.cell[0], fr.cell[1], fr.cell[2],
           fr.cell[3], fr.cell[4], fr.cell[5], fr.V, fr.mass, fr.density,
           int(fr.n[0]), int(fr.n[1]), int(fr.n[2]), fr.nrep,
           fr.min_framework_distance(), els, "|".join(fr.unknown),
           vf_he, phi_b, phi_g, phi_h, u_b, qst, lcd, pld, e10, e50, fneg,
           round(time.time() - t0, 2), npts,
           ";".join(str(int(x)) for x in hist)]
    return row


def main():
    shard = int(sys.argv[1])
    nsh = int(sys.argv[2])
    npts = int(sys.argv[3])
    out = sys.argv[4]
    uff = mc.load_uff(UFFP)
    files = sorted(os.listdir(DB))
    files = [f for f in files if f.endswith(".cif")]
    mine = files[shard::nsh]
    with open(out, "w") as fh:
        fh.write(",".join(COLS) + "\n")
        for i, f in enumerate(mine):
            try:
                row = describe(os.path.join(DB, f), uff, npts)
                fh.write(",".join(('"%s"' % v) if isinstance(v, str) else
                                  ("%.6g" % v if isinstance(v, float) else str(v))
                                  for v in row) + "\n")
            except Exception as e:
                fh.write('"%s",ERROR,,,,,,,,,,,,,,,"","%s",,,,,,,,,,,,,""\n'
                         % (f[:-4], str(e).replace(",", ";")[:120]))
            if i % 25 == 0:
                fh.flush()
    sys.stderr.write("shard %d done %d structures\n" % (shard, len(mine)))


if __name__ == "__main__":
    main()
