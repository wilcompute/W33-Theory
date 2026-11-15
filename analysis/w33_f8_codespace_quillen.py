"""Pass 12672: Quillen / Catlin-D'Angelo (Hermitian Polya) lower bounds for the F_8 regulus objective on the code space of the
rank-3 Pauli group T (dim 8) of Pass 12671 (and the rank-2 group S, dim 16).
On the code space, g(t) = 64 F(Bt) |t|^4-normalised is the bihomogeneous Hermitian quartic g = sum_j 64 |u_j.t|^4 - 9 |t|^4.
A bihomogeneous (d,d) form has a UNIQUE Hermitian coefficient matrix C on degree-d monomials (C[alpha,beta] = coefficient of
conj(t^alpha) t^beta).  For k >= 0:  c_k := max{c : |t|^{2k} (g - c |t|^4) is a Hermitian SOS} = lambda_min(D^{-1/2} C_k D^{-1/2}),
D = diag((k+2)!/alpha!) the matrix of |t|^{2(k+2)}.  c_k <= min g (each is a valid lower bound up to floating-point eigenvalue
accuracy) and c_k -> min g as k -> infinity (Quillen 1968, Catlin-D'Angelo 1996: strictly positive forms become SOS after
multiplication by a power of |t|^2).  usage: py -3 analysis/w33_f8_codespace_quillen.py [rank] [kmax]"""
import itertools, json, math, os, sys, time
from math import factorial
import numpy as np
import scipy.sparse as sps
import scipy.sparse.linalg as spl
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_regulus_constants_q16_q32.py"), encoding="utf-8").read()
gl = {"__name__": "x", "__file__": os.path.join(HERE, "w33_regulus_constants_q16_q32.py")}
exec(src[: src.index("def model(")], gl)
q, mul, trace = gl["field"](3)
RANK = int(sys.argv[1]) if len(sys.argv) > 1 else 3
KMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 5
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
Wm = np.vstack([Ut @ B for Ut in U])   # <b_j, B t> = Wm[j] @ t  (u_j = Wm[j])


def multis(d):
    return [a for a in itertools.product(range(d + 1), repeat=n) if sum(a) == d] if n <= 8 else None


def multis_fast(d):
    out = []
    def rec(i, left, cur):
        if i == n - 1: out.append(tuple(cur + [left])); return
        for v in range(left, -1, -1): rec(i + 1, left - v, cur + [v])
    rec(0, d, []); return out


mf = lambda a: math.prod(factorial(v) for v in a)
G2 = multis_fast(2); idx2 = {g: i for i, g in enumerate(G2)}
cg = np.array([2 / mf(g) for g in G2])
# a_j[gamma] = c_gamma u_j^gamma ;  |u.t|^4 = sum conj(a_j[g']) a_j[g] conj(t^g') t^g
A = np.array([[cg[i] * np.prod([Wm[j, k] ** g[k] for k in range(n)]) for i, g in enumerate(G2)] for j in range(Wm.shape[0])])
S = 64 * (A.conj().T @ A) - 9 * np.diag(cg)
# check S against direct evaluation
t_ = np.random.default_rng(1).standard_normal(n) + 1j * np.random.default_rng(2).standard_normal(n)
mon = np.array([np.prod(t_ ** np.array(g)) for g in G2])
direct = 64 * np.sum(np.abs(Wm @ t_) ** 4) - 9 * np.linalg.norm(t_) ** 4
assert abs(np.real(mon.conj() @ S @ mon) - direct) < 1e-8 * abs(direct)
res = dict(rank=RANK, code_dim=n, c8=C8, bounds=[])
for k in range(KMAX + 1):
    t0 = time.time(); d = k + 2
    Gd = multis_fast(d); idxd = {g: i for i, g in enumerate(Gd)}; Dk = multis_fast(k)
    rows, cols, vals = [], [], []
    Si, Sj = np.nonzero(np.abs(S) > 1e-14)
    for dl in Dk:
        w = factorial(k) / mf(dl)
        sh = [idxd[tuple(a + b for a, b in zip(G2[i], dl))] for i in range(len(G2))]
        rows.extend(sh[i] for i in Si); cols.extend(sh[j] for j in Sj); vals.extend(w * S[Si, Sj])
    C = sps.csr_matrix((vals, (rows, cols)), shape=(len(Gd), len(Gd)))
    dinv = np.array([1 / math.sqrt(factorial(d) / mf(a)) for a in Gd])
    Cn = sps.diags(dinv) @ C @ sps.diags(dinv); Cn = (Cn + Cn.conj().T) / 2
    if len(Gd) <= 4000: lam = float(np.linalg.eigvalsh(Cn.toarray())[0])
    else: lam = float(spl.eigsh(Cn, k=1, sigma=-20.0, which="LM", return_eigenvectors=False)[0])
    res["bounds"].append(dict(k=k, monomials=len(Gd), c_k=lam, seconds=round(time.time() - t0, 1)))
    print(f"rank {RANK} dim {n}  k={k}  monomials {len(Gd)}  c_k = {lam:.10f}   (c8 = {C8:.10f})  {time.time() - t0:.0f}s", flush=True)
    json.dump(res, open(os.path.join(ROOT, "data", f"w33_f8_codespace_quillen_rank{RANK}.json"), "w"), indent=1)
