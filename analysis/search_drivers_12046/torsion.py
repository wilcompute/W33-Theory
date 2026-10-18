"""Pass 12046 driver: the geometric Barr row of Pass 12045 with its Wilson line pinned.

mode rew  r     : Re w = r fixed; params (ln Im tau_d, Im eps_d, Im z_d, ln lambda, Im w) solve the 5 CP-even down
                  targets (square); J and the lepton ratios are then predictions.
mode full a b N : w = (a + b tau_d)/N fixed; params (ln Im tau_d, Im eps_d, Im z_d, ln lambda) fit 5 targets (one dof).
Broad starts. Run: py -3 torsion.py rew <r> <starts> <seed>  |  py -3 torsion.py full <a> <b> <N> <starts> <seed>
"""
import json
import os
import sys

import numpy as np
from scipy.optimize import least_squares

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'search_drivers_12045'))
sys.path.insert(0, os.path.dirname(HERE))
import barrfit as B  # noqa: E402
from jointlep import leptons  # noqa: E402
from w33_pass11942_hypercharge_wilson_leptons import DATA  # noqa: E402

KEYS5 = ['ms_mb', 'md_ms', 'Vus', 'Vcb', 'Vub']


def full_x(p, spec):
    if spec[0] == 'rew':
        return np.array([p[0], p[1], p[2], p[3], spec[1], p[4]])
    a, b, N = spec[1:]
    return np.array([p[0], p[1], p[2], p[3], a / N, b * np.exp(p[0]) / N])


def res5(p, spec):
    x = full_x(p, spec)
    try:
        m = B.down_real(*x[:3])
        bb = B.brow(x, 'shared')
        if not np.all(np.isfinite(bb)) or np.linalg.norm(bb) > 1e4:
            return np.full(5, 50.)
        o = B.obs(m, bb)
        r = np.array([np.log(o[k] / DATA[k]) for k in KEYS5])
        return r if np.all(np.isfinite(r)) else np.full(5, 50.)
    except Exception:
        return np.full(5, 50.)


def start(rng, spec):
    p = [np.log(10 ** rng.uniform(np.log10(.03), np.log10(6))), rng.uniform(-1.5, 1.5), rng.uniform(-2, 2), np.log(10 ** rng.uniform(-.5, 3))]
    if spec[0] == 'rew':
        p.append(rng.uniform(-10, 10))
    return np.array(p)


if __name__ == '__main__':
    if sys.argv[1] == 'rew':
        spec = ('rew', float(eval(sys.argv[2])))
        n, seed = int(sys.argv[3]), int(sys.argv[4])
        tag = f"rew_{sys.argv[2].replace('/', 'o')}_{seed}"
    else:
        spec = ('full', int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
        n, seed = int(sys.argv[5]), int(sys.argv[6])
        tag = f'full_{spec[1]}_{spec[2]}_{spec[3]}_{seed}'
    rng = np.random.default_rng(seed)
    out = []
    for i in range(n):
        r = least_squares(res5, start(rng, spec), args=(spec,), xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=2000)
        c = float(np.sum(r.fun ** 2))
        if spec[0] == 'rew' and c > 1e-18:
            continue
        x = full_x(r.x, spec)
        Od = np.array([[B.TAU, 1j * x[1]], [1j * x[1], 1j * np.exp(x[0])]])
        if np.linalg.eigvalsh(Od.imag).min() <= 0:
            continue
        try:
            J = B.obs(B.down_real(*x[:3]), B.brow(x, 'shared'))['J']
            lp = leptons(x)
        except Exception:
            continue
        out.append(dict(chi2_5=c, x=x.tolist(), J=float(J), leptons=[float(lp[0]), float(lp[1])]))
        print('sol chi2=%.2e J=%.4e (data %.3e) lept=(%.4f, %.6f) key=%s' % (c, J, DATA['J'], lp[0], lp[1],
              [round(float(np.exp(x[0])), 4), round(abs(x[1]), 4), round(abs(x[2]), 4), round(float(np.exp(x[3])), 2), round(x[5], 4)]), flush=True)
    json.dump(dict(spec=list(spec), starts=n, seed=seed, sols=out), open(os.path.join(HERE, f'torsion_{tag}.json'), 'w'), indent=1)
    print('done', len(out), flush=True)
