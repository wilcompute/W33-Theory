"""Pass 12658: (1) line-Fourier form of F for the F_q regulus sets: with B = row-wise F_q-Fourier transform of the amplitude matrix A,
        F + (q+1)/q^2 = sum over the q(q+1) affine lines l of AG(2,q) of || Fourier_l (B restricted to l) ||_4^4
    (all q+1 bases on the same footing: slope-t lines <-> basis B_t, vertical lines <-> the computational basis); checked q = 2, 4, 8.
(2) numerical min F of the F_8 regulus (six qubits, d = 64) in the CZ model (1/64 expected if it is 'stabiliser-optimal').
(3) Kantor's Lemma 6.1 quotient: project the nine F_8-regulus Lagrangians to p^perp/<p> for a point p with Tr Q(p) = 1 (non-singular
    for the F_2 quadratic form Tr Q that polarises to omega): is the image a maximal partial spread of W(9,2) (five qubits, size 9)?
    Invariants compared with the Pass 12650 set: number of F_2-quadrics vanishing on the covered set, and the spectrum multiset of the
    uncovered anticommutation graph.   usage: py -3 analysis/w33_regulus_f8_and_quotient.py"""
import itertools, json, os, time
from collections import Counter
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_regulus_mub_sets.py"), encoding="utf-8").read()
g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_regulus_mub_sets.py")}
exec(src[: src.index("res = {}; t0 = time.time()")], g)
field, regulus_codes, lags_from_codes, gs = g["field"], g["regulus_codes"], g["lags_from_codes"], g["gs"]
rng = np.random.default_rng(0); res = {}; t0 = time.time()


def model(k):
    q, mul, trace = field(k)
    Xi = np.array([[1 - 2 * trace(mul(a, b)) for b in range(q)] for a in range(q)], float)
    Phi = [np.array([[1 - 2 * trace(mul(t, mul(a, b))) for b in range(q)] for a in range(q)], float) for t in range(q)]
    def F(A):
        s = (np.abs(A) ** 4).sum()
        for t in range(q):
            K = Xi @ (A * Phi[t]) @ Xi / q; s += (np.abs(K) ** 4).sum()
        return float(s - (q + 1) / q ** 2)
    def line_form(A):
        B = A @ Xi / np.sqrt(q)  # row-wise Fourier in x2
        tot = 0.0
        for x1 in range(q):  # vertical lines x1 = const
            tot += (np.abs(Xi @ B[x1] / np.sqrt(q)) ** 4).sum()
        for t in range(q):
            for c in range(q):  # line y = c + t x1
                v = np.array([B[x1, c ^ mul(t, x1)] for x1 in range(q)])
                tot += (np.abs(Xi @ v / np.sqrt(q)) ** 4).sum()
        return float(tot - (q + 1) / q ** 2)
    return q, F, line_form


res["line_fourier_identity_residual"] = {}
for k in (1, 2, 3):
    q, F, lf = model(k); A = rng.standard_normal((q, q)) + 1j * rng.standard_normal((q, q)); A /= np.linalg.norm(A)
    res["line_fourier_identity_residual"][f"q{q}"] = abs(F(A) - lf(A))
print("line-Fourier identity residuals", res["line_fourier_identity_residual"], flush=True)
q, F8, _ = model(3)
def fobj(w):
    A = (w[:64] + 1j * w[64:]).reshape(8, 8); return F8(A / np.linalg.norm(A))
vals = sorted(minimize(fobj, rng.standard_normal(128), method="L-BFGS-B").fun for _ in range(8))
res["F8_regulus_min_F"] = vals[0]; res["F8_lowest"] = vals[:5]; res["F8_times_64"] = vals[0] * 64
print("F_8 regulus min F:", vals[:4], "x64 =", vals[0] * 64, round(time.time() - t0), "s", flush=True)
# (3) quotient
n = 6; N = 1 << (2 * n); lo = (1 << n) - 1
om = lambda a, b: (bin((a & lo) & (b >> n)).count("1") + bin((a >> n) & (b & lo)).count("1")) % 2
Q0 = lambda v: bin((v & lo) & (v >> n)).count("1") % 2
lags = lags_from_codes(6, list(regulus_codes(3).values()))
C6 = set().union(*lags) - {0}
assert all(Q0(v) == 0 for v in C6)  # the Lagrangians are totally singular for Tr Q = Q0
pos5, sing5, alt5, ns5 = gs["setup"](5)
ref = json.load(open(os.path.join(ROOT, "data", "w33_five_qubit_size9_verify.json")))["example"]


def span(gens):
    s = [0]
    for x in gens: s += [y ^ x for y in s]
    return s


def invariants5(cov):
    """cov: set of 10-bit ints (5-qubit covered points).  vanishing quadrics; uncovered anticommutation spectrum multiset"""
    m = 10; mons = [(i, j) for i in range(m) for j in range(i, m)]
    A = np.array([[(v >> i & 1) * (v >> j & 1) for (i, j) in mons] for v in sorted(cov)], dtype=np.uint8); r = 0
    for c in range(A.shape[1]):
        p = next((i for i in range(r, len(A)) if A[i, c]), None)
        if p is None: continue
        A[[r, p]] = A[[p, r]]
        for i in range(len(A)):
            if i != r and A[i, c]: A[i] ^= A[r]
        r += 1
    U = np.array(sorted(set(range(1, 1024)) - cov))
    X = np.array([[(v >> i) & 1 for i in range(10)] for v in U])
    Adj = (X[:, :5] @ X[:, 5:].T + X[:, 5:] @ X[:, :5].T) % 2
    ev = np.round(np.linalg.eigvalsh(Adj.astype(float)), 4)
    cnt = Counter(ev.tolist()); big = sorted(((k_, v) for k_, v in cnt.items() if v > 1), key=lambda t: -t[1])[:4]
    return dict(vanishing_quadrics=len(mons) - r, n_uncovered=len(U), degree=sorted(set(Adj.sum(1).tolist())), top_multiplicities=big,
                n_simple_eigs=sum(1 for v in cnt.values() if v == 1))


def quotient(p):
    qv = next(v for v in range(1, N) if om(v, p))
    rep = lambda v: v if om(v, qv) == 0 else v ^ p
    imgs = [sorted({rep(v) for v in L if v and om(v, p) == 0} - {0}) for L in lags]
    if any(set(a) & set(b) for a, b in itertools.combinations(imgs, 2)): return None
    # symplectic basis: e_i spanning imgs[0], f_i in imgs[1] dual
    def basis_of(S):
        b = []; sp_ = {0}
        for v in S:
            if v not in sp_: b.append(v); sp_ |= {x ^ v for x in sp_}
        return b
    e = basis_of(imgs[0]); assert len(e) == 5
    L1 = [0] + imgs[1]
    f = [next(v for v in L1 if all(om(v, e[j]) == (i == j) for j in range(5))) for i in range(5)]
    coord = lambda v: sum(om(v, f[i]) << i for i in range(5)) | (sum(om(v, e[i]) << i for i in range(5)) << 5)
    cov = set()
    for S in imgs: cov |= {coord(v) for v in S}
    codes = []
    for S in imgs[2:]:
        M = np.zeros((5, 5), int)
        for i in range(5):  # image of basis x = unit i: the element of S with x-coords = unit vector i
            v = next(coord(u) for u in S if (coord(u) & 31) == (1 << i)); zz = v >> 5
            for j in range(5): M[j, i] = (zz >> j) & 1
        assert (M == M.T).all()
        codes.append(sum(1 << b for b, (i, j) in enumerate(pos5) if M[i, j]))
    comp = np.ones(len(ns5), bool)
    for c in codes: comp &= ~sing5[ns5 ^ c]
    comp &= ~np.isin(ns5, codes)
    return dict(p=int(p), Q0_p=Q0(p), covered=len(cov), extendible_T=int(comp.sum()), maximal=bool(comp.sum() == 0), codes=sorted(codes), **invariants5(cov))


cov_ref = set().union(*lags_from_codes(5, ref)) - {0}
res["pass12650_set_invariants"] = invariants5(cov_ref)
print("Pass 12650 set:", res["pass12650_set_invariants"], flush=True)
cands = [v for v in range(1, N) if Q0(v) == 1]
sel = [cands[i] for i in rng.choice(len(cands), 6, replace=False)]
res["quotients"] = []
for p in sel:
    r = quotient(p); res["quotients"].append(r); print(r, round(time.time() - t0), "s", flush=True)
sing_pts = [v for v in range(1, N) if Q0(v) == 0 and v not in C6][:2]
res["control_singular_point_quotients"] = [quotient(p) is not None for p in sing_pts]
print("control (uncovered Q0-singular p gives disjoint images?):", res["control_singular_point_quotients"], flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_regulus_f8_and_quotient.json"), "w"), indent=1, default=float)
