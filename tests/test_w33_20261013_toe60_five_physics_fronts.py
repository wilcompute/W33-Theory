"""TOE60 independently regenerates seven W33 physics certificates and asserts scopes."""
import json,subprocess,sys
from pathlib import Path
import pytest
R=Path(__file__).resolve().parents[1]
NAMES=("spectral_majorization","rewired_graph_control","topological_3cell_obstruction",
       "3cell_spoof","leibniz_coefficient","sparse_flux_bounds","thermal_grid")
@pytest.fixture(scope="module")
def cert():
 for n in NAMES:
  v=subprocess.run([sys.executable,str(R/"analysis"/f"w33_20261013_toe60_{n}.py")],
   cwd=R,text=True,capture_output=True,timeout=150)
  assert v.returncode==0,(n,v.stdout[-750:],v.stderr[-2000:])
 return {n:json.loads((R/"data"/f"w33_20261013_toe60_{n}.json").read_text()) for n in NAMES}
def test_strong_spectral_majorization_falsified_all_7(cert):
 rows=cert["spectral_majorization"]["results"]
 assert len(rows)==8
 assert all(x["passes_majorization_to_numerical_tol"] is False for x in rows[1:])
 assert all(x["min_proper_partial_margin"]< -1 for x in rows[1:])
 assert rows[-1]["min_proper_partial_margin"]< -11
def test_nonW33_degree_matched_controls_detect_shorter_loops(cert):
 c=cert["rewired_graph_control"]
 assert c["W33_eight_step_flat_holonomy_on_TOE59"]==8
 assert len(c["rewired_graphs"])==28
 assert c["frequency"]["4"]==12 and c["frequency"]["6"]==16
 assert all(r["switches"]>100 for r in c["rewired_graphs"])
 assert "do NOT preserve" in c["limitation"]
def test_native_spatial_topology_needs_3cells_for_T3(cert):
 c=cert["topological_3cell_obstruction"]
 assert c["native_chain"]["rational_betti_X_2skeleton"]==[1,3,1307,0,0]
 assert c["naive_product_with_periodic_time_circle"]["rational_betti_X_times_S1"]==[1,4,1310,1307,0]
 assert c["naive_product_with_periodic_time_circle"]["H4_dimension"]==0
 a=c["minimal_necessary_3cell_homology_completion_for_T3"]
 assert a["required_rank_boundary_d3"]==1304
 assert a["required_number_3cells_without_4cells"]==1305
def test_algebraic_3cell_spoof_shows_betti_not_geometry(cert):
 c=cert["3cell_spoof"]
 assert c["rank_d2"]==78 and c["two_cycle_kernel_basis_dimension"]==1307
 assert c["max_boundary2_boundary3_residual_on_1307_implicit_cycles"]<1e-10
 assert c["constructed_rational_betti"]==[1,3,3,1]
 assert "NOT yield a manifold" in c["WARNING"]
def test_restricted_Bloch_Leibniz_exact_leading_coefficient(cert):
 c=cert["leibniz_coefficient"]
 assert c["exact_leading_coeff_rms"]==pytest.approx(1.4684458905023818)
 assert c["rms_records"][-1]["relative_vs_Oa_limit"]<.01
 assert c["rms_records"][-1]["rms_error"]<.02
def test_sparse_selected_rotor_bounds_improve_and_report_residual(cert):
 c=cert["sparse_flux_bounds"]
 assert c["selected_native_signed_Gram"]==[[8,-4,-4],[-4,8,4],[-4,4,8]]
 for x in c["cases"]:
  assert [r["states"] for r in x["rows"]]==[729,1331,2197]
  assert all(r["ground_vector_residual_norm"]<1e-7 for r in x["rows"])
  assert x["rows"][-1]["interval_width"]<x["rows"][0]["interval_width"]
 assert c["cases"][0]["rows"][-1]["interval_width"]<.071
 assert c["cases"][1]["rows"][-1]["interval_width"]<.0045
 assert "not machine-interval" in c["derivation"] or "numerically verified enclosures" in c["derivation"]
def test_flux_half_filling_favored_numerically_across_beta_grid(cert):
 c=cert["thermal_grid"]
 assert len(c["rows"])==8
 assert len(c["tested_inverse_temperatures"])==10
 assert all(r["strict_lower_at_all_sampled_beta"] for r in c["rows"][1:])
 assert c["rows"][-1]["zero_temperature_fermion_filled_sea_shift"]< -1.8
 assert "not" in c["majorization_caveat"].lower()
def test_physical_boundaries_are_explicit(cert):
 assert "does not" in cert["topological_3cell_obstruction"]["minimal_necessary_3cell_homology_completion_for_T3"]["only_necessary"].lower()
 assert "not machine-interval" in cert["sparse_flux_bounds"]["derivation"]
