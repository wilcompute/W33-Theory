"""TOE48 independent producers + TOE47 regression checks."""
from pathlib import Path
import json,subprocess,sys
import pytest
R=Path(__file__).resolve().parents[1]
PACKET={
"naimark":"naimark44",
"spam":"spam_identifiability",
"intertwiner":"rational_intertwiner",
"census":"wilson_census_provenance",
"flux":"magnetized_potential_firewall"}
@pytest.fixture(scope="module")
def certificates():
 out={}
 for key,short in PACKET.items():
  script=R/"analysis"/("w33_20261010_toe48_"+short+".py")
  p=subprocess.run([sys.executable,str(script)],cwd=R,capture_output=True,text=True,timeout=90)
  assert p.returncode==0,(key,p.stdout[-1200:],p.stderr[-1500:])
  cert=R/"data"/("w33_20261010_toe48_"+short.replace("naimark44","naimark44")+".json")
  if key=="naimark":cert=R/"data/w33_20261010_toe48_naimark44.json"
  assert cert.exists(),str(cert)
  out[key]=json.loads(cert.read_text())
 return out
def test_44_mode_41_outcome_nai_unitary_compilation(certificates):
 x=certificates["naimark"]
 assert (x["input_modes"],x["fine_grained_modes"],x["reported_coarse_grained_outcomes"])==(9,44,41)
 assert x["nearest_neighbor_two_mode_SU2_ops"]==334
 assert x["nearest_neighbor_two_mode_SU2_ops"]<=351
 assert x["max_40_state_amplitude_reconstruction_error"]<1e-12
 assert x["povm_frame_isometry_error"]<1e-12
def test_known_nine_outcome_confusion_and_rigorous_95_bound(certificates):
 x=certificates["spam"]["general_confusion"]
 assert x["independent_blocks"]==4 and x["settings"]==10 if "settings" in x else x["independent_blocks"]==4
 assert x["shots_each_setting_each_block"]==1200
 assert x["empirical_coverage"]>=.95
 assert x["a_priori_uniform_Hoeffding_radius"]>0
 assert abs(x["mean_estimated_gap"]-x["true_gap"])<5*x["sd_estimated_gap"]/x["random_trials"]**.5
def test_MNAR_loss_identifiability_explicit_physical_states(certificates):
 x=certificates["spam"]["MNAR"]
 assert x["identical_postselection_residual"]<1e-12
 assert abs(x["purity_difference"])>1e-4
 assert min(x["outcome_efficiencies_case1"])>.5
def test_exact_integer_gram_and_char3_rank_collapse(certificates):
 x=certificates["intertwiner"]
 assert x["characteristic_zero_rank"]==25
 assert x["mod_prime_ranks_H"]["3"]==14
 assert x["mod_prime_ranks_H"]["5"]==25
 assert x["mod_prime_ranks_H"]["2"]==1
 assert x["max_12_Hermitian_operator_frame_reconstruction_error"]<1e-11
def test_491_census_cannot_supply_per_model_Wilson_matrices(certificates):
 x=certificates["census"]
 assert x["census_records"]==491
 assert x["indistinguishable_combinatorial_model_point_assignments"]==19640
 assert x["maximum_unlabelled_geometry_discrimination_bits"]==0
 assert len(x["five_down_escape_labels"])==5
 assert x["categories"]=={"untwisted":339,"twisted_one_torus":152}
def test_minimal_magnetized_potential_lacks_dynamical_CP_prediction(certificates):
 x=certificates["flux"]
 assert x["negative_delta"]["VEV_support_modes"]==1
 assert x["negative_delta"]["one_Higgs_YYdag_diagonal"]
 assert x["positive_delta"]["VEV_support_modes"]==6
 assert x["positive_delta"]["phase_samples_with_identical_V"]==140
 assert x["positive_delta"]["CP_odd_ImTr_commutator_cubed_max"]>1e-6
 assert x["positive_delta"]["CP_odd_ImTr_commutator_cubed_min"]< -1e-6
 assert "global_consistency_missing" in x
