"""Pass 12051 driver: impose eps_d = C_u e^eta exp(-pi (y + Im tau_d)) on the 12045 geometric-row down system.
Params: ln Im tau_d, sign*, Im z_d, ln lambda, Re w, Im w, eta (C_u nuisance, sigma 5.3%). Residuals: 6 down targets
weighted by errors (comparator or precise) + eta/0.053. Overdetermined by one relative to 12045.
Run: py -3 instlaw.py <comparator|precise> <starts> <seed>
"""
import json
import os
import sys

import numpy as np
from scipy.optimize import least_squares

import barrfit as B

HERE = os.path.dirname(os.path.abspath(__file__))
Y, EU = B.Y_UP, B.EU
CU = EU * np.exp(2 * np.pi * Y)
ERRS = {'comparator': dict(ms_mb=.08, md_ms=.10, Vus=.003, Vcb=.025, Vub=.05, J=.04),
        'precise': dict(ms_mb=.01, md_ms=.04, Vus=.003, Vcb=.025, Vub=.05, J=.04)}


def full(p, sgn):
    lyd, zi, lam, rw, iw, eta = p
    ed = sgn * CU * np.exp(eta) * np.exp(-np.pi * (Y + np.exp(lyd)))
    return np.array([lyd, ed, zi, lam, rw, iw])


def res(p, sgn, err):
    r = B.resid(full(p, sgn), 'shared')               # ln-ratio residuals (and relative J)
    w = np.array([err[k] for k in ('ms_mb', 'md_ms', 'Vus', 'Vcb', 'Vub', 'J')])
    return np.r_[r / w, p[5] / 0.053]


if __name__ == '__main__':
    mode, n, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    err = ERRS[mode]
    rng = np.random.default_rng(seed)
    A = [-1.8444766914898252, 0.028382479377949063, 5.083585000284045, -0.0775199696196673, -0.3673566495323771]
    out = []
    for i in range(n):
        if i < n // 3:
            p0 = np.r_[np.array(A) + rng.normal(0, 0.05, 5) * (i > 0), 0.0]
            sg = 1
        else:
            p0 = np.array([np.log(10 ** rng.uniform(np.log10(.03), np.log10(3))), rng.uniform(-2, 2), np.log(10 ** rng.uniform(-.5, 3)),
                           rng.uniform(-.5, .5), rng.uniform(-10, 10), 0.0])
            sg = rng.choice([-1, 1])
        r = least_squares(res, p0, args=(sg, err), xtol=1e-14, ftol=1e-14, gtol=1e-14, max_nfev=3000)
        out.append((float(np.sum(r.fun ** 2)), sg, r.x.tolist(), r.fun.tolist()))
    out.sort(key=lambda t: t[0])
    json.dump(dict(mode=mode, CU=CU, best=out[:10]), open(os.path.join(HERE, f'instlaw_{mode}_{seed}.json'), 'w'), indent=1)
    for c, sg, x, f in out[:3]:
        print(mode, 'chi2 = %.3f' % c, 'sign', sg, 'x', np.round(x, 4).tolist(), 'pulls', np.round(f, 2).tolist(), flush=True)
