"""Pass 12717 (Claude track).
 (1) Geometric protection: Sigma and H on branes separated by L in an extra dimension; cross couplings via bulk states of mass ~M_* are
     suppressed by e^{-M_* L}; the quality requirement (Pass 12715: Goldstone mass <= M_VL from a dimension-4 cross coupling) needs
     M_* L >= ln(a / M_VL).  Bound on the compactification scale 1/L; compatibility with the dark dimension (M5 ~ 1e9 < M_GUT: none).
 (2) Renormalisable 45 + 54 vacuum: W = m tr S45^2 + mu tr S54^2 + l tr(S45^2 S54) + k tr S54^3.  Analytic B-L solution
     (S54 = s diag(1_6, -3/2 1_4), s = -m/l, a^2 from F_54), numeric F = 0 check, Hessian on 45 + 54 = 99 directions: zero modes (30) and
     the masses of the LR-adjoint (8,1)+(1,3) remnants in units of m.
 (3) Proton decay in the hybrid: tau(p -> e+ pi0) ~ 1.6e34 yr (M_X / 1e16)^4 (alpha_G^-1 / 25)^2 (factor-10 hadronic uncertainty) with the
     two-loop M12 and alpha_G of the reference and the cutoff-1e17 pseudo-Goldstone spectrum (Pass 12716); Hyper-K reach ~1e35 yr.
     Dimension-5 (higgsino) suppressed by M_SS = 1e10.
 (4) Multi-level flash with near-capacity codes: bits/cell = I_q(SNR) (Pass 12711 tables) minus a 0.5 dB LDPC gap; reads per cell q - 1;
     bits per cell and bits per read vs SNR for q = 2, 3, 4, 8.
 (5) Ternary attention: single-head attention (numpy, manual backprop, gradient-checked) on a pointer task (class of the token after a marker),
     weights Wq, Wk, Wv, Wo in fp32 / binary / ternary / 2-bit with straight-through training; accuracy and zero fraction.
usage: py -3 analysis/explore_pass12717_round.py"""
import itertools, json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
res = {}

# ======================================================================= (1)
aG, MVL = 4.1e16, 1740.0
need = math.log(aG / MVL)
geo = []
for Ms in (1e17, 2.4e18):
    geo.append(dict(M_star=Ms, ML_min=need, KK_max=Ms / need))
    print(f"(1) M_* = {Ms:.1e}: need M_* L >= ln(a/M_VL) = {need:.1f} -> compactification scale 1/L <= {Ms / need:.1e} GeV")
print("(1) dark dimension: M5 ~ 1e9 GeV < M_GUT, so the hybrid's GUT cannot live in B''s dimension: geometric protection needs a separate small "
      "dimension, with bulk KK states at <~3e15-8e16 GeV (they must come in complete multiplets not to spoil unification)")
res["geometric"] = dict(rows=geo, incompatible_with_dark_dimension=True)

# ======================================================================= (2) 45 + 54
n = 10
A45 = []
for i in range(n):
    for j in range(i + 1, n):
        M = np.zeros((n, n)); M[i, j], M[j, i] = 1, -1; A45.append(M / math.sqrt(2))
S54 = []
for i in range(n):
    for j in range(i + 1, n):
        M = np.zeros((n, n)); M[i, j] = M[j, i] = 1; S54.append(M / math.sqrt(2))
for i in range(n - 1):
    d = np.zeros(n); d[:i + 1] = 1; d[i + 1] = -(i + 1); S54.append(np.diag(d) / np.linalg.norm(d))
assert len(A45) == 45 and len(S54) == 54
cplx = lambda A: np.block([[A.real, -A.imag], [A.imag, A.real]])
TBL = cplx(1j * np.diag([1, 1, 1, 0, 0]))
m_, mu_, l_, k_ = 1.0, -1.3, 1.0, 0.5
s1 = -m_ / l_
a2 = (2 * mu_ * s1 - 1.5 * k_ * s1 ** 2) / (0.4 * l_)
assert a2 > 0
S0 = math.sqrt(a2) * TBL
P0 = s1 * np.diag([1] * 3 + [-1.5] * 2 + [1] * 3 + [-1.5] * 2)        # (x1..x5, y1..y5): colour coords 0,1,2 and 5,6,7


def W(z):
    S = np.tensordot(z[:45], np.array(A45), 1); P = np.tensordot(z[45:], np.array(S54), 1)
    return m_ * np.trace(S @ S) + mu_ * np.trace(P @ P) + l_ * np.trace(S @ S @ P) + k_ * np.trace(P @ P @ P)


z0 = np.concatenate([[np.sum(S0 * b) for b in A45], [np.sum(P0 * b) for b in S54]])
h = 1e-5; E = np.eye(99) * h
grad = np.array([(W(z0 + E[i]) - W(z0 - E[i])) / (2 * h) for i in range(99)])
print(f"(2) 45 + 54 B-L vacuum (m={m_}, mu={mu_}, l={l_}, k={k_}): s = {s1}, a^2 = {a2:.3f}; |dW| = {np.linalg.norm(grad):.1e}")
assert np.linalg.norm(grad) < 1e-6
h = 1e-3; E = np.eye(99) * h; H = np.zeros((99, 99))
for i in range(99):
    for j in range(i, 99):
        H[i, j] = H[j, i] = (W(z0 + E[i] + E[j]) - W(z0 + E[i] - E[j]) - W(z0 - E[i] + E[j]) + W(z0 - E[i] - E[j])) / (4 * h * h)
ev = np.linalg.eigvalsh(H); aev = np.sort(np.abs(ev))
nz = int(np.sum(aev < 1e-5 * aev.max()))
vals, cnts = np.unique(np.round(aev[aev > 1e-5 * aev.max()], 3), return_counts=True)
spec = {float(v): int(c) for v, c in zip(vals, cnts)}
print(f"(2) Hessian on 45 + 54: {nz} zero modes (30 Goldstones expected); massive multiplicities {spec}")
assert nz == 30
res["v45_54"] = dict(params=dict(m=m_, mu=mu_, l=l_, k=k_), s=s1, a2=a2, zero_modes=nz, spectrum=spec,
                     note="all massive states have masses O(m, mu); with renormalisable couplings they sit at the 45/54 mass scale, e.g. ~1e17, "
                          "so the octet + triplet no longer spoil unification (Pass 12716)")

# ======================================================================= (3) proton decay
P16 = json.load(open(os.path.join(ROOT, "data", "explore_pass12716_round.json"), encoding="utf-8"))["unification"]
pd_ = []
for lab, (M12, ainv) in (("reference", (P16["reference"][0], P16["reference"][1])),
                         ("cutoff 1e17, lambda 4", next((r["M12"], None) for r in P16["rows"] if abs(r["lambda_"] - 4) < 1e-9 and r["M_cut"] == 1e17))):
    ai = ainv if ainv else P16["reference"][1]
    tau = 1.6e34 * (M12 / 1e16) ** 4 * (ai / 25) ** 2
    pd_.append(dict(case=lab, M12=M12, alpha_inv=ai, tau_years=tau, range=[tau / 10, tau * 10]))
    print(f"(3) {lab}: M_X = {M12:.2e}, alpha_G^-1 = {ai:.1f}: tau(p -> e+ pi0) ~ {tau:.1e} yr (x/10 hadronic); Hyper-K ~1e35: "
          f"{'unobservable' if tau / 10 > 1e35 else 'within reach'}")
res["proton"] = dict(rows=pd_, dim5="higgsino-mediated dimension-5 decay suppressed by sfermion masses ~M_SS = 1e10 GeV: negligible")

# ======================================================================= (4) flash
P11 = json.load(open(os.path.join(ROOT, "data", "explore_pass12711_ternary_noise.json")))["noisy_radix"]
snr = np.array(P11["snr"]); I = {int(k): np.array(v) for k, v in P11["I"].items()}
gap = 10 ** (-0.5 / 20)
fl = []
for s_show in (4.0, 8.0, 16.0, 32.0, 100.0):
    row = {"snr": s_show}
    for q in (2, 3, 4, 8):
        b = float(np.interp(s_show * gap, snr, I[q])); row[f"q{q}_bits"] = b; row[f"q{q}_per_read"] = b / (q - 1)
    fl.append(row)
    print(f"(4) SNR {s_show:5.1f}: bits/cell q=2 {row['q2_bits']:.2f}, q=3 {row['q3_bits']:.2f}, q=4 {row['q4_bits']:.2f}, q=8 {row['q8_bits']:.2f}; "
          f"bits per read {row['q2_per_read']:.2f} / {row['q3_per_read']:.2f} / {row['q4_per_read']:.2f} / {row['q8_per_read']:.2f}")
res["flash"] = dict(rows=fl, note="with near-capacity codes more levels never lose density; per sensing read, binary wins; ternary is the density step "
                                  "that costs the fewest extra reads (TLC-like trade-offs)")

# ======================================================================= (5) ternary attention
rng = np.random.default_rng(17)
T, Vc, C = 8, 10, 10
Din = Vc + 1 + T
Hd = 16


def make(Nn):
    X = np.zeros((Nn, T, Din)); y = np.zeros(Nn, int); mpos = np.zeros(Nn, int)
    for s in range(Nn):
        toks = rng.integers(0, Vc, T); m = rng.integers(0, T - 1)
        for t in range(T):
            if t == m: X[s, t, Vc] = 1
            else: X[s, t, toks[t]] = 1
            X[s, t, Vc + 1 + t] = 1
        y[s] = toks[m + 1]; mpos[s] = m
    return X, y, mpos


Xtr, ytr, mtr = make(4000); Xte, yte, mte = make(2000)


def quant(W, mode):
    if mode == "fp32": return W
    if mode == "binary": return np.sign(W) * np.abs(W).mean()
    if mode == "ternary":
        d = 0.7 * np.abs(W).mean(); msk = np.abs(W) > d; a = np.abs(W[msk]).mean() if msk.any() else 0.0
        return np.sign(W) * msk * a
    s = np.abs(W).mean(); lv = np.array([-1.5, -0.5, 0.5, 1.5]) * s
    return lv[np.argmin(np.abs(W[..., None] - lv), -1)]


def forward(P, X, m, mode):
    Q_, K_, V_, O_ = (quant(P[k], mode) for k in ("q", "k", "v", "o"))
    B_ = np.arange(len(X))
    xm = X[B_, m]                                                     # (N, Din)
    q = xm @ Q_; Kx = X @ K_; Vx = X @ V_                             # (N,H), (N,T,H)
    s = np.einsum("nh,nth->nt", q, Kx) / math.sqrt(Hd); s -= s.max(1, keepdims=True)
    a = np.exp(s); a /= a.sum(1, keepdims=True)
    o = np.einsum("nt,nth->nh", a, Vx)
    logits = o @ O_ + P["b"]
    return logits, (Q_, K_, V_, O_, xm, q, Kx, Vx, a, o)


def backward(P, X, m, y, mode):
    logits, (Q_, K_, V_, O_, xm, q, Kx, Vx, a, o) = forward(P, X, m, mode)
    z = logits - logits.max(1, keepdims=True); p = np.exp(z); p /= p.sum(1, keepdims=True)
    N_ = len(y); loss = -np.mean(np.log(p[np.arange(N_), y] + 1e-12))
    dl = p.copy(); dl[np.arange(N_), y] -= 1; dl /= N_
    g = {"o": o.T @ dl, "b": dl.sum(0)}
    do = dl @ O_.T
    da = np.einsum("nh,nth->nt", do, Vx); dV = np.einsum("nt,nh->nth", a, do)
    ds = a * (da - np.sum(da * a, 1, keepdims=True)) / math.sqrt(Hd)
    dq = np.einsum("nt,nth->nh", ds, Kx); dK = np.einsum("nt,nh->nth", ds, q)
    g["q"] = xm.T @ dq; g["k"] = np.einsum("ntd,nth->dh", X, dK); g["v"] = np.einsum("ntd,nth->dh", X, dV)
    return loss, g


def init(seed):
    r = np.random.default_rng(seed)
    return {"q": r.normal(size=(Din, Hd)) / math.sqrt(Din), "k": r.normal(size=(Din, Hd)) / math.sqrt(Din),
            "v": r.normal(size=(Din, Hd)) / math.sqrt(Din), "o": r.normal(size=(Hd, C)) / math.sqrt(Hd), "b": np.zeros(C)}


Pc = init(0); Xs, ys_, ms = Xtr[:16], ytr[:16], mtr[:16]
l0, gc = backward(Pc, Xs, ms, ys_, "fp32")
for key in ("q", "k", "v", "o"):
    idx = (3, 2) if key != "o" else (2, 3); e = 1e-6
    Pp = {k2: v2.copy() for k2, v2 in Pc.items()}; Pp[key][idx] += e
    Pm = {k2: v2.copy() for k2, v2 in Pc.items()}; Pm[key][idx] -= e
    num = (backward(Pp, Xs, ms, ys_, "fp32")[0] - backward(Pm, Xs, ms, ys_, "fp32")[0]) / (2 * e)
    assert abs(num - gc[key][idx]) < 1e-6 * max(1, abs(num)), (key, num, gc[key][idx])
print("(5) attention backprop gradient-checked (finite differences)")


def train(mode, seed, epochs=60, lr=0.01, bs=100):
    P = init(seed); mom = {k: np.zeros_like(v) for k, v in P.items()}; vel = {k: np.zeros_like(v) for k, v in P.items()}; t = 0
    r = np.random.default_rng(seed)
    for ep in range(epochs):
        idx = r.permutation(len(ytr))
        for s0 in range(0, len(ytr), bs):
            j = idx[s0:s0 + bs]; _, g = backward(P, Xtr[j], mtr[j], ytr[j], mode); t += 1
            for k in P:
                mom[k] = 0.9 * mom[k] + 0.1 * g[k]; vel[k] = 0.999 * vel[k] + 0.001 * g[k] ** 2
                P[k] -= lr * (mom[k] / (1 - 0.9 ** t)) / (np.sqrt(vel[k] / (1 - 0.999 ** t)) + 1e-8)
    logits, _ = forward(P, Xte, mte, mode)
    acc = float(np.mean(np.argmax(logits, 1) == yte))
    zf = float(np.mean([np.mean(quant(P[k], mode) == 0) for k in ("q", "k", "v", "o")]))
    return acc, zf


att = {}
for mode in ("fp32", "binary", "ternary", "2bit"):
    rs = [train(mode, s) for s in (0, 1)]
    att[mode] = dict(acc=float(np.mean([x[0] for x in rs])), acc_sd=float(np.std([x[0] for x in rs])), zero_frac=float(np.mean([x[1] for x in rs])))
    print(f"(5) attention {mode:7s}: test accuracy {att[mode]['acc']:.3f} +- {att[mode]['acc_sd']:.3f}, zero weights {att[mode]['zero_frac']:.0%}")
res["attention"] = dict(task="pointer: class of the token after a marker (T=8, 10 classes, positional one-hots), single head H=16, Adam 60 epochs, 2 seeds",
                        rows=att)
json.dump(res, open(os.path.join(ROOT, "data", "explore_pass12717_round.json"), "w", encoding="utf-8"), indent=1, default=str)
print("wrote data/explore_pass12717_round.json")
