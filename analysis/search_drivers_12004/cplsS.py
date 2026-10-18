import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ANA = _os.path.dirname(_HERE)
"""Pass 12004: many-start least squares on the CP locus, the decoupled-tau control and the CP-free positive control."""
import json
import sys

import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, _ANA)
import w33_pass11942_hypercharge_wilson_leptons as P42  # noqa: E402

DATA = dict(mc_mt=(0.620 / 168.26, .05), mu_mc=(1.23e-3 / 0.620, .20), ms_mb=(0.053 / 2.86, .08),
            md_ms=(2.67e-3 / 0.053, .10), Vus=(0.2250, .003), Vcb=(0.0411, .025), Vub=(0.00382, .05))


def build(p, mode, rtd, kz):
    if mode == 'cp':            # shared tau on Re tau = 1, everything CP-real
        y, iu, yd, idd, zi = p
        tau = 1 + 1j * y
        taup = tau
        eu, ed = 1j * iu, 1j * idd
        td = rtd + 1j * yd
        zd = kz / 6 + 1j * zi
    elif mode == 'cpdec':       # down coupling's 10-factor modulus tau' independent, own CP line Re tau' = rtp (in rtd tens digit)
        y, iu, yd, idd, zi, yp = p
        tau = 1 + 1j * y
        taup = (rtd // 10) + 1j * yp
        eu, ed = 1j * iu, 1j * idd
        td = (rtd % 10) + 1j * yd
        zd = kz / 6 + 1j * zi
    else:                       # free: CP restrictions removed (positive control)
        tr, y, eur, eui, tdr, yd, edr, edi, zr, zi = p
        tau = tr + 1j * y
        taup = tau
        eu, ed = eur + 1j * eui, edr + 1j * edi
        td = tdr + 1j * yd
        zd = zr + 1j * zi
    return np.array([[tau, eu], [eu, tau]]), np.array([[taup, ed], [ed, td]]), zd


def obs(p, mode, rtd, kz):
    Omu, Omd, zd = build(p, mode, rtd, kz)
    if min(np.linalg.eigvalsh(Omu.imag).min(), np.linalg.eigvalsh(Omd.imag).min()) < 0.002 or Omd.imag[1, 1] < 0.004:
        return None
    if abs(zd.imag) / Omd.imag[1, 1] > 28 or Omu.imag[0, 0] < 0.05:
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
    return dict(mc_mt=su[1] / su[0], mu_mc=su[2] / su[1], ms_mb=sd[1] / sd[0], md_ms=sd[2] / sd[1],
                Vus=abs(V[0, 1]), Vcb=abs(V[1, 2]), Vub=abs(V[0, 2]))


def resid(p, mode, rtd, kz):
    o = obs(p, mode, rtd, kz)
    if o is None:
        return np.full(len(DATA), 50.0)
    return np.array([np.log(max(o[k], 1e-30) / v) / e for k, (v, e) in DATA.items()])


def start(rng, mode):
    s = lambda lo, hi: 10 ** rng.uniform(lo, hi) * rng.choice([-1, 1])
    base = [0.8745 * (1 + 0.02 * rng.normal()), 0.00552 * rng.choice([-1, 1]) * (1 + 0.02 * rng.normal()),
            10 ** rng.uniform(-2.3, 0.2), s(-3.5, -0.7), rng.normal(0, 0.3)]
    if mode == 'cp':
        return base
    if mode == 'cpdec':
        return base + [rng.uniform(0.2, 2.0)]
    return [rng.uniform(-1, 1), rng.uniform(0.3, 1.6), s(-4, -2), s(-4, -2), rng.uniform(-0.5, 0.5),
            10 ** rng.uniform(-1.7, -0.5), s(-3, -1.5), s(-3, -1.5), rng.uniform(-0.5, 0.5), rng.normal(0, 0.05)]


if __name__ == '__main__':
    mode, rtd, kz, nstart, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    rng = np.random.default_rng(seed)
    best = None
    for _ in range(nstart):
        r = least_squares(resid, start(rng, mode), args=(mode, rtd, kz), method='trf', max_nfev=800)
        if best is None or r.cost < best.cost:
            best = r
    o = obs(best.x, mode, rtd, kz)
    out = dict(mode=mode, rtd=rtd, kz=kz, chi2=float(2 * best.cost), x=best.x.tolist(),
               obs={k: float(v) for k, v in o.items()} if o else None)
    json.dump(out, open(_os.path.join(_HERE, f'cplsS_{mode}_{rtd}_{kz}_{seed}.json'), 'w'), indent=1)
    print(json.dumps({k: out[k] for k in ('mode', 'rtd', 'kz', 'chi2')}), {k: round(v, 5) for k, v in (out['obs'] or {}).items()}, flush=True)
