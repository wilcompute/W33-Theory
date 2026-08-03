#!/usr/bin/env python3
"""Pass 2950: classify the isodual [8,4,4]_3 outer code beyond distance."""
from __future__ import annotations
import itertools,collections,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_BT2950_TERNARY_844_CLASSIFICATION_results.json'
G=np.array([[1,1,0,1,1,0,1,0],[2,1,1,2,0,0,0,0],[1,1,0,1,0,1,0,1],[2,2,2,0,0,1,1,2]],dtype=int)%3
H=np.array([[1,1,1,1,0,0,0,0],[2,0,2,0,1,1,0,0],[2,1,1,0,2,0,1,0],[1,1,0,0,1,0,0,1]],dtype=int)%3
assert np.all(H@G.T%3==0);msgs=np.array(list(itertools.product(range(3),repeat=4)),dtype=int);C=(msgs@G)%3;D=(msgs@H)%3
cwe=collections.Counter(tuple(np.bincount(w,minlength=3)) for w in C);wte=collections.Counter(int(np.count_nonzero(w)) for w in C);dw=collections.Counter(int(np.count_nonzero(w)) for w in D)
cosets={}
for w in itertools.product(range(3),repeat=8):
 s=tuple(H@np.array(w)%3);wt=sum(x!=0 for x in w);rec=cosets.setdefault(s,{'min':99,'leaders':[],'weight_distribution':collections.Counter()});rec['weight_distribution'][wt]+=1
 if wt<rec['min']:rec['min']=wt;rec['leaders']=[w]
 elif wt==rec['min']:rec['leaders'].append(w)
assert len(cosets)==81;radius=max(r['min'] for r in cosets.values());leader_dist=collections.Counter(r['min'] for r in cosets.values());leader_mult=collections.Counter((r['min'],len(r['leaders'])) for r in cosets.values());ambient=collections.Counter({d:81*n for d,n in leader_dist.items()});types=collections.Counter(tuple(sorted(r['weight_distribution'].items())) for r in cosets.values())
def rank3(A):
 A=A.copy()%3;r=0
 for c in range(A.shape[1]):
  p=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
  if p is None:continue
  A[[r,p]]=A[[p,r]]
  if A[r,c]==2:A[r]=2*A[r]%3
  for i in range(A.shape[0]):
   if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%3
  r+=1
 return r
hull=4-rank3(G@G.T%3);support_data={}
for wt in sorted(k for k in wte if k):
 blocks=collections.Counter(tuple(i for i,x in enumerate(w) if x) for w in C if np.count_nonzero(w)==wt);unique=list(blocks);deg=collections.Counter(i for B in unique for i in B);inter=collections.Counter(len(set(A)&set(B)) for A,B in itertools.combinations(unique,2));support_data[str(wt)]={'codewords':wte[wt],'unique_supports':len(unique),'support_multiplicities':{str(k):v for k,v in collections.Counter(blocks.values()).items()},'point_degrees':{str(k):v for k,v in sorted(deg.items())},'intersection_histogram':{str(k):v for k,v in sorted(inter.items())}}
spectrum=tuple(int(wte.get(8-i,0)//2) for i in range(5));assert spectrum==(3,4,10,12,11)
checks={'parameters_844':wte[0]==1 and min(k for k in wte if k)==4,'formal_self_dual':wte==dw,'covering_radius_two':radius==2,'lcd_hull_zero':hull==0,'nine_coset_enumerator_types':len(types)==9,'spectrum_type_3_4_10_12_11':spectrum==(3,4,10,12,11),'not_uniformly_packed_wide_sense':radius!=len([w for w in dw if w])}
out={'schema':'w33.pass2950.ternary_844_classification.v1','status':'COMPLETE_EXACT','checks':checks,'check_count':len(checks),'parameters':'[8,4,4]_3','weight_enumerator':{str(k):v for k,v in sorted(wte.items())},'complete_weight_enumerator':{'/'.join(map(str,k)):v for k,v in sorted(cwe.items())},'dual_weight_enumerator':{str(k):v for k,v in sorted(dw.items())},'projective_hyperplane_spectrum':list(spectrum),'literature_spectrum_type':'first listed [8,4,4]_3 spectrum (3,4,10,12,11)','covering_radius':radius,'coset_leader_distance_distribution':{str(k):v for k,v in sorted(leader_dist.items())},'coset_leader_multiplicity_distribution':{f'{k[0]}:{k[1]}':v for k,v in sorted(leader_mult.items())},'ambient_distance_partition':{str(k):v for k,v in sorted(ambient.items())},'coset_weight_enumerator_type_count':len(types),'coset_weight_enumerator_types':[{'multiplicity':m,'enumerator':{str(k):v for k,v in t}} for t,m in types.items()],'external_distance':len([w for w in dw if w]),'uniformly_packed_wide_sense':False,'hull_dimension':hull,'lcd':True,'support_data':support_data,'claim_boundary':'Exact equivalence invariants for this code. The spectrum identifies its published spectrum type, not uniqueness within that type unless a classification source explicitly supplies it.'};assert all(checks.values());OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(f"PASS {len(checks)}/{len(checks)} radius={radius} hull={hull} spectrum={spectrum}")
