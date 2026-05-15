from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxlvii_nilpotent_ward_recursion_bridge import build_bridge  # noqa: E402


def _frac(numerator: int, denominator: int = 1) -> dict[str, int]:
    return {"numerator": numerator, "denominator": denominator}


def _all_zero(matrix: list[list[dict[str, int]]]) -> bool:
    return all(cell == _frac(0) for row in matrix for cell in row)


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]

    assert s["state_count"] == 6
    assert s["ward_orders_checked"] == 6
    assert s["first_source_numerator"] == 1
    assert s["first_source_denominator"] == 2
    assert s["terminal_source_is_zero"] is True
    assert s["left_and_right_constraints_hold"] is True
    assert s["all_identities_hold"] is True


def test_left_and_right_ward_residuals_vanish() -> None:
    payload = build_bridge()

    for order in range(1, 7):
        assert _all_zero(payload["left_residuals"][str(order)])
        assert _all_zero(payload["right_residuals"][str(order)])


def test_first_source_and_higher_source_samples() -> None:
    payload = build_bridge()
    left = payload["left_sources"]
    right = payload["right_sources"]

    assert left["1"][0][1] == _frac(1, 2)
    assert left["1"][0][2] == _frac(0)
    assert left["2"][0][2] == _frac(1, 4)
    assert left["3"][0][3] == _frac(1, 4)
    assert left["5"][0][5] == _frac(3, 4)
    assert left["6"][0][5] == _frac(0)
    assert right == left


def test_generator_commutes_with_every_jet() -> None:
    payload = build_bridge()

    for order in range(0, 7):
        assert _all_zero(payload["generator_commutators"][str(order)])


def test_all_identities_hold_and_boundary_is_explicit() -> None:
    payload = build_bridge()

    assert all(payload["identities"].values())
    assert "continuum" in payload["bridge_claim"]["conditional_layer"]
