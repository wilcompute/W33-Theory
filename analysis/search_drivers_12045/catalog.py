"""Pass 12045 driver: catalogue the isolated solutions of the square geometric-row system with BROAD starts
(Im tau_d log-uniform in [0.03, 6], eps_d in [-1.5, 1.5], Im z_d in [-2, 2], Re w in [-0.5, 0.5], Im w in [-10, 10]),
then record each exact solution with its symmetry-invariant key and its parameter-free lepton prediction.
Run: py -3 catalog.py <starts> <seed>
"""
import json
import os
import sys

import numpy as np
from scipy.optimize import least_squares

import barrfit as B
from jointlep import leptons

HERE = os.path.dirname(os.path.abspath(__file__))


def broad(rng):
    return np.array([np.log(10 ** rng.uniform(np.log10(.03), np.log10(6))), rng.uniform(-1.5, 1.5), rng.uniform(-2, 2),
                     np.log(10 ** rng.uniform(-0.5, 3)), rng.uniform(-.5, .5), rng.uniform(-10, 10)])


if __name__ == '__main__':
    n, seed = int(sys.argv[1]), int(sys.argv[2])
    rng = np.random.default_rng(seed)
    out = []
    for i in range(n):
        r = least_squares(B.resid, broad(rng), args=('shared',), xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=2000)
        if np.sum(r.fun ** 2) < 1e-18:
            x = r.x
            Od = np.array([[B.TAU, 1j * x[1]], [1j * x[1], 1j * np.exp(x[0])]])
            if np.linalg.eigvalsh(Od.imag).min() <= 0:
                continue
            try:
                a, b = leptons(x)
            except np.linalg.LinAlgError:
                continue
            key = [round(float(np.exp(x[0])), 5), round(abs(float(x[1])), 5), round(abs(float(x[2])), 5), round(float(np.exp(x[3])), 3),
                   round(float(a), 6), round(float(b), 7)]
            out.append(dict(x=x.tolist(), key=key))
            print('exact', key, flush=True)
    json.dump(dict(seed=seed, starts=n, exact=out), open(os.path.join(HERE, f'catalog_{seed}.json'), 'w'), indent=1)
    print('done', len(out), flush=True)
