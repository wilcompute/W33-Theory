from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_273_selector_phase_clock_atlas import (  # noqa: E402
    selector_phase_clock_atlas_packet,
)


PACKET = selector_phase_clock_atlas_packet()


def test_bt273_phase_factorization() -> None:
    assert PACKET["selector_count"] == 8
    assert PACKET["base_directions"] == [7, 11, 13, 14]
    assert PACKET["base_direction_distribution"] == {7: 2, 11: 2, 13: 2, 14: 2}
    assert PACKET["phase_factorization"] == "8 = mu * lambda = 4 base directions * 2 orientations"


def test_bt273_normalized_qfactorial_clocks() -> None:
    assert PACKET["even_parity_class"] == [0, 3, 5, 6, 9, 10, 12, 15]
    assert PACKET["moving_units"] == [3, 5, 6, 9, 10, 12]
    for row in PACKET["selector_rows"]:
        assert row["fixed_points"] == [0, 15]
        assert row["cycle_lengths"] == [1, 1, 6]
        assert len(row["moving_cycle"]) == 6


def test_bt273_orientation_pairs_are_inverses() -> None:
    assert PACKET["orientation_inverse_checks"] == {
        "7": True,
        "11": True,
        "13": True,
        "14": True,
    }
    assert sorted(PACKET["orientation_tables"]) == ["11", "13", "14", "7"]


def test_bt273_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 10
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt273_phase_factorization()
    test_bt273_normalized_qfactorial_clocks()
    test_bt273_orientation_pairs_are_inverses()
    test_bt273_all_checks_pass()
