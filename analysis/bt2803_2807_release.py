#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data'
def load(n):return json.loads((DATA/n).read_text())
def main():
 a=load('PART_BT2803_MINIMAL_AFFINE_FRAME_ISA_results.json');m=load('PART_BT2804_M36_CLIFFORD_DECODER_DISTILLATION_results.json');s=load('PART_BT2805_N_QUTRIT_SENSOR_EXPONENT_results.json');t=load('PART_BT2806_TRANSPOSE_CX_Q5_Q7_results.json');r=load('w33_pass2206_rtl_reference.json')
 checks={'isa_sp43':a['linear_order']==51840,'isa_asp43':a['affine_order']==4199040,'isa_two_bit':len(a['selected_micro_isa'])==4,'m36_clifford_11520':m['clifford_group_order']==11520,'m36_orbits_960_2880_2880_640':sorted(x['size'] for x in m['m36_clifford_orbits'])==[640,960,2880,2880],'m36_deep_improving_48':m['grade_results']['deep']['improving_branches']==48,'m36_other_improving_zero':sum(m['grade_results'][k]['improving_branches'] for k in ('shallow','mid_a','mid_b'))==0,'m36_explicit_protocol':m['distillation_protocol']['decoder']=='Hadamard on second logical qubit','sensor_odd_3':s['minimal_law']['n_odd']==3,'sensor_even_9':s['minimal_law']['n_even']==9,'transpose_q5_inner':t['rows'][0]['projective_class']=='inner','transpose_q7_outer':t['rows'][1]['projective_class']=='outer diagonal','transpose_cx_conjugacy':all(row['checks']['cx_direction_conjugacy'] for row in t['rows']),'live_mixer_source':r['source']=='rtl/w33_pass2773_spread_mixer36_synth.sv','dead_mixer_absent':not (ROOT/'rtl/w33_spread_mixer36.sv').exists()}
 assert all(checks.values()),[k for k,v in checks.items() if not v]
 out={'schema':'w33.pass2803_2807.five_deep_frontiers.v1','status':'COMPLETE_EXACT_REMOTE_HARDWARE_PENDING','canonical_pass_range':'2803-2807','check_count':len(checks),'checks':checks,'headline':'The deep M36 grade is two-copy distillable under full logical Clifford decoding: 48 improving branches, with an explicit H-decoded protocol improving over the full magic-witness interval.','boundaries':{'m36':'state-fidelity distillation, not a fault-tolerant injection threshold or asymptotic yield theorem','sensor':'finite mu_12 Clifford lift; arbitrary U(1) phases require exponent 3^n','hardware':'synthesis and placement are promoted only after observed CI evidence'}}
 p=DATA/'PART_BT2803_BT2807_FIVE_DEEP_FRONTIERS_results.json';p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(f"PASS {len(checks)}/{len(checks)}")
if __name__=='__main__':main()
