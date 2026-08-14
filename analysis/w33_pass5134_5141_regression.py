#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
J=json.loads((R/'data/PART_W33_PASS5134_5141_RESULTS.json').read_text())

def check():
    assert J['range']==[5134,5141]
    assert J['5134']['sharp_adjacent_pair_cap']==27
    assert J['5134']['delsarte_distance_counts']==[27,73,53,0]
    assert J['5134']['second_order_weight_lower_bound']==320
    assert J['5135']['minimal_exotic_profile']=={'h8':2,'h9':1,'A_type':248,'T_type':2472,'defect':28}
    assert J['5136']['decoder_guaranteed_radius']==5
    assert J['5136']['weight6_counterexample']==[1,2,3,6,27,54]
    assert J['5136']['false_center']==0
    assert J['5137']['all_q_linear_sector']['multiplicities']==['1','2(q-1)','(q-1)^2']
    assert J['5137']['uniform_nonlinear_gap_proof'] is False
    assert J['5139']['minimum_word_count']=='2(q+1)(q^2+1)'
    assert J['5140']['triple_intersection_law']['(1,1,2)']=='q^2'
    assert J['5140']['triple_intersection_law']['other']=='0'
    assert J['5141']['family_status']=='CONJECTURAL_BEYOND_ANCHORS'
    assert 'distance remains open' in J['boundary']
    return True

if __name__=='__main__':
    check();print('PASS5134-5141 regression: PASS')
