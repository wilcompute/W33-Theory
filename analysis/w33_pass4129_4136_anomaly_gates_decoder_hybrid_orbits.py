#!/usr/bin/env python3
"""Deterministic verifier for Passes 4129-4136."""
from __future__ import annotations
import bisect, collections, hashlib, itertools, json, math, subprocess, tempfile
from pathlib import Path
import networkx as nx
import numpy as np
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form

ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/'data/PART_4129_4136_ANOMALY_GATES_DECODER_HYBRID_ORBITS_BONKERS.json'
ANOM=ROOT/'data/w33_pass4129_anomaly_repair_optimization.json'
HYB=ROOT/'data/w33_pass4132_hybrid_sin_active_router.json'
SCHED=ROOT/'data/w33_pass4132_hybrid_permutation_schedule.json'
ORB=ROOT/'data/w33_pass4133_exact_bivalent_orbit_catalogue.json'
CPP=ROOT/'analysis/w33_pass4133_exact_bivalent_enumerator.cpp'

def chash(d):
 x=dict(d);x.pop('semantic_sha256',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def canon(v):
 v=tuple(x%3 for x in v)
 for x in v:
  if x:
   z=1 if x==1 else 2
   return tuple(z*y%3 for y in v)
def symp(u,v):return (u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%3
def geometry():
 pts=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)});idx={p:i for i,p in enumerate(pts)}
 A=np.zeros((40,40),int)
 for i,u in enumerate(pts):
  for j,v in enumerate(pts):
   if i!=j and symp(u,v)==0:A[i,j]=1
 lines=set()
 for i,u in enumerate(pts):
  for j,v in enumerate(pts):
   if j<=i or symp(u,v):continue
   S={idx[canon(tuple(a*u[k]+b*v[k] for k in range(4)))] for a,b in itertools.product(range(3),repeat=2) if a or b}
   if len(S)==4:lines.add(tuple(sorted(S)))
 lines=sorted(lines);E=[];G=nx.Graph();G.add_nodes_from(range(80))
 for l,L in enumerate(lines):
  for p in L:E.append((p,40+l));G.add_edge(p,40+l)
 D=np.zeros((80,160),int)
 for e,(p,l) in enumerate(E):D[p,e]=1;D[l,e]=-1
 return pts,A,lines,E,D,G
def lds(p):
 tails=[]
 for x in p:
  x=-x;i=bisect.bisect_left(tails,x)
  if i==len(tails):tails.append(x)
  else:tails[i]=x
 return len(tails)
def phase_z1(K=256):
 ph=math.atan2(3,-4);th=math.pi/(K+2)
 c=np.array([math.sqrt(2/(K+2))*math.sin((n+1)*th) for n in range(K+1)])
 C=float(c[:-1]@c[1:]);B=float(c[0]*c[0])
 return np.exp(1j*ph)*C+np.exp(-1j*K*ph)*B

def cycle_theta_audit(G,E):
 eid={tuple(sorted(e)):i for i,e in enumerate(E)};adj={u:sorted(G.neighbors(u)) for u in G}
 cycles=set()
 for start in range(80):
  stack=[(start,[start],{start})]
  while stack:
   u,path,seen=stack.pop()
   for v in adj[u]:
    if v==start and 8<=len(path)<=14 and len(path)%2==0:
     c=path[:];n=len(c);forms=[]
     for q in (c,list(reversed(c))):
      for k in range(n):forms.append(tuple(q[k:]+q[:k]))
     cycles.add(min(forms))
    elif v>start and v not in seen and len(path)<14:
     stack.append((v,path+[v],seen|{v}))
 cnt=collections.Counter(map(len,cycles));assert cnt=={8:1620,10:5184,12:43200,14:336960}
 w3=[(e+1)**3 for e in range(160)];w5=[(e+1)**5 for e in range(160)]
 for c in cycles:
  es=[eid[tuple(sorted((c[i],c[(i+1)%len(c)])))] for i in range(len(c))]
  a=sum((1 if i%2==0 else -1)*w3[e] for i,e in enumerate(es));b=sum((1 if i%2==0 else -1)*w5[e] for i,e in enumerate(es))
  assert a or b
 paths=collections.defaultdict(list)
 for a in range(80):
  stack=[(a,[a],{a})]
  while stack:
   u,p,s=stack.pop()
   if len(p)-1>=6:continue
   for v in adj[u]:
    if v in s:continue
    q=p+[v]
    if v>a:paths[(a,v)].append(q)
    stack.append((v,q,s|{v}))
 def flow(path):
  z={}
  for x,y in zip(path,path[1:]):
   e=eid[tuple(sorted((x,y)))];p,l=E[e];z[e]=1 if (x==p and y==l) else -1
  return z
 types=collections.Counter()
 for pair,ps in paths.items():
  for i,p in enumerate(ps):
   ip=set(p[1:-1]);lp=len(p)-1
   for j in range(i+1,len(ps)):
    q=ps[j];lq=len(q)-1;iq=set(q[1:-1])
    if lp+lq<8 or ip&iq:continue
    for k in range(j+1,len(ps)):
     r=ps[k];lr=len(r)-1;ir=set(r[1:-1])
     if lp+lr<8 or lq+lr<8 or lp+lq+lr>14 or ip&ir or iq&ir:continue
     fs=[flow(x) for x in (p,q,r)];keys=set().union(*[set(x) for x in fs])
     c1={e:fs[0].get(e,0)-fs[2].get(e,0) for e in keys};c2={e:fs[1].get(e,0)-fs[2].get(e,0) for e in keys}
     a1=sum(w3[e]*v for e,v in c1.items());a2=sum(w3[e]*v for e,v in c2.items());b1=sum(w5[e]*v for e,v in c1.items());b2=sum(w5[e]*v for e,v in c2.items())
     assert a1*b2-a2*b1
     types[tuple(sorted((lp,lq,lr)))]+=1
 assert types=={(4,4,4):4320,(3,5,5):25920,(4,4,6):25920,(2,6,6):77760}
 return cnt,types

def main():
 cert=json.loads(CERT.read_text());an=json.loads(ANOM.read_text());hy=json.loads(HYB.read_text());sc=json.loads(SCHED.read_text());orb=json.loads(ORB.read_text())
 for d in (cert,an,hy,sc,orb):assert chash(d)==d['semantic_sha256']
 pts,A,lines,E,D,G=geometry();assert len(pts)==len(lines)==40 and len(E)==160 and np.all(A.sum(1)==12)
 assert np.allclose(np.linalg.eigvalsh(A),[-4]*15+[2]*24+[12]);assert nx.girth(G)==8 and np.linalg.matrix_rank(D)==79
 M=Matrix(an['integer_anomaly_matrix']);assert smith_normal_form(M,domain=ZZ).diagonal()==Matrix.diag(1,1,1,3).diagonal();assert M.nullspace()[0]==Matrix([1,1,1,1,1])
 w=[1,15,15,24,1];dims=[6,3,3,2,1];assert min((sum(d*abs(t-x) for d,x in zip(dims,w)),t) for t in range(40))==(116,15)
 assert an['PSp_module_respecting_targets']['V15']['added_dimension']==190
 z=phase_z1();assert abs(z-complex(*cert['pass4130_relational_logical_gates']['K256_z1']))<2e-13;assert math.comb(31,15)==300540195
 incidence={(p,l) for l,L in enumerate(lines) for p in L};seen=set()
 for perm in sc['permutations']:
  assert sorted(perm)==list(range(40));seen|={(p,l) for p,l in enumerate(perm)}
 assert seen==incidence and [lds(p) for p in sc['permutations']]==[8,8,9,8]
 cyc=nx.minimum_cycle_basis(G)[0];assert len(cyc)==8
 W=cert['pass4131_decoder_through_seven']['d3_MILP_witness_edges'];assert len(W)==16 and len(W)-np.linalg.matrix_rank(D[:,W])==3
 cnt,types=cycle_theta_audit(G,E)
 with tempfile.TemporaryDirectory() as td:
  exe=Path(td)/'enum';subprocess.run(['g++','-O3','-std=c++17',str(CPP),'-o',str(exe)],check=True)
  out=subprocess.check_output([str(exe)],text=True).strip().splitlines()
 assert out==['-2 5 33264 302595 4472319893450457651','4 8 432 16131 4032860845500769235']
 assert sum(orb['lambda10_bivalent']['class_solution_counts'])==33264 and orb['lambda16_maxcut']['cuts_mod_global_reversal']==216
 I=np.eye(40);J=np.ones((40,40));P0=J/40;P2=2*I/3+A/6-J/15;Pm=I/3-A/6+J/24
 assert np.allclose(P0+P2+Pm,I) and all(np.allclose(P@P,P) for P in (P0,P2,Pm))
 L=12*I-A;e,V=np.linalg.eigh(L);U8=V@np.diag(np.exp(-1j*np.pi*e/8))@V.T;U5=V@np.diag(np.exp(-1j*np.pi*e/5))@V.T
 assert np.allclose(np.linalg.matrix_power(U8,8),I) and np.allclose(np.linalg.matrix_power(U5,5),I) and np.allclose(U8@U5,U5@U8)
 print(json.dumps({'status':cert['status'],'semantic_sha256':cert['semantic_sha256'],'cycle_counts':dict(cnt),'theta_total':sum(types.values()),'lambda10_signs':33264,'lambda16_signs':432,'hybrid_depth':9},sort_keys=True))
if __name__=='__main__':main()
