"""Pass 12718 (Claude track).
 (1) 2-layer pre-LN transformer (single head per layer, d = 32, d_ff = 64) on associative recall (k1 v1 ... k4 v4 kq -> v of kq), numpy
     autodiff (tinygrad_np, gradient-checked); attention + MLP weights in fp32 / binary / ternary / 2-bit (straight-through), embeddings and
     readout in fp32.
 (2) Vectorlike-squark threshold at M_SS for the hybrid: lambda(M_SS) = 3 y'^4/(8 pi^2) (X - X^2/12) (stop-like formula, X = A^2/M_SS^2, tan beta = 1
     tree lambda = 0) instead of 0; y' for X = 0, 2, 6.
 (3) Whole-hybrid Z10 charge table: 16_i (q16), 10_H (q10), Sigma 45 (s), S 54 (t), H 16 (qh), Hbar (qhb), driver Y (y).  Required: 16 16 10,
     Sigma^2, S^2, Sigma^2 S, S^3, Y, Y (Hbar H)^5, a neutrino operator 16 16 Hbar Hbar (Hbar H)^c (any c <= 3).  Harmful: Hbar Sigma^k S^j H (Hbar H)^c
     (all VEV fields; k >= 1) below dimension 11.  Decay of the pseudo-Goldstone Q + U: Sigma 16 Hbar Sigma^k S^j (Hbar H)^c allowed at some
     dimension n with mixing m = a (a/M_Pl)^(n-3) in [1.7e-10, 300] GeV (BBN-safe decay, mixing <= 0.18).  Z10-SO(10)^2 anomaly:
     sum q T(R) = 0 mod 5 with T(10)=1, T(16)=2, T(45)=8, T(54)=12.
 (4) Flash endurance (illustrative): SNR(N) = SNR0 / (1 + (N/N0)^0.6), SNR0 = 40, N0 = 1000; for q levels and operating density d, lifetime
     N_max(d) where I_q(SNR) >= d / 0.95; total bits written per cell = d N_max, optimised over d.
 (5) Decision table (markdown, no computation): see PASS12718_ROUND.md.
usage: py -3 analysis/explore_pass12718_round.py"""
import itertools, json, math, os, sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from tinygrad_np import T, cross_entropy, ste
res = {}

# ======================================================================= (1) transformer
NK, NV, NP = 8, 8, 4
V = NK + NV; Tn = 2 * NP + 1; d, dff = 32, 64


def make(n, rng):
    X = np.zeros((n, Tn), int); y = np.zeros(n, int)
    for i in range(n):
        ks = rng.choice(NK, NP, replace=False); vs = rng.integers(0, NV, NP); j = rng.integers(NP)
        X[i, 0:2 * NP:2] = ks; X[i, 1:2 * NP:2] = NK + vs; X[i, -1] = ks[j]; y[i] = vs[j]
    return X, y


def quant(W, mode):
    if mode == "fp32": return W
    if mode == "binary": return np.sign(W) * np.abs(W).mean()
    if mode == "ternary":
        th = 0.7 * np.abs(W).mean(); m = np.abs(W) > th; a = np.abs(W[m]).mean() if m.any() else 0.0
        return np.sign(W) * m * a
    s = np.abs(W).mean(); lv = np.array([-1.5, -0.5, 0.5, 1.5]) * s
    return lv[np.argmin(np.abs(W[..., None] - lv), -1)]


mask = np.triu(np.full((Tn, Tn), -1e9), 1)


def init(seed):
    r = np.random.default_rng(seed); P = {"E": T(r.normal(size=(V, d)) * 0.3), "P": T(r.normal(size=(Tn, d)) * 0.3), "out": T(r.normal(size=(d, NV)) / math.sqrt(d))}
    for l in range(2):
        for nm, sh in (("q", (d, d)), ("k", (d, d)), ("v", (d, d)), ("o", (d, d)), ("1", (d, dff)), ("2", (dff, d))):
            P[f"{nm}{l}"] = T(r.normal(size=sh) / math.sqrt(sh[0]))
    return P


def model(P, X, mode):
    x = T(np.eye(V)[X]) @ P["E"] + P["P"]
    W = {k: (ste(v, lambda a: quant(a, mode)) if k[0] in "qkvo12" and k not in ("out",) else v) for k, v in P.items()}
    for l in range(2):
        h = x.layernorm(); q = h @ W[f"q{l}"]; k = h @ W[f"k{l}"]; v = h @ W[f"v{l}"]
        a = ((q @ k.tr()) * (1 / math.sqrt(d)) + mask).softmax()
        x = x + (a @ v) @ W[f"o{l}"]
        h = x.layernorm(); x = x + (h @ W[f"1{l}"]).relu() @ W[f"2{l}"]
    return x.layernorm().last() @ P["out"]


rng = np.random.default_rng(18)
Xtr, ytr = make(20000, rng); Xte, yte = make(3000, rng)
P = init(0); Xs, ys = Xtr[:8], ytr[:8]
L = cross_entropy(model(P, Xs, "fp32"), ys); L.backward()
for key, idx in (("q0", (1, 2)), ("21", (3, 4)), ("E", (2, 5))):
    g = P[key].grad[idx]; e = 1e-5; P[key].val[idx] += e
    lp = cross_entropy(model(P, Xs, "fp32"), ys).val; P[key].val[idx] -= 2 * e
    lm = cross_entropy(model(P, Xs, "fp32"), ys).val; P[key].val[idx] += e
    assert abs((lp - lm) / (2 * e) - g) < 1e-5 * max(1, abs(g)), (key, (lp - lm) / (2 * e), g)
print("(1) transformer autodiff gradient-checked")


def train(mode, seed, steps=2500, bs=128, lr=3e-3):
    P = init(seed); m1 = {k: np.zeros_like(v.val) for k, v in P.items()}; m2 = {k: np.zeros_like(v.val) for k, v in P.items()}
    r = np.random.default_rng(seed)
    for t in range(1, steps + 1):
        j = r.integers(0, len(ytr), bs)
        for v in P.values(): v.grad = np.zeros_like(v.val)
        L = cross_entropy(model(P, Xtr[j], mode), ytr[j]); L.backward()
        for k, v in P.items():
            m1[k] = 0.9 * m1[k] + 0.1 * v.grad; m2[k] = 0.999 * m2[k] + 0.001 * v.grad ** 2
            v.val -= lr * (m1[k] / (1 - 0.9 ** t)) / (np.sqrt(m2[k] / (1 - 0.999 ** t)) + 1e-8)
    acc = float(np.mean(np.argmax(model(P, Xte, mode).val, 1) == yte))
    zf = float(np.mean([np.mean(quant(v.val, mode) == 0) for k, v in P.items() if k[0] in "qkvo12" and k != "out"]))
    return acc, zf


tf = {}
for mode in ("fp32", "binary", "ternary", "2bit"):
    rs = [train(mode, s) for s in (0, 1)]
    tf[mode] = dict(acc=float(np.mean([x[0] for x in rs])), accs=[x[0] for x in rs], zero_frac=float(np.mean([x[1] for x in rs])))
    print(f"(1) 2-layer transformer, {mode:7s}: test accuracy {tf[mode]['acc']:.3f} (seeds {[round(a, 3) for a in tf[mode]['accs']]}), zero weights {tf[mode]['zero_frac']:.0%}")
res["transformer"] = dict(task="associative recall, 4 key-value pairs, 8 keys / 8 values, chance 0.125", rows=tf)

# ======================================================================= (2) VL squark threshold
src03 = open(os.path.join(HERE, "toe_pass12703_round.py"), encoding="utf-8").read()
G = {"__file__": os.path.join(HERE, "toe_pass12703_round.py")}
exec(src03.split("# ======================================================================= (4)")[0], G)
initial, beta_sm, beta_vl, OFF3 = (G[k] for k in ("initial", "beta_sm", "beta_vl", "OFF3"))
K = 1 / (16 * math.pi ** 2)
dl_ = lambda y: (5 / 6) * 3 * K * y[5] ** 4 - 2 * y[4] * 3 * K * y[5] ** 2 / 3


def lam_at(yp, tgt, mvl=1740.0):
    Mt0 = 172.57 - OFF3; kw = dict(rtol=1e-9, atol=1e-12, max_step=0.5)
    y = solve_ivp(lambda t, y: beta_sm(*y[:5]) + [0.0], (0, math.log(mvl / Mt0)), np.array(initial(172.57, 125.20, 0.1180) + [yp]), **kw).y[:, -1].copy()
    y[4] += dl_(y)
    return solve_ivp(lambda t, y: beta_vl(*y), (math.log(mvl / Mt0), math.log(tgt / Mt0)), y, **kw).y[:, -1]


sq = []
MSS = 8.45e9
for X_ in (0.0, 2.0, 6.0):
    f = lambda p: lam_at(p, MSS)[4] - 3 * p ** 4 / (8 * math.pi ** 2) * (X_ - X_ ** 2 / 12)
    yp = brentq(f, 0.2, 1.0, xtol=1e-6)
    sq.append(dict(X=X_, y=yp, dlam=3 * yp ** 4 / (8 * math.pi ** 2) * (X_ - X_ ** 2 / 12)))
    print(f"(2) VL-squark mixing X = {X_}: lambda(M_SS = {MSS:.1e}) = {sq[-1]['dlam']:.4f} -> hybrid y' = {yp:.4f} (shift {yp - sq[0]['y']:+.4f})")
res["squark_threshold"] = sq

# ======================================================================= (3) Z10 table
N = 10
Tidx = {"16": 2, "10": 1, "45": 8, "54": 12}
aG, MPl = 4.1e16, 2.435e18
sols = []
for q16, s, qh, qhb in itertools.product(range(N), range(N), range(N), range(N)):
    q10 = (-2 * q16) % N; t = 0; y = 0
    if (2 * s) % N or (2 * s + t) % N: continue
    p = (qh + qhb) % N
    if (y + 5 * p) % N: continue
    if not any((2 * q16 + 2 * qhb + c * p) % N == 0 for c in range(4)): continue
    harm = 99
    for k in range(1, 9):
        for j in range(0, 4):
            for c in range(0, 5):
                dd = k + j + 2 + 2 * c
                if dd < harm and (k * s + j * t + (1 + c) * p) % N == 0: harm = dd
    if harm < 11: continue
    dec = 99
    for k in range(0, 10):
        for j in range(0, 4):
            for c in range(0, 6):
                dd = 3 + k + j + 2 * c
                if dd < dec and ((k + 1) * s + j * t + q16 + qhb + c * p) % N == 0: dec = dd
    mmix = aG * (aG / MPl) ** (dec - 3) if dec < 99 else 0.0
    anom = (3 * q16 * Tidx["16"] + q10 * Tidx["10"] + s * Tidx["45"] + t * Tidx["54"] + qh * Tidx["16"] + qhb * Tidx["16"]) % (N // 2)
    p4 = (4 * q16) % N != 0
    sols.append(dict(q16=q16, q10=q10, s=s, qh=qh, qhb=qhb, harm=harm, decay_dim=dec, m_mix=mmix, decay_ok=1.7e-10 <= mmix <= 300,
                     anomaly_free=anom == 0, forbids_16_4=p4))
good = [x for x in sols if x["decay_ok"] and x["anomaly_free"]]
print(f"(3) Z10 assignments passing quality (harmful >= dim 11): {len(sols)}; with a BBN-safe PGB decay operator: "
      f"{sum(x['decay_ok'] for x in sols)}; also anomaly-free: {len(good)}; also forbidding 16^4 (dim-5 proton decay): {sum(x['forbids_16_4'] for x in good)}")
if good:
    ex = sorted(good, key=lambda x: (not x["forbids_16_4"], x["decay_dim"]))[0]
    print(f"(3) example: q16={ex['q16']}, q10={ex['q10']}, s(45)={ex['s']}, t(54)=0, qH={ex['qh']}, qHbar={ex['qhb']}, Y=0: harmful from dim {ex['harm']}, "
          f"PGB decay operator at dim {ex['decay_dim']} (mixing mass {ex['m_mix']:.1e} GeV)")
res["z10"] = dict(n_quality=len(sols), n_decay=sum(x["decay_ok"] for x in sols), n_good=len(good), examples=good[:10])

# ======================================================================= (4) flash endurance
P11 = json.load(open(os.path.join(ROOT, "data", "explore_pass12711_ternary_noise.json")))["noisy_radix"]
snr_t = np.array(P11["snr"]); I = {int(k): np.array(v) for k, v in P11["I"].items()}
Ns = np.logspace(1, 6, 400)
SNRn = 40 / (1 + (Ns / 1000) ** 0.6)
endu = {}
for q in (2, 3, 4, 8):
    cap = np.interp(SNRn, snr_t, I[q])
    best = (0, 0, 0)
    for dd in np.linspace(0.1, math.log2(q), 60):
        ok = cap >= dd / 0.95
        nmax = Ns[ok][-1] if ok.any() else 0.0
        if dd * nmax > best[0]: best = (dd * nmax, dd, nmax)
    endu[q] = dict(total_bits=float(best[0]), density=float(best[1]), cycles=float(best[2]))
    print(f"(4) q = {q}: best operating density {best[1]:.2f} bits/cell, lifetime {best[2]:.0f} cycles, lifetime-integrated {best[0]:.0f} bits/cell")
res["flash_endurance"] = endu
json.dump(res, open(os.path.join(ROOT, "data", "explore_pass12718_round.json"), "w", encoding="utf-8"), indent=1, default=str)
print("wrote data/explore_pass12718_round.json")
