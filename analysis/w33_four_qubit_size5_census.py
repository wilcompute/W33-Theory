"""Pass 12648: all size-5 maximal partial spreads of W(7,2) through a fixed complementary pair (L0, L1) (Witt reduction, exhaustive),
the total count N5 = count * (#ordered complementary pairs) / 20, and invariants of each set through the pair (Lagrangians inside C,
partitions of C, m*, meeting histogram) to count orbit types; theta (SCS) and numerical min F for one representative per type.
usage: py -3 analysis/w33_four_qubit_size5_census.py"""
import json, os, itertools, time
from collections import Counter
import numpy as np, cvxpy as cp
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ex = {"__name__": "x", "__file__": os.path.join(HERE, "w33_exhaustive_small_maximal_spreads.py")}
src = open(os.path.join(HERE, "w33_exhaustive_small_maximal_spreads.py"), encoding="utf-8").read()
exec(src[: src.index("def decide")], ex)
lags, NV = ex["lagrangians"](4); nL = len(lags); n = 4; d = 16; lo = 15
w = lambda x, y: (bin((x & lo) & (y >> n)).count("1") + bin((x >> n) & (y & lo)).count("1")) % 2
Inc = np.zeros((nL, NV), bool)
for i, L in enumerate(lags): Inc[i, list(L)] = True
meet = (Inc.astype(np.int32) @ Inc.T.astype(np.int32)) > 0
i0 = 0; i1 = int(np.flatnonzero(~meet[i0])[0]); cand = np.flatnonzero(~meet[i0] & ~meet[i1]); base = meet[i0] | meet[i1]
sets = []; t = time.time()
for a_idx, a in enumerate(cand):
    r1 = cand[a_idx + 1:]; r1 = r1[~meet[a, r1]]
    for b_idx, b in enumerate(r1):
        r2 = r1[b_idx + 1:]; r2 = r2[~meet[b, r2]]
        if len(r2) == 0: continue
        ok = ((base | meet[a] | meet[b])[None, :] | meet[r2]).all(1)
        for c in r2[ok]: sets.append((i0, i1, int(a), int(b), int(c)))
n_disjoint = int((~meet[i0]).sum()); ordered_pairs = nL * n_disjoint
N5 = len(sets) * ordered_pairs / 20
print("sets through fixed pair:", len(sets), "| candidates", len(cand), "| N5 =", N5, "(%.0fs)" % (time.time() - t), flush=True)
def inv(S):
    C = frozenset().union(*[lags[i] for i in S]); inside = [i for i, L in enumerate(lags) if L <= C]
    hist = Counter(len(lags[i] & C) for i in range(nL) if i not in S)
    parts = [0]
    def rec(rem, cand_):
        if not rem: parts[0] += 1; return
        p = min(rem)
        for i in cand_:
            if p in lags[i] and lags[i] <= rem: rec(rem - lags[i], [j for j in cand_ if not (lags[j] & lags[i])])
    rec(C, inside)
    return (len(inside), parts[0], min(hist), tuple(sorted(hist.items())))
types = {}
for S in sets:
    k = inv(S); types.setdefault(k, []).append(S)
print("invariant types:", len(types), flush=True)
X1 = np.array([[0, 1], [1, 0]]); Z1 = np.diag([1, -1])
def pauli(v):
    M = np.eye(1)
    for i in range(n):
        x = (v >> i) & 1; z = (v >> (n + i)) & 1
        M = np.kron(M, (1j) ** (x * z) * np.linalg.matrix_power(X1, x) @ np.linalg.matrix_power(Z1, z))
    return M
rows = []
for k, lst in types.items():
    S = lst[0]; C = frozenset().union(*[lags[i] for i in S]); U = [x for x in range(1, NV) if x not in C]
    E = [(a, b) for a, b in itertools.combinations(range(len(U)), 2) if w(U[a], U[b]) == 1]
    X = cp.Variable((len(U), len(U)), symmetric=True)
    pr = cp.Problem(cp.Maximize(cp.sum(X)), [X >> 0, cp.trace(X) == 1] + [X[a, b] == 0 for a, b in E]); pr.solve(solver=cp.SCS, eps=1e-6, max_iters=30000)
    Ps = np.array([pauli(v) for v in C])
    def fg(z):
        v = z[:d] + 1j * z[d:]; nv = np.vdot(v, v).real
        Pv = Ps @ v; f = np.einsum("i,ki->k", v.conj(), Pv).real
        g = float(np.sum(f ** 2)) / d
        gr = (4 * np.einsum("ki,k->i", Pv, f) / d) / nv ** 2 - 4 * g * v / nv ** 3
        return g / nv ** 2, np.concatenate([gr.real, gr.imag])
    rng = np.random.default_rng(1)
    fmin = min(minimize(fg, rng.standard_normal(2 * d), jac=True, method="L-BFGS-B", options=dict(gtol=1e-13, maxiter=10000)).fun for _ in range(80))
    row = dict(n_inside=k[0], n_partitions=k[1], m_star=k[2], count_through_pair=len(lst), example=list(S), theta=float(pr.value), numeric_min_F=float(fmin), stabiliser_value=k[2] / 16)
    rows.append(row); print({kk: vv for kk, vv in row.items() if kk != "example"}, flush=True)
json.dump(dict(sets_through_pair=len(sets), N5=N5, n_types=len(types), types=rows), open(os.path.join(ROOT, "data", "w33_four_qubit_size5_census.json"), "w"), indent=1)
