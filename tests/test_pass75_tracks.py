#!/usr/bin/env python3
"""
Pass 75 regression tests — Tracks P, Q, R.
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_track_p_eigenvalue_ratio_formula():
    """lambda3^2/(lambda2^2+lambda3^2) should be ~0.234."""
    from w33_pass75_trackP_weinberg_angle import formula_eigenvalue_ratio, PDG
    val, _ = formula_eigenvalue_ratio()
    assert 0.22 < val < 0.26, f"Weinberg angle estimate {val:.4f} out of expected range"
    print(f"  [PASS] Track P: eigenvalue-ratio sin^2(theta_W) = {val:.5f}")


def test_track_p_qlc_within_3sigma():
    """QLC sum should be within 3 sigma of PDG."""
    from w33_pass75_trackP_weinberg_angle import quark_lepton_complementarity
    qlc = quark_lepton_complementarity()
    assert abs(qlc['pull_sigma']) < 3.0, f"QLC pull = {qlc['pull_sigma']}sigma"
    print(f"  [PASS] Track P: QLC pull = {qlc['pull_sigma']}sigma < 3sigma")


def test_track_q_def3_above_superk():
    """Def-3 GUT scale (near M_GUT) should give tau > Super-K bound."""
    from w33_pass75_trackQ_proton_decay import (
        w33_gut_scale, proton_lifetime_yr, mixing_suppression, SUPERK_BOUND_YR
    )
    scales = w33_gut_scale()
    mix = mixing_suppression()
    tau, _ = proton_lifetime_yr(scales['def3'])
    tau_corr = tau * mix['suppression_factor']
    assert tau_corr > SUPERK_BOUND_YR, (
        f"Def-3 tau = {tau_corr:.2e} yr below Super-K bound {SUPERK_BOUND_YR:.2e} yr"
    )
    print(f"  [PASS] Track Q: Def-3 tau_p = {tau_corr:.3e} yr > Super-K bound")


def test_track_q_def1_testable():
    """Def-1 GUT scale should give a finite, positive lifetime."""
    from w33_pass75_trackQ_proton_decay import (
        w33_gut_scale, proton_lifetime_yr, mixing_suppression
    )
    scales = w33_gut_scale()
  