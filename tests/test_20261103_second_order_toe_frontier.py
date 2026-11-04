"""Regression tests for five second-order TOE controls plus W33 40-mode bridge.
Intentionally runs the producer once, then verifies every certificate type."""
import importlib.util
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"analysis"/"2026_11_03_second_order_toe_frontier.py"
@pytest.fixture(scope="module")
def checked():
    spec=importlib.util.spec_from_file_location("second_order_toe",SOURCE)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.main()
def test_all_five_and_w33_pass(checked):
    keys=["SU2_nonabelian_discrete_Bianchi","causal_fixed_coupling_finite_size_drift",
          "mixed_dimension_simplicial_cone","interacting_matter_universal_coupling",
          "nongeometric_commutator_graph_inference",
          "bonus_W33_single_excitation_operator_bridge"]
    assert all(checked[k]["status"]=="PASS" for k in keys)
def test_nonabelian_cube_bianchi_covariance_negative_control(checked):
    d=checked["SU2_nonabelian_discrete_Bianchi"]
    assert d["face_count"]==6
    assert d["six_transport_face_Bianchi_residual"]<1e-12
    assert d["maximum_gauge_covariance_error"]<1e-12
    assert d["deliberately_untransported_face_product_defect"]>0.01
    assert d["largest_nontrivial_rooted_face_holonomy"]>0.1
def test_frozen_causal_null_fails_scale_stability(checked):
    d=checked["causal_fixed_coupling_finite_size_drift"]
    rows=d["finite_size"]
    assert [r["n"] for r in rows]==[32,48,72,96]
    assert d["training_only_n"]==48
    assert abs(d["theory_four_d_density"]-.1)<1e-12
    assert abs(d["reference_density_change"])<.045
    assert d["growth_density_change"]>.06
    assert rows[-1]["growth_height"]>rows[-1]["reference_height"]+3
def test_simplicial_dimension_transition_is_not_smooth_manifold(checked):
    d=checked["mixed_dimension_simplicial_cone"]
    assert d["total_subsets"]==256
    assert d["partial_mixed_dimensional_states"]==254
    assert d["initial_sphere"]["betti"]==[1,0,1,0]
    assert d["final_three_ball"]["betti"]==[1,0,0,0]
    assert sum(x["count"] for x in d["distribution_by_tetra_count_and_beta2"])==256
    assert any(x["betti2"]>1 for x in d["distribution_by_tetra_count_and_beta2"])
def test_interacting_matter_total_stress_conserved(checked):
    d=checked["interacting_matter_universal_coupling"]
    assert d["total_tensor_conserved"]
    assert d["explicit_Q_upper_t_x"]==[-174,42]
    assert d["universal_weighted_divergence"]==[0,0]
    assert d["nonuniversal_weighted_divergence"]==[174,-42]
def test_pauli_commutator_reconstruction_and_three_body_control(checked):
    d=checked["nongeometric_commutator_graph_inference"]
    assert d["hilbert_dimension"]==32
    assert d["maximum_pair_operator_reconstruction_error"]<1e-12
    assert len(d["inferred_signed_couplings"])==5
    assert d["third_body_false_positive_double_commutator_norm"]>1
    assert abs(d["third_body_exact_pair_projection"])<1e-12
    assert d["local_Z_gauge_transformed_couplings"]["0-1"]==-d["inferred_signed_couplings"]["0-1"]
def test_w33_projective_operator_bridge(checked):
    d=checked["bonus_W33_single_excitation_operator_bridge"]
    assert d["projective_points"]==40
    assert d["graph_parameters"]==[40,12,2,4]
    assert d["edges"]==240
    assert d["tested_matrix_commutators"]==50
    assert d["maximum_operator_residual"]<1e-12
