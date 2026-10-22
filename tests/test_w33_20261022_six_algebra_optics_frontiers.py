"""Falsifiable six-frontier tests: independent exact algebra plus bounded numerics."""
import pytest
from analysis.w33_20261022_six_algebra_optics_frontiers import (
    prime_power_jordan,order_five_equivariance,optical_clock,
    arithmetic_frobenius,analytic_boundary,release)

def test_pascal_primepower_jordan_4_8_9():
    r=prime_power_jordan()
    cases={a["q"]:a for a in r["cases"]}
    assert {q:v["rank_B"] for q,v in cases.items()}=={3:10,4:16,8:64,9:100}
    assert all(a["Jordan_blocks_size1"]>=0 for a in cases.values())

def test_explicit_order5_symplectic_character():
    a=order_five_equivariance()
    assert a["point_fixed_count"]==a["line_fixed_count"]==0
    assert a["transfer_sector_characters"]["quartic_96"]["trivial_C5_copies"]==16
    assert a["transfer_sector_characters"]["quartic_96"]["cyclotomic_Qzeta5_copies"]==20
    assert a["transfer_sector_characters"]["quadratic_60"]["trivial_C5_copies"]==12
    assert a["transfer_sector_characters"]["quadratic_60"]["cyclotomic_Qzeta5_copies"]==12

def test_signed_four_mode_diagonal_loss_robustness():
    r=optical_clock()
    assert r["normalized_state_revival_with_fixed_diagonal_loss"]
    assert r["mixing_error_03_four_step_residual"]>.01
    assert r["native_transfer_not_Euclidean_unitary"]

def test_golden_F9_and_primepower_curve_basechange():
    r=arithmetic_frobenius()
    assert r["golden_unit_orders"]=={"3":8,"7":16,"23":48}
    assert r["prime_power_extension_cases"]==18

def test_existing_complete_Weil_and_ccm_replay():
    r=analytic_boundary()
    assert r["CCM_small_N_first_zero_error"]<.0002
    assert r["smooth_Weil_2D_min_eigenvalue"]>0
    assert r["relative_trace_eta_scaling"]==4

def test_strict_scope_and_all_subreports():
    r=release()
    assert r["classical_RH_proved"] is False
    assert all(a["status"].startswith("PASS") for a in r.values() if isinstance(a,dict))
