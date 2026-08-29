"""Geometric pore descriptors on a fractional grid, one structure at a time.

For every grid point in the unit cell we compute the clearance
    c(r) = min_i ( |r - r_i| - sigma_i/2 )
over all framework atoms i and their periodic images, with sigma_i taken from
the pinned UFF mixing-rules file. A point is accessible to a spherical probe of
radius r_p when c(r) > r_p. The probe radius for methane is sigma_CH4/2, with
sigma_CH4 = 3.73 A from the same pinned file (TraPPE united-atom methane).

This is a *screening* descriptor: it is geometry only, it uses no simulation,
and no number produced here enters the final report as a capacity. Its purpose
is to decide which structures are worth spending GCMC on.

The clearance field is truncated at RCUT; clearances above that are reported as
RCUT, which only affects the largest-cavity estimate, never the accessible
fractions for probes smaller than RCUT.
"""
import os, sys, csv, math, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cifutil

WS = os.path.dirname(HERE)
RCUT = 5.0                 # clearance field truncation, angstrom
TARGET_SPACING = 0.30      # angstrom, perpendicular
MAX_POINTS = 2_000_000
PROBES = [1.0, 1.4, 1.865, 2.2, 2.6, 3.0]
SIGMA_CH4 = 3.73


def load_sigmas():
    """sigma (A) per element symbol from the pinned UFF mixing rules."""
    path = os.path.join(WS, "toolchain/raspa/share/raspa/forcefield/UFF",
                        "force_field_mixing_rules.def")
    sig = {}
    for line in open(path).read().splitlines()[4:]:
        p = line.split()
        if len(p) >= 4 and p[1] == "lennard-jones":
            name = p[0]
            if name.endswith("_"):
                sig[name[:-1]] = float(p[3])
    return sig


SIG = load_sigmas()


def descriptors(cifpath):
    d = cifutil.parse_cif(cifpath)
    a, b, c = d["a"], d["b"], d["c"]
    al, be, ga = d["alpha"], d["beta"], d["gamma"]
    V = cifutil.volume(a, b, c, al, be, ga)
    M = np.array(cifutil.cell_matrix(a, b, c, al, be, ga))   # rows = cell vectors
    wa, wb, wc = cifutil.perp_widths(a, b, c, al, be, ga)
    w = np.array([wa, wb, wc])

    n = np.maximum(4, np.ceil(w / TARGET_SPACING).astype(int))
    while n.prod() > MAX_POINTS:
        n = np.maximum(4, (n * 0.85).astype(int))

    frac = np.array([[x[1] % 1.0, x[2] % 1.0, x[3] % 1.0] for x in d["atoms"]])
    radii = np.array([SIG.get(x[0], 3.0) * 0.5 for x in d["atoms"]])

    clear = np.full(tuple(n), RCUT, dtype=np.float32)

    # image range needed so that every atom within RCUT of the cell is seen
    img = [int(math.ceil(RCUT / w[i])) for i in range(3)]
    ax = [np.arange(ni) for ni in n]

    for k in range(len(frac)):
        r_i = radii[k]
        reach = RCUT + r_i
        df = reach / w                      # fractional half-width of the box
        for ia in range(-img[0], img[0] + 1):
            for ib in range(-img[1], img[1] + 1):
                for ic in range(-img[2], img[2] + 1):
                    f0 = frac[k] + np.array([ia, ib, ic], dtype=float)
                    lo = np.ceil((f0 - df) * n).astype(int)
                    hi = np.floor((f0 + df) * n).astype(int)
                    lo = np.maximum(lo, 0)
                    hi = np.minimum(hi, n - 1)
                    if np.any(hi < lo):
                        continue
                    sl = tuple(slice(lo[i], hi[i] + 1) for i in range(3))
                    d0 = (ax[0][sl[0]] / n[0] - f0[0])
                    d1 = (ax[1][sl[1]] / n[1] - f0[1])
                    d2 = (ax[2][sl[2]] / n[2] - f0[2])
                    # cartesian delta = d0*A + d1*B + d2*C, broadcast over the box
                    dx = (d0[:, None, None] * M[0, 0] + d1[None, :, None] * M[1, 0]
                          + d2[None, None, :] * M[2, 0])
                    dy = (d1[None, :, None] * M[1, 1] + d2[None, None, :] * M[2, 1]
                          + d0[:, None, None] * M[0, 1])
                    dz = (d2[None, None, :] * M[2, 2] + d0[:, None, None] * M[0, 2]
                          + d1[None, :, None] * M[1, 2])
                    dist = np.sqrt(dx * dx + dy * dy + dz * dz) - r_i
                    np.minimum(clear[sl], dist.astype(np.float32), out=clear[sl])

    flat = clear.ravel()
    npts = flat.size
    phis = [float((flat > p).sum()) / npts for p in PROBES]
    lcd = float(2.0 * flat.max())
    mass = 0.0
    return dict(volume=V, npts=npts, phis=phis, lcd=lcd,
                spacing=float((V / npts) ** (1.0 / 3.0)))


HEADER = ("id,name,volume,lcd_capped,spacing," +
          ",".join("phi_%.3f" % p for p in PROBES))


def row_for(idx, name, cifpath):
    r = descriptors(cifpath)
    return "%d,%s,%.3f,%.3f,%.3f,%s" % (
        idx, name, r["volume"], r["lcd"], r["spacing"],
        ",".join("%.5f" % x for x in r["phis"]))


def _work(t):
    idx, name = t
    try:
        return row_for(idx, name, os.path.join(WS, "db", name + ".cif"))
    except Exception as e:
        return "%d,%s,nan,nan,nan%s" % (idx, name, ",nan" * len(PROBES))


if __name__ == "__main__":
    import multiprocessing as mp
    lo, hi, outcsv, nproc = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], int(sys.argv[4])
    rows = list(csv.DictReader(open(os.path.join(WS, "manifests/structures.csv"))))
    tasks = [(int(r["id"]), r["cif"]) for r in rows if lo <= int(r["id"]) < hi]
    with open(outcsv, "w", 1) as f:
        f.write(HEADER + "\n")
        with mp.Pool(nproc) as pool:
            for line in pool.imap(_work, tasks, chunksize=4):
                f.write(line + "\n")
    print("done", len(tasks))
