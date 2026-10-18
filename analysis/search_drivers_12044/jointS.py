import os as _os
import sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ANA = _os.path.dirname(_HERE)
_sys.path.insert(0, _HERE)
"""S-type generalised CP, joint fit: up home fixed by CP o g_u, down home by CP o g_d (S on the shared doublet torus),
exact doublet-Wilson condition z0' = 0 (a Z/3 shift there is a left phase on Q that the up sector does not share)."""
import json, sys
import numpy as np
from scipy.optimize import least_squares, minimize
from sfit import G, DATA, theta_c
KEYS = list(DATA)


def homes(p):
    tau = p[0] + 1j * p[1]
    eu, ed, td, zd = p[2] + 1j * p[3], p[4] + 1j * p[5], p[6] + 1j * p[7], p[8] + 1j * p[9]
    return np.array([[tau, eu], [eu, tau]]), np.array([[tau, ed], [ed, td]]), np.array([0, zd])


def img(M, Om, z):
    A, B, C, D = M[:2, :2], M[:2, 2:], M[2:, :2], M[2:, 2:]
    W = C @ Om + D
    return -np.conj((A @ Om + B) @ np.linalg.inv(W)), -np.conj(np.linalg.inv(W).T @ z)


def cons(p, gu, gd, k):
    Ou, Od, z = homes(p)
    Ou2, _ = img(G[gu], Ou, np.zeros(2, complex))
    Od2, z2 = img(G[gd], Od, z)
    v = np.array([*(Ou - Ou2)[np.triu_indices(2)], *(Od - Od2)[np.triu_indices(2)], z[1] - z2[1] - k / 3, z2[0]])
    return np.concatenate([v.real, v.imag])


def obs(p):
    Ou, Od, z = homes(p)
    if min(np.linalg.eigvalsh(Ou.imag).min(), np.linalg.eigvalsh(Od.imag).min()) < 1e-4 or abs(z[1].imag) / Od.imag[1, 1] > 60:
        return None
    try:
        Uu, su, _ = np.linalg.svd(theta_c(Ou, np.zeros(2, complex)))
        Ud, sd, _ = np.linalg.svd(theta_c(Od, z))
    except Exception:
        return None
    if not (np.isfinite(su).all() and np.isfinite(sd).all()) or su[2] == 0 or sd[2] == 0:
        return None
    V = (Uu.conj().T @ Ud)[::-1, ::-1]
    return dict(mc_mt=su[1] / su[0], mu_mc=su[2] / su[1], ms_mb=sd[1] / sd[0], md_ms=sd[2] / sd[1],
                Vus=abs(V[0, 1]), Vcb=abs(V[1, 2]), Vub=abs(V[0, 2]),
                J=float(np.imag(V[0, 0] * V[1, 1] * np.conj(V[0, 1]) * np.conj(V[1, 0]))))


def chi2(p):
    o = obs(p)
    if o is None:
        return 1e8
    c = float(sum((np.log(max(o[q], 1e-300) / v) / e) ** 2 for q, (v, e) in DATA.items()))
    return c if np.isfinite(c) else 1e8


if __name__ == '__main__':
    gu, gd, k, n, seed = sys.argv[1].replace('_', ' '), sys.argv[2].replace('_', ' '), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    rng = np.random.default_rng(seed)
    best = None; nfeas = 0
    for _ in range(n):
        th = rng.uniform(0.05, np.pi - 0.05)
        eu0 = rng.normal(size=2) * 10 ** rng.uniform(-3, -1)
        if gu == 'SS' and rng.uniform() < 0.5:          # seed at the exact S-arc up solution (upS.py)
            sg = rng.choice([-1, 1]); th = np.angle(0.67622 * sg + 0.73669j)
            eu0 = np.array([-0.003383 * sg, 0.003105]) * rng.choice([-1, 1])
        p0 = np.array([np.cos(th), np.sin(th), *eu0,
                       *(rng.normal(size=2) * 10 ** rng.uniform(-3, -0.5)), rng.uniform(-1, 1), 10 ** rng.uniform(-2, 0.7),
                       rng.uniform(-.5, .5), rng.normal(0, .3)])
        pr = least_squares(lambda p: cons(p, gu, gd, k), p0, xtol=1e-15, ftol=1e-15, gtol=1e-15)
        if np.abs(cons(pr.x, gu, gd, k)).max() > 1e-9:
            continue
        nfeas += 1
        x = pr.x
        for _r in range(3):
            try:
                m = minimize(chi2, x, method='SLSQP', constraints=[{'type': 'eq', 'fun': lambda p: cons(p, gu, gd, k)}],
                             options=dict(maxiter=500, ftol=1e-13))
                if np.abs(cons(m.x, gu, gd, k)).max() < 1e-8 and chi2(m.x) <= chi2(x):
                    x = m.x
            except Exception:
                break
        c = chi2(x)
        if best is None or c < best[0]:
            best = (c, x.tolist())
    o = obs(np.array(best[1])) if best else None
    out = dict(gu=gu, gd=gd, k=k, starts=n, feasible=nfeas, chi2=best and best[0], x=best and best[1],
               fix=float(np.abs(cons(np.array(best[1]), gu, gd, k)).max()) if best else None, obs=o)
    json.dump(out, open(f'jointS_{sys.argv[1]}_{sys.argv[2]}_{k}.json', 'w'), indent=1)
    print(json.dumps({q: out[q] for q in ('gu', 'gd', 'k', 'feasible', 'chi2', 'fix')}), 'J=', o and o['J'], flush=True)
