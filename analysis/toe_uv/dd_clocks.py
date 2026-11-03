"""What the fitted roll implies for everything else a modulus could touch.  [N] arithmetic on published bounds; no fit.
X scales as exp(kappa_X phi): Xdot/X = kappa_X phi_N H0 today.  Bounds: Lange et al PRL 126 011102 (2021) alphadot/alpha = 1.0(1.1)e-18/yr, mudot/mu = -8(36)e-18/yr; MICROSCOPE PRL 129 121102 (2022) eta(Ti,Pt) = (-1.5 +- 2.3 +- 1.5)e-15, which constrains kappa_universal kappa_alpha Delta f with Delta f the difference of electromagnetic mass fractions (about 2.4e-3 for Ti, Pt, an estimate from Bethe-Weizsaecker).
Bulk Dirac neutrinos: m_nu ~ y v / sqrt(M_D L), so at fixed M_D and v, d ln m_nu = -(1/2) d ln L; with m_tower ~ 1/L, d ln m_nu = (1/2) d ln m_tower.  Control of scale: what c' Delta phi would move sum m_nu by the 0.02 eV a cosmological fit can resolve, against the value fitted.
Dark dimension radius and Lambda: R changes by the same d ln m_tower.  usage: py -3 dd_clocks.py"""
import json
import math

out = {}
H0YR = 67.5 / 3.0857e19 * 3.156e7
out["H0_per_yr"] = H0YR
for ds in ("pantheon", "dovekie", "desy5"):
    d = json.load(open(f"fading_ds_{ds}.json"))
    row = {}
    for br in ("free_c_neg", "free_c_pos"):
        f = d[br]
        info = f["info"]
        phiN = abs(info["phip0"])
        rate = phiN * H0YR
        ka = (abs(1.0e-18) + 2 * 1.1e-18) / rate
        kmu = (8e-18 + 2 * 36e-18) / rate
        dlnm = info["dln_mDM_rec_to_0"]
        row[br] = dict(c=f["c"], cp=f["cp"], phi_N_today=phiN, kappa_alpha_max=ka, kappa_mu_max=kmu, dln_tower_rec_to_0=dlnm, dln_mnu_rec_to_0=dlnm / 2, dln_R_rec_to_0=-dlnm, dln_Lambda_if_mKK4=4 * dlnm)
    out[ds] = row
eta = math.sqrt(2.3e-15 ** 2 + 1.5e-15 ** 2)
eta2 = 1.5e-15 + 2 * eta
out["microscope"] = dict(eta_2sigma=eta2, delta_f=2.4e-3, product_bound=eta2 / (2 * 2.4e-3), geometric_mean=math.sqrt(eta2 / (2 * 2.4e-3)), kappa_alpha_at_beta_cassini=eta2 / (2 * 2.4e-3) / 0.004)
# neutrinos: scale control
sm = 0.06
out["neutrino_scale"] = dict(resolution_eV=0.02, needed_abs_dln=math.log(1 + 0.02 / sm), needed_dln_tower=2 * math.log(1 + 0.02 / sm), fitted_dln_tower=max(abs(v["dln_tower_rec_to_0"]) for ds in ("pantheon", "dovekie", "desy5") for v in out[ds].values()))
out["neutrino_scale"]["shortfall_factor"] = out["neutrino_scale"]["needed_dln_tower"] / out["neutrino_scale"]["fitted_dln_tower"]
json.dump(out, open("dd_clocks.json", "w"), indent=1)
print(json.dumps(out, indent=1))
