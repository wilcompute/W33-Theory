#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
J=json.loads((R/'data/PART_W33_PASS5174_5181_RESULTS.json').read_text())

def check():
    assert J['range']==[5174,5181]
    assert J['5174']['spectral_gap']=='q'
    assert J['5174']['second_adjacency_eigenvalue']=='3q-4'
    assert J['5175']['anchors']['8']==[1,28,343,2548,1176]
    assert J['5176']['connected_weight6_rooted_sets']==11401011
    assert J['5176']['false_first_corrections']==0
    assert J['5176']['global_guaranteed_error_weight']==6
    assert J['5177']['component_states_exhausted']==33554432
    assert J['5177']['old_P_candidate_h8_2_h9_1_possible'] is False
    assert J['5177']['minimum_positive_P_active_chart_defect']==10
    assert J['5178']['remainders_r0_to_r8']==[0,0,0,0,0,16,64,176,384]
    assert J['5179']['q5_minimum_shell_size']==36
    assert J['5180']['atom_owner_multiplicity']==2
    assert J['5181']['anchors']['q5'].startswith('P=325')
    assert 'L-heavy-only' in J['boundary']
    return True
if __name__=='__main__':check();print('PASS5174-5181 regression: PASS')
