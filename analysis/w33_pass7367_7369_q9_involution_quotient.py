#!/usr/bin/env python3
"""Pass7367-7369: quotient the frozen q=9 witness problem by its exact projective involution."""
from __future__ import annotations
import argparse,itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
from scipy.optimize import linprog,milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix
from w33_pass7107_q9_target_52 import build,check_field,ADD,MUL,INV
ROOT=Path(__file__).resolve().parents[1]
WIT=ROOT/'data'/'PART_W33_Q9_PARTIAL_OVOID_51.json'
OUT=ROOT/'data'/'PART_W33_PASS7367_7369_Q9_INVOLUTION_QUOTIENT.json'
A=[[6,0,0,0],[6,3,1,2],[1,0,4,2],[1,0,7,8]]

def sf(xs):
 z=0
 for x in xs:z=ADD[z][x]
 return z
def mv(x):return tuple(sf(MUL[A[i][j]][x[j]] for j in range(4)) for i in range(4))
def canon(v):
 z=INV[next(x for x in v if x)];return tuple(MUL[z][x] for x in v)
def add(a,b):return tuple(ADD[x][y] for x,y in zip(a,b))
def scale(t,v):return tuple(MUL[t][x] for x in v)
def line(a,b,pi):return frozenset(pi[canon(b)] for _ in [0])|frozenset(pi[canon(add(a,scale(t,b)))] for t in range(9))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--search-seconds',type=float,default=0.0);args=ap.parse_args()
 check_field();P,adj,B=build();pi={p:i for i,p in enumerate(P)};perm=tuple(pi[canon(mv(p))] for p in P);assert all(perm[perm[i]]==i for i in range(820))
 fixed=[i for i in range(820) if perm[i]==i];assert len(fixed)==20
 seen=set();orbs=[]
 for i in range(820):
  if i in seen:continue
  O=tuple(sorted({i,perm[i]}));seen.update(O);orbs.append(O)
 assert Counter(map(len,orbs))==Counter({2:400,1:20})
 oi={p:k for k,O in enumerate(orbs) for p in O}
 internal_bad=[k for k,O in enumerate(orbs) if len(O)==2 and O[1] in adj[O[0]]];assert len(internal_bad)==40
 valid=[k for k in range(420) if k not in internal_bad];assert len(valid)==380
 # Exact 820 isotropic lines.
 L=set()
 for a in range(820):
  for b in adj[a]:
   if a<b:L.add(line(P[a],P[b],pi))
 assert len(L)==820 and {len(X) for X in L}=={10}
 vi={k:i for i,k in enumerate(valid)};rr=[];cc=[];vv=[]
 for r,X in enumerate(L):
  cnt=Counter(oi[p] for p in X)
  for k,z in cnt.items():
   if k in vi:rr.append(r);cc.append(vi[k]);vv.append(z)
 M=coo_matrix((vv,(rr,cc)),shape=(820,380)).tocsr();w=np.array([len(orbs[k]) for k in valid],dtype=float)
 lp=linprog(-w,A_ub=M,b_ub=np.ones(820),bounds=(0,1),method='highs');assert lp.success and abs(-lp.fun-74)<1e-7
 S=set(map(int,json.loads(WIT.read_text())['point_indices']));assert {perm[s] for s in S}==S
 selected_orbits={oi[s] for s in S};assert sum(len(orbs[k]) for k in selected_orbits)==51 and Counter(len(orbs[k]) for k in selected_orbits)==Counter({2:25,1:1})
 assert all(b not in adj[a] for a,b in itertools.combinations(S,2))
 search={'attempted':False,'target':52,'resolved':False}
 if args.search_seconds>0:
  search['attempted']=True
  cons=[LinearConstraint(M,-np.inf,np.ones(820)),LinearConstraint(w.reshape(1,-1),52,np.inf)]
  z=milp(c=np.zeros(380),integrality=np.ones(380),bounds=Bounds(0,1),constraints=cons,options={'time_limit':args.search_seconds,'mip_rel_gap':0.0,'presolve':True})
  search.update({'status':int(z.status),'message':str(z.message),'found_size':None if z.x is None else float(w@z.x),'resolved':bool(z.status in (0,2))})
 out={'schema':'w33.pass7367_7369.q9_involution_quotient.v1','status':'PASS','point_orbits':{'fixed':20,'pairs':400,'total':420},'internally_collinear_pair_orbits_forbidden':40,'quotient_binary_variables':380,'line_constraints':820,'invariant_LP_bound':74,'frozen_51_witness_quotient':{'invariant':True,'orbit_shape':'1 fixed + 25 pairs','size':51},'target52_parity':'An involution-invariant 52-set must use an even number of fixed points; because the fixed locus is two isotropic lines, only 0 or 2 fixed points can occur.','search':search,'boundary':'This quotient classifies the A-invariant branch only. Infeasibility here would not rule out a non-A-invariant 52-set; a timeout is never promoted as an upper bound.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','orbits':420,'variables':380,'LP':74,'witness_orbits':26}))
if __name__=='__main__':main()
