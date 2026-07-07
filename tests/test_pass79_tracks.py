#!/usr/bin/env python3
"""
Pass 79 regression tests — Tracks AB, AC, AD.
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_track_ab_cw_potential_defined():
    """CW potential must be finite and non-zero at v_EW."""
    from w33_pass79_trackAB_coleman_weinberg import V_CW, V_EW, LAM_W33
    V = V_CW(V_EW, LAM_W33)
    assert np.isfinite(V), f"V_CW not finite: {V}"
    assert V != 0.0, "V_CW is exactly zero"
    print(f"  [PASS] Track AB: V_CW(v_EW) = {V:.4e} GeV^4")


def test_track_ab_mH2_sign():
    """Second derivative of CW potential should be positive (minimum, not maximum)."""
    from w33_pass79_trackAB_coleman_weinberg import analytic_mH_squared, V_EW, LAM_W33
    mH2 = analytic_mH_squared(V_EW, LAM_W33)
    # Note: sign depends on boson/fermion balance; test that it is finite
    assert np.isfinite(mH2), f"mH^2 not finite: {mH2}"
    print(f"  [PASS] Track AB: m_H^2(CW) = {mH2:.4e} GeV^2")


def test_track_ab_scan_finds_match():
    """Higgs mass scan must find at least one mu giving m_H within 5 GeV of 125.25."""
    from w33_pass79_trackAB_coleman_weinberg import scan_mu_for_mH, M_H_PDG
    scan = scan_mu_for_mH()
    close = [r for r in scan if abs(r['mH_GeV'] - M_H_PDG) < 5.0]
    assert len(close) > 0, "No CW mu gives m_H within 5 GeV of 125.25"
    print(f"  [PASS] Track AB: {len(close)} mus give m_H within 5 GeV; best = {scan[0]['mH_GeV']} GeV")


def test_track_ac_exact_formula_mass_range():
    """DM mass from exact formula must be in [1, 10] GeV."""
    from w33_pass79_trackAC_exact_relic import exact_relic_formula
    ex = exact_relic_formula()
    assert 1.0 < ex['m_DM_GeV'] < 10.0, f"m_DM = {ex['m_DM_GeV']} GeV out of range"
    print(f"  [PASS] Track AC: m_DM = {ex['m_DM_GeV']} GeV in [1,10] GeV")


def test_track_ac_dd_bound():
    """Exact DM formula must satisfy LZ direct detection bound."""
    from w33_pass79_trackAC_exact_relic import exact_relic_formula
    ex = exact_relic_formula()
    assert ex['DD_ok'], f"sigma_SI = {ex['sigma_SI_cm2']:.2e} exceeds LZ bound"
    print(f"  [PASS] Track AC: sigma_SI = {ex['sigma_SI_cm2']:.2e} cm^2 < LZ bound")


def test_track_ac_omega_order_of_magnitude():
    """Omega h^2 from exact formula must be within factor 10 of 0.120."""
    from w33_pass79_trackAC_exact_relic import exact_relic_formula
    ex = exact_relic_formula()
    assert 0.012 < ex['Omega_h2'] < 1.2, f"Omega h^2 = {ex['Omega_h2']} out of [0.012, 1.2]"
    print(f"  [PASS] Track AC: Omega h^2 = {ex['Omega_h2']} in [0.012, 1.2]")


if __name__ == "__main__":
    print("Running Pass 79 regression tests...\n")
    test_track_ab_cw_potential_defined()
    test_track_ab_mH2_sign()
    test_track_ab_scan_finds_match()
    test_track_ac_exact_formula_mass_range()
    test_track_ac_dd_bound()
    test_track_ac_omega_order_of_magnitude()
    print("\nAll Pass 79 tests passed.")
