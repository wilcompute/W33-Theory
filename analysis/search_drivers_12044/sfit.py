import os as _os
import sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ANA = _os.path.dirname(_HERE)
_sys.path.insert(0, _HERE)
"""S-type generalized CP: fit the 7 quark magnitudes with both homes on the fixed set of CP o g (penalty method)."""
import json
import sys

import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, _ANA)
import w33_pass11942_hypercharge_wilson_leptons as P42  # noqa: E402
from w33_pass12004_cp_real_bare_theta_no_fit import theta_c  # noqa: E402

DATA = dict(mc_mt=(0.620 / 168.26, .05), mu_mc=(1.23e-3 / 0.620, .20), ms_mb=(0.053 / 2.86, .08),
            md_ms=(2.67e-3 / 0.053, .10), Vus=(0.2250, .003), Vcb=(0.0411, .025), Vub=(0.00382, .05))
Z2 = np.zeros((2, 2))
I2 = np.eye(2)


def sp(a1, b1, c1, d1, a2, b2, c2, d2):
    return np.block([[np.diag([a1, a2]), np.diag([b1, b2])], [np.diag([c1, c2]), np.diag([d1, d2])]]).astype(float)


G = {'SS': sp(0, -1, 1, 0, 0, -1, 1, 0), 'S T0': sp(0, -1, 1, 0, 1, 0, 0, 1), 'S T2': sp(0, -1, 1, 0, 1, 2, 0, 1)}


def iota(M, Om, z, k):
    A, B, C, D = M[:2, :2], M[:2, 2:], M[2:, :2], M[2:, 2:]
    W = C @ Om + D
    Om2 = (A @ Om + B) @ np.linalg.inv(W)
    z2 = np.linalg.inv(W).T @ z
    return -np.conj(Om2), -np.conj(z2) + np.array([0, k / 3])


def unpack(p):
    tau = p[0] + 1j * p[1]
    eu, ed = p[2] + 1j * p[3], p[4] + 1j * p[5]
    td = p[6] + 1j * p[7]
    zd = p[8] + 1j * p[9]
    return np.array([[tau, eu], [eu, tau]]), np.array([[tau, ed], [ed, td]]), np.array([0, zd])


def obs(p):
    Omu, Omd, z = unpack(p)
    if min(np.linalg.eigvalsh(Omu.imag).min(), np.linalg.eigvalsh(Omd.imag).min()) < 0.003:
        return None
    if abs(z[1].imag) / Omd.imag[1, 1] > 60:
        return None
    try:
        Yu = theta_c(Omu, np.array([0, 0j]))
        Yd = theta_c(Omd, z)
        Uu, su, _ = np.linalg.svd(Yu)
        Ud, sd, _ = np.linalg.svd(Yd)
    except Exception:
        return None
    if not (np.isfinite(su).all() and np.isfinite(sd).all()) or su[1] == 0 or sd[1] == 0:
        return None
    V = (Uu.conj().T @ Ud)[::-1, ::-1]
    J = np.imag(V[0, 0] * V[1, 1] * np.conj(V[0, 1]) * np.conj(V[1, 0]))
    return dict(mc_mt=su[1] / su[0], mu_mc=su[2] / su[1], ms_mb=sd[1] / sd[0], md_ms=sd[2] / sd[1],
                Vus=abs(V[0, 1]), Vcb=abs(V[1, 2]), Vub=abs(V[0, 2]), J=J)


def fixres(p, gd, k):
    Omu, Omd, z = unpack(p)
    Ou, _ = iota(G['SS'], Omu, np.zeros(2, complex), 0)
    Od, zd2 = iota(G[gd], Omd, z, k)
    r = np.concatenate([(Omu - Ou)[np.triu_indices(2)], (Omd - Od)[np.triu_indices(2)], [z[1] - zd2[1]]])
    return np.concatenate([r.real, r.imag])


def resid(p, gd, k, lam):
    o = obs(p)
    if o is None:
        return np.full(len(DATA) + 14, 50.0)
    r = [np.log(max(o[q], 1e-300) / v) / e for q, (v, e) in DATA.items()]
    out = np.concatenate([r, lam * fixres(p, gd, k)])
    return out if np.all(np.isfinite(out)) else np.full(len(DATA) + 14, 50.0)


if __name__ == '__main__':
    gd, k, nstart, seed = sys.argv[1].replace('_', ' '), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    rng = np.random.default_rng(seed)
    th = 0.73624 * np.pi
    best = None
    for _ in range(nstart):
        tau = np.exp(1j * th * (1 + 0.01 * rng.normal()))
        eu = 1j * 0.0035 * rng.choice([-1, 1]) * (1 + 0.1 * rng.normal()) * tau
        td = rng.uniform(-1, 1) + 1j * 10 ** rng.uniform(-2, 0.5)
        ed = (rng.normal() + 1j * rng.normal()) * 10 ** rng.uniform(-3, -0.7)
        zd = rng.uniform(-0.5, 0.5) + 1j * rng.normal(0, 0.1)
        p0 = np.array([tau.real, tau.imag, eu.real, eu.imag, ed.real, ed.imag, td.real, td.imag, zd.real, zd.imag])
        for lam in (10.0, 1e3, 1e5):
            r = least_squares(resid, p0, args=(gd, k, lam), method='trf', max_nfev=400)
            p0 = r.x
        o = obs(r.x)
        chi = float(sum((np.log(o[q] / v) / e) ** 2 for q, (v, e) in DATA.items())) if o else 1e9
        fr = float(np.abs(fixres(r.x, gd, k)).max())
        if fr < 1e-6 and (best is None or chi < best[0]):
            best = (chi, r.x.tolist(), fr, o)
    out = dict(gd=gd, k=k, chi2=best[0] if best else None, x=best[1] if best else None, fix_residual=best[2] if best else None,
               obs={q: float(v) for q, v in best[3].items()} if best and best[3] else None)
    json.dump(out, open(_os.path.join(_HERE, f'sfit_{sys.argv[1]}_{k}_{seed}.json'), 'w'), indent=1)
    print(json.dumps({q: out[q] for q in ('gd', 'k', 'chi2', 'fix_residual')}), {q: round(v, 6) for q, v in (out['obs'] or {}).items()}, flush=True)
