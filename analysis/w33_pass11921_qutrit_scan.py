"""Scans for Pass 11921 (hypercharge Wilson line model of Pass 11918, theta truncation |n_i| <= 6, grid 12).

haar(seed, n, pair, only):  H_u = flavour-qutrit state h in the exactly 3-dim top-Yukawa space (12 stabiliser states and
    200 Haar-random states per modulus), H_d radiative (top eigenvector of the down Gram matrix).
    Row: sample, kind (0 stabiliser, 1 Haar), md/ms, ms/mb, mu/mc, mc/mt, me/mmu, mmu/mtau, Vus, Vcb, Vub, sorted |h|.
fit(seed, n, pair):  per modulus, least-squares fit of h (4 real dof, 3 class orderings x 12 starts) to
    (mu/mc, mc/mt, Vus, Vcb, Vub). Row: sample, Im Omega scale, best log-rms, the five fitted observables, down md/ms,
    ms/mb, and |g+/g0|, |g-/g0|.
"""

import sys
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11915_su5_matrix_fluxes_on_t4 as F  # noqa: E402
import w33_pass11918_hypercharge_wilson_scan as S  # noqa: E402

TARGET = np.log([2.05e-3, 3.61e-3, 0.2245, 0.0410, 0.00382])
W3 = np.exp(2j * np.pi / 3)
STAB = [np.eye(3)[k] for k in range(3)] + [np.array([W3 ** (s * j * j + t * j) for j in range(3)]) / np.sqrt(3)
                                           for s in range(3) for t in range(3)]


def _radiative(Ys):
    M = np.array([Y.ravel() for Y in Ys])
    w, V = np.linalg.eigh(M.conj() @ M.T)
    return np.tensordot(V[:, -1], np.array(Ys), 1)


def _setup(pair, rng, ximax):
    N10 = S.PAIRS[pair]
    N5 = np.round(3 * np.linalg.inv(N10)).astype(int).tolist()
    N10a = np.array(N10, float)
    lam = np.linalg.eigvalsh(N10a)
    while True:
        xi, yi = rng.uniform(0.5, ximax), rng.uniform(-0.5, 0.8)
        if min(xi + yi * lam) > 0.4:
            break
    xr, yr = rng.uniform(-0.5, 0.5, 2)
    Om = (xr + 1j * xi) * np.eye(2) + (yr + 1j * yi) * N10a

    def lat(v):
        return v[:2] + Om @ v[2:]

    P = S.positions(N10, N5, lat(rng.random(4)), lat(rng.random(4)), lat(rng.random(4) - 0.5))
    return N10, N5, Om, P, xi


def _classes(Yu_all):
    M = Yu_all.reshape(len(Yu_all), 9)
    C = M.conj() @ M.T
    supp = [tuple(np.flatnonzero(abs(Y.ravel()) > 1e-9 * abs(Y).max())) for Y in Yu_all]
    cls = {}
    for k, s_ in enumerate(supp):
        cls.setdefault(s_, []).append(k)
    Mk = []
    for ks in cls.values():
        ww, vv = np.linalg.eigh(C[np.ix_(ks, ks)])
        Mk.append(np.tensordot(vv[:, -1], Yu_all[ks], 1))
    return np.array(Mk), len(cls)


def _with_ns(fn):
    def run(*a, **k):
        saved = F.NS
        F.NS = np.array([(x, y) for x in range(-6, 7) for y in range(-6, 7)])
        try:
            return fn(*a, **k)
        finally:
            F.NS = saved
    return run


@_with_ns
def haar(seed, n, pair, only=None):
    rng = np.random.default_rng(seed)
    rows = []
    for it in range(n):
        N10, N5, Om, P, xi = _setup(pair, rng, 3.0)
        T = F.T4(Om, 12)
        Yu_all = np.array(F.yukawas(T, N10, N10, P["Q"], P["u"]))
        Yd = _radiative(F.yukawas(T, N10, N5, P["Q"], P["d"]))
        Ye = _radiative(F.yukawas(T, N10, N5, P["e"], P["L"]))
        Mk, ncls = _classes(Yu_all)
        if ncls != 3:
            continue
        Ud, sd, _ = np.linalg.svd(Yd)
        se = np.linalg.svd(Ye, compute_uv=False)
        z = rng.normal(size=(200, 3)) + 1j * rng.normal(size=(200, 3))
        hs = [(0, h) for h in STAB[:12]] + [(1, h) for h in z / np.linalg.norm(z, axis=1)[:, None]]
        if only is not None and it not in only:
            continue
        for kind, h in hs:
            Uu, su, _ = np.linalg.svd(np.tensordot(h, Mk, 1))
            V = abs(Uu.conj().T @ Ud)
            rows.append([it, kind, sd[2] / sd[1], sd[1] / sd[0], su[2] / su[1], su[1] / su[0], se[2] / se[1],
                         se[1] / se[0], V[2, 1], V[1, 0], V[2, 0], *sorted(abs(h))])
    return np.array(rows)


def _obs(p, Mk, Ud):
    h = np.array([1.0, np.exp(p[0] + 1j * p[1]), np.exp(p[2] + 1j * p[3])])
    Uu, su, _ = np.linalg.svd(np.tensordot(h, Mk, 1))
    V = abs(Uu.conj().T @ Ud)
    return np.log(np.maximum([su[2] / su[1], su[1] / su[0], V[2, 1], V[1, 0], V[2, 0]], 1e-300))


@_with_ns
def fit(seed, n, pair):
    rng = np.random.default_rng(seed)
    rows = []
    for it in range(n):
        N10, N5, Om, P, xi = _setup(pair, rng, 4.0)
        T = F.T4(Om, 12)
        Yu_all = np.array(F.yukawas(T, N10, N10, P["Q"], P["u"]))
        Yd = _radiative(F.yukawas(T, N10, N5, P["Q"], P["d"]))
        Mk0, ncls = _classes(Yu_all)
        if ncls != 3:
            continue
        Ud, sd, _ = np.linalg.svd(Yd)
        e = sorted(abs(Mk0[0][abs(Mk0[0]) > 1e-9 * abs(Mk0[0]).max()]))[::-1]
        best, bo = np.inf, None
        for perm in ([0, 1, 2], [1, 2, 0], [2, 0, 1]):
            Mk = Mk0[perm]
            for _ in range(12):
                p0 = np.r_[rng.uniform(-14, 0), rng.uniform(0, 6.3), rng.uniform(-14, 0), rng.uniform(0, 6.3)]
                r = least_squares(lambda p: _obs(p, Mk, Ud) - TARGET, p0, bounds=([-30, -50, -30, -50], [3, 50, 3, 50]))
                c = np.sqrt(np.mean(r.fun ** 2))
                if c < best:
                    best, bo = c, _obs(r.x, Mk, Ud)
        rows.append([it, xi, best, *np.exp(bo), sd[2] / sd[1], sd[1] / sd[0], e[1] / e[0], e[2] / e[0]])
    return np.array(rows)
