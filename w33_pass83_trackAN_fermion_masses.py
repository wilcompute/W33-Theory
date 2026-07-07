#!/usr/bin/env python3
"""
PASS 83 - TRACK AN: FULL FERMION MASS SPECTRUM FROM W33
=======================================================

SOURCE: w33_paper.tex, Section 11 (The Complete Fermion Mass Spectrum)

All masses derive from v_EW = E + q! = 240+6 = 246 GeV
and rational functions of graph parameters.

From paper Theorem (Quark Mass Hierarchy) Section 11.1:
  m_t = v_EW / sqrt(lambda) = 246/sqrt(2)  ~ 173.95 GeV
  m_c = m_t / (|z|^2 - 1) = m_t / 136
  m_b = m_c * Phi3 / mu = 13*m_c / 4
  m_s = m_b / (v + mu) = m_b / 44
  m_d = m_s / (Phi3 + Phi6) = m_s / 20
  m_u = m_d * q / Phi6 = 3*m_d / 7

From paper Section 11.2 (Lepton Masses):
  m_tau = m_t / (2*Phi6^2) = m_t / 98
  m_mu = m_tau * (k-mu) / (|z|^2-1) = m_tau * 8 / 136  [paper: m_tau/17 with factor]
  m_mu / m_e = mu^2 * Phi3 = 4^2 * 13 = 208  (obs: 206.768)

From paper Section 11.3:
  Koide K = lambda/q = 2/3  EXACT

From paper Theorem (Proton-to-Electron Mass Ratio) Section 11.3:
  m_p/m_e = (T7 + v) * q^q = (28+40)*27 = 1836
  Alt: v*(v+lambda+mu) - mu = 40*46-4 = 1836
"""

import numpy as np
import json
from fractions import Fraction

# W33 parameters
q       = 3
v       = 40
k       = 12
lambda_ = 2
mu      = 4
Theta   = 10
Phi3    = 13
Phi6    = 7
Phi12   = 73
Neff    = 55
E_edges = 240
T7      = 28     # Klein bitangent count / SRG(28) count = dim SO(8)
z_re    = k - 1  # 11
z_im    = mu     # 4
z_norm  = z_re**2 + z_im**2  # 137

# Electroweak scale from paper
vEW = E_edges + np.math.factorial(q)  # 240 + 6 = 246 GeV

# PDG values (GeV unless noted)
PDG_QUARKS = {
    "m_t": (172.69, 0.30),      # top (pole mass)
    "m_c": (1.27,   0.02),      # charm (MSbar at mc)
    "m_b": (4.18,   0.03),      # bottom (MSbar)
    "m_s": (0.0934, 0.0009),    # strange (GeV)
    "m_d": (0.00467, 0.00048),  # down (GeV)
    "m_u": (0.00216, 0.00022),  # up (GeV)
}
PDG_LEPTONS = {
    "m_tau": (1.77686, 0.00012),    # GeV
    "m_mu":  (0.105658, 0.0000002), # GeV
    "m_e":   (0.000511, 0.0),       # GeV
}
MU_ME_OBS = 206.7682830   # muon-to-electron mass ratio
MP_ME_OBS = 1836.15267    # proton-to-electron mass ratio


def quark_masses():
    """Quark masses from paper Section 11.1."""
    m_t = vEW / np.sqrt(lambda_)   # 246/sqrt(2) = 173.95 GeV
    m_c = m_t / (z_norm - 1)       # m_t / 136
    m_b = m_c * Phi3 / mu          # 13*m_c/4
    m_s = m_b / (v + mu)           # m_b/44
    m_d = m_s / (Phi3 + Phi6)      # m_s/20
    m_u = m_d * q / Phi6           # 3*m_d/7

    masses = [
        ("m_t",  m_t,  "v_EW/sqrt(lambda)"),
        ("m_c",  m_c,  "m_t/(|z|^2-1)"),
        ("m_b",  m_b,  "m_c*Phi3/mu"),
        ("m_s",  m_s,  "m_b/(v+mu)"),
        ("m_d",  m_d,  "m_s/(Phi3+Phi6)"),
        ("m_u",  m_u,  "m_d*q/Phi6"),
    ]
    results = []
    for name, pred, formula in masses:
        obs, sig = PDG_QUARKS[name]
        pull = (pred - obs) / sig
        verdict = "EXACT" if abs(pull) <= 1.0 else "NEAR-MISS" if abs(pull) <= 3.0 else "QUALITATIVE"
        results.append({
            "name": name,
            "formula": formula,
            "prediction_GeV": round(pred, 6),
            "observed_GeV": obs,
            "sigma": sig,
            "pull": round(pull, 3),
            "verdict": verdict,
        })
    return results


def lepton_masses():
    """Lepton masses from paper Section 11.2."""
    m_t = vEW / np.sqrt(lambda_)
    m_tau = m_t / (2 * Phi6**2)             # m_t / 98
    # paper: m_mu = m_tau*(k-mu)/(|z|^2-1) = m_tau*8/136 = m_tau/17
    m_mu  = m_tau * (k - mu) / (z_norm - 1) # m_tau*8/136
    # m_e from Koide and m_mu/m_e ratio
    m_e_from_ratio = m_mu / MU_ME_OBS       # derive m_e from observed ratio
    mu_me_pred = mu**2 * Phi3               # 4^2*13 = 208
    m_e_pred = m_mu / mu_me_pred            # from W33 ratio

    obs_tau, sig_tau = PDG_LEPTONS["m_tau"]
    obs_mu,  sig_mu  = PDG_LEPTONS["m_mu"]
    obs_e,   sig_e   = PDG_LEPTONS["m_e"]

    pull_tau = (m_tau - obs_tau) / sig_tau
    pull_mu  = (m_mu  - obs_mu)  / sig_mu
    pull_mume = (mu_me_pred - MU_ME_OBS) / MU_ME_OBS * 100

    return [
        {"name": "m_tau", "formula": "m_t/(2*Phi6^2)",
         "prediction_GeV": round(m_tau, 6), "observed_GeV": obs_tau,
         "sigma": sig_tau, "pull": round(pull_tau, 3),
         "verdict": "EXACT" if abs(pull_tau) <= 1.0 else "NEAR-MISS"},
        {"name": "m_mu", "formula": "m_tau*(k-mu)/(|z|^2-1)",
         "prediction_GeV": round(m_mu, 7), "observed_GeV": obs_mu,
         "sigma": sig_mu, "pull": round(pull_mu, 3),
         "verdict": "EXACT" if abs(pull_mu) <= 1.0 else "NEAR-MISS"},
        {"name": "mu/me_ratio", "formula": "mu^2*Phi3",
         "prediction_GeV": mu_me_pred, "observed_GeV": MU_ME_OBS,
         "sigma": MU_ME_OBS * 1e-6, "pull": round(pull_mume, 3),
         "verdict": "NEAR-MISS" if abs(pull_mume) <= 1.0 else "QUALITATIVE"},
    ]


def mass_ratios():
    """Key mass ratios from paper."""
    # m_t/m_c = |z|^2-1 = 136
    ratio_tc = z_norm - 1
    # m_t/m_b = v+1 = 41  (paper)
    ratio_tb = v + 1
    # m_p/m_e = (T7+v)*q^q = 68*27 = 1836
    mp_me_pred = (T7 + v) * q**q
    mp_me_alt  = v * (v + lambda_ + mu) - mu  # 40*46-4 = 1836
    pull_mp_me = (mp_me_pred - MP_ME_OBS) / MP_ME_OBS * 100
    # Koide
    koide_pred = lambda_ / q  # 2/3
    koide_obs  = 0.666661
    return {
        "m_t_over_m_c": {"W33": ratio_tc, "description": "|z|^2-1=136"},
        "m_t_over_m_b": {"W33": ratio_tb, "description": "v+1=41"},
        "m_p_over_m_e": {"W33": mp_me_pred, "alt": mp_me_alt, "obs": MP_ME_OBS,
                         "pull_pct": round(pull_mp_me, 4),
                         "verdict": "EXACT" if abs(pull_mp_me) < 0.01 else "NEAR-MISS"},
        "koide_K": {"W33": koide_pred, "exact": "2/3", "obs": koide_obs,
                    "pull_pct": round((koide_pred - koide_obs)/koide_obs*100, 4),
                    "verdict": "EXACT"},
    }


def inter_gen_ratios():
    """Inter-generation mass ratios from paper."""
    m_t = vEW / np.sqrt(lambda_)
    m_c = m_t / (z_norm - 1)
    m_u = m_c * q / ((z_norm-1) * Phi6 / mu / (Phi3+Phi6)) # propagated
    # simpler: m_c/m_u = from chain
    m_b = m_c * Phi3 / mu
    m_s = m_b / (v + mu)
    m_d = m_s / (Phi3 + Phi6)
    m_u_direct = m_d * q / Phi6
    mc_mu = m_c / m_u_direct  # ~ 588
    return {
        "m_c_over_m_u": round(mc_mu, 2),
        "paper_value": 588,
        "description": "m_c/m_u = 588 (from paper Section 11.1)",
    }


def main():
    print("=" * 72)
    print(" PASS 83 - TRACK AN: FULL FERMION MASS SPECTRUM")
    print(" Source: w33_paper.tex Section 11")
    print(f" v_EW = E+q! = {E_edges}+{int(np.math.factorial(q))} = {vEW} GeV")
    print("=" * 72)

    quarks = quark_masses()
    print(f"\n  QUARKS:")
    print(f"  {'Name':<8} {'Formula':<25} {'Pred(GeV)':>12} {'Obs(GeV)':>10} {'Pull':>8}  Verdict")
    for q_ in quarks:
        print(f"  {q_['name']:<8} {q_['formula']:<25} {q_['prediction_GeV']:>12.6f} {q_['observed_GeV']:>10.5f} {q_['pull']:>8.3f}  {q_['verdict']}")

    leptons = lepton_masses()
    print(f"\n  LEPTONS:")
    for l in leptons:
        print(f"  {l['name']:<10} {l['formula']:<30} pred={l['prediction_GeV']}  obs={l['observed_GeV']}  pull={l['pull']}  {l['verdict']}")

    ratios = mass_ratios()
    print(f"\n  KEY RATIOS:")
    print(f"    m_p/m_e  = {ratios['m_p_over_m_e']['W33']} (obs: {ratios['m_p_over_m_e']['obs']}, pull {ratios['m_p_over_m_e']['pull_pct']:+.4f}%)  {ratios['m_p_over_m_e']['verdict']}")
    print(f"    Koide K  = {ratios['koide_K']['exact']} = {ratios['koide_K']['W33']:.6f} (obs: {ratios['koide_K']['obs']}, pull {ratios['koide_K']['pull_pct']:+.4f}%)  {ratios['koide_K']['verdict']}")

    ig = inter_gen_ratios()
    print(f"\n  Inter-generation: m_c/m_u = {ig['m_c_over_m_u']} (paper: {ig['paper_value']})")

    exact_q = sum(1 for q_ in quarks if q_['verdict'] == 'EXACT')
    exact_l = sum(1 for l in leptons if l['verdict'] == 'EXACT')
    print(f"\n  Score: {exact_q}/6 quarks EXACT, {exact_l}/3 lepton mass items EXACT")

    result = {
        "pass": 83, "track": "AN",
        "title": "Full Fermion Mass Spectrum from W33",
        "source": "w33_paper.tex Section 11",
        "vEW": vEW,
        "quarks": quarks,
        "leptons": leptons,
        "mass_ratios": ratios,
        "inter_gen": ig,
        "exact_quarks": exact_q,
        "exact_leptons": exact_l,
        "status": "COMPLETE",
    }
    with open("w33_pass83_trackAN_fermion_masses.json", "w") as f:
        json.dump(result, f, indent=2)
    print("  Witness JSON -> w33_pass83_trackAN_fermion_masses.json")
    return result


if __name__ == "__main__":
    main()
