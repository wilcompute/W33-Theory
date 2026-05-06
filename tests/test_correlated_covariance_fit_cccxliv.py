"""Regression tests for PART CCCXLIV correlated covariance fit compiler."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCXLIV_CORRELATED_COVARIANCE_FIT.py"


def load_module():
    spec = importlib.util.spec_from_file_location("correlated_covariance_cccxliv", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_all_correlated_covariance_checks_pass():
    mod = load_module()
    results = mod.build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"]
    assert results["checks_total"] >= 11


def test_covariance_propagation_and_fit_clean_packet():
    mod = load_module()
    scale = (7.0 / 3.0) ** 2 * mod.M2_DIMLESS
    packet = mod.channels_from_scale(scale)
    sigmas = mod.default_sigmas(packet)
    cov = mod.make_value_covariance(sigmas, rho=0.25, systematic_fraction=0.35)
    fit = mod.correlated_fit(packet, cov)
    assert mod.covariance_is_symmetric(fit["scale_covariance"], tol=1e-10)
    assert abs(fit["fit"]["weighted_scale"] - scale) < 1e-8
    assert fit["fit"]["passes_reduced_chi_square_lt_3"] is True


def test_bad_packet_fails_correlated_chi_square():
    mod = load_module()
    scale = (7.0 / 3.0) ** 2 * mod.M2_DIMLESS
    packet = mod.channels_from_scale(scale)
    sigmas = mod.default_sigmas(packet)
    cov = mod.make_value_covariance(sigmas, rho=0.25, systematic_fraction=0.35)
    bad = mod.perturb_packet(packet, {"spinor_trace": 150e-6})
    bad_fit = mod.correlated_fit(bad, cov)
    assert bad_fit["fit"]["passes_reduced_chi_square_lt_3"] is False


def test_matrix_inverse_identity():
    mod = load_module()
    packet = mod.channels_from_scale((7.0 / 3.0) ** 2 * mod.M2_DIMLESS)
    sigmas = mod.default_sigmas(packet)
    cov = mod.make_value_covariance(sigmas, rho=0.25, systematic_fraction=0.35)
    fit = mod.correlated_fit(packet, cov)
    scale_cov = fit["scale_covariance"]
    inv = mod.invert_matrix(scale_cov)
    identity_check = [[sum(scale_cov[i][k] * inv[k][j] for k in range(len(mod.CHANNELS))) for j in range(len(mod.CHANNELS))] for i in range(len(mod.CHANNELS))]
    identity = [[1.0 if i == j else 0.0 for j in range(len(mod.CHANNELS))] for i in range(len(mod.CHANNELS))]
    assert mod.max_abs_matrix_diff(identity_check, identity) < 1e-6


def test_result_payload_covariance_layer():
    mod = load_module()
    results = mod.build_results()
    assert results["gls_formulas"]["covariance_propagation"] == "C_X = J C_y J^T"
    assert results["clean_correlated_fit"]["passes_reduced_chi_square_lt_3"] is True
    assert results["small_noisy_correlated_fit"]["passes_reduced_chi_square_lt_3"] is True
    assert results["bad_correlated_fit"]["passes_reduced_chi_square_lt_3"] is False
