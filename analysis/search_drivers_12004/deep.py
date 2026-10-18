import os as _os
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ANA = _os.path.dirname(_HERE)
"""Pass 12004: deep-cusp evaluator (centred summation window) and the bare CP-real down search toward Im tau_d -> 0."""
import json
import sys

import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, _ANA)
sys.path.insert(0, _HERE)
import w33_pass11942_hypercharge_wilson_leptons as P42  # noqa: E402
import downonly as D  # noqa: E402


def theta_c(Om, z, n1max=10):
    """Level-3 genus-2 theta with Wilson line, summing n2 in a window centred on the Gaussian peak."""
    Y = np.zeros((3, 3), complex)
    t1, e, t2 = Om[0, 0], Om[0, 1], Om[1, 1]
    y2 = t2.imag
    W = int(np.ceil(7.0 / np.sqrt(3 * np.pi * max(y2, 1e-6)))) + 4
    lmax = None
    terms = []
    for a in range(3):
        for b in range(3):
            acc = []
            for n1 in range(-n1max, n1max + 1):
                v1 = n1 + a / 3
                c = -(z[1].imag + e.imag * v1) / y2
                n2 = np.arange(int(np.floor(c)) - W, int(np.ceil(c)) + W + 1)
                v2 = n2 + b / 3
                ex = 3j * np.pi * (t1 * v1 * v1 + 2 * e * v1 * v2 + t2 * v2 * v2) + 6j * np.pi * (v1 * z[0] + v2 * z[1])
                acc.append(ex)
            ex = np.concatenate(acc)
            m = ex.real.max()
            terms.append((a, b, m, np.exp(ex - m).sum()))
    gmax = max(t[2] for t in terms)
    for a, b, m, s in terms:
        Y[a, b] = s * np.exp(m - gmax)
    return Y          # common positive rescaling is irrelevant for ratios and singular vectors


def obs_deep(p, rtd, kz, Uu):
    yd, idd, zi = p
    if not np.all(np.isfinite(p)) or yd <= 1e-5:
        return None
    Omd = np.array([[1 + 1j * D.Y_UP, 1j * idd], [1j * idd, rtd + 1j * yd]])
    if np.linalg.eigvalsh(Omd.imag).min() <= 0:
        return None
    Yd = theta_c(Omd, (0, kz / 6 + 1j * zi))
    if not np.isfinite(Yd).all():
        return None
    try:
        Ud, sd, _ = np.linalg.svd(Yd)
    except np.linalg.LinAlgError:
        return None
    if sd[0] == 0:
        return None
    V = (Uu.conj().T @ Ud)[::-1, ::-1]
    return dict(ms_mb=sd[1] / sd[0], md_ms=sd[2] / sd[1] if sd[1] > 0 else 0.0, Vus=abs(V[0, 1]), Vcb=abs(V[1, 2]), Vub=abs(V[0, 2]))


def resid(p, rtd, kz, Uu):
    o = obs_deep(p, rtd, kz, Uu)
    if o is None:
        return np.full(len(D.DD), 50.0)
    r = np.array([np.log(max(o[k], 1e-300) / v) / e for k, (v, e) in D.DD.items()])
    return r if np.all(np.isfinite(r)) else np.full(len(D.DD), 50.0)


if __name__ == '__main__':
    if sys.argv[1] == 'validate':
        rng = np.random.default_rng(0)
        worst = 0
        for _ in range(30):
            yd = 10 ** rng.uniform(-1.6, 0)
            Om = np.array([[1 + 1j * 0.8745, 1j * rng.uniform(-0.3, 0.3) * np.sqrt(0.8745 * yd)], [0, rng.integers(0, 2) + 1j * yd]])
            Om[1, 0] = Om[0, 1]
            z = (0, rng.integers(0, 6) / 6 + 1j * rng.uniform(-5, 5) * yd)
            A = P42.theta(Om, z)
            B = theta_c(Om, z)
            sa, sb = np.linalg.svd(A, compute_uv=False), np.linalg.svd(B, compute_uv=False)
            worst = max(worst, np.abs(sa / sa[0] - sb / sb[0]).max())
        print('max |ratio difference| vs N=40 reference over 30 points:', worst)
        sys.exit()
    rtd, kz, nstart, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    rng = np.random.default_rng(seed)
    res = []
    for sign in (1, -1):
        Uu = D.up_left(sign)
        best = None
        for _ in range(nstart):
            yd = 10 ** rng.uniform(-4.0, -1.3)
            p0 = [yd, rng.uniform(-0.9, 0.9) * np.sqrt(D.Y_UP * yd), rng.uniform(-60, 60) * yd]
            r = least_squares(resid, p0, args=(rtd, kz, Uu), method='trf', max_nfev=500, x_scale=[yd, np.sqrt(yd), yd])
            if best is None or r.cost < best.cost:
                best = r
        o = obs_deep(best.x, rtd, kz, Uu)
        res.append(dict(sign=sign, rtd=rtd, kz=kz, chi2=float(2 * best.cost), x=best.x.tolist(), obs=o))
        print(sign, rtd, kz, round(2 * best.cost, 3), [float('%.4g' % v) for v in best.x], {k: round(v, 5) for k, v in (o or {}).items()}, flush=True)
    json.dump(res, open(_os.path.join(_HERE, f'deep_{rtd}_{kz}_{seed}.json'), 'w'), indent=1, default=float)
