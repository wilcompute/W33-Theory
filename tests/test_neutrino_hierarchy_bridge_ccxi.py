"""
Regression tests for Part CCXI — Neutrino Mass Hierarchy from W(3,3).
"""
import json
import math
import os
import pytest

RESULTS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "PART_CCXI_neutrino_hierarchy_results.json"
)


@pytest.fixture(scope="module")
def results():
    with open(RESULTS_FILE) as f:
        return json.load(f)


def test_verified(results):
    assert results["verified"] is True


def test_free_parameters_zero(results):
    assert results["free_parameters"] == 0


# --- PMNS structure ---
def test_pmns_dimension_is_3(results):
    assert results["pmns"]["pmns_dimension"] == 3


def test_pmns_dimension_equals_Q(results):
    assert results["pmns"]["pmns_dimension"] == results["srg_params"]["Q"]


def test_n_mixing_angles_is_3(results):
    assert results["pmns"]["n_mixing_angles"] == 3


def test_n_dirac_cp_phases_is_1(results):
    assert results["pmns"]["n_dirac_cp_phases"] == 1


def test_n_majorana_phases_is_2(results):
    assert results["pmns"]["n_majorana_phases"] == 2


# --- Mixing angles ---
def test_theta_12_sin2_is_one_third(results):
    sin2 = results["theta_12"]["sin2_W33"]
    assert abs(sin2 - 1.0 / 3) < 1e-15


def test_theta_12_within_12pct(results):
    assert results["theta_12"]["relative_error_pct"] < 12.0


def test_theta_23_sin2_is_half(results):
    sin2 = results["theta_23"]["sin2_W33"]
    assert abs(sin2 - 0.5) < 1e-15


def test_theta_23_within_15pct(results):
    assert results["theta_23"]["relative_error_pct"] < 15.0


def test_theta_13_within_30pct(results):
    assert results["theta_13"]["relative_error_pct"] < 30.0


def test_theta_13_formula(results):
    sin2 = results["theta_13"]["sin2_W33"]
    # (LAM/K)^2 = (2/12)^2 = 1/36
    assert abs(sin2 - 1.0 / 36) < 1e-15


# --- Mass splitting ---
def test_mass_splitting_ratio_within_15pct(results):
    assert results["mass_splitting"]["relative_error_pct"] < 15.0


def test_mass_splitting_formula_gives_36(results):
    assert results["mass_splitting"]["dm2_ratio_W33"] == 36


# --- Hierarchy ---
def test_normal_hierarchy(results):
    assert results["hierarchy"]["type"] == "normal"


def test_M_LAM_over_M_NEG_greater_than_1(results):
    assert results["hierarchy"]["M_LAM_over_M_NEG"] > 1.0


# --- TBM ---
def test_tbm_sin2_12_from_Q(results):
    Q = results["srg_params"]["Q"]
    assert abs(results["tbm"]["sin2_12"] - 1.0 / Q) < 1e-15


def test_tbm_sin2_23_maximal(results):
    assert abs(results["tbm"]["sin2_23"] - 0.5) < 1e-15


# --- All checks ---
def test_all_individual_checks(results):
    for name, val in results["all_checks"].items():
        assert val is True, f"Check '{name}' failed"
