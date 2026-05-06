"""Regression tests for PART CCCXXXIV finite spectral action compiler."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from fractions import Fraction


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCXXXIV_FINITE_SPECTRAL_ACTION.py"


def load_module():
    spec = importlib.util.spec_from_file_location("finite_spectral_action_cccxxxiv", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_all_finite_spectral_action_checks_pass():
    mod = load_module()
    results = mod.build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"]
    assert results["checks_total"] >= 12


def test_spectral_determinant_and_resolvent_trace():
    mod = load_module()
    s = Fraction(100, 1)
    assert mod.characteristic_det(s) == s * s - mod.M2
    assert mod.resolvent_trace(s) == Fraction(800, 34951)


def test_zeta_values():
    mod = load_module()
    assert mod.spectral_zeta_g2(1) == Fraction(8, 5049)
    assert mod.spectral_zeta_g2(2) == Fraction(32, 5049 * 5049)


def test_cutoff_action_jump():
    mod = load_module()
    assert mod.spectral_action_cutoff(Fraction(1000, 1)) == 0
    assert mod.spectral_action_cutoff(Fraction(2000, 1)) == 2


def test_result_payload_spectral_layer():
    mod = load_module()
    results = mod.build_results()
    assert results["spectral_identities"]["det_sI_minus_G"] == "s^2 - 5049/4"
    assert results["spectral_identities"]["KG_heat_trace"] == "2 exp(-(5049/4) tau)"
    assert results["sample_values"]["zeta_G2_1"] == "8/5049"
    assert "spectral-action" in results["architecture_upgrade"]
