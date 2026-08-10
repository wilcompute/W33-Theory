from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(n): return json.loads((ROOT/'data'/n).read_text(encoding="utf-8"))
def test_summary():
 d=load('PART_BT2967_BT2973_OPTIMAL_INFORMATION_SYSTEM_summary.json'); assert d['check_count']==7 and all(d['checks'].values())
def test_calibration_identifiability():
 d=load('PART_BT2967_OPTIMAL_INFORMATION_SYSTEM_results.json'); assert d['identifiability']['aggregate_correct_wrong_erasure_jacobian_rank']==2 and d['zero_observed_error_trials_needed_for_95pct_lower_bound_above_0p999_jeffreys']==1920
def test_d4_schedules():
 d=load('PART_BT2968_OPTIMAL_INFORMATION_SYSTEM_results.json'); assert d['single_edge_minimum_triangle_count']==23 and d['two_edge_constructive_triangle_count']==29 and d['full_triangle_hypotheses']==48826 and d['full_triangle_collisions']==0
def test_backend_pareto():
 d=load('PART_BT2969_OPTIMAL_INFORMATION_SYSTEM_results.json'); assert d['logical_network']['gate_count']==199 and d['logical_network']['Toffoli']==120 and d['logical_network']['CNOT']==79 and d['pareto_decision'].startswith('For the live Holonet')
def test_m36_recompile():
 d=load('PART_BT2970_OPTIMAL_INFORMATION_SYSTEM_results.json'); assert d['physical_gate_count']==9 and d['CNOT_count']==6 and d['H_count']==3 and d['fault_event_count']==101 and d['coefficients']['two_qubit']=='956/405'
def test_controller_group():
 d=load('PART_BT2971_OPTIMAL_INFORMATION_SYSTEM_results.json'); assert d['controller_group_order']==30233088 and d['route_subgroup_order']==192 and d['one_extra_symplectic_transvection']['generated_route_group']=='A40'
def test_minimal_automaton():
 d=load('PART_BT2972_OPTIMAL_INFORMATION_SYSTEM_results.json'); assert d['minimal_future_distinguishable_states']==6048 and d['fixed_width_bits']==13 and d['partition_refinement_history']==[60,1980,5616,6048,6048]
def test_curvature_clock():
 d=load('PART_BT2973_OPTIMAL_INFORMATION_SYSTEM_results.json'); assert d['clock_order']==12 and d['clock_cycle_count']==540 and d['generated_clock_group']=='D12 of order 24'
def test_rtl_sources():
 for rel,needle in [('rtl/w33_pass2970_m36_relabel_microcode.sv','module w33_pass2970'),('rtl/w33_pass2973_curvature_clock.sv','module w33_pass2973')]: assert needle in (ROOT/rel).read_text(encoding="utf-8")
