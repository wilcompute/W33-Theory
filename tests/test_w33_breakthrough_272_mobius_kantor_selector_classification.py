from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_272_mobius_kantor_selector_classification import (  # noqa: E402
    mobius_kantor_selector_classification_packet,
)


PACKET = mobius_kantor_selector_classification_packet()


def test_bt272_matching_profile_split() -> None:
    assert PACKET["weight3_complement_edge_count"] == 32
    assert PACKET["perfect_matching_count"] == 272
    assert PACKET["profile_counts"] == {
        "(8, 4)": 4,
        "(16, 4)": 260,
        "(16, 6)": 8,
    }


def test_bt272_mobius_kantor_selector_count_and_profiles() -> None:
    assert PACKET["mobius_kantor_selector_count"] == 8
    assert PACKET["selector_xor_profiles"] == {
        "((7, 2), (11, 2), (13, 2), (14, 2))": 8,
    }
    assert len(PACKET["selector_matchings"]) == 8


def test_bt272_affine_orbit_structure() -> None:
    assert PACKET["affine_coordinate_automorphism_order"] == 384
    assert PACKET["selector_orbit_sizes"] == [8]
    assert PACKET["selector_stabilizer_order"] == 48
    assert PACKET["all_matching_orbit_sizes"] == [4, 8, 12, 24, 32, 48, 48, 96]


def test_bt272_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 10
    assert all(PACKET["checks"].values())


if __name__ == "__main__":
    test_bt272_matching_profile_split()
    test_bt272_mobius_kantor_selector_count_and_profiles()
    test_bt272_affine_orbit_structure()
    test_bt272_all_checks_pass()
