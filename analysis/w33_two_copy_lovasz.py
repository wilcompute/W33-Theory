"""Pass 12646 item 1: a two-copy Lovasz bound for the three-qubit size-5 sets.
de Gois-Hansenne-Guehne holds for every state, in particular psi (x) psi.  For the 784 dichotomic observables P (x) Q (P, Q in U):
  sum_{P,Q} <psi psi| P(x)Q |psi psi>^2 = (sum_U <P>^2)^2 <= theta(G2),
G2: (P,Q) ~ (P',Q') iff P(x)Q and P'(x)Q' anticommute iff exactly one of (P,P'), (Q,Q') anticommutes.  If theta(G2) <= 36 then
sum_U <P>^2 <= 6 and min F = 1/8.  Any dual Y = J + T (T on edges of G2) gives theta(G2) <= lambda_max(Y).
(a) 4-parameter family T = a A(x)I + b A(x)N + c I(x)A + e N(x)A (N = commuting, non-identity); (b) the coherent-closure family
T = sum y_ij B_i (x) B_j over edge pairs (SDP); (c) primal lower bound: alpha(G)^2 = 36 always (products of stabiliser states).
Control: two qubits (theta(G) = 2) must give theta(G2) <= 4.
usage: py -3 analysis/w33_two_copy_lovasz.py"""
import json, os, contextlib, io, itertools
import numpy as np, cvxpy as cp
import scipy.sparse as sps
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
cs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_strong_umub_census.py")}
_src = open(os.path.join(HERE, "w33_strong_umub_census.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src[: _src.index(chr(10) + "res = {}")], cs)
def graph(nq, size):
    pts, lag, w = cs["geometry"](2, nq); mps, _ = cs["maximal_partial_spreads"](lag)
    S = next(sorted(S) for S in mps if len(S) == size); cov = frozenset().union(*[lag[L] for L in S]); U = [i for i in range(len(pts)) if i not in cov]
    A = np.array([[1.0 if w(pts[U[a]], pts[U[b]]) == 1 else 0.0 for b in range(len(U))] for a in range(len(U))])
    return A
def four_param(A):
    n = len(A); I = np.eye(n); N = np.ones((n, n)) - I - A; J2 = np.ones((n * n, n * n))
    mats = [np.kron(A, I), np.kron(A, N), np.kron(I, A), np.kron(N, A)]
    f = lambda x: np.linalg.eigvalsh(J2 + sum(xi * M for xi, M in zip(x, mats)))[-1]
    best = min((minimize(f, np.random.default_rng(k).standard_normal(4), method="Nelder-Mead", options=dict(maxiter=4000, xatol=1e-10, fatol=1e-12)) for k in range(6)), key=lambda r: r.fun)
    return float(best.fun), [float(v) for v in best.x]
def closure_classes(A):
    n = len(A); col = np.where(np.eye(n, dtype=bool), 2, A.astype(int))
    while True:
        cls = np.unique(col); Bs = {c: (col == c).astype(np.int64) for c in cls}
        keys = [col] + [Bs[a] @ Bs[b] for a in cls for b in cls]
        _, new = np.unique(np.stack(keys, -1).reshape(n * n, -1), axis=0, return_inverse=True); new = new.reshape(n, n)
        if len(np.unique(new)) == len(cls): return new
        col = new
def closure_dual(A):
    n = len(A); col = closure_classes(A); cls = np.unique(col)
    edge = {c for c in cls if A[col == c].max() > 0}
    terms = []
    for ci in cls:
        for cj in cls:
            if (ci in edge) != (cj in edge):  # exactly one coordinate anticommutes
                terms.append(sps.kron(sps.csr_matrix((col == ci).astype(float)), sps.csr_matrix((col == cj).astype(float)), format="csr"))
    # symmetrise variable structure: Y must be symmetric; pair each term with its transpose by symmetrising the matrix
    y = cp.Variable(len(terms)); t = cp.Variable()
    Msum = sum(y[k] * ((terms[k] + terms[k].T) / 2) for k in range(len(terms)))
    pr = cp.Problem(cp.Minimize(t), [t * np.eye(n * n) - np.ones((n * n, n * n)) - Msum >> 0]); pr.solve(solver=cp.SCS, eps=1e-7, max_iters=20000)
    return float(t.value), len(terms), int(len(cls))
res = {}
for nq, size, label in [(2, 3, "two_qubits_control"), (3, 5, "three_qubits")]:
    A = graph(nq, size)
    v4, x4 = four_param(A)
    res[label] = dict(n_U=len(A), four_param_bound=v4, four_param_x=x4); print(label, res[label], flush=True)
    vc, nt, ncl = closure_dual(A)
    res[label].update(closure_dual_bound=vc, closure_terms=nt, closure_rank=ncl, sqrt_bound=vc ** 0.5, minF_lower=(2 ** nq - 1 - vc ** 0.5) / 2 ** nq)
    print(label, res[label], flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_two_copy_lovasz.json"), "w"), indent=1)
