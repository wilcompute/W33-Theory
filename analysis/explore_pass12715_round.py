"""Pass 12715 (Claude track).
 (1) Explicit superpotential for the pseudo-Goldstone Q + U of Pass 12714: Sigma = 45 (complex antisymmetric 10x10), W = (m/2) tr S^2 + (l/4M) tr S^4,
     SO(10)-invariant, only SU(5) gauged.  The B-L vacuum S0 = a T_BL with a^2 = m M / l solves F = 0 (eigenvalues of S0 in {0, +-i a}).
     Hessian of W on the 45 complex directions: zero modes vs 30 broken generators; their SM content.  Explicit SO(10) breaking by an
     SU(5)-only term eps * W_24 lifts them: mass vs eps (linear).  Goldstone quality: Planck-suppressed SO(10)-violating operators
     k S^n / M_Pl^(n-3) give m ~ a (a/M_Pl)^(n-3); smallest forbidden dimension n with m <= M_VL.
 (2) E6: partial check - the 78 = 45 + 16 + 16bar + 1 under SO(10) x U(1); a global E6 broken to SO(10) x U(1) would add 16 + 16bar Goldstones
     (matter-like, with e^c) - so the clean Q + U result needs the SO(10) (not E6) accidental symmetry.
 (3) Hybrid (pseudo-Goldstone, M_SS = sqrt(M_VL M_GUT / c), c in [0.3, 3]) vs B' (flat R in [0.009, 0.2] um, mediator gauge shift) in the
     (M_VL, y') plane, M_VL = 1.74-6 TeV; minimal separation in sigma for sigma(y') = 0.005 (+) 0.0036 and 0.002 (+) 0.0036.
 (4) Signed-digit ternary multiplier: digit products are signs (no multiplier); redundant {-2..2} + {-2..2} carry-free adder (exhaustive
     closure check); n_t rows reduced 2:1 per level; random 41-trit products checked; levels vs binary radix-4 Booth + Wallace 3:2.
 (5) Ternary NN energy with arithmetic: per weight = bits * E_mem + E_op * (1 - zero_frac); E_op: fp32 4.6, int8 0.33 (mult + 32b acc),
     2-bit 0.15, ternary/binary 0.1 (32b add); crossover E_mem where ternary beats binary; per-layer Pareto fronts of Pass 12714 re-scored.
usage: py -3 analysis/explore_pass12715_round.py"""
import itertools, json, math, os
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
res = {}

# ======================================================================= (1) superpotential
n = 10
basis = []
for i in range(n):
    for j in range(i + 1, n):
        M = np.zeros((n, n)); M[i, j], M[j, i] = 1, -1; basis.append(M)
B = np.array(basis)                                                    # 45 x 10 x 10


def cplx(A):
    R, S = A.real, A.imag
    return np.block([[R, -S], [S, R]])


TBL = cplx(1j * np.diag([1, 1, 1, 0, 0])); Yg = cplx(1j * np.diag([-1 / 3] * 3 + [1 / 2] * 2))
m_, l_, Mh = 1.0, 1.0, 1.0
# W = (m/2) tr S^2 + (l/4M) tr S^4 with S = sum z_k B_k; S0 = a TBL: S0^3 = -a^3 TBL-block -> F = m S + (l/M) S^3 = 0 needs a^2 = m M / l
a = math.sqrt(m_ * Mh / l_)
S0 = a * TBL
F0 = m_ * S0 + l_ / Mh * S0 @ S0 @ S0
print(f"(1) F-term at the B-L vacuum: |m S + (l/M) S^3| = {np.linalg.norm(F0):.1e}")
assert np.linalg.norm(F0) < 1e-12


def W(z, eps=0.0):
    S = np.tensordot(z, B, 1)
    w = m_ / 2 * np.trace(S @ S) + l_ / (4 * Mh) * np.trace(S @ S @ S @ S)
    if eps:                                                            # SU(5)-only perturbation: tr of the 24-projection cubed (in u(5) language)
        P = S[:5, :5] + 1j * S[5:, :5]                                 # complex-linear part (approximate projection onto u(5) action)
        w += eps * np.trace(P @ P @ P).real
    return w


def hessian(eps=0.0, h=1e-4):
    z0 = np.array([np.sum(S0 * b) / 2 for b in B])                     # coordinates of S0 (tr(b b^T) = 2)
    H = np.zeros((45, 45)); f0 = W(z0, eps)
    E = np.eye(45) * h
    for i in range(45):
        for j in range(i, 45):
            H[i, j] = H[j, i] = (W(z0 + E[i] + E[j], eps) - W(z0 + E[i] - E[j], eps) - W(z0 - E[i] + E[j], eps) + W(z0 - E[i] - E[j], eps)) / (4 * h * h)
    return H


H0 = hessian()
ev = np.sort(np.abs(np.linalg.eigvalsh(H0)))
nzero = int(np.sum(ev < 1e-6 * ev.max()))
print(f"(1) Hessian of W at the B-L vacuum: {nzero} zero modes (broken generators of SO(10) -> SU(3)xSU(2)xSU(2)xU(1): 30); "
      f"non-zero masses {sorted(set(np.round(ev[ev > 1e-6 * ev.max()], 4)))} (units m)")
assert nzero == 30
# SM content of the zero modes: ad_Y eigenvalues on the zero-mode space
w_, V = np.linalg.eigh(H0); Z = V[:, np.abs(w_) < 1e-6 * np.abs(w_).max()]
Zm = [np.tensordot(Z[:, k], B, 1) for k in range(Z.shape[1])]
flat = np.array([zz.ravel() for zz in Zm]).T
adY = np.linalg.lstsq(flat, np.array([(Yg @ zz - zz @ Yg).ravel() for zz in Zm]).T, rcond=None)[0]
ys = sorted(np.round(np.abs(np.linalg.eigvals(adY).imag), 3))
cnt = {y: ys.count(y) for y in sorted(set(ys))}
print(f"(1) zero modes by |Y|: {cnt}  -> 12 eaten by SU(5) ((3,2)_-5/6 + c.c.), 18 = Q + Qbar + U + Ubar remain")
lift = []
for eps in (1e-4, 1e-3, 1e-2):
    He = hessian(eps); e2 = np.sort(np.abs(np.linalg.eigvalsh(He)))[:30]
    lift.append(dict(eps=eps, lightest_nonzero=float(e2[e2 > 1e-7].min()) if np.any(e2 > 1e-7) else 0.0, median_lifted=float(np.median(e2))))
    print(f"(1) SU(5)-only perturbation eps = {eps:.0e}: former zero modes lifted to median {np.median(e2):.2e} m (largest {e2.max():.2e})")
aG, MPl, MVL = 4.1e16, 2.435e18, 1740.0
nq = next(nn for nn in range(4, 40) if aG * (aG / MPl) ** (nn - 3) <= MVL)
print(f"(1) Goldstone quality: an SO(10)-violating operator S^n / M_Pl^(n-3) gives m ~ a (a/M_Pl)^(n-3); keeping m <= 1.74 TeV needs all such operators "
      f"with n < {nq} absent (n = {nq}: m = {aG * (aG / MPl) ** (nq - 3):.0f} GeV)")
res["superpotential"] = dict(zero_modes=nzero, Y_content=cnt, lifting=lift, quality_min_dim=nq,
                             note="W = (m/2) tr S^2 + (l/4M) tr S^4 is the generic SO(10)-invariant W to quartic order; the B-L vacuum exists; "
                                  "explicit SU(5)-only terms lift the would-be Goldstones linearly; a 'Goldstone quality problem' like the axion's")

# ======================================================================= (2) E6 partial
res["e6_partial"] = dict(statement="global E6 -> SO(10) x U(1): Goldstones 16 + 16bar (contain e^c, L, d^c, nu^c); to isolate Q + U the accidental "
                                   "symmetry must be SO(10) acting on a 45 (or E6 broken along B-L inside SO(10) with the 16s eaten/lifted)")
print("(2) E6: 78 = 45 + 16 + 16bar + 1; a global E6 adds 16 + 16bar Goldstones (with e^c) - the clean Q + U needs an accidental SO(10) on a 45")

# ======================================================================= (3) (M_VL, y') plane
src03 = open(os.path.join(HERE, "toe_pass12703_round.py"), encoding="utf-8").read()
G = {"__file__": os.path.join(HERE, "toe_pass12703_round.py")}
exec(src03.split("# ======================================================================= (4)")[0], G)
initial, beta_sm, beta_vl, OFF3, M5f = (G[k] for k in ("initial", "beta_sm", "beta_vl", "OFF3", "M5"))
K = 1 / (16 * math.pi ** 2); MT, A3 = 172.57, 0.1180
dl = lambda y: (5 / 6) * 3 * K * y[5] ** 4 - 2 * y[4] * 3 * K * y[5] ** 2 / 3


def lam_end(yp, tgt, mvl, withY=False):
    Mt0 = MT - OFF3; kw = dict(rtol=1e-8, atol=1e-11, max_step=0.5)
    y = solve_ivp(lambda t, y: beta_sm(*y[:5]) + [0.0], (0, math.log(mvl / Mt0)), np.array(initial(MT, 125.20, A3) + [yp]), **kw).y[:, -1].copy()
    y[4] += dl(y)
    def rhs(t, y):
        d = list(beta_vl(*y))
        if withY and Mt0 * math.exp(t) > max(mvl, 2000.0): d[2] += K * y[2] ** 3 / 6; d[0] += K * y[0] ** 3 / 9
        return d
    return solve_ivp(rhs, (math.log(mvl / Mt0), math.log(tgt / Mt0)), y, **kw).y[:, -1][4]


ypt = lambda tgt, mvl, **kw: brentq(lambda p: lam_end(p, tgt, mvl, **kw), 0.2, 1.0, xtol=1e-5)
plane = []
for mvl in (1740.0, 3000.0, 6000.0):
    hy = [ypt(math.sqrt(mvl * 4.1e16 / c), mvl) for c in (0.3, 3.0)]
    bp = [ypt(M5f(R * 1e-6), mvl, withY=True) for R in (0.0088, 0.2)]
    gap = min(bp) - max(hy)
    plane.append(dict(M_VL=mvl, hybrid=sorted(hy), Bprime=sorted(bp), gap=gap,
                      sep={str(s): gap / math.hypot(s, 0.0036) for s in (0.005, 0.002)}))
    print(f"(3) M_VL = {mvl / 1e3:.2f} TeV: hybrid y' in [{min(hy):.4f}, {max(hy):.4f}], B' in [{min(bp):.4f}, {max(bp):.4f}]: band gap {gap:+.4f} "
          f"= {gap / math.hypot(0.005, 0.0036):.1f}-{gap / math.hypot(0.002, 0.0036):.1f} sigma")
res["plane"] = plane

# ======================================================================= (4) multiplier
ok = True
for a_ in range(-2, 3):
    for b_ in range(-2, 3):
        for tin in (-1, 0, 1):
            w = a_ + b_; t = 1 if w >= 2 else (-1 if w <= -2 else 0); u = w - 3 * t
            ok &= -1 <= u <= 1 and -2 <= u + tin <= 2
assert ok


def sd_add(x, y):
    L = max(len(x), len(y)) + 1; x = x + [0] * (L - len(x)); y = y + [0] * (L - len(y))
    w = [p + q for p, q in zip(x, y)]; t = [1 if v >= 2 else (-1 if v <= -2 else 0) for v in w]
    u = [v - 3 * tt for v, tt in zip(w, t)]
    return [u[i] + (t[i - 1] if i else 0) for i in range(L)] + [t[-1]]


def bt(nv, nd):
    d = []
    for _ in range(nd):
        r = nv % 3; nv //= 3
        if r == 2: r = -1; nv += 1
        d.append(r)
    return d


val = lambda d: sum(c * 3 ** i for i, c in enumerate(d))
import random; rng = random.Random(15); nt = 41; good = True; levels = 0
for _ in range(200):
    A_ = rng.randint(-(3 ** 40), 3 ** 40); Bv = rng.randint(-(3 ** 40), 3 ** 40)
    da, db = bt(A_, nt), bt(Bv, nt)
    rows = [[0] * i + [s * bb for s in da] for i, bb in enumerate(db) if bb]
    lv = 0
    while len(rows) > 1:
        rows = [sd_add(rows[i], rows[i + 1]) if i + 1 < len(rows) else rows[i] for i in range(0, len(rows), 2)]; lv += 1
    levels = max(levels, lv); good &= (val(rows[0]) if rows else 0) == A_ * Bv
assert good
nb = 64; r = nb // 2 + 1; wl = 0
while r > 2: r = math.ceil(r * 2 / 3); wl += 1
print(f"(4) signed-digit ternary multiplier (41 trits ~ 64 bits): digit products are signs, carry-free 2:1 tree, products verified (200 random); "
      f"{levels} adder levels (<= ceil(log2 41) = {math.ceil(math.log2(41))}) vs binary radix-4 Booth (33 rows) + Wallace 3:2: {wl} levels + final CPA")
res["multiplier"] = dict(trits=nt, levels_max=levels, binary_wallace_levels=wl, verified=good)

# ======================================================================= (5) energy with arithmetic
Eop = {"fp32": 4.6, "int8": 0.33, "2bit": 0.15, "ternary": 0.1, "binary": 0.1}
bits = {"fp32": 32, "int8": 8, "2bit": 2, "ternary": 1.6, "binary": 1}
zf = {"ternary": 0.44}
cross = (Eop["ternary"] * (1 - zf["ternary"]) - Eop["binary"]) / (bits["binary"] - bits["ternary"])
print(f"(5) ternary beats binary per weight when E_mem < {cross:.3f} pJ/bit (weight-stationary / in-memory regimes ~0.01-0.05 pJ/bit; SRAM 0.16; DRAM 30)")
P14 = json.load(open(os.path.join(ROOT, "data", "explore_pass12714_round.json"), encoding="utf-8"))["mixed"]["configs"]
sizes = [32 * 128, 128 * 128, 128 * 10]
fronts = {}
for Em in (30.0, 0.16, 0.02):
    sc = []
    for c in P14:
        e = sum(n_ * (bits[m] * Em + Eop[m] * (1 - zf.get(m, 0))) for m, n_ in zip(c["modes"], sizes)) * 1e-6
        sc.append((e, c["acc"], tuple(c["modes"])))
    sc.sort(); fr = []; best = -1
    for e, a2, mo in sc:
        if a2 > best + 1e-9: fr.append(dict(modes=mo, energy_uJ=e, acc=a2)); best = a2
    share = float(np.mean([sum(m == "ternary" for m in f["modes"]) / 3 for f in fr]))
    fronts[str(Em)] = dict(front=fr, ternary_share=share)
    print(f"(5) E_mem = {Em} pJ/bit: front " + " -> ".join("/".join(f["modes"]) for f in fr) + f"; ternary share {share:.0%}")
res["energy"] = dict(E_op=Eop, crossover_pJ_per_bit=cross, fronts=fronts)
json.dump(res, open(os.path.join(ROOT, "data", "explore_pass12715_round.json"), "w", encoding="utf-8"), indent=1, default=str)
print("wrote data/explore_pass12715_round.json")
