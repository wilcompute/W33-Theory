"""TOE53: five independent fronts and pinned Holotrade provenance."""
from pathlib import Path
import json,subprocess,sys
import pytest
R=Path(__file__).resolve().parents[1]
runs=["w33_20261013_toe53_h27_c3_extension.py",
 "w33_20261013_toe53_crossrepo_h27_frame_address.py",
 "w33_20261013_toe53_optical_15to81.py",
 "w33_20261013_toe53_spectral_noise_design.py",
 "w33_20261013_toe53_physics_unification_gates.py"]
files={"clock":"h27_c3_extension","cross":"crossrepo_h27_frame_address",
"optics":"optical_15to81_compilation","spectral":"spectral_noise_design",
"physics":"physics_unification_gates","holo":"holotrade_frame27_snapshot"}
@pytest.fixture(scope="module")
def data():
 for file in runs:
  p=subprocess.run([sys.executable,str(R/"analysis"/file)],cwd=R,
    capture_output=True,text=True,timeout=180)
  assert p.returncode==0,(file,p.stdout[-1000:],p.stderr[-1800:])
 return {k:json.loads((R/"data"/f"w33_20261013_toe53_{v}.json").read_text())
   for k,v in files.items()}
def test_clock_scalar_char_obstruction_and_constructed_graded_extension(data):
 d=data["clock"]
 assert d["scalar_FI_char_omega_minimum_number_of_81D_K81_slices"]=={"spread15":3,"cusp25":5,"line40":8}
 g=d["graded_source_clock_isometry"]
 assert len(g["orbit_charge_assignment"])==8
 assert g["source_dimension"]==40 and g["target_dimension"]==243
 assert g["max_H27_equivariance_error"]<1e-12
 assert g["max_C3_equivariance_error"]<1e-12
 assert g["isometry_inf_norm_error"]<1e-12
def test_pinned_holotrade_27_frame_action(data):
 f=data["holo"]
 assert f["source_commit"]=="b0264880d7c5fd24c6af932b892324247ab57808"
 assert len(f["frame_elation_permutations_lex_order"])==27
 assert sorted(f["frame_overlap_Qpsi_charges"])==[-2]*10+[1]*16+[4]
def test_generator_by_generator_W33_Holotrade_frame_addresses(data):
 c=data["cross"]
 assert c["group_multiplication_cases_checked"]==729
 assert c["frame_left_equivariance_cases_checked"]==729
 assert len(set(c["W33_group_index_to_Holotrade_frame_address"]))==27
 assert c["Qpsi_mu12_powers_commuting_with_frame_H27"]==[0,4,8]
def test_real_15_to81_optical_Givens_and_loss(data):
 o=data["optics"]
 assert o["input_dimension"]==15 and o["output_modes"]==81
 assert 0<o["nontrivial_adjacent_two_mode_Givens_rotations"]<=1095
 assert o["exact_matrix_reconstruction_max_element_error"]<1e-11
 assert len(o["simulated_equal_per_Givens_attenuation_scenarios"])==5
 assert o["simulated_equal_per_Givens_attenuation_scenarios"][2]["mean_transmission"]<1
 assert o["independent_Gaussian_Givens_phase_or_angle_noise"][-1]["mean_target_column_overlap_24trials"]<1
def test_optimality_claim_bounded_to_candidate_pool(data):
 s=data["spectral"]
 assert s["n_three_k_designs_evaluated"]==455
 assert s["optimized_row_normalized_smallest_sv"]>=s["original_row_normalized_smallest_sv"]-1e-12
 assert s["candidate_k_count"]==15
 assert len(s["oracle_3link_inversion_with_gaussian_measurement_noise"])==3
 for q in s["oracle_3link_inversion_with_gaussian_measurement_noise"]:
  t=q["expected_oracle_L2_error_rms"]
  m=q["oracle_known_3link_L2_error_rms_300"]
  assert abs(m/t-1)<.3
def test_physical_no_TOE_false_positive(data):
 v=data["physics"]
 assert v["n_gates"]==5 and v["n_fully_demonstrated"]==0
 assert v["conditional_uniform_FI_dimension_shortfall"]==405
 assert "NOT established" in v["clock_compatibility_conditionality"]
