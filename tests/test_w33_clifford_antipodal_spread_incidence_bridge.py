from __future__ import annotations

from analysis.w33_clifford_antipodal_spread_incidence_bridge import (
    clifford_antipodal_spread_incidence_bridge_packet,
)


PACKET = clifford_antipodal_spread_incidence_bridge_packet()


def test_mdclxxxii_global_incidence_identity() -> None:
    assert PACKET["incidence_identity"] == "36*10 = 60*6 = 40*9 = 360"
    assert PACKET["n_verified"] == 6
    assert all(PACKET["checks"].values())


def test_mdclxxxii_clifford_antipodal_design() -> None:
    report = PACKET["clifford_antipodal_report"]
    assert report["n_verified"] == 8
    assert all(report["checks"].values())
    assert report["point_count"] == 60
    assert report["block_count"] == 36
    assert report["block_size_profile"] == {"10": 36}
    assert report["point_replication_profile"] == {"6": 60}
    assert report["incidence_count"] == 360


def test_mdclxxxii_clifford_pair_profiles() -> None:
    report = PACKET["clifford_antipodal_report"]
    assert report["block_intersection_profile"] == {"0": 180, "2": 450}
    assert report["point_pair_cooccurrence_profile"] == {"0": 600, "1": 720, "2": 450}
    assert report["cooccurrence_degree_profiles"] == {
        "0": {"20": 60},
        "1": {"24": 60},
        "2": {"15": 60},
    }


def test_mdclxxxii_w33_line_spread_design() -> None:
    report = PACKET["w33_line_spread_report"]
    assert report["n_verified"] == 8
    assert all(report["checks"].values())
    assert report["point_count"] == 40
    assert report["block_count"] == 36
    assert report["block_size_profile"] == {"10": 36}
    assert report["point_replication_profile"] == {"9": 40}
    assert report["incidence_count"] == 360


def test_mdclxxxii_w33_pair_profiles() -> None:
    report = PACKET["w33_line_spread_report"]
    assert report["block_intersection_profile"] == {"1": 360, "4": 270}
    assert report["point_pair_cooccurrence_profile"] == {"0": 240, "3": 540}
    assert report["cooccurrence_degree_profiles"] == {
        "0": {"12": 40},
        "3": {"27": 40},
    }


def test_mdclxxxii_selector_boundary() -> None:
    assert "incidence-conservation theorem" in PACKET["claim_boundary"]
    assert "does not construct the missing symplectic selector" in PACKET["claim_boundary"]
    assert "60*6 = 40*9 = 36*10 = 360" in PACKET["reading"]
