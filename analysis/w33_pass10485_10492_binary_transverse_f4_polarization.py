#!/usr/bin/env python3
"""Pass10485-10492: binary transverse-pair/F4-Hermitian polarization of Lambda/2Lambda.

Pass10453-10476 gave two complementary maximal singular 12-spaces in the Leech
mod-2 quadratic space:
  E = Fix(V4) for Wilson's explicit A4 x G2(4),
  V = stored canonical V2 = im((I-M8)^2),
with perfect Leech bilinear pairing.

Choose the V basis dual to E.  In the resulting basis the quadratic form is
q(x,y)=x.y and the polar Gram is [[0,I],[I,0]].  Therefore coordinate swap is
an explicit orthogonal involution exchanging E and V.

The order-3 F4 scalar A on E has pairing-dual A^{-T} on V.  Their block diagonal
operator is fixed-point-free, orthogonal, order 3, and gives the whole 24-bit
space the structure of a 12-dimensional F4 Hermitian space.  E and V are
transverse maximal Hermitian-isotropic F4^6 halves.

At the abstract orthogonal-group level, the ordered transverse-pair stabilizer
is GL(12,2); imposing the scalar reduces it to GL(6,4).  Adding the exchange
normalizer gives GL(6,4):2, with the involution acting by contragredience.
No claim is made that the exchange itself is a Co1 word.
"""
from __future__ import annotations
import json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass10453_10476_explicit_a4g24_v2_coordinates as base
from w33_pass7333_leech_d4_form import load_flat,invariant_gram

OUT=ROOT/'data/PART_W33_PASS10485_10492_BINARY_TRANSVERSE_F4_POLARIZATION.json'

def inv2(A):
    A=np.array(A,dtype=np.uint8)&1;n=A.shape[0];M=np.concatenate([A,np.eye(n,dtype=np.uint8)],1)
    for c in range(n):
      q=next(i for i in range(c,n) if M[i,c]);M[[c,q]]=M[[q,c]]
      for i in range(n):
        if i!=c and M[i,c]:M[i]^=M[c]
    return M[:,n:]
def coords(B,Y):
    B=np.array(B,dtype=np.uint8)&1;Y=np.array(Y,dtype=np.uint8)&1
    X=np.zeros((B.shape[1],Y.shape[1]),dtype=np.uint8)
    for j in range(Y.shape[1]):
      A=np.concatenate([B.copy(),Y[:,j:j+1]],1);r=0;p=[]
      for c in range(B.shape[1]):
        q=next((i for i in range(r,B.shape[0]) if A[i,c]),None)
        if q is None:continue
        A[[r,q]]=A[[q,r]]
        for i in range(B.shape[0]):
          if i!=r and A[i,c]:A[i]^=A[r]
        p.append(c);r+=1
      assert r==B.shape[1]
      for i,c in enumerate(p):X[c,j]=A[i,-1]
    return X
def gl_order(n,q):
    z=1
    for i in range(n):z*=q**n-q**i
    return z

def main():
    a,b=base.load_pair();checks,e=base.build(a,b,'x^-1y^-1xy');I24=base.eye()
    assert checks['a2_order']==3 and checks['A4_G2_commute']
    E=base.kernel((e['a1']-I24)&1);assert E.shape==(24,12)
    M8=np.array(load_flat(ROOT/'analysis/_co0_M8.txt')[0],dtype=np.uint8)&1
    N=(I24-M8)&1;V=base.rref_cols(base.mm(N,N));assert V.shape==(24,12)
    assert base.rank2(np.column_stack([E,V]))==24

    G,dim=invariant_gram(load_flat(ROOT/'analysis/_co0_G.txt'));assert dim==1 and G is not None
    if G[0,0]<0:G=-G
    P=(E.astype(np.int64).T@G@V.astype(np.int64))%2;assert base.rank2(P)==12
    Pinv=inv2(P)
    Vd=(V@Pinv)&1
    assert np.array_equal((E.astype(np.int64).T@G@Vd.astype(np.int64))%2,np.eye(12,dtype=np.int64))
    B=np.column_stack([E,Vd])&1;Binv=inv2(B);assert base.rank2(B)==24
    J=np.block([[np.zeros((12,12),dtype=np.uint8),np.eye(12,dtype=np.uint8)],[np.eye(12,dtype=np.uint8),np.zeros((12,12),dtype=np.uint8)]])
    X=(B@J@Binv)&1
    assert np.array_equal((X@X)&1,I24)
    assert base.same_space(base.mm(X,E),V) and base.same_space(base.mm(X,V),E)

    # q on a 0/1 lift; q-preservation follows from testing a basis because the
    # difference of two quadratic forms with the same polar form is linear.
    def q(v):
      z=np.array(v,dtype=np.int64);return (int(z@G@z)//2)&1
    G2=G%2
    assert np.array_equal((X.T@G2@X)%2,G2)
    assert all(q(X[:,j])==q(np.eye(24,dtype=np.uint8)[:,j]) for j in range(24))

    # Scalar on E and pairing-dual scalar on the original V basis.
    A=coords(E,base.mm(e['a2'],E));I12=np.eye(12,dtype=np.uint8)
    assert base.order(A)==3 and not ((A@A+A+I12)&1).any()
    Adual=(Pinv@inv2(A).T@P)&1
    assert base.order(Adual)==3 and not ((Adual@Adual+Adual+I12)&1).any()
    # In dual Vd coordinates the second block is A^{-T}.
    Ad_dualbasis=(P@Adual@Pinv)&1;assert np.array_equal(Ad_dualbasis,inv2(A).T)
    Tcoord=np.block([[A,np.zeros((12,12),dtype=np.uint8)],[np.zeros((12,12),dtype=np.uint8),Ad_dualbasis]])
    T=(B@Tcoord@Binv)&1
    assert base.order(T)==3 and base.rank2((T-I24)&1)==24
    assert np.array_equal((T.T@G2@T)%2,G2)
    assert all(q(T[:,j])==q(np.eye(24,dtype=np.uint8)[:,j]) for j in range(24))
    assert np.array_equal((X@T@X)&1,inv2(T).T)

    gl64=gl_order(6,4);gl122=gl_order(12,2)
    out={
      'schema':'w33.pass10485_10492.binary_transverse_f4_polarization.v1','status':'PASS','passes':'10485-10492',
      'ambient':{'space':'Lambda/2Lambda','F2_dimension':24,'quadratic_type':'plus/hyperbolic from transverse maximal singular pair'},
      'halves':{'E_dimension_F2':12,'V2_dimension_F2':12,'intersection_dimension':0,'pairing_rank':12,'F4_dimension_each':6},
      'exchange':{'order':2,'definition':'in dual bases (e_i,v_i), X(e_i)=v_i and X(v_i)=e_i','quadratic_isometry':True,'exchanges_E_V2':True,'Co1_membership':'NOT CLAIMED'},
      'global_F4_scalar':{'order':3,'fixed_point_free':True,'minimal_polynomial':'x^2+x+1','quadratic_isometry':True,'ambient_F4_dimension':12,'relation_to_exchange':'X T X = T^{-T}'},
      'Hermitian_interpretation':'By the unconditional order-3 refinement theorem of Pass10377-10388, the Leech mod-2 quadratic form is the isotropy shadow of an F4-Hermitian form; E and V2 are transverse maximal Hermitian-isotropic F4^6 halves.',
      'abstract_stabilizers':{'ordered_transverse_pair':'GL(12,2)','order_GL12_2':gl122,'ordered_pair_plus_F4_scalar':'GL(6,4)','order_GL6_4':gl64,'unordered_pair_plus_scalar_normalizer':'GL(6,4):2','order':2*gl64},
      'theorem':'The explicit Wilson orbit-7 generator E and stored canonical V2 form a hyperbolic transverse polarization of Lambda/2Lambda. Their perfect pairing gives an explicit orthogonal exchange involution, while the Wilson order-3 scalar and its pairing-dual combine to a fixed-point-free global F4 scalar. Hence the binary Leech carrier is an F4-Hermitian 12-space with two transverse maximal F4^6 isotropic halves; at the abstract orthogonal level their scalar-preserving ordered-pair stabilizer is GL(6,4).',
      'boundary':'Exact mod-2 orthogonal/Hermitian linear algebra. The constructed exchange and pairing-dual scalar are not asserted to be specific Co1 words.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','polarization':'F4^6 + F4^6','exchange_order':2,'scalar_order':3,'GL6_4':gl64}))
if __name__=='__main__':main()
