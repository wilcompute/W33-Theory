"""Regression tests for PART CCCXLII anchor-free response identities compiler."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCXLII_ANCHOR_FREE_RESPONSE_IDENTITIES.py"


def load_module():
    spec = importlib.util.spec_from_file_location("anchor_free_cccxlii", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_all_anchor_free_checks_pass():
    mod = load_module()
    results = mod.build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"]
    assert results["checks_total"] >= 15


def test_recovered_scales_agree():
    mod = load_module()
    scale = (7.0 / 3.0) ** 2 * mod.M2_DIMLESS
    packet = mod.channels_from_scale(scale)
    scales = mod.recover_scales(packet)
    for value in scales.values():
        assert abs(value - scale) < 1e-8
    assert mod.scale_report(scales)["consistent"] is True


def test_corrupted_packet_fails():
    mod = load_module()
    packet = mod.channels_from_scale((7.0 / 3.0) ** 2 * mod.M2_DIMLESS)
    corrupted = mod.corrupt_packet(packet, "spinor_trace", 1.001)
    assert mod.scale_report(mod.recover_scales(corrupted))["consistent"] is False


def test_single_channel_predictions():
    mod = load_module()
    scale = (7.0 / 3.0) ** 2 * mod.M2_DIMLESS
    packet = mod.channels_from_scale(scale)
    tau = packet["samples"]["tau"]
    t = packet["samples"]["t"]
    s = packet["samples"]["s"]
    p = packet["samples"]["p"]
    predictors = [
        mod.predict_from_mass(packet["mass"], tau, t, s, p),
        mod.predict_from_gap(packet["gap"], tau, t, s, p),
        mod.predict_from_heat(packet["heat_trace"], tau, t, s, p),
        mod.predict_from_spinor(packet["spinor_trace"], tau, t, s, p),
        mod.predict_from_resolvent(packet["resolvent_trace"], tau, t, s, p),
        mod.predict_from_zeta(packet["zeta"], tau, t, s, p),
    ]
    for pred in predictors:
        assert mod.max_prediction_difference(pred, packet) < 1e-10


def test_result_payload_identity_layer():
    mod = load_module()
    results = mod.build_results()
    assert results["anchor_free_identities"]["gap_mass"] == "gap = 2 mass"
    assert "all_channel_scale" in results["anchor_free_identities"]
    assert results["scale_report"]["consistent"] is True
    assert results["corrupted_report"]["consistent"] is False
