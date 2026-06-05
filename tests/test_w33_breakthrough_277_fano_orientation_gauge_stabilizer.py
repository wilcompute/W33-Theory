from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_277_fano_orientation_gauge_stabilizer import (  # noqa: E402
    fano_orientation_gauge_stabilizer_packet,
)


PACKET = fano_orientation_gauge_stabilizer_packet()


def test_bt277_fano_completion_count() -> None:
    assert PACKET["completion_count"] == 2
    assert len(PACKET["unit_fano_lines"]) == 7
    assert len(PACKET["now_axes"]) == 3
    assert PACKET["peripheral_pairs"] == [(0, 41), (1, 3), (2, 4)]


def test_bt277_orientation_gauge_matches_selector_stabilizer() -> None:
    assert PACKET["orientation_gauge_size"] == 48
    assert PACKET["maps_by_completion"] == {0: 24, 1: 24}


def test_bt277_axis_sequences_are_two_lap_q_sweeps() -> None:
    rows = PACKET["axis_sequence_distribution"]
    assert len(rows) == 6
    assert {row["count"] for row in rows} == {8}
    assert all(
        row["axis_sequence"][:3] == row["axis_sequence"][3:]
        and sorted(row["axis_sequence"][:3]) == [0, 1, 2]
        for row in rows
    )


def test_bt277_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 13
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt277_fano_completion_count()
    test_bt277_orientation_gauge_matches_selector_stabilizer()
    test_bt277_axis_sequences_are_two_lap_q_sweeps()
    test_bt277_all_checks_pass()
