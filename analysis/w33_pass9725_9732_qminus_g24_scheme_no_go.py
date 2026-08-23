#!/usr/bin/env python3
"""Pass9725-9732: association-scheme transport test for Q^-(5,3) vs G2(4)/HJ.

The previous 252=252 and 126=126 count matches are pushed to the full natural
O^-(6,3) coherent configuration on the 252 nonsingular projective points.
We compare its invariant relation valencies with the exact G2(4) fixed-edge
subconstituents from Pass9365-9372.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9725_9732_QMINUS_G24_SCHEME_NO_GO.json'
P=3

def canon(v):
 v=tuple(int(x)%P for x in v)
 for x in v:
  if x:
   z=pow(x,-1,P);return tuple(z*y%P for y in v)
 raise ValueError('zero')
def q(v):return sum(int(x)*int(x) for x in v)%P

def main():
 pts=sorted({canon(v) for v in itertools.product(range(P),repeat=6) if any(v)})
 fibers={a:[np.array(v,dtype=np.int64) for v in pts if q(v)==a] for a in (0,1,2)}
 assert [len(fibers[a]) for a in (0,1,2)]==[112,126,126]
 profile={}
 for a in (1,2):
  u=fibers[a][0];c=Counter()
  for b in (1,2):
   for v in fibers[b]:
    if np.array_equal(u,v):
     c[(b,'diag')]+=1
    elif int(u@v)%P==0:c[(b,'orth')]+=1
    else:c[(b,'nonorth')]+=1
  profile[str(a)]={f'{b}:{r}':n for (b,r),n in sorted(c.items())}
 assert profile['1']=={'1:diag':1,'1:nonorth':80,'1:orth':45,'2:nonorth':90,'2:orth':36}
 assert profile['2']=={'1:nonorth':90,'1:orth':36,'2:diag':1,'2:nonorth':80,'2:orth':45}
 basis=[45,80,36,90]
 union_degrees=sorted({sum(basis[i] for i in range(4) if mask>>i&1) for mask in range(16)})
 assert union_degrees==[0,36,45,80,81,90,116,125,126,135,161,170,171,206,215,251]
 g=json.loads((ROOT/'data/PART_W33_PASS9365_9372_G24_EDGE_ORBITAL_REFINEMENT.json').read_text())
 p=g['fixed_edge_vertex_partition'];e=g['forced_edge_counts']
 assert p=={'A_common':36,'B_u_only':63,'C_v_only':63,'D_neither':252}
 ddeg=2*e['DD']//p['D_neither'];bcdeg=2*(e['BB']+e['BC']+e['CC'])//(p['B_u_only']+p['C_v_only'])
 assert ddeg==66 and bcdeg==31
 assert ddeg not in union_degrees and bcdeg not in (45,80,125)
 out={'schema':'w33.pass9725_9732.qminus_g24_scheme_no_go.v1','status':'PASS','passes':'9725-9732',
 'qminus_coherent_configuration':{'fibers':{'singular':112,'norm1':126,'norm2':126},'rank_on_nonsingular_ordered_pairs':10,'source_relation_profiles':profile,'undirected_Ominus_invariant_union_degrees_on_252':union_degrees},
 'g24_fixed_edge_subconstituents':{'D_size':252,'D_induced_degree':ddeg,'B_union_C_size':126,'B_union_C_induced_average_degree':bcdeg,'rank14_edge_refinement':g['rank14_refinement']},
 'no_go':'No O^-(6,3)-invariant union of the four natural nonsingular relations has degree 66, so the G2(4) D_252 induced graph cannot be any orbital-union graph of the natural Q^-(5,3) coherent configuration. On a single 126-point Q^- norm fiber the only nontrivial invariant degrees are 45,80,125, so the G2 B-union-C degree 31 also cannot match. In addition Q^- nonsingular points split intrinsically into two 126 fibers, whereas the naive G2 D comparison treats a single 252 cell.',
 'surviving_target':'Any genuine Hall-Janko/Q^- bridge must forget or twist the standard quadratic-form relations and use a non-natural G2 rank-14 orbital combination or an enlarged object (for example two-spaces/Lagrangians), not the point orthogonality scheme.',
 'boundary':'Exact no-go for the natural O^-(6,3) point coherent configuration and all of its invariant undirected relation unions. It does not rule out correspondences on two-spaces or other derived schemes.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','D_degree':ddeg,'Q_union_degrees':union_degrees}));return 0
if __name__=='__main__':raise SystemExit(main())
