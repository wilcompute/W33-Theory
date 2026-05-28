from __future__ import annotations

from analysis.w33_spread_double_six_association_scheme import (
    spread_double_six_association_packet,
)


PACKET = spread_double_six_association_packet()


def test_mcccxciii_global_scheme_identity() -> None:
    assert (
        PACKET["scheme_identity"]
        == "36 W33 spreads and 36 E6 double-sixes share the same two-class SRG scheme"
    )
    assert PACKET["n_verified"] == 4
    assert all(PACKET["checks"].values())


def test_mcccxciii_spread_scheme() -> None:
    spread = PACKET["spread_report"]

    assert spread["n_verified"] == 6
    assert all(spread["checks"].values())
    assert spread["spread_count"] == 36
    assert spread["spread_size_profile"] == {"10": 36}
    assert spread["line_participation_profile"] == {"9": 40}
    assert spread["overlap_profile"] == {"1": 360, "4": 270}
    assert spread["overlap_4_graph"]["degree_profile"] == {"15": 36}
    assert spread["overlap_1_graph"]["degree_profile"] == {"20": 36}


def test_mcccxciii_double_six_schemes() -> None:
    for report in PACKET["double_six_reports"]:
        assert report["n_verified"] == 6
        assert all(report["checks"].values())
        assert report["double_six_count"] == 36
        assert report["double_six_size_profile"] == {"12": 36}
        assert report["weight_participation_profile"] == {"16": 27}
        assert report["overlap_profile"] == {"4": 270, "6": 360}


def test_mcccxciii_matching_srg_parameters() -> None:
    spread = PACKET["spread_report"]

    for report in PACKET["double_six_reports"]:
        assert report["overlap_4_graph"]["degree_profile"] == spread["overlap_4_graph"]["degree_profile"]
        assert (
            report["overlap_4_graph"]["adjacent_common_neighbor_profile"]
            == spread["overlap_4_graph"]["adjacent_common_neighbor_profile"]
        )
        assert (
            report["overlap_4_graph"]["nonadjacent_common_neighbor_profile"]
            == spread["overlap_4_graph"]["nonadjacent_common_neighbor_profile"]
        )
        assert report["overlap_6_graph"]["degree_profile"] == spread["overlap_1_graph"]["degree_profile"]


def test_mcccxciii_boundary_keeps_bijection_open() -> None:
    assert "canonical spread-to-double-six bijection" in PACKET["claim_boundary"]
    assert "canonical bijection question open" in PACKET["reading"]
