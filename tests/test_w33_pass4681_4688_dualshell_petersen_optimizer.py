import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def test_4681_dual132_is_protected45():
    d = load("PART_W33_PASS4681_DUAL132_PROTECTED45.json")
    assert d["dual_weight132"]["words"] == 45
    assert d["dual_weight132"]["partition_135"] == "45 x 3"
    assert d["protected45_intertwiner"]["literal_triple_equality_with_Pass4585_4624_singular_fiber_packets"]
    assert d["protected45_intertwiner"]["PSp_stabilizer_order"] == 576
    assert d["protected45_intertwiner"]["PGSp_stabilizer_order"] == 1152
    assert d["incidence_with_dual_weight3"]["pair_graph"] == "SRG(45,12,3,3)"
    assert d["incidence_with_dual_weight3"]["packet_pair_multiplicity"] == 3


def test_4682_complementary_incidence_algebra():
    d = load("PART_W33_PASS4682_COMPLEMENTARY_135X36_ALGEBRA.json")
    assert d["incidences"]["rowwise_intersection"] == 0
    assert d["incidences"]["same_rational_column_space_dimension"] == 36
    assert d["column_gram"]["QtQ"] == "15 I + 3 A36"
    assert d["column_gram"]["MtM"] == "24 I + 6 J"
    assert d["column_gram"]["QtM"] == "6 (J-I-A36)"
    assert d["rank_smith"]["Q4"] == {"Q":36,"F2":29,"F3":36,"F5":36,"smith":{"1":29,"2":6,"4":1}}
    assert d["rank_smith"]["M8"] == {"Q":36,"F2":15,"F3":36,"F5":36,"smith":{"1":15,"2":14,"4":6,"8":1}}
    assert d["rank_smith"]["sum12"] == {"Q":21,"F2":21,"F3":14,"F5":21,"smith":{"1":14,"3":7}}
    assert d["row_gram_algebra"]["joint_multiplicities"] == [1,15,20,99]


def test_4683_voltage_scope_is_fail_closed():
    d = load("PART_W33_PASS4683_VOLTAGE_NORMALIZER_SCOPE.json")
    assert d["cohomology"] == {"dimension":3241,"deck_class_nonzero":True}
    assert d["natural_factor_normalizer"]["inside_PSp_order"] == 1
    assert d["natural_factor_normalizer"]["inside_PGSp_order"] == 2
    assert d["natural_factor_normalizer"]["isomorphism"] == "C2"
    assert d["class_action"]["normalizer_fixes_deck_class"]
    assert not d["scope_obstruction"]["PSp_action_on_fixed_labelled_base"]
    assert d["scope_obstruction"]["PSp_orbit_of_alpha_in_this_H1"] == "not defined"


def test_4684_edge_module_quotients():
    d = load("PART_W33_PASS4684_PETERSEN_EDGE_MODULE_QUOTIENTS.json")
    h, c = d["hot_module"], d["cold_module"]
    assert (h["edges"], h["edge_stabilizer_order"], h["component_quotient"], h["fiber_size"]) == (405,64,27,15)
    assert (c["edges"], c["edge_stabilizer_order"], c["quotient_edges"], c["fiber_size"]) == (1620,16,135,12)
    assert c["quotient_graph"] == "SRG(27,10,1,5)"
    assert c["quotient_edge_to_vertex_incidence_smith"] == "1^26 2^1"
    assert d["vertex_module"]["rational_split_dimensions"] == [1,20,6]


def test_4685_exact_optimizer_breakpoints():
    d = load("PART_W33_PASS4685_MIXED_TECH_PETERSEN_OPTIMIZER.json")
    f = d["exact_path_frontier"]
    assert f["uniform_over_270_sources"]
    assert f["breakpoints"] == [1,1.5,2]
    got = [(v["base_traversals_per_source"],v["shortcut_traversals_per_source"]) for v in f["regions"].values()]
    assert got == [(420,239),(548,111),(620,63),(746,0)]
    s = d["sensitivity_model"]
    assert s["loss_optimal_region"] == "R1_mixed"
    assert s["latency_optimal_region"] == "R0_shortcut_favor"
    assert s["pareto_regions_for_these_anchors"] == ["R0_shortcut_favor","R1_mixed"]


def test_4686_hypergraph_needs_dual3_shell():
    d = load("PART_W33_PASS4686_DUAL132_HYPERGRAPH_SYMMETRY_BREAKING.json")
    h = d["dual132_hypergraph_alone"]
    assert h["structure"] == "45 disjoint 3-sets"
    assert h["automorphism_group"] == "S3 wr S45 = S3^45 : S45"
    assert h["automorphism_order_digits"] == 92
    assert not h["selects_protected_E6_action"]
    a = d["add_dual3_shell"]
    assert a["two_section"] == "SRG(45,12,3,3)"
    assert a["automorphism_group_order"] == 51840
    assert a["identification"] == "PGSp(4,3)"


def test_4687_local_petersen_induction():
    d = load("PART_W33_PASS4687_PETERSEN_INDUCED_A5_S5.json")
    p, q = d["PSp_local"], d["PGSp_local"]
    assert (p["component_stabilizer_order"],p["kernel_on_10_vertices"],p["image_order"],p["image"]) == (960,16,60,"A5")
    assert p["edge_stabilizer_image"] == "V4" and p["edge_stabilizer_upstairs_order"] == 64
    assert (q["component_stabilizer_order"],q["kernel_on_10_vertices"],q["image_order"],q["image"]) == (1920,16,120,"S5")
    assert q["edge_stabilizer_image"] == "D8" and q["edge_stabilizer_upstairs_order"] == 128


def test_4688_voltage_projects_to_distance_three_only():
    d = load("PART_W33_PASS4688_VOLTAGE_ROUTING_PROJECTION_OBSTRUCTION.json")
    p = d["projection_to_selected270"]
    assert p["projected_edges"] == 4050
    assert p["all_selected270_distance"] == 3
    assert p["unique_distance3_pairs"] == 1275
    assert p["pair_multiplicity_profile"] == {"3":1200,"6":75}
    assert p["routing_edge_intersection"] == p["base_edge_hits"] == p["Petersen_shortcut_edge_hits"] == 0
    assert not d["signing_obstruction"]["canonical_direct_routing_signing"]
