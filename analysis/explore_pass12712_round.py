"""Pass 12712 (Claude track): five follow-ups to Passes 12710-12711.
 (1) Energy per bit of r-level signalling.  On chip (CMOS): every level gap needs the same on/off ratio, V_gap = n (kT/q) ln10 x decades,
     so the swing is (r-1) V_gap and energy/bit ~ (r-1)^2 V_gap^2 / log2 r.  Thermal-noise floor sqrt(kT/C) checked.  Links: eye penalty
     20 log10(r-1) dB vs channel loss alpha * f_Nyquist with f_Nyquist = D / (2 b_r) (b = 1, 1.5 (PAM3, 3 bits / 2 symbols), 2):
     which r maximises the margin at data rate D.
 (2) Light Q+U: literature status (generalised missing partner, arXiv:2308.11705) - no computation.
 (3) Exact RS graviton spectrum: J1(m/k) Y1(m e^{kL}/k) - Y1(m/k) J1(m e^{kL}/k) = 0; first mode at fixed spacing m_1 = 1 eV; species scale
     M_Pl^2 = (M5^3/k)(1 - e^{-2kL}); y' with the SM on the UV brane; where the warped B' meets the hybrid (0.470).
 (4) B' forecast: Monte Carlo over the surviving parameters (log lambda, T_RH in its window, log m_Phi in [11, 100] GeV, log |A_CP| in [0.1, 1])
     -> required BR; fraction testable at Belle II-like reach 1e-7 and at 1e-8; y' distribution and its overlap with the hybrid at FCC.
 (5) Quantisation-aware training (numpy): a 2-layer MLP on a synthetic 10-class task; full precision vs binary, ternary (TWN threshold
     0.7 mean|w|), 2-bit; straight-through estimator; test accuracy, fraction of zero weights, multiplications saved.
usage: py -3 analysis/explore_pass12712_round.py"""
import json, math, os
import numpy as np
from scipy.optimize import brentq
from scipy.special import j1, y1
from scipy.stats import norm
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
res = {}

# ======================================================================= (1)
kT_q = 0.02585; n_ss = 1.3; dec = 5
Vgap = n_ss * kT_q * math.log(10) * dec
sig_th = math.sqrt(1.380649e-23 * 300 / 1e-15)
onchip = {}
for r in (2, 3, 4):
    V = (r - 1) * Vgap; Vth = 2 * (r - 1) * sig_th * norm.isf(1e-15 / (2 * (1 - 1 / r)))
    onchip[r] = dict(swing_V=V, thermal_floor_V=Vth, energy_per_bit_rel=(r - 1) ** 2 / math.log2(r))
    print(f"(1) on-chip r={r}: swing {(r - 1) * Vgap:.2f} V (gap {Vgap:.3f} V, thermal floor {Vth * 1e3:.0f} mV at 1 fF), energy/bit x{(r - 1) ** 2 / math.log2(r):.2f} vs binary")
b = {2: 1.0, 3: 1.5, 4: 2.0}; pen = {r: 20 * math.log10(r - 1) for r in b}
c23 = pen[3] / (0.5 * (1 / b[2] - 1 / b[3])); c34 = (pen[4] - pen[3]) / (0.5 * (1 / b[3] - 1 / b[4]))
print(f"(1) links: margin_r(D) = -20log10(r-1) - alpha D/(2 b_r): NRZ best below {c23:.0f}/alpha Gb/s, PAM3 best in [{c23:.0f}, {c34:.1f}]/alpha, PAM4 above "
      f"(alpha in dB per GHz); for alpha ~ 1 dB/GHz PAM3's window is {c23:.0f}-{c34:.0f} Gb/s per pin (GDDR7 targets 32-48 Gb/s)")
res["energy"] = dict(V_gap=Vgap, thermal_sigma_1fF=sig_th, onchip=onchip, link_windows_alpha1=dict(NRZ_to_PAM3=c23, PAM3_to_PAM4=c34),
                     note="illustrative linear-in-f loss; PAM3 is the margin optimum only in a narrow band of loss x data rate")

# ======================================================================= (2)
res["light_QU"] = dict(candidate="generalised missing partner mechanism (arXiv:2308.11705): splits colour from electroweak components of vectorlike "
                                 "SU(5) 10-plets without fine-tuning; Q + U are the coloured part of a 10",
                       open="embedding in E6 (650 + 78 or 27 + 27bar sector); would remove the (M_VL/M_GUT)^2 penalty of Pass 12710")

# ======================================================================= (3) exact RS spectrum
src03 = open(os.path.join(HERE, "toe_pass12703_round.py"), encoding="utf-8").read()
G = {"__file__": os.path.join(HERE, "toe_pass12703_round.py")}
exec(src03.split("# ======================================================================= (4)")[0], G)
initial, beta_sm, beta_vl, OFF3 = (G[k] for k in ("initial", "beta_sm", "beta_vl", "OFF3"))
K = 1 / (16 * math.pi ** 2); MT, A3, MVL, MPL = 172.57, 0.1180, 1740.0, 2.435e18
dl = lambda y: (5 / 6) * 3 * K * y[5] ** 4 - 2 * y[4] * 3 * K * y[5] ** 2 / 3


def lam_end(yp, tgt):
    Mt0 = MT - OFF3; kw = dict(rtol=1e-9, atol=1e-12, max_step=0.5)
    y = solve_ivp(lambda t, y: beta_sm(*y[:5]) + [0.0], (0, math.log(MVL / Mt0)), np.array(initial(MT, 125.20, A3) + [yp]), **kw).y[:, -1].copy()
    y[4] += dl(y)
    return solve_ivp(lambda t, y: beta_vl(*y), (math.log(MVL / Mt0), math.log(tgt / Mt0)), y, **kw).y[:, -1][4]


ypt = lambda tgt: brentq(lambda p: lam_end(p, tgt), 0.2, 1.0, xtol=1e-6)


def x1(kL):
    """first root of J1(x e^{-kL}) Y1(x) - Y1(x e^{-kL}) J1(x) in x = m e^{kL}/k."""
    if kL < 1e-6: return None
    w = math.exp(-kL); f = lambda x: j1(x * w) * y1(x) - y1(x * w) * j1(x)
    xs = np.linspace(0.05, 12, 20000); v = [f(x) for x in xs]
    i = next(i for i in range(1, len(xs)) if v[i - 1] * v[i] < 0)
    return brentq(f, xs[i - 1], xs[i])


mKK = 1e-9; rows = []
for kL in (0.0, 1.0, 3.0, 5.0, 7.0, 10.0):
    if kL == 0:
        L = math.pi / mKK; M5 = (MPL ** 2 / (2 * L)) ** (1 / 3); xv = None
    else:
        xv = x1(kL); k = mKK * math.exp(kL) / xv; L = kL / k
        M5 = (MPL ** 2 * k / (1 - math.exp(-2 * kL))) ** (1 / 3)
    rows.append(dict(kL=kL, x1=xv, x1_flat_equiv=(math.pi * (1 - math.exp(-kL)) / kL * math.exp(kL)) if kL else None, M5=M5, y_UV=ypt(M5)))
    print(f"(3) kL = {kL:4.1f}: exact x1 = {xv if xv is None else round(xv, 4)}, M5 = {M5:.3e}, y'(UV brane) = {rows[-1]['y_UV']:.4f}")
yH = 0.4699
kcross = brentq(lambda kL: ypt((MPL ** 2 * (mKK * math.exp(kL) / x1(kL)) / (1 - math.exp(-2 * kL))) ** (1 / 3)) - yH, 3.0, 10.0, xtol=1e-3)
print(f"(3) exact spectrum: the warped B' (UV brane) reaches the hybrid's y' = {yH} at kL = {kcross:.2f} (interpolation in Pass 12710: ~7)")
res["rs_exact"] = dict(rows=rows, kL_cross_hybrid=kcross)

# ======================================================================= (4) B' forecast
rng = np.random.default_rng(12712); Nmc = 200000
L4, Rmax = 87.7, 0.2
loglam = rng.uniform(-4, math.log10(Rmax / L4), Nmc); R = 10 ** loglam * L4
Tmax = 5.96 * (R / Rmax) ** (-1 / 3); TR = np.exp(rng.uniform(np.log(5.96), np.log(np.maximum(Tmax, 5.961)), Nmc))
mPhi = 10 ** rng.uniform(math.log10(11), 2, Nmc); acp = 10 ** rng.uniform(-1, 0, Nmc)
Br = 1.3e-8 * (60 / TR) * (mPhi / (2 * 5.28)) / acp
fr = {f"reach {reach:.0e}": float(np.mean(Br >= reach)) for reach in (1e-6, 1e-7, 1e-8)}
# y' over R (flat, with the +0.004 gauge part of the mediator): interpolate the Pass 12707 rows
P07 = json.load(open(os.path.join(ROOT, "data", "toe_pass12707_round.json"), encoding="utf-8"))
rr = sorted((r["R_um"], r["yB"]) for r in P07["B_revised"]["rows"] if not r.get("excluded_by_2610_01825"))
yB = np.interp(np.log(R), np.log([a for a, _ in rr]), [b_ for _, b_ in rr]) + 0.0045
sep = (yB - yH) / math.hypot(0.005, 0.0036)
print(f"(4) B' needed BR: median {np.median(Br):.1e}, 90% range {np.percentile(Br, 5):.1e}-{np.percentile(Br, 95):.1e}; testable fraction: "
      + ", ".join(f"{k}: {v:.0%}" for k, v in fr.items()))
print(f"(4) B' y' (flat, mediator gauge part): {np.percentile(yB, 5):.3f}-{np.percentile(yB, 95):.3f}; FCC separation from the hybrid "
      f"(sigma_meas 0.005 (+) param 0.0036) >= 3 sigma in {np.mean(sep >= 3):.0%} of B' space, >= 5 sigma in {np.mean(sep >= 5):.0%}")
res["forecast"] = dict(Br_median=float(np.median(Br)), Br_90=[float(np.percentile(Br, 5)), float(np.percentile(Br, 95))], testable=fr,
                       y_range=[float(np.percentile(yB, 5)), float(np.percentile(yB, 95))], fcc_3sigma=float(np.mean(sep >= 3)), fcc_5sigma=float(np.mean(sep >= 5)))

# ======================================================================= (5) QAT
rng = np.random.default_rng(5)
D, H, C, Ntr, Nte = 32, 128, 10, 6000, 3000
Wt1 = rng.normal(size=(D, 64)); Wt2 = rng.normal(size=(64, C))
def teacher(X): return np.argmax(np.tanh(X @ Wt1) @ Wt2, 1)
Xtr = rng.normal(size=(Ntr, D)); ytr = teacher(Xtr); Xte = rng.normal(size=(Nte, D)); yte = teacher(Xte)


def quant(W, mode):
    if mode == "fp32": return W
    if mode == "binary": return np.sign(W) * np.abs(W).mean()
    if mode == "ternary":
        d = 0.7 * np.abs(W).mean(); m = np.abs(W) > d
        a = np.abs(W[m]).mean() if m.any() else 0.0
        return np.sign(W) * m * a
    if mode == "2bit":
        s = np.abs(W).mean() * 1.0; lv = np.array([-1.5, -0.5, 0.5, 1.5]) * s
        return lv[np.argmin(np.abs(W[..., None] - lv), -1)]


def train(mode, epochs=60, lr=0.05, bs=100, seed=0):
    r = np.random.default_rng(seed)
    W1 = r.normal(size=(D, H)) / math.sqrt(D); W2 = r.normal(size=(H, C)) / math.sqrt(H); b1 = np.zeros(H); b2 = np.zeros(C)
    for ep in range(epochs):
        idx = r.permutation(Ntr)
        for s in range(0, Ntr, bs):
            j = idx[s:s + bs]; X, y = Xtr[j], ytr[j]
            Q1, Q2 = quant(W1, mode), quant(W2, mode)
            h = np.maximum(X @ Q1 + b1, 0); z = h @ Q2 + b2; z -= z.max(1, keepdims=True); p = np.exp(z); p /= p.sum(1, keepdims=True)
            g = p; g[np.arange(len(y)), y] -= 1; g /= len(y)
            gW2 = h.T @ g; gh = g @ Q2.T * (h > 0); gW1 = X.T @ gh
            W2 -= lr * gW2; b2 -= lr * g.sum(0); W1 -= lr * gW1; b1 -= lr * gh.sum(0)       # straight-through: update latent weights
    Q1, Q2 = quant(W1, mode), quant(W2, mode)
    acc = float(np.mean(np.argmax(np.maximum(Xte @ Q1 + b1, 0) @ Q2 + b2, 1) == yte))
    zf = float((np.sum(Q1 == 0) + np.sum(Q2 == 0)) / (Q1.size + Q2.size))
    return acc, zf


bits = {"fp32": 32, "binary": 1, "ternary": math.log2(3), "2bit": 2}
qat = {}
for mode in ("fp32", "binary", "ternary", "2bit"):
    accs = [train(mode, seed=s) for s in range(3)]
    a = np.mean([x[0] for x in accs]); zf = np.mean([x[1] for x in accs])
    qat[mode] = dict(acc=float(a), acc_sd=float(np.std([x[0] for x in accs])), zero_frac=float(zf), bits_per_weight=bits[mode],
                     mults_per_weight=0.0 if mode in ("binary", "ternary") else 1.0, adds_skipped=float(zf))
    print(f"(5) {mode:7s}: test accuracy {a:.3f} +- {np.std([x[0] for x in accs]):.3f}, zero weights {zf:.0%}, {bits[mode]:.2f} bits/weight, "
          f"{'no multiplies' if mode in ('binary', 'ternary') else 'multiplies'}")
res["qat"] = dict(task="teacher MLP 32-64-10 (tanh), student 32-128-10 ReLU, 6000 train / 3000 test, 60 epochs, 3 seeds", rows=qat)
json.dump(res, open(os.path.join(ROOT, "data", "explore_pass12712_round.json"), "w", encoding="utf-8"), indent=1, default=float)
print("wrote data/explore_pass12712_round.json")
