"""Regression tests for PART CCCXLV nuisance/systematic parameter fit compiler."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCXLV_NUISANCE_PARAMETER_FIT.py"


def load_module():
    spec = importlib.util.spec_from_file_location("nuisance_fit_cccxlv", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_all_nuisance_checks_pass():
    mod = load_module()
    results = mod.build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"]
    assert results["checks_total"] >= 11


def test_clean_fit_recovers_zero_nuisance():
    mod = load_module()
    scale = (7.0 / 3.0) ** 2 * mod.M2_DIMLESS
    packet = mod.channels_from_scale(scale)
    sigmas = mod.default_sigmas(packet)
    cov = mod.make_value_covariance(sigmas, rho=0.15)
    scale_cov = mod.propagate_covariance(cov, mod.jacobian(packet))
    clean = mod.build_synthetic_scale_fit(scale, scale_cov, theta=0.0)
    assert abs(clean["fit_with_nuisance"]["beta"][0] - scale) < 1e-8
    assert abs(clean["fit_with_nuisance"]["beta"][1]) < 1e-8


def test_systematic_template_is_absorbed():
    mod = load_module()
    scale = (7.0 / 3.0) ** 2 * mod.M2_DIMLESS
    packet = mod.channels_from_scale(scale)
    cov = mod.make_value_covariance(mod.default_sigmas(packet), rho=0.15)
    scale_cov = mod.propagate_covariance(cov, mod.jacobian(packet))
    systematic = mod.build_synthetic_scale_fit(scale, scale_cov, theta=0.02)
    assert systematic["fit_without_nuisance"]["passes_reduced_chi_square_lt_3"] is False
    assert systematic["fit_with_nuisance"]["passes_reduced_chi_square_lt_3"] is True
    assert abs(systematic["fit_with_nuisance"]["beta"][1] - 0.02) < 1e-8


def test_off_template_bad_residual_fails():
    mod = load_module()
    scale = (7.0 / 3.0) ** 2 * mod.M2_DIMLESS
    packet = mod.channels_from_scale(scale)
    cov = mod.make_value_covariance(mod.default_sigmas(packet), rho=0.15)
    scale_cov = mod.propagate_covariance(cov, mod.jacobian(packet))
    bad = mod.build_synthetic_scale_fit(scale, scale_cov, theta=0.02, bad_extra=1.0)
    assert bad["fit_with_nuisance"]["passes_reduced_chi_square_lt_3"] is False


def test_result_payload_nuisance_layer():
    mod = load_module()
    results = mod.build_results()
    assert results["nuisance_model"]["design_matrix"] == "A=[1,b]"
    assert results["systematic_fit"]["fit_with_nuisance"]["passes_reduced_chi_square_lt_3"] is True
    assert results["bad_fit"]["fit_with_nuisance"]["passes_reduced_chi_square_lt_3"] is False
