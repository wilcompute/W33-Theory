"""Regression tests for PART CCCXXXVI finite spectral measure reconstruction compiler."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from fractions import Fraction


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCXXXVI_FINITE_SPECTRAL_MEASURE_RECONSTRUCTION.py"


def load_module():
    spec = importlib.util.spec_from_file_location("finite_measure_cccxxxvi", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_all_reconstruction_checks_pass():
    mod = load_module()
    results = mod.build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"]
    assert results["checks_total"] >= 13


def test_moment_recurrence_and_minimal_polynomial():
    mod = load_module()
    assert mod.M2 == Fraction(5049, 4)
    assert mod.moment(0) == 2
    assert mod.moment(1) == 0
    assert mod.moment(2) == Fraction(5049, 2)
    assert mod.recurrence_holds()
    assert mod.pade_denominator() == (Fraction(1, 1), Fraction(0, 1), -mod.M2)


def test_hankel_rank_two():
    mod = load_module()
    H2 = mod.hankel(2)
    H3 = mod.hankel(3)
    assert mod.det2(H2) == Fraction(5049, 1)
    assert mod.det3(H3) == 0


def test_reconstructed_weights_and_stieltjes():
    mod = load_module()
    assert mod.reconstruct_weights() == (Fraction(1, 1), Fraction(1, 1))
    coeffs = mod.stieltjes_large_z_coefficients(1)
    assert coeffs[0]["coefficient"] == "2"
    assert coeffs[1]["coefficient"] == "5049/2"


def test_result_payload_measure_layer():
    mod = load_module()
    results = mod.build_results()
    assert results["reconstructed_measure"]["minimal_polynomial"] == "lambda^2 - 5049/4"
    assert results["reconstructed_measure"]["weights"] == ["1", "1"]
    assert results["stieltjes_transform"]["formula"] == "S(z)=2z/(z^2-5049/4)"
    assert "inverse-spectral" in results["architecture_upgrade"]
