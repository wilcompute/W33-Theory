#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
x=json.loads((R/'data/PART_W33_PASS5074_5081_RESULTS.json').read_text())
assert x['packet']==[5074,5081]
assert x['5074']['q2_exhaustive']['minimum_active_charts']==32
assert x['5075']['satisfiable_seeds']==8 and x['5075']['unsatisfiable_seeds']==8
assert x['5076']['det_conjugator']==1 and x['5076']['q3_order_discriminant']==272
assert x['5077']['smith_floor']==780 and x['5077']['strict_one_swap_local_optimum_at_den780']
assert x['5078']['finite_anchors']=={'q2':0,'q3':4320,'q4':108800,'q5':1170000}
assert x['5079']['q3_role_counts']==[27,27,27,27]
assert x['5080']['q3_pair_generated_subgroup_orders']==[9,9,9,9,27,81]
assert 'x^2-2' in x['5081']['q2']['charpoly']
# Exact integral similarity from Pass5076, no sympy dependency.
A=((1,4),(1,0));B=((0,2),(2,1));P=((2,-1),(-1,1))
def mm(X,Y):return tuple(tuple(sum(X[i][k]*Y[k][j] for k in range(2)) for j in range(2)) for i in range(2))
assert mm(A,P)==mm(P,B)
assert P[0][0]*P[1][1]-P[0][1]*P[1][0]==1
print('PASS')
