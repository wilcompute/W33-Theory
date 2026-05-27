from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "analysis" / "w33_MCCCLXXXV_unit_gauge_witness_boundary.py"

spec = importlib.util.spec_from_file_location("w33_MCCCLXXXV_unit_gauge_witness_boundary", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def test_unit_gauge_boundary_verifies() -> None:
    payload = mod.generate_payload()
    assert payload["all_verified"]
    assert payload["verified"] == payload["total_checks"] == 12


def test_legacy_hint_arithmetic_is_preserved_but_demoted() -> None:
    payload = mod.generate_payload()
    reconciliation = payload["legacy_reconciliation"]
    assert len(reconciliation) == 5
    assert all(item["match"] for item in reconciliation)
    assert all(item["promoted_as_dimensionless_prediction"] is False for item in reconciliation)
    assert [item["strict_computed"] for item in reconciliation] == [
        667430,
        980665,
        101325,
        938272,
        9648533,
    ]


def test_strict_packet_adds_only_molar_gas_constant() -> None:
    payload = mod.generate_payload()
    orbit = payload["unit_gauge_orbit"]
    assert orbit["strict_witness_count"] == 6
    assert orbit["legacy_hint_count"] == 5
    assert orbit["strict_extra_names"] == ["molar gas constant"]
    assert orbit["unit_scaled_decimal_witnesses"] is True
    assert orbit["dimensionless_prediction_layer"] is False
    assert orbit["unsafe_legacy_universal_headline_promoted"] is False


def test_three_status_classes_are_balanced() -> None:
    payload = mod.generate_payload()
    assert payload["unit_gauge_orbit"]["classification_counts"] == {
        "CODATA measured rounded mantissa": 2,
        "SI-derived exact rounded mantissa": 2,
        "conventional exact": 2,
    }
    assert payload["checks"]["measured_entries_are_rounded_not_exact"]
    assert payload["checks"]["conventional_entries_are_exact"]
    assert payload["checks"]["derived_entries_are_exact_but_rounded_display"]


def test_molar_gas_lock_remains_the_strict_extra_bridge() -> None:
    payload = mod.generate_payload()
    assert payload["checks"]["molar_gas_lock_uses_alpha_effective_volume"]
    assert payload["unit_gauge_orbit"]["strict_extra_names"] == ["molar gas constant"]
