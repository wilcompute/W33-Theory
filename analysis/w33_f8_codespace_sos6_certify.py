"""Pass 12673: an EXACT degree-6 SOS certificate that 64F >= C_CERT on the 8-dim code space of T (Pass 12671/12672).
Basis: the 8 independent columns B0 of the code-space projector (entries in {0, +-1/8, +-i/8}), so with A = B0 t,
  g(t) := (t^H G t) (64 sum_j |w_j . t|^4 - (9 + C) (t^H G t)^2),   G = B0^H B0,  w_j = B0^H b_j  (all in Q(i))
and 64F(A) >= C for all A in the code space  <=>  g >= 0.  Certificate: g = m3^H X3 m3 + m1^H X1 m1 with X Hermitian PSD,
m3 = (t^alpha, |alpha| = 3), m1 = (t^alpha conj t_i, |alpha| = 2).  Steps: (1) SCS at fixed C maximising s with X - s I PSD (real
embedding); (2) round X to Gaussian rationals (denominator 2^R); (3) exact orthogonal projection onto the affine coefficient
constraints (each Gram entry feeds exactly one coefficient key, so the projection subtracts residual/count on each key, preserving
Hermiticity); (4) PSD proof in exact arithmetic: real embedding Y (2n x 2n, rational); floating LDL^T of Y - delta I rounded to
dyadic L, D; residual E = Y - delta I - L D L^T computed EXACTLY (integers); Y >= 0 is certified if D >= 0 and ||E||_F <= delta.
usage: py -3 analysis/w33_f8_codespace_sos6_certify.py [C_CERT] [scs_iters]"""
import itertools, json, math, os, sys, time
from fractions import Fraction as Fr
from math import factorial
import numpy as np
import scipy.sparse as sps
import scs
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_regulus_constants_q16_q32.py"), encoding="utf-8").read()
gl = {"__name__": "x", "__file__": os.path.join(HERE, "w33_regulus_constants_q16_q32.py")}
exec(src[: src.index("def model(")], gl)
q, mul, trace = gl["field"](3)
C_CERT = Fr(sys.argv[1]) if len(sys.argv) > 1 else Fr(49, 20)
ITERS = int(sys.argv[2]) if len(sys.argv) > 2 else 100000
pc = lambda n: bin(n).count("1") & 1
n = 8


def pauli(u, v):
    M = np.zeros((64, 64), complex)
    for x in range(64): M[x, x ^ u] = (-1) ** pc(v & (x ^ u))
    return M


H = [-1j * pauli(12, 53), pauli(53, 33), pauli(1, 6)]
Pr = np.eye(64, dtype=complex)
for X in H: Pr = Pr @ (np.eye(64) + X) / 2
cols = []
for j in range(64):
    if np.linalg.matrix_rank(Pr[:, cols + [j]], tol=1e-9) > len(cols): cols.append(j)
    if len(cols) == 8: break
B8 = np.round(Pr[:, cols] * 8)                     # 8 * B0, Gaussian integers
assert np.allclose(B8, Pr[:, cols] * 8)
Xi = np.array([[1 - 2 * trace(mul(a, b)) for b in range(8)] for a in range(8)])
Phi = np.array([[[1 - 2 * trace(mul(t, mul(a, b))) for b in range(8)] for a in range(8)] for t in range(8)])
U8 = [np.eye(64, dtype=int) * 8]
for t in range(8):
    Ut = np.zeros((64, 64), dtype=int)
    for x in range(64):
        e = np.zeros((8, 8), dtype=int); e.flat[x] = 1; Ut[:, x] = (Xi @ (e * Phi[t]) @ Xi).ravel()
    U8.append(Ut)
W64 = np.vstack([Ut @ B8 for Ut in U8])            # 64 * (b_j . B0 t) as rows: Gaussian integers (576 x 8)
W64 = np.round(W64).astype(complex)
G64 = np.round(B8.conj().T @ B8)                   # 64 * G
# ---- polynomial algebra: monomials as exponent pairs (A: conj exponents, B: exponents), coefficients Gaussian rationals (complex Fr pairs)
def multis(dg):
    out = []
    def rec(i, left, cur):
        if i == n - 1: out.append(tuple(cur + [left])); return
        for v in range(left, -1, -1): rec(i + 1, left - v, cur + [v])
    rec(0, dg, []); return out
mf = lambda a: math.prod(factorial(v) for v in a)
G1 = multis(1); G2 = multis(2); G3 = multis(3)
add = lambda a, b: tuple(x + y for x, y in zip(a, b))
# Hermitian forms as dicts {(A, B): complex Fraction (re, im)} meaning sum c conj(t^A) t^B
def herm_from_vector(u, power):  # |u . t|^{2 power} with u Gaussian integer vector: (sum u_i t_i)^p conj(...)^p
    lin = {}
    for g_ in multis(power):
        c = complex(mf((power,)) / mf(g_)) * np.prod([u[k] ** g_[k] for k in range(n)])
        lin[g_] = c
    return lin
def cadd(D, key, val):
    D[key] = D.get(key, 0) + val
# exact complex arithmetic via Python ints: represent Gaussian integers as complex with integer parts (exact while |.| < 2^53)
def gi(z): return (int(round(z.real)), int(round(z.imag)))
def gmul(a, b): return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])
def gadd(a, b): return (a[0] + b[0], a[1] + b[1])
def gconj(a): return (a[0], -a[1])
# quadratic form t^H (64 G) t : coefficients on (e_i, e_j)
Gq = {}
for i in range(n):
    for j in range(n):
        if G64[i, j] != 0: Gq[(G1[i], G1[j])] = gi(G64[i, j])   # conj(t_i) t_j  with coefficient (64G)_{ij}
def hmul(P, Q):
    R = {}
    for (a1, b1), c1 in P.items():
        for (a2, b2), c2 in Q.items():
            k = (add(a1, a2), add(b1, b2)); R[k] = gadd(R.get(k, (0, 0)), gmul(c1, c2))
    return {k: v for k, v in R.items() if v != (0, 0)}
# sum_j |w_j . t|^4 with w_j . t = (1/64) W64[j] . t  -> 64^4 sum |W64_j . t|^4 ; quartic as conj((W t)^2) (W t)^2
Q4 = {}
for row in W64:
    sq = {}
    for i in range(n):
        for j in range(n):
            k = add(G1[i], G1[j]); sq[k] = gadd(sq.get(k, (0, 0)), gmul(gi(row[i]), gi(row[j])))
    for ka, ca in sq.items():
        for kb, cb in sq.items():
            key = (ka, kb); Q4[key] = gadd(Q4.get(key, (0, 0)), gmul(gconj(ca), cb))
Q4 = {k: v for k, v in Q4.items() if v != (0, 0)}
G2q = hmul(Gq, Gq)                                  # (64^2) (t^H G t)^2
# target, scaled by S = 64^5 * den(C):  g * 64^5 = (64 tGt) * (64^4 * 64 * sum|w t|^4 ... ) -- assemble with common scaling:
# 64 sum |w.t|^4 = 64 * 64^-4 sum |W t|^4 ;  (t^H G t)^2 = 64^-2 G2q ;  t^H G t = 64^-1 Gq
# g = 64^-1 Gq * (64^-3 Q4 - (9 + C) 64^-2 G2q)  =  64^-4 Gq * (Q4 - 64 (9 + C) G2q)
Cn, Cd = C_CERT.numerator, C_CERT.denominator
inner = {k: (v[0] * Cd, v[1] * Cd) for k, v in Q4.items()}
for k, v in G2q.items():
    inner[k] = gadd(inner.get(k, (0, 0)), gmul(v, (-64 * (9 * Cd + Cn), 0)))
target = hmul(Gq, inner)                            # = 64^4 * Cd * g   (Gaussian integers)
SCALE = Fr(1, 64 ** 4 * Cd)
print("target terms:", len(target), flush=True)
# ---- Gram structure
m3 = [(a, (0,) * n) for a in G3]; m1 = [(a, G1[i]) for a in G2 for i in range(n)]
keys = sorted(set(target) | {(add(a1, b2), add(b1, a2)) for ms in (m3, m1) for (a1, b1) in ms for (a2, b2) in ms})
kidx = {k: i for i, k in enumerate(keys)}; KN = len(keys)
def entries(ms):
    out = []
    for p, (a1, b1) in enumerate(ms):
        for r, (a2, b2) in enumerate(ms): out.append((kidx[(add(a1, b2), add(b1, a2))], p, r))
    return out
E3, E1 = entries(m3), entries(m1)
L3, L1 = len(m3), len(m1)
count = np.zeros(KN, dtype=int)
for k, _, _ in E3 + E1: count[k] += 1
assert all(count[kidx[k]] > 0 for k in target), "target monomial not representable"
tv = np.zeros(KN, complex)
for k, v in target.items(): tv[kidx[k]] = complex(v[0], v[1])
tv_scaled = tv / float(64 ** 4 * Cd)
print("Gram sizes", L3, L1, "keys", KN, flush=True)
# ---- SCS: maximise s s.t. X_q - s I >= 0 (real embedding), A(X) = target
SIZE = {}
def sidx(i, j, n_):
    if i < j: i, j = j, i
    return j * n_ - j * (j - 1) // 2 + (i - j), (1.0 if i == j else 1 / math.sqrt(2))
nv3, nv1 = (2 * L3) * (2 * L3 + 1) // 2, (2 * L1) * (2 * L1 + 1) // 2
off3, off1 = 1, 1 + nv3; NV = 1 + nv3 + nv1; SIZE[off3] = 2 * L3; SIZE[off1] = 2 * L1
rows, cols_, vals = [], [], []
def addv(r, off, i, j, w):
    k, sc = sidx(i, j, SIZE[off]); rows.append(r); cols_.append(off + k); vals.append(w * sc)
for Ent, L, off in ((E3, L3, off3), (E1, L1, off1)):
    for (k, p_, r_) in Ent:
        addv(k, off, p_, r_, 0.5); addv(k, off, L + p_, L + r_, 0.5)
        addv(KN + k, off, L + p_, r_, 0.5); addv(KN + k, off, L + r_, p_, -0.5)
Aeq = sps.csr_matrix((vals, (rows, cols_)), shape=(2 * KN, NV))
beq = np.concatenate([tv_scaled.real, tv_scaled.imag])
# PSD rows: svec(Y) - s * svec(I) in PSD:  s = b - A x  with x = (s, y): row block = -I on y, +svec(I) on s
def svec_I(n_):
    v = np.zeros(n_ * (n_ + 1) // 2)
    for i in range(n_): v[sidx(i, i, n_)[0]] = 1.0
    return v
I3, I1 = svec_I(2 * L3), svec_I(2 * L1)
Ap = sps.hstack([sps.csr_matrix(np.concatenate([I3, I1])[:, None]), -sps.eye(NV - 1)]).tocsr()
A = sps.vstack([Aeq, Ap]).tocsc(); b = np.concatenate([beq, np.zeros(NV - 1)])
cvec = np.zeros(NV); cvec[0] = -1.0
t0 = time.time()
sol = scs.SCS(dict(A=A, b=b, c=cvec), dict(z=2 * KN, s=[2 * L3, 2 * L1]), eps_abs=1e-9, eps_rel=1e-9, max_iters=ITERS, verbose=False).solve()
s_val = float(sol["x"][0]); print(f"SCS: status {sol['info']['status']}, margin s = {s_val:.3e}, {time.time() - t0:.0f}s", flush=True)
y = sol["x"][1:]
def unsvec(vv, n_):
    M = np.zeros((n_, n_))
    for j in range(n_):
        for i in range(j, n_):
            k, sc = sidx(i, j, n_); M[i, j] = M[j, i] = vv[k] * sc
    return M
Y3, Y1 = unsvec(y[:nv3], 2 * L3), unsvec(y[nv3:], 2 * L1)
X3 = (Y3[:L3, :L3] + Y3[L3:, L3:]) / 2 + 1j * (Y3[L3:, :L3] - Y3[L3:, :L3].T) / 2
X1 = (Y1[:L1, :L1] + Y1[L1:, L1:]) / 2 + 1j * (Y1[L1:, :L1] - Y1[L1:, :L1].T) / 2
np.save(os.path.join(ROOT, "data", "w33_f8_sos6_cert_X3.npy"), X3); np.save(os.path.join(ROOT, "data", "w33_f8_sos6_cert_X1.npy"), X1)
# ---- rounding + exact projection (Gaussian rationals with denominator 2^R * 64^4 * Cd)
R = 40; DEN = (1 << R)
def rnd(M): return np.vectorize(lambda z: (int(round(z.real * DEN)), int(round(z.imag * DEN))), otypes=[object])(M)
Xr = {"3": rnd(X3), "1": rnd(X1)}
for kq in Xr:  # Hermitise exactly
    M = Xr[kq]; L = M.shape[0]
    for i in range(L):
        M[i, i] = (M[i, i][0], 0)
        for j in range(i + 1, L): M[j, i] = (M[i, j][0], -M[i, j][1])
# residual per key (in units 1/DEN): sum of entries - target*DEN*SCALE
res_ = [Fr(0)] * KN; resi = [Fr(0)] * KN
for kq, Ent in (("3", E3), ("1", E1)):
    M = Xr[kq]
    for (k, p_, r_) in Ent: res_[k] += M[p_, r_][0]; resi[k] += M[p_, r_][1]
for k, v in target.items():
    i = kidx[k]; res_[i] -= Fr(v[0]) * DEN * SCALE; resi[i] -= Fr(v[1]) * DEN * SCALE
Xf = {kq: np.vectorize(lambda z: complex(Fr(z[0]), Fr(z[1])) if False else None, otypes=[object])(Xr[kq]) for kq in Xr}
# exact corrected matrices as Fractions (re, im) / DEN
Xe = {}
for kq, Ent in (("3", E3), ("1", E1)):
    M = Xr[kq]; L = M.shape[0]
    Me = [[[Fr(M[i, j][0]), Fr(M[i, j][1])] for j in range(L)] for i in range(L)]
    for (k, p_, r_) in Ent:
        Me[p_][r_][0] -= res_[k] / count[k]; Me[p_][r_][1] -= resi[k] / count[k]
    Xe[kq] = Me
# verify exact identity and Hermiticity
chk = [Fr(0)] * KN; chki = [Fr(0)] * KN
for kq, Ent in (("3", E3), ("1", E1)):
    for (k, p_, r_) in Ent: chk[k] += Xe[kq][p_][r_][0]; chki[k] += Xe[kq][p_][r_][1]
for k in range(KN):
    v = target.get(keys[k], (0, 0))
    assert chk[k] == Fr(v[0]) * DEN * SCALE and chki[k] == Fr(v[1]) * DEN * SCALE
herm_ok = all(Xe[kq][i][j][0] == Xe[kq][j][i][0] and Xe[kq][i][j][1] == -Xe[kq][j][i][1] for kq in Xe for i in range(len(Xe[kq])) for j in range(len(Xe[kq])))
print("exact identity after projection: True; hermitian:", herm_ok, flush=True)
# ---- exact PSD proof: real embedding Y = [[Re, -Im], [Im, Re]] (scaled by DEN), Y - delta I = L D L^T + E
def certify(Me, delta_frac):
    L = len(Me); n2 = 2 * L
    Yf = np.zeros((n2, n2))
    for i in range(L):
        for j in range(L):
            re, im = float(Me[i][j][0]), float(Me[i][j][1])
            Yf[i, j] = Yf[L + i, L + j] = re; Yf[L + i, j] = im; Yf[i, L + j] = -im
    lam = np.linalg.eigvalsh(Yf)[0] / DEN
    delta = float(delta_frac)
    Cf = np.linalg.cholesky(Yf - delta * DEN * np.eye(n2))
    SC = 1 << 30
    Li = np.vectorize(lambda z: int(round(z * SC)), otypes=[object])(Cf)
    LLt = Li.dot(Li.T)                                  # exact integers, = SC^2 * (approx Y - delta DEN I)
    # E = Y*DEN... compute exactly: Ye - delta*DEN*I - LLt/SC^2, entries rational with denominator lcm
    maxE2 = Fr(0)
    dlt = Fr(delta_frac) * DEN
    for i in range(n2):
        for j in range(n2):
            ii, jj = i % L, j % L
            if (i < L) == (j < L): yv = Me[ii][jj][0]
            elif i >= L and j < L: yv = Me[ii][jj][1]
            else: yv = -Me[ii][jj][1]
            e_ = yv - (dlt if i == j else 0) - Fr(int(LLt[i, j]), SC * SC)
            maxE2 += e_ * e_
    ok = maxE2 < dlt * dlt          # ||E||_F < delta  ==>  Y = LL^T + delta I + E >= 0
    return dict(lam_min_float=float(lam), delta=str(delta_frac), frob_E_sq_over_delta_sq=float(maxE2 / (dlt * dlt)), psd_certified=bool(ok))
out = dict(C_cert=str(C_CERT), scs_margin=s_val, gram=[L3, L1], keys=KN, round_bits=R)
for kq in ("3", "1"):
    lam = np.linalg.eigvalsh(np.array([[complex(float(Xe[kq][i][j][0]), float(Xe[kq][i][j][1])) for j in range(len(Xe[kq]))] for i in range(len(Xe[kq]))]))[0] / DEN
    delta = Fr(max(lam / 4, 1e-12)).limit_denominator(1 << 40)
    out["block" + kq] = certify(Xe[kq], delta)
    print("block", kq, out["block" + kq], flush=True)
out["certified"] = out["block3"]["psd_certified"] and out["block1"]["psd_certified"]
print("CERTIFIED: 64F >= %s on the rank-3 code space:" % C_CERT, out["certified"], flush=True)
json.dump(out, open(os.path.join(ROOT, "data", "w33_f8_codespace_sos6_certificate_" + str(C_CERT).replace("/", "_") + ".json"), "w"), indent=1)
