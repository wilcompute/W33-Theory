"""
Regression tests for Part CCXIII — Higgs Mechanism and Mass Generation from W(3,3).
"""
import json
import math
import os
import pytest

RESULTS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "PART_CCXIII_higgs_mechanism_results.json"
)


@pytest.fixture(scope="module")
def results():
    with open(RESULTS_FILE) as f:
        return json.load(f)


def test_verified(results):
    assert results["verified"] is True


def test_free_parameters_zero(results):
    assert results["free_parameters"] == 0


# --- Electroweak boson structure ---
def test_massive_bosons_equals_Q(results):
    Q = results["srg_params"]["Q"]
    assert results["electroweak"]["n_massive_bosons"] == Q


def test_massive_bosons_is_3(results):
    assert results["electroweak"]["n_massive_bosons"] == 3


def test_goldstone_count_equals_Q(results):
    Q = results["srg_params"]["Q"]
    assert results["electroweak"]["n_goldstone"] == Q


def test_higgs_singlet_is_1(results):
    assert results["electroweak"]["n_higgs_singlet"] == 1


# --- Weinberg angle ---
def test_weinberg_angle_estimate(results):
    sin2_W33 = results["electroweak"]["sin2_weinberg_W33"]
    assert abs(sin2_W33 - 0.25) < 1e-9  # MU/LAP_TOP = 4/16 = 0.25


def test_weinberg_angle_within_10pct(results):
    err = results["electroweak"]["weinberg_error_pct"]
    assert err < 10.0


# --- W/Z mass ratio ---
def test_mW_mZ_ratio_within_2pct(results):
    err = results["electroweak"]["mWZ_error_pct"]
    assert err < 2.0


def test_mW_mZ_ratio_value(results):
    mWZ = results["electroweak"]["mW_mZ_W33"]
    # sqrt(3)/2
    expected = math.sqrt(3.0) / 2.0
    assert abs(mWZ - expected) < 1e-9


# --- Higgs structure ---
def test_eigenvalue_ratio_half(results):
    assert results["higgs"]["eigenvalue_ratio"] == 0.5


def test_vacuum_degeneracy_is_M_LAM(results):
    M_LAM = results["srg_params"]["M_LAM"]
    assert results["higgs"]["vacuum_degeneracy"] == M_LAM


def test_K_over_Q_equals_MU(results):
    K = results["srg_params"]["K"]
    Q = results["srg_params"]["Q"]
    MU = results["srg_params"]["MU"]
    assert K // Q == MU


def test_M_LAM_equals_Q_cubed(results):
    Q = results["srg_params"]["Q"]
    M_LAM = results["srg_params"]["M_LAM"]
    assert M_LAM == Q ** 3


# --- Yukawa count ---
def test_yukawa_estimate_is_24(results):
    assert results["yukawa"]["estimate"] == 24


def test_yukawa_within_3_of_SM(results):
    est = results["yukawa"]["estimate"]
    sm = results["yukawa"]["SM_approx"]
    assert abs(est - sm) <= 3


# --- All checks ---
def test_all_individual_checks(results):
    for name, val in results["all_checks"].items():
        assert val is True, f"Check '{name}' failed"
