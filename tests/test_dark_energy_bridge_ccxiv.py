"""
Regression tests for Part CCXIV — Dark Energy and Cosmological Constant from W(3,3).
"""
import json
import os
import pytest

RESULTS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "PART_CCXIV_dark_energy_results.json"
)


@pytest.fixture(scope="module")
def results():
    with open(RESULTS_FILE) as f:
        return json.load(f)


def test_verified(results):
    assert results["verified"] is True


def test_free_parameters_zero(results):
    assert results["free_parameters"] == 0


# --- Cosmological fractions ---
def test_omega_lambda_W33(results):
    assert abs(results["cosmology"]["omega_lambda_W33"] - 27.0 / 40.0) < 1e-9


def test_omega_lambda_within_2pct(results):
    assert results["cosmology"]["omega_lambda_error_pct"] < 2.0


def test_omega_m_W33(results):
    assert abs(results["cosmology"]["omega_m_W33"] - 12.0 / 40.0) < 1e-9


def test_omega_m_within_5pct(results):
    assert results["cosmology"]["omega_m_error_pct"] < 5.0


def test_omega_ratio_W33(results):
    assert abs(results["cosmology"]["omega_ratio_W33"] - 27.0 / 12.0) < 1e-9


def test_omega_ratio_within_5pct(results):
    assert results["cosmology"]["omega_ratio_error_pct"] < 5.0


# --- Spectral structure ---
def test_spectral_sum_positive(results):
    assert results["spectral"]["spectral_sum"] > 0


def test_spectral_sum_value(results):
    assert results["spectral"]["spectral_sum"] == 6


def test_spectral_gap_value(results):
    assert results["spectral"]["spectral_gap"] == 6


def test_spectral_gap_divides_aut(results):
    AUT_ORDER = results["srg_params"]["AUT_ORDER"]
    gap = results["spectral"]["spectral_gap"]
    assert AUT_ORDER % gap == 0


def test_suppression_exists(results):
    assert results["spectral"]["suppression"] < 1e-20


def test_ext_suppression_smaller(results):
    assert results["spectral"]["ext_suppression"] < results["spectral"]["suppression"]


# --- SRG integrity ---
def test_M_LAM_plus_M_NEG_plus_1_equals_V(results):
    p = results["srg_params"]
    assert p["M_LAM"] + p["M_NEG"] + 1 == p["V"]


def test_all_individual_checks(results):
    for name, val in results["all_checks"].items():
        assert val is True, f"Check '{name}' failed"
