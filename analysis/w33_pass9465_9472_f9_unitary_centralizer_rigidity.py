#!/usr/bin/env python3
"""Pass9465-9472: F9 unitary centralizer and transverse-glue rigidity.

Build the exact K,S,R package from Pass9237-9244.  The compatible symmetric form
B=K R^T makes C_Sp(K)(R)=Sp(K) cap O(B), the F3-realization of U(6,3).
We also exhaust the signed-coordinate monomial stabilizer of the *ordered pair*
(Golay glue, E6-relative glue).
"""
from __future__ import annotations
import itertools,json,sys
from pathlib import Path
from collections import Counter
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_rank24_root_shadow_core as rs
P=3
OUT=ROOT/'data/PART_W33_PASS9465_9472_F9_UNITARY_CENTRALIZER_RIGIDITY.json'

def detmod(A,p=3):
 A=np.array(A,dtype=np.int64)%p;n=A.shape[0];d=1
 for c in range(n):
  q=next((i for i in range(c,n) if A[i,c]),None)
  if q is None:return 0
  if q!=c:A[[c,q]]=A[[q,c]];d=-d
  d=d*int(A[c,c])%p;iv=pow(int(A[c,c]),-1,p)
  for i in range(c+1,n):
   if A[i,c]:A[i]=(A[i]-A[i,c]*iv*A[c])%p
 return d%p

def span(g):
 return {tuple(int(x) for x in (np.array(c,dtype=np.int64)@g)%P)
         for c in itertools.product(range(P),repeat=g.shape[0])}

def main():
 G=np.array(rs.GOLAY12,dtype=np.int64)%P
 old=json.loads((ROOT/'data/PART_W33_PASS9185_9196_GOLAY_TETRACODE_GLUE_BIFURCATION.json').read_text())
 E=np.array(old['N(E6^4)_relative_glue']['generator_rref'],dtype=np.int64)%P
 pairing=G@E.T%P;H=rs.inv_mod(pairing,P).T@E%P
 C=np.vstack([G,H])%P;Ci=rs.inv_mod(C,P)
 I6=np.eye(6,dtype=np.int64);Z=np.zeros((6,6),dtype=np.int64)
 D=np.block([[I6,Z],[Z,-I6]])%P;XCH=np.block([[Z,I6],[I6,Z]])%P
 K=Ci@D@C%P;S=Ci@XCH@C%P;R=K@S%P;I12=np.eye(12,dtype=np.int64)%P
 B=K@R.T%P
 assert np.array_equal(K.T%P,(-K)%P) and rs.rank_modp(K,P)==12
 assert np.array_equal(R@R%P,(-I12)%P) and np.array_equal(R@K@R.T%P,K)
 assert np.array_equal(B,B.T) and rs.rank_modp(B,P)==12
 assert np.array_equal(S@B@S.T%P,B) and np.array_equal(S@K@S.T%P,(-K)%P)
 assert np.array_equal(S@R@S%P,(-R)%P)
 # Orthogonal package: 12D B is plus type, while both glue halves are B-orthogonal O^-(6,3).
 BG=G@B@G.T%P;BE=E@B@E.T%P;cross=G@B@E.T%P
 assert not cross.any() and rs.rank_modp(BG,P)==rs.rank_modp(BE,P)==6
 assert detmod(B)==detmod(BG)==detmod(BE)==1
 # In even dimension 2m over F3, plus iff (-1)^m det is square.  m=6 -> plus; m=3 -> minus.
 assert detmod(B) in (1,) and ((-detmod(BG))%P)==2 and ((-detmod(BE))%P)==2
 # Classical centralizer order: U(6,3)=3^15 prod_i(3^i-(-1)^i).
 factors=[P**i-(-1)**i for i in range(1,7)]
 uorder=P**15
 for f in factors:uorder*=f
 assert factors==[4,8,28,80,244,728] and uorder==182699779456696320
 # Exhaust the signed-coordinate monomial automorphisms of E.  Its eight weight-3 words
 # intrinsically determine four disjoint triples, so every monomial automorphism is in
 # S_3 wr S_4 with signs restricted by the local weight-3 line.
 EW=span(E);GW=span(G)
 w3=[w for w in EW if sum(x!=0 for x in w)==3];assert len(w3)==8
 supports=sorted({tuple(i for i,x in enumerate(w) if x) for w in w3})
 assert supports==[(0,1,2),(3,4,5),(6,7,8),(9,10,11)]
 u=np.array(next(w for w in w3 if tuple(i for i,x in enumerate(w) if x)==supports[0])[:3],dtype=np.int64)%P
 first=next(int(x) for x in u if x);u=u*pow(first,-1,P)%P
 local=[]
 for perm in itertools.permutations(range(3)):
  for signs in itertools.product([1,2],repeat=3):
   M=np.zeros((3,3),dtype=np.int64)
   for src,dst in enumerate(perm):M[src,dst]=signs[src]
   v=u@M%P
   if tuple(v) in (tuple(u),tuple((-u)%P)):local.append(M)
 assert len(local)==12
 e_aut=0;common=[]
 for bp in itertools.permutations(range(4)):
  for inds in itertools.product(range(12),repeat=4):
   M=np.zeros((12,12),dtype=np.int64)
   for sb,tb in enumerate(bp):M[3*sb:3*sb+3,3*tb:3*tb+3]=local[inds[sb]]
   if not all(tuple(int(x) for x in row) in EW for row in E@M%P):continue
   e_aut+=1
   if all(tuple(int(x) for x in row) in GW for row in G@M%P):common.append(M)
 assert e_aut==62208 and len(common)==2
 assert any(np.array_equal(M,I12) for M in common) and any(np.array_equal(M,(-I12)%P) for M in common)
 out={'schema':'w33.pass9465_9472.f9_unitary_centralizer_rigidity.v1','status':'PASS','passes':'9465-9472',
  'compatible_forms':{'K':'alternating rank 12','R':'R^2=-I, symplectic','B=K R^T':'symmetric nondegenerate O+(12,3)','Golay_restriction':'O-(6,3)','E6_glue_restriction':'O-(6,3)','B_cross_pairing_G_E':0,'S':'B-isometry, K-anti-isometry, SRS=-R'},
  'unitary_centralizer':{'identification':'C_Sp(12,3)(R) = Sp(K) intersection O(B) ~= U(6,3)','order_factors':factors,'order':uorder,'SU_order':uorder//4,'PSU_order':uorder//8},
  'coordinate_monomial_rigidity':{'E6_relative_glue_signed_monomial_order':e_aut,'ordered_pair_common_signed_monomials':2,'common_group':'{+I,-I}','projective_common_group_order':1},
  'theorem':'The transverse-glue F9 structure is a finite Hermitian package: B=KR^T is plus-type in dimension 12, while the Golay and E6-relative glue halves are mutually B-orthogonal minus-type 6-spaces and simultaneously K-Lagrangians. The symplectic centralizer of R is U(6,3). Despite that enormous ambient unitary symmetry, the ordered pair of concrete glue codes is projectively rigid inside the full signed-coordinate monomial group: its common stabilizer is only +/-I.',
  'boundary':'The U(6,3) identification uses the standard classical-group equivalence between an F3 symplectic space with R^2=-I and a Hermitian F9-space. The signed-monomial rigidity is exhaustively computed here. No canonical identification with the independent Suzuki 12D module is assumed.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','U6_3':uorder,'E_monomial':e_aut,'common':len(common)}));return 0
if __name__=='__main__':raise SystemExit(main())
