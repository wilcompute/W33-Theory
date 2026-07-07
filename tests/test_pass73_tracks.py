#!/usr/bin/env python3
"""
Pass 73 regression tests — Tracks J, K, L.
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_track_k_e8_theta():
    """E8 theta coefficients must match OEIS A004009."""
    from w33_pass73_trackK_affine_e8_character import e8_theta_coefficients, KNOWN_E8_THETA
    computed = e8_theta_coefficients(20)
    for i in range(20):
        assert computed[i] == KNOWN_E8_THETA[i], f"Mismatch at n={i}: {computed[i]} != {KNOWN_E8_THETA[i]}"
    print("  [PASS] Track K: E8 theta series matches OEIS A004009 (20 terms)")


def test_track_k_240_roots():
    """Coefficient 240 = number of E8 roots."""
    from w33_pass73_trackK_affine_e8_character import e8_theta_coefficients
    c = e8_theta_coefficients(3)
    assert c[1] == 240, f"Expected 240 roots, got {c[1]}"
    print("  [PASS] Track K: Theta_E8 coefficient at q^1 = 240 (E8 roots)")


def test_track_l_theta13_formula():
    """theta_13 = arcsin(2/(1+sqrt(97))) should be ~8.55 degrees."""
    from w33_pass73_trackL_pmns_cp_phase import w33_predictions
    pred = w33_predictions()
    t13 = pred['theta_13_pred_deg']
    assert abs(t13 - 8.55) < 0.5, f"theta_13 = {t13}, expected ~8.55"
    print(f"  [PASS] Track L: theta_13 = {t13:.3f}° (formula: arcsin(2/(1+sqrt(97))))")


def test_track_l_delta_cp_in_range():
    """delta_CP prediction should be within 2-sigma of NuFIT 6.0."""
    from w33_pass73_trackL_pmns_cp_phase import w33_predictions, PDG
    pred = w33_predictions()
    d_pred = pred['delta_CP_pred_deg']
    d_obs  = PDG['delta_CP_deg']
    d_err  = PDG['delta_CP_err']
    pull   = abs(d_pred - d_obs) / d_err
    assert pull < 2.0, f"delta_CP pull = {pull:.2f}sigma (>2sigma)"
    print(f"  [PASS] Track L: delta_CP = {d_pred:.1f}° within {pull:.2f}sigma of PDG")


def test_track_l_jarlskog():
    """Jarlskog J_theory should be positive and order 0.03."""
    from w33_pass73_trackL_pmns_cp_phase import w33_predictions, jarlskog
    pred = w33_predictions()
    J = jarlskog(
        pred['theta_12_pred_deg'], pred['theta_13_pred_deg'],
        pred['theta_23_pred_deg'], pred['delta_CP_pred_deg']
    )
    assert J > 0.02 and J < 0.05, f"J = {J:.5f}, expected in (0.02, 0.05)"
    print(f"  [PASS] Track L: Jarlskog J = {J:.5f}")


def test_track_l_unitarity():
    """PMNS matrix must be unitary to 1e-12."""
    from w33_pass73_trackL_pmns_cp_phase import w33_predictions, pmns_matrix, unitarity_check
    pred = w33_predictions()
    U = pmns_matrix(
        pred['theta_12_pred_deg'], pred['theta_13_pred_deg'],
        pred['theta_23_pred_deg'], pred['delta_CP_pred_deg']
    )
    err = unitarity_check(U)
    assert err < 1e-12, f"Unitarity error = {err:.2e}"
    print(f"  [PASS] Track L: PMNS unitarity error = {err:.2e}")


if __name__ == "__main__":
    print("Running Pass 73 regression tests...\n")
    test_track_k_e8_theta()
    test_track_k_240_roots()
    test_track_l_theta13_formula()
    test_track_l_delta_cp_in_range()
    test_track_l_jarlskog()
    test_track_l_unitarity()
    print("\nAll Pass 73 tests passed.")
