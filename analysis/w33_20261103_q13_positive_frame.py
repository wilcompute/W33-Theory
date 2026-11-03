#!/usr/bin/env python3
"""Independent q13 160-line non-hyperoval spectral-module decomposition.
Uses the signed S5 orbit on Q(4,13), maps via Klein to W(3,13) and tests
positive/negative eigenspace content without building 2380x2380 adjacency.
"""
from pathlib import Path
from itertools import permutations,product
import sys,json
from collections import Counter
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis/search_drivers_12466'))
from symmetric_fast import fast_build
def main():
 q=13;rep=(1,0,1,1,6)
 def norm(w):
  h=next(int(z)%q for z in w if z%q)
  inv=pow(h,-1,q)
  return tuple((int(z)*inv)%q for z in w)
 T=set()
 for perm in permutations(range(5)):
  for s in product((1,-1),repeat=5):
   w=[(rep[perm[i]]*s[i])%q for i in range(5)]
   T.add(norm(w))
 assert len(T)==160,len(T)
 pts,lines=fast_build(q);assert len(pts)==len(lines)==2380
 h=pow(2,-1,q);imag=next(t for t in range(1,q) if t*t%q==q-1)
 invimag=pow(imag,-1,q)
 def det2(a,b,i,j):return (a[i]*b[j]-a[j]*b[i])%q
 def sq(u,v):
  return (h*(u+v)%q,h*(u-v)*invimag%q)
 cov=np.zeros(len(pts),dtype=np.int64); chosen=[]
 for j,L in enumerate(lines):
  a,b=pts[L[0]],pts[L[1]]
  a01,a23,a03,a12,a02=det2(a,b,0,1),det2(a,b,2,3),det2(a,b,0,3),det2(a,b,1,2),det2(a,b,0,2)
  x=norm(sq(a01,a23)+sq(a03,a12)+(a02,))
  assert sum(z*z for z in x)%q==0
  if x in T:
   chosen.append(j);cov[list(L)]+=1
 assert len(chosen)==160
 prof=dict(Counter(map(int,cov)))
 assert prof=={0:1340,2:960,4:80},prof
 y=17*cov-16
 assert y.sum()==0
 norm2=int(y@y)
 sums=np.array([int(y[list(L)].sum()) for L in lines],dtype=np.int64)
 Ns=np.zeros(len(pts),dtype=np.int64)
 for j,L in enumerate(lines):Ns[list(L)]+=sums[j]
 assert np.array_equal(Ns,26*y), 'exact positive-adjacency eigenvector'
 yAy=int(sums@sums-14*norm2)
 plus=(yAy+14*norm2)//26
 minus=(12*norm2-yAy)//26
 assert (yAy+14*norm2)%26==0 and (12*norm2-yAy)%26==0
 assert plus+minus==norm2 and plus>=0 and minus>=0
 # Symplectic adjacency eigenspaces r=q-1=12,s=-(q+1)=-14.
 out={'status':'PASS_Q13_NONHYPEROVAL_SPECTRAL_SUPPORT_CERTIFICATE',
 'field':13,'W33_ladder':'W(3,13)','point_count':2380,'line_count':2380,
 'monomial_orbit_size':len(T),'chosen_line_set_size':len(chosen),
 'coverage_profile':{str(k):v for k,v in sorted(prof.items())},
 'centered_integer_coverage_y':'17*coverage-16',
 'zero_sum':int(y.sum()),'centered_squared_norm':norm2,
 'point_adjacency_quadratic_form':yAy,
 'positive_eigenspace_dimension':1274,'negative_eigenspace_dimension':1105,
 'positive_eigenvalue':12,'negative_eigenvalue':-14,
 'positive_eigenspace_squared_norm':plus,
 'negative_eigenspace_squared_norm':minus,
 'positive_fraction':plus/norm2,'negative_fraction':minus/norm2,
 'geometry':'Exact Klein pullback from Q(4,13) point orbit, independent of the previously frozen q13 frame report.',
 'scope':'Exact spectral energy decomposition for the one 160-line example; not a minimum proof, not a complete orbit or cubic-tomography theorem; full symplectic group orbit covariance is predicted by rank-three action.'}
 (ROOT/'data/w33_20261103_q13_positive_frame.json').write_text(json.dumps(out,indent=2)+'\n')
 print('Q13_SPECTRAL',json.dumps(out)[:3900],flush=True)
 return out
if __name__=='__main__':main()
