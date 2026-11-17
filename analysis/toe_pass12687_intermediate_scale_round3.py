"""Pass 12687: third round on the intermediate-scale picture (Passes 12684-12686).
 (1) Leading three-loop QCD terms added to the running: beta_g3 += (65/2) g3^7/(16pi^2)^3 (pure QCD, n_f = 6) and
     beta_yt += -619.4 yt g3^6/(16pi^2)^3 (3-loop quark-mass anomalous dimension, gamma_2(n_f=6) = 4.839 in alpha_s/pi units).
     Test: does the uniform offset to the Buttazzo et al. 3-loop lambda(M_Pl) fit shrink from -0.0010?
 (2) SMASH reheating: N_* for k = 0.05/Mpc with instant (radiation-like) reheating, from the inflationary energy scale, and n_s there.
 (3) Vectorlike top partners: the rescue (Pass 12685) mass spectrum (two charge-2/3 states + one B), against LHC limits (input from
     the literature: ~1.49 TeV singlet pair production, ~1.5-1.6 TeV (T,B) doublet).
 (4) Combined likelihood (pulls in M_t, n_s, N_eff) for the competing hypotheses, with AIC.
 (5) Dark radiation of the dark dimension: g* = 3 (5D graviton) + 6 (bulk nu, fermionic) decoupled above the EW scale gives
     Delta N_eff = (4/7)(3 + 7/8*6)(10.75/g_s)^(4/3) ~ 0.22 (2411.07029 benchmark); vs ACT DR6 P-ACT-LB N_eff = 2.86 +- 0.13; and with the
     vectorlike family in the plasma (g_s 106.75 -> 138.25).
usage: py -3 analysis/toe_pass12687_intermediate_scale_round3.py"""
import json, math, os
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
G = {"__name__": "x", "__file__": os.path.join(HERE, "toe_pass12685_intermediate_scale_suite.py")}
exec(open(os.path.join(HERE, "toe_pass12685_intermediate_scale_suite.py"), encoding="utf-8").read().split("res = {}")[0], G)
beta_sm, MPL, MPL_FULL, K = G["beta_sm"], G["MPL"], G["MPL_FULL"], G["K"]
res = {}

# ---------------- (1) leading 3-loop QCD terms
def initial_raw(Mt, Mh=125.15, a3=0.1184, MW=80.384):
    dt, da, dh, dw = Mt - 173.34, (a3 - 0.1184) / 0.0007, Mh - 125.15, (MW - 80.384) / 0.014
    return [0.35830 + 0.00011 * dt - 0.00020 * dw, 0.64779 + 0.00004 * dt + 0.00011 * dw, 1.1666 + 0.00314 * da - 0.00046 * dt,
            0.93690 + 0.00556 * dt - 0.00042 * da, 0.12604 + 0.00206 * dh - 0.00004 * dt]
def lam_MPl(Mt, Mh=125.15, a3=0.1184, three=False):
    def rhs(t, y):
        d = beta_sm(*y)
        if three:
            d[2] += K ** 3 * 65 / 2 * y[2] ** 7
            d[3] += K ** 3 * (-619.4) * y[3] * y[2] ** 6
        return d
    s = solve_ivp(rhs, (0, math.log(MPL / Mt)), initial_raw(Mt, Mh, a3), rtol=1e-10, atol=1e-12)
    return s.y[4, -1]
pts = [(173.34, 125.15, 0.1184), (172.34, 125.15, 0.1184), (173.34, 125.15, 0.1191), (173.34, 126.15, 0.1184)]
three = []
for Mt, Mh, a3 in pts:
    ref = -0.0143 - 0.0066 * (Mt - 173.34) + 0.0018 * (a3 - 0.1184) / 0.0007 + 0.0029 * (Mh - 125.15)
    l2, l3 = lam_MPl(Mt, Mh, a3), lam_MPl(Mt, Mh, a3, True)
    three.append(dict(Mt=Mt, Mh=Mh, a3=a3, ref=ref, two_loop=l2, with_3loop_QCD=l3, off2=l2 - ref, off3=l3 - ref))
    print(f"(1) Mt={Mt} Mh={Mh} a3={a3}: Buttazzo {ref:+.5f} | 2-loop {l2:+.5f} (off {l2 - ref:+.5f}) | +3-loop QCD {l3:+.5f} (off {l3 - ref:+.5f})")
res["three_loop_qcd"] = three

# ---------------- (2) SMASH reheating N_*
def infl_state(xi, N):
    U = lambda p: p ** 4 / 4 / (1 + xi * p * p) ** 2
    dchi = lambda p: math.sqrt((1 + xi * p * p + 6 * xi * xi * p * p) / (1 + xi * p * p) ** 2)
    dU = lambda p: p ** 3 / (1 + xi * p * p) ** 2 - xi * p ** 5 / (1 + xi * p * p) ** 3
    eps = lambda p: 0.5 * (dU(p) / U(p) / dchi(p)) ** 2
    def eta(p):
        h = 1e-5 * p; f = lambda q: dU(q) / dchi(q)
        return (f(p + h) - f(p - h)) / (2 * h) / dchi(p) / U(p)
    pend = brentq(lambda p: eps(p) - 1, 1e-3, 1e3)
    Nof = lambda p: quad(lambda q: U(q) / dU(q) * dchi(q) ** 2, pend, p, limit=200)[0]
    ps = brentq(lambda p: Nof(p) - N, pend * 1.0001, 1e4)
    lam = 24 * math.pi ** 2 * 2.1e-9 * eps(ps) / U(ps)
    return dict(ns=1 - 6 * eps(ps) + 2 * eta(ps), r=16 * eps(ps), Vstar=lam * U(ps), Vend=lam * U(pend))
reh = []
for xi in (0.1, 1.0, 10.0, 1000.0):
    N = 57.0
    for _ in range(30):     # fixed point: N_* = 61.6 - ln(k/a0H0 ~ 222)... Liddle-Leach with instant reheating (w = 1/3)
        st = infl_state(xi, N)
        Nn = 66.89 - math.log(0.05 / 2.25e-4) + 0.25 * math.log(st["Vstar"] ** 2 / (1.5 * st["Vend"])) - (1 / 12) * math.log(106.75)
        if abs(Nn - N) < 1e-4: break
        N = Nn
    reh.append(dict(xi=xi, N_star=N, ns=st["ns"], r=st["r"], pull_ns=(st["ns"] - 0.9743) / 0.0034))
    print(f"(2) xi={xi:g}: instant reheating N_* = {N:.2f}, n_s = {st['ns']:.4f} (pull {(st['ns'] - 0.9743) / 0.0034:+.2f}), r = {st['r']:.4f}")
res["smash_reheating"] = reh

# ---------------- (3) vectorlike spectrum vs LHC limits
vEW = 246.22
spec = []
for M, yp in ((1500.0, 0.509), (3000.0, 0.498), (10000.0, 0.484)):
    sv = np.linalg.svd(np.array([[M, yp * vEW / math.sqrt(2)], [0.0, M]]), compute_uv=False)
    spec.append(dict(M_VL=M, y_prime=yp, T_masses=sorted(sv.tolist()), B_mass=M, lightest=float(min(sv)),
                     above_singlet_limit_1p49=bool(min(sv) > 1490), above_doublet_limit_1p6=bool(min(sv) > 1600)))
    print(f"(3) M_VL={M:.0f}: T masses {np.round(sorted(sv), 1)}, B {M:.0f}; lightest above 1.49 TeV: {min(sv) > 1490}, above 1.6 TeV: {min(sv) > 1600}")
res["vectorlike_spectrum"] = dict(rows=spec, limits="2412.01761 review: singlet T pair production < 1.49 TeV excluded; ATLAS (T,B) doublet < 1.6 TeV (BR-dependent)")

# ---------------- (5) dark radiation
def dNeff(gs, gstar_b=3.0, gstar_f=6.0):
    return 4 / 7 * (gstar_b + 7 / 8 * gstar_f) * (10.75 / gs) ** (4 / 3)
NEFF, SNEFF = 2.86, 0.13
dr = {}
for lab, gs in (("SM plasma at decoupling (g_s = 106.75)", 106.75), ("+ vectorlike Q+T (g_s = 138.25)", 106.75 + 7 / 8 * 36),
                ("+ VL + PQ fields + KSVZ quark + 3 nu_R (g_s ~ 156; only if T_dec > 1e11 GeV)", 106.75 + 7 / 8 * 36 + 2 + 7 / 8 * 12 + 7 / 8 * 6)):
    d = dNeff(gs); dr[lab] = dict(g_s=gs, dNeff=d, pull=(3.044 + d - NEFF) / SNEFF)
    print(f"(5) {lab}: Delta N_eff = {d:.3f}, N_eff = {3.044 + d:.3f}, pull vs ACT {(3.044 + d - NEFF) / SNEFF:+.2f} sigma")
res["dark_radiation"] = dict(rows=dr, data="ACT DR6 P-ACT-LB N_eff = 2.86 +- 0.13; P-ACT Delta N_eff < 0.14 (95%); relaxed to < 0.58 with running (2604.26541)")

# ---------------- (4) combined likelihood
p12686 = json.load(open(os.path.join(ROOT, "data", "toe_pass12686_intermediate_scale_followups.json")))["joint_boundary_test"]["results"]
pull_mt = {k: v["direct"]["pull"] for k, v in p12686.items()}
best_ns = max(reh, key=lambda d: d["pull_ns"])["pull_ns"]
SMpull_neff = (3.044 - NEFF) / SNEFF
models = {
    "SM + LCDM (free M_t, free n_s)": dict(pulls=[SMpull_neff], k=0),
    "boundary lambda(sqrt(v M_Pl)) = 0": dict(pulls=[pull_mt["sqrt(v M_Pl)"], SMpull_neff], k=0),
    "boundary at axion f_a (lattice)": dict(pulls=[pull_mt["axion f_a (lattice 2025)"], SMpull_neff], k=0),
    "full SMASH (f_a boundary + its inflation)": dict(pulls=[pull_mt["axion f_a (lattice 2025)"], best_ns, SMpull_neff], k=0),
    "lambda(M_Pl) = 0 (AS / MPP)": dict(pulls=[pull_mt["M_Pl"], SMpull_neff], k=0),
    "dark dimension, no new states": dict(pulls=[pull_mt["dark dimension M5 (R 1-30 um)"], dr["SM plasma at decoupling (g_s = 106.75)"]["pull"]], k=0),
    "dark dimension + VL quark (y' fitted)": dict(pulls=[0.0, dr["+ vectorlike Q+T (g_s = 138.25)"]["pull"]], k=1),
}
for k, m in models.items():
    m["chi2"] = float(sum(p * p for p in m["pulls"])); m["AIC"] = m["chi2"] + 2 * m["k"]
base = models["SM + LCDM (free M_t, free n_s)"]["AIC"]
for k, m in models.items():
    m["dAIC_vs_SM"] = m["AIC"] - base
    print(f"(4) {k:45s}: chi2 = {m['chi2']:.2f}, k = {m['k']}, Delta AIC vs SM = {m['dAIC_vs_SM']:+.2f}")
res["combined_likelihood"] = dict(models=models, note="pulls: M_t (direct, with 0.5 GeV pole/MC ambiguity), n_s (P-ACT-LB), N_eff (P-ACT-LB). "
                                                     "Boundary models predict M_t with no free parameter; SMASH n_s at instant-reheating N_*.")
json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12687_intermediate_scale_round3.json"), "w"), indent=1, default=float)
