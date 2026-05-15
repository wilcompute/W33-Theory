from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxlviii_retarded_green_uniqueness_bridge import build_bridge  # noqa: E402


def _frac(numerator: int, denominator: int = 1) -> dict[str, int]:
    return {"numerator": numerator, "denominator": denominator}


def _all_zero(matrix: list[list[dict[str, int]]]) -> bool:
    return all(cell == _frac(0) for row in matrix for cell in row)


def test_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]

    assert s["state_count"] == 6
    assert s["solved_ward_orders"] == 6
    assert s["retarded_inverse_top_numerator"] == 1
    assert s["retarded_inverse_top_denominator"] == 32
    assert s["terminal_solution_is_zero"] is True
    assert s["no_homogeneous_branch"] is True
    assert s["all_identities_hold"] is True


def test_retarded_green_is_two_sided_inverse() -> None:
    payload = build_bridge()

    for i in range(6):
        for j in range(6):
            expected = _frac(1 if i == j else 0)
            assert payload["left_inverse_check"][i][j] == expected
            assert payload["right_inverse_check"][i][j] == expected


def test_green_solutions_recover_ward_jets() -> None:
    payload = build_bridge()

    for order in range(1, 7):
        assert _all_zero(payload["left_solution_residuals"][str(order)])
        assert _all_zero(payload["right_solution_residuals"][str(order)])


def test_solution_samples_capture_strict_part_and_terminal_zero() -> None:
    payload = build_bridge()
    left = payload["left_green_solutions"]
    right = payload["right_green_solutions"]

    assert left["1"][0][1] == _frac(1, 2)
    assert left["1"][0][5] == _frac(1, 32)
    assert left["5"][0][5] == _frac(3, 4)
    assert _all_zero(left["6"])
    assert right == left


def test_all_identities_hold_and_boundary_is_explicit() -> None:
    payload = build_bridge()

    assert all(payload["identities"].values())
    assert "continuum" in payload["bridge_claim"]["conditional_layer"]
