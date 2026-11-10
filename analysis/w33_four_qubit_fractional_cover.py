"""Pass 12644: exact rational certificate sum_U <P>^2 <= 14 for the saved four-qubit size-9 set via a FRACTIONAL cover of the 120 uncovered
Paulis by pairwise-anticommuting sets K (sum_K w_K 1_K >= 1 pointwise, w >= 0):  sum_U <P>^2 <= sum_K w_K sum_{P in K} <P>^2 <= sum_K w_K.
Column generation: master LP (HiGHS), pricing = max-weight anticommuting set (ILP).  Then round w to rationals and verify coverage and
total EXACTLY with Fractions.  Consequence with m* = 1: min F = 1/16 exactly.
usage: py -3 analysis/w33_four_qubit_fractional_cover.py"""
import json, os, itertools, time, math
from fractions import Fraction as Fr
import numpy as np
from scipy.optimize import linprog, milp, LinearConstraint, Bounds
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ex = {"__name__": "x", "__file__": os.path.join(HERE, "w33_four_qubit_theta_exact.py")}
src = open(os.path.join(HERE, "w33_four_qubit_theta_exact.py"), encoding="utf-8").read()
exec(src[: src.index("rows, cols = []")], ex)
lags, w = ex["lags"], ex["w"]
sol = json.load(open(os.path.join(ROOT, "data", "w33_four_qubit_theta_exact.json")))["lines"]
C = frozenset().union(*[lags[i] for i in sol]); U = [x for x in range(1, 256) if x not in C]; n = len(U)
ANTI = np.array([[w(U[a], U[b]) == 1 for b in range(n)] for a in range(n)])
comm_pairs = [(a, b) for a, b in itertools.combinations(range(n), 2) if not ANTI[a, b]]
Apr = np.zeros((len(comm_pairs), n))
for k, (a, b) in enumerate(comm_pairs): Apr[k, a] = Apr[k, b] = 1
def greedy(order):
    K = []
    for v in order:
        if all(ANTI[v, u] for u in K): K.append(v)
    return frozenset(K)
rng = np.random.default_rng(0)
cols = {greedy(rng.permutation(n)) for _ in range(400)}
t0 = time.time()
for it in range(3000):
    cl = list(cols); M = np.zeros((n, len(cl)))
    for j, K in enumerate(cl): M[list(K), j] = 1
    lp = linprog(np.ones(len(cl)), A_ub=-M, b_ub=-np.ones(n), bounds=(0, None), method="highs")
    y = -lp.ineqlin.marginals
    pr = milp(-y, constraints=LinearConstraint(Apr, -np.inf, 1), integrality=np.ones(n), bounds=Bounds(0, 1))
    K = frozenset(np.where(pr.x > 0.5)[0]); val = y[list(K)].sum()
    if it % 10 == 0: print("iter", it, "LP", lp.fun, "best column reduced value", val, "columns", len(cols), flush=True)
    farley = lp.fun / max(val, 1.0)
    if val <= 1 + 1e-7: break
    cols.add(K)
    for _ in range(20):  # cheap extra columns: weighted greedy
        order = np.argsort(-(y + 0.05 * rng.random(n)))
        G = greedy(order)
        if y[list(G)].sum() > 1 + 1e-9: cols.add(G)
print("column generation done: LP =", lp.fun, "iterations", it, "%.0fs" % (time.time() - t0), flush=True)
wv = lp.x; supp = [j for j in range(len(cl)) if wv[j] > 1e-9]
res = dict(lp_value=float(lp.fun), farley_lower_bound=float(farley), n_columns=len(cl), support=len(supp), iterations=it)
# exact rounding: try denominators
best_total = None
for D in (1, 2, 3, 4, 6, 8, 12, 16, 24, 48, 120, 240, 720, 5040):
    wr = {j: Fr(math.ceil(wv[j] * D - 1e-12), D) for j in supp}
    cover = [sum((wr[j] for j in supp if v in cl[j]), Fr(0)) for v in range(n)]
    total = sum(wr.values(), Fr(0))
    if min(cover) >= 1 and total < 15:
        res.update(exact=True, denominator=D, total=str(total), min_cover=str(min(cover)),
                   all_sets_anticommuting=all(ANTI[a, b] for j in supp for a, b in itertools.combinations(sorted(cl[j]), 2)),
                   weights=[[str(wr[j]), [U[v] for v in sorted(cl[j])]] for j in supp if wr[j] > 0],
                   conclusion=("exact: sum_U <P>^2 <= %s, so F >= (15 - %s)/16 |v|^4 = %s |v|^4 (strongly unextendible)" % (total, total, (15 - total) / 16)) + ("; tight (min F = 1/16)" if total == 14 else "; not tight (min F = 1/16 numerically)"))
        break
else:
    res.update(exact=False)
print({k: v for k, v in res.items() if k != "weights"}, flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_four_qubit_fractional_cover.json"), "w"), indent=1)
