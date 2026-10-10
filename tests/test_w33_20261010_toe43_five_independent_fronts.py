"""TOE43 five independently reproducible fronts, with explicit scientific firewalls."""
from pathlib import Path
import subprocess,json,sys,math
ROOT=Path(__file__).resolve().parents[1]
def run(stem,cert):
 p=subprocess.run([sys.executable,str(ROOT/"analysis"/stem)],cwd=ROOT,
  capture_output=True,text=True,timeout=100)
 assert p.returncode==0,(stem,p.stdout[-1500:],p.stderr[-1800:])
 return json.loads((ROOT/"data"/cert).read_text())
def test_field9_elementary_abelian_SIC_48_nonconvex_searches():
 d=run("w33_20261010_toe43_field9_sic_search.py",
       "w33_20261010_toe43_sic_search.json")
 assert d["search_restarts"]==48
 assert d["status"]=="NO_FIDUCIAL_FOUND_NOT_A_PROOF"
 assert d["best_sum_squared_residual"]>0
 assert d["best_sum_squared_residual"]<.05
 assert d["best_purity_variance"]<8/75
 assert len(d["best_state"])==9
def test_complete_10_MUB_purity_collision_protocol_and_readout_calibration():
 d=run("w33_20261010_toe43_purity_mub_protocol.py",
       "w33_20261010_toe43_purity_shots.json")
 assert d["complete_W33_line_count"]==40
 assert len(d["chosen_symplectic_spread_line_indices"])==10
 assert sorted(p for L in d["line_point_sets"] for p in L)==list(range(40))
 for states in d["states"].values():
  for v in states.values():
   assert v["total_copies"]==3200
   assert abs(v["mean_error"])<.02
   assert .7<(v["monte_carlo_standard_error"]/v["predicted_standard_error"])**2<1.3
 assert abs(d["states"]["stabilizer"]["0.0"]["true_purity"]-1)<1e-12
 assert d["states"]["stabilizer"]["0.0"]["ideal_entangling_swap_test_se_same_copy_budget"]==0
def test_native_E6_fixed_layout_proxy_all_520_schedules():
 d=run("w33_20261010_toe43_e6_layout_proxy.py",
       "w33_20261010_toe43_e6_hardware.json")
 assert len(d["all_520_schedule_metrics"])==520
 assert d["old_TOE41_schedule"]["peak_grid_mst_load"]==74
 assert d["old_TOE41_schedule"]["peak_ring_mst_load"]==119
 assert d["old_TOE41_schedule"]["site_sign_flips"]==57
 assert d["minimum_peak_grid_load"]==69
 assert d["minimum_peak_ring_load"]==113
 assert d["minimum_sign_switches"]==38
 assert d["pareto_front_count"]>0
 assert len(d["lexicographic_grid_ring_sign_optimum"]["order"])==5
def test_equal_global_purity_cptp_noise_channels_and_Pminus():
 d=run("w33_20261010_toe43_equal_purity_noise.py",
       "w33_20261010_toe43_noise_fingerprints.json")
 norms=[]
 for v in d["channels"].values():
  assert abs(v["purity"]-.5)<1e-12
  assert abs(v["graph_deficit_sum"]+45)<1e-9
  norms.append(v["minus4_norm"])
 assert min(norms)<1e-10
 assert max(norms)>.9
 assert len(set(round(v,6) for v in norms))==4
def test_E8_cartan_vector_loop_shape_and_24_unbroken_generators():
 d=run("w33_20261010_toe43_e8_vector_cw_audit.py",
       "w33_20261010_toe43_e8_one_loop_audit.json")
 assert d["generator_count"]==80
 for k in range(4):
  w=d["cases"][f"witting_{k}"]
  assert w["unbroken_gauge_bosons"]==24
  assert abs(w["cw_vector_log_shape"]+6*math.log(3))<1e-10
 for k in range(8):
  assert d["cases"][f"generic_{k}"]["unbroken_gauge_bosons"]==0
 assert d["trace_Q2_spread_across_samples"]<1e-10
 assert d["cw_log_shape_spread"]>.3
