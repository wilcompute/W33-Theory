"""
Regression tests for Part CCIX — Three-Generation Fermion Structure from W(3,3).
"""
import json
import math
import os
import pytest

RESULTS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "PART_CCIX_three_generation_results.json"
)


@pytest.fixture(scope="module")
def results():
    with open(RESULTS_FILE) as f:
        return json.load(f)


def test_verified(results):
    assert results["verified"] is True


def test_free_parameters_zero(results):
    assert results["free_parameters"] == 0


# --- Generation count ---
def test_generation_count_equals_Q(results):
    assert results["generation_count"] == results["srg_params"]["Q"]


def test_generation_count_is_3(results):
    assert results["generation_count"] == 3


# --- Generation-volume identity ---
def test_Q_cubed_equals_27(results):
    Q = results["srg_params"]["Q"]
    assert Q**3 == 27


def test_M_LAM_equals_Q_cubed(results):
    assert results["M_LAM_equals_Q_cubed"] is True


def test_Q_cubed_field_value(results):
    assert results["Q_cubed"] == 27


# --- Eigenvalue generation ratio ---
def test_eigenvalue_ratio_equals_Q(results):
    assert results["eigenvalue_ratio"] == results["srg_params"]["Q"]


def test_eigenvalue_ratio_is_3(results):
    assert results["eigenvalue_ratio"] == 3


# --- Koide ratio (exact) ---
def test_koide_exact_equals_two_thirds(results):
    assert abs(results["koide_exact"] - 2 / 3) < 1e-15


def test_koide_experimental_close(results):
    assert abs(results["koide_experimental"] - 2 / 3) < 1e-3


def test_koide_experimental_5_digits(results):
    assert results["koide_error"] < 1e-4


def test_koide_digits_gt_4(results):
    assert results["koide_digits"] > 4.0


# --- Lepton masses sanity ---
def test_lepton_masses_positive(results):
    for name, m in results["lepton_masses_MeV"].items():
        assert m > 0, f"{name} mass not positive"


def test_tau_heavier_than_muon(results):
    assert results["lepton_masses_MeV"]["tau"] > results["lepton_masses_MeV"]["muon"]


def test_muon_heavier_than_electron(results):
    assert results["lepton_masses_MeV"]["muon"] > results["lepton_masses_MeV"]["electron"]


# --- Laplacian structure ---
def test_LAP_MID_equals_K_minus_lam(results):
    K = results["srg_params"]["K"]
    LAM = results["srg_params"]["LAM"]
    assert results["atoms"]["LAP_MID"] == K - LAM


def test_LAP_TOP_equals_16(results):
    assert results["atoms"]["LAP_TOP"] == 16


def test_LAP_MID_equals_10(results):
    assert results["atoms"]["LAP_MID"] == 10


# --- All individual checks ---
def test_all_individual_checks(results):
    for name, val in results["all_checks"].items():
        assert val is True, f"Check '{name}' failed"
