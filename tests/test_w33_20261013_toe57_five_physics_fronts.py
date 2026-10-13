"""TOE57 five physics fronts: true producer reproduction + narrow evidence gates."""
from pathlib import Path
import json,sys,subprocess
import pytest
R=Path(__file__).resolve().parents[1]
scripts=["two_plaquette_quantum","fermion_holonomy","gravity_potential_no_go",
         "one_loop_competition","coupling_chirality_gate"]
certificate_names=["two_plaquette_quantum","fermion_holonomy","gravity_potential_no_go",
                   "one_loop_competition","coupling_chirality_gate"]
@pytest.fixture(scope="module")
def certs():
 for name in scripts:
  q=subprocess.run([sys.executable,str(R/"analysis"/f"w33_20261013_toe57_{name}.py")],
     cwd=R,text=True,capture_output=True,timeout=180)
  assert q.returncode==0,(name,q.stdout[-700:],q.stderr[-1500:])
 return {name:json.loads((R/"data"/f"w33_20261013_toe57_{name}.json").read_text())
          for name in certificate_names}
def test_native_two_plaquette_overlap_exact_and_gauss(certs):
 c=certs["two_plaquette_quantum"]
 assert c["native_dimensions"]=={"vertices":80,"links":160,"plaquettes":1385}
 assert c["two_loop_signed_gram"]==[[8,-4],[-4,8]]
 assert c["electric_cross_coupling_at_g_0p8"]==pytest.approx(-2.56)
 for runs in c["truncated_sectors"].values():
  assert [z["level_count"] for z in runs]==[25,49,81,121]
  assert all(z["matrix_hermitian_residual"]==0 for z in runs)
  assert runs[-1]["boundary_probability"]<.02
  assert runs[-1]["gap"]>0
  assert abs(runs[-1]["ground_energy"]-runs[-2]["ground_energy"])<.09
def test_quantum_open_strings_have_physical_charge_endpoints(certs):
 t=certs["two_plaquette_quantum"]["truncated_sectors"]
 for g in (0.4,0.8,1.2):
  q=t[f"{g}_open"][-1]["gauss_charges"]
  assert sorted(x for x in q if x) == [-1,1]
  assert t[f"{g}_vacuum"][-1]["gauss_charges"]==[0]*80
def test_flat_fermion_one_loop_changes_energy_vs_boson_no_go(certs):
 v=certs["fermion_holonomy"]
 assert v["survey_count"]==85
 assert v["n_fermion_lower_than_zero"]>70
 assert v["n_boson_lower_than_zero"]==0
 assert v["sampled_min_fermion_free_energy_shift"]<-.5
 assert v["max_CP_reversal_energy_error"]<1e-9
 assert v["gauge_conjugation_free_energy_residual"]<1e-9
def test_one_loop_local_fermionic_instability_competes_bosonic_stiffness(certs):
 c=certs["one_loop_competition"]
 assert c["finite_model"]["H1_dimension"]==3
 assert max(c["fermion_hessian_eigenvalues"])<0
 assert min(c["boson_hessian_eigenvalues"])>0
 assert 100<c["number_boson_weight_threshold_to_stabilize_trivial_holonomy"]<160
 assert c["sampled_CP_symmetric_line"][5]["fermion_F_minus_zero"]<-.4
def test_gravity_Uw_potential_cannot_repair_native_D(certs):
 n=certs["gravity_potential_no_go"]
 assert n["native_edges"]==160 and n["native_vertices"]==80
 C=n["nonzero_no_go_coefficient_C"]
 assert abs(C)>1
 z=n["native_H_vs_D_for_three_electric_scales"]
 assert z[1]-z[0]==pytest.approx(C)
 assert z[2]-z[0]==pytest.approx(4*C)
 assert "independent of E" in n["theorem"]
def test_quantum_rotor_spectral_ratios_dont_fix_g(certs):
 a=certs["coupling_chirality_gate"]
 assert a["near_exact_max_norm_identity"]<1e-12
 assert len(a["coupling_groups"])==3
 r=[q["first_5_gaps_over_first_gap"] for q in a["coupling_groups"]]
 for x in r[1:]:assert x==pytest.approx(r[0],abs=1e-9)
 assert [q["lambda_beta_over_g_fourth"] for q in a["coupling_groups"]]==pytest.approx([16]*3)
def test_balanced_spinless_bipartite_index_not_Weyl_family(certs):
 a=certs["coupling_chirality_gate"]["native_site_fermion"]
 assert a["bipartition_sizes"]==[40,40]
 assert a["positive_minus_negative_basis_index"]==0
 assert a["gamma_H_anticommutator_norm"]<1e-12
 assert a["spectrum_chiral_pairing_max_residual"]<1e-9
def test_no_invented_quantum_gravity_or_physical_SM(certs):
 a=certs["coupling_chirality_gate"]
 assert len(a["required_missing_physics"])==5
 assert "no physical" in a["scope"].lower() or "Does NOT imply" in a["scope"]
 assert "NOT" in certs["fermion_holonomy"]["important_boundary"]
 assert "does not exclude" in certs["gravity_potential_no_go"]["scope"].lower()
