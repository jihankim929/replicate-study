"""Merge descriptor shards, apply the G3 pre-simulation screen, rank candidates.

Ranking model: a **local-density (Widom/LDA) estimate** integrated over the
sampled framework-energy histogram.  At each sampled point r the guest sees a
framework energy U(r), so the local fugacity is f_eff = f(P)*exp(-U/kT), and the
local density is taken to be the *bulk* CH4 density at that fugacity from the
Peng-Robinson equation of state with the same critical constants RASPA reads
from TraPPE/methane.def:

    N(P) = (1/M) sum_i rho_bulk(f(P) exp(-U_i/kT)) * 22414   [cm3(STP)/cm3]

This replaces a Langmuir surrogate whose saturation term was liquid pore
filling.  That version ranked the one structure whose working capacity I already
knew (206.5 cm3/cm3) **196th**, because liquid-filling saturation rewards huge
pores without limit: it predicted a 34 A cavity would fill to liquid density at
65 bar.  The LDA form cannot make that error -- as U -> 0 the local density
tends to the bulk gas density, so an empty cavity contributes the bulk
working capacity (~57 cm3/cm3) and no more, while a well-sized pore with
U ~ -1500 K is driven far up the isotherm and saturates by the EOS itself.

usage: rank.py <outdir>
"""
import csv, math, os, sys
import numpy as np

WS = os.environ.get("WSROOT", "/home1/users/Bei/ws/rep12")
sys.path.insert(0, os.path.join(WS, "bin"))
from descsweep import UBINS

R = 8.31446261815324
T = 298.0
P_HI, P_LO = 65.0e5, 5.8e5
TC, PC, OMEGA = 190.564, 4599200.0, 0.01142
STP = 22413.969        # cm3(STP) per mol


def pr_table(T=298.0, n=4000):
    """(log f, molar density mol/m3) along the 298 K isotherm from PR."""
    k = 0.37464 + 1.54226 * OMEGA - 0.26992 * OMEGA ** 2
    alpha = (1 + k * (1 - math.sqrt(T / TC))) ** 2
    a = 0.45724 * R * R * TC * TC / PC * alpha
    b = 0.07780 * R * TC / PC
    Ps = np.logspace(0, 11.5, n)
    lf, rho = [], []
    s2 = math.sqrt(2.0)
    for P in Ps:
        A = a * P / (R * R * T * T)
        B = b * P / (R * T)
        c = [1.0, -(1 - B), A - 3 * B * B - 2 * B, -(A * B - B * B - B ** 3)]
        rts = np.roots(c)
        Z = max(r.real for r in rts if abs(r.imag) < 1e-8 and r.real > B)
        lnphi = ((Z - 1) - math.log(Z - B)
                 - A / (2 * s2 * B) * math.log((Z + (1 + s2) * B) /
                                               (Z + (1 - s2) * B)))
        lf.append(math.log(P) + lnphi)
        rho.append(P / (Z * R * T))
    lf = np.array(lf)
    rho = np.array(rho)
    o = np.argsort(lf)
    return lf[o], rho[o]


LF, RHO = pr_table()


def fugacity(P):
    return float(np.exp(np.interp(math.log(P), np.log(np.exp(LF)), LF)))


def _fug(P):
    k = 0.37464 + 1.54226 * OMEGA - 0.26992 * OMEGA ** 2
    alpha = (1 + k * (1 - math.sqrt(T / TC))) ** 2
    a = 0.45724 * R * R * TC * TC / PC * alpha
    b = 0.07780 * R * TC / PC
    A = a * P / (R * R * T * T)
    B = b * P / (R * T)
    c = [1.0, -(1 - B), A - 3 * B * B - 2 * B, -(A * B - B * B - B ** 3)]
    rts = np.roots(c)
    Z = max(r.real for r in rts if abs(r.imag) < 1e-8 and r.real > B)
    s2 = math.sqrt(2.0)
    lnphi = ((Z - 1) - math.log(Z - B)
             - A / (2 * s2 * B) * math.log((Z + (1 + s2) * B) /
                                           (Z + (1 - s2) * B)))
    return P * math.exp(lnphi)


F_HI, F_LO = _fug(P_HI), _fug(P_LO)

# bin representative energies: midpoints, with finite stand-ins for the tails
UMID = []
for i in range(len(UBINS) - 1):
    lo, hi = UBINS[i], UBINS[i + 1]
    if lo < -1e8:
        UMID.append(-3400.0)
    elif hi > 1e8:
        UMID.append(1e9)
    else:
        UMID.append(0.5 * (lo + hi))
UMID = np.array(UMID)
# exp(-U/T), capped: beyond ~exp(40) the EOS table is already at its dense limit
BOLTZ = np.exp(np.clip(-UMID / T, -700, 40.0))


def lda_loading(hist, f):
    """cm3(STP)/cm3 from the sampled energy histogram at fugacity f."""
    tot = hist.sum()
    if tot == 0:
        return 0.0
    feff = f * BOLTZ
    rho = np.interp(np.log(np.maximum(feff, 1e-30)), LF, RHO)
    rho = np.where(UMID > 1e8, 0.0, rho)          # inside the framework
    return float((hist * rho).sum() / tot * STP * 1e-6)


def load():
    rows = []
    d = os.path.join(WS, "desc")
    for f in sorted(os.listdir(d)):
        if not f.endswith(".csv"):
            continue
        with open(os.path.join(d, f)) as fh:
            for r in csv.DictReader(fh):
                rows.append(r)
    return rows


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(WS, "tables")
    rows = load()
    out = []
    nerr = 0
    for r in rows:
        if r.get("natoms") in (None, "", "ERROR"):
            nerr += 1
            continue
        try:
            h = np.array([int(x) for x in r["uhist"].split(";")], dtype=float)
            nhi = lda_loading(h, F_HI)
            nlo = lda_loading(h, F_LO)
            out.append((r["name"], float(r["density"]), float(r["vf_he"]),
                        float(r["phi_geom"]), float(r["phi_boltz"]),
                        float(r["qst"]), float(r["lcd"]), float(r["pld_proxy"]),
                        float(r["mindist"]), int(r["natoms"]), int(r["nrep"]),
                        r["unknown"], r["elements"], nhi, nlo, nhi - nlo))
        except Exception:
            nerr += 1
    out.sort(key=lambda t: -t[15])
    cols = ("name,density,vf_he,phi_geom,phi_boltz,qst,lcd,pld_proxy,mindist,"
            "natoms,nrep,unknown,elements,n_hi_pred,n_lo_pred,wc_pred")
    with open(os.path.join(outdir, "descriptors.csv"), "w") as f:
        f.write(cols + "\n")
        for t in out:
            f.write('"%s",%.4f,%.4f,%.4f,%.5g,%.2f,%.2f,%.2f,%.3f,%d,%d,'
                    '"%s","%s",%.2f,%.2f,%.2f\n' % t)
    g3 = []
    for t in out:
        name, rho, mind, unk = t[0], t[1], t[8], t[11]
        fails = []
        if mind < 0.5:
            fails.append("overlapping_atoms")
        if not (0.20 <= rho <= 4.50):
            fails.append("density_out_of_bounds")
        if unk:
            fails.append("no_uff_entry:" + unk)
        g3.append((name, ";".join(fails) if fails else "PASS"))
    npass = sum(1 for _, s in g3 if s == "PASS")
    with open(os.path.join(outdir, "g3_screen.csv"), "w") as f:
        f.write("name,g3\n")
        for n, s in g3:
            f.write('"%s","%s"\n' % (n, s))
    print("rows=%d errors=%d g3_pass=%d g3_fail=%d f65=%.4g Pa f58=%.4g Pa"
          % (len(out), nerr, npass, len(g3) - npass, F_HI, F_LO))
    print("bulk_wc_empty_cavity=%.1f"
          % ((np.interp(math.log(F_HI), LF, RHO) -
              np.interp(math.log(F_LO), LF, RHO)) * STP * 1e-6))
    print("top15: " + " ".join("%.0f" % t[15] for t in out[:15]))
    w = [t[15] for t in out]
    print("quantiles: " + " ".join("p%s=%.1f" % (q, np.percentile(w, q))
                                   for q in (50, 90, 99, 99.9)))


if __name__ == "__main__":
    main()
