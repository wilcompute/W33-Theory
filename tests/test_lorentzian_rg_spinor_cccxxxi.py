"""Regression tests for PART CCCXXXI Lorentzian RG spinor compiler."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from fractions import Fraction


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCXXXI_LORENTZIAN_RG_SPINOR.py"


def load_module():
    spec = importlib.util.spec_from_file_location("lorentzian_rg_cccxxxi", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_all_lorentzian_rg_spinor_checks_pass():
    mod = load_module()
    results = mod.build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"]
    assert results["checks_total"] >= 15


def test_sl2_basis_and_generator_decomposition():
    mod = load_module()
    assert mod.trace(mod.G) == 0
    assert mod.commutator(mod.H, mod.E) == mod.matscale(Fraction(2, 1), mod.E)
    assert mod.commutator(mod.H, mod.F) == mod.matscale(Fraction(-2, 1), mod.F)
    assert mod.commutator(mod.E, mod.F) == mod.H
    reconstructed = mod.matadd(
        mod.matadd(mod.matscale(Fraction(mod.B, 2), mod.H), mod.matscale(Fraction(mod.A, 1), mod.E)),
        mod.F,
    )
    assert reconstructed == mod.G


def test_lorentzian_vector_norm():
    mod = load_module()
    assert (mod.Z, mod.X, mod.Y) == (Fraction(67, 2), Fraction(141, 2), Fraction(139, 2))
    assert mod.NORM == Fraction(5049, 4)
    assert mod.reconstruct_from_lorentz() == mod.G


def test_normalized_involution_and_projectors():
    mod = load_module()
    J = mod.normalized_involution()
    J2 = mod.matmul_float(J, J)
    assert mod.max_abs_entry(mod.matsub_float(J2, mod.identity_float())) < 1e-12
    P_plus, P_minus = mod.branch_projectors()
    assert mod.max_abs_entry(mod.matsub_float(mod.matmul_float(P_plus, P_plus), P_plus)) < 1e-12
    assert mod.max_abs_entry(mod.matsub_float(mod.matmul_float(P_minus, P_minus), P_minus)) < 1e-12
    assert mod.max_abs_entry(mod.matmul_float(P_plus, P_minus)) < 1e-12
    assert mod.max_abs_entry(mod.matsub_float(mod.matadd_float(P_plus, P_minus), mod.identity_float())) < 1e-12


def test_result_payload_spinor_layer():
    mod = load_module()
    results = mod.build_results()
    assert results["sl2_generator"]["decomposition"] == "G=(67/2)H + 140E + F"
    assert results["lorentzian_vector"]["norm"] == "5049/4"
    assert results["clifford_branching"]["normalized_involution"] == "J=(2/sqrt(5049))G, J^2=I"
    assert "Lorentzian spinor" in results["architecture_upgrade"]
