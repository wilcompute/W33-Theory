"""TOE58 physics fronts: independent source regeneration and strict scope checks."""
from pathlib import Path
import subprocess,sys,json
import pytest
R=Path(__file__).resolve().parents[1]
NAMES=["three_octagons","overlap_index","graph_lapse_defect",
       "fermion_polarization","holonomy_phase_diagram"]
@pytest.fixture(scope="module")
def cert():
 for name in NAMES:
  cmd=[sys.executable,str(R/"analysis"/f"w33_20261013_toe58_{name}.py")]
  p=subprocess.run(cmd,cwd=R,capture_output=True,text=True,timeout=200)
  assert p.returncode==0,(name,p.stdout[-600:],p.stderr[-1800:])
 return {n:json.loads((R/"data"/f"w33_20261013_toe58_{n}.json").read_text()) for n in NAMES}
def test_three_native_quantum_octagons_gauge_and_coupling(cert):
 q=cert["three_octagons"]
 assert q["native_rows"]==1385
 assert q["native_sites"]==80 and q["native_links"]==160
 assert q["octagon_indices"]==[0,186,164]
 assert q["signed_Gram"]==[[8,-4,-4],[-4,8,4],[-4,4,8]]
 for key,rs in q["samples"].items():
  assert [s["dimension"] for s in rs]==[27,125,343]
  assert rs[2]["ground"]<=rs[1]["ground"]+1e-10
  assert abs(rs[2]["ground"]-rs[1]["ground"])<.15
  assert sorted(x for x in rs[-1]["Gauss_endpoint_charges"] if x)==([-1,1] if "open" in key else [])
def test_static_overlap_Wilson_mass_sweep_has_zero_index(cert):
 q=cert["overlap_index"]
 assert len(q["index_zero_cases"])==10
 assert {r["m0"] for r in q["index_zero_cases"]}=={.3,.5,1.5,3.,7.}
 assert all(r["index"]==0 and r["gap"]>1e-6 and r["anticommutator"]<1e-10 for r in q["index_zero_cases"])
 assert "time-dependent 4D" in q["physics_boundary"]
def test_low_graph_eigenmode_lapses_still_break_native_GR_closure(cert):
 q=cert["graph_lapse_defect"]
 assert q["max_actual_minus_target"]>1
 assert q["max_flat_metric_defect"]>1
 assert q["proportional_lapses_actual_max"]<1e-10
 assert q["proportional_lapses_target_max"]<1e-10
 assert q["exact_D_skew_max"]<1e-10
def test_fermion_one_loop_static_Ward_zero_modes_and_nonzero_physical_H1(cert):
 q=cert["fermion_polarization"]
 assert len(q["basis"])==7
 assert q["finite_U1_gauge_free_energy_residual"]<1e-10
 assert q["max_two_pure_gauge_rows_or_columns"]<1e-8
 assert q["bare_magnetic_harmonic_curl_norm"]<1e-8
 assert max(q["harmonic_Hessian_eigenvalues"])<-.05
 assert max(abs(v) for v in q["plaquette_Hessian_eigenvalues"])>.01
def test_temperature_mu_holonomy_corner_selection_not_CP_derivation(cert):
 q=cert["holonomy_phase_diagram"]
 assert len(q["fixed_external_mu_and_temperature_grid"])==28
 assert q["number_distinct_selected_pi_corners"]==2
 assert q["selected_pi_corners"]==[[0,0,0],[1,1,1]]
 assert q["half_filling_beta4_reproduces_prior11964"]["minimizing_pi_corner"]==[1,1,1]
 assert q["half_filling_beta4_reproduces_prior11964"]["zero_minus_min"]>.8
 assert "NOT" in q["limitation"]
def test_no_false_TOE_assertions(cert):
 assert "NOT" in cert["three_octagons"]["limitation"] or "not" in cert["three_octagons"]["limitation"]
 assert "time-dependent" in cert["overlap_index"]["physics_boundary"]
 assert "not" in cert["fermion_polarization"]["scope"]
