from __future__ import annotations

import json
import math
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcmlxxxiv_post_burst_forcing_moonshine_audit import (  # noqa: E402
    DATA_PATH,
    RESULT_PATH,
    build_audit,
    write_audit,
)


def test_part_metadata_and_source_anchors_are_pinned() -> None:
    payload = build_audit()
    summary = payload["summary"]
    anchors = payload["source_anchor_checks"]
    ids = payload["identities"]

    assert summary["part"] == "DCMLXXXIV"
    assert summary["decimal"] == 984
    assert summary["ramanujan_root_status"] == (
        "corrected: additive B2 bridge, not multiplicative B2 factor"
    )
    assert summary["johnson_girth_pincer_status"] == "rejected: W33 is not J(40,12)"
    assert anchors == {
        "burst_contains_false_640320_product": True,
        "correction_contains_additive_b2_bridge": True,
        "burst_contains_johnson_girth_claim": True,
        "theta_eta_contains_a2_bridge": True,
        "monster_3b_contains_horizon_jump": True,
    }
    assert ids["part_number_is_984"] is True
    assert ids["source_anchors_present"] is True


def test_false_640320_b2_product_is_rejected_and_corrected() -> None:
    payload = build_audit()
    moonshine = payload["moonshine_640320_boundary"]
    ids = payload["identities"]

    rejected = moonshine["rejected_product"]
    assert rejected["formula"] == "2^7*q^2*5*Phi6*B2"
    assert rejected["value"] == 5_120_640
    assert rejected["target"] == 640_320
    assert rejected["classification"] == "false_multiplicative_b2_claim"

    assert moonshine["correct_prime_factorization"] == {
        2: 6,
        3: 1,
        5: 1,
        23: 1,
        29: 1,
    }
    assert moonshine["correct_edge_factorization"]["value"] == 640_320
    assert moonshine["correct_edge_factorization"]["factors"] == [240, 4, 23, 29]
    assert moonshine["correct_additive_b2_bridge"]["value"] == 640_320
    assert moonshine["correct_additive_b2_bridge"]["factors"] == [math.factorial(7), 127, 240]
    assert ids["wrong_640320_product_is_false"] is True
    assert ids["correct_prime_factorization"] is True
    assert ids["correct_edge_factorization"] is True
    assert ids["correct_additive_b2_bridge"] is True
    assert ids["b2_is_mersenne_heptad"] is True


def test_w33_is_not_johnson_j_40_12_and_girth_pincer_is_rejected() -> None:
    payload = build_audit()
    boundary = payload["johnson_girth_boundary"]
    w33 = boundary["w33_collinearity_graph"]
    johnson = boundary["johnson_J_40_12"]
    ids = payload["identities"]

    assert w33 == {
        "vertices": 40,
        "degree": 12,
        "line_count": 40,
        "line_size": 4,
        "triangles_from_lines": 160,
        "girth": 3,
    }
    assert johnson["vertices"] == math.comb(40, 12)
    assert johnson["degree"] == 336
    assert johnson["triangle_example"]["pairwise_intersections"] == {
        "A_cap_B": 11,
        "A_cap_C": 11,
        "B_cap_C": 11,
    }
    assert johnson["triangle_example"]["is_triangle_in_J_40_12"] is True
    assert boundary["girth_over_two_for_w33"]["text"] == "3/2"
    assert boundary["d_x_from_girth_over_two"] == "not_applicable"
    assert ids["w33_has_40_vertices_and_degree_12"] is True
    assert ids["w33_collinearity_has_triangles"] is True
    assert ids["johnson_j_40_12_not_w33"] is True
    assert ids["johnson_j_40_12_has_triangle_counterexample"] is True
    assert ids["girth_over_two_pincer_rejected"] is True


def test_post_burst_exact_identities_are_preserved() -> None:
    payload = build_audit()
    exact = payload["preserved_exact_identities"]
    ids = payload["identities"]

    monster = exact["monster_3b_level"]
    assert monster["level"] == 108
    assert monster["forms"] == {
        "k*q^2": 108,
        "q*N_M": 108,
        "2*horizon_jump": 108,
    }
    assert monster["q_selected_if_k_and_N_M_fixed"]["text"] == "3/1"

    theta_eta = exact["theta_eta_horizon"]
    assert theta_eta["horizon_jump"] == 54
    assert theta_eta["theta_E8_a2"] == 2160
    assert theta_eta["a2_equals_v_jump"] == 2160
    assert theta_eta["a2_over_jump"]["text"] == "40/1"

    leech = exact["leech_monster_split"]
    assert leech["leech_minimal_vectors"] == 196_560
    assert leech["leech_scaled_from_E8"] == 196_560
    assert leech["monster_c1"] == 196_884
    assert leech["monster_gap"] == 324
    assert leech["gap_form_k_q3"] == 324

    boundary_1823 = exact["prime_1823_boundary"]
    assert boundary_1823["leech_factor"] == 1820
    assert boundary_1823["additive_identity"] == 1823
    assert boundary_1823["factor_1820"] == 1820
    assert "external factor 5" in boundary_1823["classification"]

    assert ids["monster_3b_level_forms_hold"] is True
    assert ids["theta_eta_horizon_bridge_holds"] is True
    assert ids["leech_minimal_vectors_scaled_from_e8"] is True
    assert ids["monster_c1_leech_gap_holds"] is True
    assert ids["prime_1823_additive_boundary"] is True


def test_q3_status_is_preserved_but_not_johnson_proved() -> None:
    payload = build_audit()
    q3 = payload["q3_forcing_status"]

    assert q3["d_x"] == 3
    assert q3["q"] == 3
    assert q3["preserved_exact_sources"] == [
        "CSS/Hamming parameter d_X=q=3",
        "Monster level selector q=N_M/k=36/12 when N_M and k are fixed",
    ]
    assert q3["rejected_source"] == "Johnson graph girth-over-two pincer"
    assert "not a valid independent proof" in q3["classification"]


def test_static_external_sources_are_recorded_offline() -> None:
    payload = build_audit()
    sources = payload["static_external_sources"]
    ids = payload["identities"]

    assert {source["label"] for source in sources} == {
        "MathWorld Johnson Graph",
        "MathWorld Generalized Quadrangle",
        "MathWorld Leech Lattice",
    }
    assert all(source["runtime_dependency"] is False for source in sources)
    assert ids["external_sources_are_static"] is True


def test_write_and_reload() -> None:
    data_path, result_path = write_audit()
    assert data_path == DATA_PATH
    assert result_path == RESULT_PATH

    data = json.loads(data_path.read_text(encoding="utf-8"))
    result = json.loads(result_path.read_text(encoding="utf-8"))
    assert data["summary"]["all_identities_hold"] is True
    assert result["decimal"] == 984
    assert result["status"].startswith("VERIFIED")


def test_public_index_exposes_post_burst_corrective_audit() -> None:
    index = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    compact = " ".join(index.split())

    assert "Post-Burst Forcing/Moonshine Audit" in index
    assert "640320" in index
    assert "not" in compact and "2<sup>7</sup>q<sup>2</sup>5&Phi;<sub>6</sub>B<sub>2</sub>" in compact
    assert "W(3,3) is not the Johnson graph" in compact
    assert "Johnson/girth pincer is rejected" in compact
