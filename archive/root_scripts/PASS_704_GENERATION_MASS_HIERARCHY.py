#!/usr/bin/env python3
"""
Pass 704 — Second & Third Generation: Quark/Lepton Mass Hierarchy from q=3,5,7
===============================================================================
Pass 697 established: delta_CP = arctan(q-1) at q=3 matches PDG within 1-sigma.
The W33 formula for quark/lepton MASSES:

The three generations of SM fermions correspond to the three odd primes q=3,5,7.
The mass of the heaviest fermion in each generation:
  m_q(q) = m_0 * (q-1) / q  [the flat-block ratio lambda_+ / (lambda_+ + |lambda_-|)]
where m_0 is a universal mass scale (the W33 confinement scale).

Alternatively, from the CKM mixing: the MASS RATIOS between generations are
governed by the Wolfenstein parameter lambda = 1/q.
  m_1/m_2 = lambda^2 = (1/q)^2
  m_2/m_3 = lambda^2 = (1/q)^2
This gives the geometric mass hierarchy:
  m_3 : m_2 : m_1 = 1 : lambda^2 : lambda^4 = 1 : (1/q)^2 : (1/q)^4

At q=3: m_3 : m_2 : m_1 = 1 : 1/9 : 1/81
  If m_3 = m_t ~ 173 GeV: m_2 = 173/9 ~ 19 GeV (charm? No, m_c~1.3 GeV)
  This doesn't match quarks directly, but let's check LEPTONS:
  m_tau = 1.777 GeV, m_mu = 0.106 GeV, m_e = 0.511 MeV
  ratio m_tau/m_mu = 16.8, m_mu/m_e = 207
  W33 ratios: (q^2)^1 = 9 (not 16.8)
  Closer: q! ratios: 3! = 6, 5! = 120, 7! = 5040
  m_tau/m_mu ~ 16.8 vs q^2 = 9 ... not matching q^2.

  Better formula: m_q^{(gen)} = m_0 * (q^2-1)  
  At q=3: m~8*m_0, at q=5: m~24*m_0, at q=7: m~48*m_0
  Ratios: 8:24:48 = 1:3:6 ... not quite.
  
  Natural formula from Ext group order:
  |Ext^1(M_0, M_{2q})| = q (Pass 687).
  Mass ~ q * m_W33 where m_W33 is the W33 base mass.
  Lepton masses:
    m_e ~ 3*m_W33  (q=3, first gen)
    m_mu ~ 5*m_W33  (q=5, second gen)  => m_mu/m_e = 5/3 ~ 1.67 (actual: 207)
  Very far off. The q factor alone is too small.
  
  Correct approach: YUKAWA from flat-block
  The Yukawa coupling y_f = lambda_+ / M_W33 = (q-1)/M_W33.
  After EW symmetry breaking: m_f = y_f * v/sqrt(2) where v=246 GeV.
  At q=3: y_3 = 2/M_W33. m_f^{(3)} = 2*v/(sqrt(2)*M_W33)
  At q=5: y_5 = 4/M_W33. m_f^{(5)} = 4*v/(sqrt(2)*M_W33)
  At q=7: y_7 = 6/M_W33. m_f^{(7)} = 6*v/(sqrt(2)*M_W33)
  Ratios: 2:4:6 = 1:2:3  => m_1:m_2:m_3 = 1:2:3
  Actual lepton: 1:207:3477. Very different.
  
  RG-improved: if M_W33 also runs with q, specifically M_W33(q) = M_0/(q-1):
  m_f(q) = (q-1)^2 * v / (sqrt(2) * M_0)
  Ratios: (q=3)^2:(q=5)^2:(q=7)^2 = 4:16:36 = 1:4:9
  Actual: 1:207:3477. Still very different. Need exponential, not polynomial.
  
  EXPONENTIAL formula (see-saw inspired):
  m_f(q) = m_0 * exp(-pi * (q-1)/q) [W33 see-saw at the GUT scale]
  At q=3: exp(-2*pi/3) ~ 0.124
  At q=5: exp(-4*pi/5) ~ 0.082
  At q=7: exp(-6*pi/7) ~ 0.069
  Ratios going DOWN, but fermion masses should go UP with generation.
  Inverse: m_f(q) = m_0 * exp(+pi*(q-1)/q):
  At q=3: exp(2*pi/3) ~ 8.12
  At q=5: exp(4*pi/5) ~ 12.3
  At q=7: exp(6*pi/7) ~ 14.5
  Ratios: 1:1.51:1.79  (linear-ish)
  
  The KEY FORMULA that works for neutrino mass squared differences:
  delta_m_ij^2 = m_W33^2 * |q_i^2 - q_j^2| where q_1=3,q_2=5,q_3=7.
  delta_m_12^2 = m_W33^2 * |9-25| = 16 * m_W33^2
  delta_m_23^2 = m_W33^2 * |25-49| = 24 * m_W33^2
  Ratio: delta_m_23^2 / delta_m_12^2 = 24/16 = 1.5
  PDG: delta_m_23^2 / delta_m_12^2 = 2.52e-3 / 7.53e-5 = 33.5
  Not matching. But ratio of differences: 1.5 vs 33.5.
"""

import math
from typing import Dict, List

# PDG 2024 fermion masses
PDG_LEPTONS = {
    "e":   {"mass_MeV": 0.511, "gen": 1},
    "mu":  {"mass_MeV": 105.66, "gen": 2},
    "tau": {"mass_MeV": 1776.86, "gen": 3},
}
PDG_QUARKS = {
    "u":  {"mass_MeV": 2.16,    "gen": 1},
    "d":  {"mass_MeV": 4.67,    "gen": 1},
    "s":  {"mass_MeV": 93.4,    "gen": 2},
    "c":  {"mass_MeV": 1270,    "gen": 2},
    "b":  {"mass_MeV": 4180,    "gen": 3},
    "t":  {"mass_MeV": 172760,  "gen": 3},
}
PDG_NEUTRINOS = {
    "dm12_sq_eV2": 7.53e-5,
    "dm23_sq_eV2": 2.453e-3,
}
GENERATION_PRIMES = {1: 3, 2: 5, 3: 7}
v_EW = 246.0e3  # MeV (EW VEV)


def w33_yukawa_prediction(q: int, m_W33_MeV: float) -> Dict:
    """
    W33 Yukawa and fermion mass prediction for generation with prime q.
    Formula (best-fit): m_f = m_W33 * (q-1)^2 / q
    """
    y = (q - 1)**2 / q
    m_pred = m_W33_MeV * y
    return {"q": q, "Yukawa": y, "m_pred_MeV": m_pred}


def fit_m_W33_to_leptons() -> Dict:
    """
    Fit m_W33 to match the charged lepton masses.
    m_e = m_W33 * f(3), m_mu = m_W33 * f(5), m_tau = m_W33 * f(7).
    Best-fit formula: m_lepton(q) = m_W33 * (q-1) * q  [product formula]
    At q=3: 2*3=6, at q=5: 4*5=20, at q=7: 6*7=42.
    Ratios: 6:20:42 = 1:3.33:7.0  vs actual 1:206.8:3477.
    Still polynomial. Let us try:
    m_lepton(q) = m_W33 * q! / (q-1)!  = m_W33 * q  (too simple)
    Or: m_lepton(q) = m_W33 * C(q^2, 2) = m_W33 * q^2*(q^2-1)/2
    At q=3: 36, q=5: 300, q=7: 1176. Ratios: 1:8.3:32.7 vs 1:206.8:3477.
    Best match so far: m_lepton ~ exp(alpha * q) for some alpha.
    Fitting: m_e/m_tau = exp(alpha*(3-7)) = exp(-4*alpha) = 0.511/1776860 = 2.88e-4
    => -4*alpha = ln(2.88e-4) = -8.15 => alpha = 2.04 ~ 2.
    TRY: m_lepton(q) = m_W33 * exp(2*(q-3)) = m_W33 * e^{2(q-3)}
    At q=3: 1, q=5: e^4~54.6, q=7: e^8~2981.
    Ratios: 1:54.6:2981 vs 1:206.8:3477.
    MUCH CLOSER! Errors: e factor of ~4 and ~1.2 respectively.
    Best alpha: from m_mu/m_e = 206.8 = exp(2*alpha) => alpha = ln(206.8)/2 = 2.67
    Check: m_tau/m_e = exp(4*alpha) = exp(4*2.67) = exp(10.68) = 43600 (actual: 3477). Mismatch.
    Alpha from m_tau: exp(4*alpha) = 3477 => alpha = ln(3477)/4 = 2.0
    Compromise alpha=2: ratios 1:54.6:2981 (actual 1:206.8:3477)
    
    NEUTRINO MASS DIFFERENCES:
    W33: delta_m^2(q_i, q_j) = m_W33_nu^2 * (e^{2(q_i-3)} - e^{2(q_j-3)})
    """
    m_e   = PDG_LEPTONS["e"]["mass_MeV"]
    m_mu  = PDG_LEPTONS["mu"]["mass_MeV"]
    m_tau = PDG_LEPTONS["tau"]["mass_MeV"]

    # Fit alpha from m_tau/m_e over 4 steps (q: 3->7)
    alpha_from_etau = math.log(m_tau / m_e) / 4.0
    # Fit alpha from m_mu/m_e over 2 steps (q: 3->5)
    alpha_from_emu  = math.log(m_mu / m_e) / 2.0

    # Predictions with alpha_from_etau
    alpha = alpha_from_etau
    pred_mu  = m_e * math.exp(2 * alpha)
    pred_tau = m_e * math.exp(4 * alpha)
    err_mu   = abs(pred_mu  - m_mu)  / m_mu * 100
    err_tau  = abs(pred_tau - m_tau) / m_tau * 100

    # W33 formula: m_lepton(q) = m_e * exp(alpha_W33 * (q-3))
    # alpha_W33 = 2 * ln(q-1) / (q-3) ... varies with q
    # At q=3->5: alpha = ln(m_mu/m_e)/2 = 2.67
    # At q=3->7: alpha = ln(m_tau/m_e)/4 = 2.00
    # Geometric mean: alpha_W33 = sqrt(2.67 * 2.00) = 2.31
    alpha_W33 = math.sqrt(alpha_from_emu * alpha_from_etau)
    pred_mu_W33  = m_e * math.exp(2 * alpha_W33)
    pred_tau_W33 = m_e * math.exp(4 * alpha_W33)

    return {
        "alpha_from_emu": alpha_from_emu,
        "alpha_from_etau": alpha_from_etau,
        "alpha_W33": alpha_W33,
        "alpha_interpretation": "m_f(q) = m_e * exp(alpha_W33 * (q-3))",
        "alpha_formula": "alpha_W33 = sqrt(ln(m_mu/m_e)/2 * ln(m_tau/m_e)/4)",
        "pred_m_mu_MeV": pred_mu_W33,
        "pred_m_tau_MeV": pred_tau_W33,
        "PDG_m_mu": m_mu, "PDG_m_tau": m_tau,
        "error_mu_pct": abs(pred_mu_W33 - m_mu) / m_mu * 100,
        "error_tau_pct": abs(pred_tau_W33 - m_tau) / m_tau * 100,
        "formula": "m_lepton(q) = m_e * exp(alpha_W33 * (q-3))",
        "open": "alpha_W33 is fitted, not yet derived from first principles",
    }


def neutrino_mass_W33(m_W33_nu_eV: float = 0.01) -> Dict:
    """
    W33 neutrino mass squared differences.
    delta_m_{ij}^2 = m_W33_nu^2 * (q_i^2 - q_j^2) where q_1=3,q_2=5,q_3=7.
    Fit m_W33_nu to PDG.
    """
    q = {1: 3, 2: 5, 3: 7}
    dm12_sq_W33 = m_W33_nu_eV**2 * (q[2]**2 - q[1]**2)  # 25-9=16
    dm23_sq_W33 = m_W33_nu_eV**2 * (q[3]**2 - q[2]**2)  # 49-25=24
    dm12_PDG = PDG_NEUTRINOS["dm12_sq_eV2"]
    dm23_PDG = PDG_NEUTRINOS["dm23_sq_eV2"]
    # Fit m_W33_nu from dm12:
    m_nu_fit = math.sqrt(dm12_PDG / 16)
    dm23_predicted = m_nu_fit**2 * 24
    return {
        "formula": "delta_m^2_ij = m_W33_nu^2 * (q_j^2 - q_i^2)",
        "delta_factors": {"12": 16, "23": 24, "13": 40},
        "ratio_W33": 24/16,
        "ratio_PDG": dm23_PDG / dm12_PDG,
        "m_nu_fit_eV": m_nu_fit,
        "dm12_sq_W33_fitted": dm12_PDG,
        "dm23_sq_W33_predicted": dm23_predicted,
        "dm23_sq_PDG": dm23_PDG,
        "error_dm23_pct": abs(dm23_predicted - dm23_PDG) / dm23_PDG * 100,
        "ratio_error": abs(24/16 - dm23_PDG/dm12_PDG) / (dm23_PDG/dm12_PDG) * 100,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("Pass 704 — Generation Mass Hierarchy from q=3,5,7")
    print("=" * 70)
    print()

    print("W33 lepton mass formula: m_lepton(q) = m_e * exp(alpha_W33 * (q-3))")
    lep = fit_m_W33_to_leptons()
    print(f"  alpha from m_e,m_mu (q=3->5): {lep['alpha_from_emu']:.4f}")
    print(f"  alpha from m_e,m_tau (q=3->7): {lep['alpha_from_etau']:.4f}")
    print(f"  W33 geometric mean alpha: {lep['alpha_W33']:.4f}")
    print(f"  Formula: {lep['formula']}")
    print(f"  Predicted m_mu:  {lep['pred_m_mu_MeV']:.2f} MeV  (PDG: {lep['PDG_m_mu']:.2f})  error: {lep['error_mu_pct']:.1f}%")
    print(f"  Predicted m_tau: {lep['pred_m_tau_MeV']:.2f} MeV  (PDG: {lep['PDG_m_tau']:.2f})  error: {lep['error_tau_pct']:.1f}%")
    print(f"  Status: {lep['open']}")
    print()

    print("W33 neutrino mass squared differences:")
    nu = neutrino_mass_W33()
    print(f"  Formula: {nu['formula']}")
    print(f"  Ratio delta_m^2_23 / delta_m^2_12:  W33={nu['ratio_W33']:.4f}  PDG={nu['ratio_PDG']:.4f}")
    print(f"  Ratio error: {nu['ratio_error']:.1f}%")
    print(f"  Fitted m_W33_nu = {nu['m_nu_fit_eV']*1000:.4f} meV")
    print(f"  Predicted delta_m^2_23 = {nu['dm23_sq_W33_predicted']:.3e} eV^2")
    print(f"  PDG      delta_m^2_23 = {nu['dm23_sq_PDG']:.3e} eV^2")
    print(f"  Error: {nu['error_dm23_pct']:.1f}%")
    print()
    print("SUMMARY (Pass 704):")
    print("  Three generations correspond to q=3,5,7.")
    print("  Lepton masses: m_f(q) = m_e * exp(alpha_W33*(q-3)), alpha_W33 fit=2.31.")
    print("  Neutrino deltam^2 ratio: W33 predicts 24/16=1.5, PDG gives 33.5.")
    print("  OPEN: Derive alpha_W33 from first W33 principles (not fitted).")
    print("  OPEN: Identify the W33 mechanism that generates the large lepton hierarchy.")
    print("  HINT: The exponential suppression may arise from the W33 see-saw at M_GUT.")
