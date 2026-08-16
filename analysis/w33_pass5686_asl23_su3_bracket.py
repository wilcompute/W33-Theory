#!/usr/bin/env python3
"""Pass5686: the first affine symmetry breaking that admits a Lie bracket is ASL(2,3).

Pass5681 proved Hom_AGL(2,3)(Lambda^2 V8,V8)=0 for the 8D augmentation module of
the nine affine sites.  Enumerating all linear subgroups of GL(2,3) shows that the
largest proper linear subgroup already changes this: the unique subgroup of order
24 is SL(2,3), so the affine subgroup ASL(2,3)=F3^2:SL(2,3) has order 216 and
multiplicity one in Hom(Lambda^2 V8,V8).

The unique bracket has an elementary affine-plane formula.  For sites x,y,z in
F3^2 let
  phi(x,y,z)=sgn_3(det(y-x,z-x)),  sgn_3(0)=0, sgn_3(1)=+1, sgn_3(2)=-1.
Contract the alternating 3-form phi with the Euclidean pairing on the zero-sum
site module V8 to define [f,g].  Exact integer checks give Jacobi=0 and Killing
form K=-54 I on V8.  Therefore the resulting compact semisimple real Lie algebra
has dimension eight and is the compact A2 form su(3).

Determinant-two affine transformations reverse phi and hence flip the bracket.
Thus full AGL forbids the bracket, while choosing affine orientation/chirality
reduces AGL to ASL and restores su(3).
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5686_ASL23_SU3_BRACKET.json'
Q=3;I2=(1,0,0,1)

def mat(A):return np.array(A,dtype=int).reshape(2,2)
def mul(A,B):return tuple(int(x) for x in ((mat(A)@mat(B))%3).flat)
def det(A):a,b,c,d=A;return (a*d-b*c)%3
GL=[A for A in itertools.product(range(3),repeat=4) if det(A)]
SL=[A for A in GL if det(A)==1]

def closure(gens):
    G={I2};front=[I2]
    while front:
        x=front.pop()
        for g in gens:
            y=mul(g,x)
            if y not in G:G.add(y);front.append(y)
    return frozenset(G)

def all_subgroups():
    subs={frozenset([I2])};front=[frozenset([I2])]
    while front:
        H=front.pop()
        for g in GL:
            if g in H:continue
            K=closure(list(H)+[g])
            if K not in subs:subs.add(K);front.append(K)
    return subs

pts=[(x,y) for x in range(3) for y in range(3)];idx={p:i for i,p in enumerate(pts)}
def perms(H):
    out=[]
    for A in H:
        a,b,c,d=A
        for tx,ty in pts:
            out.append(tuple(idx[((a*x+b*y+tx)%3,(c*x+d*y+ty)%3)] for x,y in pts))
    return out
def compose(p,q):return tuple(p[q[i]] for i in range(9))
def hom_mult(H):
    G=perms(H);num=0
    for g in G:
        chi=sum(i==g[i] for i in range(9))-1
        g2=compose(g,g);chi2=sum(i==g2[i] for i in range(9))-1
        wedge=(chi*chi-chi2)//2
        num+=wedge*chi
    return num//len(G)
def sgn(a):a%=3;return 0 if a==0 else (1 if a==1 else -1)

def main():
    assert (len(GL),len(SL))==(48,24)
    subs=all_subgroups();assert len(subs)==55
    hist=Counter((len(H),hom_mult(H)) for H in subs)
    assert hom_mult(frozenset(GL))==0 and hom_mult(frozenset(SL))==1
    larger=[H for H in subs if len(H)>24 and H!=frozenset(GL)];assert not larger
    order24=[H for H in subs if len(H)==24];assert len(order24)==1 and order24[0]==frozenset(SL)

    phi=np.zeros((9,9,9),dtype=int)
    for i,x in enumerate(pts):
      for j,y in enumerate(pts):
       for k,z in enumerate(pts):
        u=((y[0]-x[0])%3,(y[1]-x[1])%3);v=((z[0]-x[0])%3,(z[1]-x[1])%3)
        phi[i,j,k]=sgn(u[0]*v[1]-u[1]*v[0])
    assert np.max(abs(phi+phi.swapaxes(0,1)))==0
    assert np.max(abs(phi.sum(axis=2)))==0

    GASL=perms(SL);assert len(GASL)==216
    for g in GASL:
        assert np.array_equal(phi,phi[np.ix_(g,g,g)])
    A2=next(A for A in GL if det(A)==2);g=perms([A2])[0]
    assert np.array_equal(phi,-phi[np.ix_(g,g,g)])

    def br(f,g):return np.einsum('ijk,i,j->k',phi,f,g)
    basis=[]
    for i in range(8):
        v=np.zeros(9,dtype=int);v[i]=1;v[8]=-1;basis.append(v)
    for a,b,c in itertools.product(range(8),repeat=3):
        J=br(basis[a],br(basis[b],basis[c]))+br(basis[b],br(basis[c],basis[a]))+br(basis[c],br(basis[a],basis[b]))
        assert np.max(abs(J))==0

    eye=np.eye(9,dtype=int);ads=[]
    for i in range(9):
        M=np.zeros((9,9),dtype=int)
        for j in range(9):M[:,j]=br(eye[i],eye[j])
        ads.append(M)
    K=np.array([[int(np.trace(ads[i]@ads[j])) for j in range(9)] for i in range(9)],dtype=int)
    assert np.array_equal(K,-54*np.eye(9,dtype=int)+6*np.ones((9,9),dtype=int))
    eig=np.linalg.eigvalsh(K);assert np.sum(abs(eig)<1e-8)==1 and np.all(eig[:8]<-53.9)
    out={
      'pass':5686,'status':'ORIENTATION_PRESERVING_AFFINE_SUBGROUP_CARRIES_EXACT_COMPACT_SU3_BRACKET',
      'groups':{'AGL(2,3)':432,'ASL(2,3)':216,'linear_GL2(3)':48,'linear_SL2(3)':24},
      'subgroup_enumeration':{'linear_subgroups_of_GL2(3)':55,'unique_order24_subgroup':'SL(2,3)','Hom_AGL_Lambda2V8_to_V8':0,'Hom_ASL_Lambda2V8_to_V8':1},
      'bracket':'< [f,g],h > = sum_xyz sgn_3(det(y-x,z-x)) f(x)g(y)h(z)',
      'exact_checks':{'Jacobi':'zero on all 8^3 basis triples','Killing_on_R9':'-54 I_9 + 6 J_9','Killing_on_V8':'-54 I_8','ASL_equivariance':True,'determinant_reversing_AGL_action':'bracket sign reversal'},
      'lie_identification':'Nondegenerate negative Killing makes the 8D algebra compact semisimple; its complexification is the unique 8D semisimple type A2, hence the real algebra is su(3) up to overall bracket scale.',
      'physics_interpretation':'The affine eight becomes an su(3) adjoint only after choosing an orientation/chirality that breaks AGL(2,3) to its index-two ASL(2,3) subgroup.',
      'boundary':'This is an exact finite Lie-algebra emergence on the site augmentation module. It does not yet identify physical QCD gluons, derive a Yang-Mills kinetic term/coupling, or show which dynamical mechanism chooses affine orientation.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
