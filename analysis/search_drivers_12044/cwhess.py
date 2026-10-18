import os as _os
import sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
_ANA = _os.path.dirname(_HERE)
_sys.path.insert(0, _HERE)
"""Task 3: transverse Hessian of the Codex-12034 toy Coleman-Weinberg potential across the CP-fixed theta locus."""
import sys

import numpy as np

sys.path.insert(0, _ANA)
from w33_pass12004_cp_real_bare_theta_no_fit import theta_c  # noqa: E402

NC = (3, 3, 1)


def mats(x):
    rt, y, reu, iu, rtd, yd, red, idd, rz, zi = x
    tau = rt + 1j * y
    Omu = np.array([[tau, reu + 1j * iu], [reu + 1j * iu, tau]])
    Omd = np.array([[tau, red + 1j * idd], [red + 1j * idd, rtd + 1j * yd]])
    z = np.array([0, rz + 1j * zi])
    return theta_c(Omu, np.zeros(2, complex)), theta_c(Omd, z), theta_c(Omd, 6 * z).T


def spectra(x, scale):
    out = []
    for Y in mats(x):
        Y = Y / np.linalg.norm(Y, 2)            # each sector normalised to its own top Yukawa at the reference only
        out.append(Y)
    return out


def make_V(x0, soft=1.0, Q=1.0):
    ref = mats(x0)
    norms = [np.linalg.norm(Y, 2) for Y in ref]   # fixed baseline per sector, never recomputed (as in 12034)

    def V(x):
        tot = 0.0
        for n, Y, nr in zip(NC, mats(x), norms):
            z = np.linalg.eigvalsh((Y / nr) @ (Y / nr).conj().T).clip(1e-300)
            f = lambda w: w * w * (np.log(w / Q ** 2) - 1.5)
            tot += n * np.sum(f(z + soft) - f(z))
        return tot / (16 * np.pi ** 2)
    return V


def hess(V, x0, idx, h=1e-4):
    k = len(idx)
    H = np.zeros((k, k))
    f0 = V(x0)
    for a in range(k):
        for b in range(a, k):
            ea = np.zeros(10); eb = np.zeros(10)
            ea[idx[a]] = h; eb[idx[b]] = h
            H[a, b] = H[b, a] = (V(x0 + ea + eb) - V(x0 + ea - eb) - V(x0 - ea + eb) + V(x0 - ea - eb)) / (4 * h * h)
    return H


def grad(V, x0, idx, h=1e-6):
    out = []
    for i in idx:
        e = np.zeros(10); e[i] = h
        out.append((V(x0 + e) - V(x0 - e)) / (2 * h))
    return np.array(out)


T = [0, 2, 4, 6, 8]          # transverse (real-part) directions
L = [1, 3, 5, 7, 9]          # longitudinal (imaginary-part) directions
POINTS = {
    '12005 vacuum (Re z=0)': np.array([1.0, 0.8744698731421595, 0.0, 0.005520606513514881, 0.0, 0.4315140195185126, 0.0, 0.08087153936666885, 0.0, 0.0677453432123109]),
    '12004 bare optimum':    np.array([1.0, 0.8745, 0.0, 0.00552, 0.0, 3.116, 0.0, 0.4061, 2 / 6, 12.86]),
    'random locus point':    np.array([1.0, 0.95, 0.0, 0.004, 1.0, 0.2, 0.0, 0.03, 1 / 6, 0.05]),
}
for name, x0 in POINTS.items():
    for Q in (0.5, 1.0, 2.0):
        V = make_V(x0, soft=1.0, Q=Q)
        gT, gL = grad(V, x0, T), grad(V, x0, L)
        ev = np.linalg.eigvalsh(hess(V, x0, T))
        print(f'{name:24s} Q={Q}: |grad_T|={np.abs(gT).max():.1e} |grad_L|={np.abs(gL).max():.2e}  transverse Hessian eigenvalues', np.array2string(ev, precision=3))
