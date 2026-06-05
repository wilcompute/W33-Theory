from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_286_ecube_coordinate_selector_atlas import (  # noqa: E402
    ecube_coordinate_selector_atlas_packet,
)


PACKET = ecube_coordinate_selector_atlas_packet()


def test_bt286_counts_and_stabilizer() -> None:
    assert PACKET["coordinate_conjugate_count"] == 24
    assert PACKET["pair_stabilizer_count"] == 8
    assert PACKET["selector_match_count"] == 8
    assert PACKET["unmatched_count"] == 16


def test_bt286_hits_each_selector_once() -> None:
    assert PACKET["selector_distribution"] == {index: 1 for index in range(8)}
    assert PACKET["selector_pairs_by_pivot"] == {
        "1": [6, 7],
        "2": [4, 5],
        "4": [2, 3],
        "8": [0, 1],
    }


def test_bt286_pivot_to_base_distribution() -> None:
    assert PACKET["pivot_distribution"] == {1: 2, 2: 2, 4: 2, 8: 2}
    assert PACKET["base_distribution"] == {7: 2, 11: 2, 13: 2, 14: 2}
    assert PACKET["unmatched_pivot_distribution"] == {1: 4, 2: 4, 4: 4, 8: 4}


def test_bt286_standard_convention_is_bt285_selector7() -> None:
    standard = [
        row
        for row in PACKET["selector_atlas_rows"]
        if row["coordinate_permutation"] == [1, 2, 4, 8]
    ]
    assert len(standard) == 1
    assert standard[0]["selector_index"] == 7
    assert standard[0]["internal_q_word"] == [5, 3, 9]


def test_bt286_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 13
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt286_counts_and_stabilizer()
    test_bt286_hits_each_selector_once()
    test_bt286_pivot_to_base_distribution()
    test_bt286_standard_convention_is_bt285_selector7()
    test_bt286_all_checks_pass()
