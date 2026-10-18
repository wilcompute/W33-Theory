import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ANA = _os.path.dirname(_HERE)
"""Pass 12004 scratch: fit the 7 quark magnitudes with all moduli on the theta-group generalized-CP fixed locus."""
import json
import sys

import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, _ANA)
import w33_pass11942_hypercharge_wilson_leptons as P42  # noqa: E402

DATA = dict(mc_mt=(0.620 / 168.26, .05), mu_mc=(1.23e-3 / 0.620, .20), ms_mb=(0.053 / 2.86, .08),
            md_ms=(2.67e-3 / 0.053, .10), Vus=(0.2250, .003), Vcb=(0.0411, .025), Vub=(0.00382, .05))


def model(p, rt, rtd, kz):
    y, iu, yd, idd, zi = p
    tau = rt + 1j * y
    td = rtd + 1j * yd
    eu, ed = 1j * iu, 1j * idd
    zd = kz / 6 + 1j * zi
    Omu = np.array([[tau, eu], [eu, tau]])
    Omd = np.array([[tau, ed], [ed, td]])
    return Omu, Omd, zd


def obs(p, rt, rtd, kz):
    Omu, Omd, zd = model(p, rt, rtd, kz)
    if Omu.imag[0, 0] < 0.05 or Omd.imag[1, 1] < 0.004 or min(np.linalg.eigvalsh(Omd.imag).min(), np.linalg.eigvalsh(Omu.imag).min()) < 0.002:
        return None
    if abs(zd.imag) / Omd.imag[1, 1] > 28:
        return None
    Yu = P42.theta(Omu)
    Yd = P42.normalised(Omd, (0, zd))
    if not (np.isfinite(Yu).all() and np.isfinite(Yd).all()):
        return None
    try:
        Uu, su, _ = np.linalg.svd(Yu)
        Ud, sd, _ = np.linalg.svd(Yd)
    except np.linalg.LinAlgError:
        return None
    V = (Uu.conj().T @ Ud)[::-1, ::-1]
    J = np.imag(V[0, 0] * V[1, 1] * np.conj(V[0, 1]) * np.conj(V[1, 0]))
    return dict(mc_mt=su[1] / su[0], mu_mc=su[2] / su[1], ms_mb=sd[1] / sd[0], md_ms=sd[2] / sd[1],
                Vus=abs(V[0, 1]), Vcb=abs(V[1, 2]), Vub=abs(V[0, 2]), J=J)


def resid(p, rt, rtd, kz):
    o = obs(p, rt, rtd, kz)
    if o is None:
        return np.full(len(DATA), 50.0)
    return np.array([np.log(max(o[k], 1e-30) / v) / e for k, (v, e) in DATA.items()])


def run(rtd, kz, starts, seed):
    rng = np.random.default_rng(seed)
    best = None
    for _ in range(starts):
        p0 = [rng.uniform(0.3, 1.6), 10 ** rng.uniform(-3.5, -1.5) * rng.choice([-1, 1]), 10 ** rng.uniform(-2, -0.3),
              10 ** rng.uniform(-3, -1) * rng.choice([-1, 1]), rng.normal(0, 0.05)]
        r = least_squares(resid, p0, args=(1, rtd, kz), method='trf', max_nfev=600)
        if best is None or r.cost < best.cost:
            best = r
    o = obs(best.x, 1, rtd, kz)
    return dict(rtd=rtd, kz=kz, chi2=float(2 * best.cost), x=best.x.tolist(),
                obs={k: float(v) for k, v in o.items()} if o else None)


if __name__ == '__main__':
    rtd, kz, starts, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    out = run(rtd, kz, starts, seed)
    json.dump(out, open(_os.path.join(_HERE, f'cpfit_{rtd}_{kz}_{seed}.json'), 'w'), indent=1)
    print(json.dumps({k: out[k] for k in ('rtd', 'kz', 'chi2')}), {k: round(v, 6) for k, v in (out['obs'] or {}).items()}, flush=True)
