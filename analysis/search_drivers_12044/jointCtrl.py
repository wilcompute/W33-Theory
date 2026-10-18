import os as _os
import sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ANA = _os.path.dirname(_HERE)
_sys.path.insert(0, _HERE)
"""Positive control: same projection + SLSQP machinery, up home on the CP o g_u fixed set, down home unconstrained (complex)."""
import sys, json
import numpy as np
from scipy.optimize import least_squares, minimize
from jointS import cons, chi2, obs
gu = sys.argv[1].replace('_', ' '); rng = np.random.default_rng(int(sys.argv[2]))
upc = lambda p: cons(p, gu, 'SS', 0)[[0, 1, 2, 7, 8, 9]]       # the up-home rows only (real/imag of the 3 entries)
best = 1e9
for _ in range(int(sys.argv[3])):
    th = np.angle(0.67622 * rng.choice([-1, 1]) + 0.73669j) if gu == 'SS' else rng.uniform(.05, 3.09)
    p0 = np.array([np.cos(th), np.sin(th), *(rng.normal(size=2) * 0.004), *(rng.normal(size=2) * 10 ** rng.uniform(-3, -.5)),
                   rng.uniform(-1, 1), 10 ** rng.uniform(-2, .7), rng.uniform(-.5, .5), rng.normal(0, .3)])
    x = least_squares(upc, p0, xtol=1e-15, ftol=1e-15).x
    for _r in range(3):
        try:
            m = minimize(chi2, x, method='SLSQP', constraints=[{'type': 'eq', 'fun': upc}], options=dict(maxiter=500, ftol=1e-13))
            if np.abs(upc(m.x)).max() < 1e-8 and chi2(m.x) <= chi2(x): x = m.x
        except Exception: break
    best = min(best, chi2(x))
print(gu, 'complex-down control best chi2 = %.3e' % best, flush=True)
