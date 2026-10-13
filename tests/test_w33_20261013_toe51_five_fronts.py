"""TOE51 five-front independent producer and certificate regressions."""
import json,sys,subprocess
from pathlib import Path
import pytest
R=Path(__file__).resolve().parents[1]
sources=["w33_20261013_toe51_physics_three_fronts.py",
 "w33_20261013_toe51_spectral_moment_rank.py",
 "w33_20261013_toe51_covariant_dual_compiler.py"]
certnames=["color_threshold_domain","lepton_branch_observables","dynamic_metric_gauss",
 "spectral_moment_rank","covariant_dual_compiler"]
@pytest.fixture(scope="module")
def data():
 for name in sources:
  q=subprocess.run([sys.executable,str(R/"analysis"/name)],cwd=R,
       stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=160)
  assert q.returncode==0,(name,q.stdout[-900:],q.stderr[-1200:])
 return {key:json.loads((R/"data"/f"w33_20261013_toe51_{key}.json").read_text())
           for key in certnames}
def test_bloch_spectral_rank_and_analytic_moment_gradients(data):
 x=data["spectral_moment_rank"]
 assert x["status"]=="PASS" and x["acoustic_rank"]==6
 assert x["spectral_moment_count"]==12
 assert x["joint_local_gradient_rank_1e_minus8"]==18
 assert x["nullity_after_local_linear_probes"]==142
 assert x["max_relative_check_error"]<1e-6
 assert len(x["finite_difference_checks"])==9
def test_color_threshold_domain_breakdown(data):
 x=data["color_threshold_domain"]
 assert x["status"]=="PASS"
 assert 0<x["benchmark"]["min_heavy_over_strong_equals_1_at_abs_z"]<.1
 assert x["trials"][0]["controlled_threshold"] is True
 assert x["trials"][-1]["controlled_threshold"] is False
 assert abs(x["trials"][3]["heavy_over_strong"]-1)<1e-10
def test_fitted_neutrino_branches_are_not_unique(data):
 x=data["lepton_branch_observables"]
 assert x["status"]=="PASS"
 assert x["n_branches"]==5
 assert all(z["within_free_phase_envelope"] for z in x["branches"])
 assert all(0<=z["m_ee_eV"]<.02 for z in x["branches"])
 assert len({round(z["delta_deg"],2) for z in x["branches"]})==3
 assert max(z["total_masses_eV"] for z in x["branches"])-min(z["total_masses_eV"] for z in x["branches"])>.005
def test_covariant_dual_decoder_and_noise(data):
 x=data["covariant_dual_compiler"]
 assert x["status"]=="PASS"
 assert x["n_checked_Sp4_generator_actions"]==7
 assert x["n_random_covariance_checks"]==80
 assert x["max_covariance_error"]<1e-10
 assert x["max_signal_reconstruction_error"]<1e-10
 assert abs(x["simulated_mean_squared_l2_noise"]/x["analytic_mean_squared_l2_noise"]-1)<.15
 assert x["linear_storage_dimension_K81"]==81
 assert "NOT CONSTRUCTED" in x["physical_K81_intertwiner_status"]
def test_native_canonical_weight_scalar_gauss_but_not_gravity(data):
 x=data["dynamic_metric_gauss"]
 assert x["status"]=="PASS" and x["full_native_links"]==160
 assert x["gauss_initial_inf_error"]<1e-8
 assert x["gauss_time_derivative_inf_error"]<1e-8
 assert x["magnetic_gauge_identity_inf_error"]<1e-8
 assert all(q["physical_positive_mass"] for q in x["test_single_link_equilibria"])
 assert x["test_single_link_equilibria"][-1]["equilibrium_weight"]>1
