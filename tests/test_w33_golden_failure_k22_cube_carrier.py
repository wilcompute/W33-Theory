from __future__ import annotations

from analysis.w33_golden_failure_k22_cube_carrier import (
    golden_failure_k22_cube_carrier_packet,
)


PACKET = golden_failure_k22_cube_carrier_packet()


def test_mmccclxx_all_checks_verify() -> None:
    assert PACKET["part"] == "MMCCCLXX"
    assert PACKET["n_verified"] == 12
    assert all(PACKET["checks"].values())


def test_mmccclxx_anchor_line_and_k22_pairs() -> None:
    assert PACKET["unique_failure_count"] == 108
    assert PACKET["ordered_failure_count"] == 864
    assert PACKET["anchor_line"] == 0
    assert PACKET["anchor_points"] == [0, 1, 2, 3]
    assert PACKET["active_anchor_pairs"] == [[0, 2], [0, 3], [1, 2], [1, 3]]
    assert PACKET["inactive_matching_pairs"] == [[0, 1], [2, 3]]


def test_mmccclxx_each_cross_pair_carries_27() -> None:
    assert PACKET["base_pair_failure_counts"] == {
        "0-2": 27,
        "0-3": 27,
        "1-2": 27,
        "1-3": 27,
    }

    for summary in PACKET["pair_summaries"].values():
        assert summary["failure_count"] == 27
        assert summary["endpoint_line_pair_count"] == 9
        assert summary["endpoint_line_pair_multiplicity_profile"] == {"3": 9}
        assert summary["bridge_line_count"] == 27
        assert summary["bridge_line_multiplicity_profile"] == {"1": 27}


def test_mmccclxx_global_incidence_profiles() -> None:
    assert PACKET["line_incidence_profiles"]["endpoint_lines"] == {"18": 12}
    assert PACKET["line_incidence_profiles"]["bridge_lines"] == {"4": 27}
    assert PACKET["point_incidence_profiles"]["anchor_points"] == {"54": 4}
    assert PACKET["point_incidence_profiles"]["nonanchor_points"] == {"6": 36}


def test_mmccclxx_boundary_is_not_coset_bijection_yet() -> None:
    assert "K2,2 x F3^3" in PACKET["carrier_identity"]["unique"]
    assert "does not yet identify these cubes" in PACKET["claim_boundary"]
