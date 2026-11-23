"""Pass 12714 (Claude track).
 (1) Pseudo-Goldstone light Q + U.  so(10) in the real vector rep; u(5) via the complex structure; a 45 VEV along T_BL = i diag(1,1,1,0,0)
     (the Dimopoulos-Wilczek direction; B-L on the 10 is diag(-2/3,-2/3,-2/3,0,0) up to scale).  Unbroken algebra = commutant; the broken
     generators are decomposed under SU(3) x SU(2)_L x U(1)_Y (Casimirs and ad_Y on the complexified broken space).  If SO(10) is an
     accidental global symmetry of the Higgs-sector superpotential while only SU(5) is gauged, the gauge bosons eat the (3,2)_-5/6 pair and
     the remaining Goldstone chiral multiplets are the light states.  Scale estimate for their fermions: M_SS^2 / M_GUT.
 (2) (superseded by (1); no SU(6)/SU(3)^3 run)
 (3) Radix-3 signed-digit addition with digits {-2..2} (Avizienis): t = +1 if w >= 2, -1 if w <= -2, u = w - 3t, s = u + t_in.
     Exhaustive check of correctness and carry-free locality; storage redundancy log2(5)/log2(3).
 (4) Inclusive Belle II B -> baryon + missing energy reach for B': N_BB = 5.5e10 (50 ab^-1), hadronic-tag efficiency 0.2-0.5%, signal
     efficiency 10-30%, background 0-100 events (90% CL, Feldman-Cousins-like 2.44 + 1.64 sqrt(B)); fraction of B' (Pass 12713 Monte Carlo
     priors) with inclusive BR above the reach.  Scaling of Belle's B -> Lambda + missing limit (0.71 ab^-1) for comparison.
 (5) Per-layer mixed precision: 32-128-128-10 student on the Pass 12712 teacher task; each layer binary / ternary / 2-bit (27 configs, 2 seeds);
     memory-bound energy (30 pJ/bit) vs test accuracy; Pareto front composition.
usage: py -3 analysis/explore_pass12714_round.py"""
import itertools, json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
res = {}

# ======================================================================= (1)
n = 10
so10 = []
for i in range(n):
    for j in range(i + 1, n):
        M = np.zeros((n, n)); M[i, j], M[j, i] = 1, -1; so10.append(M)


def cplx(A):
    """complex-linear map A on C^5 -> real 10x10 acting on (x, y), z = x + i y."""
    R, S = A.real, A.imag
    return np.block([[R, -S], [S, R]])


TBL = cplx(1j * np.diag([1, 1, 1, 0, 0]))
Yg = cplx(1j * np.diag([-1 / 3] * 3 + [1 / 2] * 2))
gm = []
for a in range(3):
    for b in range(a + 1, 3):
        m = np.zeros((3, 3), complex); m[a, b] = m[b, a] = 1; gm.append(m)
        m = np.zeros((3, 3), complex); m[a, b] = -1j; m[b, a] = 1j; gm.append(m)
gm += [np.diag([1, -1, 0]).astype(complex), np.diag([1, 1, -2]).astype(complex) / math.sqrt(3)]
emb3 = lambda h: np.block([[h, np.zeros((3, 2))], [np.zeros((2, 3)), np.zeros((2, 2))]])
emb2 = lambda h: np.block([[np.zeros((3, 3)), np.zeros((3, 2))], [np.zeros((2, 3)), h]])
S3 = [cplx(1j * emb3(h / 2)) for h in gm]
pa = [np.array([[0, 1], [1, 0]], complex), np.array([[0, -1j], [1j, 0]]), np.diag([1, -1]).astype(complex)]
S2 = [cplx(1j * emb2(h / 2)) for h in pa]
for X in [TBL, Yg] + S3 + S2: assert np.allclose(X, -X.T)
B = np.array([M.ravel() for M in so10]).T
comm = lambda X, Y: X @ Y - Y @ X
Cm = np.array([comm(TBL, M).ravel() for M in so10]).T
u, s, vh = np.linalg.svd(Cm); nun = int(np.sum(s < 1e-9))
unb = vh[-nun:]; brk = vh[:len(so10) - nun]
print(f"(1) 45 VEV along B-L: unbroken dimension {nun} (SU(3)xSU(2)xSU(2)xU(1) = 15), broken {len(so10) - nun}")
assert nun == 15
Bb = np.array([sum(c * so10[k] for k, c in enumerate(v)) for v in brk])      # broken generators (real basis)
flat = np.array([b.ravel() for b in Bb]).T


def ad_on_broken(X):
    """matrix of ad_X restricted to the broken span (projected)."""
    imgs = np.array([comm(X, b).ravel() for b in Bb]).T
    coef, *_ = np.linalg.lstsq(flat, imgs, rcond=None)
    return coef


AY = ad_on_broken(Yg); C3 = -sum(ad_on_broken(g) @ ad_on_broken(g) for g in S3); C2 = -sum(ad_on_broken(g) @ ad_on_broken(g) for g in S2)
w, V = np.linalg.eig(AY)
states = {}
for k in range(len(w)):
    v = V[:, k]; y = round(float((w[k] / 1j).real) * 6) / 6
    c3 = float(np.real(v.conj() @ C3 @ v / (v.conj() @ v))); c2 = float(np.real(v.conj() @ C2 @ v / (v.conj() @ v)))
    key = (round(c3, 3), round(c2, 3), round(y, 3)); states[key] = states.get(key, 0) + 1
lab3 = {0.0: "1", 1.333: "3", 3.0: "8"}; lab2 = {0.0: "1", 0.75: "2", 2.0: "3"}
dec = {f"({lab3.get(k[0], k[0])},{lab2.get(k[1], k[1])}) Y={k[2]:+.3f}": v for k, v in sorted(states.items(), key=lambda t: t[0][2])}
print("(1) broken generators under SU(3)xSU(2)_LxU(1)_Y (state counts): " + ", ".join(f"{k}: {v}" for k, v in dec.items()))
ys = sorted(k[2] for k, v in states.items() for _ in range(v))
assert sorted(set(round(abs(y), 3) for y in ys)) == [0.167, 0.667, 0.833] and len(ys) == 30
print("(1) -> gauged SU(5) eats (3,2)_-5/6 + c.c.; uneaten Goldstone multiplets = (3,2)_1/6 + (3bar,1)_-2/3 + c.c. = vectorlike Q + U, no e^c")
est = {f"M_SS={ms:.0e}": ms ** 2 / 4.1e16 for ms in (3e9, 1e10, 3e10)}
print("(1) fermion mass estimate M_SS^2/M_GUT (M_GUT = 4.1e16): " + ", ".join(f"{k}: {v / 1e3:.2f} TeV" for k, v in est.items()) + " (hybrid: 1.74 TeV)")
res["pgb"] = dict(unbroken=nun, broken=30, decomposition=dec, uneaten="Q + Qbar + U + Ubar", TeV_estimate_GeV=est,
                  note="GIFT-type (Goldstones instead of fine tuning) applied to Q + U: needs an accidental SO(10) of the Higgs-sector superpotential "
                       "(only SU(5) gauged); the 45 with a Dimopoulos-Wilczek VEV.  Scale estimate is dimensional, mechanism-dependent.")

# ======================================================================= (3)
ok = True; maxdep = 0
digits = range(-2, 3)
for xs in itertools.product(digits, repeat=3):
    for ys_ in itertools.product(digits, repeat=3):
        w_ = [a + b for a, b in zip(xs, ys_)]                                         # little-endian
        t = [1 if v >= 2 else (-1 if v <= -2 else 0) for v in w_]
        uu = [v - 3 * tt for v, tt in zip(w_, t)]
        s_ = [uu[i] + (t[i - 1] if i else 0) for i in range(3)] + [t[2]]
        val = lambda d: sum(c * 3 ** i for i, c in enumerate(d))
        ok &= val(s_) == val(xs) + val(ys_) and all(-2 <= c <= 2 for c in s_)
assert ok
print(f"(3) radix-3 signed-digit {{-2..2}} addition: exhaustive 3-digit check correct, every sum digit depends on 2 input positions (carry-free, depth O(1)); "
      f"storage {math.log2(5):.3f} bits per digit for {math.log2(3):.3f} bits of value: redundancy {math.log2(5) / math.log2(3) - 1:.0%}")
res["signed_digit"] = dict(correct=ok, locality=2, redundancy=math.log2(5) / math.log2(3) - 1,
                           note="carry-free like binary carry-save, but needs one carry-propagating conversion at the end")

# ======================================================================= (4)
NBB = 5.5e10
rng = np.random.default_rng(12713); N = 200000
L4, Rmax = 87.7, 0.2
R_ = 10 ** rng.uniform(-4, math.log10(Rmax / L4), N) * L4
Tm = 5.96 * (R_ / Rmax) ** (-1 / 3); TR = np.exp(rng.uniform(np.log(5.96), np.log(np.maximum(Tm, 5.961)), N))
Br = 1.3e-8 * (60 / TR) * (10 ** rng.uniform(math.log10(11), 2, N) / 10.56) / 10 ** rng.uniform(-1, 0, N)
rows = []
for etag in (0.002, 0.005):
    for esig in (0.1, 0.3):
        for bkg in (0, 10, 100):
            ul = 2.44 + 1.64 * math.sqrt(bkg)
            reach = ul / (NBB * 2 * etag * esig)          # two B per event, either can be tagged
            rows.append(dict(eps_tag=etag, eps_sig=esig, bkg=bkg, reach=reach, frac_B_prime=float(np.mean(Br >= reach))))
fr = [r["frac_B_prime"] for r in rows]; rc = [r["reach"] for r in rows]
print(f"(4) inclusive Belle II (50 ab^-1) reach {min(rc):.1e}-{max(rc):.1e}: covers {min(fr):.0%}-{max(fr):.0%} of B' (median need {np.median(Br):.1e})")
belle = dict(limit=3e-5, lumi=0.71, scaled=[3e-5 * 0.71 / 50, 3e-5 * math.sqrt(0.71 / 50)])
print(f"(4) Belle B -> Lambda + missing (<~3e-5 at 0.71 ab^-1) scaled to 50 ab^-1: {belle['scaled'][0]:.1e} (bkg-free) - {belle['scaled'][1]:.1e} (bkg-dominated), exclusive")
res["inclusive"] = dict(rows=rows, belle_scaling=belle)

# ======================================================================= (5)
rng = np.random.default_rng(5)
D, C, Ntr, Nte = 32, 10, 6000, 3000
Wt1 = rng.normal(size=(D, 64)); Wt2 = rng.normal(size=(64, C))
teacher = lambda X: np.argmax(np.tanh(X @ Wt1) @ Wt2, 1)
Xtr = rng.normal(size=(Ntr, D)); ytr = teacher(Xtr); Xte = rng.normal(size=(Nte, D)); yte = teacher(Xte)


def quant(W, mode):
    if mode == "binary": return np.sign(W) * np.abs(W).mean()
    if mode == "ternary":
        d = 0.7 * np.abs(W).mean(); m = np.abs(W) > d; a = np.abs(W[m]).mean() if m.any() else 0.0
        return np.sign(W) * m * a
    s = np.abs(W).mean(); lv = np.array([-1.5, -0.5, 0.5, 1.5]) * s
    return lv[np.argmin(np.abs(W[..., None] - lv), -1)]


sizes = [(D, 128), (128, 128), (128, C)]
bits = {"binary": 1.0, "ternary": 1.6, "2bit": 2.0}


def train(modes, seed, epochs=40, lr=0.05, bs=100):
    r = np.random.default_rng(seed)
    Ws = [r.normal(size=s) / math.sqrt(s[0]) for s in sizes]; bs_ = [np.zeros(s[1]) for s in sizes]
    for ep in range(epochs):
        idx = r.permutation(Ntr)
        for st in range(0, Ntr, bs):
            j = idx[st:st + bs]; h = [Xtr[j]]; Q = [quant(W, m) for W, m in zip(Ws, modes)]
            for l in range(3):
                z = h[-1] @ Q[l] + bs_[l]; h.append(np.maximum(z, 0) if l < 2 else z)
            z = h[-1] - h[-1].max(1, keepdims=True); p = np.exp(z); p /= p.sum(1, keepdims=True)
            g = p; g[np.arange(len(j)), ytr[j]] -= 1; g /= len(j)
            for l in (2, 1, 0):
                gW = h[l].T @ g; gb = g.sum(0)
                if l: g = (g @ Q[l].T) * (h[l] > 0)
                Ws[l] -= lr * gW; bs_[l] -= lr * gb
    Q = [quant(W, m) for W, m in zip(Ws, modes)]; h = Xte
    for l in range(3):
        h = h @ Q[l] + bs_[l]; h = np.maximum(h, 0) if l < 2 else h
    return float(np.mean(np.argmax(h, 1) == yte))


cfg = []
for modes in itertools.product(("binary", "ternary", "2bit"), repeat=3):
    a = float(np.mean([train(modes, s) for s in (0, 1)]))
    e = sum(bits[m] * s[0] * s[1] for m, s in zip(modes, sizes)) * 30e-6          # microjoules per inference
    cfg.append(dict(modes=modes, acc=a, energy_uJ=e))
cfg.sort(key=lambda c: c["energy_uJ"])
front = []; best = -1
for c in cfg:
    if c["acc"] > best + 1e-9: front.append(c); best = c["acc"]
for c in front:
    print(f"(5) Pareto: {'/'.join(c['modes']):24s} energy {c['energy_uJ']:.3f} uJ, accuracy {c['acc']:.3f}")
tern_share = np.mean([sum(m == "ternary" for m in c["modes"]) / 3 for c in front])
print(f"(5) ternary share of layers on the Pareto front: {tern_share:.0%} (uniform would be 33%)")
res["mixed"] = dict(configs=cfg, front=front, ternary_share_front=float(tern_share))
json.dump(res, open(os.path.join(ROOT, "data", "explore_pass12714_round.json"), "w", encoding="utf-8"), indent=1, default=str)
print("wrote data/explore_pass12714_round.json")
