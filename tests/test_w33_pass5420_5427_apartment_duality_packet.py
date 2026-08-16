from pathlib import Path
import json

from analysis.w33_pass5420_5427_apartment_duality_packet import (
    apartment_intersection_formula,
    census_anchor,
    cycle_cut_frame,
    derivative_gallery,
    footprint_bicycle,
    simplex_split,
    unsigned_condition,
)

ROOT = Path(__file__).resolve().parents[1]


def test_q3_cut_frame_regression():
    row = cycle_cut_frame(3)
    assert row["N"] == 160
    assert row["h1"] == 81
    assert row["cut"] == 79
    assert row["cut_inner_products_d0_to_d4"] == [
        "1", "27/79", "-9/79", "3/79", "-1/79"
    ]


def test_allodd_bicycle_bridge_q3_q5():
    q3 = footprint_bicycle(3)
    q5 = footprint_bicycle(5)
    assert q3["footprint_dimension_g"] == 15
    assert q3["bicycle_dimension"] == 29
    assert q5["footprint_dimension_g"] == 65
    assert q5["bicycle_dimension"] == 129


def test_apartment_intersection_formulas_and_independent_anchors():
    assert apartment_intersection_formula(3)["per_apartment_other_intersections"] == {
        "0": 1187, "1": 288, "2": 96, "3": 32, "4": 16
    }
    assert census_anchor(2)["intersection_profile"] == {
        "0": 25, "1": 32, "2": 16, "3": 8, "4": 8
    }
    assert census_anchor(3)["intersection_profile"] == {
        "0": 1187, "1": 288, "2": 96, "3": 32, "4": 16
    }
    assert census_anchor(5)["intersection_profile"] == {
        "0": 69124, "1": 3200, "2": 640, "3": 128, "4": 32
    }


def test_unsigned_condition_and_derivative_gallery():
    q3 = unsigned_condition(3)
    assert q3["lambda_max"] == 648
    assert q3["lambda_min"] == 40
    assert q3["gram_condition_squared_singular_condition"] == "81/5"
    for q in (2, 3, 5, 7, 11):
        d = derivative_gallery(q)
        assert d["finite_difference_q4"] == (q + 1) ** 4 - q**4


def test_simplex_split_q3():
    q3 = simplex_split(3)
    assert q3["N"] == 160
    assert q3["cycle_design_dimension"] == 81
    assert q3["centered_cut_design_dimension"] == 78
    assert q3["simplex_dimension"] == 159


def test_frozen_certificate_and_publication_registration():
    frozen = json.loads((ROOT / "data/PART_W33_PASS5420_5427_APARTMENT_DUALITY_PACKET.json").read_text())
    assert frozen["status"] == "THEOREM_PACKET_SOURCE_COMPLETE"
    manifest = (ROOT / "analysis/W33_CURRENT_FRONTIER_MANIFEST.tex").read_text()
    assert manifest.count("PASS5420_5427_apartment_duality_insert") == 1
    contract = json.loads((ROOT / "data/w33_publication_frontier_contract_v2.json").read_text())
    hits = [x for x in contract["local_public_sections"] if x["token"] == "pass-5420-5427-apartment-duality"]
    assert len(hits) == 1
