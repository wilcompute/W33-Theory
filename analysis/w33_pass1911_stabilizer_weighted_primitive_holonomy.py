#!/usr/bin/env python3
"""Pass 1911: stabilizer-weighted primitive holonomy from the four C4 Artin--Ihara factors."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'; OUT=DATA/'w33_pass1911_stabilizer_weighted_primitive_holonomy.json'
u=sp.symbols('u');I=sp.I;N=32
P=[
 sp.expand((1-4*u**2)*(1-u**2)**4*(1+2*u**2)**2*(1-2*u+2*u**2)**3*(1+2*u+2*u**2)**3),
 sp.expand((1-u**2)**4*(1+2*u**2)**2*(1-2*u+2*u**2)**2*(1+2*u+2*u**2)**2),
 sp.expand((1-u**2)**4*(1+2*u**2)**4*(1-2*u+2*u**2)**2*(1+2*u+2*u**2)**2),
 sp.expand((1-u**2)**4*(1+2*u**2)**2*(1-2*u+2*u**2)**2*(1+2*u+2*u**2)**2),
]
Q=[sp.expand((1-2*u+2*u**2)**e*(1+2*u+2*u**2)**e) for e in [3,2,2,2]]
def weighted(factors):
 tr=[]
 for p in factors:
  ser=sp.series(-u*sp.diff(p,u)/p,u,0,N+1).removeO().expand();tr.append([int(ser.coeff(u,n)) for n in range(1,N+1)])
 T=[[0]*N for _ in range(4)]
 for k in range(4):
  for n in range(N):
   z=sum(I**(j*k)*tr[j][n] for j in range(4));assert sp.im(z).simplify()==0;T[k][n]=int(sp.re(z))
 W={}
 for n in range(1,N+1):
  res=[T[k][n-1] for k in range(4)]
  for d in range(1,n):
   if n%d:continue
   m=n//d
   for h in range(4):res[(m*h)%4]-=d*W[(d,h)]
  for h in range(4):assert res[h]%n==0;W[(n,h)]=res[h]//n
 for n in range(1,N+1):
  for k in range(4):
   q=sum(d*sum(W[(d,h)] for h in range(4) if ((n//d)*h)%4==k) for d in range(1,n+1) if n%d==0)
   assert q==T[k][n-1]
 rows=[{'length':n,'holonomy':[W[(n,h)] for h in range(4)],'total':sum(W[(n,h)] for h in range(4))} for n in range(1,N+1) if any(W[(n,h)] for h in range(4))]
 return T,W,rows
T,W,rows=weighted(P);Tq,Wq,rowsq=weighted(Q)
R=[sp.cancel(P[j]/Q[j]) for j in range(4)];Tr,Wr,rowsr=weighted(R)
out={'schema':'w33.pass1911.stabilizer_weighted_primitive_holonomy.v2','status':'PASS','definition':'T_k(n)=sum_{d|n} d sum_h W_{d,h} 1[(n/d)h=k mod4]; W is the canonical stabilizer-weighted primitive quotient-cycle count.','sector_dimensions':[int(sp.degree(p,u)) for p in P],'sector_reciprocal_factors':[str(sp.factor(p)) for p in P],'twisted_traces':[{'length':n,'values':[T[k][n-1] for k in range(4)]} for n in range(1,N+1)],'primitive_holonomy':rows,'v9_shared_channel':{'sector_dimensions':[int(sp.degree(p,u)) for p in Q],'factors':[str(sp.factor(p)) for p in Q],'primitive_holonomy':rowsq},'hashimoto_complement':{'sector_dimensions':[int(sp.degree(sp.together(r).as_numer_denom()[0],u)-sp.degree(sp.together(r).as_numer_denom()[1],u)) for r in R],'factors':[str(sp.factor(r)) for r in R],'primitive_holonomy':rowsr},'carrier_separation_theorem':'The 24- and 90-sector natural carrier maps factor through the same V9 source and therefore have identical graph-holonomy data. Twisted Ihara invariants separate the shared 36-dimensional V9 channel from the 54-dimensional Hashimoto complement, but cannot distinguish A24 from A90; that distinction is representation-theoretic (orthogonal embeddings and outer conjugation), not graph-holonomic.','boundary':'These are graph-of-groups stabilizer-weighted counts reconstructed from twisted traces, not ordinary regular-cover voltage counts and not physical propagation phases.'}
out['checks']={'full_dimensions_90':sum(out['sector_dimensions'])==90,'v9_dimensions_36':sum(out['v9_shared_channel']['sector_dimensions'])==36,'complement_dimensions_54':sum(out['hashimoto_complement']['sector_dimensions'])==54,'sectorwise_dimension_addition':all(out['sector_dimensions'][i]==out['v9_shared_channel']['sector_dimensions'][i]+out['hashimoto_complement']['sector_dimensions'][i] for i in range(4)),'primitive_reconstruction':True}
assert all(out['checks'].values())
out['sha256_without_hash_field']=hashlib.sha256(json.dumps(out,sort_keys=True,separators=(',',':')).encode()).hexdigest();OUT.write_text(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n');print(json.dumps({'status':out['status'],'sha256':out['sha256_without_hash_field']},indent=2))
