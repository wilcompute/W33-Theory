"""Pass 12686: follow-ups to Passes 12684-12685 (intermediate-scale picture).
 (1) Electroweak T parameter of the vectorlike-quark rescue of the dark dimension (doublet Q + singlet T, Yukawa y' H Q T, no SM mixing),
     Lavoura-Silva formula for vectorlike quarks, calibrated on the SM top (T ~ N_c m_t^2/(16 pi s^2 c^2 M_Z^2)) and the custodial zero.
 (2) Joint test of the boundary conditions lambda(mu*) = 0 against (M_t, alpha_s, M_h), with the M_t pole/MC ambiguity as a nuisance.
 (3) SMASH-type quartic inflation with nonminimal coupling xi (U = lambda phi^4/4 / (1 + xi phi^2)^2 in Einstein frame): n_s, r vs xi
     and N_*, against P-ACT-LB n_s = 0.9743 +- 0.0034 and BK18 r < 0.036-0.038.
 (4) Dark-dimension neutrinos (Montero-Vafa-Valenzuela 2512.09052: m_nu ~ y^2 <H>^2 / M_5) in the rescued scenario: required y, KK masses.
 (5) Gravitational waves from post-inflationary global axion strings at f_a ~ 1e11 GeV versus LISA/PTA (scaling from Gorghetto-Hardy-
     Nicolaescu 2101.11007: detectable only for f_a >~ 1e14-1e15 GeV, Omega_GW ~ f_a^4 log^4).
 (6) Extra: the vectorlike family shifts all b_i by +2, so gauge unification differences are unchanged; couplings stay perturbative.
usage: py -3 analysis/toe_pass12686_intermediate_scale_followups.py"""
import json, math, os
import numpy as np
from scipy.optimize import brentq, minimize_scalar
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
G = {"__name__": "x", "__file__": os.path.join(HERE, "toe_pass12685_intermediate_scale_suite.py")}
src = open(os.path.join(HERE, "toe_pass12685_intermediate_scale_suite.py"), encoding="utf-8").read().split("res = {}")[0]
exec(src, G)
run, mu0, MPL, MPL_FULL = G["run"], G["mu0"], G["MPL"], G["MPL_FULL"]
res = {}
MZ, SW2 = 91.1876, 0.23122; CW2 = 1 - SW2; vEW = 246.22

# ---------------- (1) T parameter
def th_p(y1, y2):
    if abs(y1 - y2) < 1e-9 * max(y1, y2, 1e-30): return 0.0
    if y2 == 0: return y1
    if y1 == 0: return y2
    return y1 + y2 - 2 * y1 * y2 / (y1 - y2) * math.log(y1 / y2)
def th_m(y1, y2):
    if y1 == 0 or y2 == 0: return 0.0
    if abs(y1 - y2) < 1e-7 * max(y1, y2):
        return 0.0
    return 2 * math.sqrt(y1 * y2) * ((y1 + y2) / (y1 - y2) * math.log(y1 / y2) - 2)
def T_param(mu_up, mu_dn, VL, VR, Nc=3):
    """mu_up, mu_dn: masses; VL[a, i], VR[a, i]: charged-current couplings (2T^+ normalisation) between up a and down i.
    Neutral couplings U = V V^dag (up), D = V^dag V (down) (Lavoura-Silva 1993)."""
    yu = [(m / MZ) ** 2 for m in mu_up]; yd = [(m / MZ) ** 2 for m in mu_dn]
    UL, UR, DL, DR = VL @ VL.conj().T, VR @ VR.conj().T, VL.conj().T @ VL, VR.conj().T @ VR
    s = 0.0
    for a in range(len(yu)):
        for i in range(len(yd)):
            s += (abs(VL[a, i]) ** 2 + abs(VR[a, i]) ** 2) * th_p(yu[a], yd[i]) + 2 * (VL[a, i] * np.conj(VR[a, i])).real * th_m(yu[a], yd[i])
    for a in range(len(yu)):
        for b in range(a):
            s -= (abs(UL[a, b]) ** 2 + abs(UR[a, b]) ** 2) * th_p(yu[a], yu[b]) + 2 * (UL[a, b] * np.conj(UR[a, b])).real * th_m(yu[a], yu[b])
    for i in range(len(yd)):
        for j in range(i):
            s -= (abs(DL[i, j]) ** 2 + abs(DR[i, j]) ** 2) * th_p(yd[i], yd[j]) + 2 * (DL[i, j] * np.conj(DR[i, j])).real * th_m(yd[i], yd[j])
    return Nc / (16 * math.pi * SW2 * CW2) * s
# calibration: SM (t, b) with m_b = 0 must give Nc m_t^2/(16 pi s^2 c^2 M_Z^2); degenerate vectorlike doublet must give 0
Tsm = T_param([172.57], [0.0], np.array([[1.0]]), np.array([[0.0]]))
Tref = 3 * 172.57 ** 2 / (16 * math.pi * SW2 * CW2 * MZ ** 2)
Tdeg = T_param([2000.0], [2000.0], np.array([[1.0]]), np.array([[1.0]]))
print(f"(1) calibration: SM top T = {Tsm:.4f} (expected {Tref:.4f}); degenerate vectorlike doublet T = {Tdeg:.2e}")
assert abs(Tsm - Tref) < 1e-9 and abs(Tdeg) < 1e-9
def T_vl(M, yp, MT=None):
    MT = MT or M
    m = yp * vEW / math.sqrt(2)
    Mm = np.array([[M, m], [0.0, MT]])            # rows: L (T_Q, T_s), cols: R (T_Q, T_s)
    UL, sv, URh = np.linalg.svd(Mm); UR = URh.conj().T
    # charged current to B (mass M): left coupling = overlap of the up mass state with T_Q (both chiralities: Q is vectorlike)
    VL = np.array([[UL[0, a].conj()] for a in range(2)]); VR = np.array([[UR[0, a].conj()] for a in range(2)])
    return T_param(list(sv), [M], VL, VR)
rows = []
resc = json.load(open(os.path.join(ROOT, "data", "toe_pass12685_intermediate_scale_suite.json")))["dark_dimension_rescue_vectorlike"]
for r in resc:
    t = T_vl(r["M_VL"], r["y_prime_at_MVL"])
    rows.append(dict(M_VL=r["M_VL"], R_um=r["R_um"], y_prime=r["y_prime_at_MVL"], T=t))
    print(f"    M_VL = {r['M_VL']:.0f} GeV, y' = {r['y_prime_at_MVL']:.3f}: Delta T = {t:.4f}")
# split masses (M_T != M_Q) for robustness at 1.5 TeV
split = {str(mt): T_vl(1500.0, 0.51, mt) for mt in (1000.0, 1500.0, 2500.0)}
print("    1.5 TeV doublet, y' = 0.51, singlet mass 1.0/1.5/2.5 TeV: T =", {k: round(v, 4) for k, v in split.items()})
res["T_parameter"] = dict(calibration=dict(T_sm_top=Tsm, expected=Tref, degenerate_doublet=Tdeg), rescue=rows, split_singlet_mass=split,
                          bound="PDG 2024 global fit T = 0.03 +- 0.12 (2 sigma |Delta T| < ~0.27)")

# ---------------- (2) joint boundary-condition test
v = 246.22
def mt_for(mu, a3=0.1180, Mh=125.20):
    return brentq(lambda m: math.log(mu0(m, a3=a3, Mh=Mh)) - math.log(mu), 170.0, 177.5, xtol=1e-4)
hyp = {"sqrt(v M_Pl)": [math.sqrt(v * MPL_FULL)], "sqrt(v Mbar_Pl)": [math.sqrt(v * MPL)], "axion f_a (lattice 2025)": list(np.geomspace(57.2e11 / 65, 57.2e11 / 45, 5)),
       "M_GUT^2/M_Pl": [(2e16) ** 2 / MPL_FULL], "M_Pl": [MPL_FULL], "dark dimension M5 (R 1-30 um)": [5.71e8, 3.4e8, 1.84e8]}
dmt_da = (mt_for(math.sqrt(v * MPL_FULL), 0.1189) - mt_for(math.sqrt(v * MPL_FULL), 0.1171)) / 0.0018
joint = {}
for name, mus in hyp.items():
    best = None
    for mu in mus:
        mtp = mt_for(mu)
        for meas, sig, lab in ((172.57, 0.29, "direct"), (172.4, 0.7, "xsec pole")):
            s_tot = math.sqrt(sig ** 2 + 0.5 ** 2 * (lab == "direct") + (dmt_da * 0.0009) ** 2)
            chi2 = ((meas - mtp) / s_tot) ** 2
            key = lab
            if best is None: best = {}
            if key not in best or chi2 < best[key]["chi2"]: best[key] = dict(mu=mu, Mt_pred=mtp, chi2=chi2, pull=(meas - mtp) / s_tot)
    joint[name] = best
    print(f"(2) {name:32s}: " + "; ".join(f"{k}: M_t pred {b['Mt_pred']:.2f}, pull {b['pull']:+.2f}" for k, b in best.items()))
res["joint_boundary_test"] = dict(results=joint, note="direct mass gets +0.5 GeV pole/MC ambiguity; alpha_s 0.1180+-0.0009 propagated", dMt_dalpha=dmt_da)

# ---------------- (3) nonminimal quartic inflation (SMASH-like single-field limit), M_Pl reduced = 1
def infl(xi, N):
    U = lambda p: p ** 4 / 4 / (1 + xi * p * p) ** 2
    dchi = lambda p: math.sqrt((1 + xi * p * p + 6 * xi * xi * p * p) / (1 + xi * p * p) ** 2)
    def dU(p): return (p ** 3 / (1 + xi * p * p) ** 2 - xi * p ** 5 / (1 + xi * p * p) ** 3)
    eps = lambda p: 0.5 * (dU(p) / U(p) / dchi(p)) ** 2
    def eta(p):
        h = 1e-5 * p
        f = lambda q: dU(q) / dchi(q)
        return (f(p + h) - f(p - h)) / (2 * h) / dchi(p) / U(p)
    pend = brentq(lambda p: eps(p) - 1, 1e-3, 1e3)
    Nof = lambda p: quad(lambda q: U(q) / dU(q) * dchi(q) ** 2, pend, p, limit=200)[0]
    pstar = brentq(lambda p: Nof(p) - N, pend * 1.0001, 1e4)
    e, et = eps(pstar), eta(pstar)
    ns, r = 1 - 6 * e + 2 * et, 16 * e
    lam = 24 * math.pi ** 2 * 2.1e-9 * e / U(pstar)     # A_s = U/(24 pi^2 eps) with U = lambda * U(1)
    return ns, r, lam
infl_rows = []
for N in (50, 55, 60):
    for xi in (1e-3, 1e-2, 0.1, 1.0, 10.0, 1e3):
        ns, r, lam = infl(xi, N)
        infl_rows.append(dict(N=N, xi=xi, ns=ns, r=r, lam=lam, pull_ns=(ns - 0.9743) / 0.0034, r_ok=r < 0.037))
best = max(infl_rows, key=lambda d: -abs(d["pull_ns"]) if d["r_ok"] else -99)
for d in infl_rows:
    if d["N"] in (55, 60): print(f"(3) N={d['N']} xi={d['xi']:g}: n_s={d['ns']:.4f} r={d['r']:.4f} lambda={d['lam']:.2e} (n_s pull {d['pull_ns']:+.1f}, r ok {d['r_ok']})")
print(f"    best allowed point: {best}")
res["inflation"] = dict(rows=infl_rows, data="P-ACT-LB n_s = 0.9743 +- 0.0034, r < 0.037", best=best)

# ---------------- (4) dark-dimension neutrinos in the rescued scenario
GEV_INV_M = 1.97327e-16; H = 174.1
nu = []
for R in (1e-6, 30e-6):
    M5 = (MPL ** 2 / (2 * math.pi * R / GEV_INV_M)) ** (1 / 3)
    y = math.sqrt(0.05e-9 * M5) / H
    nu.append(dict(R_um=R * 1e6, M5=M5, y_for_0p05eV=y, m_KK_eV=GEV_INV_M / R * 1e9))
    print(f"(4) R={R * 1e6:.0f} um: M5={M5:.2e} GeV, y = {y:.2e} for m_nu3 = 0.05 eV; m_KK = {GEV_INV_M / R * 1e9:.3f} eV")
res["dark_dimension_neutrinos"] = dict(rows=nu, note="normal-ordering minimum sum 0.0588 eV vs DESI DR2 LCDM bound 0.064 eV (95%)")

# ---------------- (5) axion-string GWs
fa = 1e11
supp = (fa / 1e15) ** 4 * (math.log(fa / 1e-13) / math.log(1e15 / 1e-13)) ** 4   # relative to f_a = 1e15 (log ~ ln(f_a/H))
res["axion_string_GW"] = dict(f_a=fa, suppression_vs_fa_1e15=supp, note="GHN 2101.11007: global-string GWs reach LISA/ET only for f_a >~ 1e14-1e15 GeV")
print(f"(5) axion-string GW amplitude at f_a = 1e11 is ~{supp:.1e} of that at f_a = 1e15 (the detectability threshold): unobservable")

# ---------------- (6) vectorlike family and unification / perturbativity
sol, _ = run(172.57, vl=(1500.0, 0.509), mu_max=MPL)
g_end = sol.y[:3, -1]
res["vl_unification"] = dict(g_at_MPl=g_end.tolist(), note="Delta b_i = (2, 2, 2): b_i differences unchanged, so the SM non-unification pattern is unchanged")
print(f"(6) with the VL family (1.5 TeV): (gY, g2, g3) at M_Pl = {np.round(g_end, 3)}; differences of b_i unchanged")
json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12686_intermediate_scale_followups.json"), "w"), indent=1, default=float)
