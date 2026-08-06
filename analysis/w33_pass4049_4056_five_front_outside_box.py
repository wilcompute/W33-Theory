#!/usr/bin/env python3
"""Exact verifier for Passes 4049-4056."""
from __future__ import annotations
import hashlib,itertools,json,math
from pathlib import Path
import networkx as nx
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_4049_4056_FIVE_FRONT_OUTSIDE_BOX.json'
MOD=3

def sha(x):
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def norm(v):
 v=tuple(x%MOD for x in v)
 for a in v:
  if a:return tuple((1 if a==1 else 2)*x%MOD for x in v)
 raise ValueError
def form(u,v):return (u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%MOD

def geometry():
 pts=sorted({norm(v) for v in itertools.product(range(3),repeat=4) if any(v)})
 W=nx.Graph();W.add_nodes_from(range(40))
 for i,u in enumerate(pts):
  for j in range(i+1,40):
   if form(u,pts[j])==0:W.add_edge(i,j)
 lines=sorted(tuple(sorted(c)) for c in nx.find_cliques(W) if len(c)==4);assert len(lines)==40
 N=np.zeros((40,40),dtype=np.int64)
 for j,line in enumerate(lines):
  for i in line:N[i,j]=1
 A=N@N.T-4*np.eye(40,dtype=np.int64)
 L=nx.Graph();L.add_nodes_from(range(80))
 for j,line in enumerate(lines):
  for p in line:L.add_edge(p,40+j)
 edges=sorted(tuple(sorted(e)) for e in L.edges())
 D=np.zeros((80,160),dtype=np.int64)
 for j,(p,l) in enumerate(edges):D[p,j]=-1;D[l,j]=1
 X=nx.line_graph(L);AX=nx.to_numpy_array(X,nodelist=edges,dtype=np.int64)
 I=np.eye(160,dtype=np.int64)
 CC=((AX-6*I)@(AX-2*I)@(AX@AX-4*AX-2*I))//2
 assert set(np.unique(CC))=={-27,-3,1,9,81}
 return W,L,edges,N,A,D,AX,CC

def canon_cycle(path):
 out=[]
 for seq in (path,list(reversed(path))):
  for i in range(len(seq)):out.append(tuple(seq[i:]+seq[:i]))
 return min(out)
def cycles_k(G,k):
 cycles=set()
 for start in G.nodes():
  stack=[(start,[start],{start})]
  while stack:
   u,path,seen=stack.pop()
   if len(path)==k:
    if G.has_edge(u,start):cycles.add(canon_cycle(path))
    continue
   for w in G.neighbors(u):
    if w!=start and w not in seen:stack.append((w,path+[w],seen|{w}))
 return sorted(cycles)

def check_qsvt():
 x=sp.symbols('x',real=True);s=sp.sqrt(6);r=s/4
 p3=(-sp.Rational(3,5)+16*s/15)*x+(sp.Rational(8,5)-16*s/15)*x**3
 xc=sp.sqrt(-sp.diff(p3,x).subs(x,0)/(3*(sp.Rational(8,5)-16*s/15)))
 assert float(p3.subs(x,xc))>1
 p5=(sp.Rational(9,25)+24*s/25)*x+(-sp.Rational(48,25)-152*s/225)*x**3+(sp.Rational(64,25)-64*s/225)*x**5
 K=4096*(29-6*s)/16875
 qp=x**2+(1+s/2)*x+(9+s)/8;qm=x**2-(1+s/2)*x+(9+s)/8
 assert sp.simplify(1-p5**2-K*(1-x**2)*(x**2-sp.Rational(3,8))**2*qp*qm)==0
 assert sp.simplify(qp.subs(x,0))>0 and sp.simplify((1+s/2)**2-4*(9+s)/8)<0
 for z,y in [(0,0),(r,1),(1,1),(-r,-1),(-1,-1)]:assert sp.simplify(p5.subs(x,z)-y)==0
 assert sp.simplify(sp.diff(p5,x).subs(x,r))==0

def ds_family(n,L,M,t):
 li=np.array([0.,10*M*M,16*M*M]);mi=np.array([1.,24.,15.]);wi=mi*np.exp(-t*li);Ei=(wi*li).sum()/wi.sum()
 k=np.arange(n);lb=(n/L)**2*(2-2*np.cos(2*np.pi*k/n));wb=np.exp(-t*lb);Eb=(wb*lb).sum()/wb.sum()
 return float(2*t*(Ei+4*Eb))

def check_magic():
 m=np.array([0,1,-1,1],complex)/np.sqrt(3);plus=np.array([1,1],complex)/np.sqrt(2)
 q=np.conjugate(plus)@m.reshape(2,2);assert abs(np.vdot(q,q).real-5/6)<1e-14;q/=np.linalg.norm(q)
 assert np.linalg.norm(q-np.array([-1,2])/np.sqrt(5))<1e-14
 X=np.array([[0,1],[1,0]],complex);qa=(np.eye(2)-1j*X)@q/np.sqrt(2)
 assert abs(qa[1]/qa[0]-(-4+3j)/5)<1e-14

def check_frame(L,edges):
 cyc=cycles_k(L,8);assert len(cyc)==1620;idx={e:i for i,e in enumerate(edges)};C=np.zeros((160,1620),dtype=np.int16)
 for j,c in enumerate(cyc):
  for a,b in zip(c,c[1:]+c[:1]):
   e=tuple(sorted((a,b)));p,l=e;C[idx[e],j]=1 if (a,b)==(p,l) else -1
 G=C.T@C;v,n=np.unique(np.abs(G),return_counts=True)
 assert dict(zip(map(int,v),map(int,n)))=={0:1922940,1:466560,2:155520,3:51840,4:25920,8:1620}
 assert abs(np.sum((G/8)**2)-32400)<1e-10 and abs(np.sum((G/8)**4)-79785/16)<1e-10

def heat_capacity(beta):
 E=np.array([0.,10.,16.]);g=np.array([1.,24.,15.]);w=g*np.exp(-beta*E);Z=w.sum();u=(w*E).sum()/Z;u2=(w*E**2).sum()/Z
 return beta*beta*(u2-u*u)

def main():
 data=json.loads(OUT.read_text());saved=data.pop('semantic_sha256');assert sha(data)==saved=='5f99f47f1a899b76c5e3e464a56440a63f51396a94c5d1ba9978ca65303b6946'
 W,L,edges,N,A,D,AX,CC=geometry();check_qsvt()
 assert dict(zip(*np.unique(CC[:,0],return_counts=True)))=={-27:6,-3:54,1:81,9:18,81:1}
 sample=data['pass4051_four_dimensional_fiber_scaling_family']['sample']['running_spectral_dimension']
 for t,val in sample.items():assert abs(ds_family(128,32,4,float(t))-val)<1e-12
 check_magic()
 U=-(np.eye(40)+A)/3+2*np.ones((40,40))/15;col=U[:,0];adj=set(W.neighbors(0));near={0}|adj
 assert set(np.round(col[list(near)],12))=={-0.2} and set(np.round(np.delete(col,list(near)),12))=={round(2/15,12)}
 assert np.linalg.norm(U@U-np.eye(40))<1e-12
 check_frame(L,edges)
 b=data['pass4056_outside_box_spectral_calorimeter']['schottky_peak']['beta'];c=data['pass4056_outside_box_spectral_calorimeter']['schottky_peak']['C_over_kB']
 assert abs(heat_capacity(b)-c)<1e-12 and heat_capacity(b)>heat_capacity(b-1e-5) and heat_capacity(b)>heat_capacity(b+1e-5)
 print('PASS_4049_4056_FIVE_FRONT_OUTSIDE_BOX',saved)
if __name__=='__main__':main()
