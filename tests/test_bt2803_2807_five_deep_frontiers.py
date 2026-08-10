import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/'data'/name).read_text(encoding="utf-8"))
def test_minimal_isa():
 d=load('PART_BT2803_MINIMAL_AFFINE_FRAME_ISA_results.json');assert d['linear_order']==51840;assert d['affine_order']==4199040;assert d['selected_micro_isa']==['F_p','CX_pf','CX_fp','Z_p'];assert d['word_lengths']['maximum']==17
def test_m36_distillation():
 d=load('PART_BT2804_M36_CLIFFORD_DECODER_DISTILLATION_results.json');assert d['clifford_group_order']==11520;assert sorted(x['size'] for x in d['m36_clifford_orbits'])==[640,960,2880,2880];assert d['grade_results']['deep']['improving_branches']==48;assert sum(d['grade_results'][k]['improving_branches'] for k in ('shallow','mid_a','mid_b'))==0;assert d['distillation_protocol']['target_id']==7
def test_sensor_exponent():
 d=load('PART_BT2805_N_QUTRIT_SENSOR_EXPONENT_results.json');assert d['minimal_law']=={'n_even':9,'n_odd':3};assert all(d['checks'].values())
def test_transpose():
 d=load('PART_BT2806_TRANSPOSE_CX_Q5_Q7_results.json');assert d['rows'][0]['projective_class']=='inner';assert d['rows'][1]['projective_class']=='outer diagonal';assert all(d['checks'].values())
def test_mixer_retirement():
 d=load('w33_pass2206_rtl_reference.json');assert d['source']=='rtl/w33_pass2773_spread_mixer36_synth.sv';assert d['status']=='PASS_SYNTHESIZABLE_RTL_REFERENCE';assert not (ROOT/'rtl/w33_spread_mixer36.sv').exists()
