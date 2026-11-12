"""Pass 12647: the size-5 maximal partial spread of W(7,2) (Grassl/Kantor size q^{n/2}+1; found by ILP, data/w33_four_qubit_small_sizes.json):
exact strong unextendibility via an epsilon-relaxed Lovasz dual.  theta(U-graph) ~ 14.78 < 15, so (theta + delta) I - Y >= 0 exactly with
target T < 15 gives F >= (15 - T)/16 |v|^4 exactly; numerical min F ~ 0.0524 (below the stabiliser value 1/16: non-stabiliser optimum).
usage: py -3 analysis/w33_four_qubit_size5_exact.py"""
import json, os, itertools
from fractions import Fraction as Fr
import numpy as np, cvxpy as cp
import scipy.sparse as sps
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ex = {"__name__": "x", "__file__": os.path.join(HERE, "w33_four_qubit_theta_exact.py")}
src = open(os.path.join(HERE, "w33_four_qubit_theta_exact.py"), encoding="utf-8").read()
exec(src[: src.index("rows, cols = []")], ex)
lags, w = ex["lags"], ex["w"]
_f = os.path.join(ROOT, "data", "w33_four_qubit_small_sizes.json")
sol = json.load(open(_f))["k5"]["lines"] if os.path.exists(_f) else [129, 190, 287, 444, 530]  # ILP output (logged), re-verified below
C = frozenset().union(*[lags[i] for i in sol]); assert len(C) == 75 and all(len(L & C) > 0 for L in lags)
U = [x for x in range(1, 256) if x not in C]; n = len(U)
E = [(a, b) for a, b in itertools.combinations(range(n), 2) if w(U[a], U[b]) == 1]
yv = cp.Variable(len(E)); t = cp.Variable()
Lm = sps.csr_matrix((np.ones(2 * len(E)), ([a * n + b for a, b in E] + [b * n + a for a, b in E], list(range(len(E))) * 2)), shape=(n * n, len(E)))
T = cp.reshape(Lm @ yv, (n, n), order="C")
pr = cp.Problem(cp.Minimize(t), [t * np.eye(n) - np.ones((n, n)) - T >> 0]); pr.solve(solver=cp.SCS, eps=1e-9, max_iters=200000)
print("theta upper (numerical dual) =", t.value, flush=True)
def psd_exact(M):
    M = [row[:] for row in M]; m = len(M)
    for i in range(m):
        if M[i][i] <= 0:
            if M[i][i] < 0 or any(M[i][j] != 0 for j in range(i + 1, m)): return False
            continue
        for j in range(i + 1, m):
            if M[j][i] != 0:
                f = M[j][i] / M[i][i]
                for k in range(i, m): M[j][k] -= f * M[i][k]
    return True
res = dict(lines=sol, n_uncovered=n, theta_numerical=float(t.value), attempts=[])
for D, target in ((4096, Fr(149, 10)), (16384, Fr(1485, 100)), (65536, Fr(148, 10))):
    yr = [Fr(round(v * D), D) for v in yv.value]
    M = [[(target if i == j else Fr(0)) - 1 for j in range(n)] for i in range(n)]
    for k, (a, b) in enumerate(E): M[a][b] -= yr[k]; M[b][a] -= yr[k]
    ok = psd_exact(M); res["attempts"].append(dict(D=D, target=str(target), exact_psd=ok, F_lower=str((15 - target) / 16)))
    print("D", D, "target", target, "exact PSD", ok, flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_four_qubit_size5_exact.json"), "w"), indent=1)
