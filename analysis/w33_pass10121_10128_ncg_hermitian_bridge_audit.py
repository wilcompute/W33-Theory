#!/usr/bin/env python3
"""Pass10121-10128: audit the proposed NCG identification h = J*chi.

The parallel packet proposed that h=K R^T-iK is automatically Hermitian for
arbitrary invertible K and that, with chi=iR, it is the finite-field shadow of
a Connes real structure/chirality product.  Both statements are too strong.

1. Hermitianization requires compatibility: K alternating and R K-symplectic.
   The proposed rank-2 test K=I, R=J is a direct counterexample: the real part
   R^T is skew and the imaginary part -I is symmetric, so H^dagger=-H rather
   than H.
2. In the actual F9 interpretation, multiplication by i IS the operator R.
   Therefore the proposed chi=iR is R^2=-I, a scalar grading, not a nontrivial
   chirality.
3. K is a bilinear form V->V*, while a spectral-triple J is an antilinear
   isometry H->H.  The types do not match.

There is, however, a precise finite-field KO-dimension-6 SIGN SKELETON.  On
H=V+V with V=F9^n (represented over F3), let

  gamma(x,y)=(x,-y),
  J(x,y)=(conj(y),conj(x)),
  D(x,y)=(y,x).

Then J^2=+1, JD=DJ, J gamma=-gamma J and gamma D=-D gamma.  These are the
KO6 sign relations, but they do not by themselves define a Connes spectral
triple: an algebra representation, order-zero/order-one conditions and the
spectral-triple analytic axioms remain to be supplied.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10121_10128_NCG_HERMITIAN_BRIDGE_AUDIT.json'
P=3

def eq(A,B): return np.array_equal(np.array(A,dtype=np.int64)%P,np.array(B,dtype=np.int64)%P)
def hermitian_coeffs(A,B):
    # H=A+iB over F9, conjugation i->-i: H^dagger=H iff A^T=A and B^T=-B.
    return eq(A.T,A) and eq(B.T,-B)

def main():
    I2=np.eye(2,dtype=np.int64)%P
    J2=np.array([[0,1],[2,0]],dtype=np.int64)%P
    assert eq(J2@J2,-I2)

    # Parallel packet's rank-2 choice K=I.
    Kbad=I2;R=J2
    Abad=Kbad@R.T%P; Bbad=(-Kbad)%P
    assert not hermitian_coeffs(Abad,Bbad)
    assert eq(Abad.T,-Abad) and eq(Bbad.T,Bbad)

    # Compatible symplectic-form choice restores the correct coefficient symmetry.
    Kgood=J2
    assert eq(Kgood.T,-Kgood)
    assert eq(R.T@Kgood@R,Kgood)
    Agood=Kgood@R.T%P; Bgood=(-Kgood)%P
    assert hermitian_coeffs(Agood,Bgood)

    # KO6 sign skeleton on doubled F9^6, represented over F3 as 24 coordinates.
    n=6; I=np.eye(2*n,dtype=np.int64)%P
    # conjugation on one F9^n block: (a,b)->(a,-b)
    C=np.block([[np.eye(n,dtype=np.int64),np.zeros((n,n),dtype=np.int64)],
                [np.zeros((n,n),dtype=np.int64),-np.eye(n,dtype=np.int64)]])%P
    Z=np.zeros_like(I)
    gamma=np.block([[I,Z],[Z,-I]])%P
    Jop=np.block([[Z,C],[C,Z]])%P
    Dop=np.block([[Z,I],[I,Z]])%P
    Ibig=np.eye(4*n,dtype=np.int64)%P
    assert eq(Jop@Jop,Ibig)
    assert eq(Jop@Dop,Dop@Jop)
    assert eq(Jop@gamma,-gamma@Jop)
    assert eq(gamma@gamma,Ibig)
    assert eq(gamma@Dop,-Dop@gamma)

    out={
      'schema':'w33.pass10121_10128.ncg_hermitian_bridge_audit.v1','status':'PASS','passes':'10121-10128',
      'parallel_claim_audit':{
        'arbitrary_invertible_K_gives_Hermitian':False,
        'counterexample':'K=I2, R=[[0,1],[-1,0]] over F3 gives real part R^T skew and imaginary part -I symmetric',
        'compatible_condition':'K alternating nondegenerate and R K-symplectic; then the coefficient symmetry required for h=K R^T-iK is restored',
        'chi_equals_iR_problem':'In the actual F9 scalar structure, i acts as R, so chi=iR=R^2=-I is scalar/trivial as a grading.',
        'type_mismatch':'K is a bilinear form V->V*, whereas Connes J is an antilinear isometry H->H.'},
      'repaired_KO6_sign_skeleton':{
        'space':'H=V+V, V=F9^6 represented over F3',
        'gamma':'(x,y)->(x,-y)','J':'(x,y)->(conj(y),conj(x))','D':'(x,y)->(y,x)',
        'relations':{'J2':'+I','JD':'DJ','Jgamma':'-gammaJ','gamma2':'+I','gammaD':'-Dgamma'},
        'KO_signs':'(epsilon,epsilon_prime,epsilon_double_prime)=(+1,+1,-1), the standard KO-dimension-6 sign pattern'},
      'theorem':'The proposed identity h=J chi is not established and its supplied rank-2 proof is false. What survives is an exact analogy at the level of KO6 commutation signs: a doubled F9 module carries explicit J, gamma and D operators with J^2=1, JD=DJ, Jgamma=-gammaJ and gammaD=-Dgamma.',
      'boundary':'This is not a Connes spectral triple theorem and makes no Higgs/Hecke identification. A faithful algebra action, antiunitary/inner-product structure over C or an appropriate local analogue, order-zero/order-one axioms, and a Dirac/spectral-action construction would all still be required.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','parallel_rank2_Hermitian':False,'KO6_sign_skeleton':True}))
    return 0
if __name__=='__main__': raise SystemExit(main())
