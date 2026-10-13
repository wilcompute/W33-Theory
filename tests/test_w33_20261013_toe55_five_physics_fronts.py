"""TOE55 five-front native W33 physics gates and negative controls."""
from pathlib import Path
import json,sys,subprocess
import pytest
R=Path(__file__).resolve().parents[1]
scripts=["w33_20261013_toe55_native_matter_gauge.py",
         "w33_20261013_toe55_gravity_chirality.py",
         "w33_20261013_toe55_free_bloch_scaling.py",
         "w33_20261013_toe55_common_action_audit.py"]
names=["native_matter_gauge","linear_spin2_constraints","anomaly_deformation",
       "free_bloch_scaling","five_front_physical_gate"]
@pytest.fixture(scope="module")
def data():
 for name in scripts:
  q=subprocess.run([sys.executable,str(R/"analysis"/name)],cwd=R,
           capture_output=True,text=True,timeout=120)
  assert q.returncode==0,(name,q.stdout[-700:],q.stderr[-1300:])
 return {k:json.loads((R/"data"/f"w33_20261013_toe55_{k}.json").read_text())
         for k in names}
def test_native_W33_full_plaquette_gradient_gauge_identity(data):
 s=data["native_matter_gauge"]
 assert (s["w33_native_sites"],s["w33_native_links"])==(80,160)
 assert s["plaquette_rows"]>1300
 assert s["max_plaquette_gradient_residual"]<1e-13
 assert s["sample"]["max_energy_change_under_finite_gauge_transform"]<1e-9
 assert s["sample"]["max_gauss_residual"]<1e-11
def test_native_U1_matter_coupling_Ward_and_continuous_coupling(data):
 s=data["native_matter_gauge"]
 assert len(s["gauge_orbit_trials"])==3
 assert all(abs(s["sample"][f"ward_derivative_g_{g}"])<1e-8 for g in (.1,.3,.7))
 assert len(set(round(x,7) for x in s["free_gauge_coupling_values_hopping_energy"].values()))==3
def test_linearized_gravity_four_first_class_two_TT_dof(data):
 g=data["linear_spin2_constraints"]
 assert g["canonical_spatial_h_components"]==g["canonical_pi_components"]==6
 assert g["analytic_H_vs_momentum_poisson_bracket_matrix"]=="Matrix([[0, 0, 0]])"
 assert g["TT_projector_rank_at_k_1_2_3"]==2
 assert g["TT_gauge_shift_exactly_zero"]
 assert "NOT derived from W33" in g["model"]
def test_chiral_SM_with_neutrino_anomaly_continuum(data):
 a=data["anomaly_deformation"]
 assert a["SU3_cubic_anomaly"]==a["SU3_sq_U1_anomaly"]==a["SU2_sq_U1_anomaly"]=="0"
 assert a["gravitational_U1_anomaly"]==a["U1_cubed_anomaly"]=="0"
 assert a["SU2_Witten_doublet_count"]==4
 assert a["nonstandard_neutrino_electric_charge"]=="-1/7"
 assert a["control_SU2_sq_U1_anomaly_nonzero"]=="1/4"
def test_lorentz_formal_a2_nontrivial_six_direction_scaling(data):
 t=data["free_bloch_scaling"]
 assert t["n_directions"]==6
 for x in t["per_direction"]:
  assert [row["a"] for row in x["sequence"]]==[1.,.5,.25]
  assert all(abs(r-.25)<.008 for r in x["mean_speed_error_halving_ratios"])
  assert all(.1<r<.45 for r in x["polarization_split_halving_ratios"])
def test_unpredicted_alpha_and_NIST_prior_control(data):
 a=data["five_front_physical_gate"]
 assert a["uncorrected_discrepancy_sigma_if_treated_as_exact"]>210
 assert 137.03599917<a["CODATA2022_NIST_inverse_alpha"]<137.036
 assert 137.0360035<a["bare_W33_inverse_alpha_decimal"]<137.0360037
 assert "TOE40" in a["prior_repo_owner_alpha"]
def test_common_classical_action_not_spin2_or_standard_model(data):
 z=data["five_front_physical_gate"]
 assert z["canonical_configuration_variables"]["total"]==480
 assert z["constraints"]["charged_local_U1_first_class"]==80
 assert z["constraints"]["physical_configuration_count_at_generic_scalar_configuration_after_U1_reduction"]==400
 assert z["constraints"]["native_gravitational_Hamiltonian_and_spatial_diffeomorphism"]==0
 assert z["link_weight_momentum_Hessian"]["full_rank"]==160
 assert len(z["five_front_gate_status"])==5
def test_no_complete_TOE_false_positive(data):
 assert "not a" in data["native_matter_gauge"]["scope"].lower() or "no Lorentzian" in data["native_matter_gauge"]["scope"]
 assert "not established" in data["five_front_physical_gate"]["lattice_to_QED_normalization_warning"]
 assert "NOT derived from W33" in data["linear_spin2_constraints"]["model"]
