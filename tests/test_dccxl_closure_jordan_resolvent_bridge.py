from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxl_closure_jordan_resolvent_bridge import build_bridge


def _frac(cell: dict[str, int]) -> tuple[int, int]:
    return cell["numerator"], cell["denominator"]


def test_dccxl_summary_is_unipotent_six_level_resolvent() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["causal_class_count"] == 6
    assert summary["nilpotent_index"] == 6
    assert summary["resolvent_trace"] == 6
    assert summary["resolvent_determinant"] == 1
    assert summary["all_identities_hold"] is True


def test_dccxl_propagator_matrix_matches_two_power_decay() -> None:
    propagator = build_bridge()["matrices"]["propagator"]

    assert _frac(propagator[0][0]) == (1, 1)
    assert _frac(propagator[0][1]) == (1, 2)
    assert _frac(propagator[0][5]) == (1, 32)
    assert _frac(propagator[4][5]) == (1, 2)
    assert _frac(propagator[5][0]) == (0, 1)


def test_dccxl_nilpotent_generator_is_half_shift() -> None:
    generator = build_bridge()["matrices"]["nilpotent_generator"]

    for i in range(5):
        assert _frac(generator[i][i + 1]) == (1, 2)
    assert all(_frac(generator[i][i]) == (0, 1) for i in range(6))
    assert _frac(generator[0][2]) == (0, 1)


def test_dccxl_log_generator_first_superdiagonal_is_half() -> None:
    log_generator = build_bridge()["matrices"]["log_generator"]

    for i in range(5):
        assert _frac(log_generator[i][i + 1]) == (1, 2)
    assert _frac(log_generator[0][2]) == (1, 8)


def test_dccxl_jordan_read_links_to_holonomy_frontier() -> None:
    payload = build_bridge()
    jordan = payload["jordan_read"]

    assert jordan["eigenvalues"] == ["1"] * 6
    assert jordan["minimal_polynomial"] == "(x - 1)^6 for K; x^6 for K-I and N"
    assert "nilpotent holonomy frontier" in jordan["holonomy_link"]
    assert all(payload["identities"].values())


def test_dccxl_markdown_and_boundary_are_present() -> None:
    payload = build_bridge()
    text = (ROOT / "PART_DCCXL_CLOSURE_JORDAN_RESOLVENT_BRIDGE.md").read_text(
        encoding="utf-8"
    )

    assert "K = (I - N)^(-1)" in text
    assert "N^6 = 0" in text
    assert "does not identify the finite unipotent chain" in payload["honesty_boundary"]
