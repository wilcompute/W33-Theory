#!/usr/bin/env python3
"""Compact regression lock for Passes 5074-5081."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
J=json.loads((R/'data/PART_W33_PASS5074_5081_RESULTS.json').read_text())
assert J['status']=='EXECUTED_WITH_OPEN_ALL_Q_DISTANCE_AND_Q4_FULL_SHELL'
assert J['5074']['remaining_target']=='A(y) >= 4 q^3 for every non-cut cochain'
assert J['5074']['chamber_star']['active_charts']=='4q^3'
assert J['5075']['V11']=='three-term Sh_1 boundary reduces mod2 to point-opposite theta'
assert J['5076']['two_generator_min']==384 and J['5076']['three_generator_min']==384
assert J['5077']['exact_two_star_minimum']==1000 and J['5077']['best_nonzero_weight_found']==625
assert J['5078']['q3']=={'syndrome_bits':3,'rom_entries':8,'covering_radius':2,'coset_leader_hist':{'0':1,'1':6,'2':1}}
assert J['5079']['status']=='THEOREM' and J['5079']['anchors']['q5']==1170000
assert J['5080']['q2']['minimum_words']==J['5080']['q2']['chamber_stars']==45
assert J['5081']['dual_minimum_distance']==3 and J['5081']['q2_dual_coefficients']['A3']==120
P=json.loads((R/'data/PART_W33_PASS5066_5073_RESULTS.json').read_text())
assert P['5066']['W3q']['theta_generates_full_dual'] is True
assert P['5067']['status']=='UNKNOWN'
print('PASS 5074-5081')
