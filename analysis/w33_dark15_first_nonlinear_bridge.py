#!/usr/bin/env python3
"""First nonlinear equivariant bridge between the W33 point/line dark 15s.

Pass4961 proved Hom_PSp(V15_line,V15_point)=0 and Pass4977 showed the actual
PGSp outer twist does not restore it.  Here we build the standard W(3,3)
point and line permutation actions directly over F3, enumerate all 25920
projective symplectic group elements, and use exact character projectors onto
the -4 eigenspaces (the two inequivalent 15-dimensional constituents).

For a representation V, chi_Sym^d is obtained from chi(g^k) by the ordinary
cycle-index formulas.  Exact character inner products give

  Hom(Sym^2 V15_line, V15_point) = 0,
  Hom(Sym^3 V15_line, V15_point) = 0,
  Hom(Sym^4 V15_line, V15_point) = 1.

Thus the first ordinary PSp-equivariant nonlinear transceiver is quartic and
unique up to scale.  This is representation theory only; constructing a local
physical/VOA realization of the quartic map is a separate problem.
"""
from __future__ import annotations
import itertools,json
from collections import deque
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_dark15_first_nonlinear_bridge.json';q=3
J=np.array([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]],dtype=int)%q

def canon(v):
 v=np.asarray(v,dtype=int)%q;i=next(i for i,x in enumerate(v) if x);return tuple((v*pow(int(v[i]),-1,q))%q)
def om(a,b):return int(np.asarray(a)@J@np.asarray(b)%q)
P=sorted({canon(v) for v in itertools.product(range(q),repeat=4) if any(v)});pi={x:i for i,x in enumerate(P)}
L=set()
for a,b in itertools.combinations(P,2):
 if om(a,b):continue
 z=frozenset(canon(x*np.array(a)+y*np.array(b)) for x in range(q) for y in range(q) if x or y)
 if len(z)==4:L.add(z)
L=sorted(L,key=lambda z:sorted(z));li={x:i for i,x in enumerate(L)}
assert len(P)==len(L)==40
Ap=np.zeros((40,40),dtype=int);Al=np.zeros((40,40),dtype=int)
for i,a in enumerate(P):
 for j,b in enumerate(P):
  if i!=j and om(a,b)==0:Ap[i,j]=1
for i,a in enumerate(L):
 for j,b in enumerate(L):
  if i!=j and a&b:Al[i,j]=1
assert set(Ap.sum(1))==set(Al.sum(1))=={12}

def trans(v):
 v=np.asarray(v,dtype=int).reshape(1,4)%q;c=J@v.T;g=(np.eye(4,dtype=int)+c@v)%q
 assert np.array_equal(g@J@g.T%q,J);return g
V=[np.eye(4,dtype=int)[i] for i in range(4)]+[np.array(v) for v in ((1,1,0,0),(0,0,1,1),(1,0,1,0),(0,1,0,1))]

def perms(g):
 pp=tuple(pi[canon(np.array(x)@g)] for x in P)
 ll=tuple(li[frozenset(canon(np.array(x)@g) for x in z)] for z in L)
 return pp,ll
GG=[perms(trans(v)) for v in V];ID=tuple(range(40))
def comp(p,r):return tuple(r[p[i]] for i in range(40))
seen={(ID,ID)};D=deque([(ID,ID)])
while D:
 a,b=D.popleft()
 for c,d in GG:
  z=(comp(a,c),comp(b,d))
  if z not in seen:seen.add(z);D.append(z)
assert len(seen)==25920
Ap2=Ap@Ap;Al2=Al@Al

def ch15(p,A,A2):
 f=sum(p[i]==i for i in range(40));a=sum(A[p[i],i] for i in range(40));a2=sum(A2[p[i],i] for i in range(40))
 n=a2-14*a+24*f;assert n%96==0;return n//96
def ppow(p,k):
 z=ID
 for _ in range(k):z=comp(z,p)
 return z
S={2:0,3:0,4:0}
for pp,ll in seen:
 cp=ch15(pp,Ap,Ap2);c=[None]+[ch15(ppow(ll,k),Al,Al2) for k in range(1,5)]
 s2=(c[1]**2+c[2])//2
 s3=(c[1]**3+3*c[1]*c[2]+2*c[3])//6
 s4=(c[1]**4+6*c[1]**2*c[2]+3*c[2]**2+8*c[1]*c[3]+6*c[4])//24
 for d,x in ((2,s2),(3,s3),(4,s4)):S[d]+=cp*x
H={d:S[d]//len(seen) for d in S};assert H=={2:0,3:0,4:1}

def main(write=True):
 out={'schema':'w33.dark15_first_nonlinear_bridge.v1','status':'PASS',
  'headline':'The two inequivalent 15-dimensional dark constituents of the W33 point and line actions have no ordinary PSp(4,3)-equivariant bridge at linear, quadratic, or cubic degree. The first nonlinear bridge is quartic and has multiplicity exactly one: Hom_PSp(Sym^4 V15_line,V15_point)=1.',
  'group_order':len(seen),'point_action':{'vertices':40,'dark_eigenvalue':-4,'dark_dimension':15},'line_action':{'vertices':40,'dark_eigenvalue':-4,'dark_dimension':15},
  'Hom_dimensions':{'linear':0,'Sym2_line_to_point':H[2],'Sym3_line_to_point':H[3],'Sym4_line_to_point':H[4]},
  'method':'Exact full-group character inner products. The -4 character is Tr(P_g E_-), E_-=(A-12I)(A-2I)/96; symmetric-power characters use chi(g),chi(g^2),chi(g^3),chi(g^4).',
  'consequence':'The Pass4961/4977 linear and outer-twist obstructions are not the end of the point-line correlation problem: there is a unique quartic PSp-equivariant transceiver up to scale.',
  'boundary':'This certificate proves existence and uniqueness in representation theory. It does not construct a preferred normalized quartic polynomial, a local incidence formula, or a physical/VOA interaction realizing it.',
  'checks':{'40_points':True,'40_lines':True,'PSp_order_25920':True,'quadratic_zero':True,'cubic_zero':True,'quartic_unique':True}}
 if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
