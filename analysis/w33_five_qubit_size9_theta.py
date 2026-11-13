"""Pass 12652 item 4: Lovasz theta of the anticommutation graph on the 744 uncovered non-identity Paulis of the five-qubit size-9 set.
F = (31 - Sigma_U)/32 and Sigma_U <= theta (de Gois-Hansenne-Guhne), so theta = 30 would give min F = 1/32 exactly (the stabiliser
value; Pass 12651 numerics).  Also the trivial lower bound alpha >= 30 (uncovered part of a Lagrangian meeting C once).
usage: py -3 analysis/w33_five_qubit_size9_theta.py"""
import json, os, time, itertools
import numpy as np, cvxpy as cp
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
n = 5; pos = [(i, j) for i in range(n) for j in range(i, n)]
ex = json.load(open(os.path.join(ROOT, "data", "w33_five_qubit_size9_verify.json")))["example"]
def decode(code):
    S = np.zeros((n, n), int)
    for b, (i, j) in enumerate(pos):
        if code >> b & 1: S[i, j] = S[j, i] = 1
    return S
vec = lambda xv, zv: tuple(int(v) for v in xv) + tuple(int(v) for v in zv)
C = set()
for x in range(1, 1 << n):
    xv = np.array([(x >> i) & 1 for i in range(n)])
    C.add(vec(xv, [0] * n)); C.add(vec([0] * n, xv))
    for c in ex: C.add(vec(xv, decode(c) @ xv % 2))
allp = [tuple((v >> i) & 1 for i in range(2 * n)) for v in range(1, 1 << (2 * n))]
U = [p for p in allp if p not in C]
assert len(C) == 279 and len(U) == 744
Ua = np.array(U)
symp = (Ua[:, :n] @ Ua[:, n:].T + Ua[:, n:] @ Ua[:, :n].T) % 2  # 1 = anticommute
deg = symp.sum(1)
res = dict(n_uncovered=len(U), degrees=sorted(set(deg.tolist())))
# alpha lower bound: Lagrangians meeting C exactly once (graphs of symmetric T with exactly one... ) -- brute: greedy commuting sets
best = 0
rng = np.random.default_rng(3)
for _ in range(3000):
    order = rng.permutation(len(U)); S = []
    for v in order:
        if all(symp[v, w] == 0 for w in S): S.append(v)
    best = max(best, len(S))
res["alpha_greedy"] = best
print(res, flush=True)
t0 = time.time()
N = len(U); X = cp.Variable((N, N), symmetric=True)
ii, jj = np.nonzero(np.triu(symp, 1))
cons = [X >> 0, cp.trace(X) == 1, X[ii, jj] == 0]
prob = cp.Problem(cp.Maximize(cp.sum(X)), cons)
prob.solve(solver=cp.SCS, eps=1e-7, max_iters=200000, verbose=False)
res.update(theta=float(prob.value), status=prob.status, seconds=round(time.time() - t0, 1), n_edges=int(len(ii)))
print(res, flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_five_qubit_size9_theta.json"), "w"), indent=1)
