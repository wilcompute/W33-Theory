#!/usr/bin/env python3
"""Compact deterministic regression lock for Passes 5066-5073."""
from __future__ import annotations
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
J=json.loads((R/'data/PART_W33_PASS5066_5073_RESULTS.json').read_text())
assert J['status']=='PASS_WITH_OPEN_Q4_SHELL_AND_ALL_Q_DISTANCE'
assert J['5066']['W3q']['theta_generates_full_dual'] is True
assert J['5067']['status']=='UNKNOWN'
assert J['5067']['generator_kernel_dimension']==169
assert J['5067']['model_425']['result']=='TIME_LIMIT_NO_INCUMBENT'
assert J['5067']['model_256']['result']=='TIME_LIMIT_NO_INCUMBENT'
assert J['5068']['subdivision_2_height_dimensions']==[81,29,29,23,1,1,0]
assert J['5068']['spaces']==['H1_81','Bike29','Bike29','W23','J','J','0']
assert J['5069']['outer_split']==[2,3]
assert J['5069']['commute'] is True
assert J['5070']['smith_floor_raw_basis']['inverse_denominator']==780
assert J['5070']['raw_subset_gap'] is False
assert J['5071']['identity']=='A10*S = S*(B2-4I)'
assert J['5072']['orders']=={'H':16,'N_PSp_H':32,'N_PGSp_H':64}
assert J['5072']['quotient']=='N_PGSp(H)/H ~= V4'
assert J['5073']['tanner_6_cycles']==1170000
# Cross-check frozen earlier owners rather than duplicating them.
P51=json.loads((R/'data/PART_W33_PASS5051_Q_FAMILY_THETA_CODE.json').read_text())
assert P51['q2']['code']==[90,16,16] and P51['q3']['code']==[1620,81,81]
P31=json.loads((R/'data/PART_W33_PASS5031_CRITICAL_GROUPS.json').read_text())
assert P31['all_edge_subdivision']['critical_group']=={'2':52,'8':6,'80':22,'320':1}
print('PASS 5066-5073')
