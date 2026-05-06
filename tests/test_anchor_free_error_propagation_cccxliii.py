"""Regression tests for PART CCCXLIII anchor-free error propagation compiler."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCXLIII_ANCHOR_FREE_ERROR_PROPAGATION.py"


def load_module():
    spec = importlib.util.spec_from_file_location("anchor_free_error_cccxliii", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_all_error_propagation_checks_pass():
    mod = load_module()
    results = mod.build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"]
    assert results["checks_total"] >= 11


def test_clean_packet_consensus_recovers_scale():
    mod = load_module()
    scale = (7.0 / 3.0) ** 2 * mod.M2_DIMLESS
    packet = mod.channels_from_scale(scale)
    uncertainties = mod.default_uncertainties(packet)
    estimates = mod.all_channel_estimates(packet, uncertainties)
    consensus = mod.weighted_consensus(estimates)
    assert abs(consensus["weighted_scale"] - scale) < 1e-8
    assert consensus["passes_3sigma_channel_test"] is True


def test_noisy_and_bad_packets_classify_correctly():
    mod = load_module()
    scale = (7.0 / 3.0) ** 2 * mod.M2_DIMLESS
    packet = mod.channels_from_scale(scale)
    uncertainties = mod.default_uncertainties(packet)
    noisy = mod.perturb_packet(packet, {"mass": 0.4e-6, "gap": -0.3e-6, "heat_trace": 0.2e-6})
    noisy_consensus = mod.weighted_consensus(mod.all_channel_estimates(noisy, uncertainties))
    assert noisy_consensus["passes_3sigma_channel_test"] is True
    bad = mod.perturb_packet(packet, {"spinor_trace": 100e-6})
    bad_consensus = mod.weighted_consensus(mod.all_channel_estimates(bad, uncertainties))
    assert bad_consensus["passes_3sigma_channel_test"] is False


def test_derivatives_match_finite_difference():
    mod = load_module()
    packet = mod.channels_from_scale((7.0 / 3.0) ** 2 * mod.M2_DIMLESS)
    for name in ["mass", "gap", "heat_trace", "spinor_trace", "resolvent_trace", "zeta"]:
        analytic = mod.derivative_scale_wrt_channel(name, packet[name], packet["samples"])
        numerical = mod.finite_difference_derivative(name, packet[name], packet["samples"])
        denom = max(1.0, abs(analytic))
        assert abs(analytic - numerical) / denom < 1e-6


def test_result_payload_error_layer():
    mod = load_module()
    results = mod.build_results()
    assert results["derivative_formulas"]["mass"] == "dX/dm=2m"
    assert results["clean_consensus"]["passes_3sigma_channel_test"] is True
    assert results["noisy_consensus"]["passes_3sigma_channel_test"] is True
    assert results["bad_consensus"]["passes_3sigma_channel_test"] is False
