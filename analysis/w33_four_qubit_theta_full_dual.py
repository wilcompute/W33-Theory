"""Pass 12644: full (unreduced) Lovasz dual for the saved four-qubit set: min t s.t. t I - (J + T) >= 0, T symmetric supported on
anticommuting pairs.  Solve to high accuracy (Clarabel), try rational rounding of T (several denominators), and check 14 I - (J + T)
PSD EXACTLY (Fraction LDL^T).  Success => theta <= 14 => min F = 1/16 exactly (m* = 1).
usage: py -3 analysis/w33_four_qubit_theta_full_dual.py"""
import json, os, itertools
from fractions import Fraction as Fr
import numpy as np, cvxpy as cp
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ex = {"__name__": "x", "__file__": os.path.join(HERE, "w33_four_qubit_theta_exact.py")}
src = open(os.path.join(HERE, "w33_four_qubit_theta_exact.py"), encoding="utf-8").read()
exec(src[: src.index("rows, cols = []")], ex)
lags, w = ex["lags"], ex["w"]
sol = json.load(open(os.path.join(ROOT, "data", "w33_four_qubit_theta_exact.json")))["lines"]
C = frozenset().union(*[lags[i] for i in sol]); U = [x for x in range(1, 256) if x not in C]; n = len(U)
E = [(a, b) for a, b in itertools.combinations(range(n), 2) if w(U[a], U[b]) == 1]
yv = cp.Variable(len(E)); t = cp.Variable()
import scipy.sparse as sps
rows = [a for a, b in E] + [b for a, b in E]; colsI = [b for a, b in E] + [a for a, b in E]
Tm = sum(yv[k] * sps.csr_matrix(([1.0, 1.0], ([E[k][0], E[k][1]], [E[k][1], E[k][0]])), shape=(n, n)) for k in range(len(E))) if False else None
# build T via reshape of a sparse linear map
L = sps.csr_matrix((np.ones(2 * len(E)), ([a * n + b for a, b in E] + [b * n + a for a, b in E], list(range(len(E))) * 2)), shape=(n * n, len(E)))
T = cp.reshape(L @ yv, (n, n), order="C")
prob = cp.Problem(cp.Minimize(t), [t * np.eye(n) - np.ones((n, n)) - T >> 0])
prob.solve(solver=cp.CLARABEL)
print("full dual t =", t.value, flush=True)
def psd_exact(M):
    M = [row[:] for row in M]; m = len(M)
    for i in range(m):
        if M[i][i] < 0: return False, i
        if M[i][i] == 0:
            if any(M[i][j] != 0 for j in range(i + 1, m)): return False, i
            continue
        for j in range(i + 1, m):
            if M[j][i] != 0:
                f = M[j][i] / M[i][i]
                for k in range(i, m): M[j][k] -= f * M[i][k]
    return True, None
res = dict(t=float(t.value), n_edges=len(E), attempts=[])
ys = yv.value
for D in (1, 2, 4, 7, 8, 14, 16, 28, 56, 112):
    yr = [Fr(round(v * D), D) for v in ys]
    Mx = [[Fr(14 if i == j else 0) - 1 for j in range(n)] for i in range(n)]
    for k, (a, b) in enumerate(E):
        Mx[a][b] -= yr[k]; Mx[b][a] -= yr[k]
    ok, fail = psd_exact(Mx)
    mn = float(np.linalg.eigvalsh(np.array([[float(x) for x in r] for r in Mx]))[0])
    res["attempts"].append(dict(D=D, exact_psd=ok, min_eig_float=mn))
    print("D", D, "exact PSD", ok, "min eig", mn, flush=True)
    if ok:
        res.update(certified=True, denominator=D, conclusion="theta <= 14 exactly => min F = 1/16 exactly")
        break
else:
    res["certified"] = False
json.dump(res, open(os.path.join(ROOT, "data", "w33_four_qubit_theta_full_dual.json"), "w"), indent=1)
# ---- epsilon-relaxed exact certificate: (14 + delta) I - Y >= 0 exactly with rounded rational Y
res["relaxed"] = []
for D, delta in ((112, Fr(1, 400)), (256, Fr(1, 1000)), (512, Fr(1, 2000))):
    yr = [Fr(round(v * D), D) for v in ys]
    Mx = [[Fr(14 if i == j else 0) + (delta if i == j else 0) - 1 for j in range(n)] for i in range(n)]
    for k, (a, b) in enumerate(E):
        Mx[a][b] -= yr[k]; Mx[b][a] -= yr[k]
    ok, _ = psd_exact(Mx)
    row = dict(D=D, delta=str(delta), exact_psd=ok, theta_upper=str(14 + delta), F_lower=str((1 - delta) / 16), F_lower_float=float((1 - delta) / 16))
    res["relaxed"].append(row); print(row, flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_four_qubit_theta_full_dual.json"), "w"), indent=1)
