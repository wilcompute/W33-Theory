from __future__ import annotations

from analysis.w33_golden_ordered_d4_torsor import (
    golden_ordered_d4_torsor_packet,
)


PACKET = golden_ordered_d4_torsor_packet()


def test_mmccclxxiii_all_checks_verify() -> None:
    assert PACKET["part"] == "MMCCCLXXIII"
    assert PACKET["n_verified"] == 12
    assert all(PACKET["checks"].values())


def test_mmccclxxiii_counts_are_product() -> None:
    assert PACKET["ordered_failure_count"] == 864
    assert PACKET["unique_support_count"] == 108
    assert PACKET["product_identity"]["ordered"] == "K2,2_edges * B27 * D4 = 4*27*8 = 864"


def test_mmccclxxiii_orientation_labels_are_balanced() -> None:
    assert len(PACKET["orientation_labels"]) == 8
    assert set(PACKET["orientation_count_profile"].values()) == {108}


def test_mmccclxxiii_pair_and_bridge_profiles() -> None:
    assert PACKET["pair_count_profile"] == {
        "0-2": 216,
        "0-3": 216,
        "1-2": 216,
        "1-3": 216,
    }
    assert set(PACKET["bridge_count_profile"].values()) == {32}
    assert len(PACKET["bridge_count_profile"]) == 27
    assert PACKET["support_orientation_profile"] == {"8": 108}


def test_mmccclxxiii_boundary_keeps_next_target_open() -> None:
    assert "dihedral lift" in PACKET["reading"]
    assert "does not identify these ordered product coordinates" in PACKET["claim_boundary"]
