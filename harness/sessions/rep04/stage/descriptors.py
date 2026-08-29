#!/usr/bin/env python3
"""Cheap per-structure descriptors by Widom sampling of the CH4-framework potential.

For each structure we draw N uniform random points in the unit cell and evaluate
the TraPPE methane (united-atom, single site) / UFF framework Lennard-Jones
energy with the pinned protocol's real-space treatment: 12.8 A cutoff,
truncated, unshifted, no tail correction, no charges.  From the resulting sample
of U we record

  * a histogram of U (so any model of the form n = <g(U)> can be refit later
    without touching the structures again),
  * the Henry-limit Boltzmann factor <exp(-bU)>,
  * hard-sphere probe-accessible fractions at three probe radii,
  * a local-density-approximation estimate of absolute loading at both protocol
    pressures.

The LDA estimate is a screening surrogate only.  It is calibrated against real
GCMC and never enters a reported number.

usage: descriptors.py <sid_list_file> <out_csv> [nsamples]
"""
import sys, os, math, csv
import numpy as np

WS = os.environ.get('REP04_WS', '/home1/users/Bei/ws/rep04')
UFF = os.path.join(WS, 'toolchain/raspa/share/raspa/forcefield/UFF/force_field_mixing_rules.def')
CUTOFF = 12.8
T = 298.0
KB = 1.0                      # energies carried in kelvin throughout
NBINS = 90
UMIN, UMAX = -9000.0, 0.0     # K; bins over attractive energies
# TraPPE methane united atom, as it appears in the pinned mixing-rules file.
PROBE = 'CH4_sp3'
# hard-sphere probe radii (A) for purely geometric accessible fractions
HS_RADII = (1.0, 1.6, 1.865)


def load_uff():
    eps, sig = {}, {}
    with open(UFF) as f:
        lines = [l for l in f]
    n = int(lines[3].split()[0])
    for l in lines[5:5 + n]:
        t = l.split()
        if len(t) >= 4 and t[1] == 'lennard-jones':
            eps[t[0]] = float(t[2]); sig[t[0]] = float(t[3])
    return eps, sig


def read_cif(path):
    cell = {}
    tags = None
    els, fx, fy, fz = [], [], [], []
    idx_sym = idx_lab = ix = iy = iz = None
    reading = False
    for line in open(path, 'r', errors='replace'):
        s = line.strip()
        if not s or s.startswith('#'):
            continue
        low = s.lower()
        if low.startswith('_cell_length_') or low.startswith('_cell_angle_'):
            cell[low.split()[0]] = float(s.split()[1]); continue
        if low == 'loop_':
            tags = []; reading = False; continue
        if tags is not None and s.startswith('_'):
            tags.append(low); continue
        if tags is not None:
            if '_atom_site_fract_x' in tags:
                idx_sym = tags.index('_atom_site_type_symbol') if '_atom_site_type_symbol' in tags else None
                idx_lab = tags.index('_atom_site_label') if '_atom_site_label' in tags else None
                ix = tags.index('_atom_site_fract_x'); iy = tags.index('_atom_site_fract_y')
                iz = tags.index('_atom_site_fract_z'); reading = True
            else:
                reading = False
            tags = None
        if reading:
            t = s.split()
            if len(t) <= max(ix, iy, iz):
                reading = False; continue
            el = t[idx_sym] if idx_sym is not None else ''.join(c for c in t[idx_lab] if c.isalpha())
            els.append(el); fx.append(float(t[ix])); fy.append(float(t[iy])); fz.append(float(t[iz]))
    return cell, els, np.array([fx, fy, fz]).T


def cell_matrix(c):
    a, b, cc = c['_cell_length_a'], c['_cell_length_b'], c['_cell_length_c']
    al, be, ga = (math.radians(c['_cell_angle_alpha']), math.radians(c['_cell_angle_beta']),
                  math.radians(c['_cell_angle_gamma']))
    v1 = np.array([a, 0.0, 0.0])
    v2 = np.array([b*math.cos(ga), b*math.sin(ga), 0.0])
    cx = cc*math.cos(be)
    cy = cc*(math.cos(al) - math.cos(be)*math.cos(ga))/math.sin(ga)
    cz = math.sqrt(max(cc*cc - cx*cx - cy*cy, 1e-12))
    v3 = np.array([cx, cy, cz])
    return np.array([v1, v2, v3])          # rows are lattice vectors


def perp_widths(M):
    V = abs(np.linalg.det(M))
    return np.array([V/np.linalg.norm(np.cross(M[1], M[2])),
                     V/np.linalg.norm(np.cross(M[0], M[2])),
                     V/np.linalg.norm(np.cross(M[0], M[1]))])


def peng_robinson_fugacity(P, T=298.0, Tc=190.564, Pc=4599200.0, w=0.01142):
    R = 8.314462618
    k = 0.37464 + 1.54226*w - 0.26992*w*w
    alpha = (1.0 + k*(1.0 - math.sqrt(T/Tc)))**2
    a = 0.45724*R*R*Tc*Tc/Pc*alpha
    b = 0.07780*R*Tc/Pc
    A = a*P/(R*R*T*T); B = b*P/(R*T)
    coef = [1.0, -(1.0 - B), A - 3*B*B - 2*B, -(A*B - B*B - B**3)]
    roots = np.roots(coef)
    Z = max(r.real for r in roots if abs(r.imag) < 1e-8 and r.real > 0)
    lnphi = (Z - 1.0 - math.log(Z - B)
             - A/(2*math.sqrt(2)*B)*math.log((Z + (1+math.sqrt(2))*B) /
                                             (Z + (1-math.sqrt(2))*B)))
    return P*math.exp(lnphi), Z


def sample_structure(path, eps, sig, nsamp, rng):
    cell, els, frac = read_cif(path)
    M = cell_matrix(cell)
    V = abs(np.linalg.det(M))
    w = perp_widths(M)
    # replicate framework so every sample point in the home cell sees all
    # neighbours within CUTOFF
    reps = [int(math.ceil(CUTOFF/wi)) for wi in w]
    shifts = np.array([[i, j, k]
                       for i in range(-reps[0], reps[0]+1)
                       for j in range(-reps[1], reps[1]+1)
                       for k in range(-reps[2], reps[2]+1)], dtype=np.float64)
    allf = (frac[:, None, :] + shifts[None, :, :]).reshape(-1, 3)
    tile = np.tile(np.arange(len(els)), (len(shifts), 1)).T.reshape(-1)
    order = np.argsort(tile, kind='stable')
    allf = allf[np.argsort(np.repeat(np.arange(len(els)), len(shifts)), kind='stable')]
    xyz = (allf @ M).astype(np.float32)
    elrep = np.repeat(np.array(els), len(shifts))

    # per-atom mixed LJ parameters against the methane probe
    ep = np.array([math.sqrt(eps[e + '_']*eps[PROBE]) for e in els], dtype=np.float32)
    sg = np.array([0.5*(sig[e + '_'] + sig[PROBE]) for e in els], dtype=np.float32)
    epr = np.repeat(ep, len(shifts)); sgr = np.repeat(sg, len(shifts))
    # UFF radii for the hard-sphere probes: sigma/2 of the framework atom
    rad = np.array([0.5*sig[e + '_'] for e in els], dtype=np.float32)
    radr = np.repeat(rad, len(shifts))

    # prune atoms that cannot reach the home cell at all
    lo = xyz.min(axis=0)
    keep = np.ones(len(xyz), dtype=bool)
    corners = (np.array([[i, j, k] for i in (0, 1) for j in (0, 1) for k in (0, 1)],
                        dtype=np.float64) @ M).astype(np.float32)
    bmin = corners.min(axis=0) - CUTOFF; bmax = corners.max(axis=0) + CUTOFF
    keep = np.all((xyz >= bmin) & (xyz <= bmax), axis=1)
    xyz, epr, sgr, radr = xyz[keep], epr[keep], sgr[keep], radr[keep]

    c2 = np.float32(CUTOFF*CUTOFF)
    hist = np.zeros(NBINS + 2, dtype=np.int64)   # [<UMIN] + NBINS + [>=UMAX]
    boltz_sum = 0.0
    hs_hits = np.zeros(len(HS_RADII), dtype=np.int64)
    usum = 0.0; ucount = 0
    beta = 1.0/T

    CH = 2048
    umin_seen = 1e30
    ulist = []
    done = 0
    while done < nsamp:
        n = min(CH, nsamp - done)
        pf = rng.random_sample((n, 3))
        p = (pf @ M).astype(np.float32)
        d = p[:, None, :] - xyz[None, :, :]
        r2 = np.einsum('ijk,ijk->ij', d, d)
        within = r2 < c2
        # hard-sphere accessibility: no framework atom closer than rad+probe
        rmin_gap = np.where(within, np.sqrt(r2) - radr[None, :], np.float32(1e9)).min(axis=1)
        for i, pr in enumerate(HS_RADII):
            hs_hits[i] += int((rmin_gap >= pr).sum())
        sr2 = np.where(within, (sgr[None, :]**2)/np.maximum(r2, np.float32(1e-6)), np.float32(0.0))
        sr6 = sr2*sr2*sr2
        u = (4.0*epr[None, :]*(sr6*sr6 - sr6)).sum(axis=1)     # kelvin
        ulist.append(u.astype(np.float32))
        done += n

    u = np.concatenate(ulist)
    umin_seen = float(u.min())
    # Boltzmann average, guarded against overflow on hard overlaps
    uc = np.clip(u, -1e5, 1e5)
    boltz = np.exp(-uc/T, dtype=np.float64)
    kh = float(boltz.mean())
    idx = np.clip(((u - UMIN)/(UMAX - UMIN)*NBINS).astype(np.int64) + 1, 0, NBINS + 1)
    idx[u < UMIN] = 0; idx[u >= UMAX] = NBINS + 1
    hist = np.bincount(idx, minlength=NBINS + 2)
    return dict(V=V, natoms=len(els), reps=reps, u=u, kh=kh, hist=hist,
                hs=hs_hits/float(nsamp), umin=umin_seen,
                mass=None)


def lda_loading(u, V, f_Pa, T=298.0, vex=63.0):
    """Local-density-approximation absolute loading, molecules per unit cell.

    rho(r) = rho0 exp(-bU) / (1 + rho0 vex exp(-bU)); rho0 from the fugacity as
    an ideal gas.  vex is a single excluded-volume parameter, calibrated later.
    """
    kB = 1.380649e-23
    rho0 = f_Pa/(kB*T)*1e-30                 # molecules per A^3
    b = np.exp(-np.clip(u, -1e4, 1e4)/T, dtype=np.float64)
    dens = rho0*b/(1.0 + rho0*vex*b)
    return float(dens.mean()*V)


def main():
    sids = [l.split()[0] for l in open(sys.argv[1]) if l.strip()]
    out = sys.argv[2]
    nsamp = int(sys.argv[3]) if len(sys.argv) > 3 else 20000
    eps, sig = load_uff()
    smap = {}
    for l in open(os.path.join(WS, 'manifest/sid_map.tsv')):
        a, b = l.split('\t'); smap[a] = b.strip()
    f65, _ = peng_robinson_fugacity(6500000.0)
    f58, _ = peng_robinson_fugacity(580000.0)
    rng = np.random.RandomState(20260829)
    cols = (['sid', 'V_A3', 'natoms', 'kh_boltz', 'umin_K', 'umean_neg_K',
             'frac_U_lt0', 'frac_U_ltm500', 'frac_U_ltm1000', 'frac_U_ltm1500']
            + ['hs_%g' % r for r in HS_RADII]
            + ['lda65_uc', 'lda58_uc', 'lda65_v', 'lda58_v', 'lda_dc_v']
            + ['h%d' % i for i in range(NBINS + 2)])
    new = not os.path.exists(out)
    fh = open(out, 'a')
    if new:
        fh.write(','.join(cols) + '\n')
    for sid in sids:
        try:
            path = os.path.join(WS, 'db', smap[sid])
            d = sample_structure(path, eps, sig, nsamp, rng)
            u = d['u']; V = d['V']
            n65 = lda_loading(u, V, f65); n58 = lda_loading(u, V, f58)
            # molecules/unit cell -> cm^3 STP/cm^3 : n/V * 22414 * 1e24/6.022e23
            conv = 22413.96/(6.02214076e23)*1e24/V
            row = [sid, '%.4f' % V, d['natoms'], '%.6g' % d['kh'], '%.6g' % d['umin'],
                   '%.6g' % float(u[u < 0].mean()) if (u < 0).any() else '0',
                   '%.5f' % float((u < 0).mean()), '%.5f' % float((u < -500).mean()),
                   '%.5f' % float((u < -1000).mean()), '%.5f' % float((u < -1500).mean())]
            row += ['%.5f' % x for x in d['hs']]
            row += ['%.4f' % n65, '%.4f' % n58, '%.4f' % (n65*conv), '%.4f' % (n58*conv),
                    '%.4f' % ((n65 - n58)*conv)]
            row += ['%d' % x for x in d['hist']]
            fh.write(','.join(str(x) for x in row) + '\n')
        except Exception as e:
            fh.write('%s,ERR,%s\n' % (sid, type(e).__name__))
        fh.flush()
    fh.close()


if __name__ == '__main__':
    main()
