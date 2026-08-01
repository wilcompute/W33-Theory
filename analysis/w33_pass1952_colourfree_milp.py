#!/usr/bin/env python3
"""Genuinely unpinned nine-colour frame MILP with one sound geometric lex leader."""
from __future__ import annotations
import argparse,collections,importlib.util,json,time
from pathlib import Path
import numpy as np
from scipy.optimize import Bounds,LinearConstraint,milp
from scipy.sparse import lil_matrix
ROOT=Path(__file__).resolve().parents[1];COMMON=ROOT/'analysis/w33_pass1801_1805_common.py';COMP=ROOT/'data/w33_pass1837_middle_layer_compression.json'
def load_common():
 s=importlib.util.spec_from_file_location('c',COMMON);m=importlib.util.module_from_spec(s);assert s.loader;s.loader.exec_module(m);return m
def compose(p,q):return tuple(p[q[i]] for i in range(len(q)))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=20);ap.add_argument('--colors',type=int,default=9);a=ap.parse_args();D=load_common().build_geometry();edge_frames=collections.defaultdict(list)
 for i,m in enumerate(D['matchings']):
  for e in m:edge_frames[e].append(i)
 pack=json.loads(COMP.read_text());F=[tuple(x) for x in pack['canonical_six_line_pack']];Fset={frozenset(x) for x in F}
 idp=tuple(range(40));seen={idp:(tuple(range(45)),tuple(range(540)))};Q=collections.deque([idp])
 while Q:
  pp=Q.popleft();op,fp=seen[pp]
  for gp,ge,gl,gf,go,gos in D['acts']+[D['outer']]:
   np_=compose(gp,pp)
   if np_ not in seen:seen[np_]=(tuple(go[op[i]] for i in range(45)),tuple(gf[fp[i]] for i in range(540)));Q.append(np_)
 stab=[fp for pp,(op,fp) in seen.items() if {frozenset(op[i] for i in x) for x in F}==Fset];g=max(stab,key=lambda p:sum(i!=p[i] for i in range(540)));gi=[0]*540
 for i,j in enumerate(g):gi[j]=i
 N=540;K=a.colors;ny=N*K;nq=N*K;NV=ny+nq+N+1;Y=lambda i,c:i*K+c;QV=lambda i,c:ny+i*K+c;EV=lambda i:ny+nq+i
 rows=[];lb=[];ub=[]
 def add(d,l,u):rows.append(d);lb.append(l);ub.append(u)
 for i in range(N):add({Y(i,c):1 for c in range(K)},1,1)
 for fs in edge_frames.values():
  for c in range(K):add({Y(i,c):1 for i in fs},1,1)
 for i in range(N):
  j=gi[i]
  for c in range(K):
   q=QV(i,c);x=Y(i,c);z=Y(j,c);add({q:1,x:-1},-np.inf,0);add({q:1,z:-1},-np.inf,0);add({q:-1,x:1,z:1},-np.inf,1)
 add({EV(0):1},1,1)
 for i in range(N):
  add({EV(i+1):1,EV(i):-1},-np.inf,0)
  d={EV(i+1):1};d.update({QV(i,c):-1 for c in range(K)});add(d,-np.inf,0)
  d={EV(i+1):-1,EV(i):1};d.update({QV(i,c):1 for c in range(K)});add(d,-np.inf,1)
  d={EV(i):K-1}
  for c in range(K):d[Y(i,c)]=d.get(Y(i,c),0)+c;d[Y(gi[i],c)]=d.get(Y(gi[i],c),0)-c
  add(d,-np.inf,K-1)
 A=lil_matrix((len(rows),NV),dtype=float)
 for r,d in enumerate(rows):
  for c,v in d.items():A[r,c]=v
 t=time.time();res=milp(np.zeros(NV),integrality=np.ones(NV),bounds=Bounds(np.zeros(NV),np.ones(NV)),constraints=LinearConstraint(A.tocsr(),np.array(lb),np.array(ub)),options={'time_limit':a.seconds,'mip_rel_gap':0})
 out={'status_code':int(res.status),'message':res.message,'seconds':time.time()-t,'variables':NV,'constraints':len(rows),'nonzeros':int(A.nnz),'primal_solution':res.x is not None,'node_count':getattr(res,'mip_node_count',None),'mip_gap':getattr(res,'mip_gap',None)}
 print(json.dumps(out,indent=2,sort_keys=True));return out
if __name__=='__main__':main()
