#!/usr/bin/env python3
"""
Pass 77 regression tests — Tracks V, W, X.
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_track_v_original_m2_overproduction():
    """Original M2 scenario should give Omega h^2 > 0.12 (overproduction)."""
    from w33_pass77_trackV_relic_density import (
        sigma_ann_v, relic_density, M_Z_GEV, epsilon, lambda1, lambda3
    )
    m_M2 = M_Z_GEV * epsilon
    W33f = (lambda1 * lambda3)**2
    sigma, _ = sigma_ann_v(m_M2, W33f)
    Omega = relic_density(sigma)
    assert Omega > 0.12, f"Expected overproduction, got Omega h^2 = {Omega:.4f}"
    print(f"  [PASS] Track V: M2 Omega h^2 = {Omega:.4f} > 0.12 (overproduction confirmed)")


def test_track_v_resonance_enhances_cross_section():
    """BW factor at m_DM = M_Z/2 should be much larger than at m_DM = 2 GeV."""
    from w33_pass77_trackV_relic_density import breit_wigner_enhancement, M_Z_GEV
    BW_low  = breit_wigner_enhancement(2.0)
    BW_peak = breit_wigner_enhancement(M_Z_GEV / 2)
    assert BW_peak > BW_low * 100, f"BW peak ({BW_peak:.3e}) not >> BW low ({BW_low:.3e})"
    print(f"  [PASS] Track V: BW peak/low ratio = {BW_peak/BW_low:.2e}")


def test_track_w_spectrum_multiplicities():
    """GQ(3,3) eigenvalue multiplicities must sum to 40."""
    from w33_pass77_trackW_cosmological_constant import EIGENVALUES
    total = sum(m for _, m in EIGENVALUES)
    assert total == 40, f"Multiplicities sum to {total}, expected 40"
    print(f"  [PASS] Track W: eigenvalue multiplicities sum to {total}")


def test_track_w_cc_problem_open():
    """Epsilon^2 suppression should still leave CC many orders too large."""
    from w33_pass77_trackW_cosmological_constant import cc_hierarchy_analysis
    a = cc_hierarchy_analysis()
    assert a['log10_ratio_eps2'] > 10, (
        f"epsilon^2 residual only {a['log10_ratio_eps2']:.0f} decades above obs"
    )
    print(f"  [PASS] Track W: epsilon^2 CC residual is 10^{a['log10_ratio_eps2']:.0f} x observed (CC open)")


def test_track_x_w33_improves_spread():
    """W33 threshold corrections should reduce the coupling spread."""
    from w33_pass77_trackX_gauge_unification import unification_analysis
    r = unification_analysis()
    assert r['spread_W33_corrected'] <= r['spread_SM_only'], (
        f"W33 corrections worsened spread: {r['spread_W33_corrected']:.3f} > {r['spread_SM_only']:.3f}"
    )
    print(f"  [PASS] Track X: spread {r['spread_SM_only']:.3f} -> {r['spread_W33_corrected']:.3f} ({r['spread_improvement']}% improvement)")


def test_track_x_log_ratio_positive():
    """log(Lambda_W33/M_Z) must be positive (Lambda_W33 > M_Z)."""
    from w33_pass77_trackX_gauge_unification import unification_analysis
    r = unification_analysis()
    assert r['log_Lambda_over_MZ'] > 0, "Lambda_W33 < M_Z, something is wrong"
    print(f"  [PASS] Track X: log(Lambda_W33/M_Z) = {r['log_Lambda_over_MZ']:.4f} > 0")


if __name__ == "__main__":
    print("Running Pass 77 regression tests...\n")
    test_track_v_original_m2_overproduction()
    test_track_v_resonance_enhances_cross_section()
    test_track_w_spectrum_multiplicities()
    test_track_w_cc_problem_open()
    test_track_x_w33_improves_spread()
    test_track_x_log_ratio_positive()
    print("\nAll Pass 77 tests passed.")
