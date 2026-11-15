"""Pass 12673: GLOBAL degree-6 SOS lower bound for the nine F_8-regulus MUBs of C^64, reduced by the Heisenberg group and by
Gamma = GammaL(1,64) = Z_63 x| Z_6 (Singer cycle omega of GL(2,8), the F_8-linear Frobenius x -> x^8 and the coordinatewise
Frobenius (a,b) -> (a^2,b^2) of F_8^2; all act on the index set by permutations and preserve F -- checked numerically).
Second formulation (the first, w33_f8_global_sos6.py, had nnz(A) = 3.6e7): variables are values gamma_rho of the invariant Gram
matrix on Gamma-orbits rho of monomial PAIRS (so each variable feeds exactly one coefficient class: sparse equalities), and PSD
is imposed on one Z_63-Fourier block per orbit of characters under j -> k j (the others are unitarily equivalent).
  f_c = |psi|^2 ( sum_{P in Ccov} |<psi|P|psi>|^2 - c |psi|^4 ) = sum_a shift_a ( m_B1^H G1 m_B1 + m_B3^H G3 m_B3 ),
  S_P(kappa) = 64 sum_{rho -> kappa} |rho| gamma_rho,  S_T(kappa) = |kappa| T(mu_kappa),
  M^j_{O1 O2} = sum_m zeta^{j m} G_{o1, omega^m o2} >= 0  (orbits O with stabiliser order s_O | j).
Numerical SDP (SCS); no rounding.  Ceiling: global degree-6 <= code-space degree-6 = 2.4967 < c8 (Pass 12672).
usage: py -3 analysis/w33_f8_global_sos6_v2.py"""
import itertools, json, math, os, sys, time
from collections import Counter, defaultdict
from math import gcd
import numpy as np
import scipy.sparse as sps
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
src = open(os.path.join(HERE, "w33_regulus_constants_q16_q32.py"), encoding="utf-8").read()
gl = {"__name__": "x", "__file__": os.path.join(HERE, "w33_regulus_constants_q16_q32.py")}
exec(src[: src.index("rng = np.random")], gl)
K = int(os.environ.get("REG_K", "3"))
q, mul, trace = gl["field"](K); _, fg = gl["model"](K)
D = q * q; N1 = D - 1
C8 = (47 - 32 * math.cos(2 * math.pi / 9)) / 9
pc = lambda n: bin(n).count("1") & 1
t00 = time.time(); log = lambda *a: print(*a, f"[{time.time() - t00:.0f}s]", flush=True)
# ---------- covered set, h table
Xi = np.array([[1 - 2 * trace(mul(a, b)) for b in range(q)] for a in range(q)], float)
Phi = np.array([[[1 - 2 * trace(mul(t, mul(a, b))) for b in range(q)] for a in range(q)] for t in range(q)], float)
U = [np.eye(D)]
for t in range(q):
    Ut = np.zeros((D, D))
    for x in range(D):
        e = np.zeros((q, q)); e.flat[x] = 1; Ut[:, x] = (Xi @ (e * Phi[t]) @ Xi / q).ravel()
    U.append(Ut)
def pauli(u, v):
    M = np.zeros((D, D))
    for x in range(D): M[x, x ^ u] = (-1) ** pc(v & (x ^ u))
    return M
Ccov = [(u, v) for u in range(D) for v in range(D) if (u, v) != (0, 0) and any(np.allclose(Dm := Ut @ pauli(u, v) @ Ut.T, np.diag(np.diag(Dm))) for Ut in U)]
assert len(Ccov) == (q + 1) * N1
CONTROL = os.environ.get("CONTROL", "")
if CONTROL == "all": Ccov = [(u, v) for u in range(D) for v in range(D) if (u, v) != (0, 0)]      # exact answer N1
elif CONTROL == "zgroup": Ccov = [(0, v) for v in range(1, D)]                                    # exact answer 0
h = np.zeros((D, D))
for (a, b) in Ccov:
    for s_ in range(D): h[a, s_] += (-1) ** pc(b & s_)
log("covered set ready")
# ---------- the group: omega (order N1) normalised by fro and by an F_8-linear involution-type nu
def apply(gm, v): return (mul(v[0], gm[0][0]) ^ mul(v[1], gm[1][0]), mul(v[0], gm[0][1]) ^ mul(v[1], gm[1][1]))
def perm_of(gm): return np.array([q * a + b for (a, b) in (apply(gm, (x // q, x % q)) for x in range(D))])
def porder(P):
    Q = P.copy(); k = 1
    while not np.array_equal(Q, np.arange(D)): Q = Q[P]; k += 1
    return k
F_PERM = lambda A: fg(np.concatenate([(A / np.linalg.norm(A)).real, (A / np.linalg.norm(A)).imag]))[0]
fro = np.array([q * mul(x // q, x // q) + mul(x % q, x % q) for x in range(D)])
GLs = [perm_of(((a, b), (c, d))) for a, b, c, d in itertools.product(range(q), repeat=4) if mul(a, d) ^ mul(b, c)]
inv = lambda P: np.argsort(P)
comp = lambda P, Q: P[Q]              # (P o Q)[x] = P[Q[x]]
def powers(P):
    out = [np.arange(D)]
    for _ in range(N1 - 1): out.append(comp(P, out[-1]))
    return out
om = None
for P in GLs:
    if porder(P) != N1: continue
    pw = powers(P); conj_ = comp(comp(fro, P), inv(fro))
    ks = [k for k in range(N1) if np.array_equal(pw[k], conj_)]
    if ks: om, OMP, kfro = P, pw, ks[0]; break
USE_FRO = om is not None
if not USE_FRO:      # no Singer cycle normalised by the coordinatewise Frobenius in these coordinates: use <omega, nu> only
    om = next(P for P in GLs if porder(P) == N1); OMP = powers(om); kfro = 1
nu, knu = None, None
for P in GLs:
    c_ = comp(comp(P, om), inv(P))
    if np.array_equal(c_, OMP[q]): nu, knu = P, q; break
assert nu is not None
rng = np.random.default_rng(7)
for P in (fro, nu, om):
    A = rng.standard_normal(D) + 1j * rng.standard_normal(D); assert abs(F_PERM(A) - F_PERM(A[P])) < 1e-12
# coset representatives phi of <omega> in Gamma and their twists k(phi): phi omega phi^-1 = omega^k
PHI = []
for e in range(K if USE_FRO else 1):
    for f in range(2):
        P = np.arange(D); k = 1
        for _ in range(e): P = comp(fro, P); k = k * kfro % N1
        for _ in range(f): P = comp(nu, P); k = k * knu % N1
        PHI.append((P, k))
GAMMA = [comp(OMP[a], P) for P, _ in PHI for a in range(N1)]
log(f"Gamma: |<omega>| = N1, fro twist {kfro}, nu twist {knu}, |Gamma| = {len({tuple(g) for g in GAMMA})}")
# ---------- monomial blocks and Z_63 orbits
B1 = [(x, y, x ^ y) for x in range(D) for y in range(x, D)]
B3 = sorted({tuple(sorted((x, y, x ^ y))) for x in range(D) for y in range(D)})
def act1(P, m): x, y, z = (int(P[i]) for i in m); return (min(x, y), max(x, y), z)
def act3(P, m): return tuple(sorted(int(P[i]) for i in m))
def z63_orbits(B, act):
    loc = {}; reps = []
    for m in B:
        if m in loc: continue
        orb = []
        for k in range(N1):
            mk = act(OMP[k], m)
            if mk == m and k > 0: break
            orb.append(mk)
        O = len(reps); reps.append((m, N1 // len(orb), len(orb)))
        for k, mk in enumerate(orb): loc[mk] = (O, k)
    return reps, loc
def prod1(m1, m2):
    (x, y, z), (x2, y2, z2) = m1, m2
    return (tuple(sorted((x, y, z2))), tuple(sorted((z, x2, y2))))
def prod3(m1, m2): return (tuple(m1), tuple(m2))
def canon(mono):
    Bt, Ut_ = mono; best = None
    for P in GAMMA:
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


class Block:
    def __init__(self, name, B, act, prod):
        self.name, self.act, self.prod = name, act, prod
        self.reps, self.loc = z63_orbits(B, act)
        R = self.reps; nO = len(R)
        # Z63 pair orbits (O1, O2, m mod g12)
        self.g12 = [[gcd(R[i][2], R[j][2]) for j in range(nO)] for i in range(nO)]
        pairs = [(i, j, m) for i in range(nO) for j in range(nO) for m in range(self.g12[i][j])]
        pid = {p: n for n, p in enumerate(pairs)}
        size = [N1 // gcd(R[i][1], R[j][1]) for (i, j, m) in pairs]
        # union-find under the coset representatives phi
        par = list(range(len(pairs)))
        def find(a):
            while par[a] != a: par[a] = par[par[a]]; a = par[a]
            return a
        for P, k in PHI[1:]:
            for n, (i, j, m) in enumerate(pairs):
                u1 = R[i][0]; u2 = act(OMP[m % N1], R[j][0])
                i2, a1 = self.loc[act(P, u1)]; j2, a2 = self.loc[act(P, u2)]
                m2 = (a2 - a1) % self.g12[i2][j2]
                ra, rb = find(n), find(pid[(i2, j2, m2)])
                if ra != rb: par[ra] = rb
        roots = sorted({find(n) for n in range(len(pairs))}); rid = {r: n for n, r in enumerate(roots)}
        self.orb_of_pair = [rid[find(n)] for n in range(len(pairs))]
        self.orb_size = [0] * len(roots)
        for n in range(len(pairs)): self.orb_size[self.orb_of_pair[n]] += size[n]
        self.pairs, self.pid = pairs, pid
        # conjugate orbit: (i, j, m) -> (j, i, -m)
        self.orb_conj = [None] * len(roots)
        for n, (i, j, m) in enumerate(pairs):
            o = self.orb_of_pair[n]; oc = self.orb_of_pair[pid[(j, i, (-m) % self.g12[j][i])]]
            assert self.orb_conj[o] in (None, oc); self.orb_conj[o] = oc
        # class of each orbit (via one representative pair)
        rep_pair = {}
        for n in range(len(pairs)): rep_pair.setdefault(self.orb_of_pair[n], pairs[n])
        self.orb_class = [None] * len(roots)
        for o, (i, j, m) in rep_pair.items():
            self.orb_class[o] = ccanon(prod(R[i][0], act(OMP[m % N1], R[j][0])))
        log(f"{name}: {nO} Z63-orbits of monomials, {len(pairs)} Z63 pair-orbits, {len(roots)} Gamma pair-orbits")


blk1 = Block("B1", B1, act1, prod1); blk3 = Block("B3", B3, act3, prod3)
classes = sorted(set(blk1.orb_class) | set(blk3.orb_class)); cidx = {k: i for i, k in enumerate(classes)}; NK = len(classes)
log(f"coefficient classes: {NK}")
# ---------- target
def orbit_size(mu):
    Bt, Ut_ = mu; seen = set()
    for P in GAMMA:
        b = [int(P[i]) for i in Bt]; u = [int(P[i]) for i in Ut_]
        for s_ in range(D): seen.add((tuple(sorted(i ^ s_ for i in b)), tuple(sorted(i ^ s_ for i in u))))
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
    A_ = sum(h[a, x ^ y] for (a, x, y, w) in tuples); B_ = 0
    if tuple(sorted(Bt)) == tuple(sorted(Ut_)):
        cnt = Counter(Bt); B_ = 6 / math.prod(math.factorial(v) for v in cnt.values())
    return A_, B_
TA = np.zeros(NK); TB = np.zeros(NK)
for k, mu in enumerate(classes):
    sz = orbit_size(mu); A_, B_ = tcoef(mu); TA[k] = sz * A_; TB[k] = sz * B_
log("target ready")
# ---------- variables: per block, per conj-pair of Gamma pair-orbits: real (self-conjugate) or complex
var = 1; vmap = {}           # (block name, orbit) -> (col_re, col_im or None, sign_im)
for blk in (blk1, blk3):
    for o in range(len(blk.orb_size)):
        if (blk.name, o) in vmap: continue
        oc = blk.orb_conj[o]
        if oc == o: vmap[(blk.name, o)] = (var, None, 0); var += 1
        else:
            vmap[(blk.name, o)] = (var, var + 1, 1); vmap[(blk.name, oc)] = (var, var + 1, -1); var += 2
NVAR = var
rows, cols, vals = [], [], []
for blk in (blk1, blk3):
    for o, kap in enumerate(blk.orb_class):
        r = cidx[kap]; w = D * blk.orb_size[o]; cre, cim, sg = vmap[(blk.name, o)]
        rows.append(r); cols.append(cre); vals.append(w)                     # Re S_P
        if cim is not None: rows.append(NK + r); cols.append(cim); vals.append(sg * w)   # Im S_P
for r in range(NK): rows.append(r); cols.append(0); vals.append(TB[r])
Aeq = sps.csr_matrix((vals, (rows, cols)), shape=(2 * NK, NVAR)); beq = np.concatenate([TA, np.zeros(NK)])
# ---------- PSD blocks: one j per orbit of j -> k j (k in the twists of the coset reps)
twists = sorted({k for _, k in PHI})
jrep = []; seenj = set()
for j in range(N1):
    if j in seenj: continue
    orbj = {(k * j) % N1 for k in twists} | {(k * k2 * j) % N1 for k in twists for k2 in twists}
    seenj |= orbj; jrep.append(j)
zeta = np.exp(2j * np.pi / N1)
def sidx(i, j_, n_):  # SCS lower-triangular column-major, off-diagonal scaled sqrt2
    if i < j_: i, j_ = j_, i
    return j_ * n_ - j_ * (j_ - 1) // 2 + (i - j_), (1.0 if i == j_ else 1 / math.sqrt(2))
prow, pcol, pval = [], [], []; cones = []; off = 0
for blk in (blk1, blk3):
    R = blk.reps
    for j in jrep:
        mem = [i for i, (_, s, _) in enumerate(R) if j % s == 0]
        n_ = len(mem)
        if n_ == 0: continue
        N2 = 2 * n_
        for a_, i1 in enumerate(mem):
            for b_, i2 in enumerate(mem):
                # M[a,b] = sum_m zeta^{jm} gamma(orbit of (i1, i2, m mod g)) ; collect coefficients on (Re, Im) of variables
                acc = defaultdict(complex)
                g = blk.g12[i1][i2]
                for m in range(N1):
                    o = blk.orb_of_pair[blk.pid[(i1, i2, m % g)]]
                    cre, cim, sg = vmap[(blk.name, o)]
                    z = zeta ** (j * m)
                    acc[(cre, "re")] += z                    # gamma = Re + i sg Im
                    if cim is not None: acc[(cim, "im")] += 1j * sg * z
                # real embedding entries: Y[a,b] = Re M, Y[n+a, n+b] = Re M, Y[n+a, b] = Im M
                for (col, _), coef in acc.items():
                    for (ii, jj, part) in ((a_, b_, "re"), (n_ + a_, n_ + b_, "re"), (n_ + a_, b_, "im")):
                        if ii < jj: continue                 # lower triangle only (Y symmetric)
                        v = coef.real if part == "re" else coef.imag
                        if abs(v) < 1e-12: continue
                        k_, sc = sidx(ii, jj, N2)
                        prow.append(off + k_); pcol.append(col); pval.append(-v * (math.sqrt(2) if ii != jj else 1.0))   # s = svec(Y) = -A x
        cones.append(N2); off += N2 * (N2 + 1) // 2
Apsd = sps.csr_matrix((pval, (prow, pcol)), shape=(off, NVAR))
A = sps.vstack([Aeq, Apsd]).tocsc(); b = np.concatenate([beq, np.zeros(off)])
qv = np.zeros(NVAR); qv[0] = -1.0
log(f"SDP: {NVAR} variables, {2 * NK} equalities, {len(cones)} PSD blocks (max {max(cones)}), nnz(A) = {A.nnz}")
import scs
sol = scs.SCS(dict(A=A, b=b, c=qv), dict(z=2 * NK, s=cones), eps_abs=float(os.environ.get("SCS_EPS", "1e-7")),
              eps_rel=float(os.environ.get("SCS_EPS", "1e-7")), max_iters=int(os.environ.get("SCS_ITERS", "100000")),
              verbose=bool(os.environ.get("SCS_VERBOSE"))).solve()
val = float(sol["x"][0]); status = sol["info"]["status"]
log(f"GLOBAL degree-6 SOS bound: 64F >= {val:.10f}  (status {status}); c8 = {C8:.10f}; previous best global 2.0818")
json.dump(dict(control=CONTROL, bound=val, status=status, c8=C8, n_classes=NK, n_vars=NVAR, nnz=int(A.nnz), cones=cones, jreps=jrep,
               gamma_order=len({tuple(g) for g in GAMMA}), seconds=round(time.time() - t00)),
          open(os.path.join(ROOT, "data", "w33_f8_global_sos6" + ("" if K == 3 else f"_q{q}") + ("_control_" + CONTROL if CONTROL else "") + ".json"), "w"), indent=1)
