"""Pass 12674: SOS lower bounds for the F_8 regulus objective on Pauli code spaces, in the EFFECTIVE n'-qubit model.
For an isotropic uncovered Pauli group T (rank r) the code-space objective is c(psi) = sum_{(x,z) != 0} n(x,z) <E_{x,z}>^2 / |psi|^4
over psi in C^{2^{n'}}, n' = 6 - r, where (x,z) are standard symplectic coordinates of T^perp/T and n(x,z) counts covered Paulis
in the coset (Pass 12672 §1).  T: rank 3 (n' = 3, 8-dim); S: rank 2 (n' = 4, the 16-dim 'common code' of the other track).
SOS of total degree 2k:  |psi|^{2(k-2)} (sum n <E>^2 - c |psi|^4) = sum over charge blocks of m^H G m, reduced by the n'-qubit Pauli
group: G block-diagonal by Z-character chi = xor of the monomial's indices; X-shifts relate chi-blocks (k odd: one block suffices)
or act inside them (k even: Fourier over the shift group).  Variables live on shift-orbits of monomial pairs (sparse coefficient
matching on shift classes of degree-(k,k) monomials).  Validation: the minimum of the effective objective (random starts) equals c8,
and the T, degree-6 bound must reproduce the code-space value 2.4967 of Pass 12672 (different code).
usage: py -3 analysis/w33_f8_codespace_effective_sos.py {T|S} k"""
import collections, itertools, json, math, os, sys, time
from math import factorial
import numpy as np
import scipy.sparse as sps
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
lsrc = open(os.path.join(HERE, "w33_f8_pauli_stabiliser_ladder.py"), encoding="utf-8").read()
gl = {"__name__": "x", "__file__": os.path.join(HERE, "w33_f8_pauli_stabiliser_ladder.py")}
exec(lsrc[: lsrc.index("res = {}")], gl)
covered, comm, C8 = gl["covered"], gl["comm"], gl["C8"]
WHICH = sys.argv[1] if len(sys.argv) > 1 else "T"; KDEG = int(sys.argv[2]) if len(sys.argv) > 2 else 3
t00 = time.time(); log = lambda *a: print(*a, f"[{time.time() - t00:.0f}s]", flush=True)
gens = [(12, 53), (53, 33)] + ([(1, 6)] if WHICH == "T" else [])
if os.environ.get("GENS"): gens = [tuple(int(x) for x in g.split(",")) for g in os.environ["GENS"].split(";")]   # e.g. type-B stabiliser
vec = lambda k: (k[0] << 6) | k[1]; lab = lambda v: (v >> 6, v & 63)
def span(vs):
    out = {0}
    for v in vs: out |= {x ^ v for x in out}
    return out
Tset = span([vec(g) for g in gens]); r = len(gens); nq = 6 - r; N = 1 << nq
form = lambda a, b: 0 if comm(lab(a), lab(b)) else 1
Tperp = [v for v in range(1 << 12) if all(form(v, t) == 0 for t in Tset)]
assert len(Tperp) == 1 << (12 - r)
# complement of T inside T^perp (2 nq vectors), then symplectic basis of the quotient
def rank_ok(basis, v):
    piv = []
    for b in basis + [v]:
        x = b
        for p in piv: x = min(x, x ^ p)
        if x == 0: return False
        piv.append(x); piv.sort(reverse=True)
    return True
comp_ = []; base = [vec(g) for g in gens]
for v in Tperp:
    if len(comp_) == 2 * nq: break
    if rank_ok(base + comp_, v): comp_.append(v)
E_, F_ = [], []; rem = list(comp_)
def sform(a, b): return form(a, b)
pool = [v for v in Tperp]
while len(E_) < nq:
    e = next(v for v in pool if v not in Tset and all(sform(v, x) == 0 for x in E_ + F_) and rank_ok(base + E_ + F_, v))
    f = next(v for v in pool if sform(e, v) == 1 and all(sform(v, x) == 0 for x in E_ + F_))
    E_.append(e); F_.append(f)
std = lambda v: (sum(sform(v, F_[i]) << i for i in range(nq)), sum(sform(E_[i], v) << i for i in range(nq)))
weights = collections.Counter()
for v in Tperp:
    if v in Tset: continue
    if covered(lab(v)): weights[std(v)] += 1
assert sum(1 for v in Tset if v and covered(lab(v))) == 0
nw = np.zeros((N, N))
for (x, z), w in weights.items(): nw[x, z] = w
log(f"{WHICH}: n' = {nq}, covered Paulis in T^perp: {sum(weights.values())}, weight histogram {sorted(collections.Counter(weights.values()).items())}")
pcount = lambda n: bin(n).count("1")
def ceff(psi):
    psi = psi / np.linalg.norm(psi); tot = 0.0
    for (x, z), w in weights.items():
        ph = np.array([(-1) ** (pcount(z & (y ^ x)) & 1) for y in range(N)])
        tot += w * abs(np.vdot(psi, ph * psi[np.arange(N) ^ x])) ** 2
    return tot
rng = np.random.default_rng(1)
mins = sorted(minimize(lambda w: ceff(w[:N] + 1j * w[N:]), rng.standard_normal(2 * N), method="BFGS").fun for _ in range(12))
log(f"effective-model minimum over 12 starts: {mins[0]:.10f}  (c8 = {C8:.10f})")
assert abs(mins[0] - C8) < 1e-6
h = np.zeros((N, N))
for x in range(N):
    for s_ in range(N): h[x, s_] = sum(nw[x, z] * (-1) ** (pcount(z & s_) & 1) for z in range(N))
# ---------------- monomials and blocks
def multisets(n_, size): return list(itertools.combinations_with_replacement(range(n_), size))
xorall = lambda t: __import__("functools").reduce(lambda a, b: a ^ b, t, 0)
shiftm = lambda m, s: (tuple(sorted(i ^ s for i in m[0])), tuple(sorted(i ^ s for i in m[1])))
blocks = []                                     # list of (a, b, monomials in this charge) ; a = #unbarred, b = #barred
for a in range(KDEG, (KDEG - 1) // 2, -1):
    b = KDEG - a
    if a < b: continue
    mons = [(U, B) for U in multisets(N, a) for B in multisets(N, b)]
    blocks.append((a, b, mons))
def prod(m1, m2):   # conj(t^U1 tbar^B1) * t^U2 tbar^B2 : barred = U1 + B2, unbarred = B1 + U2
    return (tuple(sorted(m1[0] + m2[1])), tuple(sorted(m1[1] + m2[0])))
def canon(mu):
    best = None
    for s_ in set(mu[0]) | ({0} if not mu[0] else set()):
        c_ = shiftm(mu, s_)
        if best is None or c_ < best: best = c_
    return best
var_rows = collections.defaultdict(list)       # class -> list of (var, weight, conj_flag)
cones = []; psd_entries = []; CONE_META = []   # CONE_META: per cone, (kind, xi, member monomial reps, stabiliser sizes)                    # psd_entries: list of (cone_index, i, j, list of (var, coeff complex))
VARS = {}                                       # canonical pair-orbit key -> var index; conj handled by key ordering
def pair_key(m1, m2):                            # canonical rep of the shift orbit of the pair
    best = None
    for s_ in range(N):
        k_ = (shiftm(m1, s_), shiftm(m2, s_))
        if best is None or k_ < best: best = k_
    return best
def pair_orbit_size(m1, m2):
    return len({(shiftm(m1, s_), shiftm(m2, s_)) for s_ in range(N)})
def getvar(m1, m2):
    k1 = pair_key(m1, m2); k2 = pair_key(m2, m1)
    if k1 <= k2:
        if k1 not in VARS: VARS[k1] = len(VARS)
        return VARS[k1], (k1 == k2), False
    if k2 not in VARS: VARS[k2] = len(VARS)
    return VARS[k2], False, True                 # this pair is the conjugate of the stored one
odd = (KDEG % 2 == 1)
for (a, b, mons) in blocks:
    chi = collections.defaultdict(list)
    for m in mons: chi[xorall(m[0]) ^ xorall(m[1])].append(m)
    if odd:                                      # one block (chi = 0); shifts relate blocks
        B0 = chi[0]; L = len(B0)
        ci = len(cones); cones.append(L); CONE_META.append(("odd", None, list(B0), [1] * L))
        for i, m1 in enumerate(B0):
            for j, m2 in enumerate(B0):
                if j < i: continue
                v, selfc, cj = getvar(m1, m2)
                psd_entries.append((ci, i, j, [(v, 1.0, cj)]))
        # coefficient matching: every pair (m1, m2) of block chi=0 represents a shift orbit of size N
        for m1 in B0:
            for m2 in B0:
                v, selfc, cj = getvar(m1, m2); var_rows[canon(prod(m1, m2))].append((v, N, cj))
    else:                                        # blocks per chi; Fourier over shifts inside
        for c_, Bc in chi.items():
            # shift orbits inside the block
            seen = set(); orbs = []
            for m in Bc:
                if m in seen: continue
                o = {shiftm(m, s_) for s_ in range(N)}; seen |= o
                stab = [s_ for s_ in range(N) if shiftm(m, s_) == m]; orbs.append((m, stab))
            for xi in range(N):
                mem = [(m, st) for (m, st) in orbs if all(pcount(xi & s_) % 2 == 0 for s_ in st)]
                if not mem: continue
                ci = len(cones); cones.append(len(mem)); CONE_META.append(("even", xi, [o for o, _ in mem], [len(st) for _, st in mem]))
                for i, (o1, _) in enumerate(mem):
                    for j, (o2, _) in enumerate(mem):
                        if j < i: continue
                        terms = []
                        for s_ in range(N):
                            v, selfc, cj = getvar(o1, shiftm(o2, s_)); terms.append((v, (-1) ** (pcount(xi & s_) % 2), cj))
                        psd_entries.append((ci, i, j, terms))
            # coefficient matching: each shift orbit of pairs in this block, once
            done = set()
            for m1 in Bc:
                for m2 in Bc:
                    kk = pair_key(m1, m2)
                    if kk in done: continue
                    done.add(kk); v, selfc, cj = getvar(m1, m2)
                    var_rows[canon(prod(m1, m2))].append((v, pair_orbit_size(m1, m2), cj))
log(f"degree {2 * KDEG}: {len(VARS)} complex pair-orbit variables, {len(cones)} PSD blocks (max {max(cones)}), {len(var_rows)} classes")
# ---------------- target
def orbit_size(mu): return len({shiftm(mu, s_) for s_ in range(N)})
def tcoef(mu):
    Bt, Ut = mu; k = KDEG; tuples = set()
    for pb in set(itertools.permutations(Bt)):
        for pu in set(itertools.permutations(Ut)):
            y, wx = pb[0], pb[1]; yx, w = pu[0], pu[1]
            if tuple(sorted(pb[2:])) != tuple(sorted(pu[2:])) or pb[2:] != pu[2:]: continue
            x = y ^ yx
            if wx != w ^ x: continue
            tuples.add((x, y, w) + tuple(pb[2:]))
    A_ = sum(h[x, y ^ w] for (x, y, w, *rest) in tuples)
    B_ = 0
    if Bt == Ut:
        cnt = collections.Counter(Bt); B_ = factorial(k) / math.prod(factorial(v) for v in cnt.values())
    return A_, B_
classes = sorted(var_rows); cidx = {c_: i for i, c_ in enumerate(classes)}; NK = len(classes)
TA = np.zeros(NK); TB = np.zeros(NK)
for i, mu in enumerate(classes):
    sz = orbit_size(mu); A_, B_ = tcoef(mu); TA[i] = sz * A_; TB[i] = sz * B_
log("target ready")
# ---------------- SCS
NV = 1 + 2 * len(VARS)                            # c, (Re, Im) per variable
col = lambda v, part: 1 + 2 * v + part
rows, cols_, vals = [], [], []
for kap, lst in var_rows.items():
    rr = cidx[kap]
    for (v, w, cj) in lst:
        rows.append(rr); cols_.append(col(v, 0)); vals.append(w)
        rows.append(NK + rr); cols_.append(col(v, 1)); vals.append(-w if cj else w)
for i in range(NK): rows.append(i); cols_.append(0); vals.append(TB[i])
Aeq = sps.csr_matrix((vals, (rows, cols_)), shape=(2 * NK, NV)); beq = np.concatenate([TA, np.zeros(NK)])
def sidx(i, j_, n_):
    if i < j_: i, j_ = j_, i
    return j_ * n_ - j_ * (j_ - 1) // 2 + (i - j_), (1.0 if i == j_ else 1 / math.sqrt(2))
offs = []; o = 0
for L in cones: offs.append(o); o += (2 * L) * (2 * L + 1) // 2
prow, pcol, pval = [], [], []
for (ci, i, j, terms) in psd_entries:
    L = cones[ci]; N2 = 2 * L
    acc = collections.defaultdict(complex)       # M[i,j] = sum coeff * gamma, gamma = Re + i Im (conj: Re - i Im)
    for (v, cf, cj) in terms:
        acc[col(v, 0)] += cf; acc[col(v, 1)] += (-1j if cj else 1j) * cf
    for c_, z in acc.items():
        # real embedding: Y[i,j] = Re M, Y[L+i, L+j] = Re M, Y[L+i, j] = Im M, Y[L+j, i] = -Im M (i != j)
        ents = [(i, j, z.real), (L + i, L + j, z.real), (L + i, j, z.imag)]
        if i != j: ents.append((L + j, i, -z.imag))
        for (ii, jj, val) in ents:
            if abs(val) < 1e-14: continue
            k_, sc = sidx(ii, jj, N2)
            prow.append(offs[ci] + k_); pcol.append(c_); pval.append(-val * (math.sqrt(2) if ii != jj else 1.0))
Apsd = sps.csr_matrix((pval, (prow, pcol)), shape=(o, NV))
A = sps.vstack([Aeq, Apsd]).tocsc(); bb = np.concatenate([beq, np.zeros(o)]); qv = np.zeros(NV); qv[0] = -1.0
log(f"SDP: {NV} real variables, {2 * NK} equalities, nnz {A.nnz}")
import scs
sol = scs.SCS(dict(A=A, b=bb, c=qv), dict(z=2 * NK, s=[2 * L for L in cones]), eps_abs=1e-8, eps_rel=1e-8,
              max_iters=int(os.environ.get("SCS_ITERS", "200000")), verbose=False).solve()
val = float(sol["x"][0])
log(f"{WHICH} code space (n' = {nq}), degree {2 * KDEG} SOS bound: c >= {val:.10f}  (status {sol['info']['status']}); c8 = {C8:.10f}")
json.dump(dict(space=WHICH, nq=nq, degree=2 * KDEG, bound=val, status=sol["info"]["status"], c8=C8, n_vars=len(VARS), n_classes=NK,
               cones=cones, effective_min=mins[0], weights=sorted(collections.Counter(weights.values()).items())),
          open(os.path.join(ROOT, "data", f"w33_f8_codespace_effective_sos_{WHICH}_deg{2 * KDEG}.json"), "w"), indent=1)
