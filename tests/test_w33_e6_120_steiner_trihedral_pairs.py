from __future__ import annotations

from analysis.w33_e6_120_steiner_trihedral_pairs import (
    e6_120_steiner_trihedral_pairs_packet,
)


PACKET = e6_120_steiner_trihedral_pairs_packet()


def test_mcccxcvi_global_trihedral_pair_identity() -> None:
    assert (
        PACKET["trihedral_pair_identity"]
        == "36 double-sixes + 45 tritangents -> 120 Steiner trihedral pairs"
    )
    assert PACKET["n_verified"] == 5
    assert all(PACKET["checks"].values())
    assert len(PACKET["matter_sector_reports"]) == 8


def test_mcccxcvi_each_sector_has_120_pairs() -> None:
    for report in PACKET["matter_sector_reports"]:
        assert report["n_verified"] == 11
        assert all(report["checks"].values())
        assert report["trihedral_pair_count"] == 120
        assert report["double_six_triple_size_profile"] == {"3": 120}
        assert report["pairwise_double_six_overlap_profile"] == {"(6, 6, 6)": 120}
        assert report["union_size_profile"] == {"18": 120}
        assert report["complement_size_profile"] == {"9": 120}
        assert report["triple_intersection_size_profile"] == {"0": 120}


def test_mcccxcvi_trihedra_partition_structure() -> None:
    for report in PACKET["matter_sector_reports"]:
        assert report["contained_tritangent_count_profile"] == {"6": 120}
        assert report["trihedra_partition_pair_count_profile"] == {"1": 120}


def test_mcccxcvi_incidence_profiles() -> None:
    for report in PACKET["matter_sector_reports"]:
        assert report["weight_participation_profile"] == {"40": 27}
        assert report["tritangent_participation_profile"] == {"16": 45}
        assert report["double_six_participation_profile"] == {"10": 36}
        assert report["double_six_pair_participation_profile"] == {"1": 360}


def test_mcccxcvi_reading_boundary() -> None:
    assert "120 finite Steiner" in PACKET["reading"]
    assert "without claiming a continuum surface equation" in PACKET["claim_boundary"]
