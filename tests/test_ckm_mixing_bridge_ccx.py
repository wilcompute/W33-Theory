"""
Regression tests for Part CCX — CKM Quark Mixing from W(3,3).
"""
import json
import math
import os
import pytest

RESULTS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "PART_CCX_ckm_mixing_results.json"
)


@pytest.fixture(scope="module")
def results():
    with open(RESULTS_FILE) as f:
        return json.load(f)


def test_verified(results):
    assert results["verified"] is True


def test_free_parameters_zero(results):
    assert results["free_parameters"] == 0


# --- CKM dimension ---
def test_ckm_dimension_equals_Q(results):
    assert results["ckm_dimension"] == results["srg_params"]["Q"]


def test_ckm_is_3x3(results):
    assert results["ckm_dimension"] == 3


# --- Physical angles and CP phases ---
def test_n_physical_mixing_angles_is_3(results):
    assert results["n_physical_mixing_angles"] == 3


def test_n_physical_angles_from_Q(results):
    Q = results["srg_params"]["Q"]
    assert results["n_physical_mixing_angles"] == Q * (Q - 1) // 2


def test_n_cp_phases_is_1(results):
    assert results["n_cp_phases"] == 1


def test_n_cp_phases_from_Q(results):
    Q = results["srg_params"]["Q"]
    assert results["n_cp_phases"] == (Q - 1) * (Q - 2) // 2


# --- Cabibbo angle ---
def test_cabibbo_primary_close(results):
    err = results["cabibbo"]["error"]
    assert err < 0.005  # 1.4% error → |0.22222 - 0.22537| < 0.005


def test_cabibbo_within_2pct(results):
    assert results["cabibbo"]["relative_error_pct"] < 2.0


def test_cabibbo_digits_ge_1pt8(results):
    assert results["cabibbo"]["digits"] >= 1.8


def test_cabibbo_formula_is_2over9(results):
    sin_C = results["cabibbo"]["sin_C_W33_primary"]
    assert abs(sin_C - 2 / 9) < 1e-15


def test_cabibbo_fraction_string(results):
    assert results["cabibbo"]["sin_C_W33_fraction"] == "4/18"


# --- Alternative formula ---
def test_alt_formula_within_5pct(results):
    assert results["cabibbo_alt"]["relative_error_pct"] < 5.0


# --- Wolfenstein hierarchy ---
def test_wolfenstein_hierarchy_decreasing(results):
    w = results["wolfenstein"]
    assert w["sin_12"] > w["sin_23"] > w["sin_13"]


def test_wolfenstein_sin_12_range(results):
    sin_12 = results["wolfenstein"]["sin_12"]
    assert 0.20 < sin_12 < 0.25


# --- All checks ---
def test_all_individual_checks(results):
    for name, val in results["all_checks"].items():
        assert val is True, f"Check '{name}' failed"
