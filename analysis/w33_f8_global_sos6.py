"""Pass 12673: a GLOBAL degree-6 SOS lower bound for the nine F_8-regulus MUBs of C^64, by symmetry reduction.
Target (psi in C^64 unnormalised, covered Pauli set Ccov, |Ccov| = 567):
    f_c(psi) = |psi|^2 ( sum_{P in Ccov} |<psi|P|psi>|^2 - c |psi|^4 ) >= 0   <=>   64 F >= c on all states.
Certificate: f_c = sum of Hermitian squares of degree-3 polynomials, charge blocks psi psi psi (B3) and psi psi conj(psi) (B1).
Symmetry G = Heisenberg (Pauli) group x| Z_63 (Singer cycle of GL(2,8), acting on the index space F_8^2 = F_64 by permutations;
all of GL(2,8) preserves F, Pass 12671).  An invariant certificate is block-diagonal by Z-character x^y^z = c (blocks related by
X-shifts, so one block c = 0 suffices: B1 = {psi_x psi_y conj psi_{x^y}} (2080), B3 = {psi_x psi_y psi_{x^y}} (715)), and inside
the block by the 63 characters of Z_63 (orbit Fourier vectors).  Coefficient matching is done on orbit sums over classes of degree
(3,3) monomials under shifts x| Z_63:  S_P(kappa) = 64 * 63 * sum_j sum_{O1,O2} H^j_{O1 O2} sum_m e^{-2 pi i j m/63}
[class(o1^H omega^m o2) = kappa],  S_T(kappa) = |kappa| T(mu_kappa).  Solved with Clarabel; any feasible point is a lower bound
(numerical SDP; no rounding here).  Upper limit: degree-6 global <= degree-6 code-space value 2.4967 (Pass 12672) < c8.
usage: py -3 analysis/w33_f8_global_sos6.py"""
import itertools, json, math, os, sys, time
from collections import defaultdict
import numpy as np
import scipy.sparse as sps
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_regulus_constants_q16_q32.py"), encoding="utf-8").read()
gl = {"__name__": "x", "__file__": os.path.join(HERE, "w33_regulus_constants_q16_q32.py")}
exec(src[: src.index("def model(")], gl)
q, mul, trace = gl["field"](3)
C8 = (47 - 32 * math.cos(2 * math.pi / 9)) / 9
pc = lambda n: bin(n).count("1") & 1
t00 = time.time()
# ---------- covered labels (u, v) in this repo's convention, via the CZ-model basis unitaries
Xi = np.array([[1 - 2 * trace(mul(a, b)) for b in range(8)] for a in range(8)], float)
Phi = np.array([[[1 - 2 * trace(mul(t, mul(a, b))) for b in range(8)] for a in range(8)] for t in range(8)], float)
U = [np.eye(64)]
for t in range(8):
    Ut = np.zeros((64, 64))
    for x in range(64):
        e = np.zeros((8, 8)); e.flat[x] = 1; Ut[:, x] = (Xi @ (e * Phi[t]) @ Xi / 8).ravel()
    U.append(Ut)
def pauli(u, v):
    M = np.zeros((64, 64))
    for x in range(64): M[x, x ^ u] = (-1) ** pc(v & (x ^ u))
    return M
Ccov = [(u, v) for u in range(64) for v in range(64) if (u, v) != (0, 0) and any(np.allclose(D := Ut @ pauli(u, v) @ Ut.T, np.diag(np.diag(D))) for Ut in U)]
assert len(Ccov) == 567
h = np.zeros((64, 64))     # h[a][s] = sum_{b : (a,b) covered} (-1)^{b.s}
for (a, b) in Ccov:
    for s_ in range(64): h[a, s_] += (-1) ** pc(b & s_)
print("covered set and h-table ready", round(time.time() - t00), "s", flush=True)
# ---------- Singer cycle omega in GL(2,8) acting on indices x = 8a + b as row vector (a, b) -> (a, b) g
def apply(gm, v):
    return (mul(v[0], gm[0][0]) ^ mul(v[1], gm[1][0]), mul(v[0], gm[0][1]) ^ mul(v[1], gm[1][1]))
def perm_of(gm):
    return np.array([8 * a + b for (a, b) in (apply(gm, (x // 8, x % 8)) for x in range(64))])
def porder(P):
    Q = P.copy(); k = 1
    while not np.array_equal(Q, np.arange(64)): Q = Q[P]; k += 1
    return k
om = None
for a, b, c, d in itertools.product(range(8), repeat=4):
    if mul(a, d) ^ mul(b, c) == 0: continue
    P = perm_of(((a, b), (c, d)))
    if porder(P) == 63: om = P; break
OMP = [np.arange(64)]
for k in range(1, 63): OMP.append(om[OMP[-1]])      # OMP[k][x] = omega^k (x)
OMP = np.array(OMP)
# ---------- monomial blocks (c = 0)
B1 = [(x, y, x ^ y) for x in range(64) for y in range(x, 64)]            # psi_x psi_y conj psi_{x^y}
B3 = sorted({tuple(sorted((x, y, x ^ y))) for x in range(64) for y in range(64)})   # psi_x psi_y psi_{x^y}
assert len(B1) == 2080 and len(B3) == 715
def act1(k, m): x, y, z = (int(OMP[k % 63][i]) for i in m); return (min(x, y), max(x, y), z)
def act3(k, m): return tuple(sorted(int(OMP[k % 63][i]) for i in m))
def orbits(B, act):
    idx = {m: i for i, m in enumerate(B)}; seen = set(); out = []
    for m in B:
        if m in seen: continue
        orb = []; k = 0
        while True:
            mk = act(k, m)
            if mk in orb: break
            orb.append(mk); k += 1
        seen |= set(orb); out.append((m, 63 // len(orb) if 63 % len(orb) == 0 else None, len(orb)))
    return out
O1 = orbits(B1, act1); O3 = orbits(B3, act3)
assert all(s is not None for _, s, _ in O1 + O3)
print("orbits: B1", len(O1), " B3", len(O3), round(time.time() - t00), "s", flush=True)
# monomial products -> (barred multiset, unbarred multiset)
def prod1(m1, m2):  # conj(psi_x psi_y conj psi_z) * psi_x' psi_y' conj psi_z'  = conj psi_x conj psi_y psi_z psi_x' psi_y' conj psi_z'
    (x, y, z), (x2, y2, z2) = m1, m2
    return (tuple(sorted((x, y, z2))), tuple(sorted((z, x2, y2))))
def prod3(m1, m2):
    return (tuple(m1), tuple(m2))
def canon(mono):
    """canonical representative of a (barred, unbarred) monomial under X-shifts x| Z_63 (and record nothing else)"""
    Bt, Ut_ = mono; best = None
    for k in range(63):
        P = OMP[k]
        b = [int(P[i]) for i in Bt]; u = [int(P[i]) for i in Ut_]
        for s_ in set(b):
            cand = (tuple(sorted(i ^ s_ for i in b)), tuple(sorted(i ^ s_ for i in u)))
            if best is None or cand < best: best = cand
    return best
CAN = {}
def ccanon(mono):
    r = CAN.get(mono)
    if r is None: r = canon(mono); CAN[mono] = r
    return r
# ---------- coefficient structure  A[j][(O1,O2)] -> {kappa: complex}
zeta = np.exp(-2j * np.pi / 63)
def build(Ol, act, prod):
    blocks = {j: [i for i, (_, s, _) in enumerate(Ol) if j % s == 0] for j in range(63)}
    coef = defaultdict(lambda: defaultdict(complex))      # (j, i1, i2) -> kappa -> value
    for i1, (o1, s1, _) in enumerate(Ol):
        for i2, (o2, s2, _) in enumerate(Ol):
            km = [ccanon(prod(o1, act(m, o2))) for m in range(63)]
            for j in range(63):
                if j % s1 or j % s2: continue
                d_ = coef[(j, i1, i2)]
                for m, kap in enumerate(km): d_[kap] += zeta ** (j * m)
    return blocks, coef
t0 = time.time()
blk1, coef1 = build(O1, act1, prod1); print("B1 coefficient map", round(time.time() - t0), "s, classes so far", len(set(CAN.values())), flush=True)
blk3, coef3 = build(O3, act3, prod3); print("B3 coefficient map", round(time.time() - t0), "s", flush=True)
classes = sorted({k for d_ in list(coef1.values()) + list(coef3.values()) for k in d_})
cidx = {k: i for i, k in enumerate(classes)}; NK = len(classes)
print("classes:", NK, flush=True)
# ---------- target per class: S_T = |kappa| T(mu), T = A(mu) - c B(mu)
def orbit_size(mu):
    Bt, Ut_ = mu; seen = set()
    for k in range(63):
        P = OMP[k]; b = [int(P[i]) for i in Bt]; u = [int(P[i]) for i in Ut_]
        for s_ in range(64): seen.add((tuple(sorted(i ^ s_ for i in b)), tuple(sorted(i ^ s_ for i in u))))
    return len(seen)
def tcoef(mu):
    Bt, Ut_ = mu; tuples = set()
    for pb in set(itertools.permutations(Bt)):
        for pu in set(itertools.permutations(Ut_)):
            x, ya, w = pb; xa, y, w2 = pu
            if w != w2: continue
            a = x ^ xa
            if ya != y ^ a: continue
            tuples.add((a, x, y, w))
    A = sum(h[a, x ^ y] for (a, x, y, w) in tuples)
    Bv = 0
    if tuple(sorted(Bt)) == tuple(sorted(Ut_)):
        from collections import Counter
        cnt = Counter(Bt); Bv = math.factorial(3) / math.prod(math.factorial(v) for v in cnt.values())
    return A, Bv
t0 = time.time()
TA = np.zeros(NK); TB = np.zeros(NK)
for k, mu in enumerate(classes):
    sz = orbit_size(mu); A_, B_ = tcoef(mu); TA[k] = sz * A_; TB[k] = sz * B_
print("target classes computed", round(time.time() - t0), "s", flush=True)
# classes of the target not reachable by the Gram blocks?
# (every degree-(3,3) Z-character-0 class with nonzero target must be in `classes`; check a random sample)
# ---------- SDP (Clarabel): variables c, real embeddings of H^j (B1 and B3 blocks)
import clarabel
USE_SCS = "--clarabel" not in sys.argv
def sidx(i, j_, n_):  # SCS: lower triangle column-major; Clarabel: upper triangle column-major; off-diagonal scaled sqrt2
    if USE_SCS:
        if i < j_: i, j_ = j_, i
        return j_ * n_ - j_ * (j_ - 1) // 2 + (i - j_), (1.0 if i == j_ else 1 / math.sqrt(2))
    if i > j_: i, j_ = j_, i
    return j_ * (j_ + 1) // 2 + i, (1.0 if i == j_ else 1 / math.sqrt(2))
var_off = 1; cones = []; rowsE, colsE, valsE = [], [], []
blocks_meta = []
for name, blk, coef in (("B1", blk1, coef1), ("B3", blk3, coef3)):
    for j in range(63):
        mem = blk[j]; n_ = len(mem)
        if n_ == 0: continue
        N2 = 2 * n_; nv = N2 * (N2 + 1) // 2
        blocks_meta.append((name, j, n_, var_off))
        for a_, i1 in enumerate(mem):
            for b_, i2 in enumerate(mem):
                d_ = coef.get((j, i1, i2))
                if not d_: continue
                for kap, val in d_.items():
                    r = cidx[kap]; w = 64 * 63 * val      # S_P contribution: w * H[a,b],  H = Xr + i Xi
                    # H[a,b] = (Y[a,b] + Y[n+a, n+b])/2 + i (Y[n+a, b] - Y[n+b, a])/2
                    for (ii, jj, cr, ci) in ((a_, b_, 0.5, 0), (n_ + a_, n_ + b_, 0.5, 0), (n_ + a_, b_, 0, 0.5), (n_ + b_, a_, 0, -0.5)):
                        kk, sc = sidx(ii, jj, N2)
                        coefc = (cr + 1j * ci) * w * sc       # contribution to S_P = coefc * y
                        if coefc.real: rowsE.append(r); colsE.append(var_off + kk); valsE.append(coefc.real)
                        if coefc.imag: rowsE.append(NK + r); colsE.append(var_off + kk); valsE.append(coefc.imag)
        cones.append(N2); var_off += nv
NV = var_off
# equality: S_P(y) + c TB = TA  (real rows), imag rows: S_P imag = 0 (target real-symmetric per class pair handled by both kappa, conj)
for r in range(NK): rowsE.append(r); colsE.append(0); valsE.append(TB[r])
Aeq = sps.csr_matrix((valsE, (rowsE, colsE)), shape=(2 * NK, NV)); beq = np.concatenate([TA, np.zeros(NK)])
Apsd = -sps.eye(NV, format="csr")[1:]
A = sps.vstack([Aeq, Apsd]).tocsc(); b = np.concatenate([beq, np.zeros(NV - 1)])
qv = np.zeros(NV); qv[0] = -1.0
print(f"SDP: {NV} variables, {2 * NK} equalities, {len(cones)} PSD blocks (max size {max(cones)})", flush=True)
t0 = time.time()
if USE_SCS:
    import scs
    sol = scs.SCS(dict(A=A, b=b, c=qv), dict(z=2 * NK, s=cones), eps_abs=1e-8, eps_rel=1e-8, max_iters=200000, verbose=False).solve()
    val = float(sol["x"][0]); status = sol["info"]["status"]
else:
    P = sps.csc_matrix((NV, NV))
    cl = [clarabel.ZeroConeT(2 * NK)] + [clarabel.PSDTriangleConeT(n_) for n_ in cones]
    st = clarabel.DefaultSettings(); st.verbose = False; st.max_iter = 400
    sol = clarabel.DefaultSolver(P, qv, A, b, cl, st).solve(); val = float(sol.x[0]); status = str(sol.status)
print(f"GLOBAL degree-6 SOS bound: c >= {val:.10f}  (status {status}, {time.time() - t0:.0f}s); c8 = {C8:.10f}; previous best exact 2.0818", flush=True)
class _Sol: pass
sol = _Sol(); sol.status = status
json.dump(dict(bound=val, status=str(sol.status), c8=C8, n_classes=NK, n_vars=NV, blocks=[(a, j, n_) for a, j, n_, _ in blocks_meta],
               orbits=dict(B1=len(O1), B3=len(O3)), seconds=round(time.time() - t00)),
          open(os.path.join(ROOT, "data", "w33_f8_global_sos6.json"), "w"), indent=1)
