from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):return json.loads((ROOT/'data'/name).read_text(encoding="utf-8"))
def test_release_summary():
 d=load('PART_BT2946_BT2952_SEVEN_FRONT_CLOSURE_summary.json');assert d['check_count']==8 and all(d['checks'].values())
def test_affine_optimum():
 d=load('PART_BT2946_AFFINE_SUPPORT_OPTIMUM_results.json');assert d['minimum_length']==15 and d['checks']['n14_double_infeasible']
def test_compiled_m36():
 d=load('PART_BT2947_M36_COMPILED_BRANCH_results.json');assert d['primitive_gate_count']==15 and d['measurement_count']==2 and d['output_ray']==7 and d['coefficients']=={'input':'2/3','measurement':'4/9','one_qubit':'140/81','two_qubit':'2084/405'}
def test_oam_fabric():
 d=load('PART_BT2948_OAM_SPREAD_FABRIC_results.json');assert d['registers']=={'addresses':40,'oam_line_modes':10,'time_or_frequency_slots':4};assert d['triangle_holonomy_cycle_histogram']=={'2-1-1':60,'2-2':60}
def test_reversible_transcript():
 d=load('PART_BT2949_REVERSIBLE_TRANSCRIPT_results.json');assert d['permutation_size']==256 and d['known_zero_high_bit_on_valid_inputs'];assert d['cycle_length_histogram']=={'6':1,'43':1,'74':1,'133':1};assert d['valid_codewords']==81 and d['invalid_output_range']==[81,255]
def test_ternary_classification():
 d=load('PART_BT2950_TERNARY_844_CLASSIFICATION_results.json');assert d['covering_radius']==2 and d['lcd'] and d['projective_hyperplane_spectrum']==[3,4,10,12,11]
def test_quarter_turn():
 d=load('PART_BT2951_ISODUAL_OAM_QUARTER_TURN_results.json');assert d['algebra']=='D^2=-I, D^4=I' and all(d['checks'].values())
def test_joint_rank_and_rtl_sources():
 d=load('PART_BT2952_ROUTER_OBSERVER_FUSION_results.json');assert d['valid_joint_states']==3240 and d['fixed_width_joint_bits']==12 and d['strategies'][1]['fixed_bit_saving']==9
 for rel,needle in [('rtl/w33_pass2947_m36_branch_microcode.sv','module w33_pass2947'),('tools/gen_bt2948_oam_router_rtl.py','generated 90 directed'),('analysis/bt2949_reversible_transcript_codec.py','PASS 256/256'),('rtl/w33_pass2951_isodual_quarter_turn.sv','module w33_pass2951'),('rtl/w33_pass2952_joint_rank_codec.sv','module w33_pass2952')]:assert needle in (ROOT/rel).read_text(encoding="utf-8")
