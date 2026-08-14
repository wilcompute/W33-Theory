#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
J=json.loads((R/'data/PART_W33_PASS5214_5221_RESULTS.json').read_text())

def check():
    assert J['range']==[5214,5221]
    assert J['5214']['global_solutions']==6
    assert J['5214']['constraint_arity']=={'unary':17250,'binary':7500,'higher':0}
    assert J['5215']['connected_orbit_counts']==[1,5,57,1043,25929,734414]
    assert J['5215']['weight7_extensions_tested']==64439500
    assert J['5215']['global_guaranteed_error_weight']==7
    assert J['5216']['q3']['vertices']==540 and J['5216']['q5']['vertices']==9750
    assert J['5217']['outer_shell_distinct_atoms']==16 and J['5217']['complement_atoms']==9
    assert J['5218']['leader36_closed'] is False
    assert J['5219']['fundamental_L_triangle_syndrome_weight_each']==664
    assert J['5220']['q5']=={'atom_variables':11700,'internal_relations':3575,'P_side_dimension':8125,'L_rank':7500,'code_dimension':625}
    assert J['5221']['q5']['nullity_A']==2676 and J['5221']['q5']['nullity_A_plus_I']==2859
    assert 'leader36' in J['boundary'] and 'distance25' in J['boundary'].replace(' ','')
    return True

if __name__=='__main__':
    check();print('PASS5214-5221 regression: PASS')
