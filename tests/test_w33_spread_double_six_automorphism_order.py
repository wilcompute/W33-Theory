from __future__ import annotations

from analysis.w33_spread_double_six_automorphism_order import automorphism_order_packet


PACKET = automorphism_order_packet()


def test_mcccxcv_automorphism_order_identity() -> None:
    orbit_stabilizer = PACKET["orbit_stabilizer"]

    assert orbit_stabilizer["identity"] == "51840 = 36 * 1440"
    assert orbit_stabilizer["orbit_size_of_first_spread"] == 36
    assert orbit_stabilizer["stabilizer_order_of_first_spread"] == 1440
    assert orbit_stabilizer["automorphism_order"] == 51840
    assert orbit_stabilizer["factorization"] == {"2": 7, "3": 4, "5": 1}


def test_mcccxcv_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 6
    assert all(PACKET["checks"].values())


def test_mcccxcv_search_witnesses() -> None:
    search = PACKET["search"]

    assert search["stabilizer_search_nodes"] > 0
    assert len(search["first_stabilizer_solution"]) == 36
    assert sorted(search["first_stabilizer_solution"]) == list(range(36))


def test_mcccxcv_boundary_keeps_labeling_open() -> None:
    assert "does not choose a unique canonical spread-to-double-six labeling" in PACKET["claim_boundary"]
    assert "automorphism order 51840" in PACKET["reading"]
