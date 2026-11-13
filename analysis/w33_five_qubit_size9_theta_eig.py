"""Pass 12652 addendum: Lovasz theta of the 744-vertex anticommutation graph G on the uncovered Paulis of the five-qubit size-9 set,
by the eigenvalue formulation (Lovasz 1979, Thm 3): theta(G) = min lambda_max(A) over symmetric A with A_ii = 1 and A_ij = 1 whenever
i, j commute (non-adjacent in G); entries on anticommuting pairs are free.  EVERY feasible A is an upper-bound certificate, so this
gives a rigorous (floating-point) upper bound without an SDP solver.  Lower bound: alpha >= 30 (greedy commuting set).
The cvxpy/SCS run of w33_five_qubit_size9_theta.py did not finish in 7 h at eps 1e-7 and was stopped.
Method: A = J - E where E is supported on edges; start at the Hoffman point E = t*Adj (bound 31), then L-BFGS on the smoothed
lambda_max (log-sum-exp of eigenvalues, beta increasing).  Final certificate: the exact lambda_max of the returned A, plus a
symmetry-reduced (orbital) check.  usage: py -3 analysis/w33_five_qubit_size9_theta_eig.py"""
import json, os, time
import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
n = 5; pos = [(i, j) for i in range(n) for j in range(i, n)]
ex = json.load(open(os.path.join(ROOT, "data", "w33_five_qubit_size9_verify.json")))["example"]


def decode(code):
    S = np.zeros((n, n), int)
    for b, (i, j) in enumerate(pos):
        if code >> b & 1:
            S[i, j] = S[j, i] = 1
    return S


vec = lambda xv, zv: tuple(int(v) for v in xv) + tuple(int(v) for v in zv)
C = set()
for x in range(1, 1 << n):
    xv = np.array([(x >> i) & 1 for i in range(n)])
    C.add(vec(xv, [0] * n)); C.add(vec([0] * n, xv))
    for c in ex:
        C.add(vec(xv, decode(c) @ xv % 2))
allp = [tuple((v >> i) & 1 for i in range(2 * n)) for v in range(1, 1 << (2 * n))]
U = [p for p in allp if p not in C]
assert len(C) == 279 and len(U) == 744
Ua = np.array(U)
adj = (Ua[:, :n] @ Ua[:, n:].T + Ua[:, n:] @ Ua[:, :n].T) % 2
N = len(U)
ii, jj = np.nonzero(np.triu(adj, 1))
J = np.ones((N, N))


def build(e):
    A = J.copy()
    A[ii, jj] -= e; A[jj, ii] -= e
    return A


def smooth(e, beta):
    w, V = np.linalg.eigh(build(e))
    m = w[-1]; p = np.exp(beta * (w - m)); s = p.sum()
    f = m + np.log(s) / beta
    q = p / s
    # d f / d A = V diag(q) V^T ; dA/de_k = -(E_ij + E_ji)
    Gm = (V * q) @ V.T
    return f, -2 * Gm[ii, jj]


t0 = time.time()
lam_adj = np.linalg.eigvalsh(adj.astype(float))
t = 1.0 / (-lam_adj[0])  # Hoffman scaling: J - t*Adj; check its lambda_max
e = np.full(len(ii), N / (lam_adj[-1] - lam_adj[0]))
hoff = float(np.linalg.eigvalsh(build(e))[-1])
print("Hoffman-point lambda_max", hoff, flush=True)
hist = []
for beta in (5, 20, 80, 320, 1280, 5000):
    r = minimize(smooth, e, args=(beta,), jac=True, method="L-BFGS-B", options=dict(maxiter=600, maxcor=30))
    e = r.x
    lm = float(np.linalg.eigvalsh(build(e))[-1])
    hist.append(dict(beta=beta, lambda_max=lm, iters=int(r.nit), sec=round(time.time() - t0)))
    print(hist[-1], flush=True)
A = build(e)
w = np.linalg.eigvalsh(A)
res = dict(n_vertices=N, n_edges=int(len(ii)), hoffman_point=hoff, history=hist, theta_upper=float(w[-1]),
           top_eigs=[float(x) for x in w[-6:]], alpha_lower=30, e_stats=dict(min=float(e.min()), max=float(e.max()),
           distinct_rounded=int(len(np.unique(np.round(e, 4))))), seconds=round(time.time() - t0, 1))
np.save(os.path.join(ROOT, "data", "w33_five_qubit_size9_theta_eig_e.npy"), e) if False else None
print(res, flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_five_qubit_size9_theta_eig.json"), "w"), indent=1)
