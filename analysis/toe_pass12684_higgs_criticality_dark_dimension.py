"""Pass 12684: does the dark dimension's species scale coincide with the scale where the SM Higgs quartic vanishes?
Quantitative version of a coincidence noted qualitatively by Montero-Vafa-Valenzuela (arXiv:2205.12293: M_hat ~ Lambda^(1/12) M_pl^(2/3)
~ 1e9-1e10 GeV, 'may be related to the instability of the Higgs potential at ~1e11 GeV').

SM running: MSbar NNLO initial conditions at mu = M_t from Buttazzo et al. arXiv:1307.3536 (eqs. 57-61 fits), two-loop RGEs for
(gY, g2, g3, yt, lambda) with V = lambda (|H|^2 - v^2/2)^2.  VALIDATION: their 3-loop fit lambda(M_Pl) = -0.0143 - 0.0066 (M_t - 173.34)
+ 0.0018 (alpha3 - 0.1184)/0.0007 + 0.0029 (M_h - 125.15) must be reproduced to within the 2- vs 3-loop difference (a few 1e-3).

Dark dimension (one extra dimension of radius R, SM on a brane): M_5^3 = M_pl^2 / (2 pi R) with reduced M_pl = 2.435e18 GeV (the
2 pi R = circumference convention; other conventions shift M_5 by O(1) factors, reported as a band), m_KK = 1/R,
Lambda_DE^(1/4) = 2.25e-3 eV, R = lam * Lambda^(-1/4).
Hypothesis H: lambda_H(mu = M_5) = 0  (e.g. a high-scale SUSY threshold with tan beta = 1 at the species scale; Ibanez-Valenzuela 2013).
Outputs: mu_0(M_t, alpha3, M_h); the implied R, m_KK, lam, and the B-L dark-dimension neutrino scale m_nu ~ y^2 <H>^2 / M_5.
usage: py -3 analysis/toe_pass12684_higgs_criticality_dark_dimension.py"""
import json, math, os
import numpy as np
from scipy.integrate import solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
K = 1 / (16 * math.pi ** 2)


def beta(t, y):
    gY, g2, g3, yt, lam = y
    gY2, g22, g32, yt2 = gY * gY, g2 * g2, g3 * g3, yt * yt
    b1 = [41 / 6 * gY ** 3, -19 / 6 * g2 ** 3, -7 * g3 ** 3,
          yt * (9 / 2 * yt2 - 8 * g32 - 9 / 4 * g22 - 17 / 12 * gY2),
          24 * lam ** 2 - 6 * yt2 ** 2 + 12 * lam * yt2 - 3 * lam * (3 * g22 + gY2) + 3 / 8 * (2 * g22 ** 2 + (g22 + gY2) ** 2)]
    b2 = [gY ** 3 * (199 / 18 * gY2 + 9 / 2 * g22 + 44 / 3 * g32 - 17 / 6 * yt2),
          g2 ** 3 * (3 / 2 * gY2 + 35 / 6 * g22 + 12 * g32 - 3 / 2 * yt2),
          g3 ** 3 * (11 / 6 * gY2 + 9 / 2 * g22 - 26 * g32 - 2 * yt2),
          yt * (-12 * yt2 ** 2 + yt2 * (131 / 16 * gY2 + 225 / 16 * g22 + 36 * g32 - 12 * lam)
                + 1187 / 216 * gY2 ** 2 - 3 / 4 * g22 * gY2 + 19 / 9 * g32 * gY2 - 23 / 4 * g22 ** 2 + 9 * g22 * g32 - 108 * g32 ** 2 + 6 * lam ** 2),
          (-312 * lam ** 3 - 144 * lam ** 2 * yt2 + 36 * lam ** 2 * (3 * g22 + gY2) - 3 * lam * yt2 ** 2 + 80 * lam * g32 * yt2
           + 45 / 2 * lam * g22 * yt2 + 85 / 6 * lam * gY2 * yt2 - 73 / 8 * lam * g22 ** 2 + 39 / 4 * lam * g22 * gY2 + 629 / 24 * lam * gY2 ** 2
           + 30 * yt2 ** 3 - 32 * g32 * yt2 ** 2 - 8 / 3 * gY2 * yt2 ** 2 - 9 / 4 * g22 ** 2 * yt2 + 21 / 2 * g22 * gY2 * yt2 - 19 / 4 * gY2 ** 2 * yt2
           + 305 / 16 * g22 ** 3 - 289 / 48 * g22 ** 2 * gY2 - 559 / 48 * g22 * gY2 ** 2 - 379 / 48 * gY2 ** 3)]
    return [K * a + K * K * b for a, b in zip(b1, b2)]


def initial(Mt=173.34, Mh=125.15, a3=0.1184, MW=80.384):
    dt, da, dh, dw = Mt - 173.34, (a3 - 0.1184) / 0.0007, Mh - 125.15, (MW - 80.384) / 0.014
    return [0.35830 + 0.00011 * dt - 0.00020 * dw,
            0.64779 + 0.00004 * dt + 0.00011 * dw,
            1.1666 + 0.00314 * da - 0.00046 * dt,
            0.93690 + 0.00556 * dt - 0.00042 * da,
            0.12604 + 0.00206 * dh - 0.00004 * dt]


MPL = 2.435e18


def run(Mt=173.34, Mh=125.15, a3=0.1184):
    y0 = initial(Mt, Mh, a3)
    t1 = math.log(MPL / Mt)
    ev = lambda t, y: y[4]
    ev.terminal = False; ev.direction = -1
    sol = solve_ivp(beta, (0, t1), y0, rtol=1e-10, atol=1e-12, events=ev, dense_output=True)
    mu0 = Mt * math.exp(sol.t_events[0][0]) if len(sol.t_events[0]) else float("inf")
    return sol.y[4, -1], mu0, sol


# ---- validation against Buttazzo et al. 3-loop fit
val = []
for Mt, a3, Mh in [(173.34, 0.1184, 125.15), (172.34, 0.1184, 125.15), (173.34, 0.1191, 125.15), (173.34, 0.1184, 126.15)]:
    lp, mu0, _ = run(Mt, Mh, a3)
    ref = -0.0143 - 0.0066 * (Mt - 173.34) + 0.0018 * (a3 - 0.1184) / 0.0007 + 0.0029 * (Mh - 125.15)
    val.append(dict(Mt=Mt, a3=a3, Mh=Mh, lambda_MPl=lp, buttazzo_3loop=ref, diff=lp - ref, mu0=mu0))
    print(f"validation Mt={Mt} a3={a3} Mh={Mh}: lambda(M_Pl) = {lp:.5f} vs Buttazzo 3-loop {ref:.5f} (diff {lp - ref:+.5f}); lambda = 0 at {mu0:.3e} GeV")
assert all(abs(v["diff"]) < 0.004 for v in val), "2-loop running disagrees with the published 3-loop fit"
# ---- current inputs (PDG 2024/2025): M_t = 172.57 +- 0.29 (direct) ; pole-mass-from-xsec 172.4 +- 0.7 ; alpha_s = 0.1180 +- 0.0009 ; M_h = 125.20 +- 0.11
LAM4 = 2.25e-12   # GeV
scan = []
for Mt in np.arange(170.5, 176.01, 0.25):
    for a3 in (0.1171, 0.1180, 0.1189):
        lp, mu0, _ = run(Mt, 125.20, a3)
        scan.append(dict(Mt=float(Mt), a3=a3, mu0=mu0, lambda_MPl=lp))
# implied dark-dimension radius if M_5 = mu_0 (circumference convention) and the band from O(1) convention factors 1/(2pi) .. 1
def radius_from_M5(M5, conv=2 * math.pi):
    return MPL ** 2 / (conv * M5 ** 3)          # GeV^-1
GEV_INV_M = 1.97327e-16
rows = []
for r in scan:
    if not math.isfinite(r["mu0"]): continue
    R = radius_from_M5(r["mu0"]); Rlo, Rhi = radius_from_M5(r["mu0"], 2 * math.pi * 2 * math.pi), radius_from_M5(r["mu0"], 1.0)
    rows.append(dict(r, R_m=R * GEV_INV_M, R_band_m=(Rlo * GEV_INV_M, Rhi * GEV_INV_M), mKK_eV=1e9 / R, lam=R * LAM4,
                     m_nu_eV_y1e3=(1e-3) ** 2 * 174.0 ** 2 / r["mu0"] * 1e9))
# the dark-dimension window: 1 um <~ R <~ 30 um (fifth-force bound ~ 30-40 um; R ~ lam Lambda^-1/4 with lam 1e-4..1e-1 -> ~ 0.01..90 um)
for a3 in (0.1171, 0.1180, 0.1189):
    print(f"\nalpha_s = {a3}:")
    for r in rows:
        if r["a3"] == a3 and abs(r["Mt"] * 4 - round(r["Mt"] * 4)) < 1e-9 and abs(r["Mt"] - round(r["Mt"] * 2) / 2) < 1e-9:
            print(f"  M_t = {r['Mt']:.2f}: lambda=0 at mu0 = {r['mu0']:.2e} GeV -> R = {r['R_m'] * 1e6:.3g} um (band {r['R_band_m'][0] * 1e6:.2g}-{r['R_band_m'][1] * 1e6:.2g} um), m_KK = {r['mKK_eV']:.3g} eV")
# which M_t puts R in [1, 30] um (central convention)?
def mt_window(a3, Rmin=1e-6, Rmax=30e-6):
    ok = [r["Mt"] for r in rows if r["a3"] == a3 and Rmin <= r["R_m"] <= Rmax]
    return (min(ok), max(ok)) if ok else None
win = {str(a3): mt_window(a3) for a3 in (0.1171, 0.1180, 0.1189)}
print("\nM_t window putting R in the dark-dimension range [1, 30] um (circumference convention):", win)
json.dump(dict(validation=val, scan=rows, Mt_window_R_1_to_30um=win, conventions=dict(MPL_reduced=MPL, M5_cubed="MPL^2/(2 pi R)", Lambda_quarter_GeV=LAM4)),
          open(os.path.join(ROOT, "data", "toe_pass12684_higgs_criticality_dark_dimension.json"), "w"), indent=1)
# ---------------- Part 2: lambda = 0 at 'natural' scales, and the look-elsewhere control
from scipy.optimize import brentq
OFF3 = 0.155        # GeV: shift of the required M_t from the uniform 2- vs 3-loop offset (-0.0010 in lambda(M_Pl) / 0.0066 per GeV)
def mt_for_scale(mu, a3=0.1180, Mh=125.20):
    f = lambda Mt: math.log(run(Mt, Mh, a3)[1]) - math.log(mu)
    return brentq(f, 170.6, 177.0, xtol=1e-4) + OFF3
v = 246.22
scales = {"sqrt(v M_Pl), M_Pl = 1.2209e19": math.sqrt(v * 1.2209e19), "sqrt(v Mbar_Pl), reduced": math.sqrt(v * MPL),
          "sqrt(M_Z M_Pl)": math.sqrt(91.19 * 1.2209e19), "sqrt(m_t Mbar_Pl)": math.sqrt(172.57 * MPL),
          "dark dimension M_5, R = 1 um": (MPL ** 2 / (2 * math.pi * 1e-6 / GEV_INV_M)) ** (1 / 3),
          "dark dimension M_5, R = 30 um": (MPL ** 2 / (2 * math.pi * 30e-6 / GEV_INV_M)) ** (1 / 3),
          "M_GUT^2 / M_Pl (string SUSY-breaking, Ibanez-Valenzuela)": (2e16) ** 2 / 1.2209e19,
          "M_Pl (lambda(M_Pl) = 0)": 1.2209e19}
nat = {}
for k, mu in scales.items():
    try:
        mt = mt_for_scale(mu); da = mt_for_scale(mu, 0.1189) - mt
    except ValueError:
        mt, da = float("nan"), float("nan")
    nat[k] = dict(scale_GeV=mu, Mt_required=mt, dMt_per_alpha_s_sigma=da)
    print(f"  lambda = 0 at {k:55s} ({mu:.2e} GeV): M_t = {mt:.2f} GeV (+-{abs(da):.2f} from alpha_s)")
# look-elsewhere: log-uniform scale in [1e8, 1e19]; fraction whose required M_t is within 1 sigma of the measurement
MT_MEAS, SIG = 172.57, math.hypot(0.29, 0.32)
grid = np.linspace(8, 19, 221); req = []
for e in grid:
    try: req.append(mt_for_scale(10 ** e))
    except ValueError: req.append(float("nan"))
req = np.array(req); frac = float(np.mean(np.abs(req - MT_MEAS) < SIG))
print(f"look-elsewhere: a log-uniform scale in [1e8, 1e19] GeV matches M_t within 1 sigma ({SIG:.2f} GeV) with probability {frac:.3f}")
res = json.load(open(os.path.join(ROOT, "data", "toe_pass12684_higgs_criticality_dark_dimension.json")))
res.update(natural_scales=nat, look_elsewhere=dict(prior="log-uniform 1e8..1e19 GeV", sigma_GeV=SIG, probability_within_1sigma=frac,
                                                  log10_scale_grid=grid.tolist(), Mt_required=req.tolist()))
json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12684_higgs_criticality_dark_dimension.json"), "w"), indent=1)
# ---------------- Part 3: the post-inflationary QCD-axion window (Benabou-Buschmann-Foster-Safdi, PRL 2025: m_a in (45, 65) ueV)
# m_a = 57.2 ueV (1e11 GeV / f_a)  ->  f_a in (0.88, 1.27) x 1e11 GeV.  M_t for which lambda_H = 0 inside that window:
fa_lo, fa_hi = 57.2e11 / 65, 57.2e11 / 45
ax = {str(a3): (mt_for_scale(fa_hi, a3), mt_for_scale(fa_lo, a3)) for a3 in (0.1171, 0.1180, 0.1189)}
print(f"axion window f_a = {fa_lo:.2e}-{fa_hi:.2e} GeV: lambda_H = 0 there needs M_t in", {k: (round(a, 2), round(b, 2)) for k, b, a in [(k, *v) for k, v in ax.items()]})
# and the axion mass implied by f_a = mu_0 at the measured top mass
ma = {}
for Mt in (172.14, 172.57, 173.00):
    mu0 = run(Mt - OFF3, 125.20, 0.1180)[1]; ma[str(Mt)] = 57.2 * 1e11 / mu0
print("m_a (ueV) if f_a = mu_0(M_t):", {k: round(v, 1) for k, v in ma.items()})
res = json.load(open(os.path.join(ROOT, "data", "toe_pass12684_higgs_criticality_dark_dimension.json")))
res.update(axion_window=dict(source="Benabou et al. PRL 2025, m_a 45-65 ueV", fa_GeV=(fa_lo, fa_hi), Mt_required=ax, ma_ueV_if_fa_eq_mu0=ma))
json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12684_higgs_criticality_dark_dimension.json"), "w"), indent=1)
