"""Pass 11924 scan: two Delta(54) triplets (Higgs h, flavon phi): general self-potentials + lam * general mixed quartic
(C_de = C_{-d,-e} for Delta(54); unconstrained for the Delta(27) control). For each coupling draw, the global minimum
at lam = 0.1 and its continuation to lam = 0.01 and 0.001; record the up-sector gap of Y(h) = h_{a+b} g_{a-b}, g even.
Columns: gap(0.1), gap(0.01), gap(0.001), Higgs max Pauli expectation at 0.1."""
import numpy as np
from scipy.optimize import minimize

W = np.exp(2j * np.pi / 3)
XP = np.roll(np.eye(3), 1, axis=0); ZP = np.diag([1, W, W * W])
PAULIS = np.array([np.linalg.matrix_power(XP, a) @ np.linalg.matrix_power(ZP, b) for a in range(3) for b in range(3) if (a, b) != (0, 0)])
G = np.array([1, 0.1, 0.1])
IDX = np.arange(3)


def unit(x):
    z = x[:3] + 1j * x[3:]
    return z / np.linalg.norm(z)


def sp(h, a, c):
    return a * np.sum(np.abs(h) ** 4) + np.real(c * np.sum(np.conj(h) ** 2 * h[(IDX + 1) % 3] * h[(IDX + 2) % 3]))


def mixed(h, f, C):
    v = 0.0
    for d in range(3):
        hh = np.conj(h) * h[(IDX + d) % 3]
        for e in range(3):
            v += np.real(C[d, e] * np.sum(hh * np.conj(f[(IDX + e) % 3]) * f[(IDX + e - d) % 3]))
    return v


def gap(h):
    Y = h[(IDX[:, None] + IDX[None, :]) % 3] * G[(IDX[:, None] - IDX[None, :]) % 3]
    s = np.linalg.svd(Y, compute_uv=False)
    return min(abs(s[0] - s[1]), abs(s[1] - s[2])) / s[0]


def pmax(h):
    return float(np.max(np.abs(np.einsum('i,pij,j->p', np.conj(h), PAULIS, h))))




def scan(sym, seed, n, only=None):
    rng = np.random.default_rng(seed)
    rows = []
    for trial in range(n):
        ah, ch, af, cf = rng.normal(), rng.normal() + 1j * rng.normal(), rng.normal(), rng.normal() + 1j * rng.normal()
        C = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
        if sym == 'd54':
            C = (C + C[np.ix_([0, 2, 1], [0, 2, 1])]) / 2

        def F(x, lam):
            return sp(unit(x[:6]), ah, ch) + sp(unit(x[6:]), af, cf) + lam * mixed(unit(x[:6]), unit(x[6:]), C)

        best = None
        for _ in range(20):
            r = minimize(F, rng.normal(size=12), args=(0.1,), method='BFGS', options=dict(gtol=1e-12))
            if best is None or r.fun < best.fun - 1e-13:
                best = r
        x = best.x
        gaps = [gap(unit(x[:6]))]
        pm = pmax(unit(x[:6]))
        for lam in (0.01, 0.001):
            x = min((minimize(F, x + 1e-5 * rng.normal(size=12), args=(lam,), method='BFGS', options=dict(gtol=1e-13)) for _ in range(4)),
                    key=lambda q: q.fun).x
            gaps.append(gap(unit(x[:6])))
        if only is None or trial in only:
            rows.append(gaps + [pm])
    return np.array(rows)
