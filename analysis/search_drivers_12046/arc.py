"""Pass 12046 driver: pseudo-arclength continuation of the 1-dim solution curve of the 5 CP-even down targets
(unknowns: ln Im tau_d, Im eps_d, Im z_d, ln lambda, Re w, Im w) through each 12045 branch. Passes folds in Re w.
Records J and lepton ratios along the curve. Run: py -3 arc.py <A|B|C> <h> <maxsteps>
"""
import json
import os
import sys

import numpy as np
from scipy.optimize import least_squares

import torsion as T
from curve import SOLS

KEYS5 = T.KEYS5


def F(x):
    try:
        m = T.B.down_real(*x[:3])
        b = T.B.brow(x, 'shared')
        if not np.all(np.isfinite(b)) or np.linalg.norm(b) > 1e5:
            return np.full(5, 50.)
        o = T.B.obs(m, b)
        r = np.array([np.log(o[k] / T.DATA[k]) for k in KEYS5])
        return r if np.all(np.isfinite(r)) else np.full(5, 50.)
    except Exception:
        return np.full(5, 50.)


def jac(x, h=1e-7):
    return np.array([(F(x + h * e) - F(x - h * e)) / (2 * h) for e in np.eye(6)]).T


def tangent(x, prev=None):
    _, s, vt = np.linalg.svd(jac(x))
    t = vt[-1]
    if prev is not None and t @ prev < 0:
        t = -t
    return t, s


def info(x):
    m = T.B.down_real(*x[:3])
    J = T.B.obs(m, T.B.brow(x, 'shared'))['J']
    lp = T.leptons(x)
    Od = np.array([[T.B.TAU, 1j * x[1]], [1j * x[1], 1j * np.exp(x[0])]])
    return dict(x=x.tolist(), rew=float(x[4]), J=float(J), leptons=[float(lp[0]), float(lp[1])], minImOd=float(np.linalg.eigvalsh(Od.imag).min()))


def run(x0, h, nmax, direction):
    x = least_squares(F, x0, xtol=1e-15, ftol=1e-15, gtol=1e-15).x
    t, _ = tangent(x)
    t = direction * t
    pts = []
    hk = h
    for k in range(nmax):
        for _try in range(14):
            xp = x + hk * t
            r = least_squares(lambda y: np.r_[F(y), 50 * t @ (y - xp)], xp, xtol=1e-14, ftol=1e-14, gtol=1e-14)
            if np.abs(F(r.x)).max() < 1e-9 and np.linalg.norm(r.x - x) < 3 * hk:
                break
            hk /= 2
        else:
            print('stuck at step', k, 'Re w', round(x[4], 4), 'x', np.round(x, 4).tolist(), flush=True)
            break
        hk = min(4 * h, hk * 1.5)
        x = r.x
        t, s = tangent(x, t)
        d = info(x)
        if d['minImOd'] <= 1e-4:
            print('reached the boundary Im Omega_d -> 0 at Re w', round(x[4], 4), flush=True)
            break
        pts.append(d)
    return pts


if __name__ == '__main__':
    name, h, nmax = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
    x0 = np.array(SOLS[name])
    pts = run(x0, h, nmax, -1)[::-1] + [info(least_squares(F, x0, xtol=1e-15, ftol=1e-15, gtol=1e-15).x)] + run(x0, h, nmax, +1)
    json.dump(dict(branch=name, h=h, points=pts), open(os.path.join(T.HERE, f'arc_{name}.json'), 'w'))
    rw = np.array([p['rew'] for p in pts])
    Js = np.array([p['J'] for p in pts])
    print(name, 'points', len(pts), 'Re w range [%.4f, %.4f]' % (rw.min(), rw.max()), 'J range [%.3e, %.3e]' % (Js.min(), Js.max()), flush=True)
    # crossings of torsion / control values of Re w (mod 1)
    for target in (0, 1 / 2, 1 / 6, -1 / 6, 1 / 3, -1 / 3, 1 / 4, -1 / 4, 1 / 5, -1 / 5, 1 / 10, -1 / 10, 2 / 5, -2 / 5):
        g = ((rw - target + 0.5) % 1) - 0.5
        for i in range(len(g) - 1):
            if g[i] == 0 or (g[i] * g[i + 1] < 0 and abs(g[i] - g[i + 1]) < 0.5):
                f = g[i] / (g[i] - g[i + 1]) if g[i] != g[i + 1] else 0
                J = Js[i] + f * (Js[i + 1] - Js[i])
                l = np.array(pts[i]['leptons']) + f * (np.array(pts[i + 1]['leptons']) - np.array(pts[i]['leptons']))
                print(name, 'Re w = %+.4f crossing: J = %+.4e (J/J_data = %+.3f)  leptons (%.4f, %.6f)' % (target, J, J / T.DATA['J'], *l), flush=True)
