"""Pass 12671: an EXACT six-qubit state attaining c8 = (47 - 32 cos(2 pi/9))/9 for the nine F_8-regulus MUBs of C^64.
Input: the 45-digit rank-3-stabiliser minimiser (data/w33_f8_rank3_stabiliser_exact.json).  Hermitian Paulis
Hh(u,v) = i^{|u&v|} X^u Z^v with (X^u Z^v psi)[x] = (-1)^{v.(x^u)} psi[x^u].  Every expectation r = <Hh> is identified by pslq in
K0 = Q(g, sqrt3), g = 2cos(2pi/9) (g^3 = 3g - 1), basis [1, g, g^2, s, s g, s g^2], s = sqrt 3 (residual < 1e-40 asserted).
Then rho := (1/64) sum r_P Hh_P is built in EXACT arithmetic over K = K0(i) (12 rational coordinates, common denominator) and checked:
rho^dagger = rho, tr rho = 1, rho^2 = rho (so rho is a pure state), and the nine basis distributions p_{t,k} = (U_t rho U_t^T)_{kk}
(U_t the exact CZ-model basis unitaries, entries in {0, +-1/8, 1}) give 64 F = 64 (sum p^2 - 9/64) EXACTLY equal to (47 - 16 g)/9.
No floating point enters the verification; floats are used only to FIND the exact coefficients.
usage: py -3 analysis/w33_f8_exact_witness.py"""
import json, os
from fractions import Fraction
import numpy as np
import mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_regulus_constants_q16_q32.py"), encoding="utf-8").read()
gl = {"__name__": "x", "__file__": os.path.join(HERE, "w33_regulus_constants_q16_q32.py")}
exec(src[: src.index("def model(")], gl)
q, mul, trace = gl["field"](3)
pc = lambda n: bin(n).count("1")
mp.mp.dps = 50
d = json.load(open(os.path.join(ROOT, "data", "w33_f8_rank3_stabiliser_exact.json")))
x = [mp.mpf(s) for s in d["minimiser"]]
# rebuild the 64-dim state from the eigenspace basis (same construction as w33_f8_rank3_stabiliser_exact.py)
def pauli_np(u, v):
    M = np.zeros((64, 64), complex)
    for y in range(64): M[y, y ^ u] = (-1) ** (pc(v & (y ^ u)) & 1)
    return M
Hs = [-1j * pauli_np(12, 53), pauli_np(53, 33), pauli_np(1, 6)]
Proj = np.eye(64, dtype=complex)
for X in Hs: Proj = Proj @ (np.eye(64) + X) / 2
cols = []
for j in range(64):
    if np.linalg.matrix_rank(Proj[:, cols + [j]], tol=1e-9) > len(cols): cols.append(j)
    if len(cols) == 8: break
ex = lambda z: mp.mpc(mp.mpf(int(round(z.real * 8))) / 8, mp.mpf(int(round(z.imag * 8))) / 8)
Qb = []
for j in cols:
    v = [ex(Proj[i, j]) for i in range(64)]
    for w in Qb:
        ip = mp.fsum(mp.conj(w[i]) * v[i] for i in range(64)); v = [v[i] - ip * w[i] for i in range(64)]
    nr = mp.sqrt(mp.fsum(abs(z) ** 2 for z in v)); Qb.append([z / nr for z in v])
t = [mp.mpc(x[2 * j], x[2 * j + 1]) for j in range(8)]
A = [mp.fsum(Qb[j][i] * t[j] for j in range(8)) for i in range(64)]
nr = mp.sqrt(mp.fsum(abs(z) ** 2 for z in A)); A = [z / nr for z in A]
g = 2 * mp.cos(2 * mp.pi / 9); s3 = mp.sqrt(3)
B6 = [1, g, g * g, s3, s3 * g, s3 * g * g]
# --- identify every Hermitian Pauli expectation in K0
r = {}
for u in range(64):
    for v in range(64):
        ph = mp.mpc(0, 1) ** (pc(u & v) % 4)
        e = ph * mp.fsum(mp.conj(A[y]) * (-1) ** (pc(v & (y ^ u)) & 1) * A[y ^ u] for y in range(64))
        assert abs(mp.im(e)) < mp.mpf(10) ** -40
        e = mp.re(e)
        if abs(e) < mp.mpf(10) ** -40: continue
        rel = mp.pslq([e] + B6, maxcoeff=10 ** 4, maxsteps=10 ** 6)
        assert rel is not None and rel[0] != 0, (u, v)
        coeffs = [Fraction(-c, rel[0]) for c in rel[1:]]
        assert abs(e - mp.fsum(mp.mpf(c.numerator) / c.denominator * b for c, b in zip(coeffs, B6))) < mp.mpf(10) ** -40
        r[(u, v)] = coeffs
print("nonzero expectations identified exactly:", len(r), flush=True)
# --- exact arithmetic in K = Q(g)(s)(i): coordinates e = a + 3b + 6c for g^a s^b i^c
def basis_mul(e1, e2):
    a1, b1, c1 = e1 % 3, (e1 // 3) % 2, e1 // 6; a2, b2, c2 = e2 % 3, (e2 // 3) % 2, e2 // 6
    coef = 1; b = b1 + b2; c = c1 + c2
    if b == 2: coef *= 3; b = 0
    if c == 2: coef *= -1; c = 0
    gpow = [0, 0, 0, 0, 0]; gpow[a1 + a2] = coef
    if gpow[4]: gpow[2] += 3 * gpow[4]; gpow[1] -= gpow[4]; gpow[4] = 0          # g^4 = 3g^2 - g
    if gpow[3]: gpow[1] += 3 * gpow[3]; gpow[0] -= gpow[3]; gpow[3] = 0          # g^3 = 3g - 1
    out = [0] * 12
    for a in range(3): out[a + 3 * b + 6 * c] += gpow[a]
    return out
T = np.array([[basis_mul(e1, e2) for e2 in range(12)] for e1 in range(12)], dtype=object)
DEN = 64 * 27
rho = np.zeros((12, 64, 64), dtype=object)
for (u, v), co in r.items():
    k = pc(u & v) % 4  # i^k: k=0 ->1, 1 -> i, 2 -> -1, 3 -> -i
    sgn, im = [(1, 0), (1, 1), (-1, 0), (-1, 1)][k]
    for e0, cfrac in enumerate(co):
        if cfrac == 0: continue
        val = cfrac * DEN * sgn / 64; assert val.denominator == 1; val = int(val)
        e = e0 + 6 * im
        for y in range(64):
            rho[e, y, y ^ u] += val * (-1) ** (pc(v & (y ^ u)) & 1)
def kmatmul(M, N):  # M, N: (12,n,m) integer object arrays; returns (12,...) product (no denominators)
    out = np.zeros((12, M.shape[1], N.shape[2]), dtype=object)
    for e1 in range(12):
        if not M[e1].any(): continue
        for e2 in range(12):
            if not N[e2].any(): continue
            P = M[e1].dot(N[e2])
            for e in range(12):
                if T[e1, e2, e]: out[e] += T[e1, e2, e] * P
    return out
def conjT(M):  # conjugate transpose: i -> -i
    out = np.array([M[e].T.copy() for e in range(12)], dtype=object)
    out[6:] *= -1; return out
herm = all((conjT(rho)[e] == rho[e]).all() for e in range(12))
tr = [sum(rho[e][y, y] for y in range(64)) for e in range(12)]
trace_one = tr[0] == DEN and all(v == 0 for v in tr[1:])
rho2 = kmatmul(rho, rho)
idem = all((rho2[e] == DEN * rho[e]).all() for e in range(12))
print("hermitian", herm, "trace 1", trace_one, "rho^2 = rho", idem, flush=True)
# --- exact basis distributions: U_t from the CZ model (U_0 = identity, U_t = vec of Xi (E o Phi_t) Xi / 8)
Xi = np.array([[1 - 2 * trace(mul(a, b)) for b in range(8)] for a in range(8)], dtype=object)
Phi = [np.array([[1 - 2 * trace(mul(tt, mul(a, b))) for b in range(8)] for a in range(8)], dtype=object) for tt in range(8)]
total = [Fraction(0)] * 12  # sum over bases and outcomes of p^2, in K0 coordinates (i-part must vanish)
sq_terms = []
for tt in range(9):
    if tt == 0:
        U8 = np.eye(64, dtype=object) * 8
    else:
        U8 = np.zeros((64, 64), dtype=object)
        for xx in range(64):
            E = np.zeros((8, 8), dtype=object); E[xx // 8, xx % 8] = 1
            U8[:, xx] = (Xi.dot(E * Phi[tt - 1]).dot(Xi)).ravel()
    Uk = np.zeros((12, 64, 64), dtype=object); Uk[0] = U8
    M = kmatmul(kmatmul(Uk, rho), conjT(Uk))  # = 64 * DEN * U rho U^T
    for k in range(64):
        p = [M[e][k, k] for e in range(12)]  # p_k * 64 * DEN
        assert all(v == 0 for v in p[6:])
        pp = kmatmul(np.array(p, dtype=object).reshape(12, 1, 1), np.array(p, dtype=object).reshape(12, 1, 1))
        for e in range(12): total[e] += Fraction(int(pp[e][0, 0]), (64 * DEN) ** 2)
c_exact = [64 * (total[e] - (Fraction(9, 64) if e == 0 else 0)) for e in range(12)]
target = [Fraction(47, 9), Fraction(-16, 9)] + [Fraction(0)] * 10
print("64 F exactly (coords in 1, g, g^2, s, ...):", [str(v) for v in c_exact[:6]], flush=True)
ok = c_exact == target
print("EXACT: 64 F(rho) == (47 - 16 g)/9 = (47 - 32 cos(2pi/9))/9 :", ok, flush=True)
res = dict(n_nonzero=len(r), hermitian=bool(herm), trace_one=bool(trace_one), idempotent=bool(idem), c_exact=[str(v) for v in c_exact],
           equals_closed_form=bool(ok), field="Q(2cos(2pi/9), sqrt3, i)",
           expectations={f"{u},{v}": [str(c) for c in co] for (u, v), co in sorted(r.items())})
json.dump(res, open(os.path.join(ROOT, "data", "w33_f8_exact_witness.json"), "w"), indent=1)
