from __future__ import annotations

from analysis.w33_spread_double_six_scheme_isomorphism import (
    spread_double_six_scheme_isomorphism_packet,
)


PACKET = spread_double_six_scheme_isomorphism_packet()


def test_mcccxciv_global_isomorphism_identity() -> None:
    assert (
        PACKET["isomorphism_identity"]
        == "spread overlap 4 <-> double-six overlap 4; spread overlap 1 <-> double-six overlap 6"
    )
    assert PACKET["n_verified"] == 4
    assert all(PACKET["checks"].values())


def test_mcccxciv_each_report_has_valid_mapping() -> None:
    for report in PACKET["reports"]:
        mapping = report["mapping_spread_index_to_double_six_index"]

        assert report["n_verified"] == 5
        assert all(report["checks"].values())
        assert sorted(mapping) == list(range(36))
        assert report["target_anchor"] == 0
        assert mapping[0] == 0


def test_mcccxciv_overlap_classes_preserved() -> None:
    for report in PACKET["reports"]:
        verification = report["verification"]

        assert verification["relation_failure_count"] == 0
        assert verification["spread_overlap_profile_under_mapping"] == {"1": 360, "4": 270}
        assert verification["target_overlap_profile_under_mapping"] == {"4": 270, "6": 360}


def test_mcccxciv_same_mapping_all_eight_charts() -> None:
    first = PACKET["reports"][0]["mapping_spread_index_to_double_six_index"]

    for report in PACKET["reports"]:
        assert report["mapping_spread_index_to_double_six_index"] == first


def test_mcccxciv_boundary_keeps_canonical_labeling_open() -> None:
    assert "does not prove uniqueness" in PACKET["claim_boundary"]
    assert "canonical labeling problem open" in PACKET["reading"]
