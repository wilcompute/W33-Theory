"""Pass 12644 item 4: the four-qubit rung (d = 16, W(7,2): 255 points, 2295 Lagrangian 4-spaces).
(a) Lagrangians = one orbit of a fixed Lagrangian under transvections t_u(x) = x + w(x,u) u.
(b) Smallest maximal partial spread by ILP (HiGHS): y_L binary, disjoint (each point <= 1), maximal (each Lagrangian meets the union),
    minimise size; report the size and solver status; also the size-9 = d/2+1 feasibility (Mandayam et al. conjecture).
(c) For the solution: uncovered set U, anticommutation graph, theta (SDP), alpha (ILP), the qubit bound (d-1-theta)/d <= min F and the
    numerical min F (L-BFGS over C^16) together with the stabiliser value m*/d.
usage: py -3 analysis/w33_four_qubit_rung.py"""
import itertools, json, os, time
from collections import Counter
import numpy as np, cvxpy as cp
from scipy.optimize import milp, LinearConstraint, Bounds, minimize
import scipy.sparse as sps
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
n = 4; d = 2 ** n; NV = 2 ** (2 * n)
pc = lambda x: bin(x).count("1")
def w(x, y):
    lo = (1 << n) - 1
    return (pc((x & lo) & (y >> n)) + pc((x >> n) & (y & lo))) % 2
pts = list(range(1, NV))
L0 = frozenset(v for v in range(1, NV) if v < (1 << n))  # span of X-type vectors: x-part only
assert all(w(a, b) == 0 for a in L0 for b in L0) and len(L0) == 2 ** n - 1
seen = {L0}; stack = [L0]
while stack:
    L = stack.pop()
    for u in pts:
        M = frozenset(x ^ (u if w(x, u) else 0) for x in L)
        if M not in seen: seen.add(M); stack.append(M)
lags = sorted(seen, key=lambda s: sorted(s)); nL = len(lags)
print("Lagrangians:", nL, flush=True)
res = dict(n_lagrangians=nL)
# ILP
rows, cols = [], []
for i, L in enumerate(lags):
    for x in L: rows.append(x - 1); cols.append(i)
Apt = sps.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(NV - 1, nL))
meet = (Apt.T @ Apt) > 0
Amax = sps.csr_matrix(meet.astype(float))
def solve(extra=None, tl=900):
    cons = [LinearConstraint(Apt, 0, 1), LinearConstraint(Amax, 1, np.inf)]
    if extra is not None: cons.append(extra)
    t = time.time()
    r = milp(np.ones(nL), constraints=cons, integrality=np.ones(nL), bounds=Bounds(0, 1), options=dict(time_limit=tl))
    return r, time.time() - t
r, el = solve()
sol = [i for i in range(nL) if r.x is not None and r.x[i] > 0.5]
res.update(min_size_found=len(sol), ilp_status=int(r.status), ilp_message=r.message, ilp_seconds=el, mip_dual_bound=float(getattr(r, "mip_dual_bound", float("nan")) or float("nan")))
print("smallest maximal partial spread found:", len(sol), "| status", r.status, r.message, "| dual bound", res["mip_dual_bound"], "| %.0fs" % el, flush=True)
C = frozenset().union(*[lags[i] for i in sol]); U = [x for x in pts if x not in C]
E = [(a, b) for a, b in itertools.combinations(range(len(U)), 2) if w(U[a], U[b]) == 1]
X = cp.Variable((len(U), len(U)), symmetric=True)
pr = cp.Problem(cp.Maximize(cp.sum(X)), [X >> 0, cp.trace(X) == 1] + [X[i, j] == 0 for i, j in E]); pr.solve(solver=cp.SCS, eps=1e-7, max_iters=50000)
th = float(pr.value)
A = np.zeros((len(E), len(U)))
for k, (i, j) in enumerate(E): A[k, i] = A[k, j] = 1
ra = milp(-np.ones(len(U)), constraints=LinearConstraint(A, -np.inf, 1), integrality=np.ones(len(U)), bounds=Bounds(0, 1), options=dict(time_limit=300))
al = int(round(-ra.fun))
mstar = min(len(L & C) for i, L in enumerate(lags) if i not in sol)
# numerical min F: F = (1/d) sum_{P in C} <P>^2
X1 = np.array([[0, 1], [1, 0]]); Z1 = np.diag([1, -1])
def pauli(v):
    M = np.eye(1)
    for i in range(n):
        x = (v >> i) & 1; z = (v >> (n + i)) & 1
        M = np.kron(M, (1j) ** (x * z) * np.linalg.matrix_power(X1, x) @ np.linalg.matrix_power(Z1, z))
    return M
Ps = np.array([pauli(v) for v in C])
def fg(z):
    v = z[:d] + 1j * z[d:]; nv = np.vdot(v, v).real
    Pv = Ps @ v; f = np.einsum("i,ki->k", v.conj(), Pv).real
    g = float(np.sum(f ** 2)) / d
    gr = (4 * np.einsum("ki,k->i", Pv, f) / d) / nv ** 2 - 4 * g * v / nv ** 3
    return g / nv ** 2, np.concatenate([gr.real, gr.imag])
rng = np.random.default_rng(0)
fmin = min(minimize(fg, rng.standard_normal(2 * d), jac=True, method="L-BFGS-B", options=dict(gtol=1e-12, maxiter=5000)).fun for _ in range(80))
res.update(n_uncovered=len(U), anticommutation_degrees=sorted(set(Counter(i for e in E for i in e).values())), theta=th, alpha=al,
           minF_lower_theta=(d - 1 - th) / d, stabiliser_value=mstar / d, m_star=mstar, numeric_min_F=float(fmin))
print({k: res[k] for k in ("n_uncovered", "anticommutation_degrees", "theta", "alpha", "minF_lower_theta", "stabiliser_value", "numeric_min_F")}, flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_four_qubit_rung.json"), "w"), indent=1, default=str)
