from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "analysis" / "w33_cyclotomic_genus_reciprocal_sheets.py"

spec = importlib.util.spec_from_file_location("w33_cyclotomic_genus_reciprocal_sheets", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def test_reciprocal_live_dual_roots() -> None:
    payload = mod.generate_payload()
    assert payload["checks"]["live_root_is_negative_sheet"]
    assert payload["checks"]["dual_root_is_positive_sheet"]
    assert payload["roots"]["x_minus_exp_gap_beta"] == "2/7"
    assert payload["roots"]["x_plus_exp_gap_beta"] == "7/2"
    assert payload["checks"]["root_variables_are_reciprocal"]


def test_q3_uniqueness_locks() -> None:
    payload = mod.generate_payload()
    assert payload["checks"]["ratio_uniqueness_scanned_q3_to_q14"]
    assert payload["checks"]["nontrivial_gap_factorial_lock"]
    equal_ratio_qs = [item["q"] for item in payload["uniqueness"]["ratio_scan"] if item["equal"]]
    assert equal_ratio_qs == [3]
    nontrivial_gap_qs = [
        item["q"]
        for item in payload["uniqueness"]["gap_factorial_scan"]
        if item["equal"] and item["q"] >= 3
    ]
    assert nontrivial_gap_qs == [3]


def test_now_derivative_pisano_alpha_lock() -> None:
    payload = mod.generate_payload()
    assert payload["checks"]["now_value_is_negative_multiplicity"]
    assert payload["checks"]["heat_trace_now_is_vertex_count"]
    assert payload["now"]["Omega_live_0"] == 15
    assert payload["now"]["Omega_dual_0"] == 15
    assert payload["now"]["Z_0"] == 40
    assert payload["now"]["live_derivative_0"] == -114
    assert payload["now"]["dual_derivative_0"] == -276
    assert payload["now"]["pisano_137"] == 276
    assert payload["checks"]["dual_now_derivative_is_pisano_alpha"]
    assert payload["checks"]["derivatives_center_on_phi3_g"]
    assert payload["checks"]["derivatives_split_by_q4"]


def test_cyclotomic_inputs_are_exact() -> None:
    payload = mod.generate_payload()
    assert payload["checks"]["phi4_is_low_energy_and_pi11"]
    assert payload["checks"]["phi5_is_ihara_square"]
    assert payload["energies"]["E_low"] == 10
    assert payload["energies"]["E_high"] == 16
    assert payload["energies"]["gap"] == 6


def test_all_boolean_checks_verified() -> None:
    payload = mod.generate_payload()
    assert payload["all_verified"]
    assert payload["verified_boolean_checks"] == payload["total_boolean_checks"]
    assert payload["verified_boolean_checks"] >= 14
