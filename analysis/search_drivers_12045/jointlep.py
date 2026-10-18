"""Pass 12045 driver: geometric Barr row (shared 5bar torus) + 12007 common matching for charged leptons.

Two outputs per start:
  * a quark-only exact solve (6 equations, 6 unknowns) -> its parameter-free lepton prediction;
  * a joint fit of 6 quark + 2 lepton residuals (8 equations, 6 unknowns) -> best chi^2.
Run: py -3 jointlep.py <starts> <seed>
"""
import json
import os
import sys

import numpy as np
from scipy.optimize import least_squares

import barrfit as B
from w33_pass11942_hypercharge_wilson_leptons import LEPTONS, normalised

HERE = os.path.dirname(os.path.abspath(__file__))


def leptons(x, mode='shared'):
    Od = np.array([[B.TAU, 1j * x[1]], [1j * x[1], 1j * np.exp(x[0])]])
    d = B.PH.conj()[:, None] * normalised(Od, (0, 1j * x[2]))
    e = B.PH.conj()[:, None] * normalised(Od, (0, 6j * x[2]))
    e = e.real / np.linalg.norm(d)
    b = B.brow(x, mode)
    K = np.eye(3) - np.outer(b.conj(), b) / (1 + np.vdot(b, b).real)
    ev, O = np.linalg.eigh(K)
    A = (O * np.sqrt(np.clip(ev, 0, None))) @ O.conj().T
    se = np.linalg.svd(A.T @ e.T, compute_uv=False)
    return se[1] / se[0], se[2] / se[1]


def lres(x):
    try:
        a, b = leptons(x)
        r = np.array([np.log(a / LEPTONS['mmu_mtau']), np.log(b / LEPTONS['me_mmu'])])
        return r if np.all(np.isfinite(r)) else np.full(2, 50.)
    except Exception:
        return np.full(2, 50.)


def jres(x):
    return np.r_[B.resid(x, 'shared'), lres(x)]


if __name__ == '__main__':
    n, seed = int(sys.argv[1]), int(sys.argv[2])
    rng = np.random.default_rng(seed)
    exact, joint = [], []
    for i in range(n):
        x0 = B.start(rng, 'shared')
        r = least_squares(B.resid, x0, args=('shared',), xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=3000)
        if np.sum(r.fun ** 2) < 1e-18:
            a, b = leptons(r.x)
            exact.append(dict(x=r.x.tolist(), mmu_mtau=float(a), me_mmu=float(b)))
            print('exact', np.round(r.x, 5).tolist(), 'leptons %.5f %.6f' % (a, b), flush=True)
        rj = least_squares(jres, x0, xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=3000)
        joint.append((float(np.sum(rj.fun ** 2)), rj.x.tolist()))
    joint.sort()
    json.dump(dict(seed=seed, starts=n, exact=exact, joint_best=joint[:10]), open(os.path.join(HERE, f'jointlep_{seed}.json'), 'w'), indent=1)
    print('joint best', joint[0][0], 'n_exact', len(exact), flush=True)
