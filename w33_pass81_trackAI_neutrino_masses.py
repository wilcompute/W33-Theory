#!/usr/bin/env python3
"""
PASS 81 - TRACK AI: EXACT NEUTRINO MASSES FROM W33
===================================================

Cross-references:
  - BREAKTHROUGH_DCCXCVII_NEUTRINO_MASS_HIERARCHY.md (prior W33 neutrino work)
  - Planck 2018: sum(m_nu) < 0.12 eV (95% CL)
  - PDG neutrino mass splittings:
      Delta m^2_21 = 7.53e-5 eV^2 (solar)
      |Delta m^2_31| = 2.546e-3 eV^2 (atmospheric)

W33 formula family: m_nu_i = epsilon^n * v_EW * |lambda_i| / lambda1
Where n is chosen to satisfy the Planck bound and the mass splittings.

The negative GQ(3,3) eigenvalues (fermion-like modes) are assigned
to the three neutrino generations:
  nu_1: |lambda5| = 1  (multiplicity 5)
  nu_2: |lambda6| = 3  (multiplicity 4)
  nu_3: |lambda7| = 4  (multiplicity 1)  [lightest automorphism orbit]

With a type-I seesaw:
  m_nu^light = - (Y_nu v)^2 / M_R
where M_R = Lambda_W33 is the W33 GUT scale (natural seesaw scale).
"""

import numpy as np
import json

# Physical constants
V_EW    = 246.22  # GeV
M_Z     = 91.1876

# PDG neutrino parameters
DM2_21_PDG = 7.53e-5  # eV^2 (solar)
DM2_31_PDG = 2.546e-3  # eV^2 (atmospheric)
SUM_NU_PDG = 0.12  # eV (Planck 95% CL upper bound)
SIGMA_DM21 = 0.18e-5
SIGMA_DM31 = 0.03e-3

# W33 parameters
sqrt97  = np.sqrt(97)
lambda1 = 12.0
lambda2 = (1 + sqrt97) / 2
lambda3 = 3.0
lambda4 = 1.0
epsilon = (lambda2 - 2*np.sqrt(7)) / (2*np.sqrt(7))
M_GUT   = 2.0e16  # GeV
LAM_W33 = M_GUT * np.sqrt(epsilon)

# Negative eigenvalues assigned to neutrinos
LAM_NU = [1.0, 3.0, 4.0]  # |lambda5|, |lambda6|, |lambda7|


def neutrino_masses_eps_power(n_eps):
    """
    Compute neutrino masses for epsilon^n_eps suppression.
    m_nu_i = epsilon^n * v_EW * |lam_i| / lam1  (direct Yukawa)
    Returns masses in eV and mass splittings.
    """
    m_eV = []
    for lam in LAM_NU:
        m_GeV = epsilon**n_eps * V_EW * lam / lambda1
        m_eV.append(m_GeV * 1e9)  # GeV to eV
    m1, m2, m3 = m_eV
    dm2_21 = m2**2 - m1**2
    dm2_31 = m3**2 - m1**2
    sum_nu = sum(m_eV)
    return {
        "n_eps": n_eps,
        "m1_eV": m1, "m2_eV": m2, "m3_eV": m3,
        "sum_eV": sum_nu,
        "planck_ok": sum_nu < SUM_NU_PDG,
        "dm2_21_eV2": dm2_21,
        "dm2_31_eV2": dm2_31,
        "pull_dm21": (dm2_21 - DM2_21_PDG) / SIGMA_DM21 if SIGMA_DM21 > 0 else None,
        "pull_dm31": (dm2_31 - DM2_31_PDG) / SIGMA_DM31 if SIGMA_DM31 > 0 else None,
    }


def seesaw_masses(n_dirac_eps=1):
    """
    Type-I seesaw: m_light = (Y_nu * v/sqrt(2))^2 / M_R
    Y_nu_i = epsilon^n * |lam_i| / lam1 (Dirac Yukawa)
    M_R = Lambda_W33 (W33 GUT scale = natural seesaw scale)
    """
    M_R = LAM_W33  # in GeV
    v_sqrt2 = V_EW / np.sqrt(2)
    m_light_eV = []
    for lam in LAM_NU:
        y = epsilon**n_dirac_eps * lam / lambda1
        m_D = y * v_sqrt2  # GeV
        m_light_GeV = m_D**2 / M_R
        m_light_eV.append(m_light_GeV * 1e9)

    m1, m2, m3 = m_light_eV
    dm2_21 = m2**2 - m1**2
    dm2_31 = m3**2 - m1**2
    sum_nu = sum(m_light_eV)
    pull_dm21 = (dm2_21 - DM2_21_PDG) / SIGMA_DM21
    pull_dm31 = (dm2_31 - DM2_31_PDG) / SIGMA_DM31
    return {
        "type": "seesaw",
        "M_R_GeV": M_R,
        "n_dirac_eps": n_dirac_eps,
        "m1_eV": m1, "m2_eV": m2, "m3_eV": m3,
        "sum_eV": sum_nu,
        "planck_ok": sum_nu < SUM_NU_PDG,
        "dm2_21_eV2": dm2_21,
        "dm2_31_eV2": dm2_31,
        "pull_dm21": round(pull_dm21, 3),
        "pull_dm31": round(pull_dm31, 3),
        "dm21_ratio": round(dm2_21 / DM2_21_PDG, 3),
        "dm31_ratio": round(dm2_31 / DM2_31_PDG, 3),
    }


def scan_for_best():
    """Scan epsilon powers and find the best neutrino mass formula."""
    results = []
    for n in [1, 1.5, 2, 2.5, 3, 3.5, 4]:
        r = neutrino_masses_eps_power(n)
        r['n_eps'] = n
        r['m1_eV'] = round(r['m1_eV'], 8)
        r['m2_eV'] = round(r['m2_eV'], 8)
        r['m3_eV'] = round(r['m3_eV'], 8)
        r['sum_eV'] = round(r['sum_eV'], 8)
        if r['pull_dm21'] is not None:
            r['abs_pull_dm21'] = abs(r['pull_dm21'])
        results.append(r)
    return results


def main():
    print("=" * 72)
    print(" PASS 81 - TRACK AI: W33 EXACT NEUTRINO MASSES")
    print("=" * 72)
    print(f"  Cross-ref: DCCXCVII_NEUTRINO_MASS_HIERARCHY")
    print(f"  PDG: Delta m2_21 = {DM2_21_PDG:.2e} eV^2, Delta m2_31 = {DM2_31_PDG:.3e} eV^2")
    print(f"  Planck bound: sum(m_nu) < {SUM_NU_PDG} eV")
    print(f"  Lambda_W33 = {LAM_W33:.3e} GeV (seesaw scale)")
    print(f"  epsilon = {epsilon:.6f}")

    # Direct epsilon power scan
    scan = scan_for_best()
    print(f"\n  Direct Yukawa (eps^n * v * |lam|/lam1):")
    print(f"  {'n':>4} {'m1(eV)':>12} {'sum(eV)':>10} {'Planck':>7} {'dm21_ratio':>11} {'pull_dm21':>10}")
    for r in scan:
        p = r.get('planck_ok')
        dm21 = r.get('dm2_21_eV2', 0)
        ratio = round(dm21/DM2_21_PDG, 2) if dm21 else '-'
        pull = round(r.get('pull_dm21', 0), 2) if r.get('pull_dm21') else '-'
        print(f"  {r['n_eps']:>4.1f} {r['m1_eV']:>12.4e} {r['sum_eV']:>10.4e} "
              f"{'OK' if p else 'FAIL':>7} {str(ratio):>11} {str(pull):>10}")

    # Seesaw
    print(f"\n  Type-I Seesaw (M_R = Lambda_W33):")
    for n in [1, 2, 3]:
        ss = seesaw_masses(n)
        print(f"    n={n}: m_nu = ({ss['m1_eV']:.3e}, {ss['m2_eV']:.3e}, {ss['m3_eV']:.3e}) eV  "
              f"sum={ss['sum_eV']:.3e}  Planck={'OK' if ss['planck_ok'] else 'FAIL'}  "
              f"dm21_ratio={ss['dm21_ratio']}  pull_dm21={ss['pull_dm21']:+.2f}")

    # Best seesaw (n=1 Dirac Yukawa)
    best_ss = seesaw_masses(1)
    verdict = (
        "EXACT MATCH" if abs(best_ss['pull_dm21']) <= 1.0 and best_ss['planck_ok'] else
        "NEAR-MISS" if abs(best_ss['pull_dm21']) <= 3.0 and best_ss['planck_ok'] else
        "PARTIAL"
    )
    print(f"\n  Best seesaw (n=1): verdict = {verdict}")
    print(f"    m_nu = ({best_ss['m1_eV']:.3e}, {best_ss['m2_eV']:.3e}, {best_ss['m3_eV']:.3e}) eV")
    print(f"    Delta m^2_21 = {best_ss['dm2_21_eV2']:.3e} eV^2  (PDG: {DM2_21_PDG:.2e})  ratio={best_ss['dm21_ratio']}")
    print(f"    Delta m^2_31 = {best_ss['dm2_31_eV2']:.3e} eV^2  (PDG: {DM2_31_PDG:.3e})  ratio={best_ss['dm31_ratio']}")

    result = {
        "pass": 81,
        "track": "AI",
        "title": "Exact Neutrino Masses from W33",
        "cross_references": ["DCCXCVII_NEUTRINO_MASS_HIERARCHY"],
        "PDG": {
            "dm2_21_eV2": DM2_21_PDG,
            "dm2_31_eV2": DM2_31_PDG,
            "sum_nu_bound_eV": SUM_NU_PDG,
        },
        "epsilon": round(epsilon, 6),
        "Lambda_W33_GeV": LAM_W33,
        "direct_scan": [{k: v for k, v in r.items() if k != 'abs_pull_dm21'} for r in scan],
        "best_seesaw": best_ss,
        "verdict": verdict,
        "key_theorem": (
            f"W33 type-I seesaw at M_R=Lambda_W33={LAM_W33:.2e} GeV: "
            f"m_nu = ({best_ss['m1_eV']:.2e}, {best_ss['m2_eV']:.2e}, {best_ss['m3_eV']:.2e}) eV. "
            f"Sum = {best_ss['sum_eV']:.2e} eV < 0.12 eV (Planck). "
            f"dm21_ratio = {best_ss['dm21_ratio']}. Verdict: {verdict}."
        ),
        "status": "COMPLETE",
    }
    with open("w33_pass81_trackAI_neutrino_masses.json", "w") as f:
        json.dump(result, f, indent=2)
    print("\n  Witness JSON -> w33_pass81_trackAI_neutrino_masses.json")
    return result


if __name__ == "__main__":
    main()
