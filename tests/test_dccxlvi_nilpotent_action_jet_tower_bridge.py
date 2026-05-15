from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxlvi_nilpotent_action_jet_tower_bridge import build_bridge  # noqa: E402


def _frac(numerator: int, denominator: int = 1) -> dict[str, int]:
    return {"numerator": numerator, "denominator": denominator}


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]

    assert s["state_count"] == 6
    assert s["highest_nonzero_derivative_order"] == 5
    assert s["first_zero_derivative_order"] == 6
    assert s["top_path_fifth_derivative_numerator"] == 3
    assert s["top_path_fifth_derivative_denominator"] == 4
    assert s["all_identities_hold"] is True


def test_top_path_profile_is_exact() -> None:
    payload = build_bridge()

    assert payload["top_path_profile"] == {
        "0": _frac(1, 160),
        "1": _frac(1, 32),
        "2": _frac(1, 8),
        "3": _frac(3, 8),
        "4": _frac(3, 4),
        "5": _frac(3, 4),
        "6": _frac(0),
    }


def test_support_begins_on_order_superdiagonal() -> None:
    payload = build_bridge()
    third_jet = payload["jet_tower_at_z1"]["3"]
    sixth_jet = payload["jet_tower_at_z1"]["6"]

    assert third_jet[0][1] == _frac(0)
    assert third_jet[0][2] == _frac(0)
    assert third_jet[0][3] == _frac(1, 4)
    assert third_jet[0][5] == _frac(3, 8)
    assert all(cell == _frac(0) for row in sixth_jet for cell in row)


def test_lower_jets_match_action_variation_and_hessian_samples() -> None:
    payload = build_bridge()
    tower = payload["jet_tower_at_z1"]

    assert tower["0"][0][1] == _frac(1, 2)
    assert tower["0"][0][2] == _frac(1, 8)
    assert tower["0"][0][5] == _frac(1, 160)
    assert tower["1"][0][1] == _frac(1, 2)
    assert tower["1"][0][2] == _frac(1, 4)
    assert tower["1"][0][5] == _frac(1, 32)
    assert tower["2"][0][1] == _frac(0)
    assert tower["2"][0][2] == _frac(1, 4)
    assert tower["2"][0][5] == _frac(1, 8)


def test_closed_form_witness_and_bridge_boundary() -> None:
    payload = build_bridge()

    for item in payload["formula_witness"]:
        assert item["entry"] == item["expected"]
    assert all(payload["identities"].values())
    assert "continuum" in payload["bridge_claim"]["conditional_layer"]
