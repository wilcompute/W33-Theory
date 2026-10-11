"""TOE49 five independent regressions of the newly landed 11906-11911 data."""
from pathlib import Path
import json,subprocess,sys
import pytest
R=Path(__file__).resolve().parents[1]
items={
"gauge":("gauge_vector_audit","gauge_vector_audit"),
"ckm":("ckm_mass_labels","ckm_mass_label_audit"),
"cw":("cw_scale_invariance","cw_scale_counterterm"),
"stats":("cross_sector_statistics","cross_sector_statistics"),
"parity":("exact_siegel_parity","exact_siegel_charge_parity")}
@pytest.fixture(scope="module")
def data():
 a={}
 for k,(src,cert) in items.items():
  p=subprocess.run([sys.executable,str(R/"analysis"/f"w33_20261010_toe49_{src}.py")],
    cwd=R,text=True,capture_output=True,timeout=120)
  assert p.returncode==0,(k,p.stdout[-900:],p.stderr[-1200:])
  a[k]=json.loads((R/"data"/f"w33_20261010_toe49_{cert}.json").read_text())
 return a
def test_new_600_rational_Wilson_vectors(data):
 a=data["gauge"]
 assert a["total_models"]==600
 assert a["model_source_counts"]=={"a8_sm_all.txt":104,"rescan_all_SM.txt":387,"split10_all_SM.txt":109}
 assert a["all_models_have_9_rows_of_16_rationals"]
 assert sum(a["n_distinct_nonzero_W_distribution"].values())==600
 assert len(a["model_details"])==600
def test_mass_ordered_ckm_not_fourth_largest(data):
 a=data["ckm"]
 p=a["repo_analog_at_eps_003"]
 assert .20<p["fourth_largest"]<.24
 assert p["Vus"]<.001
 assert p["Vub"]>.99
 assert abs(p["J"])<1e-12
def test_higgs_amplitude_phase_scan_excludes_one_fixed_toy_fit(data):
 a=data["ckm"]["extended_amplitude_phase_scan"]
 assert a["count"]==6336
 assert a["all_3_target_entries_within_factor2_count"]==0
 assert min(z["score"] for z in a["top_five"])>1.
def test_CW_matching_scale_finite_counterterm_exact(data):
 a=data["cw"]
 assert a["max_52_points_relative_Vshift_error"]<1e-10
 assert a["counterterm_shift_needed_GeV2"]>0
 assert a["msoft_GeV"]==1000
def test_cross_sector_tau_obstruction_and_scan_sensitivity(data):
 a=data["stats"]
 assert 1.55<a["cross_sector"]["required_effective_area_up_over_down"]<1.65
 assert 600<a["cross_sector"]["invariant_down_over_up"]<800
 b=a["supersymmetric_Z3_scan"]
 assert b["draws_total"]==80000 and b["successes_reported"]==0
 assert 3e-5<b["conditional_95pct_one_sided_binomial_upper_hit_probability_if_IID"]<4e-5

def test_full_Siegel_even_charge_lock_and_mirror(data):
 a=data["parity"]
 assert a["n_random_positive_definite_complex_Siegel_moduli"]==36
 assert a["max_class_zero_complex_light_amplitude_difference"]<1e-12
 assert a["max_class_1_2_charge_mirror_complex_difference"]<1e-12
