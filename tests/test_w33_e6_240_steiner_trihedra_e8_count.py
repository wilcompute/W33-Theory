from __future__ import annotations

from analysis.w33_e6_240_steiner_trihedra_e8_count import (
    e6_240_steiner_trihedra_e8_count_packet,
)


PACKET = e6_240_steiner_trihedra_e8_count_packet()


def test_mcccxcvii_global_trihedron_identity() -> None:
    assert (
        PACKET["trihedron_identity"]
        == "120 Steiner trihedral pairs -> 240 individual Steiner trihedra"
    )
    assert PACKET["e8_count_resonance"] == "240 = E8 root count = W33 oriented-corner count"
    assert PACKET["n_verified"] == 6
    assert all(PACKET["checks"].values())
    assert len(PACKET["matter_sector_reports"]) == 8


def test_mcccxcvii_each_sector_has_240_trihedra() -> None:
    for report in PACKET["matter_sector_reports"]:
        assert report["n_verified"] == 12
        assert all(report["checks"].values())
        assert report["trihedron_count"] == 240
        assert report["partner_pair_count"] == 120
        assert report["trihedron_size_profile"] == {"3": 240}
        assert report["trihedron_cover_size_profile"] == {"9": 240}


def test_mcccxcvii_partner_pair_structure() -> None:
    for report in PACKET["matter_sector_reports"]:
        assert report["cover_group_size_profile"] == {"2": 120}
        assert report["partner_participation_profile"] == {"1": 240}
        assert report["same_cover_tritangent_overlap_profile"] == {"0": 120}


def test_mcccxcvii_incidence_profiles() -> None:
    for report in PACKET["matter_sector_reports"]:
        assert report["weight_participation_profile"] == {"80": 27}
        assert report["tritangent_participation_profile"] == {"16": 45}


def test_mcccxcvii_overlap_profiles() -> None:
    for report in PACKET["matter_sector_reports"]:
        assert report["trihedron_tritangent_overlap_profile"] == {"0": 23280, "1": 5400}
        assert report["trihedron_weight_intersection_profile"] == {
            "0": 480,
            "2": 12960,
            "3": 8640,
            "5": 6480,
            "9": 120,
        }


def test_mcccxcvii_reading_boundary() -> None:
    assert "without collapsing the claim into a continuum E8 identification" in PACKET["reading"]
    assert "finite E6 cubic-surface incidence theorem" in PACKET["claim_boundary"]
