"""Pass 12657: is the AG(2,4) inequality (*) of w33_typeB_affine_plane_inequality.py provable at the first real-SOS level?
Find the largest delta with   LHS(A) - delta (sum |A_p|^2)^2 = <A (x) A| M2 |A (x) A> + <A (x) conj A| M1 |A (x) conj A>,
M1, M2 >= 0 Hermitian 256 x 256 (a 'decomposable' / PSD + partial-transpose certificate; this is the general U(1)-invariant degree-4
real SOS).  delta* = 3/8 would prove min F = 1/16 for type B up to solver precision (exact rounding is a separate step).
Control: the same SDP for the two-qubit triple analogue is not needed (proved); as a sanity control the SDP with LHS replaced by
(sum |A|^2)^2 must return delta* = 1.  usage: py -3 analysis/w33_typeB_decomposable_certificate.py"""
import itertools, json, os, time
import numpy as np, scipy.sparse as sp, cvxpy as cp
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_typeB_affine_plane_inequality.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_typeB_affine_plane_inequality.py")}
exec(src[: src.index("# model F from the CZ construction")], g)
lines, pairings = g["lines"], g["pairings"]
n = 16; idx = lambda a, b, c, d: ((a * n + b) * n + c) * n + d
Kt = np.zeros(n ** 4); Kn = np.zeros(n ** 4)
for p in range(n):
    Kt[idx(p, p, p, p)] += 1
    for r in range(n):
        Kt[idx(p, p, r, r)] += 0.25; Kn[idx(p, r, p, r)] += 1
for l in lines:
    for (a, b), (c, d) in pairings(l):
        for (u, v, w, x) in ((a, b, a, b), (c, d, c, d), (a, b, c, d), (c, d, a, b)): Kt[idx(u, v, w, x)] += 1
# symmetriser over a<->b and c<->d ; reduce to canonical representatives a<=b, c<=d
canon = {}; rows = []; cols = []
for a, b, c, d in itertools.product(range(n), repeat=4):
    key = (min(a, b), max(a, b), min(c, d), max(c, d))
    rows.append(canon.setdefault(key, len(canon))); cols.append(idx(a, b, c, d))
S = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(len(canon), n ** 4))
# K1[a,b,c,d] = M1[(a,c),(d,b)]  (row index a*n+c, col index d*n+b); vec in C order of the 256x256 matrix
r1 = []; c1 = []
for a, b, c, d in itertools.product(range(n), repeat=4):
    r1.append(idx(a, b, c, d)); c1.append((a * n + c) * (n * n) + (d * n + b))
P1 = sp.csr_matrix((np.ones(len(r1)), (r1, c1)), shape=(n ** 4, n ** 4))
SP1 = (S @ P1).tocsr(); St = S @ Kt; Sn = S @ Kn


def solve(target, label):
    M1 = cp.Variable((n * n, n * n), hermitian=True); M2 = cp.Variable((n * n, n * n), hermitian=True); delta = cp.Variable()
    v1 = cp.reshape(M1, (n ** 4,), order="C"); v2 = cp.reshape(M2, (n ** 4,), order="C")
    cons = [M1 >> 0, M2 >> 0, S @ v2 + SP1 @ v1 == target - delta * Sn]
    prob = cp.Problem(cp.Maximize(delta), cons); t0 = time.time()
    prob.solve(solver=cp.SCS, eps=1e-6, max_iters=40000, verbose=False)
    r = dict(label=label, delta=float(delta.value), status=prob.status, seconds=round(time.time() - t0, 1))
    print(r, flush=True); return r


res = dict(control_norm_squared=solve(Sn, "control: LHS = norm^2 (expect 1)"), typeB=solve(St, "type B (target 3/8 = 0.375)"))
res["proves_three_eighths_numerically"] = bool(abs(res["typeB"]["delta"] - 0.375) < 1e-4)
json.dump(res, open(os.path.join(ROOT, "data", "w33_typeB_decomposable_certificate.json"), "w"), indent=1)
