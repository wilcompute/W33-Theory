"""Regression tests for PART CCCXXXIX multi-anchor consistency compiler."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCXXXIX_MULTI_ANCHOR_CONSISTENCY.py"


def load_module():
    spec = importlib.util.spec_from_file_location("multi_anchor_cccxxxix", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_all_multi_anchor_checks_pass():
    mod = load_module()
    results = mod.build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"]
    assert results["checks_total"] >= 11


def test_consistent_packet_recovers_all_kappas():
    mod = load_module()
    kappa = 7.0 / 3.0
    packet = mod.make_anchor_packet(kappa)
    kappas = mod.recover_kappas(packet)
    for value in kappas.values():
        assert abs(value - kappa) < 1e-12
    assert mod.consistency_report(kappas)["consistent"] is True


def test_corrupted_packet_fails_consistency():
    mod = load_module()
    bad_packet = mod.make_inconsistent_packet(7.0 / 3.0)
    bad_report = mod.consistency_report(mod.recover_kappas(bad_packet))
    assert bad_report["consistent"] is False
    assert bad_report["max_abs_deviation"] > bad_report["tolerance"]


def test_calibration_invariants():
    mod = load_module()
    ratios = mod.dimensionless_ratios(7.0 / 3.0)
    ratios_unit = mod.dimensionless_ratios(1.0)
    assert abs(ratios["projective_gap_over_mass"] - 2.0) < 1e-12
    assert abs(ratios["M_phys_squared_over_kappa_squared"] - ratios_unit["M_phys_squared_over_kappa_squared"]) < 1e-12
    assert abs(ratios["zeta_p2_scaled_back"] - ratios_unit["zeta_p2_scaled_back"]) < 1e-18


def test_result_payload_falsifiability_layer():
    mod = load_module()
    results = mod.build_results()
    assert results["consistency_report"]["consistent"] is True
    assert results["inconsistent_report"]["consistent"] is False
    assert results["anchor_formulas"]["mass"] == "kappa=M_phys/M"
    assert "falsifiable" in results["architecture_upgrade"]
