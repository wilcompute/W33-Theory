import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def test_4640_degree27_schlaefli():
    d = load("PART_W33_PASS4640_DEGREE27_SCHLAEFLI_CARRIER.json")
    assert d["group_order"] == 25920
    assert d["point_stabilizer_order"] == 960
    assert d["subdegrees"] == [1, 10, 16]
    assert d["degree16_orbital_graph"]["parameters"] == "SRG(27,16,10,8)"
    assert d["degree16_orbital_graph"]["spectrum"] == {"-2": 20, "16": 1, "4": 6}


def test_4641_split_octonion_triality_normalizer():
    d = load("PART_W33_PASS4641_SPLIT_OCTONION_TRIALITY_NORMALIZER.json")
    t = d["explicit_triality"]
    assert t["norm_multiplicative_exhaustive_pairs"] == 65536
    assert (t["nonzero_singular_vectors"], t["left_annihilators"], t["right_annihilators"]) == (135, 135, 135)
    assert t["incidence_failures"] == {
        "left_right_to_right_point": 0,
        "point_left_to_left_right": 0,
        "point_right_to_left_point": 0,
    }
    n = d["type_preserving_normalizer"]
    assert n["PSp_centralizer"] == "C3"
    assert n["order"] == 155520
    assert n["quotient_by_PSp"] == "S3"


def test_4642_selected_line_smith_and_correction():
    d = load("PART_W33_PASS4642_SELECTED_LINE_SMITH_COHERENT.json")
    i = d["incidence"]
    assert (i["rank_Q"], i["rank_F2"]) == (120, 119)
    assert i["smith_nonzero_profile"] == {"1": 119, "2": 1}
    assert i["smith_zero_count"] == 15
    assert d["PSp_coherent_configuration"]["rank"] == 9
    s = d["corrected_selected_line_graph_spectrum"]
    assert s == {"-3": 150, "0": 24, "15": 1, "3": 60, "6": 20, "9": 15}
    assert sum(s.values()) == 270
    old = load("PART_W33_PASS4589_APARTMENT_SELECTED_SINGULAR_GRAPH.json")
    assert old["selected_line_intersection_graph"]["spectrum"]["-3"] == 150


def test_4643_three_spread_sheets():
    d = load("PART_W33_PASS4643_THREE_SPREAD_SHEETS.json")
    s = d["spread_carrier"]
    assert s["W33_spreads"] == 36
    assert s["degree36_half_spinor_orbits"] == 3
    assert s["representative_stabilizer_order"] == 720
    assert s["fixed_spreads_per_representative_stabilizer"] == 1
    assert d["sheet_symmetry"]["combined_ambient_type_preserving_quotient"] == "S3"


def test_4644_routing_falsifier():
    d = load("PART_W33_PASS4644_HOLONET_ROUTING_FALSIFIER.json")
    p = d["selected_point_router"]
    l = d["selected_line_router"]
    assert (p["vertices"], p["degree"], p["diameter"], p["vertex_connectivity"]) == (135, 12, 3, 12)
    assert (l["vertices"], l["degree"], l["diameter"], l["vertex_connectivity"]) == (270, 15, 3, 15)
    assert l["spectrum"]["-3"] == 150


def test_4645_flat_triality_fourier_holonomy():
    d = load("PART_W33_PASS4645_TRIALITY_FOURIER_HOLONOMY.json")
    assert d["centered_triality"]["rank_Q"] == 50
    assert d["three_cycle"]["P"] == "U_BP U_AB U_PA=E_P"
    assert d["three_cycle"]["holonomy"] == "identity on the active 50-dimensional constituent"


def test_4646_triple_double_six_weld():
    d = load("PART_W33_PASS4646_TRIPLE_DOUBLE_SIX_WELD.json")
    p = d["per_sheet"]
    assert (p["shape"], p["row_sum"], p["column_sum"], p["rank_Q"]) == ([27, 36], 16, 12, 21)
    c = d["three_sheet_collapse"]
    assert c["R1_equals_R2_equals_R3"] is True
    assert c["stacked_rank_Q"] == 21
    assert c["sheet_difference_kernel_dimension"] == 72
    assert c["total_kernel_dimension"] == 87


def test_4647_apartment_d12_cover():
    d = load("PART_W33_PASS4647_APARTMENT_D12_HOLONOMY.json")
    h = d["homogeneous_cover"]
    assert (h["apartments"], h["selected_lines"], h["fiber_size"]) == (1620, 270, 6)
    m = d["local_monodromy"]
    assert (m["core_kernel_order"], m["image_order"], m["image_isomorphism"]) == (8, 12, "D12")
    assert m["element_order_census"] == {"1": 1, "2": 7, "3": 2, "6": 2}
    b = d["flag_block_system"]
    assert (b["blocks"], b["sheets_per_block"], b["quotient_image"], b["quotient_order"]) == (3, 2, "S3", 6)
    assert b["kernel_in_D12"] == "central C2 half-turn"
