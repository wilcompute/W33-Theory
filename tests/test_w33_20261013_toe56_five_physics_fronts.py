"""TOE56 native five physics fronts: regenerate ALL source-derived certificates."""
from pathlib import Path
import json,subprocess,sys
import pytest
R=Path(__file__).resolve().parents[1]
scripts=["compact_u1","rotor_chirality","gravity_interaction","coupling_unification"]
certs={"compact":"compact_u1","rotor":"rotor_chirality",
"gravity":"dynamical_gravity_and_interaction","gates":"five_physics_gates"}
@pytest.fixture(scope="module")
def results():
 for name in scripts:
  p=subprocess.run([sys.executable,str(R/"analysis"/f"w33_20261013_toe56_{name}.py")],
      cwd=R,text=True,capture_output=True,timeout=150)
  assert p.returncode==0,(name,p.stdout[-500:],p.stderr[-1400:])
 return {k:json.loads((R/"data"/f"w33_20261013_toe56_{n}.json").read_text())
         for k,n in certs.items()}
def test_exact_native_compact_chain_and_three_holonomy_directions(results):
 d=results["compact"]
 assert d["native_W33_dimensions"]=={"sites":80,"edges":160,"plaquettes":1385,
 "rank_gradient":79,"rank_plaquette":78,"first_cohomology":3}
 assert d["native_complex_exact_PB_max"]==0
 assert d["first_cohomology"]["P_H_residual"]<1e-8
 assert d["first_cohomology"]["Bt_H_residual"]<1e-8
def test_quadratic_TOE55_magnetic_term_fails_compact_large_gauge(results):
 d=results["compact"]["compact_link_2pi_shift"]
 assert d["quadratic_breaking"]>1
 assert d["compact_absolute_difference"]<1e-10
def test_compact_U1_and_holonomy_physical_scaffold(results):
 d=results["compact"]
 assert d["native_local_gauge"]["charged_matter_hopping_difference"]<1e-10
 assert d["native_local_gauge"]["large_link_shift_hopping_difference"]<1e-10
 assert d["first_cohomology"]["charged_hopping_harmonic_shift_difference"]>.001
 a=d["harmonic_quadratic_recovery_relative_errors"]
 assert abs(a[1]/a[0]-.25)<.02 and abs(a[2]/a[1]-.25)<.02
def test_quantum_flux_Gauss_superselection_and_bare_g(results):
 v=results["rotor"]
 assert v["selected_native_local_plaquette_length"]==8
 assert v["int_boundary_of_native_loop_zero"]==0
 s=v["quantum_sector_spectra"]
 assert len(s)==6
 assert all(z["lowest_energy"]>0 and z["first_excited_gap"]>0 for z in s.values())
 assert abs(s["neutral_0.3"]["lowest_energy"]-s["neutral_1.1"]["lowest_energy"])>.01
 assert sum(abs(x) for x in s["open_0.3"]["flux_sector_endpoint_charge"])==2
def test_rectangular_incidence_index_not_physical_Weyl(results):
 v=results["rotor"]["native_bloch_chiral_index"]
 assert len(v)==2
 assert [(z["rank_incidence"],z["vertex_positive_chiral_zero_modes"],
          z["edge_negative_chiral_zero_modes"],z["index"]) for z in v]==[
          (79,1,81,-80),(80,0,80,-80)]
def test_candidate_native_link_scaling_constraint_fails(results):
 v=results["gravity"]["candidate_diffeo_poisson"]
 assert v["verdict"].startswith("NOT_FIRST_CLASS")
 assert abs(v["analytic_H_vs_D"]-v["finite_difference_H_vs_D"])<1e-8
 assert abs(v["H_vs_D_on_U1_Gauss_surface"])>.001
def test_interacting_compact_Wilson_has_quartic_and_gauge_free_hessian(results):
 a=results["gravity"]["compact_B_interaction"]
 assert a["exact_quartic_coefficient"]<0
 assert a["quartic_finite_difference"][-1]["relative_error_vs_exact_taylor"]<.004
 assert a["max_background_hessian_times_gradient_residual"]<1e-10
 v=results["gates"]
 assert v["beta_1_compatible_nonzero_spectrum"]["number_positive"]==78
 r=v["bare_parameter_grid"]
 assert (r["1.0,0.7"]["quartic_compact_self_interaction_amplitude"]/
         r["0.5,0.7"]["quartic_compact_self_interaction_amplitude"])==pytest.approx(4.)
 assert r["0.25,0.7"]["analytic_bare_quadratic_Hessian_direction"]==pytest.approx(
        r["1.0,0.7"]["analytic_bare_quadratic_Hessian_direction"])
def test_conditional_nonlinearity_smooth_flux_a4(results):
 d=results["gravity"]["conditional_a2_flux_scaling"]
 assert len(d["a_values"])==3
 assert all(abs(x-1/16)<.004 for x in d["error_halving_ratios"])
 assert "ASSUMED" in d["hypothesis"]
def test_five_physics_fronts_do_not_overclaim_TOE(results):
 s=results["gates"]
 assert s["n_common_physics_gates_met"]==1
 assert len(s["required_gates"])==6
 assert s["minimum_number_of_external_bare_scalar_parameters"]==7
 assert "not" in s["important_scope"].lower() or "No physical TOE" in s["important_scope"]
