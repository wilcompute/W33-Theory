from __future__ import annotations

from analysis.w33_e6_36_double_six_bridge import e6_36_double_six_packet


PACKET = e6_36_double_six_packet()


def test_mcccxcii_global_double_six_identity() -> None:
    assert PACKET["double_six_identity"] == "27 E6 weights -> 72 six-cliques -> 36 double-sixes"
    assert PACKET["n_verified"] == 5
    assert all(PACKET["checks"].values())
    assert len(PACKET["matter_sector_reports"]) == 8


def test_mcccxcii_each_sector_has_72_six_cliques_and_36_double_sixes() -> None:
    for report in PACKET["matter_sector_reports"]:
        assert report["weight_count"] == 27
        assert report["schlaefli_degree_profile"] == {"16": 27}
        assert report["six_clique_count"] == 72
        assert report["double_six_count"] == 36
        assert report["n_verified"] == 8
        assert all(report["checks"].values())


def test_mcccxcii_row_and_weight_participation() -> None:
    for report in PACKET["matter_sector_reports"]:
        assert report["row_clique_participation_profile"] == {"1": 72}
        assert report["weight_double_six_participation_profile"] == {"16": 27}


def test_mcccxcii_cross_matching_profile() -> None:
    for report in PACKET["matter_sector_reports"]:
        assert report["cross_edge_count_profile"] == {"6": 36}


def test_mcccxcii_reading_boundary() -> None:
    assert "36 double-six layer" in PACKET["reading"]
    assert "finite cubic-surface incidence theorem" in PACKET["claim_boundary"]
