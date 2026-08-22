#!/usr/bin/env python3
"""Pass7337-7352: q=9 line-clique cuts, hyperbolic secants, and a hidden witness involution."""
from __future__ import annotations
import argparse,itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix
from w33_pass7107_q9_target_52 import ADD,MUL,NEG,INV,build,check_field
ROOT=Path(__file__).resolve().parents[1]
WIT=ROOT/'data'/'PART_W33_Q9_PARTIAL_OVOID_51.json';OUT=ROOT/'data'/'PART_W33_PASS7337_7352_Q9_CLIQUES_SECANTS_INVOLUTION.json'

def add(u,v):return tuple(ADD[a][b] for a,b in zip(u,v))
def scale(a,v):return tuple(MUL[a][x] for x in v)
def canon(v):
 z=INV[next(x for x in v if x)];return tuple(MUL[z][x] for x in v)
def line_through(a,b):return frozenset([b]+[canon(add(a,scale(t,b))) for t in range(9)])
def mm(A,B):
 return [[sumf(MUL[A[i][k]][B[k][j]] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def sumf(xs):
 z=0
 for x in xs:z=ADD[z][x]
 return z
def mv(A,x):return tuple(sumf(MUL[A[i][j]][x[j]] for j in range(4)) for i in range(4))
def tr(A):return [list(x) for x in zip(*A)]
def eye4(a=1):return [[a if i==j else 0 for j in range(4)] for i in range(4)]
def gf2rank(A):
 B={}
 for row in A:
  x=sum((int(v)&1)<<i for i,v in enumerate(row))
  while x:
   k=x.bit_length()-1
   if k in B:x^=B[k]
   else:B[k]=x;break
 return len(B)

def lp_bound(nvar,constraints):
 rr=[];cc=[];vv=[]
 for r,C in enumerate(constraints):
  for c in C:rr.append(r);cc.append(c);vv.append(1.0)
 A=coo_matrix((vv,(rr,cc)),shape=(len(constraints),nvar)).tocsr()
 res=linprog(-np.ones(nvar),A_ub=A,b_ub=np.ones(len(constraints)),bounds=(0,1),method='highs')
 assert res.success;return float(-res.fun)

def main():
 check_field();P,adj,B=build();assert len(P)==820 and {len(x) for x in adj}=={90};pi={p:i for i,p in enumerate(P)}
 S=list(map(int,json.loads(WIT.read_text())['point_indices']));Ss=set(S);assert len(S)==51
 # Exact 820 isotropic GQ lines, each a 10-clique; each point lies on 10 lines.
 L=set()
 for a in range(820):
  for b in adj[a]:
   if a<b:L.add(line_through(P[a],P[b]))
 assert len(L)==820 and {len(x) for x in L}=={10}
 deg=Counter(i for X in L for i in X);assert set(deg.values())=={10}
 assert all(all(v in adj[u] for u,v in itertools.combinations(X,2)) for X in L)
 # Fix a noncollinear pair WLOG as in Pass7107. Compare edge LP and line-clique LP.
 p0=0;p1=next(j for j in range(1,820) if j not in adj[p0]);keep=[i for i in range(820) if i not in adj[p0] and i not in adj[p1] and i not in (p0,p1)];idx={p:i for i,p in enumerate(keep)}
 assert len(keep)==648
 edges=[]
 for a in keep:
  for b in adj[a]:
   if b in idx and a<b:edges.append((idx[a],idx[b]))
 assert len(edges)==23040
 linecuts=[]
 for X in L:
  C=tuple(sorted(idx[p] for p in X if p in idx))
  if len(C)>1:linecuts.append(C)
 assert len(linecuts)==800 and Counter(map(len,linecuts))==Counter({8:720,9:80})
 edge_lp=lp_bound(648,edges)+2;line_lp=lp_bound(648,linecuts)+2
 assert abs(edge_lp-326.0)<1e-7 and abs(line_lp-82.0)<1e-7
 # Hyperbolic secants determined by common-center sets of witness pairs.
 sec=Counter()
 for a,b in itertools.combinations(S,2):sec[frozenset(adj[a]&adj[b])]+=1
 assert sum(sec.values())==1275 and all(len(X)==10 for X in sec)
 assert Counter(sec.values())==Counter({1:978,3:95,6:2})
 secants={2:978,3:95,4:2}
 # The old 103 special triads are exactly C(3,3)*95+C(4,3)*2.
 special=[]
 for a,b,c in itertools.combinations(range(51),3):
  if len(adj[S[a]]&adj[S[b]]&adj[S[c]])==10:special.append((a,b,c))
 assert len(special)==103 and 95+4*2==103
 H=np.zeros((103,51),dtype=np.uint8)
 for r,e in enumerate(special):H[r,list(e)]=1
 assert gf2rank(H)==51
 # The special-triad incidence hypergraph has one nontrivial automorphism; harden it by an exact GF(9) lift.
 A=[[6,0,0,0],[6,3,1,2],[1,0,4,2],[1,0,7,8]]
 J=[[0,1,0,0],[2,0,0,0],[0,0,0,1],[0,0,2,0]]
 assert mm(mm(tr(A),J),A)==J and mm(A,A)==eye4(2)
 perm=tuple(pi[canon(mv(A,p))] for p in P);assert len(set(perm))==820 and {perm[s] for s in S}==Ss
 wp={s:i for i,s in enumerate(S)};sp=tuple(wp[perm[s]] for s in S);assert sum(sp[i]==i for i in range(51))==1 and all(sp[sp[i]]==i for i in range(51))
 E={frozenset(e) for e in special};assert {frozenset(sp[i] for i in e) for e in E}==E
 fixed=[i for i in range(820) if perm[i]==i];assert len(fixed)==20 and len(Ss&set(fixed))==1
 e3=[(0,1,0,0),(0,0,1,1)];e6=[(5,4,1,0),(1,5,0,1)]
 for lam,Bs in ((3,e3),(6,e6)):
  assert all(mv(A,v)==scale(lam,v) for v in Bs) and B(Bs[0],Bs[1])==0
  X={pi[canon(add(scale(a,Bs[0]),scale(b,Bs[1])))] for a in range(9) for b in range(9) if a or b}
  assert len(X)==10 and X<=set(fixed)
 out={'schema':'w33.pass7337_7352.q9_cliques_secants_involution.v1','status':'PASS','passes':'7337-7352','line_clique_cuts':{'GQ_lines':820,'line_size':10,'fixed_noncollinear_pair_candidates':648,'pairwise_constraints':23040,'surviving_line_constraints':800,'line_candidate_sizes':{'8':720,'9':80},'pairwise_LP_total_bound':326,'line_clique_LP_total_bound':82,'interpretation':'820 geometric line inequalities dominate the pairwise edge model and recover the Hoffman-scale LP bound with far fewer rows'},'ten_center_triads':{'special_triads':103,'hyperbolic_secant_spectrum':{str(k):v for k,v in secants.items()},'meaning':'95 hyperbolic lines meet the witness in 3 points and 2 meet it in 4; the 103 triads are their C(m,3) presentations','direct_center-vs-secant_switch_cuts':'redundant with atomic collinearity conflicts; no false strengthening claimed'},'hidden_involution':{'matrix_GF9':A,'GF9_encoding':'k=(k mod 3)+(k//3)i, i^2=2','symplectic':True,'square':'A^2=-I','projective_order':2,'witness_cycle_shape':'1^1 2^25','projective_fixed_points':20,'fixed_locus':'two totally isotropic 10-point lines, the projectivized eigenspaces lambda=+i and -i','witness_fixed_points':1},'boundary':'The line-clique LP improves the relaxation but does not decide target 52. No bounded MILP timeout is promoted as an upper bound.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','line_LP':82,'secants':secants,'involution_fixed':20}))
if __name__=='__main__':main()
