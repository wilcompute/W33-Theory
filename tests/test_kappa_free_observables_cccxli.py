"""Regression tests for PART CCCXLI kappa-free observable consistency compiler."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCXLI_KAPPA_FREE_OBSERVABLES.py"


def load_module():
    spec = importlib.util.spec_from_file_location("kappa_free_cccxli", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_all_kappa_free_checks_pass():
    mod = load_module()
    results = mod.build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"]
    assert results["checks_total"] >= 12


def test_all_channels_recover_same_lambda():
    mod = load_module()
    Lambda = mod.Lambda_from_kappa(7.0 / 3.0)
    channels = mod.channels_from_Lambda(Lambda)
    recovered = mod.recover_all_Lambdas(channels)
    for value in recovered.values():
        assert abs(value - Lambda) < 1e-9
    assert mod.consistency_report(recovered)["consistent"] is True


def test_corrupted_channel_fails_lambda_consistency():
    mod = load_module()
    Lambda = mod.Lambda_from_kappa(7.0 / 3.0)
    channels = mod.channels_from_Lambda(Lambda)
    corrupted = mod.corrupt_channel(channels, "heat_trace", 1.01)
    report = mod.consistency_report(mod.recover_all_Lambdas(corrupted))
    assert report["consistent"] is False


def test_kappa_recovered_after_lambda():
    mod = load_module()
    kappa = 7.0 / 3.0
    Lambda = mod.Lambda_from_kappa(kappa)
    assert abs(mod.kappa_from_Lambda(Lambda) - kappa) < 1e-12


def test_one_anchor_predictions_recover_lambda():
    mod = load_module()
    Lambda = mod.Lambda_from_kappa(7.0 / 3.0)
    channels = mod.channels_from_Lambda(Lambda)
    for key in ["mass", "heat_trace", "spinor_trace", "resolvent_trace", "zeta"]:
        predictions = mod.kappa_free_predictions_from_one_channel(key, channels[key])
        assert abs(predictions["Lambda"] - Lambda) < 1e-9


def test_result_payload_lambda_layer():
    mod = load_module()
    results = mod.build_results()
    assert results["kappa_free_scale"]["symbol"] == "Lambda"
    assert results["channel_formulas"]["resolvent_trace"] == "Lambda=s^2-2s/R"
    assert results["consistency_report"]["consistent"] is True
    assert results["corrupted_report"]["consistent"] is False
