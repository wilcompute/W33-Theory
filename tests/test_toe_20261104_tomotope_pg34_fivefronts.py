"""Five-front exact tomotope 24-cell PG3F4 / Witting temporal / KS hardware tests.

The source producers and original literature distinguish prior-art identities
from the extra local computations. No physical TOE is asserted.
"""
import importlib.util,sys,math
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
for p in (ROOT,ROOT/"analysis"):
    if str(p) not in sys.path:sys.path.insert(0,str(p))
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m
@pytest.fixture(scope="module")
def pg():
    return load("toepg34","analysis/toe_20261104_pg34_icosian_quadric.py").main()
@pytest.fixture(scope="module")
def subgroup():
    return load("toe_h4_sg","analysis/toe_20261104_h4_24cell_reye_index2.py").run()
@pytest.fixture(scope="module")
def instrument():
    return load("toe_witting_instr","analysis/toe_20261104_temporal_witting_instrument_noise.py").main()
@pytest.fixture(scope="module")
def interferometer():
    return load("toe_ks_interferometer","analysis/toe_20261104_ks18_witting_interferometer_compiler.py").main()

def test_icosian_24cell_pg34_complete_point_classification(pg):
    assert (pg["inscribed_24cells"],pg["antipodal_axes"])==(25,60)
    assert pg["PG3F4_points"]==85 and pg["PG3F4_lines"]==357 and pg["PG3F4_planes"]==85
    assert pg["cells_as_projective_rank1_2x2_F4_matrices"]==25
    assert pg["axes_as_projective_invertible_2x2_F4_matrices"]==60
    assert pg["axis_permutations_equal_A5_equal_PGL2_F4"]
    assert {tuple(rec["permutation"]) for rec in pg["icosian_axis_permutations_60"]}.__len__()==60

def test_icosian_polarity_incidence_and_projective_line_spectrum(pg):
    assert pg["axis_cell_polar_incidence_exact_matches_300_memberships"]
    assert pg["cell_axis_incidence_rows_each"]==12
    assert pg["cell_axis_incidence_cols_each"]==5
    assert pg["lines_through_each_point"]==21 and pg["points_on_each_line"]==5
    assert pg["line_types_number_quadric_points"]=={0:72,1:75,2:200,5:10}

def test_all_25_projective_tangent_planes_exactly_reye(pg):
    assert pg["all_25_24cells_reye_graphs_are_16_tangent_plane_secants"]
    assert pg["all_25_spatial_hexagon_planes_equal_projective_secant_triples"]
    rows=pg["reye_tangent_plane_records_25"]
    assert len(rows)==25
    for row in rows:
        assert len(row["incidence_axes"])==12
        assert len(row["central_hexagon_axes"])==16
        assert all(len(t)==3 for t in row["central_hexagon_axes"])
        assert row["icosian_hexagon_planes_identical_to_projective_secants"]
        assert row["tangent_plane_projective_lines"]==21
        assert row["lines_not_through_quadric_center"]==16

def test_actual_order288_reye_embedding_and_center_kernel(subgroup):
    assert subgroup["original_H4_stabilizer_on_600cell_vertices_order"]==576
    assert subgroup["effective_H4_stabilizer_on_12axes_16hexagons_order"]==288
    assert subgroup["all_reye_automorphisms_order"]==576
    assert subgroup["effective_image_has_index2_in_reye"]
    assert subgroup["parameterization_kernel_size"]==4
    assert subgroup["effective_group_center_order"]==1
    assert subgroup["effective_group_order_histogram"]=={"1":1,"2":27,"3":80,"4":36,"6":144}
    assert len(subgroup["cell24_axis_to_published_Reye_axis_index_map"])==12
    assert len(set(subgroup["cell24_hexagon_to_published_Reye_line_index_map"]))==16

def test_witting_instrument_exact_two_design_and_kraus_cptp(instrument):
    assert instrument["kraus_operator_count"]==120
    assert (instrument["input_history_dimension"],instrument["output_ququart_dimension"])==(9,4)
    assert instrument["CPTP_completeness_worst_residual"]<1e-10
    assert instrument["map_is_measure_and_prepare_entanglement_breaking"]
    assert instrument["Witting_40_ray_first_moment_identity"]=="sum_r |r><r|=10 I4"

def test_local_witting_cannot_witness_choi_history(instrument):
    assert abs(instrument["p0_to_p1_channel_states_full_joint_trace_distance"]-8/9)<1e-12
    assert abs(instrument["ideal_joint_time_process_distinguishing_success_probability"]-17/18)<1e-12
    assert instrument["output_only_Witting_readout_p0_vs_p1_trace_distance"]==0
    assert instrument["output_only_Witting_readout_p0_vs_p1_success_probability"]==.5
    controls=instrument["sample_readouts"]
    assert len(controls)==5
    assert all(z["trace_output_local"]==controls[0]["trace_output_local"] for z in controls)

def test_multitime_depolarizing_composition_13_14_boundary(instrument):
    assert instrument["last_entangled_exchange_for_p_point_one"]==13
    assert instrument["first_entanglement_breaking_exchange_for_p_point_one"]==14
    records=instrument["flagged_erasure_and_repeated_exchanges"]
    assert len(records)==28
    for row in records:
        m=row["exchange_count"];eta=row["survival_probability"]
        expected=eta*max(0,(4*(.9**m)-1)/3)
        assert abs(row["Choi_entanglement_negativity_unconditional"]-expected)<1e-11

def test_all_16_critical_KS_sets_compiled(interferometer):
    assert interferometer["num_published_critical_18_ray_sets"]==16
    assert len(interferometer["all_16_critical_set_compiled_resource_summary"])==16
    assert interferometer["best_18ray_nine_contexts_couplers"]==28
    assert len(interferometer["best_18ray_contexts"])==9
    assert sum(interferometer["best_18ray_context_gate_counts"])==28
    assert interferometer["maximal_unitary_reconstruction_residual"]<1e-10

def test_all_40_witting_bases_compiled(interferometer):
    assert interferometer["Witting_40_tetrad_basis_count"]==40
    assert sum(interferometer["Witting_fourmode_couplers_per_context"])==150
    assert interferometer["Witting_total_couplers_for_40_contexts"]==150
    assert len(interferometer["Witting_all_40_contexts"])==40

def test_classical_contextuality_bound_exact_and_conditional_noise(interferometer):
    assert interferometer["one_witness_exhaustive_binary_assignments"]==2**18
    assert interferometer["contextuality_noncontextual_classical_bound"]==7
    assert interferometer["ideal_quantum_context_product_sum"]==9
    eps=interferometer["independent_sign_flip_epsilon_strictly_below_to_violate"]
    assert math.isclose(eps,(1-(7/9)**.25)/2,abs_tol=1e-12)
    assert 0.03<eps<0.031

def test_200_global_reye_hexagon_gluings_are_polar_line_dual(pg):
    hist=pg["24cell_pair_shared_icosian_axes_histogram"]
    assert hist=={0:100,3:200}
    assert pg["200_distinct_shared_3axis_hexagons"]==200
    assert pg["all_200_shared_hexagons_match_polar_duals_of_2quadric_secants"]
    edges=pg["shared_hexagon_between_cell_pairs"]
    assert len(edges)==200
    assert len({tuple(v) for v in edges.values()})==200
    assert all(len(v)==3 for v in edges.values())

def test_full_coupler_matrix_payloads_reconstruct_each_of_49_bases(interferometer):
    import numpy as np
    from exploration.w33_witting_srg_bridge import construct_witting_rays
    from analysis.toe_20261104_reye_peres_critical_ks import RAYS
    W=np.array(construct_witting_rays())
    rows=interferometer["Witting_all_40_contexts"]+interferometer["best_18ray_contexts"]
    assert len(rows)==49
    for record in rows:
        A=np.diag(np.exp(1j*np.array(record["phases"])))
        for g in reversed(record["blocks"]):
            i,j=g["modes"]
            small=np.array(g["exact_Givens_block_real"])+1j*np.array(g["exact_Givens_block_imag"])
            G=np.eye(4,dtype=complex)
            G[np.ix_([i,j],[i,j])]=small
            assert np.max(abs(small.conj().T@small-np.eye(2)))<1e-12
            A=G.conj().T@A
        if "ray_labels" in record:
            B=np.column_stack([W[k] for k in record["ray_labels"]])
        else:
            B=np.column_stack([np.array(RAYS[k-1],dtype=float)/
                np.linalg.norm(RAYS[k-1]) for k in record["rays"]])
        assert np.max(abs(A-B[:,record["permutation"]]))<1e-10
