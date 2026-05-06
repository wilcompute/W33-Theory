"""Regression tests for PART CCCXXXII finite Dirac factorization compiler."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from fractions import Fraction


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCXXXII_FINITE_DIRAC_FACTORIZATION.py"


def load_module():
    spec = importlib.util.spec_from_file_location("finite_dirac_cccxxxii", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_all_finite_dirac_checks_pass():
    mod = load_module()
    results = mod.build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"]
    assert results["checks_total"] >= 10


def test_generator_square_and_mass_shell():
    mod = load_module()
    assert mod.g_square() == mod.matscale(mod.MASS_SQUARED, mod.I)
    assert mod.MASS_SQUARED == Fraction(5049, 4)
    assert mod.det(mod.G) == -mod.MASS_SQUARED
    assert mod.trace(mod.G) == 0


def test_dirac_factorization_has_no_first_order_term():
    mod = load_module()
    minus_plus = mod.dirac_factor_product(-1, +1)
    plus_minus = mod.dirac_factor_product(+1, -1)
    assert minus_plus["D1"] == mod.ZERO
    assert plus_minus["D1"] == mod.ZERO
    assert minus_plus["constant"] == mod.matscale(Fraction(-1, 1), mod.g_square())
    assert plus_minus["constant"] == mod.matscale(Fraction(-1, 1), mod.g_square())


def test_same_sign_factor_has_first_order_term():
    mod = load_module()
    plus_plus = mod.dirac_factor_product(+1, +1)
    assert plus_plus["D1"] == mod.matscale(Fraction(2, 1), mod.G)


def test_result_payload_dirac_layer():
    mod = load_module()
    results = mod.build_results()
    assert results["finite_dirac_equation"]["first_order"] == "d psi/dt = G psi"
    assert results["finite_klein_gordon_equation"]["mass_squared"] == "5049/4"
    assert results["finite_klein_gordon_equation"]["mass"] == "sqrt(5049)/2"
    assert "Dirac/Klein-Gordon" in results["architecture_upgrade"]
