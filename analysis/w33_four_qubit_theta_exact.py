"""Pass 12644: the four-qubit size-9 set: lines, spectrum and Hoffman bound (exact dual: w33_four_qubit_theta_dual.py); was: exact certificate theta <= 14 for the four-qubit size-9 set (uncovered anticommutation graph, 120 vertices, 56-regular).
Rebuild the ILP solution deterministically from data/w33_four_qubit_rung.json is not possible (lines not saved), so re-solve with the
same model and a 'first feasible size-9' stop, then: exact integer spectrum (sympy charpoly factor), Lovasz/Hoffman bound
theta <= n(-lmin)/(k - lmin); if that is not 14, an exact dual from the coherent closure.
usage: py -3 analysis/w33_four_qubit_theta_exact.py"""
import itertools, json, os, time
import numpy as np, sympy as sp
from fractions import Fraction as Fr
from scipy.optimize import milp, LinearConstraint, Bounds
import scipy.sparse as sps
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
n = 4; d = 16; NV = 256
pc = lambda x: bin(x).count("1")
def w(x, y):
    lo = 15
    return (pc((x & lo) & (y >> n)) + pc((x >> n) & (y & lo))) % 2
L0 = frozenset(range(1, 16)); seen = {L0}; stack = [L0]
while stack:
    L = stack.pop()
    for u in range(1, NV):
        M = frozenset(x ^ (u if w(x, u) else 0) for x in L)
        if M not in seen: seen.add(M); stack.append(M)
lags = sorted(seen, key=lambda s: sorted(s)); nL = len(lags)
rows, cols = [], []
for i, L in enumerate(lags):
    for x in L: rows.append(x - 1); cols.append(i)
Apt = sps.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(NV - 1, nL)); Amax = sps.csr_matrix(((Apt.T @ Apt) > 0).astype(float))
r = milp(np.ones(nL), constraints=[LinearConstraint(Apt, 0, 1), LinearConstraint(Amax, 1, np.inf), LinearConstraint(np.ones((1, nL)), 9, 9)],
         integrality=np.ones(nL), bounds=Bounds(0, 1), options=dict(time_limit=1500))
sol = [i for i in range(nL) if r.x[i] > 0.5]
C = frozenset().union(*[lags[i] for i in sol]); U = [x for x in range(1, NV) if x not in C]
An = np.array([[1 if w(U[a], U[b]) == 1 else 0 for b in range(len(U))] for a in range(len(U))])
ev = np.linalg.eigvalsh(An.astype(float))
vals, mult = np.unique(np.round(ev, 6), return_counts=True)
k = int(round(ev[-1])); lmin = float(ev[0])
res = dict(size=len(sol), lines=sol, n_uncovered=len(U), degree=k, spectrum={str(v): int(m) for v, m in zip(vals, mult)},
           lambda_min=lmin, hoffman_bound=len(U) * (-lmin) / (k - lmin))
print(res)
json.dump(res, open(os.path.join(ROOT, "data", "w33_four_qubit_theta_exact.json"), "w"), indent=1, default=str)
