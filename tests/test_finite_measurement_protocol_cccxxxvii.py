"""Regression tests for PART CCCXXXVII finite measurement protocol compiler."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from fractions import Fraction


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCXXXVII_FINITE_MEASUREMENT_PROTOCOL.py"


def load_module():
    spec = importlib.util.spec_from_file_location("finite_measurement_cccxxxvii", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_all_measurement_protocol_checks_pass():
    mod = load_module()
    results = mod.build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"]
    assert results["checks_total"] >= 11


def test_tier_a_recovers_mass_and_weights():
    mod = load_module()
    tier = mod.tier_a_from_moments(mod.moment(0), mod.moment(1), mod.moment(2))
    assert tier["symmetric"] is True
    assert tier["recovered_M2"] == Fraction(5049, 4)
    assert tier["weights_if_symmetric"] == (Fraction(1, 1), Fraction(1, 1))


def test_tier_b_rank_certificate():
    mod = load_module()
    cert = mod.tier_b_certificate()
    assert cert["H2_det"] == Fraction(5049, 1)
    assert cert["H3_det"] == 0
    assert cert["rank_two"] is True
    assert cert["recurrence_m4_equals_M2_m2"] is True


def test_tier_c_response_samples_recover_mass():
    mod = load_module()
    s = Fraction(100, 1)
    R = mod.resolvent_trace(s)
    assert mod.recover_M2_from_resolvent_sample(s, R) == mod.M2
    tau = 0.001
    H = mod.heat_trace(tau)
    assert abs(mod.recover_M2_from_heat_sample(tau, H) - float(mod.M2)) < 1e-9
    t = 0.01
    T = mod.spinor_trace(t)
    assert abs(mod.recover_M_from_spinor_trace(t, T) - mod.M) < 1e-9


def test_tier_d_projectors():
    mod = load_module()
    Pp, Pm = mod.projectors_from_measured_mass()
    assert mod.max_abs(mod.matsub_float(mod.matmul_float(Pp, Pp), Pp)) < 1e-12
    assert mod.max_abs(mod.matsub_float(mod.matmul_float(Pm, Pm), Pm)) < 1e-12
    assert mod.max_abs(mod.matmul_float(Pp, Pm)) < 1e-12


def test_result_payload_observability_layer():
    mod = load_module()
    results = mod.build_results()
    assert results["tier_A_moment_reconstruction"]["recovered_M2"] == "5049/4"
    assert results["tier_B_rank_certificate"]["rank_two"] is True
    assert results["tier_D_projector_reconstruction"]["formula"] == "P_±=(I±G/M)/2"
    assert "observability" in results["architecture_upgrade"]
