"""Pass 12643 item 1: exact strong-unextendibility bounds for QUBIT Pauli MUB sets from the Lovasz theta of the uncovered
anticommutation graph.
For n qubits, d = 2^n, pure states satisfy sum_{all 4^n - 1 Paulis} <P>^2 = d - 1, and the twirl identity gives
F(v) = (1/d) sum_{covered P} <P>^2 = (d - 1 - sum_{P in U} <P>^2) / d,   U = uncovered points.
Uncertainty relation (de Gois-Hansenne-Guehne 2023; Xu-Schwonnek-Winter 2023): for +-1-valued observables with anticommutation graph G
(edge = anticommuting pair), sum <A_i>^2 <= theta(G) (Lovasz theta).  Lower side: alpha(G) (a commuting set, realised by a stabiliser
state) is attained.  So  (d - 1 - theta(G))/d <= min F <= (d - 1 - alpha(G))/d,  and if theta = alpha the minimum is exact.
Compute theta (SDP, cvxpy) and alpha (exact, networkx/ILP) for: two qubits size 3 (control: min F = 1/4), three qubits size 5 (1/8),
three qubits size 9 (the other class).  Also report vertex-transitivity data for an exact value (theta(G) theta(Gbar) = n if G is
vertex-transitive).
usage: py -3 analysis/w33_lovasz_theta_unextendible.py"""
import json, os, contextlib, io, itertools
import numpy as np, cvxpy as cp
from scipy.optimize import milp, LinearConstraint, Bounds
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
cs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_strong_umub_census.py")}
_src = open(os.path.join(HERE, "w33_strong_umub_census.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src[: _src.index("\nres = {}")], cs)
def theta(n, edges):
    X = cp.Variable((n, n), symmetric=True)
    cons = [X >> 0, cp.trace(X) == 1] + [X[i, j] == 0 for i, j in edges]
    pr = cp.Problem(cp.Maximize(cp.sum(X)), cons); pr.solve(solver=cp.CLARABEL)
    return float(pr.value)
def alpha(n, edges):
    A = np.zeros((len(edges), n))
    for k, (i, j) in enumerate(edges): A[k, i] = A[k, j] = 1
    r = milp(-np.ones(n), constraints=LinearConstraint(A, -np.inf, 1), integrality=np.ones(n), bounds=Bounds(0, 1))
    return int(round(-r.fun))
res = {}
for (p, nq, size, known) in [(2, 2, 3, 0.25), (2, 3, 5, 0.125)]:  # size-9 sets are complete MUB sets (nothing uncovered)
    pts, lag, w = cs["geometry"](p, nq); mps, _ = cs["maximal_partial_spreads"](lag)
    S = next(sorted(S) for S in mps if len(S) == size)
    cov = frozenset().union(*[lag[L] for L in S]); U = [i for i in range(len(pts)) if i not in cov]
    E = [(a, b) for a, b in itertools.combinations(range(len(U)), 2) if w(pts[U[a]], pts[U[b]]) == 1]
    Ec = [(a, b) for a, b in itertools.combinations(range(len(U)), 2) if w(pts[U[a]], pts[U[b]]) == 0]
    d = 2 ** nq; th = theta(len(U), E); thc = theta(len(U), Ec); al = alpha(len(U), E)
    deg = sorted(set(sum(1 for e in E if i in e) for i in range(len(U))))
    row = dict(d=d, size=size, n_uncovered=len(U), anticommutation_degrees=deg, theta=th, theta_complement=thc, theta_product=th * thc,
               alpha=al, lower_bound_minF=(d - 1 - th) / d, upper_bound_minF=(d - 1 - al) / d, known_min_F=known)
    res["p%d_n%d_size%d" % (p, nq, size)] = row
    print(row, flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_lovasz_theta_unextendible.json"), "w"), indent=1)
