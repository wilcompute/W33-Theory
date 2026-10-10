"""TOE44: five independent algebra/measurement/circuit/channel/CP tests."""
from pathlib import Path
import json,subprocess,sys,math
R=Path(__file__).resolve().parents[1]
def run(script,cert):
 process=subprocess.run([sys.executable,str(R/"analysis"/script)],cwd=R,
  capture_output=True,text=True,timeout=95)
 assert process.returncode==0,(process.stdout[-900:],process.stderr[-2000:])
 return json.loads((R/"data"/cert).read_text())
def test_sic_product_state_sharp_bound_and_entanglement_requirement():
 d=run("w33_20261010_toe44_product_sic_bound.py",
       "w33_20261010_toe44_product_sic_bound.json")
 assert d["product_lower_bound_variance"]=="1/150"
 assert abs(d["numeric_saturation_variance"]-1/150)<1e-12
 assert d["minimum_random_product_variance"]>=1/150-1e-12
 assert d["previous_global_entangled_48start_best_variance"]<1/150
def test_W33_10_MUB_calibrated_loss_and_readout_assay():
 d=run("w33_20261010_toe44_mub_spam.py",
       "w33_20261010_toe44_mub_spam.json")
 assert d["symplectic_W33_line_count"]==40
 assert len(d["verified_spread_line_indices"])==10
 assert len(d["verified_zline_point_indices"])==4
 assert abs(d["calibrated_mean_purity"]-d["true_global_purity"])<.005
 assert abs(d["uncalibrated_bias"])>.02
 assert .93<d["conditional_gaussian_95pct_coverage"]<.97
 assert .04<d["standard_error_mean"]<.06
def test_exact_45_native_e6_ccz_ternary_clifford_R_compilation():
 d=run("w33_20261010_toe44_exact_ccz_7R.py",
       "w33_20261010_toe44_ternary_ccz_compiler.json")
 q=d["total_native_gate_resources"]
 assert q["three_qutrit_CCZ_terms"]==45
 assert q["R_ninth_root_gates"]==315
 assert q["SUM_two_qutrit_Clifford_gates"]==450
 assert q["ideal_45_term_5_layer_bundled_primitive_depth"]==85
 assert d["native_sign_count"]=={"positive":22,"negative":23}
 assert len(d["example_positive_ops"])==17
def test_one_ancilla_magic_injection_feed_forward_is_exact():
 d=json.loads((R/"data/w33_20261010_toe44_ternary_ccz_compiler.json").read_text())
 q=d["total_native_gate_resources"]
 assert q["consumed_R_magic_states"]==315
 assert q["total_SUM_with_magic_injections"]==765
 assert q["injection_Z_measurements"]==315
 assert q["adaptive_single_qutrit_Clifford_corrections"]==315
 assert q["max_concurrent_magic_ancillas_in_ideal_disjoint_layer"]==9
 for sign,rows in d["magic_injection_correction_tables"].items():
  assert len(rows)==3
  for m,row in enumerate(rows):
   assert row["measurement"]==m
   for x,c in enumerate(row["phase_correction_omega_exponents"]):
    f=lambda v:(v%3)**3%9
    assert (-int(sign)*f(m-x)+3*c+int(sign)*f(m)-int(sign)*f(x))%9==0
def test_W33_power_moments_fail_to_identify_CPTP_channels():
 d=run("w33_20261010_toe44_channel_identifiability.py",
       "w33_20261010_toe44_channel_identifiability.json")
 p=d["input_probe_results"]["primary_00"]
 s=d["input_probe_results"]["secondary_interference_01_02"]
 assert p["trace_distance"]<1e-12
 assert s["trace_distance"]>.62
 assert s["max_power_difference"]<1e-12
 assert s["max_complex_exp_component_difference"]>.6
def test_E8_single_degree12_coupling_CP_phase_is_rephasable():
 d=run("w33_20261010_toe44_e8_cp_cw_firewall.py",
       "w33_20261010_toe44_e8_cp_phase_firewall.json")
 assert d["max_single_invariant_cp_residual_30_trials"]<1e-12
 assert d["CP_compatible_max_residual"]<1e-12
 assert d["CP_incompatible_min_residual_over_12_branches"]>.2
 assert abs(d["vector_witting_shape_F"]+6*math.log(3))<1e-10
