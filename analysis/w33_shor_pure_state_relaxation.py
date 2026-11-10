"""Pass 12644 item 1: an SDP bound on max_{pure psi} sum_{P in U} <P>^2 that uses products, not just anticommutation.
n qubits, Hermitian Paulis P_a (a in F_2^{2n}), x_a = <psi|P_a|psi> (x_0 = 1).  rho = (1/d) sum_a x_a P_a is pure iff rho^2 = rho, i.e.
for every c:  sum_a Re(k_{a,a+c}) x_a x_{a+c} = d x_c,  where P_a P_b = k_{ab} P_{a+b}.  Shor lift: Z = [[1, x^T], [x, X]] >= 0 (index 0 =
identity), replace x_a x_b by X_ab -> linear constraints.  Valid extras: X_aa <= 1.  Maximise sum_{a in U} X_aa.
min F >= (d - 1 - bound)/d.  Controls: two qubits size 3 (true max 2, so bound must be >= 2), compare with theta (2) ;
three qubits size 5: true max 6, theta 4 + sqrt5.
usage: py -3 analysis/w33_shor_pure_state_relaxation.py"""
import itertools, json, os, contextlib, io, time
import numpy as np, cvxpy as cp
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
cs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_strong_umub_census.py")}
_src = open(os.path.join(HERE, "w33_strong_umub_census.py"), encoding="utf-8").read()
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src[: _src.index("\nres = {}")], cs)
X1 = np.array([[0, 1], [1, 0]]); Z1 = np.diag([1, -1])
def pauli(n, a):
    M = np.eye(1)
    for i in range(n):
        x, z = a[i], a[n + i]
        M = np.kron(M, (1j) ** (x * z) * np.linalg.matrix_power(X1, x) @ np.linalg.matrix_power(Z1, z))
    return M
def run(n, size, extra_cliques=False):
    d = 2 ** n
    pts, lag, w = cs["geometry"](2, n); mps, _ = cs["maximal_partial_spreads"](lag)
    S = next(sorted(S) for S in mps if len(S) == size); cov = frozenset().union(*[lag[L] for L in S])
    vecs = [tuple(v) for v in itertools.product(range(2), repeat=2 * n)]  # index 0 = identity
    vi = {v: i for i, v in enumerate(vecs)}; N = len(vecs)
    Ps = [pauli(n, v) for v in vecs]
    U = [vi[pts[i]] for i in range(len(pts)) if i not in cov]
    Z = cp.Variable((N, N), symmetric=True)
    cons = [Z >> 0, Z[0, 0] == 1] + [Z[a, a] <= 1 for a in range(1, N)]
    for c in range(N):
        terms = []
        for a in range(N):
            b = vi[tuple((x + y) % 2 for x, y in zip(vecs[a], vecs[c]))]
            k = np.trace(Ps[a] @ Ps[b] @ Ps[c].conj().T) / d  # P_a P_b = k P_c
            if abs(k.real) > 0.5:
                terms.append(k.real * Z[a, b])
        cons.append(sum(terms) == d * Z[0, c])
    if extra_cliques:
        # rho >= 0: M_ab = <P_a P_b> = k_ab x_{a+b}  (Hermitian, linear in x = Z[0, :])
        Mr = [[None] * N for _ in range(N)]; Mi = [[None] * N for _ in range(N)]
        rows_r, rows_i = [], []
        for a in range(N):
            rr, ri = [], []
            for b in range(N):
                c = vi[tuple((x + y) % 2 for x, y in zip(vecs[a], vecs[b]))]
                k = np.trace(Ps[a] @ Ps[b] @ Ps[c].conj().T) / d
                rr.append(k.real * Z[0, c]); ri.append(k.imag * Z[0, c])
            rows_r.append(cp.hstack(rr)); rows_i.append(cp.hstack(ri))
        MR = cp.vstack(rows_r); MI = cp.vstack(rows_i)
        cons += [cp.bmat([[MR, -MI], [MI, MR]]) >> 0]
        for a, b in itertools.combinations(range(1, N), 2):
            k = np.trace(Ps[a] @ Ps[b] @ Ps[vi[tuple((x + y) % 2 for x, y in zip(vecs[a], vecs[b]))]].conj().T) / d
            if abs(k.imag) > 0.5:  # anticommuting
                cons.append(Z[a, a] + Z[b, b] <= 1)
    pr = cp.Problem(cp.Maximize(sum(Z[a, a] for a in U)), cons)
    t = time.time(); pr.solve(solver=cp.CLARABEL)
    val = float(pr.value)
    return dict(n=n, size=size, n_uncovered=len(U), shor_bound=val, minF_lower=(d - 1 - val) / d, seconds=time.time() - t, status=pr.status)
res = {}
for n, size in [(2, 3), (3, 5)]:
    for ex in (False, True):
        r = run(n, size, ex); res["n%d_size%d_%s" % (n, size, "strong" if ex else "plain")] = r; print(r, flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_shor_pure_state_relaxation.json"), "w"), indent=1)
