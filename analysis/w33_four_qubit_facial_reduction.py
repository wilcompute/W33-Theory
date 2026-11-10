"""Pass 12645 item 1: EXACT theta <= 14 for the saved four-qubit size-9 set by facial reduction.
Maximum independent sets of the uncovered anticommutation graph (size 14) = Lagrangians meeting C in one point, minus that point (a
commuting set of 14 lies in a unique maximal isotropic 4-space).  Each gives a primal optimum X_S = 1_S 1_S^T / 14, so every optimal dual
Y = J + T must satisfy (14 I - Y) 1_S = 0, i.e. for i not in S: sum_{j in S, j~i} T_ij = -14 (i in S: automatic).
Impose these equalities, re-solve the dual, round the free variables, solve the pivot variables EXACTLY from the rref (so the kernel is
exact), and check 14 I - Y PSD by exact rational LDL^T (zero pivots must have zero rows).
Generalised (Pass 12646): optional argument = index into data/w33_four_qubit_set_census.json; alpha = 15 - m*, the alpha-sets are
the Lagrangians meeting C in m* points minus those points.
usage: py -3 analysis/w33_four_qubit_facial_reduction.py [census_index]"""
import json, os, itertools, sys
from fractions import Fraction as Fr
import numpy as np, cvxpy as cp, sympy as sp
import scipy.sparse as sps
from sympy.polys.matrices import DomainMatrix
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
ex = {"__name__": "x", "__file__": os.path.join(HERE, "w33_four_qubit_theta_exact.py")}
src = open(os.path.join(HERE, "w33_four_qubit_theta_exact.py"), encoding="utf-8").read()
exec(src[: src.index("rows, cols = []")], ex)
lags, w = ex["lags"], ex["w"]
if len(sys.argv) > 1:
    CI = int(sys.argv[1]); sol = json.load(open(os.path.join(ROOT, "data", "w33_four_qubit_set_census.json")))[CI]["lines"]
else:
    CI = None; sol = json.load(open(os.path.join(ROOT, "data", "w33_four_qubit_theta_exact.json")))["lines"]
C = frozenset().union(*[lags[i] for i in sol]); U = [x for x in range(1, 256) if x not in C]; n = len(U); ui = {x: i for i, x in enumerate(U)}
E = [(a, b) for a, b in itertools.combinations(range(n), 2) if w(U[a], U[b]) == 1]; ei = {e: k for k, e in enumerate(E)}
mstar = min(len(L & C) for i, L in enumerate(lags) if i not in sol); ALPHA = 15 - mstar
alpha_sets = [frozenset(ui[x] for x in L - C) for i, L in enumerate(lags) if i not in sol and len(L & C) == mstar]
assert all(len(S) == ALPHA for S in alpha_sets) and all(w(U[a], U[b]) == 0 for S in alpha_sets for a, b in itertools.combinations(S, 2))
rowsA, rhs = [], []
for S in alpha_sets:
    for i in range(n):
        if i in S: continue
        r = {}
        for j in S:
            e = (min(i, j), max(i, j))
            if e in ei: r[ei[e]] = 1
        rowsA.append(r); rhs.append(-ALPHA)
print("alpha sets:", len(alpha_sets), "| slackness equations:", len(rowsA), flush=True)
Asp = sps.lil_matrix((len(rowsA), len(E)))
for k, r in enumerate(rowsA):
    for c, v in r.items(): Asp[k, c] = v
Asp = Asp.tocsr()
yv = cp.Variable(len(E)); t = cp.Variable()
Lm = sps.csr_matrix((np.ones(2 * len(E)), ([a * n + b for a, b in E] + [b * n + a for a, b in E], list(range(len(E))) * 2)), shape=(n * n, len(E)))
T = cp.reshape(Lm @ yv, (n, n), order="C")
pr = cp.Problem(cp.Minimize(t), [t * np.eye(n) - np.ones((n, n)) - T >> 0, Asp @ yv == np.array(rhs, float)])
try:
    pr.solve(solver=cp.CLARABEL)
except cp.error.SolverError:
    print("Clarabel failed; SCS fallback", flush=True); pr.solve(solver=cp.SCS, eps=1e-10, max_iters=300000)
print("status", pr.status, flush=True)
print("reduced-face dual t =", t.value, flush=True)
# exact rref of the slackness system
Ad = DomainMatrix([[sp.QQ(r.get(c, 0)) for c in range(len(E))] + [sp.QQ(b)] for r, b in zip(rowsA, rhs)], (len(rowsA), len(E) + 1), sp.QQ)
R, piv = Ad.rref()
piv = [p for p in piv if p < len(E)]
Rl = R.to_list()
print("rank of slackness system:", len(piv), flush=True)
def psd_exact(M):
    M = [row[:] for row in M]; m = len(M)
    for i in range(m):
        if M[i][i] < 0: return False
        if M[i][i] == 0:
            if any(M[i][j] != 0 for j in range(i + 1, m)): return False
            continue
        for j in range(i + 1, m):
            if M[j][i] != 0:
                f = M[j][i] / M[i][i]
                for k in range(i, m): M[j][k] -= f * M[i][k]
    return True
res = dict(census_index=CI, lines=sorted(sol), m_star=mstar, alpha=ALPHA, n_alpha_sets=len(alpha_sets), n_equations=len(rowsA), rank=len(piv), t=float(t.value), attempts=[])
ys = yv.value; pivset = set(piv)
for D in (1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 4096, 16384, 65536, 262144):
    y = [Fr(round(v * D), D) for v in ys]
    for r_i, p in enumerate(piv):  # rref row r_i has leading 1 at column p
        row = Rl[r_i]
        val = Fr(row[-1].numerator, row[-1].denominator) if hasattr(row[-1], "numerator") else Fr(str(row[-1]))
        for c in range(len(E)):
            if c != p and c not in pivset and row[c] != 0:
                val -= Fr(str(row[c])) * y[c]
        y[p] = val
    # verify equations exactly
    eq_ok = all(sum((y[c] * v for c, v in r.items()), Fr(0)) == b for r, b in zip(rowsA, rhs))
    M = [[Fr(ALPHA if i == j else 0) - 1 for j in range(n)] for i in range(n)]
    for k, (a, b) in enumerate(E):
        M[a][b] -= y[k]; M[b][a] -= y[k]
    ok = eq_ok and psd_exact(M)
    mn = float(np.linalg.eigvalsh(np.array([[float(x) for x in r] for r in M]))[0])
    res["attempts"].append(dict(D=D, equations_exact=eq_ok, exact_psd=ok, min_eig_float=mn)); print("D", D, "eq", eq_ok, "PSD", ok, "min eig", mn, flush=True)
    if ok:
        res.update(certified=True, denominator=D, conclusion="theta <= %d EXACTLY => min F = %d/16 exactly (attained by stabiliser states, m* = %d)" % (ALPHA, mstar, mstar))
        break
else:
    res["certified"] = False
json.dump(res, open(os.path.join(ROOT, "data", "w33_four_qubit_facial_reduction%s.json" % ("" if CI is None else "_census%d" % CI)), "w"), indent=1)
