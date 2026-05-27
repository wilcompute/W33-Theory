from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "analysis" / "w33_MCCCLXXXIV_measured_derived_constants_substrate.py"

spec = importlib.util.spec_from_file_location("w33_MCCCLXXXIV_measured_derived_constants_substrate", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def test_all_witnesses_match() -> None:
    payload = mod.generate_payload()
    assert payload["all_verified"]
    assert payload["verified"] == payload["total_checks"] == 15
    assert payload["checks"]["all_scaled_integers_match"]


def test_classification_boundary_is_explicit() -> None:
    payload = mod.generate_payload()
    classes = {item["class"] for item in payload["witnesses"]}
    assert classes == {
        "CODATA measured rounded mantissa",
        "conventional exact",
        "SI-derived exact rounded mantissa",
    }
    assert payload["checks"]["not_all_entries_are_measured"]
    assert payload["checks"]["exact_or_derived_entries_present"]
    assert payload["checks"]["rounded_boundary_present"]


def test_claude_hint_constants_verify_with_status() -> None:
    payload = mod.generate_payload()
    by_name = {item["name"]: item for item in payload["witnesses"]}
    assert by_name["Newtonian constant G"]["computed"] == 667430
    assert by_name["standard gravity g0"]["computed"] == 980665
    assert by_name["standard atmosphere"]["computed"] == 101325
    assert by_name["proton mass energy equivalent"]["computed"] == 938272
    assert by_name["Faraday constant"]["computed"] == 9648533


def test_molar_gas_constant_new_factorization() -> None:
    payload = mod.generate_payload()
    by_name = {item["name"]: item for item in payload["witnesses"]}
    assert by_name["molar gas constant"]["computed"] == 8314463
    assert payload["checks"]["gas_constant_factorization"]
    assert payload["checks"]["gas_factor_a"]
    assert payload["checks"]["gas_factor_b"]
    assert payload["checks"]["leff_alpha"]


def test_exponent_witnesses_are_substrate_labeled() -> None:
    payload = mod.generate_payload()
    exponent_text = "\n".join(item["exponent_witness"] for item in payload["witnesses"])
    for token in ["p_Ih", "mu^2", "F5", "q", "mu", "r", "q!"]:
        assert token in exponent_text
