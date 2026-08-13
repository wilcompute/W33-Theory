#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def J(name): return json.loads((R/'data'/name).read_text())
a=J('PART_W33_PASS5052_Q4_APARTMENT_CODE.json'); assert a['code']==[13600,256,256] and a['theta_rank']==13344 and a['theta_checks']==54400
b=J('PART_W33_PASS5053_Q3_MINIMUM_SHELL.json'); assert b['minimum_words']==160 and b['residual_weight81_after_excluding_all_chamber_stars']=='INFEASIBLE'
c=J('PART_W33_PASS5054_JACOBIAN_BICYCLE_BRIDGE.json'); assert c['bike_dimension']==29 and c['hom_dimension']==1 and c['nonzero_map_rank']==15 and not c['isomorphic']
d=J('PART_W33_PASS5055_STEINBERG_FIVE_CHANNELS.json'); assert d['orientation_split']==[8,8] and d['epsilon_dimension']==5 and d['epsilon_supports']==[8,16,8,40,40]
e=J('PART_W33_PASS5056_V24_EXACT_COMPILER.json'); assert e['old_denominator']==9360 and e['new_denominator']==3120 and e['point_star_smith_max']==780
f=J('PART_W33_PASS5057_CODE_RECONSTRUCTS_BUILDING.json'); assert f['minimum_words']==160 and f['reconstructed_panel_graph']['isomorphic_to_W33_Levi']
g=J('PART_W33_PASS5059_THETA_TANNER.json'); assert g['q2']['girth']==8 and g['q3']['six_cycles']==4320 and g['q4']['six_cycles']==108800
text=(R/'analysis'/'PASS5052_5059_EXECUTED_OUTCOMES.md').read_text(); assert '**5058' in text and 'no complete Fano planes' in text
assert 54400*3//13600==12 and 4320*3//1620==8
print('PASS Pass5052-5059 regression')
