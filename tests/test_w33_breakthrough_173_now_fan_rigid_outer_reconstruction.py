from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_173_now_fan_rigid_outer_reconstruction import (  # noqa: E402
    now_fan_rigid_outer_reconstruction_packet,
)


PACKET = now_fan_rigid_outer_reconstruction_packet()


def test_bt173_now_fan_signature_classes() -> None:
    assert PACKET["signature_class_size_distribution"] == {1: 7, 2: 7, 4: 6}
    assert len(PACKET["singleton_classes"]) == 7
    assert len(PACKET["forced_pairs"]) == 7
    assert len(PACKET["four_cells"]) == 6


def test_bt173_matching_search_is_64_to_1() -> None:
    assert PACKET["four_cell_option_counts"] == [2, 2, 2, 2, 2, 2]
    assert PACKET["candidate_count"] == 64
    assert PACKET["valid_candidate_count"] == 1


def test_bt173_recovered_outer_matches_bt171() -> None:
    assert PACKET["recovered_outer_zero_based"] == PACKET["known_outer_zero_based"]
    assert PACKET["recovered_cycle_distribution"] == {1: 7, 2: 19}


def test_bt173_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 11
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt173_now_fan_signature_classes()
    test_bt173_matching_search_is_64_to_1()
    test_bt173_recovered_outer_matches_bt171()
    test_bt173_all_checks_pass()
