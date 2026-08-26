#!/usr/bin/env python3
"""Pass10453-10476 closure: explicit F4^6 coordinates from Wilson's A4 x G2(4) subgroup.

This script extends w33_pass10453_10476_explicit_a4g24_v2_coordinates.py.
It evaluates Wilson's exact subgroup words in the stored Co1 module and proves that

  E = Fix(a1) = Fix(V4)

is a 12-dimensional, totally singular, type-4-free orbit-7 generator.  It then:

* constructs the order-3 scalar S=a2|E and verifies S^2+S+I=0;
* builds six explicit F4 basis vectors of E;
* exports 6x6 F4 matrices for the Wilson G2(4) generators;
* factors Phi_13 over F4 through the exact minimal polynomial of g1;
* compares E to stored canonical V2=im((I-M8)^2), proving E cap V2=0;
* uses the perfect E--V2 Leech pairing to construct the dual order-3 F4 scalar on
  the stored V2.

The last operator is a canonical orthogonal/polarization construction.  It is NOT claimed
here to be a Co1 word; the missing Co1 conjugator E -> V2 remains a separate target.
"""
from __future__ import annotations
from collections import deque
import json,sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass10453_10476_explicit_a4g24_v2_coordinates as base
from w33_pass7333_leech_d4_form import load_flat,invariant_gram

OUT=ROOT/'data/PART_W33_PASS10453_10476_EXPLICIT_A4G24_COORDINATE_CLOSURE.json'


def vecint(v):
    x=0
    for i,b in enumerate(np.array(v,dtype=np.uint8).tolist()):
        if b:x|=1<<i
    return x

def all_span_ints(B):
    vals=[0]
    for j in range(B.shape[1]):
        b=vecint(B[:,j]);vals += [x^b for x in vals]
    return vals

def orbit_bits(gens,start,cap=200000):
    start=vecint(start);seen={start};Q=deque([start])
    maps=[[vecint(A[:,j]) for j in range(24)] for A in gens]
    def act(x,mp):
        y=0;j=0
        while x:
            if x&1:y^=mp[j]
            x>>=1;j+=1
        return y
    while Q:
        x=Q.popleft()
        for mp in maps:
            y=act(x,mp)
            if y not in seen:
                seen.add(y);Q.append(y)
                if len(seen)>cap:raise RuntimeError('orbit cap exceeded')
    return seen

def inv2n(A):
    A=np.array(A,dtype=np.uint8)&1;n=A.shape[0]
    X=np.concatenate([A,np.eye(n,dtype=np.uint8)],axis=1)
    for c in range(n):
        q=next(i for i in range(c,n) if X[i,c])
        X[[c,q]]=X[[q,c]]
        for i in range(n):
            if i!=c and X[i,c]:X[i]^=X[c]
    return X[:,n:]
def solve_coords(B,Y):
    B=np.array(B,dtype=np.uint8)&1;Y=np.array(Y,dtype=np.uint8)&1
    n=B.shape[1];m=B.shape[0];X=np.zeros((n,Y.shape[1]),dtype=np.uint8)
    for j in range(Y.shape[1]):
        A=np.concatenate([B.copy(),Y[:,j:j+1]],axis=1);r=0;piv=[]
        for c in range(n):
            q=next((i for i in range(r,m) if A[i,c]),None)
            if q is None:continue
            A[[r,q]]=A[[q,r]]
            for i in range(m):
                if i!=r and A[i,c]:A[i]^=A[r]
            piv.append(c);r+=1
        assert r==n
        x=np.zeros(n,dtype=np.uint8)
        for i,c in enumerate(piv):x[c]=A[i,-1]
        assert np.array_equal((B@x)&1,Y[:,j])
        X[:,j]=x
    return X

# F4 encoding: 0,1,w,1+w -> 0,1,2,3 with w^2+w+1=0.
def f4_mul(x,y):
    a=x&1;b=(x>>1)&1;c=y&1;d=(y>>1)&1
    return (a*c ^ b*d) | ((a*d ^ b*c ^ b*d)<<1)
def f4_pow(x,n):
    r=1
    while n:
        if n&1:r=f4_mul(r,x)
        x=f4_mul(x,x);n//=2
    return r
def f4_inv(x):
    assert x;return f4_pow(x,2)
def f4_mm(A,B):
    A=np.array(A,dtype=np.uint8);B=np.array(B,dtype=np.uint8)
    C=np.zeros((A.shape[0],B.shape[1]),dtype=np.uint8)
    for i in range(A.shape[0]):
        for k in range(A.shape[1]):
            if A[i,k]:
                for j in range(B.shape[1]):
                    if B[k,j]:C[i,j]^=f4_mul(int(A[i,k]),int(B[k,j]))
    return C
def f4_solve(A,b):
    A=np.array(A,dtype=np.uint8);b=np.array(b,dtype=np.uint8).reshape(-1,1)
    M=np.concatenate([A,b],axis=1);m,n=A.shape;r=0;pivs=[]
    for c in range(n):
        q=next((i for i in range(r,m) if M[i,c]),None)
        if q is None:continue
        M[[r,q]]=M[[q,r]];u=f4_inv(int(M[r,c]))
        M[r]=np.array([f4_mul(int(v),u) for v in M[r]],dtype=np.uint8)
        for i in range(m):
            if i!=r and M[i,c]:
                t=int(M[i,c]);M[i]^=np.array([f4_mul(t,int(v)) for v in M[r]],dtype=np.uint8)
        pivs.append(c);r+=1
    x=np.zeros(n,dtype=np.uint8)
    for i,c in enumerate(pivs):x[c]=M[i,n]
    return x,r
def f4_poly_mul(p,q):
    r=[0]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):r[i+j]^=f4_mul(a,b)
    return r

def main():
    a,b=base.load_pair()
    checks,els=base.build(a,b,'x^-1y^-1xy')
    assert checks['c1_order']==26 and checks['a2_order']==3 and checks['g1_order']==13
    assert checks['g2_order']==13 and checks['g1g2_order']==15 and checks['A4_G2_commute']
    I=base.eye()

    E=base.kernel((els['a1']-I)&1);assert E.shape==(24,12)
    assert all(base.invariant(E,els[k]) for k in ('a1','a2','g1','g2'))

    # Three V4 involutions have one common 12-space, equal to Fix(a1).
    def conj(x,y):return base.mm(base.mm(base.inv2(y),x),y)
    V4=[els['a1'],conj(els['a1'],els['a2']),conj(els['a1'],base.pw(els['a2'],2))]
    F=base.kernel(np.vstack([((v-I)&1) for v in V4]))
    assert F.shape==(24,12) and base.same_space(F,E)

    # Reconstruct positive Leech Gram and certify total singularity/type-4-free.
    gens_int=load_flat(ROOT/'analysis/_co0_G.txt')
    G,dim=invariant_gram(gens_int);assert dim==1 and G is not None
    if G[0,0]<0:G=-G
    Ei=E.astype(np.int64)
    assert not ((Ei.T@G@Ei)%2).any()
    assert all((int(Ei[:,j]@G@Ei[:,j])//2)%2==0 for j in range(12))
    idx=next(i for i in range(24) if int(G[i,i])==4)
    type4=orbit_bits([a,b],np.eye(24,dtype=np.uint8)[:,idx])
    assert len(type4)==98280
    eclasses=all_span_ints(E)[1:]
    type4_count=sum(x in type4 for x in eclasses);assert type4_count==0

    # Stored V2 and transverse pairing.
    M8=np.array(load_flat(ROOT/'analysis/_co0_M8.txt')[0],dtype=np.uint8)&1
    Nmat=(I-M8)&1;V2=base.rref_cols(base.mm(Nmat,Nmat));assert V2.shape==(24,12)
    inter=24-base.rank2(np.column_stack([E,V2]));assert inter==0
    P=(Ei.T@G@V2.astype(np.int64))%2;assert base.rank2(P)==12

    # Induced F2 actions on E.
    S=solve_coords(E,base.mm(els['a2'],E));G1=solve_coords(E,base.mm(els['g1'],E));G2=solve_coords(E,base.mm(els['g2'],E))
    I12=np.eye(12,dtype=np.uint8)
    assert base.order(S)==3 and not ((S@S+S+I12)&1).any()
    assert np.array_equal((S@G1)&1,(G1@S)&1) and np.array_equal((S@G2)&1,(G2@S)&1)
    assert base.order(G1)==13 and base.order(G2)==13 and base.order((G1@G2)&1)==15
    phi=np.zeros((12,12),dtype=np.uint8)
    for k in range(13):phi^=base.pw(G1,k)
    assert not phi.any() and base.rank2((G1-I12)&1)==12

    # Six F4 basis vectors: choose v_i so {v_i,Sv_i} is an F2 basis.
    pairvec=[];C=np.zeros((12,0),dtype=np.uint8);r=0
    for j in range(12):
        v=np.eye(12,dtype=np.uint8)[:,j];sv=(S@v)&1
        T=np.column_stack([C,v,sv]);rr=base.rank2(T)
        if rr==r+2:pairvec.append(v.copy());C=T;r=rr
        if r==12:break
    assert len(pairvec)==6 and base.rank2(C)==12
    def to_f4(M):
        out=np.zeros((6,6),dtype=np.uint8)
        for j,v in enumerate(pairvec):
            y=(M@v)&1;c=solve_coords(C,y[:,None])[:,0]
            for i in range(6):out[i,j]=int(c[2*i])+2*int(c[2*i+1])
        return out
    G1f=to_f4(G1);G2f=to_f4(G2);Sf=to_f4(S)
    assert np.array_equal(Sf,2*np.eye(6,dtype=np.uint8))

    # Exact degree-6 factor of Phi13 over F4.
    pwrs=[np.eye(6,dtype=np.uint8)]
    for _ in range(6):pwrs.append(f4_mm(pwrs[-1],G1f))
    coeff,rr=f4_solve(np.column_stack([X.reshape(-1) for X in pwrs[:6]]),pwrs[6].reshape(-1));assert rr==6
    poly=[int(x) for x in coeff]+[1]
    assert poly==[1,3,0,2,0,3,1]
    bar=[f4_pow(x,2) if x else 0 for x in poly]
    assert f4_poly_mul(poly,bar)==[1]*13

    # Pairing-dual F4 scalar on stored V2.
    Pinv=inv2n(P);Sinv=inv2n(S)
    Sdual=(Pinv@Sinv.T@P)&1
    assert base.order(Sdual)==3 and not ((Sdual@Sdual+Sdual+I12)&1).any()
    assert np.array_equal((S.T@P@Sdual)&1,P)

    out={
      'schema':'w33.pass10453_10476.explicit_a4g24_coordinate_closure.v1','status':'PASS','passes':'10453-10476',
      'wilson_word_checks':checks,
      'explicit_orbit7_generator':{
        'definition':'E=Fix(a1)=Fix(V4)','dimension':12,'totally_singular':True,'type4_count':0,
        'basis_bitstrings':[''.join(str(int(x)) for x in E[:,j]) for j in range(12)]},
      'relation_to_stored_V2':{
        'stored_V2_dimension':12,'intersection_dimension':inter,'sum_dimension':24,
        'pairing_rank':base.rank2(P),'interpretation':'E and stored V2 are complementary maximal totally singular orbit-7 generators; their Leech bilinear pairing is perfect'},
      'explicit_F4_structure_on_E':{
        'scalar':'a2 restricted to E','scalar_order':3,'minimal_polynomial':'x^2+x+1',
        'six_F4_basis_ambient_bitstrings':[''.join(str(int(x)) for x in (E@v)&1) for v in pairvec],
        'g1_F4_matrix_encoding_0_1_w_1plusw':G1f.tolist(),'g2_F4_matrix_encoding_0_1_w_1plusw':G2f.tolist(),
        'g1_order':13,'g2_order':13,'g1g2_order':15,
        'g1_minpoly_low_to_high_F4':poly,'frobenius_conjugate_factor':bar,
        'factor_identity':'p(x)*pbar(x)=Phi_13(x)=1+x+...+x^12'},
      'stored_V2_dual_scalar':{
        'construction':'S_V=P^-1 S_E^-T P from the perfect E--V2 pairing','order':3,'minimal_polynomial':'x^2+x+1',
        'matrix_12x12_in_stored_V2_basis':Sdual.tolist(),
        'pairing_identity':'S_E^T P S_V = P','co1_membership':'NOT CLAIMED'},
      'theorem':('Wilson\'s explicit A4 x G2(4) subgroup in the actual stored Co1 module fixes a concrete good generator E=Fix(V4). E is 12-dimensional, totally singular and contains zero Leech type-4 classes. The A4 order-3 generator acts on E as the scalar w of F4, and the commuting G2(4) generators become explicit 6x6 F4 matrices. The order-13 generator has irreducible degree-6 factor p=1+(1+w)x+w x^3+(1+w)x^5+x^6 (encoding [1,3,0,2,0,3,1]); its Frobenius conjugate multiplies with p to Phi13. E is complementary to the stored canonical V2 with perfect Leech pairing, which canonically induces an explicit dual F4 scalar on stored V2.'),
      'boundary':('All matrix, singularity and type-4 statements are exact repo computations. E and stored V2 are in the same published orbit-7 class, but an explicit Co1 conjugating word E->V2 is not yet constructed. The pairing-dual scalar on stored V2 is an exact orthogonal construction; membership in Co1 is deliberately not asserted.')
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print('RESULT_JSON='+json.dumps(out,sort_keys=True))
    return 0
if __name__=='__main__':raise SystemExit(main())
