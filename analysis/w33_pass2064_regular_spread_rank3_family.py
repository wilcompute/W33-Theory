#!/usr/bin/env python3
"""Regular symplectic-spread orbit census for q=3,5,7.

Default mode verifies the frozen certificate.  Use --full to rebuild every
projective point, isotropic line, regular spread orbit, pair intersection, and
strongly regular relation.  The full q=7 run is intentionally not a CI step.
"""
from __future__ import annotations
import argparse,itertools,hashlib,json
from collections import Counter,deque
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/'data/w33_pass2064_regular_spread_rank3_family_q357.json'
EXPECTED='28c28d5078aa495c3022a6a6153b0e83d55a70a9160179c15cd23a4d8a25a60e'

def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def nonsquare(q):
 sq={x*x%q for x in range(1,q)};return next(x for x in range(2,q) if x not in sq)
def norm(v,q):
 v=tuple(int(x)%q for x in v)
 for x in v:
  if x:
   z=pow(x,-1,q);return tuple(z*y%q for y in v)
 raise ValueError
def matvec(M,v,q):return tuple(sum(int(M[i,j])*v[j] for j in range(4))%q for i in range(4))
def kmul(z,w,mu,q):
 a,b=z;c,d=w;return ((a*c+b*d*mu)%q,(a*d+b*c)%q)
def build_orbit(q):
 mu=nonsquare(q)
 J=np.array([[0,0,1,0],[0,0,0,mu],[-1,0,0,0],[0,-mu,0,0]],dtype=np.int64)%q
 pts=sorted({norm(v,q) for v in itertools.product(range(q),repeat=4) if any(v)})
 pi={p:i for i,p in enumerate(pts)}
 def B(x,y):return int(np.array(x,dtype=np.int64)@J@np.array(y,dtype=np.int64)%q)
 lines=set()
 for i,x in enumerate(pts):
  for y in pts[i+1:]:
   if B(x,y):continue
   L={pi[norm(tuple((a*x[k]+b*y[k])%q for k in range(4)),q)]
      for a in range(q) for b in range(q) if (a,b)!=(0,0)}
   if len(L)==q+1:lines.add(tuple(sorted(L)))
 lines=sorted(lines);li={L:i for i,L in enumerate(lines)}
 base=[]
 for slope in list(itertools.product(range(q),repeat=2))+[None]:
  L=set()
  for lam in itertools.product(range(q),repeat=2):
   if lam==(0,0):continue
   if slope is None:x=(0,0);y=lam
   else:x=lam;y=kmul(lam,slope,mu,q)
   L.add(pi[norm((x[0],x[1],y[0],y[1]),q)])
  base.append(li[tuple(sorted(L))])
 base=tuple(sorted(base));assert len(base)==q*q+1
 I=np.eye(4,dtype=np.int64);line_gens=[]
 for v in pts: # all point transvections: complete and generator-choice free
  vv=np.array(v,dtype=np.int64);M=(I+np.outer(vv,J@vv))%q
  pp=tuple(pi[norm(matvec(M,p,q),q)] for p in pts)
  line_gens.append(tuple(li[tuple(sorted(pp[x] for x in L))] for L in lines))
 seen={base};todo=deque([base])
 while todo:
  S=todo.popleft()
  for g in line_gens:
   T=tuple(sorted(g[x] for x in S))
   if T not in seen:seen.add(T);todo.append(T)
 return sorted(seen)
def census(q):
 S=build_orbit(q);n=len(S);dist=Counter();A=np.zeros((n,n),dtype=np.int8)
 for i,j in itertools.combinations(range(n),2):
  z=len(set(S[i])&set(S[j]));dist[z]+=1
  if z==q+1:A[i,j]=A[j,i]=1
 deg=set(map(int,A.sum(1)));assert len(deg)==1;k=next(iter(deg))
 AA=A.astype(np.int32)@A.astype(np.int32)
 adj={int(AA[i,j]) for i in range(n) for j in range(i+1,n) if A[i,j]}
 non={int(AA[i,j]) for i in range(n) for j in range(i+1,n) if not A[i,j]}
 assert len(adj)==len(non)==1
 lam=next(iter(adj));muv=next(iter(non))
 vals=np.linalg.eigvalsh(A.astype(float));spec=Counter(int(round(x)) for x in vals)
 return {'q':q,'spreads':n,'intersection_distribution':{str(a):b for a,b in sorted(dist.items())},
         'qplus1_relation':{'k':k,'lambda_':lam,'mu':muv,
                            'eigenvalues':{str(a):b for a,b in sorted(spec.items(),reverse=True)}}}
def main(full=False):
 d=json.loads(CERT.read_text());assert d['sha256_without_hash_field']==EXPECTED==digest(d)
 assert all(d['checks'].values())
 if full:
  got={str(q):census(q) for q in (3,5,7)}
  for q,row in got.items():
   frozen=d['complete_finite_results'][q]
   assert row['spreads']==frozen['spreads']
   assert row['intersection_distribution']==frozen['intersection_distribution']
   assert row['qplus1_relation']==frozen['qplus1_relation']
 else:got={q:{'spreads':r['spreads'],'intersection_distribution':r['intersection_distribution']} for q,r in d['complete_finite_results'].items()}
 out={'status':d['status'],'mode':'full' if full else 'certificate-replay','q':got,
      'certificate':EXPECTED,'boundary':d['boundary']}
 print(json.dumps(out,indent=2,sort_keys=True));return out
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--full',action='store_true');args=ap.parse_args();main(args.full)
