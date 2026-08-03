import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(n):return json.loads((ROOT/'data'/n).read_text())
def test_m36_no_go():
 d=load('PART_BT2772_M36_4_2_STABILIZER_CENSUS_summary.json');assert d['search_space']['branches']==21420;assert {r['grade']:r['m36_closed_branches'] for r in d['rows']}=={'shallow':35,'deep':237,'mid':11};assert all(r['certified_nonimproving_branches']==r['m36_closed_branches'] for r in d['rows'])
def test_sensor():
 d=load('PART_BT2773_METAPLECTIC_INTERFEROMETER_summary.json');assert (d['class_count'],d['theta_pair_count'])==(34,33);assert d['shots_per_quadrature_hoeffding']==29579
def test_compiler():
 d=load('PART_BT2774_STRUCTURED_CX_COMPILER_summary.json');assert d['checks']=={'all_pairs_present':True,'all_rewrites_verified':True,'group_elements':51840};assert d['memory_bits']['compression_ratio']>40
def test_repeater():
 d=load('PART_BT2776_REPEATER_REMOTE_SUM_summary.json');assert d['isotropic_recurrence']['fixed_points']==[1/9,1/3,1.0];r=d['scenario_summary']['1280']['best_distillable_rate'];assert r['segments']==8 and r['distillable']
def test_release():
 d=load('PART_BT2772_BT2776_FIVE_FRONTIERS_results.json');assert d['check_count']==19 and all(d['checks'].values())
