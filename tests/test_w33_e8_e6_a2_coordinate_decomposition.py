from __future__ import annotations

from analysis.w33_e8_e6_a2_coordinate_decomposition import (
    e8_e6_a2_coordinate_decomposition_packet,
)


PACKET = e8_e6_a2_coordinate_decomposition_packet()


def test_mccclxxxix_global_decomposition_identity() -> None:
    assert PACKET["decomposition_identity"] == "240 = 72_E6 + 6_A2 + 81 + 81"
    assert PACKET["n_verified"] == 5
    assert all(PACKET["checks"].values())


def test_mccclxxxix_each_coordinate_sector_counts() -> None:
    expected = {
        "E6_zero_coordinate_roots": 72,
        "A2_coordinate_roots": 6,
        "matter_81_coset_1": 81,
        "matter_81_coset_2": 81,
    }

    for report in PACKET["coordinate_reports"]:
        assert report["sector_counts"] == expected
        assert report["n_verified"] == 10
        assert all(report["checks"].values())


def test_mccclxxxix_e6_a2_subsystems() -> None:
    for report in PACKET["coordinate_reports"]:
        assert report["sector_ranks"]["E6_zero_coordinate_roots"] == 6
        assert report["sector_ranks"]["A2_coordinate_roots"] == 2
        assert report["E6_zero_coordinate"]["norm_profile"] == {"2": 72}
        assert report["E6_zero_coordinate"]["representative_local_profile"] == {
            "-1": 20,
            "-2": 1,
            "0": 30,
            "1": 20,
            "2": 1,
        }
        assert report["E6_zero_coordinate"]["unique_local_profile_count"] == 1
        assert report["E6_zero_coordinate"]["reflection_closure_failures"] == 0
        assert report["A2_coordinate"]["orthogonality_to_E6_max"] == "0"


def test_mccclxxxix_conjugate_81_sectors() -> None:
    for report in PACKET["coordinate_reports"]:
        matter = report["matter"]

        assert matter["coset_1_count"] == 81
        assert matter["coset_2_count"] == 81
        assert matter["coset_1_rank"] == 8
        assert matter["coset_2_rank"] == 8
        assert matter["coset_2_is_negative_of_coset_1"] is True


def test_mccclxxxix_reading_boundary() -> None:
    assert "canonical E8 -> E6 x A2 split" in PACKET["reading"]
    assert "finite root-system decomposition theorem" in PACKET["claim_boundary"]
