"""Pass 12722 (Claude track), items 1, 2, 4, 5 (item 3: explore_pass12722_charlm64.py).
 (1) The seesaw operator (y/M) 16 16 Hbar Hbar gives M_R = y <Hbar>^2 / M and, for one Hbar fluctuation along the pseudo-Goldstone triplet,
     a triplet-matter coupling g ~ sqrt2 M_R / <Hbar> into both QQ and QL channels (126 contraction).  No symmetry can remove it without
     removing neutrino masses.  Proton stability (Pass 12721: |g_QQ g_QL| <= 1.7e-25 at M_T = 1.74 TeV) caps M_R1 (first-generation entries);
     with the minimal SO(10) Dirac relation m_D = m_u (GUT scale), m_1 >= m_u^2 / M_R1,max; sum of masses vs DESI DR2 + CMB (< 0.064 eV, 95%;
     0.070 with Pantheon+).
 (2) The light d-type triplet as a vectorlike B quark: pair limits 1.45-1.52 TeV (CMS 2024 PRD; ATLAS/CMS recast 2412.01761); with the
     doublet's B, two B-like states double the rate: shift ~ ln 2 x 184 GeV (sigma(M) slope of Pass 12693).
 (4) y' of the hybrid with the light 5 + 5bar fermions (Dirac (3,1)_1/3 and (1,2)_1/2 at 1.74 TeV): Delta b_Y = 10/9, Delta b_2 = 2/3,
     Delta b_3 = 2/3 (SM normalisation) added above 1.74 TeV; lambda(M_SS = 8.45e9) = 0.
 (5) Thawing quintessence vs DESI DR2 + CMB + Pantheon+ (w0 = -0.857 +- 0.057, wa = -0.55 +- 0.235, correlation assumed -0.9): the thawing
     relation wa ~ -1.58 (1 + w0) (Dutta-Scherrer-type CPL mapping); best-fit point and Delta chi^2 vs the CPL best fit and vs LambdaCDM.
usage: py -3 analysis/explore_pass12722_round.py"""
import json, math, os
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
res = {}

# ======================================================================= (1)
gmax = math.sqrt(1.7e-25)
nu = []
dm21, dm31 = 7.4e-5, 2.51e-3
for vH in (1e16, 4e16):
    MR1 = gmax * vH / math.sqrt(2)
    for mu_gut in (4e-4, 7e-4):
        m1 = mu_gut ** 2 / MR1 * 1e9                              # eV
        s_no = m1 + math.sqrt(m1 ** 2 + dm21) + math.sqrt(m1 ** 2 + dm31)
        nu.append(dict(vHbar=vH, MR1_max=MR1, m_u_GUT=mu_gut, m1_min_eV=m1, sum_NO_eV=s_no, excluded_064=s_no > 0.064, excluded_070=s_no > 0.070))
        print(f"(1) <Hbar> = {vH:.0e}, m_u(GUT) = {mu_gut * 1e3:.1f} MeV: M_R1 <= {MR1:.1e} GeV -> m_1 >= {m1:.3f} eV, sum m_nu (NO) >= {s_no:.3f} eV "
              f"({'excluded' if s_no > 0.064 else 'allowed'} by DESI+CMB < 0.064; {'excluded' if s_no > 0.070 else 'allowed'} by < 0.070)")
res["seesaw_triplets"] = dict(rows=nu, g_max=gmax,
                              note="minimal SO(10) relation m_D = m_u and a flavour-diagonal M_R; 126-type Dirac contributions or a small (M_R)_11 with "
                                   "large mixing can evade the floor")

# ======================================================================= (2)
shift = math.log(2) * 184.0
res["vlb"] = dict(limit_range=[1450, 1520], two_B_shift=shift, effective=[1450 + shift, 1520 + shift],
                  verdict="the light d-type triplet at 1.74 TeV is allowed (effective B limit ~1.58-1.65 TeV); HL-LHC reaches it")
print(f"(2) VLB pair limits 1.45-1.52 TeV; with two B-like states (doublet B + triplet D) ~ +{shift:.0f} GeV -> {1450 + shift:.0f}-{1520 + shift:.0f} GeV < 1740: allowed")

# ======================================================================= (4)
src03 = open(os.path.join(HERE, "toe_pass12703_round.py"), encoding="utf-8").read()
G = {"__file__": os.path.join(HERE, "toe_pass12703_round.py")}
exec(src03.split("# ======================================================================= (4)")[0], G)
initial, beta_sm, beta_vl, OFF3 = (G[k] for k in ("initial", "beta_sm", "beta_vl", "OFF3"))
K = 1 / (16 * math.pi ** 2)
dl_ = lambda y: (5 / 6) * 3 * K * y[5] ** 4 - 2 * y[4] * 3 * K * y[5] ** 2 / 3


def lam_end(yp, tgt, Mt, extra, mvl=1740.0):
    Mt0 = Mt - OFF3; kw = dict(rtol=1e-9, atol=1e-12, max_step=0.5)
    y = solve_ivp(lambda t, y: beta_sm(*y[:5]) + [0.0], (0, math.log(mvl / Mt0)), np.array(initial(Mt, 125.20, 0.1180) + [yp]), **kw).y[:, -1].copy()
    y[4] += dl_(y)
    def rhs(t, y):
        d = list(beta_vl(*y))
        if extra: d[0] += K * y[0] ** 3 * 10 / 9; d[1] += K * y[1] ** 3 * 2 / 3; d[2] += K * y[2] ** 3 * 2 / 3
        return d
    return solve_ivp(rhs, (math.log(mvl / Mt0), math.log(tgt / Mt0)), y, **kw).y[:, -1][4]


yy = {}
for Mt in (172.57, 172.80):
    for extra in (False, True):
        yy[f"Mt={Mt}|5+5bar={extra}"] = brentq(lambda p: lam_end(p, 8.45e9, Mt, extra), 0.2, 1.0, xtol=1e-6)
    print(f"(4) M_t = {Mt}: hybrid y' = {yy[f'Mt={Mt}|5+5bar=False']:.4f} (Q + U) -> {yy[f'Mt={Mt}|5+5bar=True']:.4f} (with the light 5 + 5bar fermions)")
res["y_with_5"] = yy

# ======================================================================= (5)
w0c, s0, wac, sa, rho = -0.857, 0.057, -0.55, 0.235, -0.9
Cinv = np.linalg.inv(np.array([[s0 ** 2, rho * s0 * sa], [rho * s0 * sa, sa ** 2]]))
chi2 = lambda w0, wa: float(np.array([w0 - w0c, wa - wac]) @ Cinv @ np.array([w0 - w0c, wa - wac]))
r = minimize_scalar(lambda w0: chi2(w0, -1.58 * (1 + w0)), bounds=(-1.0, -0.5), method="bounded")
th = dict(w0=r.x, wa=-1.58 * (1 + r.x), chi2=r.fun, chi2_LCDM=chi2(-1, 0))
print(f"(5) thawing quintessence (wa = -1.58(1+w0)): best w0 = {r.x:.3f}, wa = {th['wa']:.3f}, chi2 = {r.fun:.2f} vs CPL best fit 0 and LambdaCDM {th['chi2_LCDM']:.2f} "
      f"(1 dof less than CPL: thawing improves on LambdaCDM by Delta chi2 = {th['chi2_LCDM'] - r.fun:.2f})")
res["thawing"] = dict(desi=dict(w0=w0c, s0=s0, wa=wac, sa=sa, rho_assumed=rho), best=th,
                      note="an uncoupled thawing field evades lunar ranging (no G variation); it captures part of the DESI preference")
json.dump(res, open(os.path.join(ROOT, "data", "explore_pass12722_round.json"), "w"), indent=1, default=float)
print("wrote data/explore_pass12722_round.json")
