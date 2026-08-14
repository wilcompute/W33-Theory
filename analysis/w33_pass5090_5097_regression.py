#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
x=json.loads((R/'data/PART_W33_PASS5090_5097_RESULTS.json').read_text())
assert x['packet']==[5090,5097]
assert x['5090']['sat']==8 and x['5090']['unsat']==8
assert x['5091']['detP']==1 and x['5091']['disc_q3_order']==272
assert x['5092']['strict_one_swap_local_optimum']
assert x['5093']['anchors']['q3']==[27,27,27,27]
assert x['5094']['q3_pair_generated_orders']==[9,9,9,9,27,81]
assert not x['5095']['q2']['isomorphic'] and not x['5095']['q4']['isomorphic']
assert x['5096']['identities']['active_charts']=='256-t'
assert 'sum_O' in x['5097']['identity']
A=((1,4),(1,0));C=((0,2),(2,1));P=((2,-1),(-1,1))
def mm(X,Y):return tuple(tuple(sum(X[i][k]*Y[k][j] for k in range(2)) for j in range(2)) for i in range(2))
assert mm(A,P)==mm(P,C)
print('PASS')
