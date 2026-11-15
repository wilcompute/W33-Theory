"""Direct apartment/octets/E6 tritangent correspondence regression.

Compares to repo's independent Pass1536 octet fixture (NOT merely 45 counts).
"""
import importlib.util
import json
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"analysis"/"toe_20261115_frame45_octet_E6_direct_dictionary.py"
def module():
    s=importlib.util.spec_from_file_location("frame45_new",SRC)
    m=importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

@pytest.fixture(scope="module")
def result():
    return module().reproduce()

def test_exact_45_x_36_components(result):
    assert result["n_frames"]==1620
    assert result["components"]==45 and result["frame_count_per_component"]==36
    assert result["component_isomorphism_verified_all_45"]
    assert result["component_graph"]=="J(4,2) Cartesian-product J(4,2)"
    assert result["component_graph_spectrum"]=={
        "-4":4,"-2":12,"0":9,"2":4,"4":6,"8":1
    }

def test_components_exactly_existing_BT1536_octets(result):
    assert result["component_support_points"]==8
    assert result["component_to_prior_BT1536_octets_exact_set_equality"]
    assert len(result["45_component_supports_in_our_point_indices"])==45
    assert len(set(tuple(x) for x in result["45_component_supports_in_our_point_indices"]))==45

def test_intrinsic_45_graph_srg(result):
    assert result["45_disjoint_support_SRG"]==[45,12,3,3]
    assert result["45_SRG_identity"]=="C^2=9 I+3 J"
    assert result["45_pair_octet_support_intersections"]=={0:270,2:720}

def test_exact_schlafli_27_graph_and_explicit_classical_labeling(result):
    assert result["cubic_27_line_graph_SRG"]==[27,10,1,5]
    actual=set(result["cubic_27_intersection_graph_isomorphism"].values())
    expected={f"a{i}" for i in range(6)}|{f"b{i}" for i in range(6)}
    expected|={f"c{i}{j}" for i in range(6) for j in range(i+1,6)}
    assert actual==expected
    assert result["all_45_explicit_blowup_triads_match"]
    assert result["tritangent_types"]=={"a_i_b_j_c_ij":30,"three_pair_partition":15}

def test_40_points_partition_in_27_five_octet_spreads(result):
    assert result["27_partitions_of_W33_40_points_into_five_disjoint_K44"]
    assert result["point_octet_times_octet_line_incidence"]=="P_40x45 @ T_45x27 = J_40x27"
    assert result["27_line_45_tritangent_incidence_degree"]==[5,3]

def test_no_go_naive_linear_observer_to_E6_matter_transfer(result):
    assert (result["rank_P"],result["rank_T"])==(25,21)
    assert (result["centered_rank_P"],result["centered_rank_T"])==(24,20)
    assert result["centered_transfer_exactly_zero"]
    assert result["45_representation_decomposition"].startswith("1 + 24")
    assert "phase/orientation" in result["naive_linear_observer_to_matter_obstruction"]

def test_reports_existing_prior_art_explicitly(result):
    p=result["prior_art"]
    assert "TOE23" in p and "TOE24" in p
    assert "Pass1536" in p
    assert "not" in result["limitation"] or "no" in result["limitation"]

def test_write_and_read_certificate(result):
    m=module()
    m.OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    s=json.loads(m.OUT.read_text())
    assert s["status"]=="PASS_EXACT_COMPONENT_OCTET_SCHLAFLI_DICTIONARY"
    assert s["centered_transfer_exactly_zero"]


def test_all_order_unweighted_45_hop_no_information_transfer(result):
    assert result["tritangent_graph_on_lines_identity"]=="C_45x45 @ T_45x27 = 3T + J"
    assert result["all_order_disjoint_octet_walk_obstruction"]=="P C^m T = 12^m J for every integer m >= 0"
    assert result["walk_order_range_independently_integer_tested"]==list(range(7))
    assert result["centered_transfer_exactly_zero"]


def test_native_two_point_quadratic_bridge_breaks_linear_obstruction(result):
    assert result["two_point_conditioned_W33_to_E6_tensor_shape"]==[40,40,27]
    assert result["two_point_conditional_E6_multiplicities"]=={
       "same_W33_point":27,"adjacent_W33_points":9,"nonadjacent_W33_points":3}
    assert result["each_W33_point_induces_nine_disjoint_E6_tritangent_triples"]
    assert result["all_40_point_conditioned_40x27_transfer_matrices_rank"]==9
    assert result["equivariant_symplectic_transvection_witnesses"]==7
    assert result["each_E6_line_40x40_pair_matrix_identity"].startswith("Q_l^2=8")
    assert "not a physical matter coupling" in result["quadratic_bridge_scope"]


def test_all_40_transvection_clocks_recover_27_E6_tritangent_triples(result):
    assert result["all_40_point_transvections_on_E6_lines_order"]==3
    assert result["all_40_point_transvections_orbit_type"]=="3^9, nine free 3-cycles"
    assert result["each_40_point_nine_cycles_equal_its_nine_tritangent_triples"]
    assert result["W33_adjacency_iff_cubic_line_transvections_commute"]
    assert result["commuting_pair_count_and_product_order"]=={"240":3,"540":6}
    assert result["all_780_pairs_checked"]
    assert "BT875" in result["operator_prior_art"]
    assert "not continuous E6 gauge" in result["operator_scope"]
