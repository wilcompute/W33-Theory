"""Pass 12045 driver: exact (nonlinear) posterior on branch C. Unknowns: the 8 log quark targets. Residuals: their
priors (errors ERR) plus the two charged-lepton ratios of the branch-C solution (theory error TH). Each evaluation
follows branch C from the nominal targets by homotopy. Output: MAP shifts, Laplace errors, implied Weber invariant.
Run: py -3 mapC.py <TH> [precise]
"""
import json
import os
import sys

import numpy as np
from scipy.optimize import least_squares

import barrfit as B
import mcC as M
from jointlep import leptons
from w33_pass11942_hypercharge_wilson_leptons import DATA as D0, LEPTONS

HERE = os.path.dirname(os.path.abspath(__file__))
KEYS = list(D0)
PRECISE = dict(mc_mt=.02, mu_mc=.05, ms_mb=.01, md_ms=.04, Vus=.003, Vcb=.025, Vub=.05, J=.04)   # lattice-era precision
ERRV = np.array([(PRECISE if len(sys.argv) > 2 and sys.argv[2] == 'precise' else M.ERR)[k] for k in KEYS])
XC = np.load(os.path.join(HERE, 'solC.npy'))
CACHE = {}


def follow(dlog, steps=12):
    pu, xd = np.array([B.Y_UP, B.EU]), XC.copy()
    for s in np.linspace(1 / steps, 1, steps):
        ts = {k: D0[k] * np.exp(s * d) for k, d in zip(KEYS, dlog)}
        ru = least_squares(M.up_resid, pu, args=(ts,), xtol=1e-15, ftol=1e-15)
        M.set_up(*ru.x)
        B.DATA = ts
        rd = least_squares(B.resid, xd, args=('shared',), xtol=1e-15, ftol=1e-15, gtol=1e-15)
        if np.abs(ru.fun).max() > 1e-8 or np.abs(rd.fun).max() > 1e-8:
            return None
        pu, xd = ru.x, rd.x
    return xd


def res(dlog, th):
    x = follow(dlog)
    if x is None:
        return np.full(10, 1e3)
    a, b = leptons(x)
    return np.r_[dlog / ERRV, [np.log(a / LEPTONS['mmu_mtau']) / th, np.log(b / LEPTONS['me_mmu']) / th]]


if __name__ == '__main__':
    th = float(sys.argv[1])
    r = least_squares(res, np.zeros(8), args=(th,), diff_step=1e-4, xtol=1e-10, ftol=1e-10)
    J = r.jac
    cov = np.linalg.inv(J.T @ J)
    out = dict(theory_error=th, chi2=float(np.sum(r.fun ** 2)), lepton_pulls=r.fun[8:].tolist(),
               map_log_shift={k: float(v) for k, v in zip(KEYS, r.x)}, laplace_sigma={k: float(np.sqrt(c)) for k, c in zip(KEYS, np.diag(cov))},
               weber_log_shift=float(r.x[1] - r.x[0]),
               weber_sigma=float(np.sqrt(cov[1, 1] + cov[0, 0] - 2 * cov[0, 1])))
    json.dump(out, open(os.path.join(HERE, f'mapC_{th}{"_precise" if len(sys.argv) > 2 else ""}.json'), 'w'), indent=1)
    print(json.dumps(out, indent=1), flush=True)
