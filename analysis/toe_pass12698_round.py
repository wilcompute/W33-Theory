"""Pass 12698: Bayesian evidence with explanatory credit, the MeV ALP, long-lived triplet limits, Delta_R^V vs the Cabibbo gap.
 (1) Evidence (Laplace-free numerical integrals over explicit priors) for SM + LCDM + generic DM, the sqrt(v M_Pl) boundary, completion A
     and completion B, with likelihoods m_t N(172.57, 0.43), n_s N(0.9743, 0.0034) [and P-ACT 0.9709(38)], Omega_DM h^2 N(0.120, 0.0012).
     SM: m_t ~ U(165, 180), n_s ~ U(0.94, 1.00), Omega ~ U(0, 0.3).
     A: log f_a ~ U(9, 13); m_t(f_a) from lambda(f_a) = 0 (log10 mu0 = log10 5.41e10 - 1.56 (m_t - 172.57), theory 0.1 GeV);
        Omega(f_a) = 0.12 (f_a / 1.04e11)^1.17 with 30 % lognormal theory spread (post-inflation axion);
        n_s = 0.9653 + 0.22 b, log10 b ~ U(-3, -1); thermal-leptogenesis credit needs xi >= 10: prior fraction 0.5 of log xi ~ U(-1, 3).
     B: y' ~ U(0, 1) with m_t(y') linearised from two runs (R = 1 um, M_VL = 1.65 TeV); n_s ~ U(0.94, 1.00) (inflation unspecified);
        Omega = 0.12 (T_i / T_*)^3 with ln T_i ~ U(ln 0.1, ln 10) GeV (graviton DM, Omega ~ T_i^3).
 (2) MeV photophilic ALP for the keV window: freeze-in yield estimate from Primakoff production at T ~ m (order of magnitude).
 (3) Long-lived lightest T (mixing < 1e-8): R-hadron limits for a fermionic triplet from a stop-like limit (~1.34 TeV), the
     fermion/scalar cross-section ratio (~7 at 1.5 TeV, assumed) and the 3x triplet rate, using the computed sigma(M) slope.
 (4) Delta_R^V: lattice 0.02439(18) (Ma et al. PRL 2024) gives V_ud(0+) = 0.97386(30); remaining gap to the neutron 0.97456(44) and the
     Delta_R^V shift that would close it.
usage: py -3 analysis/toe_pass12698_round.py"""
import json, math, os
import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
res = {}
G = {"__name__": "x", "__file__": os.path.join(HERE, "toe_pass12685_intermediate_scale_suite.py")}
exec(open(os.path.join(HERE, "toe_pass12685_intermediate_scale_suite.py"), encoding="utf-8").read().split("res = {}")[0], G)
mu0, MPL = G["mu0"], G["MPL"]
GEV_INV_M = 1.97327e-16
M5 = (MPL ** 2 / (2 * math.pi * 1e-6 / GEV_INV_M)) ** (1 / 3)
yp = {}
for mt in (172.07, 172.57, 173.07):
    yp[mt] = brentq(lambda y: math.log(mu0(mt, vl=(1650.0, y))) - math.log(M5), 0.05, 1.5, xtol=1e-5)
dy_dmt = (yp[173.07] - yp[172.07]) / 1.0
print(f"(1) completion B: y'(m_t) = {yp[172.07]:.3f}, {yp[172.57]:.3f}, {yp[173.07]:.3f} at m_t = 172.07/172.57/173.07 -> dy'/dm_t = {dy_dmt:.4f} per GeV")
def N(x, m, s): return math.exp(-0.5 * ((x - m) / s) ** 2) / (s * math.sqrt(2 * math.pi))
MT, SMT = 172.57, 0.43
OM, SOM = 0.120, 0.0012
def evidences(ns_obs, ns_sig):
    Z = {}
    Lmt_free = 1 / 15.0                      # integral of N over m_t prior U(165,180)
    Lns_free = 1 / 0.06
    Lom_free = 1 / 0.3
    Z["SM + LCDM + generic DM"] = Lmt_free * Lns_free * Lom_free
    Z["boundary sqrt(v M_Pl) + generic DM"] = N(172.57, MT, math.hypot(SMT, 0.1)) * Lns_free * Lom_free
    # A
    lf = np.linspace(9, 13, 4001); dlf = lf[1] - lf[0]
    mt_pred = 172.57 + (math.log10(5.41e10) - lf) / 1.56
    om_pred = 0.12 * (10 ** lf / 1.04e11) ** 1.17
    Lmt = np.exp(-0.5 * ((mt_pred - MT) / math.hypot(SMT, 0.1)) ** 2) / (math.hypot(SMT, 0.1) * math.sqrt(2 * math.pi))
    sl = 0.30   # lognormal theory spread on Omega prediction
    Lom = np.exp(-0.5 * (np.log(OM / om_pred) / math.hypot(sl, SOM / OM)) ** 2) / (OM * math.hypot(sl, SOM / OM) * math.sqrt(2 * math.pi))
    IA = float((Lmt * Lom).sum() * dlf / 4.0)
    lb = np.linspace(-3, -1, 2001); dlb = lb[1] - lb[0]
    ns_pred = 0.9653 + 0.22 * 10 ** lb
    Lns = np.exp(-0.5 * ((ns_pred - ns_obs) / ns_sig) ** 2) / (ns_sig * math.sqrt(2 * math.pi))
    IB = float(Lns.sum() * dlb / 2.0)
    Z["completion A"] = IA * IB * 0.5
    # B
    Lmt_B = 1.0 / abs(dy_dmt) * 1.0 if 0 < yp[172.57] < 1 else 0.0     # integral over y' ~ U(0,1) of N(m_t(y')) = |dm_t/dy'| ... per unit y'
    Lmt_B = abs(1 / dy_dmt) ** -1 if False else abs(dy_dmt)               # = 1/|dm_t/dy'| (density of m_t per unit prior)
    lt = np.linspace(math.log(0.1), math.log(10), 4001); dlt = lt[1] - lt[0]
    om_B = 0.12 * np.exp(3 * lt)
    Lom_B = np.exp(-0.5 * ((om_B - OM) / SOM) ** 2) / (SOM * math.sqrt(2 * math.pi))
    Z["completion B"] = Lmt_B * Lns_free * float(Lom_B.sum() * dlt / (math.log(10) - math.log(0.1)))
    base = Z["SM + LCDM + generic DM"]
    return {k: dict(Z=v, bayes_factor_vs_SM=v / base) for k, v in Z.items()}
ev = {"P-ACT-LB n_s": evidences(0.9743, 0.0034), "P-ACT n_s (no DESI)": evidences(0.9709, 0.0038)}
for lab, d in ev.items():
    print(f"(1) {lab}: " + "; ".join(f"{k} B = {v['bayes_factor_vs_SM']:.2f}" for k, v in d.items()))
res["evidence"] = dict(dy_dmt=dy_dmt, yprime=yp, rows=ev, note="priors and likelihoods in the docstring; N_eff likelihood common to all (3.044) and omitted")
# (2) MeV ALP freeze-in (order of magnitude)
alpha = 1 / 137.0
alp = {}
for m, g in ((1e-3, 3.2e-9), (2e-3, 1.1e-9), (4e-3, 4.0e-10)):
    T = m; H = 1.66 * math.sqrt(10.75) * T * T / 1.22e19
    Gam = alpha * g * g * T ** 3 / 8          # Primakoff rate per ALP-photon, rough
    Y = (Gam / H) * 0.0278                    # n_eq/s for one boson ~ 0.0278 g*_s^-1 scaling folded in
    zeta = m * Y * 7.04
    alp[f"m={m * 1e3:.0f} MeV"] = dict(g=g, Gamma_over_H=Gam / H, Y=Y, zeta_GeV=zeta, needed_zeta=1.7e-6, shortfall=1.7e-6 / zeta)
    print(f"(2) ALP m = {m * 1e3:.0f} MeV, g = {g:.1e}: Gamma/H at T~m = {Gam / H:.1e}, freeze-in zeta ~ {zeta:.1e} GeV (needed ~1.7e-6; shortfall x{1.7e-6 / zeta:.0e})")
res["mev_alp"] = dict(rows=alp, note="freeze-in falls far short; needs non-thermal production; SN1987A bounds near g ~ 1e-9 are uncertain by factors of a few")
# (3) R-hadron limit estimate
slope = math.log(1.58 / 0.918) / 100.0
stop_lim = 1340.0
shift = math.log(7.0 * 3.0) / slope
res["long_lived_triplet"] = dict(stop_like_limit=stop_lim, fermion_over_scalar=7.0, triplet_factor=3.0, mass_shift=shift, lightest_T_limit=stop_lim + shift,
                                 note="estimate: fermion/scalar cross-section ratio ~7 assumed; R-hadron searches would exclude the long-lived regime to ~1.9 TeV")
print(f"(3) long-lived lightest T (mixing < 1e-8): stop-like R-hadron limit {stop_lim:.0f} + {shift:.0f} GeV -> ~{stop_lim + shift:.0f} GeV")
# (4)
v0, s0, vn, sn = 0.97386, 0.00030, 0.97456, 0.00044
rel = (v0 / vn) ** 2 - 1
dR = -rel * (1 + 0.02439)            # V^2 ~ 1/(1 + Delta_R^V)
res["delta_RV"] = dict(V_ud_lattice=v0, gap_sigma=(vn - v0) / math.hypot(s0, sn), Delta_RV_shift_needed=-dR, lattice_unc=0.00018,
                       shift_over_unc=dR / 0.00018)
print(f"(4) lattice Delta_R^V: V_ud(0+) = {v0} -> gap to neutron {(vn - v0) / math.hypot(s0, sn):.1f} sigma; closing it needs Delta_R^V lower by {dR:.5f} "
      f"= {dR / 0.00018:.0f}x the lattice uncertainty")
json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12698_round.json"), "w"), indent=1, default=float)
# ---------------- (1b) prior sensitivity and look-elsewhere for the post-hoc boundary choice
sens = {}
for width in (15.0, 5.0, 2.0):
    scale = 15.0 / width          # SM's m_t integral 1/width instead of 1/15: SM evidence x scale
    row = {k: v["bayes_factor_vs_SM"] / scale for k, v in ev["P-ACT-LB n_s"].items()}
    row["boundary, trials-corrected (8 candidate scales)"] = row["boundary sqrt(v M_Pl) + generic DM"] / 8
    row["completion A, trials-corrected (8)"] = row["completion A"] / 8
    sens[f"SM m_t prior width {width:g} GeV"] = row
    print(f"(1b) SM m_t prior width {width:g} GeV: " + "; ".join(f"{k} {v:.2f}" for k, v in row.items() if k != "SM + LCDM + generic DM"))
res["evidence"]["prior_sensitivity"] = sens
json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12698_round.json"), "w"), indent=1, default=float)
