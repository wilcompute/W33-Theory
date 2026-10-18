"""Pass 12045 search driver: is the Barr row a level-3 theta vector b_c = lambda theta_c(tau_B, w)?

mode 'shared' : tau_B = tau_d (the 5bar torus itself)             -> 6 parameters for 6 down targets
mode 'free'   : tau_B an independent modulus                       -> 8 parameters
mode 'row'    : 12005's free complex row (positive control)        -> 8 parameters
Run: py -3 barrfit.py <mode> <starts> <seed>
"""
import json
import os
import sys

import numpy as np
from scipy.optimize import least_squares

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from w33_pass11942_hypercharge_wilson_leptons import DATA, normalised, theta  # noqa: E402

Y_UP, EU = .8744698731421595, .005520606513514881
TAU = 1 + 1j * Y_UP
PH = np.exp(1j * np.pi * np.arange(3) ** 2 / 3)
KEYS = ['ms_mb', 'md_ms', 'Vus', 'Vcb', 'Vub', 'J']


def theta1(tau, w, N=12):
    """Level-3 genus-1 theta vector theta_c(tau, w) = sum_n exp(3 pi i tau (n+c/3)^2 + 6 pi i (n+c/3) w)."""
    n = np.arange(-N, N + 1)
    return np.array([np.exp(3j * np.pi * tau * (n + c / 3) ** 2 + 6j * np.pi * (n + c / 3) * w).sum() for c in range(3)])


def up_real():
    Ou = np.array([[TAU, 1j * EU], [1j * EU, TAU]])
    u = PH.conj()[:, None] * theta(Ou) * PH.conj()[None, :]
    u = u.real / np.linalg.norm(u)
    return u @ np.diag([np.sign(np.linalg.det(u)), 1, 1])


U = up_real()
UU, SU, _ = np.linalg.svd(U)


def down_real(lyd, ed, zi):
    Od = np.array([[TAU, 1j * ed], [1j * ed, 1j * np.exp(lyd)]])
    d = PH.conj()[:, None] * normalised(Od, (0, 1j * zi))
    if abs(d.imag).max() > 1e-9 * abs(d).max():
        raise ValueError('not CP-real')
    d = d.real / np.linalg.norm(d)
    return d


def obs(m, b):
    K = np.eye(3) - np.outer(b.conj(), b) / (1 + np.vdot(b, b).real)
    ev, O = np.linalg.eigh(K)
    A = (O * np.sqrt(np.clip(ev, 0, None))) @ O.conj().T
    Ud, sd, _ = np.linalg.svd(m @ A)
    V = (UU.conj().T @ Ud)[::-1, ::-1]
    J = float((V[0, 0] * V[1, 1] * V[0, 1].conj() * V[1, 0].conj()).imag)
    return dict(ms_mb=sd[1] / sd[0], md_ms=sd[2] / sd[1], Vus=abs(V[0, 1]), Vcb=abs(V[1, 2]), Vub=abs(V[0, 2]), J=J)


def brow(x, mode):
    if mode == 'shared':
        return np.exp(x[3]) * theta1(1j * np.exp(x[0]), x[4] + 1j * x[5]) * np.exp(-3 * np.pi * x[5] ** 2 / np.exp(x[0]))
    if mode == 'free':
        tb = x[6] + 1j * np.exp(x[7])
        return np.exp(x[3]) * theta1(tb, x[4] + 1j * x[5]) * np.exp(-3 * np.pi * x[5] ** 2 / tb.imag)
    return np.array([x[3], x[4] + 1j * x[5], x[6] + 1j * x[7]])


def resid(x, mode):
    try:
        m = down_real(*x[:3])
        b = brow(x, mode)
        if not np.all(np.isfinite(b)) or np.linalg.norm(b) > 1e4:
            return np.full(6, 50.)
        o = obs(m, b)
    except Exception:
        return np.full(6, 50.)
    r = [np.log(o[k] / DATA[k]) for k in KEYS[:5]] + [(o['J'] - DATA['J']) / DATA['J']]
    r = np.array(r)
    return r if np.all(np.isfinite(r)) else np.full(6, 50.)


def start(rng, mode):
    x = [np.log(rng.uniform(.05, 3)), rng.uniform(.005, .3) * rng.choice([-1, 1]), rng.normal(0, .3),
         np.log(10 ** rng.uniform(-1, 1.5)), rng.uniform(-.5, .5), rng.normal(0, .3)]
    if mode == 'free':
        x += [rng.uniform(-.5, .5), np.log(rng.uniform(.1, 2))]
    if mode == 'row':
        x = x[:3] + list(rng.normal(size=5) * 10 ** rng.uniform(-1, 1.2))
    return np.array(x)


if __name__ == '__main__':
    mode, n, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    rng = np.random.default_rng(seed)
    sols = []
    for i in range(n):
        r = least_squares(resid, start(rng, mode), args=(mode,), xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=3000)
        c = float(np.sum(r.fun ** 2))
        sols.append((c, r.x.tolist()))
        if c < 1e-16:
            print(f'{mode} start {i}: EXACT chi={c:.2e} x={np.round(r.x, 6).tolist()}', flush=True)
    sols.sort()
    json.dump(dict(mode=mode, seed=seed, starts=n, best=sols[:20], n_exact=sum(c < 1e-16 for c, _ in sols)),
              open(os.path.join(HERE, f'barrfit_{mode}_{seed}.json'), 'w'), indent=1)
    print(mode, 'best', sols[0][0], 'n_exact', sum(c < 1e-16 for c, _ in sols), flush=True)
