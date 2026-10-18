import os as _os
import sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ANA = _os.path.dirname(_HERE)
_sys.path.insert(0, _HERE)
import numpy as np
from scipy.optimize import minimize_scalar
from sfit import theta_c
from jointS import img
from sfit import sp
T = (0.620 / 168.26, 1.23e-3 / 0.620)
M = sp(0, -1, 1, 0, 1, -2, 0, 1)
def home(lr, br):
    rho = 10 ** lr; th = np.arccos(1 - rho ** 2 / 2); eps = rho * np.exp(1j * ((th + np.pi) / 2 + br * np.pi))
    return np.array([[np.exp(1j * th), eps], [eps, np.exp(1j * th)]])
O = home(-1.3, 0); O2, _ = img(M, O, np.zeros(2, complex)); print('fixed-point residual of the S x T^-2 up home:', np.abs(O - O2).max())
def chiu(lr, br):
    O = home(lr, br)
    if np.linalg.eigvalsh(O.imag).min() < 1e-7: return np.inf
    s = np.linalg.svd(theta_c(O, np.zeros(2, complex)), compute_uv=False)
    return (np.log(s[1] / s[0] / T[0]) / .05) ** 2 + (np.log(s[2] / s[1] / T[1]) / .20) ** 2
for br in (0, 1):
    L = np.linspace(-6, 0.3, 6301); v = np.array([chiu(l, br) for l in L]); i = int(np.argmin(v))
    r = minimize_scalar(lambda l: chiu(l, br), bounds=(L[max(i - 2, 0)], L[min(i + 2, len(L) - 1)]), method='bounded', options=dict(xatol=1e-12))
    print('branch', br, 'valid', np.isfinite(v).sum(), 'min chi2_up = %.4g at |eps_u| = %.4g' % (chiu(r.x, br), 10 ** r.x), 'min eig Im at min', np.linalg.eigvalsh(home(r.x, br).imag).min())
