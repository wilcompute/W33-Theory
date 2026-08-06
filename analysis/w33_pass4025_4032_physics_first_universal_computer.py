#!/usr/bin/env python3
"""Deterministic audit for Passes 4025-4032."""
from __future__ import annotations
import hashlib,itertools,json,math
from pathlib import Path
import networkx as nx
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_4025_4032_PHYSICS_FIRST_UNIVERSAL_COMPUTER.json'
def canonical_sha(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def norm(v):
 v=tuple(x%3 for x in v)
 for x in v:
  if x:return tuple((1 if x==1 else 2)*y%3 for y in v)
 raise ValueError
def form(u,v):return (u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%3
def geometry():
 pts=sorted({norm(v) for v in itertools.product(range(3),repeat=4) if any(v)})
 W=nx.Graph();W.add_nodes_from(range(40))
 for i,u in enumerate(pts):
  for j in range(i+1,40):
   if form(u,pts[j])==0:W.add_edge(i,j)
 lines=sorted(tuple(sorted(c)) for c in nx.find_cliques(W) if len(c)==4);assert len(lines)==40
 N=np.zeros((40,40))
 for j,line in enumerate(lines):
  for i in line:N[i,j]=1
 A=N@N.T-4*np.eye(40);assert W.number_of_edges()==240 and np.allclose(A.sum(1),12)
 L=nx.Graph();L.add_nodes_from(range(80));edges=[]
 for j,line in enumerate(lines):
  for p in line:L.add_edge(p,40+j);edges.append((p,40+j))
 edges=sorted(edges);D=np.zeros((80,160))
 for k,(p,l) in enumerate(edges):D[p,k]=-1;D[l,k]=1
 return W,L,nx.line_graph(L),N,A,D
def check_error_budget(x):
 d,t=sp.symbols('d t',real=True);d0=2*sp.sqrt(2);t0=sp.pi/sp.sqrt(2)
 def amp(s):
  o=sp.sqrt(d*d+4*s*s);return sp.exp(-sp.I*d*t/2)*(sp.cos(o*t/2)+sp.I*d*sp.sin(o*t/2)/o)
 def leak(s):
  o=sp.sqrt(d*d+4*s*s);return 4*s*s*sp.sin(o*t/2)**2/o**2
 tr=15+amp(4)-24*amp(sp.sqrt(6));F=sp.re(tr*sp.conjugate(tr))/1600;P=(leak(4)+24*leak(sp.sqrt(6)))/40
 v=[d,t];HF=sp.Matrix([[sp.simplify(sp.diff(F,a,b).subs({d:d0,t:t0})) for b in v] for a in v]);HP=sp.Matrix([[sp.simplify(sp.diff(P,a,b).subs({d:d0,t:t0})) for b in v] for a in v])
 assert HF==sp.Matrix([[-323*sp.pi**2/5184,-17*sp.pi/36],[-17*sp.pi/36,-8]])
 assert HP==sp.Matrix([[149*sp.pi**2/5184,17*sp.pi/36],[17*sp.pi/36,8]])
 assert x['optimal_retiming']=='delta_tau = -(17*pi/288) delta_d'
def check_compiler(N,x):
 H=np.block([[np.zeros((40,40)),N],[N.T,np.zeros((40,40))]])
 a=-3/20+4*np.sqrt(6)/15;b=1/40-np.sqrt(6)/60;P=a*H+b*np.linalg.matrix_power(H,3)
 w,V=np.linalg.eigh(H);S=(V*np.where(abs(w)>1e-9,np.sign(w),0))@V.T
 assert np.linalg.norm(P-S,2)<1e-12 and x['operator_error']<1e-12
def check_bridge(D,x):
 P=np.eye(160)-np.linalg.pinv(D)@D;Q=np.eye(160)-P;e=np.eye(160)[:,0]
 s=np.linalg.svd(P@np.outer(e,e)@Q,compute_uv=False)[0]
 assert round(np.trace(P))==81 and np.linalg.matrix_rank(D)==79
 assert abs(s-math.sqrt(81*79)/160)<1e-12 and abs(s-x['singular_value_numeric'])<1e-12
def main():
 data=json.loads(OUT.read_text());saved=data.pop('semantic_sha256');assert canonical_sha(data)==saved=='cc50a83926bd9d32770c33dcfb48ba04640d3601a3fbf64b29f34bb22f940a2f';data['semantic_sha256']=saved
 W,L,X,N,A,D=geometry();assert (nx.diameter(W),nx.diameter(L),nx.diameter(X))==(2,4,4)
 check_error_budget(data['pass4025_exact_revival_error_budget']);check_compiler(N,data['pass4026_exact_polar_compiler']);check_bridge(D,data['pass4027_mode_H1_bridge'])
 C=-A;theta=np.linalg.norm(C,'fro')/np.sqrt(480);assert abs(theta-1)<1e-12
 assert np.linalg.norm((C+12*np.eye(40))@(C+2*np.eye(40))@(C-4*np.eye(40)))<1e-10
 assert abs(math.log2(81)-data['pass4032_thermodynamic_holographic_capacity']['capacity_bits'])<1e-15
 print('PASS_4025_4032_PHYSICS_FIRST',saved)
if __name__=='__main__':main()
