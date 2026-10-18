import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ANA = _os.path.dirname(_HERE)
"""Pass 12004: down sector alone on the CP locus -- (i) tau frozen at the exact up solution, (ii) own CP-real tau'."""
import json
import sys

import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, _ANA)
import w33_pass11942_hypercharge_wilson_leptons as P42  # noqa: E402

DD = dict(ms_mb=(0.053 / 2.86, .08), md_ms=(2.67e-3 / 0.053, .10), Vus=(0.2250, .003), Vcb=(0.0411, .025), Vub=(0.00382, .05))
Y_UP, E_UP = 0.8745, 0.00552


def up_left(sign):
    tau = 1 + 1j * Y_UP
    e = 1j * E_UP * sign
    return np.linalg.svd(P42.theta(np.array([[tau, e], [e, tau]])))[0]


def obs(p, mode, rtd, kz, Uu):
    if not np.all(np.isfinite(p)):
        return None
    if mode == 'free':                       # positive control: tau frozen at the up solution, down parameters complex
        ydr, yd, edr, idd, zr, zi = p
        Omd = np.array([[1 + 1j * Y_UP, edr + 1j * idd], [edr + 1j * idd, ydr + 1j * yd]])
        zd = zr + 1j * zi
        if yd < 0.004 or np.linalg.eigvalsh(Omd.imag).min() < 0.002 or abs(zi) / yd > 28:
            return None
        Yd = P42.normalised(Omd, (0, zd))
        if not np.isfinite(Yd).all():
            return None
        try:
            Ud, sd, _ = np.linalg.svd(Yd)
        except np.linalg.LinAlgError:
            return None
        V = (Uu.conj().T @ Ud)[::-1, ::-1]
        return dict(ms_mb=sd[1] / sd[0], md_ms=sd[2] / sd[1], Vus=abs(V[0, 1]), Vcb=abs(V[1, 2]), Vub=abs(V[0, 2]))
    if mode == 'frozen':
        yd, idd, zi = p
        taup = 1 + 1j * Y_UP
    else:
        yd, idd, zi, rp, yp = p[0], p[1], p[2], mode, p[3]
        taup = int(rp) + 1j * yp
    Omd = np.array([[taup, 1j * idd], [1j * idd, rtd + 1j * yd]])
    zd = kz / 6 + 1j * zi
    if yd < 0.004 or np.linalg.eigvalsh(Omd.imag).min() < 0.002 or abs(zi) / yd > 28 or Omd.imag[0, 0] < 0.05:
        return None
    Yd = P42.normalised(Omd, (0, zd))
    if not np.isfinite(Yd).all():
        return None
    try:
        Ud, sd, _ = np.linalg.svd(Yd)
    except np.linalg.LinAlgError:
        return None
    V = (Uu.conj().T @ Ud)[::-1, ::-1]
    return dict(ms_mb=sd[1] / sd[0], md_ms=sd[2] / sd[1], Vus=abs(V[0, 1]), Vcb=abs(V[1, 2]), Vub=abs(V[0, 2]))


def resid(p, mode, rtd, kz, Uu):
    o = obs(p, mode, rtd, kz, Uu)
    if o is None:
        return np.full(len(DD), 50.0)
    r = np.array([np.log(max(o[k], 1e-30) / v) / e for k, (v, e) in DD.items()])
    return r if np.all(np.isfinite(r)) else np.full(len(DD), 50.0)


if __name__ == '__main__':
    mode, nstart, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])     # mode: 'frozen' or '0'/'1' (Re tau' of own CP line)
    rng = np.random.default_rng(seed)
    results = []
    for sign in (1, -1):
        Uu = up_left(sign)
        for rtd in ((0,) if mode == 'free' else (0, 1)):
            for kz in ((0,) if mode == 'free' else range(6)):
                best = None
                for _ in range(nstart):
                    if mode == 'free':
                        p0 = [rng.uniform(-1, 1), 10 ** rng.uniform(-2.3, 0.2), 10 ** rng.uniform(-3.5, -0.7) * rng.choice([-1, 1]),
                              10 ** rng.uniform(-3.5, -0.7) * rng.choice([-1, 1]), rng.uniform(-0.5, 0.5), rng.normal(0, 0.3)]
                    else:
                        p0 = [10 ** rng.uniform(-2.3, 0.2), 10 ** rng.uniform(-3.5, -0.7) * rng.choice([-1, 1]), rng.normal(0, 0.3)]
                    if mode not in ('frozen', 'free'):
                        p0 += [rng.uniform(0.15, 2.5)]
                    r = least_squares(resid, p0, args=(mode, rtd, kz, Uu), method='trf', max_nfev=600)
                    if best is None or r.cost < best.cost:
                        best = r
                o = obs(best.x, mode, rtd, kz, Uu)
                results.append(dict(sign=sign, rtd=rtd, kz=kz, chi2=float(2 * best.cost), x=best.x.tolist(),
                                    obs={k: float(v) for k, v in o.items()} if o else None))
                print(mode, sign, rtd, kz, round(2 * best.cost, 3), {k: round(v, 5) for k, v in (o or {}).items()}, flush=True)
    json.dump(results, open(_os.path.join(_HERE, f'downonly_{mode}_{seed}.json'), 'w'), indent=1)
