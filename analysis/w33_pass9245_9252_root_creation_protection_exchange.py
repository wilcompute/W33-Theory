#!/usr/bin/env python3
"""Pass9245-9252 outside-box: root-creation/protection exchange between the glues.

The E6-relative glue has four projective weight-3 local extension directions;
each +/- pair creates 54 visible E6 roots over one W33 line point.  Under the
canonical orthogonal exchange S between the transverse E6 and Golay glues,
those four directions become a [12,4,6]_3 Golay subcode with no weight-3 words.
"""
from __future__ import annotations
import itertools,json,sys
from collections import Counter
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_rank24_root_shadow_core as rs
OUT=ROOT/'data/PART_W33_PASS9245_9252_ROOT_CREATION_PROTECTION_EXCHANGE.json';P=3

def rref(a):
 a=np.array(a,dtype=np.int64)%P;m,n=a.shape;r=0
 for c in range(n):
  q=next((i for i in range(r,m) if a[i,c]),None)
  if q is None:continue
  a[[r,q]]=a[[q,r]];a[r]=a[r]*pow(int(a[r,c]),-1,P)%P
  for i in range(m):
   if i!=r and a[i,c]:a[i]=(a[i]-a[i,c]*a[r])%P
  r+=1
 return a[:r]
def span(g):return {tuple((np.array(c,dtype=np.int64)@g)%P) for c in itertools.product(range(P),repeat=g.shape[0])}
def wen(words):return Counter(sum(int(x)!=0 for x in w) for w in words)

def main():
 G=np.array(rs.GOLAY12,dtype=np.int64)%P;GW=span(G)
 cert=json.loads((ROOT/'data/PART_W33_PASS9185_9196_GOLAY_TETRACODE_GLUE_BIFURCATION.json').read_text())
 E=np.array(cert['N(E6^4)_relative_glue']['generator_rref'],dtype=np.int64)%P;EW=span(E)
 pairing=G@E.T%P;H=rs.inv_mod(pairing,P).T@E%P;C=np.vstack([G,H])%P;Ci=rs.inv_mod(C,P)
 I6=np.eye(6,dtype=np.int64);Z=np.zeros((6,6),dtype=np.int64);Swap=np.block([[Z,I6],[I6,Z]])%P
 S=Ci@Swap@C%P;assert np.array_equal(S@S.T%P,np.eye(12,dtype=np.int64)%P)
 w3=sorted(w for w in EW if sum(int(x)!=0 for x in w)==3);assert len(w3)==8
 supports=sorted({tuple(i for i,x in enumerate(w) if x) for w in w3});assert supports==[(0,1,2),(3,4,5),(6,7,8),(9,10,11)]
 U=[]
 for supp in supports:
  w=np.array(next(w for w in w3 if tuple(i for i,x in enumerate(w) if x)==supp),dtype=np.int64)%P
  first=next(int(x) for x in w if x);w=w*pow(first,-1,P)%P;U.append(w)
 U=rref(U);ue=wen(span(U));assert U.shape==(4,12) and ue==Counter({9:32,6:24,12:16,3:8,0:1})
 V=rref(U@S%P);assert V.shape==(4,12)
 VW=span(V);assert all(w in GW for w in VW)
 ve=wen(VW);assert ve==Counter({9:48,6:28,12:4,0:1})
 out={'schema':'w33.pass9245_9252.root_creation_protection_exchange.v1','status':'PASS','passes':'9245-9252',
      'E6_local_extension_code':{'parameters':'[12,4,3]_3','weight_enumerator':{str(k):int(v) for k,v in sorted(ue.items())},'four_projective_weight3_directions':True,'root_role':'the four +/- pairs of weight-3 words create 4*54=216 visible E6 roots'},
      'exchange_image_in_Golay':{'parameters':'[12,4,6]_3','size':81,'weight_enumerator':{str(k):int(v) for k,v in sorted(ve.items())},'contained_in_extended_ternary_Golay':True,'weight3_words':0},
      'theorem':'The canonical glue-exchange involution sends the four-dimensional E6 local root-extension sector to an 81-word [12,4,6]_3 subcode of the extended ternary Golay code. The directions that create norm-2 E6 roots on one side become a distance-6 rootless/protected sector on the other.',
      'interpretation_boundary':'“creation/protection duality” is a code/lattice statement: minimum glue weight 3 allows norm-2 extensions, whereas minimum weight 6 forbids them. It is not by itself a dynamical particle-creation or error-correction process.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','source_min':3,'image_min':6,'image_size':81,'image_enum':dict(ve)}))
 return 0
if __name__=='__main__':raise SystemExit(main())
