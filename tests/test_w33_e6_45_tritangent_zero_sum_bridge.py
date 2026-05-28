from __future__ import annotations

from analysis.w33_e6_45_tritangent_zero_sum_bridge import e6_45_tritangent_zero_sum_packet


PACKET = e6_45_tritangent_zero_sum_packet()


def test_mcccxci_global_tritangent_identity() -> None:
    assert PACKET["tritangent_identity"] == "27 E6 weights -> 45 zero-sum triples"
    assert PACKET["n_verified"] == 4
    assert all(PACKET["checks"].values())
    assert len(PACKET["matter_sector_reports"]) == 8


def test_mcccxci_each_sector_has_45_zero_sum_triangles() -> None:
    for report in PACKET["matter_sector_reports"]:
        assert report["weight_count"] == 27
        assert report["edge_count"] == 135
        assert report["triangle_count"] == 45
        assert report["zero_sum_triangle_count"] == 45
        assert report["n_verified"] == 7
        assert all(report["checks"].values())


def test_mcccxci_edge_and_vertex_multiplicities() -> None:
    for report in PACKET["matter_sector_reports"]:
        assert report["edge_triangle_multiplicity_profile"] == {"1": 135}
        assert report["vertex_triangle_multiplicity_profile"] == {"5": 27}


def test_mcccxci_triangle_inner_products() -> None:
    for report in PACKET["matter_sector_reports"]:
        assert report["triangle_inner_product_profile"] == {
            "(Fraction(-2, 3), Fraction(-2, 3), Fraction(-2, 3))": 45
        }


def test_mcccxci_reading_boundary() -> None:
    assert "27 matter weights carry exactly 45 tritangent" in PACKET["reading"]
    assert "without asserting a continuum Yukawa model" in PACKET["claim_boundary"]
