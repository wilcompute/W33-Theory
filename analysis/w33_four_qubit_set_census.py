"""Pass 12646 item 2: are the four-qubit size-9 maximal partial spreads equivalent?  Sample several solutions of the minimum-size ILP
with random objective weights (size fixed to 9), and for each compute invariants: number of Lagrangians inside the covered set C, the
meeting histogram of the other Lagrangians with C, m*, number of partitions of C into 9 Lagrangians (mirror partners), and theta (SCS).
Different invariants => different Sp(8,2)-orbits.  usage: py -3 analysis/w33_four_qubit_set_census.py"""
import json, os, itertools, time
from collections import Counter
import numpy as np, cvxpy as cp
from scipy.optimize import milp, LinearConstraint, Bounds
import scipy.sparse as sps
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ex = {"__name__": "x", "__file__": os.path.join(HERE, "w33_four_qubit_theta_exact.py")}
src = open(os.path.join(HERE, "w33_four_qubit_theta_exact.py"), encoding="utf-8").read()
exec(src[: src.index("rows, cols = []")], ex)
lags, w = ex["lags"], ex["w"]; nL = len(lags); NV = 256
rows, cols = [], []
for i, L in enumerate(lags):
    for x in L: rows.append(x - 1); cols.append(i)
Apt = sps.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(NV - 1, nL)); Amax = sps.csr_matrix(((Apt.T @ Apt) > 0).astype(float))
def invariants(sol):
    C = frozenset().union(*[lags[i] for i in sol]); inside = [i for i, L in enumerate(lags) if L <= C]
    hist = Counter(len(lags[i] & C) for i in range(nL) if i not in sol)
    parts = [0]
    def rec(rem, cand):
        if not rem: parts[0] += 1; return
        p = min(rem)
        for i in cand:
            if p in lags[i] and lags[i] <= rem: rec(rem - lags[i], [j for j in cand if not (lags[j] & lags[i])])
    rec(C, inside)
    U = [x for x in range(1, NV) if x not in C]; n = len(U)
    E = [(a, b) for a, b in itertools.combinations(range(n), 2) if w(U[a], U[b]) == 1]
    X = cp.Variable((n, n), symmetric=True)
    pr = cp.Problem(cp.Maximize(cp.sum(X)), [X >> 0, cp.trace(X) == 1] + [X[a, b] == 0 for a, b in E]); pr.solve(solver=cp.SCS, eps=1e-7, max_iters=50000)
    return dict(lines=sorted(sol), n_inside=len(inside), n_partitions=parts[0], m_star=min(hist), meeting_histogram=dict(sorted(hist.items())), theta=float(pr.value))
out = []
prev = json.load(open(os.path.join(ROOT, "data", "w33_four_qubit_theta_exact.json")))["lines"]
out.append(dict(source="saved (Pass 12644)", **invariants(prev))); print(out[-1], flush=True)
rng = np.random.default_rng(7); found = [sorted(prev)]
for trial in range(4):
    c = rng.uniform(0.5, 1.5, nL)
    cons = [LinearConstraint(Apt, 0, 1), LinearConstraint(Amax, 1, np.inf), LinearConstraint(np.ones((1, nL)), 9, 9)]
    for f in found:
        r = np.zeros(nL); r[f] = 1; cons.append(LinearConstraint(r.reshape(1, -1), -np.inf, 8))
    t = time.time(); r = milp(c, constraints=cons, integrality=np.ones(nL), bounds=Bounds(0, 1), options=dict(time_limit=1200))
    if r.x is None: print("trial", trial, "no solution", r.message, flush=True); continue
    sol = [i for i in range(nL) if r.x[i] > 0.5]; found.append(sorted(sol))
    out.append(dict(source="random objective %d (%.0fs)" % (trial, time.time() - t), **invariants(sol))); print(out[-1], flush=True)
    json.dump(out, open(os.path.join(ROOT, "data", "w33_four_qubit_set_census.json"), "w"), indent=1)
json.dump(out, open(os.path.join(ROOT, "data", "w33_four_qubit_set_census.json"), "w"), indent=1)
