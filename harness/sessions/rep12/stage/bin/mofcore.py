"""Core CIF parsing + UFF/TraPPE descriptor engine (rep12).

Force-field parameters are read from the PINNED UFF mixing-rules file so that
screening descriptors use the same epsilon/sigma the claim-grade GCMC uses.
The helium probe is an AUXILIARY parameter (charter s3, Rev 22): the pinned
pseudo_atoms.def contains no helium, so the He void fraction (gate G3) uses the
Talu-Myers helium parameters stated in HE_PARAMS below.  Logged, not pinned.
"""
import math, os, re
import numpy as np

CUTOFF = 12.8
TEMP = 298.0

# auxiliary (non-pinned) helium probe: Talu & Myers J.Phys.Chem.B 105 (2001)
HE_PARAMS = (10.9, 2.64)
# pinned TraPPE united-atom methane (toolchain molecules/TraPPE + UFF mixing)
CH4_PARAMS = (148.0, 3.73)

MASSES = {
 "H":1.008,"He":4.0026,"Li":6.94,"Be":9.0122,"B":10.811,"C":12.011,"N":14.007,
 "O":15.999,"F":18.998,"Ne":20.180,"Na":22.990,"Mg":24.305,"Al":26.982,
 "Si":28.086,"P":30.974,"S":32.065,"Cl":35.453,"Ar":39.948,"K":39.098,
 "Ca":40.078,"Sc":44.956,"Ti":47.867,"V":50.942,"Cr":51.996,"Mn":54.938,
 "Fe":55.845,"Co":58.933,"Ni":58.693,"Cu":63.546,"Zn":65.38,"Ga":69.723,
 "Ge":72.63,"As":74.922,"Se":78.971,"Br":79.904,"Kr":83.798,"Rb":85.468,
 "Sr":87.62,"Y":88.906,"Zr":91.224,"Nb":92.906,"Mo":95.95,"Tc":98.0,
 "Ru":101.07,"Rh":102.91,"Pd":106.42,"Ag":107.87,"Cd":112.41,"In":114.82,
 "Sn":118.71,"Sb":121.76,"Te":127.60,"I":126.90,"Xe":131.29,"Cs":132.91,
 "Ba":137.33,"La":138.91,"Ce":140.12,"Pr":140.91,"Nd":144.24,"Pm":145.0,
 "Sm":150.36,"Eu":151.96,"Gd":157.25,"Tb":158.93,"Dy":162.50,"Ho":164.93,
 "Er":167.26,"Tm":168.93,"Yb":173.05,"Lu":174.97,"Hf":178.49,"Ta":180.95,
 "W":183.84,"Re":186.21,"Os":190.23,"Ir":192.22,"Pt":195.08,"Au":196.97,
 "Hg":200.59,"Tl":204.38,"Pb":207.2,"Bi":208.98,"Th":232.04,"Pa":231.04,
 "U":238.03,"Np":237.0,"Pu":244.0,"Am":243.0}


def load_uff(path):
    """element symbol -> (eps/kB [K], sigma [A]) from the pinned mixing rules."""
    out = {}
    with open(path) as f:
        for l in f:
            p = l.split()
            if len(p) < 4 or p[1] != "lennard-jones":
                continue
            name = p[0]
            if not name.endswith("_"):
                continue
            el = name[:-1]
            if el in MASSES:
                out[el] = (float(p[2]), float(p[3]))
    return out


_CELL_RE = re.compile(r"^_cell_(length|angle)_(\w+)\s+([-\d.eE+]+)")


def parse_cif(path):
    """Return (cell6, symbols, frac coords Nx3).  P1 CIFs only."""
    a = b = c = al = be = ga = None
    syms = []
    fr = []
    with open(path) as f:
        lines = f.read().split("\n")
    i = 0
    n = len(lines)
    while i < n:
        s = lines[i].strip()
        m = _CELL_RE.match(s)
        if m:
            v = float(m.group(3))
            k = m.group(2)
            if k == "a":
                a = v
            elif k == "b":
                b = v
            elif k == "c":
                c = v
            elif k == "alpha":
                al = v
            elif k == "beta":
                be = v
            elif k == "gamma":
                ga = v
        elif s == "loop_":
            j = i + 1
            tags = []
            while j < n and lines[j].strip().startswith("_"):
                tags.append(lines[j].strip().split()[0])
                j += 1
            if any(t.startswith("_atom_site_") for t in tags):
                idx = dict((t, k) for k, t in enumerate(tags))
                ix = idx.get("_atom_site_fract_x")
                iy = idx.get("_atom_site_fract_y")
                iz = idx.get("_atom_site_fract_z")
                its = idx.get("_atom_site_type_symbol")
                ilb = idx.get("_atom_site_label")
                while j < n:
                    t = lines[j].strip()
                    if not t or t.startswith("_") or t == "loop_" or t.startswith("#"):
                        break
                    p = t.split()
                    if len(p) < len(tags):
                        break
                    raw = p[its] if its is not None else p[ilb]
                    el = re.sub(r"[^A-Za-z]", "", raw)
                    if len(el) > 1:
                        el = el[0].upper() + el[1:].lower()
                    syms.append(el)
                    fr.append((float(p[ix]), float(p[iy]), float(p[iz])))
                    j += 1
                i = j
                continue
        i += 1
    if a is None or not syms:
        raise ValueError("unparsable cif " + path)
    return (a, b, c, al, be, ga), syms, np.array(fr, dtype=np.float64)


def cell_matrix(cell):
    a, b, c, al, be, ga = cell
    al, be, ga = math.radians(al), math.radians(be), math.radians(ga)
    ca, cb, cg, sg = math.cos(al), math.cos(be), math.cos(ga), math.sin(ga)
    cx = c * cb
    cy = c * (ca - cb * cg) / sg
    cz = math.sqrt(max(c * c - cx * cx - cy * cy, 1e-12))
    return np.array([[a, 0.0, 0.0], [b * cg, b * sg, 0.0], [cx, cy, cz]])


def perp_widths(M):
    V = abs(np.linalg.det(M))
    w = []
    for i in range(3):
        u, v = M[(i + 1) % 3], M[(i + 2) % 3]
        w.append(V / np.linalg.norm(np.cross(u, v)))
    return np.array(w), V


def supercell_counts(M, cutoff=CUTOFF):
    w, V = perp_widths(M)
    n = np.maximum(1, np.ceil(2.0 * cutoff / w).astype(int))
    return n, V, w


class Frame(object):
    def __init__(self, path, uff):
        self.name = os.path.basename(path)[:-4]
        cell, syms, fr = parse_cif(path)
        self.cell = cell
        self.syms = syms
        self.frac = fr % 1.0
        self.M = cell_matrix(cell)
        self.n, self.V, self.w = supercell_counts(self.M)
        self.natoms = len(syms)
        self.mass = sum(MASSES.get(s, 0.0) for s in syms)
        self.unknown = sorted(set(s for s in syms if s not in uff))
        self.density = self.mass / (self.V * 0.6022140761)
        nx, ny, nz = self.n
        sh = np.array(np.meshgrid(np.arange(nx), np.arange(ny), np.arange(nz),
                                  indexing="ij")).reshape(3, -1).T
        f2 = (self.frac[:, None, :] + sh[None, :, :]).reshape(-1, 3)
        self.Ms = self.M * self.n[:, None]
        self.sfrac = f2 / self.n[None, :]
        self.nrep = int(np.prod(self.n))
        eps = np.array([uff.get(s, (0.0, 0.0))[0] for s in syms])
        sig = np.array([uff.get(s, (0.0, 0.0))[1] for s in syms])
        self.eps = np.repeat(eps, self.nrep)
        self.sig = np.repeat(sig, self.nrep)

    def min_framework_distance(self, cap=6000, seed=0):
        """smallest nonzero framework-framework distance in the unit cell."""
        F = self.frac
        n = len(F)
        sel = np.arange(n)
        if n > cap:
            sel = np.random.RandomState(seed).choice(n, cap, replace=False)
        best = 1e9
        for k in range(0, len(sel), 256):
            q = F[sel[k:k + 256]]
            d = q[:, None, :] - F[None, :, :]
            d -= np.round(d)
            v = d.dot(self.M)
            r = np.sqrt((v * v).sum(-1))
            r[r < 1e-6] = 1e9
            best = min(best, float(r.min()))
        return best

    def probe(self, npts, seed=0, chunk=200):
        """Random Widom sampling.  Returns (uHe, uCH4 in K, dmin_surf in A)."""
        rs = np.random.RandomState(seed)
        pf = rs.random_sample((npts, 3))
        uHe = np.empty(npts)
        uCH4 = np.empty(npts)
        dsurf = np.empty(npts)
        eHe, sHe = HE_PARAMS
        eC, sC = CH4_PARAMS
        epsHe = 4.0 * np.sqrt(self.eps * eHe)
        sigHe2 = (0.5 * (self.sig + sHe)) ** 2
        epsC = 4.0 * np.sqrt(self.eps * eC)
        sigC2 = (0.5 * (self.sig + sC)) ** 2
        half = 0.5 * self.sig
        rc2 = CUTOFF * CUTOFF
        for k in range(0, npts, chunk):
            q = pf[k:k + chunk]
            d = q[:, None, :] - self.sfrac[None, :, :]
            d -= np.round(d)
            v = d.dot(self.Ms)
            r2 = (v * v).sum(-1)
            r2c = np.where(r2 < rc2, r2, np.inf)
            x = sigHe2[None, :] / r2c
            x3 = x * x * x
            uHe[k:k + chunk] = (epsHe[None, :] * (x3 * x3 - x3)).sum(1)
            x = sigC2[None, :] / r2c
            x3 = x * x * x
            uCH4[k:k + chunk] = (epsC[None, :] * (x3 * x3 - x3)).sum(1)
            dsurf[k:k + chunk] = (np.sqrt(r2) - half[None, :]).min(1)
        return uHe, uCH4, dsurf
