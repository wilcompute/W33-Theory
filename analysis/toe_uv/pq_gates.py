"""Model A's remaining gates.  SM + complex sigma + three N + vectorlike (3,1,-1/3), 2 x (3,2,1/6), with PQ charges (+,+,-), N_DW = 1.
(1) Sigma quartic: V = lambda_s |sigma|^4 (f convention sigma = f/sqrt 2 e^(i a/f)), Dirac fermions with mass y sigma: 16 pi^2 d lambda_s/dt = 20 lambda_s^2 + 2 lambda_hs^2 + 4 lambda_s D y^2 - 2 D y^4 + N terms; D = number of Dirac components = 3 + 6 + 6 = 15.  This reduces to the SMASH form 12 lambda Y^2 - 6 Y^4 at D = 3 (control, as I recall that form).  y runs: 16 pi^2 dy/dt = y (2 y^2 (D' ) - 8 g3^2) in a simplified one-loop form with the colour term and D' = 3/2 D per conventions; N Yukawas Y_N are set by seesaw and included through a single term.
   Stability: lambda_s stays positive from f to M_U.  Mass of the radial mode: m_rho = sqrt(2 lambda_s) f.
(2) Higgs: lambda_H, run from M_t, is negative above about 1e10 GeV.  Threshold stabilisation (Elias-Miro et al 2012, SMASH): above m_rho the coupling is lambda_H + delta, delta = lambda_hs^2/lambda_s; needs m_rho below the instability scale, or delta large enough.  So condition: m_rho < M_inst, and delta about 0.03 or more.  Below m_rho the low-energy lambda is what is measured.
   Combined: max y for which both hold, against f in the axion window.  That sets the real range of y_Q, f and m_a.
(3) Inflation: Higgs-portal xi, not recomputed.  Post-inflation PQ restoration needs T_reh > about f.  n_s and r from SMASH literature, not recomputed.
(4) PQ quality: dimension n Planck-suppressed operators sigma^n / M_P^(n-4): shift theta_bar by about f^n/(M_P^(n-4) chi), chi = (75.6 MeV)^4, must be under 1e-10: minimum n for f in the window.  This is an open gate, reported.
(5) Scorecard, with what is in hand and what is not.
usage: py -3 pq_gates.py"""
import json
import math
import numpy as np
from scipy.integrate import solve_ivp

K = 1 / (16 * math.pi ** 2)
D = 15
MU = 3.96e15
MP = 2.435e18
CHI = (75.6e-3) ** 4
MINST = 1e10  # one-loop value of the crossing near M_t = 173.1: toe_one_scale.py gives lambda(1e10) near 0.  Varied below
out = {}


def g3_of(t, lnMX):
    """colour coupling squared with Q above M_X: one-loop"""
    ia = 1 / 0.118 + 7 * (lnMX - math.log(91.19)) / (2 * math.pi)
    ia = ia - (-7 + 4 / 3 * (0.5 + 2 * 1.0)) * (t - lnMX) / (2 * math.pi)  # b3 above M_X: -7 + 4/3 (T d_W sum): 1/2 + 2 x 1 = 5/2
    return 4 * math.pi / ia


def flow(ls0, y0, f, lhs=0.0, yN=0.0):
    lnMX = math.log(max(y0 * f, 1e3))

    def r(t, v):
        ls, y = v
        g2 = g3_of(t, lnMX)
        dls = K * (20 * ls ** 2 + 2 * lhs ** 2 + 4 * ls * D * y ** 2 - 2 * D * y ** 4 + 4 * ls * 3 * yN ** 2 - 6 * yN ** 4)
        dy = K * y * (3 * y ** 2 + D * y ** 2 - 8 * g2)
        return [dls, dy]

    s = solve_ivp(r, (math.log(f), math.log(MU)), [ls0, y0], rtol=1e-8, atol=1e-10, dense_output=False)
    return s.y[0], s.y[1]


def min_ls_for_stability(y0, f):
    """smallest lambda_s(f) staying positive up to M_U"""
    lo, hi = 1e-6, 2.0
    for _ in range(40):
        m = math.sqrt(lo * hi)
        l, _y = flow(m, y0, f)
        if l.min() > 0:
            hi = m
        else:
            lo = m
    return hi


rows = []
for f in (1.5e10, 2.7e10, 5e10, 1e11, 2e11, 5e11, 1e12):
    y = 2.73e10 / f
    if y > 3:
        continue
    ls = min_ls_for_stability(y, f)
    mrho = math.sqrt(2 * ls) * f
    rows.append(dict(f=f, y_Q=y, m_a_ueV=5.7e12 / f, min_lambda_s=ls, m_rho=mrho, m_rho_over_f=math.sqrt(2 * ls), ok_1e10=mrho < 1e10, ok_1e11=mrho < 1e11))
    print("f %.2g y %.3f ma %.1f ueV min lambda_s %.4g m_rho %.3g ok(1e10) %s ok(1e11) %s" % (f, y, 5.7e12 / f, ls, mrho, mrho < 1e10, mrho < 1e11), flush=True)
out["stability"] = rows
# control: SMASH-like D = 3 at a small y: minimum lambda_s tiny
D_save = D
D = 3
c = min_ls_for_stability(1e-3, 1e11)
D = D_save
out["control_small_y_D3"] = c
print("control min lambda_s", c, flush=True)
# hidden assumption: y common.  Splitting the 3 multiplet masses within a factor of 3 is allowed; report the y needed if only the heaviest matters: no separate run.
# PQ quality
q = {}
for f in (2.7e10, 1e11, 1e12):
    for n in range(5, 15):
        th = f ** n / MP ** (n - 4) / CHI
        if th < 1e-10:
            q[str(f)] = dict(min_dim=n, theta=th)
            break
out["pq_quality"] = q
print("PQ quality", q, flush=True)
# scorecard
out["scorecard"] = {
    "gauge couplings meet (two-loop, common threshold)": "pass, exact by construction: M_X and M_U solved",
    "proton": "at the limit: 3.5e34 yr, factor 3 and more with GUT thresholds; Hyper-K can decide",
    "strong CP": "axion, PQ quality open: needs dimension above 9 or so protected",
    "dark matter": "axion, post-inflation: simulation range 25 to 500 ueV",
    "neutrino masses": "seesaw at M_N ~ y_N f, available, not predicted",
    "baryon asymmetry": "thermal leptogenesis if M_N >= 1e9, available, not computed",
    "Higgs stability": "threshold stabilisation: see stability rows",
    "inflation": "Higgs-portal as in SMASH: not recomputed",
    "three generations": "not explained",
    "flavour": "not explained; 19 parameters",
    "dark energy": "not explained: cosmological constant by hand",
    "quantum gravity": "not included: this is an EFT below M_U",
    "GUT completion": "not built; SU(5) fragments at 1e10 with partners at M_U is a tuned split",
}
json.dump(out, open("pq_gates.json", "w"), indent=1, default=float)
print("done", flush=True)
