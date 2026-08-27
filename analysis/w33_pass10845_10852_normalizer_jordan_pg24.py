#!/usr/bin/env python3
"""Pass10845-10852: exact Jordan decomposition of Wilson's C6 normalizer on V2.

Wilson's explicit complement n has order 6 on the natural F4^6 module.  In
characteristic two its Jordan decomposition is

    n = s u,   s=n^4 (order3),   u=n^3 (order2),   su=us.

The involution u has fixed F4-dimension3.  The semisimple part s has the three
F4 eigenvalues 1,w,w^2, each with multiplicity2 on F4^6.  On each two-space u
is one nontrivial J2 block, so

    n ~ J2(1) + J2(w) + J2(w^2).

Consequently Fix(u)=F4^3 inherits one eigenline of each eigenvalue.  On its 64
affine vectors s has 4 fixed vectors and20 3-cycles; projectively on PG(2,4)
it has 3 fixed points and6 3-cycles.

The unique s-fixed F4-line supplies a scalar-gauge class of three nonzero
translations.  Each translation commutes with s and pairs all64 fixed vectors
into32 pairs.  These are candidate local realizations of the J2^32 stable
correction from Pass10837, but are not asserted to extend through C13.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
import w33_pass10477_10484_h4_normalizer_27state_quotient as Q
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10845_10852_NORMALIZER_JORDAN_PG24.json'

def rank4(A):
    A=np.array(A,dtype=np.uint8).copy();r=0
    for c in range(A.shape[1]):
      q=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
      if q is None:continue
      if q!=r:A[[r,q]]=A[[q,r]]
      u=Q.invs(int(A[r,c]));A[r]=np.array([Q.mul(int(x),u) for x in A[r]],dtype=np.uint8)
      for i in range(A.shape[0]):
        if i!=r and A[i,c]:
          t=int(A[i,c]);A[i]^=np.array([Q.mul(t,int(x)) for x in A[r]],dtype=np.uint8)
      r+=1
    return r

def build_normalizer():
    g1=np.array([[3,0,0,1,2,0],[3,3,2,0,1,2],[2,0,0,0,0,2],[1,2,2,3,2,3],[2,0,1,2,0,0],[1,2,2,1,3,0]],dtype=np.uint8)
    g2=np.array([[3,1,2,2,1,1],[2,1,1,3,0,0],[2,3,1,0,3,0],[3,3,1,1,1,1],[3,2,1,1,2,1],[3,2,2,0,2,3]],dtype=np.uint8)
    g3=Q.pw(Q.mm(Q.pw(g1,4),g2),4);X=Q.pw(Q.mm(Q.mm(Q.mm(g1,g2),g1),Q.pw(g2,2)),3);g4=Q.conj(X,Q.pw(g2,4))
    A=Q.pw(Q.mm(Q.pw(Q.mm(g3,g4),3),g4),3);B=Q.pw(Q.mm(g3,g4),4);B=Q.mm(B,g4);B=Q.mm(B,g3);B=Q.mm(B,g4);B=Q.mm(B,Q.pw(Q.mm(g3,Q.pw(g4,2)),2));g5=Q.mm(Q.mm(A,Q.pw(B,3)),Q.invm(A))
    Y=Q.mm(Q.mm(Q.mm(g3,g4),g3),Q.pw(g4,2));g6=Q.mm(Q.pw(Y,-2),Q.mm(Q.pw(Q.mm(Q.mm(g3,g4),Q.pw(Y,2)),5),Q.pw(Y,2)))
    g7=Q.conj(g6,Q.mm(g5,Q.pw(g6,2)));g8=Q.mm(Q.mm(Q.mm(g5,g7),g5),Q.pw(g7,2));n=Q.mm(g5,g7)
    assert Q.order(g8)==13 and Q.order(n)==6 and np.array_equal(Q.conj(g8,n),Q.pw(g8,4))
    return g8,n

def main():
    g8,n=build_normalizer();I=Q.eye(6);u=Q.pw(n,3);s=Q.pw(n,4)
    assert Q.order(u)==2 and Q.order(s)==3 and np.array_equal(Q.mm(s,u),n)
    assert np.array_equal(Q.mm(s,u),Q.mm(u,s))
    fix_u=6-rank4(u^I);assert fix_u==3
    eig={}
    for lam in (1,2,3):
      M=s.copy()
      for i in range(6):M[i,i]^=lam
      eig[str(lam)]=6-rank4(M)
    assert eig=={'1':2,'2':2,'3':2}

    # Enumerate Fix(u) and s action directly.
    vecs=[np.array(v,dtype=np.uint8) for v in itertools.product(range(4),repeat=6)]
    F=[v for v in vecs if np.array_equal(Q.mv(u,v),v)];assert len(F)==64
    fi={tuple(map(int,v)):i for i,v in enumerate(F)}
    ps=[fi[tuple(map(int,Q.mv(s,v)))] for v in F]
    seen=set();aff=[]
    for i in range(64):
      if i in seen:continue
      C=[];j=i
      while j not in seen:seen.add(j);C.append(j);j=ps[j]
      aff.append(C)
    assert Counter(map(len,aff))==Counter({3:20,1:4})

    # Projective points of Fix(u): scalar triples among the 63 nonzero vectors.
    def norm(v):
      for x in v:
        if x:
          z=Q.invs(int(x));return tuple(Q.mul(z,int(y)) for y in v)
      raise ValueError
    P=sorted({norm(v) for v in F if any(v)});assert len(P)==21;pi={p:i for i,p in enumerate(P)}
    pp=[pi[norm(Q.mv(s,np.array(p,dtype=np.uint8)))] for p in P]
    seen=set();proj=[]
    for i in range(21):
      if i in seen:continue
      C=[];j=i
      while j not in seen:seen.add(j);C.append(j);j=pp[j]
      proj.append(C)
    assert Counter(map(len,proj))==Counter({3:6,1:3})

    # s-fixed affine vectors form the eigenvalue-1 F4 line (4 vectors).
    fixed_vecs=[F[i] for i,C in enumerate([[i] for i in range(64)]) if ps[i]==i]
    assert len(fixed_vecs)==4
    nonzero=[v for v in fixed_vecs if any(v)];assert len(nonzero)==3
    # Translation by any nonzero fixed vector commutes with s and is fixed-point-free.
    translation_pairings=[]
    for a in nonzero:
      perm=[]
      for v in F:
        w=v^a;perm.append(fi[tuple(map(int,w))])
      assert all(perm[perm[i]]==i and perm[i]!=i for i in range(64))
      assert all(perm[ps[i]]==ps[perm[i]] for i in range(64))
      translation_pairings.append(perm)
    assert len(translation_pairings)==3

    out={
      'schema':'w33.pass10845_10852.normalizer_jordan_pg24.v1','status':'PASS','passes':'10845-10852',
      'normalizer':{'n_order':6,'semisimple_part':'s=n^4, order3','unipotent_part':'u=n^3, order2','commuting':True,'n_equals_su':True},
      'F4_6_Jordan':{'Fix_u_dimension_F4':3,'s_eigenspace_dimensions':eig,'Jordan_form':'J2(1) + J2(w) + J2(w^2)','minimal_polynomial':'(x-1)^2(x-w)^2(x-w^2)^2 = x^6+1'},
      'fixed_cone':{'affine_vectors':64,'s_orbits_on_vectors':{'1':4,'3':20},'projective_points':'PG(2,4), 21 points','s_orbits_on_projective_points':{'1':3,'3':6}},
      'local_pairing_family':{'s_fixed_F4_line_vectors':4,'nonzero_translation_choices':3,'each_translation_pairs':32,'commutes_with_s':True,'interpretation':'a unique pairing orbit up to multiplication by F4^x; candidate local realization of the J2^32 correction'},
      'theorem':'The Wilson order-six complement has exact F4 Jordan form J2(1)+J2(w)+J2(w^2). Its involution-fixed cone is F4^3 and projectivizes to PG(2,4); the semisimple C3 fixes three projective eigendirections. The unique s-fixed F4 line supplies three scalar-equivalent fixed-point-free translations, each pairing the 64 fixed states into 32 C3-compatible pairs.',
      'boundary':'Exact F4 matrix calculation. The affine translations are permutations of the fixed 64-state set, not linear Co1 elements and not claimed to extend equivariantly through C13.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','Jordan':'J2(1)+J2(w)+J2(w2)','Fix_u':'F4^3','PG24_C3':'1^3 3^6','pairings':3}))
if __name__=='__main__':main()
