#!/usr/bin/env python3
"""
Pass 76 regression tests — Tracks S, T, U.
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_track_s_below_ligo():
    """Graviton zero-mode bound must be below LIGO bound."""
    from w33_pass76_trackS_graviton_mass import w33_graviton_bound, LIGO_BOUND_EV
    g = w33_graviton_bound()
    assert g['m_g_zero_mode_bound_eV'] < LIGO_BOUND_EV, (
        f"Graviton bound {g['m_g_zero_mode_bound_eV']:.2e} exceeds LIGO {LIGO_BOUND_EV:.2e}"
    )
    print(f"  [PASS] Track S: m_g < {g['m_g_zero_mode_bound_eV']:.3e} eV < LIGO {LIGO_BOUND_EV:.2e} eV")


def test_track_s_gw_speed():
    """GW speed constraint must be satisfied."""
    from w33_pass76_trackS_graviton_mass import graviton_speed_test
    spd = graviton_speed_test()
    assert spd['consistent'], f"GW speed test failed: delta_v/c = {spd['delta_v_over_c']:.2e}"
    print(f"  [PASS] Track S: GW speed delta_v/c = {spd['delta_v_over_c']:.2e} << 1e-15")


def test_track_t_m2_mass_range():
    """Light WIMP mass should be 1-5 GeV."""
    from w33_pass76_trackT_dark_matter import scenario_M2_light_wimp
    m2 = scenario_M2_light_wimp()
    assert 1.0 < m2['m_DM_GeV'] < 5.0, f"m_DM = {m2['m_DM_GeV']} GeV out of range"
    print(f"  [PASS] Track T: M2 m_DM = {m2['m_DM_GeV']} GeV in range [1,5] GeV")


def test_track_t_m2_direct_detection():
    """Light WIMP sigma_SI must be below LZ bound."""
    from w33_pass76_trackT_dark_matter import scenario_M2_light_wimp
    m2 = scenario_M2_light_wimp()
    assert m2['direct_detection_ok'], (
        f"sigma_SI = {m2['sigma_SI_cm2']:.2e} above LZ bound {m2['LZ_bound_cm2']:.2e}"
    )
    print(f"  [PASS] Track T: sigma_SI = {m2['sigma_SI_cm2']:.2e} cm^2 < LZ bound")


def test_track_t_symmetry_group_order():
    """Aut(GQ(3,3)) order should be 51840."""
    from w33_pass76_trackT_dark_matter import w33_dm_symmetry
    sym = w33_dm_symmetry()
    assert sym['group_order'] == 51840, f"Group order {sym['group_order']} != 51840"
    print(f"  [PASS] Track T: |Aut(GQ(3,3))| = {sym['group_order']}")


def test_track_t_m1_wimpzilla_mass():
    """WIMPZILLA mass should be > 1e13 GeV."""
    from w33_pass76_trackT_dark_matter import scenario_M1_wimpzilla
    m1 = scenario_M1_wimpzilla()
    assert m1['m_DM_GeV'] > 1e13, f"WIMPZILLA mass {m1['m_DM_GeV']:.2e} < 1e13 GeV"
    print(f"  [PASS] Track T: WIMPZILLA m_DM = {m1['m_DM_GeV']:.3e} GeV > 1e13 GeV")


if __name__ == "__main__":
    print("Running Pass 76 regression tests...\n")
    test_track_s_below_ligo()
    test_track_s_gw_speed()
    test_track_t_m2_mass_range()
    test_track_t_m2_direct_detection()
    test_track_t_symmetry_group_order()
    test_track_t_m1_wimpzilla_mass()
    print("\nAll Pass 76 tests passed.")
