"""Pass 12657: the minimal qubit MUB sets as REGULI over F_q, q = 2^k (n = 2k qubits = two F_q-'qudits').
Model: symplectic space F_q^4 = {(x1, x2, z1, z2)} with omega = Tr_{F_q/F_2}(x.z' + z.x') and F_q-valued quadratic form
Q = x1 z1 + x2 z2 (a hyperbolic quadric Q^+(3,q)).  One regulus of Q is the set of q + 1 lines
    L_inf = {x = 0},   L_t = {z1 = t x2, z2 = t x1},  t in F_q,
pairwise disjoint Lagrangians over F_2 (Kantor, arXiv:1601.04194, Thm 5.2: size q^k'+1 sets in dimension 4k'; here k' = k).
In rank-code form: S_t = [[0, M_t], [M_t, 0]] with M_t[i][j] = Tr(t b_i b_j).  The eigenbases are the computational basis and
CZ_t (F (x) F)|x1, x2>, CZ_t = diag chi(t x1 x2): an explicit family of q + 1 bases of C^q (x) C^q.
Tests:  (1) q = 4: maximal (all 448 nonsingular T killed); invariants 'Lagrangians inside C' and 'partitions of C' -- type B of
            Pass 12648 has (10, 2), type A (6, 1); numerical min F (1/16 expected).
        (2) q = 8: maximal over all 888,832 nonsingular symmetric 6x6 T; covered set = the 567 points with Q = 0.
        (3) covered set = {Q = 0} for q = 2, 4, 8, so Sigma_C <P>^2 is a quadric sum over F_q.
        (4) the index-of-coincidence formula derived in the pass note,
              sum_{t in F_q} IC_t = (1/q) [ c + 2 (1 - IC_inf) + R' ],   c = |sum_x A(x)^2|^2,
              R' = sum_{sigma != 0} sum_{lam != 0, 1} G(sigma, lam sigma),  G(s, d) = sum_x A(x) A(x+s) conj(A(x+d) A(x+s+d)),
            checked on random A for q = 2, 4, 8; q = 2 gives F = (1 + c)/2 - 1/4... i.e. Sigma IC = 1 + c/2 >= 1 (the proof of 1/4).
usage: py -3 analysis/w33_regulus_mub_sets.py"""
import itertools, json, os, time
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
POLY = {1: 0b11, 2: 0b111, 3: 0b1011}


def field(k):
    q = 1 << k; poly = POLY[k]
    def mul(a, b):
        r = 0
        while b:
            if b & 1: r ^= a
            b >>= 1; a <<= 1
            if a >> k & 1: a ^= poly
        return r
    tr = lambda a: (lambda s: bin(s).count("1") % 2 if k == 1 else None)(a)
    def trace(a):
        s = 0; y = a
        for _ in range(k): s ^= y; y = mul(y, y)
        assert s in (0, 1); return s
    return q, mul, trace


def regulus_codes(k):
    q, mul, trace = field(k); n = 2 * k
    pos = [(i, j) for i in range(n) for j in range(i, n)]
    codes = {}
    for t in range(1, q):
        M = [[trace(mul(t, mul(1 << i, 1 << j))) for j in range(k)] for i in range(k)]
        S = [[0] * n for _ in range(n)]
        for i in range(k):
            for j in range(k): S[i][k + j] = S[k + j][i] = M[i][j]
        codes[t] = sum(1 << b for b, (i, j) in enumerate(pos) if S[i][j])
    return codes


g = {"__name__": "x", "__file__": os.path.join(HERE, "w33_selfdual_pauli_lp.py")}
src = open(os.path.join(HERE, "w33_selfdual_pauli_lp.py"), encoding="utf-8").read()
exec(src[: src.index("t0 = time.time()")], g)
lags_from_codes = g["lags_from_codes"]
gs = {"__name__": "x", "__file__": os.path.join(HERE, "w33_symmetric_rank_code_spreads.py")}
srcs = open(os.path.join(HERE, "w33_symmetric_rank_code_spreads.py"), encoding="utf-8").read()
exec(srcs[: srcs.index("def code_of")], gs)
res = {}; t0 = time.time()
for k in (1, 2, 3):
    q, mul, trace = field(k); n = 2 * k; d = 1 << n
    codes = regulus_codes(k); lags = lags_from_codes(n, list(codes.values()))
    C = set().union(*lags) - {0}
    # quadric Q = x1 z1 + x2 z2 over F_q with dual-basis z coordinates: z_j = Tr(z b_j) -> recover z in F_q
    dual = []
    for j in range(k):  # element e_j with Tr(e_j b_i) = delta_ij
        dual.append(next(e for e in range(q) if all(trace(mul(e, 1 << i)) == (i == j) for i in range(k))))
    def Qv(v):
        x = v & (d - 1); zc = v >> n
        x1, x2 = x & (q - 1), x >> k
        z = lambda c: (lambda bits: __import__("functools").reduce(lambda a, b: a ^ b, [dual[j] for j in range(k) if bits >> j & 1], 0))(c)
        z1, z2 = z(zc & (q - 1)), z(zc >> k)
        return mul(x1, z1) ^ mul(x2, z2)
    quad = {v for v in range(1, d * d) if Qv(v) == 0}
    pos, sing, alt, ns = gs["setup"](n)
    comp = np.ones(len(ns), bool)
    for c in codes.values(): comp &= ~sing[ns ^ c]
    comp &= ~np.isin(ns, list(codes.values()))
    rec = dict(q=q, n_qubits=n, size=q + 1, covered=len(C), covered_equals_quadric=bool(C == quad), n_nonsingular_T=int(len(ns)),
               extendible_T=int(comp.sum()), maximal=bool(comp.sum() == 0), codes=sorted(codes.values()))
    res[f"q{q}"] = rec; print(rec, round(time.time() - t0), "s", flush=True)
# q = 4 invariants against the census types
ex4 = {"__name__": "x", "__file__": os.path.join(HERE, "w33_exhaustive_small_maximal_spreads.py")}
src4 = open(os.path.join(HERE, "w33_exhaustive_small_maximal_spreads.py"), encoding="utf-8").read()
exec(src4[: src4.index("def decide")], ex4)
lags4, _ = ex4["lagrangians"](4)
C4 = set().union(*lags_from_codes(4, res["q4"]["codes"])) - {0}
inside = [L for L in lags4 if set(L) <= C4]
def n_partitions(inside):
    cnt = 0
    def rec(ch, rem):
        nonlocal cnt
        if not rem: cnt += 1; return
        p = min(rem)
        for L in inside:
            if p in L and set(L) <= rem: rec(ch + [L], rem - set(L))
    rec([], set(C4)); return cnt
res["q4"]["lagrangians_inside_C"] = len(inside); res["q4"]["partitions_of_C"] = n_partitions(inside)
census = json.load(open(os.path.join(ROOT, "data", "w33_four_qubit_size5_census.json")))
res["q4"]["census_types_(n_inside,n_partitions)"] = [(t["n_inside"], t["n_partitions"]) for t in census["types"]]
print({k_: res["q4"][k_] for k_ in ("lagrangians_inside_C", "partitions_of_C", "census_types_(n_inside,n_partitions)")}, flush=True)
# CZ-model bases and the IC formula
rng = np.random.default_rng(0)
def ic_model(k, A):
    q, mul, trace = field(k)
    chi = lambda y: 1 - 2 * trace(y)
    ic_inf = float((np.abs(A) ** 4).sum())
    ics = []
    for t in range(q):
        B = np.array([[A[x1, x2] * chi(mul(t, mul(x1, x2))) for x2 in range(q)] for x1 in range(q)])
        K = np.array([[sum(B[x1, x2] * chi(mul(k1, x1) ^ mul(k2, x2)) for x1 in range(q) for x2 in range(q)) / q for k2 in range(q)] for k1 in range(q)])
        ics.append(float((np.abs(K) ** 4).sum()))
    def G(s, dl):
        tot = 0
        for x1 in range(q):
            for x2 in range(q):
                a = A[x1, x2]; b = A[x1 ^ s[0], x2 ^ s[1]]; c_ = A[x1 ^ dl[0], x2 ^ dl[1]]; e = A[x1 ^ s[0] ^ dl[0], x2 ^ s[1] ^ dl[1]]
                tot += a * b * np.conj(c_ * e)
        return tot
    c = abs((A ** 2).sum()) ** 2
    Rp = sum(G(s, (mul(lam, s[0]), mul(lam, s[1]))) for s in itertools.product(range(q), repeat=2) if s != (0, 0) for lam in range(2, q))
    rhs = (c + 2 * (1 - ic_inf) + Rp.real) / q
    return ic_inf, sum(ics), rhs, abs(Rp.imag)
form = {}
for k in (1, 2, 3):
    q = 1 << k; worst = 0
    for _ in range(3 if k < 3 else 1):
        A = rng.standard_normal((q, q)) + 1j * rng.standard_normal((q, q)); A /= np.linalg.norm(A)
        ic_inf, lhs, rhs, im = ic_model(k, A); worst = max(worst, abs(lhs - rhs), im)
    form[f"q{q}"] = worst
res["IC_formula_max_residual"] = form; print("IC formula residuals", form, flush=True)
# numerical min F in the CZ model for q = 4
def F_model(k, w):
    q = 1 << k; A = (w[: q * q] + 1j * w[q * q:]).reshape(q, q); A = A / np.linalg.norm(A)
    ic_inf, s, _, _ = ic_model(k, A); return ic_inf + s - (q + 1) / q ** 2
best = min(minimize(lambda w: F_model(2, w), rng.standard_normal(32), method="L-BFGS-B").fun for _ in range(12))
res["q4_min_F_CZ_model"] = float(best); print("q = 4 CZ-model min F:", best, "(1/16 =", 1 / 16, ")", flush=True)
json.dump(res, open(os.path.join(ROOT, "data", "w33_regulus_mub_sets.json"), "w"), indent=1, default=int)
