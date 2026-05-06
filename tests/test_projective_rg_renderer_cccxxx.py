"""Regression tests for PART CCCXXX projective RG renderer compiler."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from fractions import Fraction


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCXXX_PROJECTIVE_RG_RENDERER.py"


def load_module():
    spec = importlib.util.spec_from_file_location("projective_rg_cccxxx", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_all_projective_renderer_checks_pass():
    mod = load_module()
    results = mod.build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"]
    assert results["checks_total"] >= 10


def test_generator_invariants():
    mod = load_module()
    assert mod.trace2(mod.G) == 0
    assert mod.det2(mod.G) == Fraction(-5049, 4)
    assert mod.generator_square() == ((Fraction(5049, 4), Fraction(0, 1)), (Fraction(0, 1), Fraction(5049, 4)))


def test_projective_flow_matches_beta():
    mod = load_module()
    y0 = float(mod.B)
    deriv = mod.derivative_numeric(y0, 0.0)
    assert abs(deriv - mod.beta(y0)) < 1e-4


def test_mobius_matrix_is_sl2():
    mod = load_module()
    M = mod.mobius_matrix(0.05)
    det = mod.det_float(M)
    assert abs(det - 1.0) < 1e-12


def test_result_payload_projective_renderer():
    mod = load_module()
    results = mod.build_results()
    assert results["generator"]["square_form"] == "G^2=(5049/4)I"
    assert results["riccati_flow"]["equation"] == "dy/dt = 140 + 67y - y^2"
    assert "cosh" in results["mobius_renderer"]["exp_tG"]
    assert "finite PSL(2)-type action" in results["architecture_upgrade"]
