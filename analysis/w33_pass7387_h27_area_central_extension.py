#!/usr/bin/env python3
"""Pass7387: the Pass7183 affine-area voltage is the qutrit Heisenberg central extension."""
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7387_H27_AREA_CENTRAL_EXTENSION.json'
F=range(3);V=[(a,b) for a in F for b in F];E=[((a,b),z) for a,b in V for z in F]
def det(u,v):return (u[0]*v[1]-u[1]*v[0])%3
def mul(x,y):
 u,z=x;v,w=y;return (((u[0]+v[0])%3,(u[1]+v[1])%3),(z+w-det(u,v))%3)
def inv(x):u,z=x;return (((-u[0])%3,(-u[1])%3),(-z)%3)
def comm(x,y):return mul(mul(mul(x,y),inv(x)),inv(y))
def matdet(g):return (g[0]*g[3]-g[1]*g[2])%3
def act(g,x):
 u,z=x;d=matdet(g);return (((g[0]*u[0]+g[1]*u[1])%3,(g[2]*u[0]+g[3]*u[1])%3),(d*z)%3)
def main():
 e=((0,0),0)
 assert len(E)==27
 assert all(mul(mul(x,y),z)==mul(x,mul(y,z)) for x in E for y in E for z in E)
 assert all(mul(x,inv(x))==e==mul(inv(x),x) for x in E)
 assert all(mul(mul(x,x),x)==e for x in E)
 Z=[x for x in E if all(mul(x,y)==mul(y,x) for y in E)];assert Z==[((0,0),z) for z in F]
 C={comm(x,y) for x in E for y in E};assert C==set(Z)
 assert all(comm((u,0),(v,0))==((0,0),det(u,v)) for u in V for v in V)
 # The alternating form is nondegenerate and spans the 1-dimensional space Alt^2(F3^2)^*.
 assert all(any(det(u,v)!=0 for v in V) for u in V if u!=(0,0))
 # Every GL(2,3) matrix lifts by the determinant action on the center.
 GL=[]
 for a,b,c,d in itertools.product(F,repeat=4):
  g=(a,b,c,d)
  if matdet(g):GL.append(g)
 assert len(GL)==48
 assert all(act(g,mul(x,y))==mul(act(g,x),act(g,y)) for g in GL for x in E for y in E)
 SL=[g for g in GL if matdet(g)==1];assert len(SL)==24
 # Cayley connection used in Pass7186.
 S={((a,b),0) for a,b in V if (a,b)!=(0,0)};assert len(S)==8
 deg={x:len({mul(x,s) for s in S}) for x in E};assert set(deg.values())=={8}
 out={'schema':'w33.pass7387.h27_area_central_extension.v1','status':'PASS','order':27,'exponent':3,'center_order':3,'derived_subgroup_order':3,'quotient':'F3^2','law':'(u,z)(v,w)=(u+v,z+w-det(u,v))','commutator':'[(u,z),(v,w)]=(0,det(u,v))','extraspecial':'Heisenberg H27, nonabelian extraspecial 3-group of exponent 3','cohomology':'The Pass7183 edge voltage c(u,v)=-det(u,v) has nondegenerate alternating commutator det. Alt^2(F3^2)^* is one-dimensional, so up to nonzero central rescaling this is the unique nontrivial bilinear Heisenberg extension.','GL2_lift':'g:(u,z)->(gu,det(g)z)','GL2_order':48,'SL2_order':24,'Cayley_connection_size':8,'bridge':'The affine-area cocycle, the E8-derived 27-fibre cover, and the repo H27 qutrit Heisenberg model are not merely isomorphic graphs: the voltage itself is the central-extension 2-cocycle whose commutator is the symplectic determinant.','boundary':'Finite group/cohomology theorem only; no physical gauge field is inferred.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','group':'H27','center':3,'GL2':48}))
if __name__=='__main__':main()
