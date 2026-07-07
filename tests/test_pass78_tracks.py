#!/usr/bin/env python3
"""
Pass 78 regression tests — Tracks Y, Z, AA.
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_track_y_spread_improves():
    """2-loop + W33 spread must be less than 1-loop SM spread."""
    from w33_pass78_trackY_2loop_unification import unification_analysis_2loop
    r = unification_analysis_2loop()
    assert r['spread_hierarchy']['2loop_W33_threshold'] < r['spread_hierarchy']['1loop_SM'], \
        "2-loop W33 did not improve over 1-loop SM"
    print(f"  [PASS] Track Y: spread {r['spread_hierarchy']['1loop_SM']:.3f} -> "
          f"{r['spread_hierarchy']['2loop_W33_threshold']:.3f}")


def test_track_y_matter_content():
    """W33 extra matter Delta b_i must be positive for U1 and SU2."""
    from w33_pass78_trackY_2loop_unification import DB1_W33, DB2_W33, DB3_W33
    assert DB1_W33 > 0 and DB2_W33 > 0, "W33 matter should increase b1, b2"
    print(f"  [PASS] Track Y: Delta b = ({DB1_W33:.2f}, {DB2_W33:.2f}, {DB3_W33:.2f})")


def test_track_z_scan_finds_candidates():
    """Higgs mass scan must find at least 1 formula within 5-sigma."""
    from w33_pass78_trackZ_higgs_mass import scan_formulas
    results = scan_formulas()
    within_5sig = [r for r in results if r['abs_pull'] <= 5.0]
    assert len(within_5sig) > 0, "No W33 Higgs formula within 5-sigma"
    print(f"  [PASS] Track Z: {len(within_5sig)} formulas within 5-sigma, best pull = {results[0]['pull']:+.3f}")


def test_track_z_vev_scale():
    """All formulas must use v_EW ~ 246 GeV as base scale."""
    from w33_pass78_trackZ_higgs_mass import V_EW_GEV
    assert 245 < V_EW_GEV < 248, f"v_EW = {V_EW_GEV} GeV out of range"
    print(f"  [PASS] Track Z: v_EW = {V_EW_GEV} GeV")


def test_track_z_epsilon_value():
    """Epsilon must be the correct Ramanujan value ~0.02512."""
    from w33_pass78_trackZ_higgs_mass import epsilon
    assert 0.024 < epsilon < 0.027, f"epsilon = {epsilon:.6f} out of expected range"
    print(f"  [PASS] Track Z: epsilon = {epsilon:.6f}")


if __name__ == "__main__":
    print("Running Pass 78 regression tests...\n")
    test_track_y_spread_improves()
    test_track_y_matter_content()
    test_track_z_scan_finds_candidates()
    test_track_z_vev_scale()
    test_track_z_epsilon_value()
    print("\nAll Pass 78 tests passed.")
