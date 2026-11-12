"""Pass 12649 item 2: are optima isolated or families?  Numerical Hessian of F on the unit sphere (real coordinates, projected to the
tangent space minus the phase direction) at polished optima: the number of near-zero eigenvalues = local dimension of the optimum set.
Control: three-qubit size-5 set (minimisers form a continuum, Pass 12647).  Targets: four-qubit genuine size-5 set (type A, min 0.05236)
and the two-qutrit pentad (min 0.14711, single profile).
usage: py -3 analysis/w33_optimum_hessian_nullity.py"""
import json, os, contextlib, io
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
def hessian_nullity(Fn, d, starts=40, seed=0):
    rng = np.random.default_rng(seed)
    best = min((minimize(Fn, rng.standard_normal(2 * d), method="BFGS", options=dict(gtol=1e-13)) for _ in range(starts)), key=lambda r: r.fun)
    x = best.x / np.linalg.norm(best.x); h = 1e-4; D = 2 * d
    def g(y): return Fn(y / np.linalg.norm(y))
    H = np.zeros((D, D))
    for i in range(D):
        for j in range(i, D):
            ei = np.zeros(D); ej = np.zeros(D); ei[i] = h; ej[j] = h
            H[i, j] = H[j, i] = (g(x + ei + ej) - g(x + ei - ej) - g(x - ei + ej) + g(x - ei - ej)) / (4 * h * h)
    v = x[:d] + 1j * x[d:]; phase = np.concatenate([(1j * v).real, (1j * v).imag])
    B = np.linalg.svd(np.column_stack([x, phase]), full_matrices=True)[0][:, 2:]  # orthonormal complement of radial + phase
    ev = np.linalg.eigvalsh(B.T @ H @ B)
    return float(best.fun), [float(e) for e in ev[:6]], int(np.sum(np.abs(ev) < 1e-4 * max(1.0, np.abs(ev).max())))
res = {}
cs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_strong_umub_census.py")}
_s = open(os.path.join(HERE, "w33_strong_umub_census.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(_s[: _s.index(chr(10) + "res = {}")], cs)
for label, p, nq in [("three_qubit_control", 2, 3), ("pentad", 3, 2)]:
    pts, lag, w = cs["geometry"](p, nq); B_ = cs["bases_for"](p, nq, pts, lag); mps, _ = cs["maximal_partial_spreads"](lag)
    S = sorted(next(S for S in mps if len(S) == 5)); E = [b for L in S for b in B_[L].T]; d = p ** nq
    Fn = lambda z, E=E, d=d: sum((abs(np.vdot(e, z[:d] + 1j * z[d:])) ** 2 / (np.linalg.norm(z) ** 2) - 1 / d) ** 2 for e in E)
    f, ev, nul = hessian_nullity(Fn, d); res[label] = dict(min_F=f, smallest_tangent_eigs=ev, nullity=nul); print(label, res[label], flush=True)
ex2 = {"__name__": "x", "__file__": os.path.join(HERE, "w33_four_qubit_theta_exact.py")}
s2 = open(os.path.join(HERE, "w33_four_qubit_theta_exact.py"), encoding="utf-8").read()
exec(s2[: s2.index("rows, cols = []")], ex2)
C = frozenset().union(*[ex2["lags"][i] for i in [129, 190, 287, 444, 530]])
X1 = np.array([[0, 1], [1, 0]]); Z1 = np.diag([1, -1])
def pauli(v):
    M = np.eye(1)
    for i in range(4):
        x_ = (v >> i) & 1; z_ = (v >> (4 + i)) & 1
        M = np.kron(M, (1j) ** (x_ * z_) * np.linalg.matrix_power(X1, x_) @ np.linalg.matrix_power(Z1, z_))
    return M
Ps = np.array([pauli(v) for v in sorted(C)])
def F4(z):
    v = z[:16] + 1j * z[16:]; v = v / np.linalg.norm(v)
    return float(np.sum(np.einsum("i,kij,j->k", v.conj(), Ps, v).real ** 2)) / 16
f, ev, nul = hessian_nullity(F4, 16, starts=30); res["four_qubit_genuine"] = dict(min_F=f, smallest_tangent_eigs=ev, nullity=nul); print("four_qubit_genuine", res["four_qubit_genuine"], flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_optimum_hessian_nullity.json"), "w"), indent=1)
