"""Regression tests for PART CCCXXXVIII unit map/calibration compiler."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from fractions import Fraction


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCXXXVIII_UNIT_MAP_CALIBRATION.py"


def load_module():
    spec = importlib.util.spec_from_file_location("unit_map_cccxxxviii", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_all_unit_map_checks_pass():
    mod = load_module()
    results = mod.build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"]
    assert results["checks_total"] >= 11


def test_scaled_generator_mass_shell():
    mod = load_module()
    kappa = Fraction(7, 3)
    Gp = mod.scaled_generator(kappa)
    assert mod.matmul(Gp, Gp) == mod.matscale(mod.scaled_mass_squared(kappa), mod.I)
    assert mod.scaled_mass_squared(kappa) == kappa * kappa * mod.M2


def test_resolvent_scaling_law():
    mod = load_module()
    kappa = Fraction(7, 3)
    s_phys = Fraction(100, 1)
    assert mod.resolvent_phys(s_phys, kappa) == mod.scale_resolvent_from_dimless(s_phys, kappa)


def test_heat_spinor_and_zeta_scaling():
    mod = load_module()
    kappa = Fraction(7, 3)
    tau_phys = 0.001
    t_phys = 0.01
    assert abs(mod.heat_trace_phys(tau_phys, float(kappa)) - mod.heat_trace_dimless(float(kappa * kappa) * tau_phys)) < 1e-15
    assert abs(mod.spinor_trace_phys(t_phys, float(kappa)) - mod.spinor_trace_dimless(float(kappa) * t_phys)) < 1e-15
    assert mod.zeta_phys(2, kappa) == mod.zeta_dimless(2) / (kappa ** 4)


def test_projector_invariance_under_unit_map():
    mod = load_module()
    Pp1, Pm1 = mod.branch_projectors_float(1.0)
    Ppk, Pmk = mod.branch_projectors_float(7.0 / 3.0)
    assert mod.max_abs_diff(Pp1, Ppk) < 1e-12
    assert mod.max_abs_diff(Pm1, Pmk) < 1e-12


def test_calibration_recipes_recover_kappa():
    mod = load_module()
    kappa = 7.0 / 3.0
    assert abs(mod.calibrate_kappa_from_mass(kappa * mod.M) - kappa) < 1e-12
    H = mod.heat_trace_phys(0.001, kappa)
    assert abs(mod.calibrate_kappa_from_heat(0.001, H) - kappa) < 1e-12


def test_result_payload_unit_map_layer():
    mod = load_module()
    results = mod.build_results()
    assert results["calibration_constant"]["symbol"] == "kappa"
    assert results["scaling_laws"]["projectors"] == "P_± are invariant under kappa"
    assert results["sample_scaled_sector"]["M_phys_squared"] == "27489/4"
    assert "one calibration constant" in results["theorem"]
