"""
Regression tests for Part CCXII — Baryon Asymmetry and CP Violation from W(3,3).
"""
import json
import math
import os
import pytest

RESULTS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "PART_CCXII_baryon_asymmetry_results.json"
)


@pytest.fixture(scope="module")
def results():
    with open(RESULTS_FILE) as f:
        return json.load(f)


def test_verified(results):
    assert results["verified"] is True


def test_free_parameters_zero(results):
    assert results["free_parameters"] == 0


# --- Sakharov conditions ---
def test_sakharov_baryon_violation(results):
    assert results["sakharov"]["baryon_violation"] is True


def test_sakharov_cp_violation(results):
    assert results["sakharov"]["cp_violation"] is True


def test_sakharov_non_equilibrium(results):
    assert results["sakharov"]["non_equilibrium"] is True


def test_all_three_sakharov_met(results):
    assert results["sakharov"]["all_satisfied"] is True


# --- CP violation ---
def test_n_cp_phases_is_1(results):
    assert results["cp"]["n_cp_phases"] == 1


def test_cp_phases_from_Q(results):
    Q = results["srg_params"]["Q"]
    assert results["cp"]["n_cp_phases"] == (Q - 1) * (Q - 2) // 2


def test_jarlskog_structural_positive(results):
    assert results["cp"]["jarlskog_structural"] > 0


def test_jarlskog_structural_below_max(results):
    J = results["cp"]["jarlskog_structural"]
    J_max = 1.0 / (6.0 * math.sqrt(3.0))
    assert J < J_max


# --- Baryon asymmetry ---
def test_baryon_asymmetry_order_magnitude(results):
    ratio = results["baryon_asymmetry"]["ratio_estimate_to_exp"]
    assert 1e1 < ratio < 1e4


def test_baryon_asymmetry_positive(results):
    assert results["baryon_asymmetry"]["eta_W33_estimate"] > 0


# --- Automorphism group ---
def test_aut_order_correct(results):
    assert results["automorphism"]["order"] == 51840


def test_aut_z3_power_ge_4(results):
    assert results["automorphism"]["Z3_power"] >= 4


# --- Q=3 minimality ---
def test_Q_equals_3(results):
    assert results["srg_params"]["Q"] == 3


def test_spectral_gap_positive(results):
    assert results["srg_params"]["LAP_MID"] > 0


# --- All checks ---
def test_all_individual_checks(results):
    for name, val in results["all_checks"].items():
        assert val is True, f"Check '{name}' failed"
