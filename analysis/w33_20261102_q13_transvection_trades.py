#!/usr/bin/env python3
"""Independent q13 160-line even-set neighbor trade test under all symplectic
point-center transvections (one fixed parameter each) and several scales.

The symmetric difference of any two even line sets is an even line set; if
overlap >80 with a distinct 160-set, we immediately improve the 160 upper bound.
"""
from pathlib import Path
from itertools import permutations,product
import sys,json
from collections import Counter
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis/search_drivers_12466'))
from symmetric_fast import fast_build

def main():
 q=13;rep=(1,0,1,1,6)
 def norm(w):
  v=next(int(z)%q for z in w if z%q)
  inv=pow(v,-1,q)
  return tuple((int(z)*inv)%q for z in w)
 T=set()
 for perm in permutations(range(5)):
  for signs in product((1,-1),repeat=5):
   T.add(norm([rep[perm[i]]*signs[i] for i in range(5)]))
 assert len(T)==160
 pts,lines=fast_build(q);n=len(pts)
 idx={tuple(map(int,v)):i for i,v in enumerate(pts)}
 assert len(idx)==n==2380
 h=pow(2,-1,q);ii=pow(next(x for x in range(1,q) if x*x%q==q-1),-1,q)
 def det(a,b,i,j):return (int(a[i])*int(b[j])-int(a[j])*int(b[i]))%q
 def sq(u,v):return (h*(u+v)%q,h*(u-v)*ii%q)
 selected=[]
 for l,L in enumerate(lines):
  a,b=pts[L[0]],pts[L[1]]
  y=norm(sq(det(a,b,0,1),det(a,b,2,3))+
        sq(det(a,b,0,3),det(a,b,1,2))+(det(a,b,0,2),))
  if y in T:selected.append(l)
 assert len(selected)==160
 # A line is uniquely specified by any two points.
 selected_pairs={}
 endpoints=[]
 for j in selected:
  L=list(map(int,lines[j]))
  endpoints.extend(L[:2])
  for i in range(len(L)):
   for k in range(i):
    selected_pairs[(min(L[i],L[k]),max(L[i],L[k]))]=j
 endpoints=sorted(set(endpoints))
 endpoint_vectors=np.asarray([pts[i] for i in endpoints],dtype=np.int64)
 positions={pt:i for i,pt in enumerate(endpoints)}
 ep=[(positions[int(lines[j][0])],positions[int(lines[j][1])]) for j in selected]
 trials=[]
 maxima=[];globalbest={'xor_weight':320,'overlap':0}
 for c in (1,2,5):
  hist=Counter()
  for a_id,a in enumerate(pts):
   a=np.asarray(a,dtype=np.int64)
   pairings=(endpoint_vectors[:,0]*a[2]-endpoint_vectors[:,2]*a[0]+
            endpoint_vectors[:,1]*a[3]-endpoint_vectors[:,3]*a[1])%q
   transformed=(endpoint_vectors+c*pairings[:,None]*a)%q
   image=[idx[norm(u)] for u in transformed]
   overlap=0;hits=set()
   for i,j in ep:
    ti,tj=image[i],image[j]
    hit=selected_pairs.get((min(ti,tj),max(ti,tj)))
    if hit is not None:
     assert hit not in hits
     hits.add(hit)
     overlap+=1
   hist[overlap]+=1
   weight=320-2*overlap
   if weight<globalbest['xor_weight'] and weight>0:
    globalbest={'c':c,'center':a_id,'overlap':overlap,
                'xor_weight':weight,'center_point':list(map(int,pts[a_id]))}
  trials.append({'c':c,'max_overlap':max(hist),'max_overlap_count':hist[max(hist)],
                'min_nonzero_xor_weight':min(320-2*k for k in hist if k!=160),
                'overlap_histogram':{str(k):v for k,v in sorted(hist.items())}})
  print('TRADE',c,'max',max(hist),'minimum_nontrivial_xor',trials[-1]['min_nonzero_xor_weight'],flush=True)
 out={'status':'PASS_Q13_TRANSVECTION_EVEN_SET_TRADES',
   'original_line_count':160,'distinct_transvection_centers':n,
   'nonzero_transvection_parameters':[1,2,5],
   'total_tested_transvections':3*n,
   'trade_summary':trials,'best_distinct_symmetric_difference':globalbest,
   'improved_upper_bound':globalbest['xor_weight']<160,
   'exact_invariance':'For incidence mod 2, N(s XOR t)=Ns+Nt=0, so each nonempty difference is an even line set.',
   'scope':'Complete all 2380 centers at three nonzero transvection parameters c; not the full Sp4(13) orbit, no global min-weight proof. Already known existence of 160-line set credited to parallel Pass12527.'}
 (ROOT/'data/w33_20261102_q13_transvection_trades.json').write_text(json.dumps(out,indent=2)+'\n')
 print('Q13_BEST_TRADE',json.dumps({k:v for k,v in out.items() if k!='trade_summary'})[:2500],flush=True)
 return out
if __name__=='__main__':main()
