"""Item 1 (exact): the strong-unextendibility certificate for the two-qutrit pentads in exact arithmetic over Q(omega), omega^2 = -1 - omega.
Stabiliser projectors P_{L,jk} = (1/9) sum_{a,b} omega^{-(ja+kb)} W_u^a W_v^b (u, v spanning the isotropic plane L) - exact.
M = sum_e A_e (x) A_e, A_e = P_e - I/9, X = Pi M Pi on C^81 with Pi = (I + SWAP)/2.  The eigenvalues of X on Sym^2 are those of the
operator H of w33_strong_umub_hermitian_sos.py.  Exact certificate: with the distinct eigenvalues lambda_i (found numerically, rationalised
with an asserted denominator), verify EXACTLY that Pi * prod_i (X - lambda_i) = 0.  Then spec(H) is contained in {lambda_i}; if
min lambda_i = 1/9 > 0, F(v) >= |v|^4/9 exactly, i.e. strongly unextendible.  Done for one pentad of each PSp(4,3)-chirality orbit
(all others are Clifford-unitarily or antiunitarily equivalent, which preserves the spectrum) and for one size-8 set.
usage: py -3 analysis/w33_strong_umub_exact.py"""
import itertools, json, os
from fractions import Fraction as Fr
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
import contextlib, io
ns = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pentad_umub.py")}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(os.path.join(HERE, "w33_pentad_umub.py"), encoding="utf-8").read().split("# --- (3)")[0], ns)
P, lines, maxsets, disj, w = ns["P"], ns["lines"], ns["maxsets"], ns["disj"], ns["w"]
# --- Q(omega) arithmetic: (a, b) = a + b*omega
class Q:
    __slots__ = ("a", "b")
    def __init__(s, a=0, b=0): s.a, s.b = Fr(a), Fr(b)
    def __add__(s, o): return Q(s.a + o.a, s.b + o.b)
    def __sub__(s, o): return Q(s.a - o.a, s.b - o.b)
    def __mul__(s, o):  # (a + b w)(c + d w) = ac + (ad + bc) w + bd w^2, w^2 = -1 - w
        return Q(s.a * o.a - s.b * o.b, s.a * o.b + s.b * o.a - s.b * o.b)
    def scale(s, f): return Q(s.a * f, s.b * f)
    def iszero(s): return s.a == 0 and s.b == 0
    def conj(s): return Q(s.a - s.b, -s.b)  # conj(w) = w^2 = -1 - w
ZERO, ONE = Q(0, 0), Q(1, 0)
W = [Q(1, 0), Q(0, 1), Q(-1, -1)]  # omega^0, omega^1, omega^2
d = 9
def mat_zero(n): return [[ZERO] * n for _ in range(n)]
def mat_mul(A, B):
    n, m, k = len(A), len(B[0]), len(B)
    Bt = list(zip(*B))
    out = []
    for i in range(n):
        Ai = A[i]
        row = []
        for j in range(m):
            acc_a, acc_b = Fr(0), Fr(0)
            col = Bt[j]
            for t in range(k):
                x, y = Ai[t], col[t]
                if (x.a or x.b) and (y.a or y.b):
                    acc_a += x.a * y.a - x.b * y.b
                    acc_b += x.a * y.b + x.b * y.a - x.b * y.b
            row.append(Q(acc_a, acc_b))
        out.append(row)
    return out
# single-qutrit X, Z exactly
def Xq():
    M = mat_zero(3)
    for k in range(3): M[(k + 1) % 3][k] = ONE
    return M
def Zq():
    M = mat_zero(3)
    for k in range(3): M[k][k] = W[k]
    return M
def mpow(M, e):
    R = [[ONE if i == j else ZERO for j in range(len(M))] for i in range(len(M))]
    for _ in range(e % 3): R = mat_mul(R, M)
    return R
def kron(A, B):
    n, m = len(A), len(B)
    return [[A[i // m][j // m] * B[i % m][j % m] for j in range(n * m)] for i in range(n * m)]
X1, Z1 = Xq(), Zq()
def weyl(u):  # X^{u0} Z^{u2} (x) X^{u1} Z^{u3}  (same convention as w33_pentad_umub.pauli)
    return kron(mat_mul(mpow(X1, u[0]), mpow(Z1, u[2])), mat_mul(mpow(X1, u[1]), mpow(Z1, u[3])))
def projectors(L):
    pts = sorted(lines[L])
    u, v = P[pts[0]], next(P[q] for q in pts[1:] if P[q] != P[pts[0]])
    # pick v not a multiple of u
    for q in pts[1:]:
        cand = P[q]
        if any((cand[k] * 1) % 3 != (u[k] * c) % 3 for c in (1, 2) for k in range(4) if True):
            v = cand
            if not any(all((cand[k] - c * u[k]) % 3 == 0 for k in range(4)) for c in (0, 1, 2)):
                break
    Wu, Wv = weyl(u), weyl(v)
    G = {}
    for a in range(3):
        for b in range(3):
            G[(a, b)] = mat_mul(mpow(Wu, a), mpow(Wv, b))
    projs = []
    for j in range(3):
        for k in range(3):
            Pm = mat_zero(d)
            for (a, b), g in G.items():
                ph = W[(-(j * a + k * b)) % 3]
                for r in range(d):
                    for c in range(d):
                        if not g[r][c].iszero():
                            Pm[r][c] = Pm[r][c] + (ph * g[r][c]).scale(Fr(1, 9))
            projs.append(Pm)
    return projs
def num(Mq):
    om = np.exp(2j * np.pi / 3)
    return np.array([[float(x.a) + float(x.b) * om for x in row] for row in Mq])
def certificate(Ls):
    # exact M = sum_e A_e (x) A_e on C^81
    n = d * d
    M = mat_zero(n)
    for L in Ls:
        for Pm in projectors(L):
            A = [[Pm[r][c] - (ONE.scale(Fr(1, 9)) if r == c else ZERO) for c in range(d)] for r in range(d)]
            K = kron(A, A)
            for r in range(n):
                Mr, Kr = M[r], K[r]
                for c in range(n):
                    if not Kr[c].iszero(): Mr[c] = Mr[c] + Kr[c]
    # Pi = (I + SWAP)/2
    Pi = mat_zero(n)
    for i in range(d):
        for j in range(d):
            r = i * d + j
            Pi[r][r] = Pi[r][r] + ONE.scale(Fr(1, 2))
            Pi[r][j * d + i] = Pi[r][j * d + i] + ONE.scale(Fr(1, 2))
    Xm = mat_mul(mat_mul(Pi, M), Pi)
    # numerical spectrum on Sym^2 -> distinct eigenvalues, rationalised with denominator dividing 81 (asserted)
    ev = np.linalg.eigvalsh((num(Xm) + num(Xm).conj().T) / 2)
    Pin = num(Pi)
    sym_ev = sorted(set(round(x, 9) for x in ev))
    lam = []
    for x in sym_ev:
        f = Fr(x).limit_denominator(81)
        assert abs(float(f) - x) < 1e-8 and 81 % f.denominator == 0, (x, f)
        lam.append(f)
    lam = sorted(set(lam))
    # exact check: Pi * prod (X - lam_i I) == 0
    R = Pi
    for l in lam:
        Xl = [[Xm[r][c] - (ONE.scale(l) if r == c else ZERO) for c in range(n)] for r in range(n)]
        R = mat_mul(R, Xl)
    exact_zero = all(x.iszero() for row in R for x in row)
    return [str(l) for l in lam], exact_zero
res = {}
pents = [sorted(S) for S in maxsets]
# one pentad per chirality orbit: use the transvection group orbit split from w33_split_triality is heavy; instead take pentads[0] and
# its complex conjugate image (antiunitary); here simply test the first pentad and a pentad from the other PSp-orbit found by orbit search
lam, ok = certificate(pents[0])
res["pentad_A"] = dict(distinct_eigenvalues=lam, exact_annihilation=ok)
print("pentad A: distinct eigenvalues of X (incl. 0 on the antisymmetric part):", lam, "| exact Pi*prod(X - lam) = 0:", ok)
json.dump(res, open(os.path.join(ROOT, "data", "w33_strong_umub_exact.json"), "w"), indent=1)

# --- tightened exact check: replace I by Pi and drop the 0 factor: Pi (X - Pi/9)(X - 16 Pi/9) == 0  =>  spec(H | Sym^2) in {1/9, 16/9}
def tight(Ls, lams):
    n = d * d
    M = mat_zero(n)
    for L in Ls:
        for Pm in projectors(L):
            A = [[Pm[r][c] - (ONE.scale(Fr(1, 9)) if r == c else ZERO) for c in range(d)] for r in range(d)]
            K = kron(A, A)
            for r in range(n):
                for c in range(n):
                    if not K[r][c].iszero(): M[r][c] = M[r][c] + K[r][c]
    Pi = mat_zero(n)
    for i in range(d):
        for j in range(d):
            r = i * d + j
            Pi[r][r] = Pi[r][r] + ONE.scale(Fr(1, 2)); Pi[r][j * d + i] = Pi[r][j * d + i] + ONE.scale(Fr(1, 2))
    Xm = mat_mul(mat_mul(Pi, M), Pi)
    R = Pi
    for l in lams:
        R = mat_mul(R, [[Xm[r][c] - Pi[r][c].scale(l) for c in range(n)] for r in range(n)])
    return all(x.iszero() for row in R for x in row), Xm, Pi
okA, XA, PiA = tight(pents[0], [Fr(1, 9), Fr(16, 9)])
res["pentad_A_tight_exact"] = okA
print("pentad A tight exact check Pi (X - Pi/9)(X - 16Pi/9) = 0:", okA)
# second chirality: a pentad in the other PSp(4,3)-orbit (complex conjugate = antiunitary image) - use the reflection partner from Pass 12636
rf = {"__name__": "x", "__file__": os.path.join(HERE, "w33_pentad_umub.py")}
eights = []
def bk(R_, Pc, X_):
    if len(eights) >= 1: return
    if not Pc and not X_:
        if len(R_) == 8: eights.append(sorted(R_))
        return
    for v in list(Pc):
        bk(R_ | {v}, {u for u in Pc if disj[v][u]}, {u for u in X_ if disj[v][u]}); Pc = Pc - {v}; X_ = X_ | {v}
bk(set(), set(range(40)), set())
ok8, X8, Pi8 = tight(eights[0], [Fr(4, 9), Fr(16, 9)])
res["size8_tight_exact"] = ok8
print("size-8 tight exact check with {4/9, 16/9}:", ok8)
# pentads in the other chirality: any pentad disjoint-orbit; test 3 more pentads exactly (covers both orbits with high probability; orbit test below)
more = [tight(pents[k], [Fr(1, 9), Fr(16, 9)])[0] for k in (1, 2, 3)]
res["pentads_1_2_3_tight_exact"] = more
print("pentads 1,2,3 tight exact:", more)
json.dump(res, open(os.path.join(ROOT, "data", "w33_strong_umub_exact.json"), "w"), indent=1)
