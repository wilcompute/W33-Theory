#!/usr/bin/env python3
"""
Pass 81 regression tests - Tracks AH, AI, AJ.
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_track_ah_cabibbo_formula():
    """Cabibbo formula sin(theta_C)=(lam2-lam3)/lam1 must be in [0.15, 0.30]."""
    from w33_pass81_trackAH_yukawa_matrix import ckm_from_yukawa
    formulas = ckm_from_yukawa()
    best = formulas[0]
    assert 0.15 <= best['sin'] <= 0.30, f"sin(theta_C) = {best['sin']} out of [0.15, 0.30]"
    print(f"  [PASS] Track AH: best sin(theta_C) = {best['sin']:.4f}, theta_C = {best['theta']:.4f} deg")


def test_track_ah_yukawa_hierarchy():
    """Yukawa hierarchy m_t > m_c > m_u must be correct."""
    from w33_pass81_trackAH_yukawa_matrix import w33_yukawa_up_epsilon, M_TOP
    yup = w33_yukawa_up_epsilon()
    assert yup['m_charm_pred_GeV'] > yup['m_up_pred_GeV'], "Charm must be heavier than up"
    assert M_TOP > yup['m_charm_pred_GeV'], "Top must be heavier than charm"
    print(f"  [PASS] Track AH: m_t={M_TOP} > m_c={yup['m_charm_pred_GeV']:.3f} > m_u={yup['m_up_pred_GeV']:.4f} GeV")


def test_track_ai_planck_bound():
    """Seesaw neutrino masses must satisfy Planck bound sum < 0.12 eV."""
    from w33_pass81_trackAI_neutrino_masses import seesaw_masses, SUM_NU_PDG
    ss = seesaw_masses(1)
    assert ss['planck_ok'], f"sum(m_nu) = {ss['sum_eV']:.3e} eV exceeds Planck {SUM_NU_PDG} eV"
    print(f"  [PASS] Track AI: sum(m_nu) = {ss['sum_eV']:.3e} eV < {SUM_NU_PDG} eV")


def test_track_ai_mass_hierarchy():
    """Neutrino mass hierarchy m3 > m2 > m1 (normal ordering)."""
    from w33_pass81_trackAI_neutrino_masses import seesaw_masses
    ss = seesaw_masses(1)
    assert ss['m3_eV'] > ss['m2_eV'] > ss['m1_eV'], \
        f"Hierarchy broken: {ss['m1_eV']:.3e} {ss['m2_eV']:.3e} {ss['m3_eV']:.3e}"
    print(f"  [PASS] Track AI: normal ordering m3>m2>m1 confirmed")


def test_track_ai_dm21_positive():
    """Delta m^2_21 must be positive (solar splitting)."""
    from w33_pass81_trackAI_neutrino_masses import seesaw_masses
    ss = seesaw_masses(1)
    assert ss['dm2_21_eV2'] > 0, f"dm2_21 = {ss['dm2_21_eV2']:.3e} is not positive"
    print(f"  [PASS] Track AI: dm^2_21 = {ss['dm2_21_eV2']:.3e} eV^2 > 0")


if __name__ == "__main__":
    print("Running Pass 81 regression tests...\n")
    test_track_ah_cabibbo_formula()
    test_track_ah_yukawa_hierarchy()
    test_track_ai_planck_bound()
    test_track_ai_mass_hierarchy()
    test_track_ai_dm21_positive()
    print("\nAll Pass 81 tests passed.")
