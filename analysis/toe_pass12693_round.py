"""Pass 12693: five follow-ups to Pass 12692.
 (1) Low-N_eff mechanisms vs light elements.  (a) Photon-entropy injection after neutrino decoupling and after BBN: N_eff = 3.044 F^(-4/3)
     needs F = (3.044/N_eff)^(3/4); eta_BBN = F eta_CMB and D/H ~ eta^-1.6 (PRIMAT D/H = 2.439(37)e-5 at Planck eta; Cooke+2018
     2.527(30)e-5).  (b) Low reheating: raises Y_p and is bounded T_RH > 5.96 MeV, N_eff > 2.98 (2501.01369): cannot give low N_eff AND low Y_p.
     (c) Electron-neutrino asymmetry xi_e: lowers Y_p (dY_p/dxi_e ~ -0.2, approximate) with negligible N_eff change: explains helium only.
 (2) Completion B triplet: the B and T' pairs cascade to the lightest T (soft W*), so standard pair searches see ~3x the single-T rate:
     shift of the 1.49 TeV single-T limit using the computed sigma(M) slope (Pass 12692); long-lived regime of the lightest T.
 (3) Aligned Froggatt-Nielsen charges for completion A's flavour-from-PQ sector: C_sd ~ (1/2)|dX_Q eps^dX_Q + dX_d eps^dX_d|,
     V_us ~ eps^dX_Q, m_d/m_s ~ eps^(dX_Q + dX_d), eps = 0.22 (N_DW = 1 normalisation, O(1) coefficients).
 (4) Proton fraction needed for the KM3NeT flux if cosmogenic: E^2 Phi(200 PeV, per flavour) ~ f_p x [1e-9 (no evolution) .. 1e-8 (strong)].
 (5) EMPRESS consistency: chi^2 and Birge ratio of the four Y_p, EMPRESS vs the other three, N_eff with Birge-inflated errors.
usage: py -3 analysis/toe_pass12693_round.py"""
import json, math, os
import numpy as np
from scipy.stats import chi2 as chi2d

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
res = {}
# (1a)
DH_STD, DH_STD_E, DH_OBS, DH_OBS_E = 2.439e-5, 0.037e-5, 2.527e-5, 0.030e-5
ent = {}
for neff in (2.86, 2.83, 2.95):
    F = (3.044 / neff) ** 0.75; dh = DH_STD * F ** -1.6
    ent[str(neff)] = dict(F=F, DH_pred=dh, pull=(DH_OBS - dh) / math.hypot(DH_OBS_E, DH_STD_E * F ** -1.6))
    print(f"(1a) N_eff = {neff}: photon-entropy factor F = {F:.4f}; post-BBN injection -> D/H = {dh:.3e}, pull vs Cooke {ent[str(neff)]['pull']:+.1f} sigma (standard: {(DH_OBS - DH_STD) / math.hypot(DH_OBS_E, DH_STD_E):+.1f})")
xi = (0.2439 - 0.2467) / -0.2
dneff_xi = 3 * 15 / 7 * (2 * (xi / math.pi) ** 2 + (xi / math.pi) ** 4) / 3     # e-flavour only
res["low_neff"] = dict(post_BBN_entropy=ent, low_reheating="2501.01369: low T_RH raises Y_p; T_RH > 5.96 MeV, N_eff > 2.98 (BBN+Planck+lensing+DESI): cannot produce low Y_p and N_eff ~ 2.85 together",
                       lepton_asymmetry=dict(xi_e_for_helium=xi, dNeff=dneff_xi, note="explains helium only; CMB N_eff = 2.86 stays -1.4 sigma"))
print(f"(1b) low reheating: raises Y_p, T_RH > 5.96 MeV -> excluded as joint explanation")
print(f"(1c) lepton asymmetry: xi_e ~ {xi:.3f} lowers Y_p to the helium mean; Delta N_eff = {dneff_xi:.1e} (CMB deficit unexplained)")
# (2)
s1600, s1700 = 1.58, 0.918          # fb, 13.6 TeV, K-scaled (Pass 12692)
slope = math.log(s1600 / s1700) / 100.0
dm = math.log(3.0) / slope
lim_single = 1490.0
lightest_lim = lim_single + dm
MVL_lim = lightest_lim + 44.4
v = 246.22
th_ll = math.sqrt(1.97327e-16 / 1e-3 * 16 * math.pi * v ** 2 / 1700.0 ** 3)     # c tau = 1 mm
res["vlq_effective_limit"] = dict(sigma_slope_per_GeV=slope, mass_shift_for_3x_rate=dm, lightest_T_limit=lightest_lim, M_VL_limit=MVL_lim,
                                  theta_long_lived_1mm=th_ll, note="prompt regime theta > ~1e-7: standard searches with 3x rate; theta < theta_ll: displaced / R-hadron searches")
print(f"(2) 3x rate shifts the single-T limit by {dm:.0f} GeV: lightest T > {lightest_lim:.0f} GeV -> M_VL > {MVL_lim:.0f} GeV; lightest T long-lived (c tau > 1 mm) for mixing < {th_ll:.1e}")
# (3)
eps = 0.22
fn = []
for dq in (0, 1, 2):
    for dd in (0, 1, 2):
        C = 0.5 * abs(dq * eps ** dq + dd * eps ** dd)
        vus, mdms = eps ** dq, eps ** (dq + dd)
        ok_flav = (0.225 / 3 <= vus <= 0.225 * 3) and (0.05 / 3 <= mdms <= 0.05 * 3)
        fn.append(dict(dX_Q=dq, dX_d=dd, C_sd=C, V_us=vus, md_over_ms=mdms, flavour_ok_within_3=ok_flav, NA62_ok=C < 0.091))
        print(f"(3) dX_Q={dq} dX_d={dd}: C_sd ~ {C:.3f} (NA62 {'ok' if C < 0.091 else 'X'}), V_us ~ {vus:.3f}, m_d/m_s ~ {mdms:.3f} (flavour {'ok' if ok_flav else 'X'})")
both = [r for r in fn if r["flavour_ok_within_3"] and r["NA62_ok"]]
res["aligned_FN"] = dict(rows=fn, both_ok=both)
print(f"(3) charge assignments passing both flavour (within x3) and NA62: {[(r['dX_Q'], r['dX_d']) for r in both]}")
# (4)
fp = {}
for lab, flux in (("joint fit 7.5e-10", 7.5e-10), ("KM3NeT-only 5.8e-8", 5.8e-8)):
    fp[lab] = dict(f_p_strong_evolution=flux / 1e-8, f_p_no_evolution=flux / 1e-9)
    print(f"(4) {lab}: proton fraction needed {flux / 1e-8:.2g} (strong evolution) - {flux / 1e-9:.2g} (no evolution)")
res["proton_fraction"] = dict(rows=fp, note="f_p > 1 impossible: the KM3NeT-only flux cannot be cosmogenic; the joint flux needs f_p ~ 0.08 with strong evolution (Auger allows ~0.1)")
# (5)
obs = {"Aver+2021": (0.2453, 0.0034), "Hsyu+2020": (0.2436, 0.0040), "Kurichin+2021": (0.2462, 0.0022), "EMPRESS 2022": (0.2370, 0.0034)}
y = np.array([o for o, _ in obs.values()]); s = np.array([e for _, e in obs.values()]); w = 1 / s ** 2
m = (w * y).sum() / w.sum(); chi = float((((y - m) / s) ** 2).sum()); birge = math.sqrt(chi / 3)
others = [k for k in obs if k != "EMPRESS 2022"]; wo = np.array([1 / obs[k][1] ** 2 for k in others]); yo = np.array([obs[k][0] for k in others])
mo, so = (wo * yo).sum() / wo.sum(), 1 / math.sqrt(wo.sum())
pull_emp = (0.2370 - mo) / math.hypot(0.0034, so)
sig_infl = birge / math.sqrt(w.sum())
neff_infl = 3.044 + (m - 0.2467) / 0.013
res["empress"] = dict(chi2=chi, dof=3, p=float(chi2d.sf(chi, 3)), birge=birge, EMPRESS_vs_others_pull=pull_emp,
                      Yp_mean=float(m), Yp_sigma_inflated=sig_infl, Neff=neff_infl, Neff_sigma_inflated=sig_infl / 0.013)
print(f"(5) four Y_p: chi2 = {chi:.2f}/3 (p = {chi2d.sf(chi, 3):.3f}), Birge {birge:.2f}; EMPRESS vs others {pull_emp:+.2f} sigma; "
      f"with Birge-inflated errors N_eff = {neff_infl:.2f} +- {sig_infl / 0.013:.2f}")
comb = (2.86 / 0.13 ** 2 + neff_infl / (sig_infl / 0.013) ** 2) / (1 / 0.13 ** 2 + 1 / (sig_infl / 0.013) ** 2)
comb_s = 1 / math.sqrt(1 / 0.13 ** 2 + 1 / (sig_infl / 0.013) ** 2)
res["empress"]["combined_with_ACT"] = dict(Neff=comb, sigma=comb_s, pull_vs_SM=(comb - 3.044) / comb_s)
print(f"(5) ACT + helium (inflated): N_eff = {comb:.2f} +- {comb_s:.2f} ({(comb - 3.044) / comb_s:+.1f} sigma vs 3.044)")
json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12693_round.json"), "w"), indent=1)
