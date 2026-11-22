"""Pass 12695: follow-ups to Pass 12694, plus V_ud from neutron decay.
 (1) PQ-neutral light flavon for completion A: flavon-mediated K-Kbar mixing with couplings ~ sqrt(m_d m_s)/v_F and m_phi ~ v_F gives
     C ~ m_d m_s / v_F^4; epsilon_K bound Lambda > 1.6e5 TeV for an O(1) imaginary (d s)^2 coefficient (UTfit) -> lower bound on v_F.
 (2) Completion B at HL-LHC: single-T projections (exclusion ~1.85 TeV, CMS 2016; discovery 1.44 TeV, CMS 2022) shifted by the 3x
     cascade rate (+202 GeV, Pass 12693); soft-lepton acceptance from the muon-decay (Michel) spectrum with endpoint dM/2.
 (3) Third-family axion: E/N for third-generation-only PQ charges (quarks only; quarks + tau), g_a-gamma ~ (E/N - 1.92) vs KSVZ;
     domain-wall number of the minimal assignment.
 (4) Post-BBN photon-entropy injection window: no D photodisintegration while E_max = m_e^2/(22 T) < 2.22 MeV (T > ~5.3 keV), no
     spectral distortion for z > 2e6 (T > ~0.47 keV): window T ~ 5-30 keV; D/H pull with PRIMAT vs PArthENoPE at F = 1.048.
 (5) N_eff forecasts: if N_eff = 2.85, SO (0.05) and CMB-S4 (0.03) significance vs 3.044.
 (6) Extra: V_ud from the neutron: |V_ud|^2 tau_n (1 + 3 g_A^2) = 4908.6(1.9) s (Czarnecki-Marciano-Sirlin 2018); first-row unitarity
     with V_us from K_l3 (0.2231(6)) and K_mu2 (0.2252(5)); compare superallowed V_ud = 0.97373(31).
usage: py -3 analysis/toe_pass12695_round.py"""
import json, math, os
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
res = {}
# (1)
md, ms = 0.0047, 0.093
Lam = 1.6e5 * 1e3
vF = (md * ms * Lam ** 2) ** 0.25
res["light_flavon"] = dict(v_F_min_GeV=vF, note="flavon scale >~ 2 TeV keeps epsilon_K safe for O(1) phases; PQ-neutral so NA62 unaffected")
print(f"(1) PQ-neutral flavon: epsilon_K needs v_F >~ {vF / 1e3:.1f} TeV")
# (2)
shift = 202.0
proj = dict(exclusion_single=1850.0, discovery_single=1440.0)
reach = dict(lightest_T_exclusion=proj["exclusion_single"] + shift, lightest_T_discovery=proj["discovery_single"] + shift,
             M_VL_exclusion=proj["exclusion_single"] + shift + 44.4, M_VL_discovery=proj["discovery_single"] + shift + 44.4, current_M_VL_limit=1737.0)
xmin = 5.0 / 22.2
acc = quad(lambda x: 2 * x * x * (3 - 2 * x), xmin, 1)[0]
reach["soft_lepton_E_gt_5GeV_fraction_rest_frame"] = acc
res["hl_lhc_reach"] = reach
print(f"(2) HL-LHC: M_VL exclusion reach ~{reach['M_VL_exclusion']:.0f} GeV, discovery ~{reach['M_VL_discovery']:.0f} GeV (current limit 1737): "
      f"discovery below the present limit -> HL-LHC can only exclude B up to ~2.1 TeV; soft-lepton E > 5 GeV fraction {acc:.2f}")
# (3)
Qu, Qd, Qe = 2 / 3, -1 / 3, -1
EN = {}
EN["KSVZ (one neutral heavy quark)"] = dict(E_over_N=0.0)
for lab, (Xt, Xb, Xtau) in {"quarks only (t, b)": (1, 1, 0), "t, b, tau": (1, 1, 1)}.items():
    N = 0.5 * (Xt + Xb); E = 3 * (Qu ** 2 * Xt + Qd ** 2 * Xb) + Qe ** 2 * Xtau
    EN[lab] = dict(E_over_N=E / N, N_DW=int(round(2 * N)))
for k, v in EN.items():
    v["g_agg_relative_to_KSVZ"] = abs(v["E_over_N"] - 1.92) / 1.92
    v["integration_time_factor_vs_KSVZ"] = 1 / v["g_agg_relative_to_KSVZ"] ** 4 if v["g_agg_relative_to_KSVZ"] > 0 else float("inf")
    print(f"(3) {k}: E/N = {v['E_over_N']:.3f}, N_DW = {v.get('N_DW', 1)}, g_agg / g_KSVZ = {v['g_agg_relative_to_KSVZ']:.2f}, haloscope time x{v['integration_time_factor_vs_KSVZ']:.0f}")
res["third_family_axion"] = dict(rows=EN, note="E/N = 5/3 (quarks only) nearly cancels the 1.92 QCD term: g_agg ~ 7.7x weaker than KSVZ; N_DW = 2 needs a "
                                              "domain-wall solution (Lazarides-Shafi or tiny explicit breaking) in the post-inflationary scenario")
# (4)
me = 0.511
T_pd = me ** 2 / (22 * 2.224)
res["kev_window"] = dict(T_no_photodisintegration_keV=T_pd * 1e3, T_no_distortion_keV=0.47, T_BBN_end_keV=30)
for lab, (dh, e) in {"PRIMAT": (2.439, 0.037), "PArthENoPE": (2.51, 0.11)}.items():
    F = 1.0479; pred = dh * F ** -1.6
    res["kev_window"][f"DH_pull_{lab}"] = (2.527 - pred) / math.hypot(0.030, e * F ** -1.6)
print(f"(4) post-BBN injection window T ~ {T_pd * 1e3:.1f}-30 keV (no D photodisintegration, no spectral distortion); D/H pull with F = 1.048: "
      f"PRIMAT {res['kev_window']['DH_pull_PRIMAT']:+.1f}, PArthENoPE {res['kev_window']['DH_pull_PArthENoPE']:+.1f} sigma (explains CMB N_eff only, not helium)")
# (5)
fc = {lab: (3.044 - 2.85) / s for lab, s in (("Simons Observatory", 0.05), ("CMB-S4", 0.03))}
res["neff_forecast"] = fc
print("(5) if N_eff = 2.85: " + ", ".join(f"{k} {v:.1f} sigma" for k, v in fc.items()))
# (6)
vud = {}
for lab, tau, stau in (("bottle 877.8", 877.8, 0.3), ("beam 888.1", 888.1, 2.0)):
    gA, sgA = 1.27641, 0.00056
    v2 = 4908.6 / (tau * (1 + 3 * gA ** 2)); v = math.sqrt(v2)
    sv = 0.5 * v * math.sqrt((1.9 / 4908.6) ** 2 + (stau / tau) ** 2 + (6 * gA * sgA / (1 + 3 * gA ** 2)) ** 2)
    row = dict(V_ud=v, sigma=sv, pull_vs_superallowed=(v - 0.97373) / math.hypot(sv, 0.00031))
    for vlab, vus, svus in (("K_l3", 0.2231, 0.0006), ("K_mu2", 0.2252, 0.0005)):
        S = v * v + vus * vus + 1.5e-5
        sS = math.hypot(2 * v * sv, 2 * vus * svus)
        row[f"unitarity_{vlab}"] = dict(sum=S, deficit_sigma=(S - 1) / sS)
    vud[lab] = row
    print(f"(6) neutron ({lab}, g_A PERKEO III): V_ud = {v:.5f} +- {sv:.5f} (vs superallowed 0.97373: {row['pull_vs_superallowed']:+.1f} sigma); "
          f"unitarity K_l3 {row['unitarity_K_l3']['sum']:.5f} ({row['unitarity_K_l3']['deficit_sigma']:+.1f}), K_mu2 {row['unitarity_K_mu2']['sum']:.5f} ({row['unitarity_K_mu2']['deficit_sigma']:+.1f})")
S0 = 0.97373 ** 2 + 0.2231 ** 2 + 1.5e-5
vud["superallowed_Kl3"] = dict(sum=S0, deficit_sigma=(S0 - 1) / math.hypot(2 * 0.97373 * 0.00031, 2 * 0.2231 * 0.0006))
print(f"(6) superallowed + K_l3: {S0:.5f} ({vud['superallowed_Kl3']['deficit_sigma']:+.1f} sigma) -- the Cabibbo-angle anomaly")
res["Vud_neutron"] = vud
json.dump(res, open(os.path.join(ROOT, "data", "toe_pass12695_round.json"), "w"), indent=1)
