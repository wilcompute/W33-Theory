#!/usr/bin/env python3
import json, math
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def J(name): return json.loads((R/'data'/name).read_text())
a=J('PART_W33_PASS5044_EXACT_APARTMENT_ERASURE.json'); assert a['code']==[1620,81,81] and a['dual_dimension']==1539 and a['weight3_checks']==4320 and a['safe_through']==80
b=J('PART_W33_PASS5045_JACOBIAN_2ADIC_FILTRATION.json'); assert b['height_dimensions']==[81,29,29,23,1,1] and b['successive_kill_counts']==[52,0,6,22,0,1]
c=J('PART_W33_PASS5046_LOCAL_V24_COMPILER.json'); assert c['global_rank']==24 and c['point_star']['rank']==24 and len(c['basis_apartment_indices'])==24
d=J('PART_W33_PASS5047_W3Q_SYMBOLIC_BUILDING_THEOREM.json'); assert d['levi_cycle_rank']=='q^4' and d['apartments_per_chamber']=='q^4'
e=J('PART_W33_PASS5048_APARTMENT_ACTION.json'); assert e['dimension_sum']==1620 and e['square_sum']==131 and e['degree81_multiplicity']==5
f=J('PART_W33_PASS5049_THETA_DUAL_GEOMETRY.json'); assert f['theta_triples']==4320 and f['complete_dual_weight3_shell']
g=J('PART_W33_PASS5051_Q_FAMILY_THETA_CODE.json'); assert g['q2']['code']==[90,16,16] and g['q3']['code']==[1620,81,81]
assert 3*4320//1620==8
assert 3*120//90==4
print('PASS Pass5044-5051 regression')
