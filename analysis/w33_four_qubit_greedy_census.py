"""Pass 12647 item 1: test 'mirror partner <=> theta > alpha' on many four-qubit size-9 maximal partial spreads.  Randomised greedy
(random Lagrangian order, add when disjoint) yields maximal partial spreads; keep the size-9 ones, deduplicate, compute invariants
(Lagrangians inside C, number of partitions of C = 1 + mirror partners, m*) and theta (SCS) for up to 40 distinct sets.
usage: py -3 analysis/w33_four_qubit_greedy_census.py"""
import json, os, itertools, time
from collections import Counter
import numpy as np, cvxpy as cp
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ex = {"__name__": "x", "__file__": os.path.join(HERE, "w33_four_qubit_theta_exact.py")}
src = open(os.path.join(HERE, "w33_four_qubit_theta_exact.py"), encoding="utf-8").read()
exec(src[: src.index("rows, cols = []")], ex)
lags, w = ex["lags"], ex["w"]; nL = len(lags)
Inc = np.zeros((nL, 256), bool)
for i, L in enumerate(lags): Inc[i, list(L)] = True
meet = (Inc.astype(np.int32) @ Inc.T.astype(np.int32)) > 0
rng = np.random.default_rng(12647); sizes = Counter(); sets = {}
t = time.time()
while time.time() - t < 1500 and len(sets) < 400:
    avail = np.ones(nL, bool); chosen = []
    for i in rng.permutation(nL):
        if avail[i]:
            chosen.append(i); avail &= ~meet[i]
    sizes[len(chosen)] += 1
    if len(chosen) <= 9: sets[tuple(sorted(int(c) for c in chosen))] = True
print("greedy size distribution:", dict(sorted(sizes.items())), "| distinct size<=9:", len(sets), flush=True)
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
    return C, len(inside), parts[0], min(hist), tuple(sorted(hist.items()))
def theta(C):
    U = [x for x in range(1, 256) if x not in C]; n = len(U)
    E = [(a, b) for a, b in itertools.combinations(range(n), 2) if w(U[a], U[b]) == 1]
    X = cp.Variable((n, n), symmetric=True)
    pr = cp.Problem(cp.Maximize(cp.sum(X)), [X >> 0, cp.trace(X) == 1] + [X[a, b] == 0 for a, b in E]); pr.solve(solver=cp.SCS, eps=1e-7, max_iters=50000)
    return float(pr.value)
rows = []; seen_inv = {}
for sol in list(sets)[:400]:
    C, ni, parts, ms, hist = invariants(sol); hist = tuple((int(a), int(b)) for a, b in hist)
    key = (len(sol), ni, parts, ms, hist)
    if key in seen_inv: seen_inv[key]["count"] += 1; continue
    if len(seen_inv) >= 40: continue
    th = theta(C)
    row = dict(size=len(sol), lines=[int(c) for c in sol], n_inside=ni, n_partitions=parts, m_star=ms, theta=th, alpha=15 - ms, theta_gt_alpha=bool(th > 15 - ms + 1e-3), count=1)
    seen_inv[key] = row; rows.append(row); print({k: v for k, v in row.items() if k != "lines"}, flush=True)
    json.dump(dict(sizes=dict(sizes), classes=rows), open(os.path.join(ROOT, "data", "w33_four_qubit_greedy_census.json"), "w"), indent=1)
agree = sum(1 for r in rows if (r["n_partitions"] > 1) == r["theta_gt_alpha"])
summary = dict(n_classes=len(rows), mirror_iff_theta_gt_alpha_holds=agree, of=len(rows))
print(summary, flush=True)
json.dump(dict(sizes=dict(sizes), classes=rows, summary=summary), open(os.path.join(ROOT, "data", "w33_four_qubit_greedy_census.json"), "w"), indent=1)
