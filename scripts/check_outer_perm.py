#!/usr/bin/env python3
import sys
from pathlib import Path
import json
import numpy as np
# ensure repo root on path for imports
REPO = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(REPO))
from scripts.ce2_global_cocycle import _simple_family_sign_map

sm = _simple_family_sign_map()
print('len sign_map', len(sm))
print('(1,21,0) present?', (1,21,0) in sm)

model=json.loads(Path('artifacts/e6_cubic_affine_heisenberg_model.json').read_text(encoding="utf-8"))
vec_to_eid={ (int(v['u'][0])%3,int(v['u'][1])%3,int(v['z'])%3): int(k) for k,v in model['e6id_to_heisenberg'].items() }
def outer(u,t):
    A=np.array([[1,2],[2,0]],dtype=int)%3
    b=np.array([0,2],dtype=int)%3
    up=tuple(int(x) for x in (A@np.array(u)+b)%3)
    x,y=u
    tp=(2*t+(2+2*x+y))%3
    return up,tp

perm=[None]*27
for k,v in model['e6id_to_heisenberg'].items():
    eid=int(k)
    u=(int(v['u'][0])%3,int(v['u'][1])%3)
    t=int(v['z'])%3
    up,tp=outer(u,t)
    perm[eid]=vec_to_eid[(up[0],up[1],tp)]
print('perm',perm)

# find bad triples
bad=[]
for (c,m,o) in sm.keys():
    cp,mp,op=perm[c],perm[m],perm[o]
    if (cp,mp,op) not in sm:
        bad.append((c,m,o,cp,mp,op))
print('bad count', len(bad))
if bad:
    print('first few', bad[:10])

# compute intersection stats with branch classification
from scripts.ce2_global_cocycle import _heisenberg_vec_maps, _f3_omega, _f3_k_of_direction

def branch_constant_line(c_i,m_i,o_i):
    e6id_to_vec,_ = _heisenberg_vec_maps()
    uc1,uc2,_ = e6id_to_vec[int(c_i)]
    um1,um2,_ = e6id_to_vec[int(m_i)]
    d1 = (um1-uc1) % 3
    d2 = (um2-uc2) % 3
    if (d1,d2) == (0,0):
        return False
    w = _f3_omega((uc1,uc2),(d1,d2))
    return (d1 != 0) and (int(w) == _f3_k_of_direction((d1,d2)))

ratio_counts={+1:0,-1:0}
branch_counts={'constant':{+1:0,-1:0},'weil':{+1:0,-1:0}}
skipped=0
for (c,m,o),s in sm.items():
    cp,mp,op = perm[c], perm[m], perm[o]
    if (cp,mp,op) not in sm:
        skipped += 1
        continue
    sp = sm[(cp,mp,op)]
    r = sp//s
    ratio_counts[r] += 1
    branch = 'constant' if branch_constant_line(c,m,o) else 'weil'
    branch_counts[branch][r] += 1

print('skipped', skipped, 'out of', len(sm))
print('ratio_counts', ratio_counts)
print('branch_counts', branch_counts)
