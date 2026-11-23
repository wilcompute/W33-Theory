"""Pass 12716 (Claude track).
 (0) Gauged-SO(10) GIFT count: sectors Sigma (45, VEV along B-L) and H (16 + 16bar, VEV -> SU(5)) with no cross couplings have accidental
     SO(10)_S x SO(10)_H; broken 30 + 21; the gauged diagonal SO(10) -> SM eats 33; the SM content of the 18 uneaten multiplets.
 (1) Can a discrete symmetry protect it?  Charge search over Z_N (N <= 30), non-R (W charge 0) and R (W charge 2): Sigma-sector templates
     S1 = {S^2, S^4}, S2 = {X S^2, S^4, X^3}; H-sector Hn = {Y, Y (Hbar H)^n} (Y has no VEV).  Violating operators: Hbar S^k H (Hbar H)^c X^a
     (and products of two such cores), dimension k + 2 + 2c + a; the best (largest) minimal allowed violating dimension per template.
 (2) Unification with the pseudo-Goldstone spectrum: the LR-adjoint remnants of the 45 ((8,1) + (1,3) at 2m-4m) with m = lambda a^2 / M:
     Pass 12705's two-loop unify_adj with the octet + triplet at those masses.
 (3) Ternary compute-in-memory crossbar: E_w = E_cell + E_ADC / rows (+ DAC) with an ADC Walden FOM; binary (1 device, unsigned) vs
     ternary (2 devices differential, zero draws no current); against the 0.073 pJ/bit threshold of Pass 12715.
 (4) FCC posterior odds: hypothetical measurements (M_VL, y') -> Bayes factors of hybrid (c log-uniform [0.3, 3]) and B' (R log-uniform
     [0.009, 0.2] um) against 'generic VLQ' (y' uniform [0, 1]), times the current prior odds (Pass 12709-12710).
 (5) Ternary vs binary Hamming codes at equal cell noise: binary Hamming(127,120) vs ternary Hamming(121,116) (d = 3); level-error rates
     from Gaussian noise on a fixed swing; information per cell and decoded bit-error rate vs SNR.
usage: py -3 analysis/explore_pass12716_round.py"""
import itertools, json, math, os
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
res = {}
K = 1 / (16 * math.pi ** 2)

# ======================================================================= (0) GIFT count
n = 10
so10 = []
for i in range(n):
    for j in range(i + 1, n):
        M = np.zeros((n, n)); M[i, j], M[j, i] = 1, -1; so10.append(M)
cplx = lambda A: np.block([[A.real, -A.imag], [A.imag, A.real]])
TBL = cplx(1j * np.diag([1, 1, 1, 0, 0])); Yg = cplx(1j * np.diag([-1 / 3] * 3 + [1 / 2] * 2))
gm = []
for a_ in range(3):
    for b_ in range(a_ + 1, 3):
        m = np.zeros((3, 3), complex); m[a_, b_] = m[b_, a_] = 1; gm.append(m)
        m = np.zeros((3, 3), complex); m[a_, b_] = -1j; m[b_, a_] = 1j; gm.append(m)
gm += [np.diag([1, -1, 0]).astype(complex), np.diag([1, 1, -2]).astype(complex) / math.sqrt(3)]
S3 = [cplx(1j * np.block([[h / 2, np.zeros((3, 2))], [np.zeros((2, 3)), np.zeros((2, 2))]])) for h in gm]
pa = [np.array([[0, 1], [1, 0]], complex), np.array([[0, -1j], [1j, 0]]), np.diag([1, -1]).astype(complex)]
S2 = [cplx(1j * np.block([[np.zeros((3, 3)), np.zeros((3, 2))], [np.zeros((2, 3)), h / 2]])) for h in pa]
comm = lambda X, Y: X @ Y - Y @ X
J = cplx(1j * np.eye(5))


def complement(gens_unbroken):
    U = np.array([g.ravel() for g in gens_unbroken]).T
    A = np.array([g.ravel() for g in so10]).T
    P = U @ np.linalg.pinv(U)
    R = A - P @ A
    u, s, vh = np.linalg.svd(R, full_matrices=False)
    return [u[:, k].reshape(n, n) for k in range(int(np.sum(s > 1e-9)))]


def sm_content(gens):
    flat = np.array([g.ravel() for g in gens]).T
    ad = lambda X: np.linalg.lstsq(flat, np.array([comm(X, g).ravel() for g in gens]).T, rcond=None)[0]
    AY = ad(Yg); C3 = -sum(ad(g) @ ad(g) for g in S3); C2 = -sum(ad(g) @ ad(g) for g in S2)
    w, V = np.linalg.eig(AY); out = {}
    for k in range(len(w)):
        v = V[:, k]; y = round(float((w[k] / 1j).real) * 6) / 6
        c3 = round(float(np.real(v.conj() @ C3 @ v / (v.conj() @ v))), 2); c2 = round(float(np.real(v.conj() @ C2 @ v / (v.conj() @ v))), 2)
        key = f"({ {0.0: '1', 1.33: '3', 3.0: '8'}.get(c3, c3)},{ {0.0: '1', 0.75: '2', 2.0: '3'}.get(c2, c2)}){y:+.3f}"
        out[key] = out.get(key, 0) + 1
    return out


def commutant(X):
    Cm = np.array([comm(X, g).ravel() for g in so10]).T
    u, s, vh = np.linalg.svd(Cm); k = int(np.sum(s < 1e-9))
    return [sum(c * so10[i] for i, c in enumerate(v)) for v in vh[-k:]]


lr = commutant(TBL); u5 = commutant(J)
Jn = J / np.linalg.norm(J); u5 = [g - np.sum(g * Jn) * Jn for g in u5]
u5 = [g for g in u5 if np.linalg.norm(g) > 1e-9]
sm_alg = S3 + S2 + [Yg]
bS, bH, eaten = sm_content(complement(lr)), sm_content(complement(u5)), sm_content(complement(sm_alg))
tot = {k: bS.get(k, 0) + bH.get(k, 0) - eaten.get(k, 0) for k in set(bS) | set(bH) | set(eaten)}
left = {k: v for k, v in tot.items() if v}
print(f"(0) broken: Sigma sector {sum(bS.values())}, H sector {sum(bH.values())}; eaten by gauged SO(10) -> SM {sum(eaten.values())}; "
      f"uneaten {sum(left.values())}: {dict(sorted(left.items()))}")
assert sum(bS.values()) == 30 and sum(bH.values()) == 21 and sum(eaten.values()) == 33 and sum(left.values()) == 18
assert all(v > 0 for v in left.values()) and not any(k.startswith("(1,") for k in left)
res["gift_count"] = dict(sigma=bS, H=bH, eaten=eaten, uneaten=left)

# ======================================================================= (1) discrete protection search


def search(N, r, Stmpl, n_h):
    best = -1; arg = None
    xs = range(N) if Stmpl == "S2" else [0]
    for s in range(N):
        for x in xs:
            if Stmpl == "S1":
                if (2 * s - r) % N or (4 * s - r) % N: continue
                hasX = False
            else:
                if (x + 2 * s - r) % N or (4 * s - r) % N or (3 * x - r) % N: continue
                hasX = True
            y = r % N
            for p in range(N):
                if (y + n_h * p - r) % N: continue
                mind = 99
                for k in range(1, 9):
                    for c in range(0, 5):
                        for a in range(0, 5 if hasX else 1):
                            d = k + 2 + 2 * c + a
                            if d >= mind: continue
                            if (k * s + (1 + c) * p + a * x - r) % N == 0: mind = d
                for k1, k2 in itertools.combinations_with_replacement(range(1, 5), 2):
                    d = k1 + k2 + 4
                    if d < mind and ((k1 + k2) * s + 2 * p - r) % N == 0: mind = d
                if mind > best: best, arg = mind, dict(s=s, x=x, p=p, y=y)
    return best, arg


prot = {}
for Stmpl in ("S1", "S2"):
    for n_h in (1, 2, 3, 4, 5):
        bestN = None
        for r in (0, 2):
            for N in range(2, 31):
                b, arg = search(N, r, Stmpl, n_h)
                key = f"{Stmpl}|H{n_h}|{'R' if r else 'nonR'}"
                if b > prot.get(key, {"best": -1})["best"]:
                    prot[key] = dict(best=b, N=N, charges=arg)
        print(f"(1) {Stmpl} with H-sector Y(HbarH)^{n_h}: best minimal violating dimension non-R {prot[f'{Stmpl}|H{n_h}|nonR']['best']} "
              f"(N={prot[f'{Stmpl}|H{n_h}|nonR']['N']}), R {prot[f'{Stmpl}|H{n_h}|R']['best']} (N={prot[f'{Stmpl}|H{n_h}|R']['N']})")
ok11 = {k: v for k, v in prot.items() if v["best"] >= 11}
print(f"(1) templates reaching dimension >= 11 (quality requirement): {sorted(ok11) or 'none'}")
res["protection"] = dict(rows=prot, reaching_11=sorted(ok11),
                         theorem="if Hbar H appears linearly with a VEV-less driving field (n = 1), Hbar S^2 H carries the charge of the allowed S^2 term: "
                                 "violation at dimension 4-5 is unavoidable; higher powers (Hbar H)^n push it to 2n + dim(S-monomial)")

# ======================================================================= (2) unification with the octet + triplet remnants
src05 = open(os.path.join(HERE, "toe_pass12705_round.py"), encoding="utf-8").read()
blk = "#" + src05.split("# ---- (2b)")[1].split("ref = unify_adj(1e30)")[0]
G5 = {"np": np, "math": math, "os": os, "HERE": HERE, "K": K}
exec(blk, G5)
unify_adj = G5["unify_adj"]
ref = unify_adj(1e30)
aG, MPl = 4.1e16, 2.435e18
uni = []
for lam in (1.0, 4.0, 4 * math.pi):
    for Mcut in (MPl, 1e17):
        mm = lam * aG ** 2 / Mcut
        M12, ai, dl = unify_adj(2 * mm)
        uni.append(dict(lambda_=lam, M_cut=Mcut, m=mm, M_adj=2 * mm, M12=M12, delta=dl))
        print(f"(2) lambda = {lam:5.2f}, cutoff {Mcut:.1e}: m = {mm:.1e}, octet+triplet at {2 * mm:.1e}: M12 = {M12:.2e}, delta = {dl:+.2f} (reference {ref[2]:+.2f})")
res["unification"] = dict(reference=ref, rows=uni,
                          note="the quartic tr S^4 / M with M = M_Pl puts the LR-adjoint (8,1)+(1,3) at ~1e15: unification spoiled (cf. Pass 12705); "
                               "a cutoff ~1e17 or a renormalisable completion (e.g. a heavy 54) is needed")

# ======================================================================= (3) crossbar
rows_ = (64, 128, 256)
cim = []
for R_ in rows_:
    for fom in (10e-15, 50e-15):
        for name, dev, rng_levels in (("binary", 1, R_ + 1), ("ternary", 2, 2 * R_ + 1)):
            enob = math.log2(rng_levels)
            Eadc = fom * 2 ** min(enob, 8)                     # ADC capped at 8 bits (partial sums truncated)
            Ecell = dev * 1e-15 * (0.56 if name == "ternary" else 1.0)
            Ew = Ecell + Eadc / R_
            cim.append(dict(rows=R_, fom_fJ=fom * 1e15, type=name, E_pJ=Ew * 1e12, below_threshold=Ew * 1e12 < 0.073))
            print(f"(3) {R_} rows, ADC FOM {fom * 1e15:.0f} fJ/step, {name:7s}: {Ew * 1e12:.4f} pJ per weight-op ({'below' if Ew * 1e12 < 0.073 else 'above'} 0.073)")
res["crossbar"] = cim

# ======================================================================= (4) posterior odds
src03 = open(os.path.join(HERE, "toe_pass12703_round.py"), encoding="utf-8").read()
G = {"__file__": os.path.join(HERE, "toe_pass12703_round.py")}
exec(src03.split("# ======================================================================= (4)")[0], G)
initial, beta_sm, beta_vl, OFF3, M5f = (G[k] for k in ("initial", "beta_sm", "beta_vl", "OFF3", "M5"))
dl_ = lambda y: (5 / 6) * 3 * K * y[5] ** 4 - 2 * y[4] * 3 * K * y[5] ** 2 / 3


def lam_end(yp, tgt, mvl, withY=False):
    Mt0 = 172.57 - OFF3; kw = dict(rtol=1e-8, atol=1e-11, max_step=0.5)
    y = solve_ivp(lambda t, y: beta_sm(*y[:5]) + [0.0], (0, math.log(mvl / Mt0)), np.array(initial(172.57, 125.20, 0.1180) + [yp]), **kw).y[:, -1].copy()
    y[4] += dl_(y)
    def rhs(t, y):
        d = list(beta_vl(*y))
        if withY and Mt0 * math.exp(t) > max(mvl, 2000.0): d[2] += K * y[2] ** 3 / 6; d[0] += K * y[0] ** 3 / 9
        return d
    return solve_ivp(rhs, (math.log(mvl / Mt0), math.log(tgt / Mt0)), y, **kw).y[:, -1][4]


ypt = lambda tgt, mvl, **kw: brentq(lambda p: lam_end(p, tgt, mvl, **kw), 0.2, 1.0, xtol=1e-5)
prior = {"hybrid": 0.75, "B'": 0.044, "generic VLQ": 1.0}
odds = []
for mvl, yobs, truth in ((3000.0, None, "hybrid"), (3000.0, None, "B'")):
    cs = np.exp(np.linspace(math.log(0.3), math.log(3), 7)); Rs = np.exp(np.linspace(math.log(0.0088), math.log(0.2), 7))
    yH = np.array([ypt(math.sqrt(mvl * aG / c), mvl) for c in cs]); yB = np.array([ypt(M5f(R * 1e-6), mvl, withY=True) for R in Rs])
    yobs = float(np.median(yH if truth == "hybrid" else yB))
    for sm in (0.005, 0.002):
        st = math.hypot(sm, 0.0036)
        LH = float(np.mean(norm.pdf(yobs, yH, st))); LB = float(np.mean(norm.pdf(yobs, yB, st))); LG = 1.0
        post = {"hybrid": prior["hybrid"] * LH, "B'": prior["B'"] * LB, "generic VLQ": prior["generic VLQ"] * LG}
        odds.append(dict(M_VL=mvl, truth=truth, y_obs=yobs, sigma=sm, BF_hybrid=LH, BF_Bprime=LB, posterior=post))
        print(f"(4) truth {truth:6s}, M_VL = 3 TeV, y'_obs = {yobs:.4f}, sigma_meas {sm}: BF vs generic VLQ: hybrid {LH:.1f}, B' {LB:.2f}; "
              f"posterior odds hybrid : B' : generic = {post['hybrid']:.2f} : {post[chr(66) + chr(39)]:.3f} : 1")
res["odds"] = odds

# ======================================================================= (5) Hamming codes
codes = {"binary Hamming(127,120)": (2, 127, 120), "ternary Hamming(121,116)": (3, 121, 116)}
ham = []
for snr in (6.0, 8.0, 10.0, 12.0, 14.0):
    for nm, (q, nn, kk) in codes.items():
        ps = 2 * (1 - 1 / q) * norm.sf(snr / (2 * (q - 1)))          # level spacing V/(q-1), sigma = V/snr
        pblk = 1 - (1 - ps) ** nn - nn * ps * (1 - ps) ** (nn - 1)
        info = kk * math.log2(q) / nn
        ber = pblk * 3 / nn * (kk * math.log2(q)) / (kk * math.log2(q))   # ~3 symbol errors per failed block, spread over the block
        ham.append(dict(snr=snr, code=nm, p_symbol=ps, p_block=pblk, info_bits_per_cell=info, ber_approx=pblk * 3 / nn))
        print(f"(5) SNR {snr:4.1f}: {nm:26s} info/cell {info:.3f} bits, symbol error {ps:.1e}, block failure {pblk:.1e}")
res["hamming"] = ham
json.dump(res, open(os.path.join(ROOT, "data", "explore_pass12716_round.json"), "w", encoding="utf-8"), indent=1, default=str)
print("wrote data/explore_pass12716_round.json")
