"""Pass 12647 item 4 follow-up: Kantor (Adv. Geom. 2017) reports Grassl's examples of maximal symplectic partial spreads of size
q^{n/2}+1 for even n, q (here 2n = 8, q = 2: size 5).  Feasibility ILPs for maximal partial spreads of W(7,2) of size exactly k = 3, 4, 5
(HiGHS, time-limited); for a size-5 set: invariants, theta, numerical min F and the stabiliser value m*/16.
usage: py -3 analysis/w33_four_qubit_small_sizes.py"""
import json, os, itertools, time
from collections import Counter
import numpy as np, cvxpy as cp
from scipy.optimize import milp, LinearConstraint, Bounds, minimize
import scipy.sparse as sps
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ex = {"__name__": "x", "__file__": os.path.join(HERE, "w33_four_qubit_theta_exact.py")}
src = open(os.path.join(HERE, "w33_four_qubit_theta_exact.py"), encoding="utf-8").read()
exec(src[: src.index("rows, cols = []")], ex)
lags, w = ex["lags"], ex["w"]; nL = len(lags); NV = 256; d = 16
rows, cols = [], []
for i, L in enumerate(lags):
    for x in L: rows.append(x - 1); cols.append(i)
Apt = sps.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(NV - 1, nL)); Amax = sps.csr_matrix(((Apt.T @ Apt) > 0).astype(float))
out = {}
for k in (5, 4):
    t = time.time()
    r = milp(np.zeros(nL), constraints=[LinearConstraint(Apt, 0, 1), LinearConstraint(Amax, 1, np.inf), LinearConstraint(np.ones((1, nL)), k, k)],
             integrality=np.ones(nL), bounds=Bounds(0, 1), options=dict(time_limit=2400))
    sol = [i for i in range(nL) if r.x is not None and r.x[i] > 0.5]
    out["k%d" % k] = dict(status=int(r.status), message=r.message, found=bool(sol), lines=sol, seconds=time.time() - t)
    print(k, out["k%d" % k], flush=True)
    if sol and not out.get("smallest"):
        C = frozenset().union(*[lags[i] for i in sol]); U = [x for x in range(1, NV) if x not in C]; n = len(U)
        assert len(C) == 15 * k and all(len(L & C) > 0 for L in lags)
        hist = Counter(len(lags[i] & C) for i in range(nL) if i not in sol)
        E = [(a, b) for a, b in itertools.combinations(range(n), 2) if w(U[a], U[b]) == 1]
        X = cp.Variable((n, n), symmetric=True)
        pr = cp.Problem(cp.Maximize(cp.sum(X)), [X >> 0, cp.trace(X) == 1] + [X[a, b] == 0 for a, b in E]); pr.solve(solver=cp.SCS, eps=1e-7, max_iters=50000)
        X1 = np.array([[0, 1], [1, 0]]); Z1 = np.diag([1, -1])
        def pauli(v):
            M = np.eye(1)
            for i in range(4):
                x = (v >> i) & 1; z = (v >> (4 + i)) & 1
                M = np.kron(M, (1j) ** (x * z) * np.linalg.matrix_power(X1, x) @ np.linalg.matrix_power(Z1, z))
            return M
        Ps = np.array([pauli(v) for v in C])
        def fg(z):
            v = z[:d] + 1j * z[d:]; nv = np.vdot(v, v).real
            Pv = Ps @ v; f = np.einsum("i,ki->k", v.conj(), Pv).real
            g = float(np.sum(f ** 2)) / d
            gr = (4 * np.einsum("ki,k->i", Pv, f) / d) / nv ** 2 - 4 * g * v / nv ** 3
            return g / nv ** 2, np.concatenate([gr.real, gr.imag])
        rng = np.random.default_rng(0)
        fmin = min(minimize(fg, rng.standard_normal(2 * d), jac=True, method="L-BFGS-B", options=dict(gtol=1e-13, maxiter=10000)).fun for _ in range(150))
        out["smallest"] = dict(k=k, lines=sol, n_uncovered=n, m_star=min(hist), theta=float(pr.value), alpha_candidate=15 - min(hist),
                               numeric_min_F=float(fmin), stabiliser_value=min(hist) / 16, meeting_histogram=dict(sorted(hist.items())))
        print("smallest:", {kk: vv for kk, vv in out["smallest"].items() if kk not in ("lines", "meeting_histogram")}, flush=True)
json.dump(out, open(os.path.join(ROOT, "data", "w33_four_qubit_small_sizes.json"), "w"), indent=1)
