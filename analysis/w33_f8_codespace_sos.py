"""Pass 12672: degree-4 SOS lower bound for the F_8 regulus objective restricted to the 8-dim code space of the rank-3 Pauli group
T = <-iP(12,53), P(53,33), P(1,6)> (Pass 12671), and to the 16-dim code space of S = <-iP(12,53), P(53,33)> (Pass 12660/12671).
On a code space with orthonormal basis B, 64 F(Bt) = 64 sum_j |<w_j, t>|^4 - 9 |t|^4 with w_j = B^dagger b_j over the 576 basis
vectors b_j of the nine MUBs.  In real coordinates x (t = x1 + i x2) |<w,t>|^2 = x^T Q_w x, so 64F = sum_j 64 (x^T Q_j x)^2 - 9 (x^T x)^2.
SOS: maximise c such that 64F - c (x^T x)^2 = m(x)^T G m(x), G PSD, m = degree-2 monomials.  A bound c_SOS <= min over the code space;
c_SOS = c8 would certify (numerically) that the code-space minimum is exactly the Pass 12671 value.
usage: py -3 analysis/w33_f8_codespace_sos.py [rank]   (rank 3 -> 8-dim, rank 2 -> 16-dim)"""
import itertools, json, math, os, sys, time
import numpy as np
import cvxpy as cp
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_regulus_constants_q16_q32.py"), encoding="utf-8").read()
gl = {"__name__": "x", "__file__": os.path.join(HERE, "w33_regulus_constants_q16_q32.py")}
exec(src[: src.index("def model(")], gl)
q, mul, trace = gl["field"](3)
RANK = int(sys.argv[1]) if len(sys.argv) > 1 else 3
C8 = (47 - 32 * math.cos(2 * math.pi / 9)) / 9
pc = lambda n: bin(n).count("1") & 1


def pauli(u, v):
    M = np.zeros((64, 64), complex)
    for x in range(64): M[x, x ^ u] = (-1) ** pc(v & (x ^ u))
    return M


H = [-1j * pauli(12, 53), pauli(53, 33), pauli(1, 6)][:RANK]
Pr = np.eye(64, dtype=complex)
for X in H: Pr = Pr @ (np.eye(64) + X) / 2
w_, V = np.linalg.eigh((Pr + Pr.conj().T) / 2); B = V[:, w_ > 0.5]; n = B.shape[1]
Xi = np.array([[1 - 2 * trace(mul(a, b)) for b in range(8)] for a in range(8)], float)
Phi = np.array([[[1 - 2 * trace(mul(t, mul(a, b))) for b in range(8)] for a in range(8)] for t in range(8)], float)
U = [np.eye(64)]
for t in range(8):
    Ut = np.zeros((64, 64))
    for x in range(64):
        e = np.zeros((8, 8)); e.flat[x] = 1; Ut[:, x] = (Xi @ (e * Phi[t]) @ Xi / 8).ravel()
    U.append(Ut)
W = np.vstack([Ut @ B for Ut in U])          # rows: <b_j| B, so <b_j, B t> = W[j] @ t
N = 2 * n
# |W_j t|^2 = x^T Q_j x with x = (Re t, Im t): W_j t = (a + i b)(x1 + i x2)
Qs = []
for row in W:
    a, b = row.real, row.imag
    re = np.concatenate([a, -b]); im = np.concatenate([b, a])
    Qs.append(np.outer(re, re) + np.outer(im, im))
# quartic coefficient dictionary of 64 sum (x^T Q x)^2 - c (x^T x)^2 ; build K = 64 sum vec(Q) vec(Q)^T  as a 4-tensor, symmetrise via monomials
mons2 = [(i, j) for i in range(N) for j in range(i, N)]; idx2 = {m: k for k, m in enumerate(mons2)}
mons4 = {}
def m4(key):
    key = tuple(sorted(key))
    if key not in mons4: mons4[key] = len(mons4)
    return mons4[key]
for k1, (i, j) in enumerate(mons2):
    for k2, (k, l) in enumerate(mons2):
        if k2 >= k1: m4((i, j, k, l))
coef = np.zeros(len(mons4)); coefI = np.zeros(len(mons4))
Qstack = np.array(Qs)
T4 = 64 * np.einsum("nij,nkl->ijkl", Qstack, Qstack)
I = np.eye(N)
for (key, r) in mons4.items():
    # coefficient of the monomial in sum_{ijkl} T[i,j,k,l] x_i x_j x_k x_l = sum over distinct orderings
    perms = set(itertools.permutations(key))
    coef[r] = sum(T4[p] for p in perms) - 9 * sum(I[p[0], p[1]] * I[p[2], p[3]] for p in perms)
    coefI[r] = sum(I[p[0], p[1]] * I[p[2], p[3]] for p in perms)
G = cp.Variable((len(mons2), len(mons2)), symmetric=True); c = cp.Variable()
# m^T G m = sum_{k1,k2} G[k1,k2] x^{m1} x^{m2}; group by quartic monomial
rows = {r: [] for r in mons4.values()}
for k1, m1 in enumerate(mons2):
    for k2, m2 in enumerate(mons2):
        rows[mons4[tuple(sorted(m1 + m2))]].append((k1, k2))
import scipy.sparse as sps
data, ri, ci = [], [], []
L = len(mons2)
for r, lst in rows.items():
    for (k1, k2) in lst: ri.append(r); ci.append(k1 * L + k2); data.append(1.0)
Amat = sps.csr_matrix((data, (ri, ci)), shape=(len(mons4), L * L))
cons = [G >> 0, Amat @ cp.vec(G, order="C") == coef - c * coefI]
t0 = time.time()
prob = cp.Problem(cp.Maximize(c), cons)
prob.solve(solver="CLARABEL")
val = float(c.value)
eig = np.linalg.eigvalsh(G.value)
print(f"rank {RANK}: code-space dim {n}, SOS bound c_SOS = {val:.12f}  vs c8 = {C8:.12f}  gap {val - C8:.2e}; status {prob.status}; "
      f"min Gram eig {eig[0]:.2e}; {time.time() - t0:.0f}s", flush=True)
res = dict(rank=RANK, code_dim=n, c_sos=val, c8=C8, gap=val - C8, status=prob.status, gram_size=L, n_quartic=len(mons4), min_gram_eig=float(eig[0]))
json.dump(res, open(os.path.join(ROOT, "data", f"w33_f8_codespace_sos_rank{RANK}.json"), "w"), indent=1)
