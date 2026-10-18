"""Pass 12046 driver: follow each 12045 branch along Re w by continuation.

With Re w as the curve parameter, the remaining 5 parameters solve the 5 CP-even down targets exactly; J(Re w) and
the lepton ratios are recorded along the curve. Run: py -3 curve.py <A|B|C> [step]
"""
import json
import os
import sys

import numpy as np
from scipy.optimize import least_squares

import torsion as T

SOLS = {'A': [-1.8444766914898252, 0.05894435138670266, 0.028382479377949063, 5.083585000284045, -0.0775199696196673, -0.3673566495323771],
        'B': [1.139142, -1.15415, -0.238268, 5.502257, 0.403614, -0.99549],
        'C': [0.995395, 0.44687, 1.105663, 5.106863, -0.003056, -6.817541]}


def solve(p0, r):
    spec = ('rew', r)
    q = least_squares(T.res5, p0, args=(spec,), xtol=1e-15, ftol=1e-15, gtol=1e-15)
    return q.x, float(np.abs(q.fun).max())


def record(p, r):
    x = T.full_x(p, ('rew', r))
    J = T.B.obs(T.B.down_real(*x[:3]), T.B.brow(x, 'shared'))['J']
    lp = T.leptons(x)
    return dict(rew=float(r), x=x.tolist(), J=float(J), leptons=[float(lp[0]), float(lp[1])])


if __name__ == '__main__':
    name = sys.argv[1]
    h = float(sys.argv[2]) if len(sys.argv) > 2 else 0.004
    x0 = np.array(SOLS[name])
    r0 = x0[4]
    p0 = np.r_[x0[:4], x0[5]]
    p0, e = solve(p0, r0)
    pts = [record(p0, r0)]
    for direction in (+1, -1):
        p, r = p0.copy(), r0
        while abs(r - r0) < 1.0:
            rn = r + direction * h
            pn, e = solve(p, rn)
            if e > 1e-9 or np.abs(pn - p).max() > 0.5:   # lost the branch: halve the step once, else stop
                pn, e = solve(p, r + direction * h / 4)
                if e > 1e-9 or np.abs(pn - p).max() > 0.5:
                    print(name, 'branch lost at Re w =', round(r, 4), flush=True)
                    break
                rn = r + direction * h / 4
            p, r = pn, rn
            pts.append(record(p, r))
    pts.sort(key=lambda d: d['rew'])
    json.dump(dict(branch=name, points=pts), open(os.path.join(T.HERE, f'curve_{name}.json'), 'w'))
    for target in (1 / 6, 1 / 3, -1 / 6, -1 / 3, 0.25, -0.25, 0.2, -0.2, 0.1, -0.1, 0.5, -0.5, 0.0):
        for d in pts:
            pass
        near = [d for d in pts if abs(((d['rew'] - target + 0.5) % 1) - 0.5) < 1e-9 + h / 2]
        if near:
            d = min(near, key=lambda d: abs(((d['rew'] - target + 0.5) % 1) - 0.5))
            print(name, 'Re w~%.4f (target %+.4f): J=%+.4e leptons=(%.4f, %.6f)' % (d['rew'], target, d['J'], *d['leptons']), flush=True)
    print(name, 'covered Re w in [%.4f, %.4f], %d points' % (pts[0]['rew'], pts[-1]['rew'], len(pts)), flush=True)
