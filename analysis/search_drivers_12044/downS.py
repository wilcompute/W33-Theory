import os as _os
import sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ANA = _os.path.dirname(_HERE)
_sys.path.insert(0, _HERE)
"""S-type CP, down sector at the exact up solution: constrained fit on the full fixed set (incl. doublet Wilson component)."""
import json, sys
import numpy as np
from scipy.optimize import least_squares, minimize
from sfit import G, DATA, theta_c
from upS import up
UPS = {'+': (0.832764, 0.823581), '-': (2.318011, 2.308829)}
DK = ['ms_mb', 'md_ms', 'Vus', 'Vcb', 'Vub']


def homes(p, tau):
    ed, td, zd = p[0] + 1j * p[1], p[2] + 1j * p[3], p[4] + 1j * p[5]
    return np.array([[tau, ed], [ed, td]]), np.array([0, zd])


def fixfull(p, tau, gd, k):
    Om, z = homes(p, tau)
    M = G[gd]; A, B, C, D = M[:2, :2], M[:2, 2:], M[2:, :2], M[2:, 2:]
    W = C @ Om + D
    O2 = -np.conj((A @ Om + B) @ np.linalg.inv(W))
    z2 = -np.conj(np.linalg.inv(W).T @ z)
    r = [(Om - O2)[0, 1], (Om - O2)[1, 1], (Om - O2)[0, 0]]
    z0 = z2[0]                                  # doublet component of the image: must be a real element of Z/3
    rz = [z[1] - (z2[1] + k / 3), z0.imag + 0j, (z0.real - np.round(3 * z0.real) / 3) + 0j]
    v = np.array(r + rz)
    return np.concatenate([v.real, v.imag[:4]])


def dres(p, Ou):
    Od, z = homes(p, Ou[0, 0])
    if np.linalg.eigvalsh(Od.imag).min() < 1e-4 or abs(z[1].imag) / Od.imag[1, 1] > 60:
        return np.full(5, 30.0)
    try:
        Uu, su, _ = np.linalg.svd(theta_c(Ou, np.zeros(2, complex)))
        Ud, sd, _ = np.linalg.svd(theta_c(Od, z))
    except Exception:
        return np.full(5, 30.0)
    V = (Uu.conj().T @ Ud)[::-1, ::-1]
    o = dict(ms_mb=sd[1] / sd[0], md_ms=sd[2] / sd[1], Vus=abs(V[0, 1]), Vcb=abs(V[1, 2]), Vub=abs(V[0, 2]))
    out = np.array([np.log(max(o[q], 1e-300) / DATA[q][0]) / DATA[q][1] for q in DK])
    return out if np.all(np.isfinite(out)) else np.full(5, 30.0)


def J(p, Ou):
    Od, z = homes(p, Ou[0, 0])
    Uu, _, _ = np.linalg.svd(theta_c(Ou, np.zeros(2, complex)))
    Ud, _, _ = np.linalg.svd(theta_c(Od, z))
    V = (Uu.conj().T @ Ud)[::-1, ::-1]
    return float(np.imag(V[0, 0] * V[1, 1] * np.conj(V[0, 1]) * np.conj(V[1, 0])))


if __name__ == '__main__':
    sgn, gd, k, n, seed = sys.argv[1], sys.argv[2].replace('_', ' '), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    Ou = up(*UPS[sgn]); tau = Ou[0, 0]
    rng = np.random.default_rng(seed)
    best = None; nfeas = 0
    for _ in range(n):
        p0 = np.array([*(rng.normal(size=2) * 10 ** rng.uniform(-3, -0.5)), rng.uniform(-1, 1), 10 ** rng.uniform(-2, 0.7),
                       rng.uniform(-.5, .5), rng.normal(0, .3)])
        pr = least_squares(lambda p: fixfull(p, tau, gd, k), p0, xtol=1e-14, ftol=1e-14)   # project onto the fixed set
        if np.abs(fixfull(pr.x, tau, gd, k)).max() > 1e-9:
            continue
        nfeas += 1
        cons = {'type': 'eq', 'fun': lambda p: fixfull(p, tau, gd, k)}
        try:
            m = minimize(lambda p: float(np.sum(dres(p, Ou) ** 2)), pr.x, method='SLSQP', constraints=[cons],
                         options=dict(maxiter=400, ftol=1e-12))
            x = m.x
        except Exception:
            x = pr.x
        fr = float(np.abs(fixfull(x, tau, gd, k)).max())
        if fr > 1e-7:
            continue
        c = float(np.sum(dres(x, Ou) ** 2))
        if best is None or c < best[0]:
            best = (c, x.tolist(), fr)
    out = dict(up=sgn, gd=gd, k=k, starts=n, feasible=nfeas, chi2=best and best[0], x=best and best[1], fix=best and best[2],
               J=J(np.array(best[1]), Ou) if best else None,
               obs=dict(zip(DK, (dres(np.array(best[1]), Ou) if best else [None] * 5).tolist() if best else [])))
    json.dump(out, open(f'downS_{sgn}_{sys.argv[2]}_{k}_{seed}.json', 'w'), indent=1)
    print(json.dumps({q: out[q] for q in ('up', 'gd', 'k', 'feasible', 'chi2', 'fix', 'J')}), flush=True)
