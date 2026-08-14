#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
J=json.loads((R/'data/PART_W33_PASS5158_5165_RESULTS.json').read_text())

def check():
    assert J['range']==[5158,5165]
    assert J['5158']['integer_weight_lower_bound']==641
    assert J['5158']['strict_counterexample_leader_at_least']==22
    assert J['5159']['q5_rooted_histogram']=={'1':19375,'5':500}
    assert J['5159']['nonconstant_signature_classes']==0
    assert J['5160']['radius5_failures']==0
    assert J['5160']['radius5_max_sweeps']==3
    assert J['5160']['centered_weight6_motifs']==32
    assert J['5160']['centered_weight6_motifs_repaired']==32
    assert J['5160']['global_radius6_proved'] is False
    assert J['5161']['strict_counterexample_leader_at_least']==23
    assert J['5161']['sector_weight_lower_bounds']['33']==668
    assert J['5162']['dependency_code_second_weight']=='2q'
    assert J['5163']['strict_counterexample_leader_at_least']==24
    assert min(J['5163']['sector_weight_lower_bounds'].values())>=760
    assert J['5164']['actual_W40_P4_lower']==97
    assert J['5164']['W40_integer_weight_lower_bound']==629
    assert J['5164']['strict_counterexample_leader_at_least']==25
    assert J['5165']['q3_anchor']==[1,8,32,40]
    assert J['requested_front_audits']['q5_exotic_625_profile']['profile_eliminated'] is False
    assert J['requested_front_audits']['all_q_nonlinear_theta_gap']['duplicated_here'] is False
    assert 'leaders >=25' in J['boundary']
    return True

if __name__=='__main__':
    check();print('PASS5158-5165 regression: PASS')
