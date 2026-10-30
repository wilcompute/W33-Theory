#!/usr/bin/env python3
"""Exact discrete finite-speed wave propagation on H_p Cayley graphs.
Stable local recurrence is a graph toy model, not derived Lorentzian spacetime.
"""
from fractions import Fraction as F
from collections import defaultdict
import json
G=((1,0,0),(-1,0,0),(0,1,0),(0,-1,0))
def left(g,h,p):
 a,b,c=g;x,y,z=h
 return ((a+x)%p,(b+y)%p,(c+z+a*y)%p)
def B(u,p):
 out=defaultdict(F)
 for v,a in u.items():
  for g in G:out[left(g,v,p)]+=a/4
 return {v:a for v,a in out.items() if a}
def combo(a,b,ka=1,kb=1):
 out=defaultdict(F)
 for v,x in a.items():out[v]+=ka*x
 for v,x in b.items():out[v]+=kb*x
 return {v:x for v,x in out.items() if x}
def dot(a,b):return sum((x*b.get(v,0) for v,x in a.items()),F(0))
def energy(u,v,p):return dot(u,u)+dot(v,v)-2*dot(u,B(v,p))
def balls(p,r):
 seen={(0,0,0)};front=seen;sets=[seen.copy()]
 for t in range(r):
  front={left(g,x,p) for g in G for x in front}-seen
  seen|=front;sets.append(seen.copy())
 return sets
def verify(p=17,ticks=6):
 delta={(0,0,0):F(1)}
 u,v=delta,B(delta,p)
 shells=balls(p,ticks)
 e=energy(v,u,p);assert e==F(3,4)
 record=[dict(t=0,occupied=1,ball=1),dict(t=1,occupied=len(v),ball=len(shells[1]))]
 for t in range(1,ticks):
  nxt=combo(B(v,p),u,2,-1)
  assert set(nxt).issubset(shells[t+1])
  assert energy(nxt,v,p)==e
  record.append(dict(t=t+1,occupied=len(nxt),ball=len(shells[t+1])))
  u,v=v,nxt
 assert [x["ball"] for x in record]==[1,5,17,53,135,299,593]
 return dict(status="PASS",p=p,n=p**3,degree=4,ticks=ticks,
   recurrence="u(t+1)=2*(A/4)*u(t)-u(t-1)",
   exact_energy=str(e),finite_support_cone=True,records=record,
   bound="one Cayley-graph hop per time step; graph word metric is anisotropic Heisenberg",
   limitation="No Lorentzian metric, relativity principle, continuum gravity, or physical speed of light derived.")
if __name__=="__main__":print(json.dumps(verify(),indent=2))
