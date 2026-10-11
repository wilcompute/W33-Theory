"""TOE45 targeted reproducibility checks for the new cusp/Pauli tomography bridge."""
from pathlib import Path
import json,subprocess,sys
R=Path(__file__).resolve().parents[1]
S="w33_20261010_toe45_cusp_collision_reconstruction.py"
C="w33_20261010_toe45_cusp_collision_tomography.json"
def replay():
 p=subprocess.run([sys.executable,str(R/"analysis"/S)],cwd=R,
                  capture_output=True,text=True,timeout=35)
 assert p.returncode==0,(p.stdout[-2000:],p.stderr[-2000:])
 return json.loads((R/"data"/C).read_text())
def test_40_cusp_line_incidence_and_wilson_4_plus_36_selector():
 d=replay()
 g=d["geometry"]
 assert (g["points"],g["cusps_context_lines"],g["rank"])==(40,40,25)
 assert g["singular_values_squared"]=={"16":1,"6":24,"0":15}
 assert g["one_Wilson_point_incident_cusps"]==4
 assert g["nonincident_cusps"]==36
 assert g["one_nonincident_cusp_commuting_points_with_Wilson"]==1
 assert (g["incident_flag_total"],g["nonincident_pair_total"])==(160,1440)
def test_exact_pure_pauli_power_recovery_from_40_collision_probabilities():
 d=replay()
 assert d["pure_cases"]==64
 assert d["max_pure_reconstruction_error"]<1e-12
 assert d["max_pure_minus_sector"]<1e-12
 assert d["cusp_factorization_variance_duality"]["pure_equality"].startswith("The gap")
def test_explicit_positive_equal_purity_density_matrices_same_all_cusp_collisions():
 d=replay()["positive_counterexample"]
 assert min(d["min_eigenvalue_rho_plus"],d["min_eigenvalue_rho_minus"],d["min_eigenvalue_rho_baseline"])>.1
 assert abs(d["purity_rho_plus"]-d["purity_rho_minus"])<1e-12
 assert d["max_cusp_collision_difference"]<1e-12
 assert d["baseline_vs_dark_max_cusp_collision_difference"]<1e-12
 assert d["dark_sector_difference_norm"]>1e-6
 assert d["density_operator_difference_norm"]>1e-4
 assert d["max_full_MUB_projector_collision_check"]<1e-12
def test_exact_90_virtual_purity_and_40_context_collision_gap():
 d=replay()["cusp_factorization_variance_duality"]
 assert d["nondegenerate_frame_count"]==90
 assert abs(d["dark_mixed_variance"]-d["dark_mixed_predicted_gap"])<1e-14
 assert d["dark_mixed_variance"]>1e-13
 assert d["dark_mixed_cusp_variance"]<1e-15
 assert d["baseline_same_cusps_mixed_variance"]<1e-15
 assert abs(d["pure_example_frame_and_cusp_variance"][0]-d["pure_example_frame_and_cusp_variance"][1])<1e-12
 assert d["random_mixed_cases"]==20
 assert d["random_mixed_max_dark_variance_gap"]>1e-5
def test_cusp_context_labels_are_grounded_in_preexisting_pass11899():
 old=json.loads((R/"data/w33_pass11899_kahler_special_points_cp.json").read_text())
 o=[row for row in old["orbits"] if row["stabiliser"]==648]
 assert len(o)==1 and o[0]["orbit"]==40
 assert o[0]["fixed_w33_lines"]==1 and o[0]["fixed_w33_points"]==0
 assert old["all_checks_pass"]
