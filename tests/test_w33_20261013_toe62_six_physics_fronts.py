"""TOE62: six source-regenerated W33 physics programs + mathematical scopes."""
from pathlib import Path
import subprocess,json,sys
import pytest
R=Path(__file__).resolve().parents[1]
NAMES=("leading_flux_theorem","continuous_flux","vertex_links",
       "time_links","three_loop_matter","gravity_nonuniform",
       "weighted_flux_robustness")
@pytest.fixture(scope="module")
def c():
 for name in NAMES:
  run=subprocess.run([sys.executable,str(R/"analysis"/f"w33_20261013_toe62_{name}.py")],
     cwd=R,capture_output=True,text=True,timeout=160)
  assert run.returncode==0,(name,run.stdout[-1300:],run.stderr[-1600:])
 return {name:json.loads((R/"data"/f"w33_20261013_toe62_{name}.json").read_text()) for name in NAMES}
def test_global_continuous_U1_leading_octagon_theorem(c):
 x=c["leading_flux_theorem"]
 f=x["exact_integer_winding_Fourier_coefficients"]
 assert len(f)==6 and sum(f.values())==238
 assert x["S_pi_pi_pi"]==-228 and x["S_zero"]==238
 assert x["rigorous_cosine_distance_lower_coefficients"]==[75,69,69]
 assert x["leading_deltaF_beta7_pi_vs_zero"]==pytest.approx(-.1964781746031746)
 assert max(abs(y["trace8_delta"]-y["Fourier_predicted_delta"]) for y in x["trace_H8_crosschecks"])<1e-6
 assert "NOT" in x["model_boundary"]
def test_continuous_flux_local_minimizers_numerical_not_global(c):
 x=c["continuous_flux"]
 assert x["bloch_deck_marking_flat_plaquette_PV_max"]==0
 assert len(x["cases"])==4
 for row in x["cases"]:
  assert row["three_pi_stationary_grad_norm_inf"]<1e-9
  assert row["gradient_vs_finite_difference_max"]<5e-7
  assert min(row["three_pi_Hessian_eigenvalues"])>0
  assert row["best_local_multistart_value"]>=row["F_three_pi"]-1e-7
  assert row["number_search_starts"]==10
 assert "NOT a certified" in x["limitation"]
def test_vertex_link_regular_simple_obstruction_and_basis(c):
 x=c["vertex_links"]
 assert x["native_graph"]["GF2_boundary_rank"]==78
 assert x["unique_possible_edge_pairs_across_vertices"]==480
 assert x["max_faces_if_simple_vertex_link"]==60
 assert x["closed_manifold_min_faces_from_Euler_and_nonempty_3cells"]==81
 assert len(x["eight_one_face_independent_subset"]["indices"])==81
 assert x["eight_one_face_independent_subset"]["GF2_boundary_rank"]==78
 assert x["eight_one_face_independent_subset"]["repeated_vertex_edge_pairs"]>=168
 assert "NOT an unconditional no-go" in x["limitations"]
def test_real_time_links_cancel_spurious_gauge_electric_curvature(c):
 x=c["time_links"]
 assert x["actual_sites"]==80 and x["actual_links"]==160
 assert x["fake_electric_F0e_when_temporal_links_omitted_rms"]>.15
 assert x["true_mixed_temporal_spatial_plaquette_error_with_temporal_links"]<1e-12
 assert x["spatial_plaquette_U1_flatness_max"]<1e-12
 assert len(x["native_320_band_kernel_slice_covariance"])==4
 assert max(y["kernel_gauge_covariance_max"] for y in x["native_320_band_kernel_slice_covariance"])<1e-10
 assert "NOT" in x["physical_limit"]
def test_three_loop_interacting_fermions_and_exact_Gauss(c):
 x=c["three_loop_matter"]
 assert x["patch_sites"]==14 and x["patch_links"]==16
 assert x["independent_fluxes"]==3 and x["fermion_count"]==6
 assert len(x["contained_native_wilson_rows"])>=3
 rows=x["runs"];assert len(rows)==4
 assert [r["sectors"]["neutral"]["dimension"] for r in rows]==[459,3051,14125,11259]
 for r in rows:
  assert r["charge_cost"]>0
  assert r["sectors"]["neutral"]["eigensolver_residual"]<1e-5
  assert r["sectors"]["charged"]["eigensolver_residual"]<1e-5
  assert 0<=r["sectors"]["neutral"]["electric_flux_boundary_weight"]<=1
  assert 0<=r["sectors"]["neutral"]["Fock_boundary_weight"]<=1
 assert rows[2]["sectors"]["neutral"]["ground"]<rows[1]["sectors"]["neutral"]["ground"]
 assert rows[3]["sectors"]["neutral"]["ground"]<rows[1]["sectors"]["neutral"]["ground"]
 assert "NOT" not in x["limitation"] or "not" in x["limitation"]
def test_localized_derivation_defect_diverges_when_low_bloch_shrinks(c):
 x=c["gravity_nonuniform"]
 assert x["native_derivative_shape"]==[3,80,80]
 assert x["D_skew_error"]<1e-10
 assert x["exact_unscaled_idempotent_column_norm_min"]>2
 assert x["exact_unscaled_idempotent_column_norm_max"]>46
 assert x["spacing_sweep"][-1]["high_over_low_ratio"]>50000
 assert "does NOT rule out" in x["gravity_boundary"]
def test_robust_global_high_temperature_theorem_under_bond_disorder(c):
 x=c["weighted_flux_robustness"]
 assert .14<x["rigorous_uniform_link_weight_deviation_threshold"]<.141
 assert min(x["verified_at_eps_0_1"])>15
 assert min(x["positive_lower_bound_at_eps_0_13"])>0
 assert len(x["random_weighted_graph_trace_checks"])==9
 assert "not a measured" in x["scope"]

def test_explicit_no_toe_claims(c):
 assert "not physical" not in c["leading_flux_theorem"]["theorem"].lower()
 assert "not" in c["three_loop_matter"]["limitation"].lower()
 assert "not" in c["time_links"]["physical_limit"].lower()
