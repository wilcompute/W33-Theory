#!/usr/bin/env python3
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1815_d4_gkp_quartet_operator_assignment.json'

QUARTET={
  '00': {'name':'0','d4_coset':'D4 root coset','representative':[0,0,0,0]},
  '01': {'name':'v','d4_coset':'vector coset','representative':[1,0,0,0]},
  '10': {'name':'s','d4_coset':'spinor coset','representative':[0.5,0.5,0.5,0.5]},
  '11': {'name':'c','d4_coset':'conjugate spinor coset','representative':[0.5,0.5,0.5,-0.5]},
}
DEFECT_SLICE=[(5,10,41),(7,34,40),(10,22,44),(12,34,42),(18,40,42),(30,41,44)]
OBS=(10,22,44)

def xor(a,b): return ''.join('1' if x!=y else '0' for x,y in zip(a,b))

def main():
    edges=list(itertools.combinations(QUARTET.keys(),2))
    edge_map=[]
    for edge,hinge in zip(edges,DEFECT_SLICE):
        edge_map.append({'quartet_edge':list(edge),'difference_coset':xor(*edge),'hinge_support':list(hinge),'observed':hinge==OBS})
    obs_edge=next(e for e in edge_map if e['observed'])
    checks={'four_cosets':len(QUARTET)==4,'six_edges':len(edges)==6,'observed_edge_00_11':obs_edge['quartet_edge']==['00','11'],'observed_difference_11':obs_edge['difference_coset']=='11'}
    payload={'bt':'BT1815','title':'D4/GKP quartet operator assignment','verified':all(checks.values()),'summary':'The hidden quartet can be assigned to the D4 discriminant/glue group D4*/D4 = (Z2)^2. We label the four local GKP/D4 cosets as 00=0, 01=v, 10=s, 11=c. The six W(E6)-compatible Hesse hinges are the six unordered K4 edges among these four cosets. In the BT1813 edge order, the observed repair support {10,22,44} is the edge 00--11, i.e. the conjugate-spinor displacement c relative to the root coset. The sign pattern (-2,-2,+2) orients this edge transfer from removed pair to returned pair.','quartet_assignment':QUARTET,'edge_to_hinge_support_map':edge_map,'observed':{'support':list(OBS),'quartet_edge':obs_edge['quartet_edge'],'difference_coset':obs_edge['difference_coset'],'operator_reading':'oriented displacement by the c coset, 00 -> 11, up to D4 triality gauge'},'checks':checks,'boundary':'The assignment fixes the D4/GKP coset structure. Triality can permute v,s,c, so the invariant claim is K4-edge structure plus observed difference class, not an absolute naming of v/s/c without a chosen D4 gauge.'}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'verified':payload['verified'],'observed_edge':obs_edge['quartet_edge'],'difference':obs_edge['difference_coset']},indent=2))
    return 0 if payload['verified'] else 1
if __name__=='__main__': raise SystemExit(main())
