import os as _os
import sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ANA = _os.path.dirname(_HERE)
_sys.path.insert(0, _HERE)
"""Exact one-parameter scans for the surviving S-type branches."""
import numpy as np
from scipy.optimize import minimize_scalar
from sfit import DATA, theta_c
from upS import up
UPS = {'+': (0.832764, 0.823581), '-': (2.318011, 2.308829)}
DK = ['ms_mb', 'md_ms', 'Vus', 'Vcb', 'Vub']


def dhome(tau, a1, sg):
    u = np.exp(1j * a1)
    t = (1 - abs(tau) ** 2) / (2 * (1 - (np.conj(tau) * u).real))
    if not 0 < t < 1:
        return None
    w = (tau - t * u) / (1 - t)
    if w.imag <= 1e-6:
        return None
    c, s = np.sqrt(t), sg * np.sqrt(1 - t)
    R = np.array([[c, -s], [s, c]])
    return R @ np.diag([u, w / abs(w)]) @ R.T


def chi_down(Ou, Od):
    if Od is None or np.linalg.eigvalsh(Od.imag).min() < 1e-5:
        return np.nan, None
    Uu, _, _ = np.linalg.svd(theta_c(Ou, np.zeros(2, complex)))
    Ud, sd, _ = np.linalg.svd(theta_c(Od, np.zeros(2, complex)))
    V = (Uu.conj().T @ Ud)[::-1, ::-1]
    o = dict(ms_mb=sd[1] / sd[0], md_ms=sd[2] / sd[1], Vus=abs(V[0, 1]), Vcb=abs(V[1, 2]), Vub=abs(V[0, 2]))
    return sum((np.log(max(o[q], 1e-300) / DATA[q][0]) / DATA[q][1]) ** 2 for q in DK), o


print('(a) CP o (SxS) on both homes, Wilson-free down, tau at the exact up solution')
for su in '+-':
    Ou = up(*UPS[su]); tau = Ou[0, 0]
    for sg in (1, -1):
        A = np.linspace(1e-4, np.pi - 1e-4, 20001)
        vals = np.array([chi_down(Ou, dhome(tau, a, sg))[0] for a in A])
        i = np.nanargmin(vals)
        r = minimize_scalar(lambda a: chi_down(Ou, dhome(tau, a, sg))[0] if np.isfinite(chi_down(Ou, dhome(tau, a, sg))[0]) else 1e12,
                            bounds=(A[max(i - 2, 0)], A[min(i + 2, len(A) - 1)]), method='bounded', options=dict(xatol=1e-12))
        c, o = chi_down(Ou, dhome(tau, r.x, sg))
        print(f'  up {su} sign {sg:+d}: valid {np.isfinite(vals).sum()}/{len(A)}  min chi2_down = {c:.4g} at a1={r.x:.6f}', {k: round(v, 5) for k, v in o.items()})

print('(b) CP o (S x T0) up home: |tau|=1, 2cos(theta) = -|eps_u|^2, arg eps_u = (theta+pi)/2 mod pi')
T = (0.620 / 168.26, 1.23e-3 / 0.620)
for br in (0, 1):
    def chiu(lr):
        rho = 10 ** lr; th = np.arccos(-rho ** 2 / 2); eps = rho * np.exp(1j * ((th + np.pi) / 2 + br * np.pi))
        tau = np.exp(1j * th); O = np.array([[tau, eps], [eps, tau]])
        if np.linalg.eigvalsh(O.imag).min() < 1e-6: return np.nan, None
        s = np.linalg.svd(theta_c(O, np.zeros(2, complex)), compute_uv=False)
        o = (s[1] / s[0], s[2] / s[1])
        return (np.log(o[0] / T[0]) / .05) ** 2 + (np.log(o[1] / T[1]) / .20) ** 2, o
    L = np.linspace(-6, 0.15, 6001)
    v = np.array([chiu(l)[0] for l in L]); i = np.nanargmin(v)
    r = minimize_scalar(lambda l: chiu(l)[0], bounds=(L[max(i - 2, 0)], L[min(i + 2, 6000)]), method='bounded', options=dict(xatol=1e-12))
    print(f'  branch {br}: min chi2_up = {chiu(r.x)[0]:.4g} at |eps_u| = {10 ** r.x:.5g}, (mc/mt, mu/mc) =', np.round(chiu(r.x)[1], 6), 'target', np.round(T, 6))
