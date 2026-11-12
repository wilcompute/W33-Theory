"""Pass 12648 item 3: the non-stabiliser optimum of the size-5 four-qubit set (lines [129, 190, 287, 444, 530]).  Polish min F to double
precision (many L-BFGS starts + BFGS refinement), report the value, the number of distinct |<P>| profiles among optima, the profile levels
over covered Paulis, and an identification attempt that is ACCEPTED only if a low-degree integer polynomial (coefficients <= 10^4) fits
with residual < 1e-13 -- NOTE (Pass 12648): this criterion proved too loose; the resulting cubic fit is rejected in the JSON (candidate count makes it expected by chance).
usage: py -3 analysis/w33_four_qubit_size5_optimum.py"""
import json, os
from collections import Counter
import numpy as np, mpmath as mp
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ex = {"__name__": "x", "__file__": os.path.join(HERE, "w33_exhaustive_small_maximal_spreads.py")}
src = open(os.path.join(HERE, "w33_exhaustive_small_maximal_spreads.py"), encoding="utf-8").read()
exec(src[: src.index("def decide")], ex)
lags, NV = ex["lagrangians"](4); n = 4; d = 16
# map the lines of the Pass 12647 set (indexing of w33_four_qubit_theta_exact.py) -> recompute in this indexing via the stored sets
ex2 = {"__name__": "x", "__file__": os.path.join(HERE, "w33_four_qubit_theta_exact.py")}
src2 = open(os.path.join(HERE, "w33_four_qubit_theta_exact.py"), encoding="utf-8").read()
exec(src2[: src2.index("rows, cols = []")], ex2)
C = frozenset().union(*[ex2["lags"][i] for i in [129, 190, 287, 444, 530]]); assert len(C) == 75
X1 = np.array([[0, 1], [1, 0]]); Z1 = np.diag([1, -1])
def pauli(v):
    M = np.eye(1)
    for i in range(n):
        x = (v >> i) & 1; z = (v >> (n + i)) & 1
        M = np.kron(M, (1j) ** (x * z) * np.linalg.matrix_power(X1, x) @ np.linalg.matrix_power(Z1, z))
    return M
Ps = np.array([pauli(v) for v in sorted(C)])
def fg(z):
    v = z[:d] + 1j * z[d:]; nv = np.vdot(v, v).real
    Pv = Ps @ v; f = np.einsum("i,ki->k", v.conj(), Pv).real
    g = float(np.sum(f ** 2)) / d
    gr = (4 * np.einsum("ki,k->i", Pv, f) / d) / nv ** 2 - 4 * g * v / nv ** 3
    return g / nv ** 2, np.concatenate([gr.real, gr.imag])
rng = np.random.default_rng(3); sols = []
for _ in range(200):
    r = minimize(fg, rng.standard_normal(2 * d), jac=True, method="L-BFGS-B", options=dict(gtol=1e-14, ftol=1e-18, maxiter=20000))
    r = minimize(fg, r.x, jac=True, method="BFGS", options=dict(gtol=1e-15))
    sols.append(r)
sols.sort(key=lambda r: r.fun); best = sols[0].fun
opt = [r for r in sols if r.fun < best + 1e-11]
def prof(r):
    v = r.x[:d] + 1j * r.x[d:]; v = v / np.linalg.norm(v)
    return tuple(sorted(np.round(np.abs([np.vdot(v, P @ v) for P in Ps]), 7)))
profiles = Counter(prof(r) for r in opt)
levels = Counter(prof(opt[0]))
mp.mp.dps = 30
x = mp.mpf(repr(float(best))); accepted = None
for deg in (1, 2, 3, 4):
    p = mp.findpoly(x, deg, maxcoeff=10000, tol=1e-12)
    if p:
        val = abs(mp.polyval(p, x))
        if val < 1e-13 * max(abs(c) for c in p): accepted = dict(degree=deg, coefficients=[int(c) for c in p], residual=float(val)); break
res = dict(min_F=float(best), n_optima=len(opt), starts=len(sols), n_profiles=len(profiles), covered_levels={str(k): v for k, v in sorted(levels.items())},
           stabiliser_value=1 / 16, identification=accepted)
print(res); json.dump(res, open(os.path.join(ROOT, "data", "w33_four_qubit_size5_optimum.json"), "w"), indent=1)
