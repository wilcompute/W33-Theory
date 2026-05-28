from __future__ import annotations

from analysis.w33_e6_minuscule_27_a2_phase_factorization import (
    e6_minuscule_27_a2_phase_packet,
)


PACKET = e6_minuscule_27_a2_phase_packet()


def test_mcccxc_global_factorization() -> None:
    assert PACKET["factorization_identity"] == "81 = 27_E6 * 3_A2"
    assert PACKET["n_verified"] == 5
    assert all(PACKET["checks"].values())
    assert len(PACKET["matter_sector_reports"]) == 8


def test_mcccxc_each_sector_is_27_times_3() -> None:
    for report in PACKET["matter_sector_reports"]:
        assert report["matter_root_count"] == 81
        assert report["projected_weight_count"] == 27
        assert report["multiplicity_profile"] == {"3": 27}
        assert report["projected_weight_rank"] == 6
        assert report["projected_weight_norm_profile"] == {"4/3": 27}
        assert report["projected_weight_sum_zero"] is True


def test_mcccxc_e6_minuscule_weight_checks() -> None:
    for report in PACKET["matter_sector_reports"]:
        assert report["projected_weight_gram_square_minus_6_gram_max_residual"] == "0"
        assert report["e6_reflection_closure_failures"] == 0
        assert report["e6_root_pairing_profile"] == {"-1": 432, "0": 1080, "1": 432}
        assert report["n_verified"] == 11
        assert all(report["checks"].values())


def test_mcccxc_schlaefli_graphs() -> None:
    for report in PACKET["matter_sector_reports"]:
        schlaefli = report["schlaefli_graph"]
        complement = report["complement_graph"]

        assert schlaefli["vertices"] == 27
        assert schlaefli["degree_profile"] == {"16": 27}
        assert schlaefli["edge_count"] == 216
        assert schlaefli["adjacent_common_neighbor_profile"] == {"10": 216}
        assert schlaefli["nonadjacent_common_neighbor_profile"] == {"8": 135}

        assert complement["vertices"] == 27
        assert complement["degree_profile"] == {"10": 27}
        assert complement["edge_count"] == 135
        assert complement["adjacent_common_neighbor_profile"] == {"1": 135}
        assert complement["nonadjacent_common_neighbor_profile"] == {"5": 216}


def test_mcccxc_reading_boundary() -> None:
    assert "finite E6 minuscule representation geometry" in PACKET["reading"]
    assert "without asserting a continuum particle spectrum" in PACKET["claim_boundary"]
