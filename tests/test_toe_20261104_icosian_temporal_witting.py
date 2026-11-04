"""Cross-paper counterexamples: 600-cell stabilizer vs Reye and Choi two-time qutrit."""
import importlib.util
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
def importer(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod

@pytest.fixture(scope="module")
def cell():
    return importer("icosian_cosets",
        "analysis/toe_20261104_icosian_24cell_tomotope_obstruction.py").main()

@pytest.fixture(scope="module")
def time():
    return importer("qutrit_history",
        "analysis/toe_20261104_temporal_choi_witting_bridge.py").main()

def test_exact_icosian_subgroup_and_twentyfive_cells(cell):
    g=cell["geometry"]
    assert (g["quaternion_vertices"],g["Hurwitz_binary_tetrahedral_order"])==(120,24)
    assert g["distinct_conjugate_subgroups_of_order24"]==5
    assert g["cosets_per_subgroup"]==5 and g["inscribed_24cells"]==25
    assert g["each_600cell_vertex_in_n_24cells"]==5
    assert g["unordered_24cell_intersections"]=={"0_vertices":100,"6_vertices":200}

def test_600cell_5x5_rook_and_E8_PG3F4_count(cell):
    g=cell["geometry"]
    assert g["disjointness_graph_srg"]==[25,8,3,2]
    assert g["disjointness_graph_is_isomorphic_to_5x5_rook"]
    assert g["total_five_cell_decompositions"]==10
    assert g["projective_600cell_antipodal_axes"]==60
    assert g["axes_plus_24cells_85_points_of_PG3_F4_count"]==85
    assert g["each_axis_in_five_24cells"]

def test_equal_576_orders_are_nonisomorphic_groups(cell):
    s=cell["stabilizer"];r=cell["reye"]
    assert s["one_inscribed_24cell_H4_stabilizer_order"]==576
    assert r["reye_medial_color_preserving_automorphism_order"]==576
    assert s["central_antipodal_order2_exists"] and r["reye_group_center_order"]==1
    assert s["stabilizer_order_histogram"]["12"]==96
    assert "12" not in r["reye_order_histogram"]
    assert "NOT isomorphic" in cell["exact_no_go"]

def test_one_qutrit_two_time_choi_is_9_not_3(time):
    assert time["Pauli_3x3_single_system_operator_basis_size"]==9
    assert time["two_time_Choi_operator_Hilbert_dimension"]==9
    assert time["two_commuting_qutrit_factor_algebras_dimensions"]==[9,9]
    assert time["full_double_operator_algebra_dimension"]==81
    assert time["identity_process_Choi_Schmidt_rank"]==3
    assert time["identity_process_Choi_reduced_density"]=="I_3/3"

def test_two_qutrit_symplectic_and_witting_graphs_same_but_not_rays(time):
    assert time["finite_commutation_graph_SRG"]==[40,12,2,4]
    assert time["commuting_pairs"]==240
    assert time["projective_order3_nonidentity_Pauli_classes"]==40
    assert time["Witting_ququart_rays"]==40 and time["Witting_ray_Hilbert_dimension"]==4
    assert time["Witting_orthogonality_graph_exactly_isomorphic"]
    assert time["Pauli_reps_are_pairwise_Hilbert_Schmidt_orthogonal"]
    assert time["Witting_Ray_and_Pauli_Operator_gram_matrices_are_not_equal"]
    assert len(set(time["explicit_graph_isomorphism_pauli_index_to_witting_index"]))==40

def test_temporal_choi_isotropic_entanglement_witness_under_noise(time):
    rows=time["ideal_depolarizing_Choi_positivity_And_partial_transpose_witness"]
    assert [r["depolarizing_probability"] for r in rows]==[0,.25,.5,.75,1]
    assert abs(rows[0]["Choi_partial_transpose_negativity"]-1)<1e-12
    assert rows[3]["Choi_partial_transpose_negativity"]<1e-12
    assert rows[4]["Choi_partial_transpose_negativity"]<1e-12
    assert all(abs(r["normalized_Choi_entanglement_fidelity"]-
                   (1-8*r["depolarizing_probability"]/9))<1e-12 for r in rows)
    assert [r["entanglement_witness_F_exceeds_one_third"] for r in rows]==[True,True,True,False,False]
