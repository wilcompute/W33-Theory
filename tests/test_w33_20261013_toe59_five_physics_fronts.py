"""TOE59: source-regenerated physics acceptance tests, no fake TOE claims."""
from pathlib import Path
import json,sys,subprocess
import pytest
R=Path(__file__).resolve().parents[1]
producers=[
 "wilson_girth_moments","eight_cycle_census","highT_winding",
 "flux_error_bound","external_4d_flux_gate","longwave_leibniz",
 "lorentz_velocity_gate",
]
@pytest.fixture(scope="module")
def cert():
 for n in producers:
  p=subprocess.run([sys.executable,str(R/"analysis"/f"w33_20261013_toe59_{n}.py")],
       cwd=R,capture_output=True,text=True,timeout=110)
  assert p.returncode==0,(n,p.stdout[-1500:],p.stderr[-2500:])
 return {n:json.loads((R/"data"/f"w33_20261013_toe59_{n}.json").read_text()) for n in producers}
def test_native_pi_winding_minimal_octagon(cert):
 rows=cert["wilson_girth_moments"]["tested_corners"]
 assert len(rows)==8
 assert rows[0]["first_flux_sensitive_moment"] is None
 for r in rows[1:]:
  assert r["shortest_nontrivial_winding_length"]==8
  assert r["first_flux_sensitive_moment"]==8
  assert r["trace_moment_difference"]<0
  assert all(v==0 for k,v in r["delta_at_even_lengths"].items() if int(k)<8)
def test_independent_cycle_census_exact_trace_moments(cert):
 c=cert["eight_cycle_census"]
 assert c["all_undirected_simple_eight_cycles"]==1620
 assert c["TOE38_octs_len"]==1382
 assert c["zero_integer_winding_cycles"]==1382
 assert c["nonzero_integer_winding_cycles"]==238
 assert sum(c["mod2_winding_counts"].values())==1620
 assert "all eight" in c["fourier_oriented_trace_check"]
def test_fermion_high_temperature_coefficient_exact(cert):
 c=cert["highT_winding"]
 assert c["native_P_times_deck_voltages_max"]==0
 assert c["exact_fermion_free_energy_series_coeff_of_beta7_traceH8"]=="17/645120"
 rows=c["winding_moment_rows"]
 assert rows[-1]["leading_coefficient_float"]==pytest.approx(-.1964781746031746)
 for r in rows[1:]:
  assert r["leading_coefficient_float"]<0
  assert r["temperature_checks"][0]["fractional_deviation_from_leading"]<.04
  assert all(x["free_energy_difference"]<0 for x in r["temperature_checks"])
def test_three_loop_infinite_flux_error_bound(cert):
 q=cert["flux_error_bound"]
 assert q["minimum_flux_quadratic_eigenvalue"]==pytest.approx(4.0,abs=1e-12)
 intervals=q["rigorous_intervals"]
 assert len(intervals)==2
 for r in intervals:
  assert 0<r["combined_best_lower_bound"]<r["best_upper_bound"]
  assert r["bound_rows"][2]["error_width_upper"]<r["bound_rows"][1]["error_width_upper"]
 assert intervals[0]["combined_best_lower_bound"]==pytest.approx(3.3462780288114065)
 assert intervals[1]["combined_best_lower_bound"]==pytest.approx(2.25435263552348)
def test_external_four_torus_index_needs_topology(cert):
 c=cert["external_4d_flux_gate"]
 assert c["sites"]==81
 assert [r["U1_second_Chern_character"] for r in c["records"]]==[1,0,-1,1]
 assert max(r["gauge_curvature_residual"] for r in c["records"])<1e-12
 assert "EXTERNAL CONTROL" in c["native_boundary"]
def test_W33_low_momentum_Leibniz_error_decays(cert):
 c=cert["longwave_leibniz"]
 assert len(c["records"])==4
 assert all(.49<x<.51 for x in c["halving_ratios"])
 assert c["records"][-1]["physical_Leibniz_rms"]<c["records"][0]["physical_Leibniz_rms"]/7
 assert "NOT" in c["interpretation"]
def test_photon_spinor_speed_needs_bare_tuning(cert):
 c=cert["lorentz_velocity_gate"]
 assert c["photon_low_k_mean_speed_squared"]==pytest.approx(2.,abs=.001)
 assert len(c["matched_bare_parameter_pairs"])==2
 assert sorted(r["electric_epsilon"] for r in c["matched_bare_parameter_pairs"])==[1.,2.]
 assert c["static_one_loop_gauge_Ward_residual"]<1e-8
 assert "not a new interacting" in c["limitation"]
def test_no_physical_TOE_overclaim(cert):
 assert "not physical 4D" in cert["wilson_girth_moments"]["limits"]
 assert "full W33" in cert["flux_error_bound"]["limits"]
 assert "not an executed nonzero overlap index" in cert["external_4d_flux_gate"]["prior_art"]
