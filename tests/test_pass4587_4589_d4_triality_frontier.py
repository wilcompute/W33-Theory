import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


def test_pass4587_triality_algebra_certificate():
    d = load("PART_W33_PASS4587_D4_TRIALITY.json")
    assert d["totally_singular_subspaces"] == {
        "dimension_1": 135,
        "dimension_2": 1575,
        "dimension_3": 2025,
        "dimension_4": 270,
        "maximal_families": [135, 135],
    }
    assert d["cross_incidence"]["row_degree"] == 15
    assert d["cross_incidence"]["centered_rank_Q"] == 50
    assert d["cross_incidence"]["centered_triality"] == "D_PA D_AB = 54 D_PB, cyclically"
    assert d["outer_relation_graph"]["parameters"] == "SRG(135,70,37,35)"


def test_pass4588_apartment_cover_and_no_go_certificate():
    d = load("PART_W33_PASS4588_APARTMENT_TRIALITY_OBSTRUCTION.json")
    a = d["apartment_to_singular_line"]
    assert (a["apartments"], a["selected_singular_lines"]) == (1620, 270)
    assert a["apartments_per_selected_line"] == 6
    assert a["selected_lines_through_each_singular_point"] == 6
    assert a["apartment_lifts_per_point_line_flag"] == 2
    local = d["local_selector_test"]
    assert local["equivariant_bijection"] is False
    assert sorted(local["generator_action_orbits"]) == [1, 2, 3]
    assert local["common_kernel_order"] == 8
    assert local["both_image_orders"] == 12
    assert d["half_spinor_PSp_orbits"] == [27, 36, 36, 36, 135]
    assert d["spread_bridge"]["degree36_half_spinor_orbits"] == 3


def test_pass4589_selected_graph_certificate():
    d = load("PART_W33_PASS4589_APARTMENT_SELECTED_SINGULAR_GRAPH.json")
    inc = d["incidence"]
    assert (inc["points"], inc["selected_lines"]) == (135, 270)
    assert (inc["point_degree"], inc["line_size"]) == (6, 3)
    assert (inc["rank_Q"], inc["rank_F2"]) == (120, 119)
    g = d["point_graph"]
    assert (g["vertices"], g["degree"], g["edges"], g["triangles"]) == (135, 12, 810, 270)
    assert g["triangles_are_exactly_selected_lines"] is True
    assert g["spectrum"] == {"-6": 15, "-3": 24, "0": 60, "3": 20, "6": 15, "12": 1}
    l = d["selected_line_intersection_graph"]
    assert (l["vertices"], l["degree"], l["edges"]) == (270, 15, 2025)
    assert l["spectrum"] == {"-3": 150, "0": 24, "3": 60, "6": 20, "9": 15, "15": 1}
    assert sum(l["spectrum"].values()) == 270


def test_pass4591_rank120_module_no_go():
    d = load("PART_W33_PASS4591_RANK120_ANISOTROPIC_MODULE_NO_GO.json")
    assert d["modules"] == {
        "anisotropic_permutation_degree": 120,
        "selected_line_incidence_rowspace_dimension_Q": 120,
    }
    assert d["shallow_generator_trace_pairs"] == [[3, 3]] * 5
    w = d["separating_element"]
    assert w["order"] == 6
    assert w["selected_incidence_rowspace_character"] == -1
    assert w["anisotropic_permutation_character"] == 3
