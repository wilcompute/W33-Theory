"""
Regression tests for Part CCVIII — Fine Structure Constant α⁻¹ from W(3,3).
Loads PART_CCVIII_alpha_derivation_results.json and asserts key properties.
"""
import json
import math
import os
import pytest

RESULTS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "PART_CCVIII_alpha_derivation_results.json"
)


@pytest.fixture(scope="module")
def results():
    with open(RESULTS_FILE) as f:
        return json.load(f)


def test_verified(results):
    assert results["verified"] is True


def test_int_part_is_137(results):
    assert results["int_part"] == 137


def test_free_parameters_zero(results):
    assert results["free_parameters"] == 0


def test_formula_B_frac_numerator(results):
    assert results["formula_B"]["frac_numerator"] == 36


def test_formula_B_frac_denominator(results):
    assert results["formula_B"]["frac_denominator"] == 1000


def test_formula_B_value_close(results):
    assert abs(results["formula_B"]["value"] - 137.036) < 1e-6


def test_formula_B_digits_ge_6(results):
    assert results["formula_B"]["digits"] >= 6.0


def test_formula_B_better_than_A(results):
    assert results["formula_B"]["error"] < results["formula_A"]["error"]


def test_formula_B_error_lt_1e6(results):
    assert results["formula_B"]["error"] < 1e-6


def test_formula_A_digits_ge_5(results):
    assert results["formula_A"]["digits"] >= 5.0


def test_denom_B_is_1000(results):
    assert results["all_checks"]["denom_B_is_1000"] is True


def test_all_individual_checks(results):
    for name, val in results["all_checks"].items():
        assert val is True, f"Check '{name}' failed"


def test_experiment_value_reasonable(results):
    exp = results["alpha_inv_experiment"]
    assert 137.035 < exp < 137.037


def test_residual_sign_negative(results):
    # experiment < formula_B → residual negative
    assert results["residual"] < 0


def test_vieta_product_check(results):
    assert results["all_checks"]["vieta_product"] is True


def test_vieta_sum_check(results):
    assert results["all_checks"]["vieta_sum"] is True
