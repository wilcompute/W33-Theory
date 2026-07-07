#!/usr/bin/env python3
"""
Pass 74 regression tests — Tracks M, N, O.
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_track_m_e8_theta_sigma3():
    """σ₃(n) formula: σ₃(1)=1, σ₃(2)=9, σ₃(3)=28."""
    from w33_pass74_trackM_monster_moonshine import e8_theta
    c = e8_theta(5)
    assert c[1] == 240,    f"Expected 240, got {c[1]}"
    assert c[2] == 2160,   f"Expected 2160, got {c[2]}"
    assert c[3] == 6720,   f"Expected 6720, got {c[3]}"
    print("  [PASS] Track M: E8 theta coefficients 1, 2, 3 correct")


def test_track_m_moonshine_c0():
    """Z_{W33}³·q coefficient at q⁰ should be 1 (j(q)·q constant term)."""
    from w33_pass74_trackM_monster_moonshine import (
        e8_theta, eta_power, ps_divide, ps_cube, J_TIMES_Q
    )
    N = 12
    z = ps_divide(e8_theta(N), eta_power(8, N), N)
    z3 = ps_cube(z, N)
    c0 = round(float(z3[0]))
    assert c0 == J_TIMES_Q[0], f"z³[0] = {c0}, expected {J_TIMES_Q[0]}"
    print(f"  [PASS] Track M: Z_W33³·q[0] = {c0} (= j(q)·q constant term)")


def test_track_m_moonshine_c1():
    """Coefficient of q¹ in Z_{W33}³ should be 744."""
    from w33_pass74_trackM_monster_moonshine import (
        e8_theta, eta_power, ps_divide, ps_cube, J_TIMES_Q
    )
    N = 12
    z = ps_divide(e8_theta(N), eta_power(8, N), N)
    z3 = ps_cube(z, N)
    c1 = round(float(z3[1]))
    assert c1 == J_TIMES_Q[1], f"z³[1] = {c1}, expected {J_TIMES_Q[1]}"
    print(f"  [PASS] Track M: Z_W33³·q[1] = {c1} (= 744, j-function constant)")


def test_track_m_moonshine_c2():
    """Coefficient of q² in Z_{W33}³ should be 196884."""
    from w33_pass74_trackM_monster_moonshine import (
        e8_theta, eta_power, ps_divide, ps_cube, J_TIMES_Q
    )
    N = 13
    z = ps_divide(e8_theta(N), eta_power(8, N), N)
    z3 = ps_cube(z, N)
    c2 = round(float(z3[2]))
    assert c2 == J_TIMES_Q[2], f"z³[2] = {c2}, expected {J_TIMES_Q[2]}"
    print(f"  [PASS] Track M: Z_W33³·q[2] = {c2} (= 196884, Monster dimension)")


def test_track_n_cosmological_bound():
    """All three neutrino mass hypotheses must satisfy Σmᵢ < 0.12 eV."""
    from w33_pass74_trackN_neutrino_masses import (
        golden_ratio_masses, eigenvalue_ratio_masses, direct_eigenvalue_masses, PDG_NU
    )
    dm21 = PDG_NU['delta_m21_sq_eV2']
    dm31 = PDG_NU['delta_m31_sq_eV2']
    for fn, name in [
        (golden_ratio_masses, 'H1'),
        (eigenvalue_ratio_masses, 'H2'),
        (direct_eigenvalue_masses, 'H3'),
    ]:
        r = fn(dm21, dm31)
        assert r['sum_bound_satisfied'], f"{name}: Σmᵢ exceeds 0.12 eV"
        print(f"  [PASS] Track N: {name} Σmᵢ = {r['sum_mi_meV']} meV < 120 meV")


def test_track_n_h1_ruled_out():
    """Golden ratio H1 should be ruled out (ratio discrepancy factor ~9)."""
    from w33_pass74_trackN_neutrino_masses import golden_ratio_masses, PDG_NU
    r = golden_ratio_masses(PDG_NU['delta_m21_sq_eV2'], PDG_NU['delta_m31_sq_eV2'])
    assert r['ratio_discrepancy_factor'] > 5, \
        f"Expected H1 ruled out (factor >5), got {r['ratio_discrepancy_factor']}"
    print(f"  [PASS] Track N: H1 (golden ratio) ruled out, discrepancy factor = {r['ratio_discrepancy_factor']}")


if __name__ == "__main__":
    print("Running Pass 74 regression tests...\n")
    test_track_m_e8_theta_sigma3()
    test_track_m_moonshine_c0()
    test_track_m_moonshine_c1()
    test_track_m_moonshine_c2()
    test_track_n_cosmological_bound()
    test_track_n_h1_ruled_out()
    print("\nAll Pass 74 tests passed.")
