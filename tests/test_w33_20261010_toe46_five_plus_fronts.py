"""TOE46 cross-front exact/regression audit. All producers deterministic."""
from pathlib import Path
import json,subprocess,sys
import pytest
ROOT=Path(__file__).resolve().parents[1]
CASES={
"dark":("w33_20261010_toe46_dark_fibers_mub_quartic.py","w33_20261010_toe46_dark_and_mub_quartic.json"),
"census":("w33_20261010_toe46_census_selector_firewall.py","w33_20261010_toe46_census_selector_firewall.json"),
"flux":("w33_20261010_toe46_magnetized_overlap_flux336.py","w33_20261010_toe46_magnetized_overlap_flux336.json"),
"weil":("w33_20261010_toe46_even_weil_dark_test.py","w33_20261010_toe46_even_weil_dark_rep_test.json"),
}
@pytest.fixture(scope="module")
def certs():
 out={}
 for key,(script,data) in CASES.items():
  process=subprocess.run([sys.executable,str(ROOT/"analysis"/script)],cwd=ROOT,
                  capture_output=True,text=True,timeout=90)
  assert process.returncode==0,(key,process.stdout[-1500:],process.stderr[-1500:])
  out[key]=json.loads((ROOT/"data"/data).read_text())
 return out
def test_general_full_rank_local_dark_fiber(certs):
 x=certs["dark"]
 assert x["dark_sector_dimension"]==15
 assert x["full_rank_state_min_eigen"]>0
 assert x["analytic_perturbation_upper_bound"]<x["full_rank_state_min_eigen"]
 assert min(x["physical_plus_min_eigen"],x["physical_minus_min_eigen"])>0
 assert x["same_purity_abs_difference"]<1e-12
 assert x["same_cusp_max_difference"]<1e-12
 assert x["different_density_frobenius"]>1e-9
def test_40_pauli_10_MUB_four_block_quartic_gap(certs):
 x=certs["dark"]
 m=x["measurement"]
 assert m["settings"]==10 and len(m["distinct_context_lines"])==10
 assert m["prepared_copies_per_trial"]==38400
 assert m["trials"]==160
 assert x["random_pure_Haar"]["true_gap"]<1e-24
 for k in ("random_mixed_Wishart","random_pure_Haar"):
  v=x[k]
  assert abs(v["estimate_mean"]-v["true_gap"])<5*v["standard_error_of_MC_mean"]+1e-7
 assert x["random_mixed_Wishart"]["true_gap"]>1e-5
def test_491_model_census_and_geometric_non_discrimination(certs):
 x=certs["census"]
 c=x["census"];g=x["geometry"]
 assert c["records"]==491
 assert c["kinds"]=={"untwisted":339,"twisted_one_torus":152}
 assert c["twisted_local_10"]==152
 assert c["down_non_single_point_models"]==5
 assert g["all_40_holonomy_choices_incidence_4_36"]
 assert g["every_nonincident_context_has_exactly_one_commuting_pauli"]
 assert x["zero_model_discrimination_from_unlabelled_incidence"]
def test_flux336_normalization_and_yukawa_conservation(certs):
 x=certs["flux"]
 assert x["flux_numbers"]=={"I_ab":3,"I_bc":3,"I_ca":-6,"gcd":3}
 assert x["max_L2_orthonormality_error_M3"]<1e-7
 assert x["max_L2_orthonormality_error_M6"]<1e-7
 assert x["max_forbidden_overlap"]<1e-12
 assert x["min_allowed_overlap"]>1e-4
 for row in x["all_six_fixed_Higgs_rows"]:
  assert len(row["nonzero_entries"])==3
  assert row["YYdag_offdiagonal_max"]<1e-12
  sing=row["singular_values"]
  assert min(abs(sing[0]-sing[1]),abs(sing[1]-sing[2]))<1e-10
def test_multi_higgs_mixing_and_cp_odd_invariant(certs):
 x=certs["flux"]["independent_two_Higgs_example"]
 assert x["mass_matrix_commutator_norm"]>1e-2
 assert abs(x["imag_trace_of_commutator_cubed"])>1e-4
 assert len(x["absolute_mixing_matrix"])==3
def test_even_weil_sym_square_not_dark_irrep(certs):
 x=certs["weil"]
 assert x["projective_equivalence_rejected_if_nonzero"]
 assert x["max_absolute_character_magnitude_difference"]>5.9
 assert len(x["random_word_character_tests"])==32
 assert abs(x["generator_character_absolute_tests"]["S"][2]-2)<1e-10
