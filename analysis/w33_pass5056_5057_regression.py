#!/usr/bin/env python3
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
def load(name): return json.loads((R/'data'/name).read_text())
a=load('PART_W33_PASS5056_Q4_THETA_APARTMENT_CODE.json')
b=load('PART_W33_PASS5057_LOCAL_THETA_CUTSPACE.json')
assert a['code']==[13600,256,256]
assert a['theta_checks']==54400 and a['theta_check_rank_f2']==13344
assert a['theta_checks_span_full_dual'] and a['theta_checks_per_apartment']==12
assert b['q4_chamber_star']['active_charts_total']==256
assert all(x['minimum_nonzero_local_weight']==x['q'] for x in b['checked_local_q'])
print('Pass5056-5057 regression PASS')
