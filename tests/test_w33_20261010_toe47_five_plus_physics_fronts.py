"""TOE47 reproducibility and exact mathematical/finite-shot checks."""
from pathlib import Path
import json,subprocess,sys
import pytest
R=Path(__file__).resolve().parents[1]
producer={
"cusp":("w33_20261010_toe47_cusp_even5_ic_povm.py","w33_20261010_toe47_even5_cusp_ic_povm.json"),
"purity":("w33_20261010_toe47_cusp_povm_purity.py","w33_20261010_toe47_even5_single_povm_purity.json"),
"fisher":("w33_20261010_toe47_dark_fisher_rank.py","w33_20261010_toe47_dark_fisher_information.json"),
"spam":("w33_20261010_toe47_spam_gap_variance.py","w33_20261010_toe47_spam_gap_exact_variance.json"),
"wilson":("w33_20261010_toe47_wilson_charge_conditional_mubs.py","w33_20261010_toe47_wilson_conditional_mubs.json"),
"flux":("w33_20261010_toe47_relative_wilson_flux336.py","w33_20261010_toe47_relative_wilson_flux336.json")}
@pytest.fixture(scope="module")
def cert():
 out={}
 for key,(source,dat) in producer.items():
  x=subprocess.run([sys.executable,str(R/"analysis"/source)],cwd=R,
    text=True,capture_output=True,timeout=90)
  assert x.returncode==0,(key,x.stdout[-1200:],x.stderr[-2000:])
  out[key]=json.loads((R/"data"/dat).read_text())
 return out
def test_even_weil_projector_orbit_is_40_rays_line_equivariant(cert):
 d=cert["cusp"]
 assert d["cusp_rays"]==40
 assert d["projector_Hermitian_span_dimension"]==25
 assert d["Gram_eigenvalues"]=={"8":1,"4/3":24,"0":15}
 assert d["off_diagonal_squared_inner_product_counts"]=={"1/3":480,"1/9":1080}
 assert d["max_generator_equivariance_error"]<1e-12
 for val in d["seven_W33_line_action_character_checks"].values():
  assert abs(val["visible_character"]-val["End5_character"])<1e-10
def test_cusp_projectors_form_2_design_and_informationally_complete_povm(cert):
 d=cert["cusp"]
 assert d["max_projective_2_design_error"]<1e-12
 assert d["max_30_random_mixed_reconstruction_error"]<1e-12
 assert d["exact_IC_POVM"].startswith("E_r=P_r/8")
 b=d["two_qutrit_41_outcome_embedding"]
 assert b["even_outcomes"]==40 and b["odd_leakage_outcomes"]==1
 assert b["effect_operator_span_dimension"]==26
 assert b["invisible_two_qutrit_traceless_directions"]==55
 assert b["max_15_random_two_qutrit_even_block_reconstruction_error"]<1e-12
def test_single_fixed_40_outcome_5D_purity_assay(cert):
 d=cert["purity"]
 assert d["readout_eps"]==.06 and d["pairs_per_trial"]==6500
 for k,v in d["cases"].items():
  assert abs(48*v["exact_collision"]-1-v["true_purity"])<1e-12
  assert abs(v["calibrated_estimate_mean"]-v["true_purity"])<5*v["predicted_single_trial_se"]/d["simulated_repetitions"]**.5
def test_collision_fisher_25_vs_full_ten_MUB_80(cert):
 d=cert["fisher"]
 assert (d["real_density_parameter_count"],d["collision_fisher_rank"],d["full_MUB_fisher_rank"])==(80,25,80)
 assert d["collision_fisher_nullity"]==55 and d["full_MUB_fisher_nullity"]==0
 assert d["one_dark_fixed_purity_direction"]["collision_score_norm"]<1e-11
 assert d["one_dark_fixed_purity_direction"]["full_MUB_Fisher_quadratic"]>1
def test_quartic_spam_exact_covariance_with_MAR_loss(cert):
 d=cert["spam"]
 assert d["shots"]["four_blocks"]==4 and d["shots"]["basis_count"]==10
 assert abs(d["mean_calibrated_estimate"]-d["rho_true_gap"])<5*(d["mean_exact_conditional_variance"]/d["shots"]["replicates"])**.5
 assert .7<d["variance_ratio_empirical_to_exact"]<1.3
 assert d["minimum_observed_valid_pairs_per_setting_and_block"]>250
 assert abs(d["mean_uncalibrated_estimate"]-d["rho_true_gap"])>1e-5
def test_Wilson_charge_four_conditional_qutrit_MUBs(cert):
 d=cert["wilson"]
 assert d["charge_values"]==3 and d["rank_of_each_charge_sector"]==3
 assert d["bases_per_charge_sector"]==4
 assert d["maximum_conditional_MUB_overlap_error"]<1e-12
 assert d["max_collision_block_identity_error"]<1e-12
def test_relative_Wilson_displacement_lifts_single_Higgs_doublet_not_CKM(cert):
 d=cert["flux"]
 b=d["sampled_shifts"]
 assert len(b)==6 and b[0]["split"]<1e-12
 assert all(v["split"]>1e-6 for v in b[1:])
 assert d["small_shift_linear_ratio_range"][1]/d["small_shift_linear_ratio_range"][0]<1.1
 assert d["flux"]["left"]==3 and d["flux"]["Higgs_conjugate"]==-6
