#!/usr/bin/env python3
"""Pass10009-10016: lift the F9^6 glue from associated graded to the full mod-3 residue ring.

Let K=Q3(i), O_K=Z3[i], and L=K(zeta_9).  The extension L/K is totally
ramified of degree 6 with t=zeta_9-1 a uniformizer.  Since

 Phi_9(1+t) = t^6 + 6t^5 + 15t^4 + 21t^3 + 18t^2 + 9t + 3,

we have modulo 3

 O_L/3 O_L ~= F9[t]/(t^6).

Thus the six F9 layers found earlier are not merely an associated-graded count:
the entire residue ring is the length-six truncated F9 algebra.

This pass also constructs an explicit regular order-9 unitary action on the
six-dimensional F9 residue module.  In a power-basis convention let N be the
regular nilpotent Jordan shift and U=I+N, representing multiplication by
zeta_9=1+t (up to reversing the power basis).  Over characteristic 3,
U^9=I but U^3!=I.  The displayed skew matrix A gives a Hermitian Gram H=iA;
U^dagger H U=H and H is nondegenerate.

This closes the complete reduction modulo 3.  It is NOT yet an explicit
integral self-dual O_L lattice over Z3.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10009_10016_F9_RESIDUE_RING_UNITARY_LIFT.json'
P=3

A=np.array([
 [0,0,0,0,0,1],
 [0,0,0,0,2,2],
 [0,0,0,1,2,1],
 [0,0,2,0,0,0],
 [0,1,1,0,0,0],
 [2,1,2,0,0,0]],dtype=np.int64)%P


def rankp(M):
    M=np.array(M,dtype=np.int64)%P;r=0
    for c in range(M.shape[1]):
        q=next((i for i in range(r,M.shape[0]) if M[i,c]),None)
        if q is None:continue
        if q!=r:M[[r,q]]=M[[q,r]]
        M[r]=(M[r]*pow(int(M[r,c]),-1,P))%P
        for i in range(M.shape[0]):
            if i!=r and M[i,c]:M[i]=(M[i]-M[i,c]*M[r])%P
        r+=1
    return r

def main():
    # Coefficients low-to-high of Phi_9(1+t).
    coeff=[3,9,18,21,15,6,1]
    assert [x%3 for x in coeff]==[0,0,0,0,0,0,1]

    N=np.zeros((6,6),dtype=np.int64)
    for j in range(5):N[j,j+1]=1
    I=np.eye(6,dtype=np.int64)%P
    U=(I+N)%P
    assert not np.any(np.linalg.matrix_power(N,6)%P)
    assert np.any(np.linalg.matrix_power(N,5)%P)
    assert np.array_equal(np.linalg.matrix_power(U,9)%P,I)
    assert not np.array_equal(np.linalg.matrix_power(U,3)%P,I)

    # H=iA.  Since conjugation sends i -> -i, Hermitian symmetry of iA is A^T=-A.
    assert np.array_equal(A.T%P,(-A)%P)
    assert rankp(A)==6
    # U is defined over F3, so dagger is ordinary transpose; i factors out.
    assert np.array_equal(U.T@A@U%P,A)

    out={
      'schema':'w33.pass10009_10016.f9_residue_ring_unitary_lift.v1','status':'PASS','passes':'10009-10016',
      'local_field':{'K':'Q3(i), unramified quadratic over Q3','L':'K(zeta_9)','relative_ramification_index':6,'residue_field':'F9','uniformizer':'t=zeta_9-1'},
      'exact_residue_ring':{
        'Phi9_1_plus_t_coefficients_low_to_high':coeff,
        'mod3_relation':'t^6=0',
        'isomorphism':'O_L / 3 O_L ~= F9[t]/(t^6)',
        'F9_dimension':6,'F3_dimension':12},
      'regular_unitary_model':{
        'N':'6x6 regular nilpotent Jordan shift','N_nilpotency_index':6,
        'U':'I+N, representing multiplication by 1+t up to power-basis reversal',
        'U_order':9,
        'Hermitian_Gram':'H=i*A over F9, with A over F3',
        'A':A.tolist(),
        'A_rank':6,
        'Hermitian_reason':'A^T=-A and conjugation(i)=-i, hence (iA)^dagger=iA',
        'unitary_identity':'U^T A U = A, equivalently U^dagger H U=H'},
      'theorem':('The glue F9^6 phase space admits the full mod-3 cyclotomic residue-ring structure O_{Q3(i,zeta9)}/3 ~= F9[t]/(t^6), together with an explicit regular order-9 nondegenerate unitary action U=1+t. This upgrades the previous six-layer associated-graded match to an actual length-six truncated residue algebra.'),
      'boundary':'This is an exact finite-level/local reduction. It does not yet construct an integral self-dual O_L lattice or prove that the Niemeier lattice itself is an O_L lattice.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','ring':'F9[t]/(t^6)','U_order':9,'hermitian_rank':6}))
    return 0
if __name__=='__main__':raise SystemExit(main())
