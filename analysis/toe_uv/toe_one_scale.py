"""One action, one scale: D3-branes at C^3/Z_3 (Aldazabal, Ibanez, Quevedo, Uranga hep-th/0005067), left-right model.
Everything below is forced by one number M_s, except stated order-one factors.  The paper assumes SUSY and M_R at 1 TeV.  Gravity mediation says M_SUSY = kappa M_s^2 / M_P, so here the loop is closed:
   SM from M_Z to M_S, MSSM from M_S to M_R (M_R >= M_S), left-right from M_R to M_s, with tree relation sin^2 = 3/14 at M_s and g3 = g2.
Solve for M_s from alpha_3, predict sin^2 theta_W(M_Z).  One loop, with threshold size shown by varying kappa over 0.1 to 10 and M_R.
Control: M_S = M_R = 1 TeV and MSSM below must return the paper's 9e11 GeV and 0.231.
Then, at the solved M_s:
  neutrino: m3 = c v^2 / M_s with c = 1, compare sqrt(dm31) = 0.0501 eV.
  axion: f_a = M_s / (g?) taken as M_s, with M_s/(4 pi) as the other end: m_a, Omega_a h^2 = 0.12 (f_a / 9e11)^(7/6) theta^2 (standard misalignment, order-one anharmonic neglected), and the theta needed.
  Higgs: lambda(M_S) = (g^2 + g'^2)/8 cos^2 2 beta at tree level; run the SM down at one loop in g1, g2, g3, y_t, lambda from the measured values up; find the tan beta that matches.  Failure if no real solution.
  proton: dim 6 with M_s: tau ~ M_s^4 / (alpha^2 m_p^5), in years, against 2.4e34; gauged B - L is not what forbids it.
  gravitino and moduli: m_3/2 = M_s^2/M_P; volume modulus mass m_3/2^(3/2)/M_P^(1/2) (LVS scaling); moduli problem if under 30 TeV.
  bulk radius: all six equal, r^-1 from M_P^2 = 2 M_s^8 V_6 / ((2 pi)^7 g_s^2).
  dark energy: not explained.  Reported as the failure: the vacuum energy needed compared with M_S^4.
usage: py -3 toe_one_scale.py"""
import json
import math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

MZ, AE, A3, SIN = 91.19, 1 / 127.9, 0.118, 0.2312
MP = 2.435e18
V = 174.1
HC = 1.973269804e-16  # GeV m
SM = (41 / 6, -19 / 6, -7.0)
MSSM = (11.0, 1.0, -3.0)
B1P, BL, B3 = 7.0, 3.0, -3.0


def solve(MS, MR, kappa=None):
    """given M_S and M_R, find M_s from alpha_3, and sin^2"""
    Y = 1 / AE - 14 / (3 * A3)
    t1 = (SM[0] + SM[1] - 14 / 3 * SM[2]) * math.log(MS / MZ)
    t2 = (MSSM[0] + MSSM[1] - 14 / 3 * MSSM[2]) * math.log(MR / MS)
    BB = B1P + BL - 14 / 3 * B3
    L = (2 * math.pi * Y - t1 - t2) / BB
    Ms = MR * math.exp(L)
    s = 3 / 14 * (1 + 11 * AE / (6 * math.pi) * ((SM[1] - 3 / 11 * SM[0]) * math.log(MS / MZ) + (MSSM[1] - 3 / 11 * MSSM[0]) * math.log(MR / MS) + (BL - 3 / 11 * B1P) * L))
    return Ms, s


def closed(kappa, MR_over_MS=1.0):
    f = lambda ln: math.log(solve(kappa * math.exp(2 * ln) / MP, MR_over_MS * kappa * math.exp(2 * ln) / MP)[0]) - ln
    x = brentq(f, math.log(1e8), math.log(1e17))
    Ms = math.exp(x)
    MS = kappa * Ms ** 2 / MP
    return Ms, MS, solve(MS, MR_over_MS * MS)[1]


out = {}
out["control"] = dict(Ms=solve(1000.0, 1000.0)[0], sin2=solve(1000.0, 1000.0)[1], note="the paper runs MSSM from M_Z: below uses SM to M_S")
Y0 = 1 / AE - 14 / (3 * A3)
m0 = 1000.0
Ms0 = m0 * math.exp((2 * math.pi * Y0 - 26.0 * math.log(m0 / MZ)) / (B1P + BL - 14 / 3 * B3))
out["control_paper"] = dict(Ms=Ms0, sin2=3 / 14 * (1 + 11 * AE / (6 * math.pi) * ((BL - 3 / 11 * B1P) * math.log(Ms0 / m0) + (1 - 3) * math.log(m0 / MZ))))
print("control paper", out["control_paper"], flush=True)
print("TeV SUSY with SM below", out["control"], flush=True)
rows = {}
for kappa in (0.01, 0.1, 1.0, 10.0):
    for mr in (1.0, 10.0, 100.0):
        Ms, MS, s = closed(kappa, mr)
        rows[f"k{kappa}_r{mr}"] = dict(kappa=kappa, MR_over_MS=mr, Ms=Ms, MSUSY=MS, sin2=s, pull_percent=100 * (s - SIN) / SIN)
out["closed_loop"] = rows
for k, v in rows.items():
    print(k, "Ms %.3g MSUSY %.3g sin2 %.4f (%+.1f%%)" % (v["Ms"], v["MSUSY"], v["sin2"], v["pull_percent"]), flush=True)
# What running would fix sin2 with the closed loop?  Extra doublet pairs n above M_S change B_L, B_1'.
fix = {}
for n in range(0, 7):
    for nr in range(0, 7):
        BLn, B1n = BL + n, B1P + nr
        def sol(MS):
            L = (2 * math.pi * Y0 - (SM[0] + SM[1] - 14 / 3 * SM[2]) * math.log(MS / MZ)) / (B1n + BLn - 14 / 3 * B3)
            Ms = MS * math.exp(L)
            return Ms, L
        g = lambda ln: math.log(sol(math.exp(2 * ln) / MP)[0]) - ln
        try:
            x = brentq(g, math.log(1e6), math.log(1e18))
        except ValueError:
            continue
        Ms = math.exp(x)
        MS = Ms ** 2 / MP
        L = math.log(Ms / MS)
        s = 3 / 14 * (1 + 11 * AE / (6 * math.pi) * ((SM[1] - 3 / 11 * SM[0]) * math.log(MS / MZ) + (BLn - 3 / 11 * B1n) * L))
        fix[f"dBL{n}_dB1{nr}"] = dict(dBL=n, dB1=nr, Ms=Ms, MS=MS, sin2=s)
out["extra_doublets"] = fix
best = sorted(fix.values(), key=lambda r: abs(r["sin2"] - SIN))[:6]
print("extra", [(r["dBL"], r["dB1"], "%.2g" % r["Ms"], "%.2g" % r["MS"], round(r["sin2"], 4)) for r in best], flush=True)


# Higgs: SM running from M_t, one-loop with measured couplings (Buttazzo et al at M_t = 173.1)
def rge(t, y):
    g1, g2, g3, yt, lam = y  # g1 = g' non-GUT
    k = 1 / (16 * math.pi ** 2)
    return [k * 41 / 6 * g1 ** 3, k * -19 / 6 * g2 ** 3, k * -7 * g3 ** 3, k * yt * (4.5 * yt ** 2 - 8 * g3 ** 2 - 2.25 * g2 ** 2 - 17 / 12 * g1 ** 2), k * (24 * lam ** 2 - 6 * yt ** 4 + 0.375 * (2 * g2 ** 4 + (g2 ** 2 + g1 ** 2) ** 2) + lam * (12 * yt ** 2 - 9 * g2 ** 2 - 3 * g1 ** 2))]


Y0h = [0.3587, 0.6478, 1.1666, 0.9369, 0.12604]
sol = solve_ivp(rge, (0, math.log(1e18 / 173.1)), Y0h, dense_output=True, rtol=1e-9, atol=1e-11)
out["higgs_cross_check"] = dict(lam_at_1e10=float(sol.sol(math.log(1e10 / 173.1))[4]), lam_at_1e18=float(sol.sol(math.log(1e18 / 173.1))[4]))
hg = {}
for MS in (1e3, 1e4, 1e5, 3e5, 1e6, 1e7, 1e9):
    g1, g2, g3, yt, lam = sol.sol(math.log(MS / 173.1))
    c = lam * 8 / (g1 ** 2 + g2 ** 2)
    tb = None
    if 0 <= c <= 1:
        c2b = math.sqrt(c)
        tb = math.tan(0.5 * math.acos(-c2b)) if c2b < 1 else float("inf")
    hg[f"{MS:.0e}"] = dict(lam=float(lam), cos2_2beta=float(c), tan_beta=tb)
out["higgs_matching"] = hg
print("higgs", {k: (round(v["lam"], 4), None if v["tan_beta"] is None else round(v["tan_beta"], 2)) for k, v in hg.items()}, flush=True)

# the rest at the closed solution with kappa = 1 and at the paper's scale
sec = {}
for name, Ms, MS in (("closed_k1", rows["k1.0_r1.0"]["Ms"], rows["k1.0_r1.0"]["MSUSY"]), ("paper", Ms0, 1000.0)):
    fa = {}
    for lab, f in (("Ms", Ms), ("Ms_over_4pi", Ms / (4 * math.pi))):
        om = 0.12 * (f / 9e11) ** (7 / 6)
        fa[lab] = dict(fa=f, m_a_ueV=5.7 * 1e12 / f, Omega_h2_theta1=om, theta_needed=math.sqrt(0.12 / om) if om > 0 else None)
    a = 1 / 30.0
    tau_s = Ms ** 4 / (a ** 2 * 0.938 ** 5) * 6.582e-25
    gs = 0.05
    V6 = (MP ** 2) * (2 * math.pi) ** 7 * gs ** 2 / (2 * Ms ** 8)
    r = V6 ** (1 / 6)
    m32 = Ms ** 2 / MP
    sec[name] = dict(Ms=Ms, MSUSY=MS, m_nu_eV=V ** 2 / Ms * 1e9, m_nu_over_atm=V ** 2 / Ms * 1e9 / 0.0501, axion=fa, proton_years=tau_s / 3.156e7, m32_GeV=m32, modulus_GeV=m32 ** 1.5 / MP ** 0.5, rinv_GeV=1 / r, r_m=r * HC, rho_DE_over_MSUSY4=(2.3e-12) ** 4 / MS ** 4)
out["sectors"] = sec
for k, v in sec.items():
    print(k, {a: (float("%.3g" % b) if isinstance(b, float) else b) for a, b in v.items() if a != "axion"}, {a: {c: float("%.3g" % d) for c, d in b.items()} for a, b in v["axion"].items()}, flush=True)
json.dump(out, open("toe_one_scale.json", "w"), indent=1, default=float)
