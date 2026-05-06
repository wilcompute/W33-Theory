"""Regression tests for PART CCCXXXIII finite propagator/resolvent compiler."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from fractions import Fraction


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCXXXIII_FINITE_PROPAGATOR_RESOLVENT.py"


def load_module():
    spec = importlib.util.spec_from_file_location("finite_propagator_cccxxxiii", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_all_finite_propagator_checks_pass():
    mod = load_module()
    results = mod.build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"]
    assert results["checks_total"] >= 10


def test_resolvent_identity_exact():
    mod = load_module()
    s = Fraction(100, 1)
    R = mod.resolvent(s)
    assert mod.matmul(mod.sI_minus_G(s), R) == mod.I
    assert mod.matmul(R, mod.sI_minus_G(s)) == mod.I
    assert s * s - mod.M2 == Fraction(34951, 4)


def test_projector_propagator_matches_hyperbolic():
    mod = load_module()
    t = 0.01
    U_hyp = mod.exp_hyperbolic(t)
    U_proj = mod.exp_projector(t)
    assert mod.max_abs_float(mod.matsub_float(U_hyp, U_proj)) < 1e-12


def test_propagator_semigroup():
    mod = load_module()
    U1 = mod.exp_projector(0.01)
    U2 = mod.exp_projector(0.02)
    U12 = mod.exp_projector(0.03)
    assert mod.max_abs_float(mod.matsub_float(mod.matmul_float(U1, U2), U12)) < 1e-10


def test_result_payload_propagator_layer():
    mod = load_module()
    results = mod.build_results()
    assert results["resolvent"]["formula"] == "(sI-G)^(-1)=(sI+G)/(s^2-5049/4)"
    assert results["propagator"]["branch_form"] == "exp(tG)=exp(mt)P_+ + exp(-mt)P_-"
    assert results["mass_shell"]["mass_squared"] == "5049/4"
    assert "Green's-function" in results["architecture_upgrade"]
