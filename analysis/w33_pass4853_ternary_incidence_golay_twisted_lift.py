#!/usr/bin/env python3
"""Pass4853 — lift the cycle/K3,3 bridge into ternary Levi homology.

Pass4807 identifies C^perp/L canonically with H1(Levi(GQ(4,2));F3).  Build the
1080 projective Levi 8-cycles and 360 projective K3,3 homology witnesses directly
on the 135 Levi edges.  The cycle lines span all 64 homology dimensions, whereas
the K3,3 witness lines span only 54.

The unweighted 1080x360 containment matrix has ternary kernel <1>.  If one could
orient the 360 projective K3,3 witnesses so their linear map factored through
that unweighted incidence quotient, the corresponding sign vector s in {+/-1}
would satisfy sum s_K h_K=0.  An exact mixed-integer modular feasibility test
proves no such full-support sign relation exists.  Thus the correct equivariant
lift is the orientation double cover/local sign system, not the untwisted
projective incidence matrix.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
import numpy as np,networkx as nx
from scipy import sparse
from scipy.optimize import milp,LinearConstraint,Bounds
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data/PART_W33_PASS4853_TERNARY_INCIDENCE_GOLAY_TWISTED_LIFT.json'

def Q(x):
 b=[(x>>i)&1 for i in range(6)];a,c,d,e,f,g=b;return (a*c+d*e+f+f*g+g)&1
def rankmod(A,p=3):
 A=np.array(A,dtype=np.int64)%p;r=0
 for c in range(A.shape[1]):
  q=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
  if q is None:continue
  A[[r,q]]=A[[q,r]];A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
  for i in range(A.shape[0]):
   if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
  r+=1
  if r==A.shape[0]:break
 return r

def main()->int:
 qp=[x for x in range(1,64) if Q(x)==0];pts=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(qp,2) if a^b in qp});lines=[tuple(i for i,P in enumerate(pts) if x in P) for x in qp]
 G=nx.Graph();G.add_nodes_from(range(27))
 for i,j in itertools.combinations(range(27),2):
  if set(lines[i])&set(lines[j]):G.add_edge(i,j)
 q4=[]
 for S in itertools.combinations(range(27),4):
  H=G.subgraph(S)
  if H.number_of_edges()==4 and set(dict(H.degree()).values())=={2} and nx.is_connected(H):q4.append(frozenset(S))
 K=[]
 for S in itertools.combinations(range(27),6):
  H=G.subgraph(S)
  if H.number_of_edges()==9 and set(dict(H.degree()).values())=={3} and nx.is_bipartite(H):
   A,B=nx.algorithms.bipartite.sets(H)
   if len(A)==len(B)==3:K.append(frozenset(S))
 assert len(q4)==1080 and len(K)==360
 M=np.zeros((1080,360),dtype=np.uint8)
 for j,S in enumerate(K):M[[i for i,C in enumerate(q4) if C<=S],j]=1
 assert rankmod(M,3)==359 and np.all((M@np.ones(360,dtype=int))%3==0)

 ledges=sorted((p,L) for L,S in enumerate(lines) for p in S);lei={e:i for i,e in enumerate(ledges)};assert len(ledges)==135
 D=np.zeros((72,135),dtype=int)
 for e,(p,L) in enumerate(ledges):D[p,e]=-1;D[45+L,e]=1
 assert rankmod(D,3)==71

 # One orientation for every projective four-cycle line.  Column rescaling by -1
 # changes no projective span, so rank is orientation-independent.
 C=np.zeros((135,1080),dtype=int)
 for j,S in enumerate(q4):
  H=G.subgraph(S);start=min(S);nxt=min(H.neighbors(start));cyc=[start,nxt]
  while len(cyc)<4:
   prev,cur=cyc[-2],cyc[-1];cyc.append(next(v for v in H.neighbors(cur) if v!=prev))
  for a,b in zip(cyc,cyc[1:]+cyc[:1]):
   p=next(iter(set(lines[a])&set(lines[b])));C[lei[(p,a)],j]-=1;C[lei[(p,b)],j]+=1
 assert not np.any((D@C)%3) and rankmod(C,3)==64

 # Projective K3,3 homology witness: orient from one bipartition to the other.
 H3=np.zeros((135,360),dtype=int)
 for j,S in enumerate(K):
  A,B=nx.algorithms.bipartite.sets(G.subgraph(S))
  if min(S) not in A:A,B=B,A
  for a in A:
   for b in B:
    if not G.has_edge(a,b):continue
    p=next(iter(set(lines[a])&set(lines[b])));H3[lei[(p,a)],j]-=1;H3[lei[(p,b)],j]+=1
 assert not np.any((D@H3)%3)
 rk=rankmod(H3,3);assert rk==54

 # No sign gauge can make the all-one incidence relation a homology relation.
 # s_j=1-2x_j with x_j binary; H3*s = 3q.
 rr=[];cc=[];dd=[];rhs=[]
 for i in range(135):
  for j in np.flatnonzero(H3[i]):rr.append(i);cc.append(int(j));dd.append(float(-2*H3[i,j]))
  rr.append(i);cc.append(360+i);dd.append(-3.);rhs.append(float(-H3[i].sum()))
 A=sparse.coo_matrix((dd,(rr,cc)),shape=(135,495)).tocsr();lo=np.r_[np.zeros(360),np.full(135,-20.)];hi=np.r_[np.ones(360),np.full(135,20.)]
 R=milp(np.zeros(495),integrality=np.ones(495),bounds=Bounds(lo,hi),constraints=LinearConstraint(A,np.array(rhs),np.array(rhs)),options={'presolve':True})
 assert R.status==2
 old=json.loads((ROOT/'data/PART_W33_PASS4807_GOLAY_LEVI_HOMOLOGY.json').read_text());assert old['Levi_H1_dim_F3']==64 and old['global_quotient_dim']==64
 out={'pass':4853,
  'ambient_ternary_filtration':'Pass4807: C^perp / (direct_sum_27 punctured ternary Golay G10) ~= H1(Levi(GQ(4,2));F3), dimension 64',
  'projective_Levi_8_cycle_family':{'count':1080,'span_dimension_F3':64,'spans_all_Levi_H1':True},
  'projective_K33_weight6_family':{'count':360,'span_dimension_F3':54,'codimension_in_Levi_H1':10,'kernel_dimension_of_oriented_witness_map':306},
  'unweighted_cycle_K33_incidence':{'shape':[1080,360],'rank_F3':359,'kernel':'<all-one>','linear_factorization_to_K33_homology_after_any_projective_sign_choice':False,'sign_gauge_MILP_status':'infeasible'},
  'twisted_lift':{'domain':'anti-invariant part of the 720-object oriented-K3,3 double cover over F3','deck_action':'orientation reversal acts by -1','map':'send an oriented K3,3 to its signed 18-edge Levi homology flow','PGSp_equivariant':True,'rank':54,'kernel_dimension':306,'composition_with_Golay_filtration':'via Pass4807 canonical isomorphism into the 64-dimensional nonlocal ternary logical quotient'},
  'obstruction':'The ordinary 360-object projective incidence forgets the orientation local system. Since ker_F3(M)=<1> but no +/- orientation section has signed witness sum zero, no untwisted linear map can carry the unweighted 1080_3--360_9 incidence quotient to the K3,3 homology witness map.',
  'theorem':'The exact binary-cycle/K3,3 incidence does lift to the ternary Golay/Levi filtration only after restoring the K3,3 orientation sign local system. The 360 projective weight-6 witnesses generate a 54-dimensional PGSp-invariant subspace of the 64-dimensional Levi homology quotient; the remaining ten homology dimensions are not generated by this canonical K3,3 family.',
  'boundary':'The 10-dimensional quotient is not identified with any pre-existing 10-dimensional object from its dimension alone. The orientation-double-cover lift is algebraic/homological, not a physical phase assignment.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
