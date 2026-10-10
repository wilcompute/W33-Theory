from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/'data'/name).read_text())
def test_m36_symmetry():
 d=load('PART_BT3003_M36_SYMMETRY_ORBIT_results.json');assert d['three_copy_local_wreath_symmetry_order']==34992 and d['pilot_candidates_one_orbit'] and d['pilot_candidate_orbit_size']==729 and d['copy_permutation_pivot_orbits']==98
def test_d4_28():
 d=load('PART_BT3004_D4_TWO_EDGE_SCHEDULE_results.json');assert d['triangle_count']==28 and d['hypotheses']==48826 and d['full_group_valued_syndromes_unique']
def test_a4_shell():
 d=load('PART_BT3005_GOLDEN_A4_SHELL_results.json');assert d['a4_order']==12 and d['scheduler']['pulses_per_period']==89 and d['scheduler']['cyclic_no_adjacent_expensive_slots']
def test_clock_flags():
 d=load('PART_BT3006_CLOCK_FLAG_BRIDGE_results.json');assert d['geometry']['total_flags']==6480 and d['group_action']['flag_orbit']==6480 and d['clock_test']['semiregular_12_power_540_elements']==0
def test_receiver():
 d=load('PART_BT3007_COMPONENT_SEQUENTIAL_CHIRALITY_results.json');r=d['copy_cost_rows']['0.001'];assert r['success_probability']>.996 and 7<r['expected_copies']<8
def test_tetrahedral_shell():
 d=load('PART_BT3008_TETRAHEDRAL_A4_SIC_results.json');assert d['orientation_preserving_symmetry_count']==12 and abs(d['rows']['1']['single_copy_success']-.5)<1e-12
def test_calendar():
 d=load('PART_BT3009_D12_STURMIAN_CALENDAR_results.json');assert d['superperiod']==2796 and set(d['events_by_d12_phase'].values())=={89} and d['time_reversal_cyclic_shifts']==[89]
def test_summary():
 d=load('PART_BT3003_BT3009_SEVEN_FRONT_summary.json');assert d['check_count']==7 and all(d['checks'].values())
