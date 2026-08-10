#!/usr/bin/env python3
"""Pass 4751 — exact S3 Fourier transform of the 45-point voltage connection.

The 3-sheet selected135 cover uses the 3-point permutation representation
1 + Std_2 of S3. We construct the 90x90 integer matrix-valued standard block
explicitly from the Pass4716 voltages and prove its polynomial

    X (X^2 - 36 I) = 0.

The integral sum-zero basis is not orthonormal, so this block need not be
symmetric in those coordinates; its spectrum is obtained with the general
matrix eigensolver and cross-checked against the exact polynomial and the full
135x135 symmetric lift. Together with the trivial 45x45 GQ block this gives the
full selected135 spectrum. The regular 6-sheet S3 closure then splits as
trivial + sign + two standard blocks, reproducing Pass4719 exactly.

This also tests the tempting idea that selected270's 1±sqrt(13) sector is the
same S3 Fourier mechanism. It is not: no Fourier block here has factor
x^2-2x-12. The radical belongs to the distinct multiplicity-two PSp(20)
router sector isolated in Pass4747.
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path
import numpy as np
from w33_pass4716_selected270_bundle_connection import build_bundle
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4751_S3_FOURIER_VOLTAGE.json'

def perm_matrix3(p):
    M=np.zeros((3,3),dtype=int)
    for i,j in enumerate(p):M[j,i]=1
    return M

def std_matrix(p):
    # Integral standard sum-zero basis b1=(1,-1,0), b2=(0,1,-1).
    B=np.array([[1,0],[-1,1],[0,-1]],dtype=int);Y=perm_matrix3(p)@B
    # Solve B C = Y using first and third coordinates: c1=Y0, c2=-Y2.
    C=np.vstack((Y[0,:],-Y[2,:])).astype(int)
    assert np.array_equal(B@C,Y)
    return C

def spectrum_counter_symmetric(A):
    z=np.linalg.eigvalsh(A.astype(float));return Counter(round(float(x),8) for x in z)
def spectrum_counter_general(A):
    z=np.linalg.eigvals(A.astype(float));
    assert max(abs(float(x.imag)) for x in z)<1e-7
    return Counter(round(float(x.real),8) for x in z)

def main():
    X=build_bundle();G=X['G45'];sig=X['sig'];n=45
    A=np.zeros((n,n),dtype=int);S=np.zeros((2*n,2*n),dtype=int);L=np.zeros((3*n,3*n),dtype=int)
    for u,v in G.edges():
        A[u,v]=A[v,u]=1
        P=perm_matrix3(sig[(u,v)]);L[3*u:3*u+3,3*v:3*v+3]=P;L[3*v:3*v+3,3*u:3*u+3]=P.T
        T=std_matrix(sig[(u,v)]);Ti=std_matrix(sig[(v,u)])
        S[2*u:2*u+2,2*v:2*v+2]=T;S[2*v:2*v+2,2*u:2*u+2]=Ti
    assert np.array_equal(L,L.T)
    # In the integral sum-zero basis, inverse group matrices are adjoint for the
    # Gram form B^T B, not necessarily ordinary transposes.
    B=np.array([[1,0],[-1,1],[0,-1]],dtype=int);Q=B.T@B
    Qbig=np.kron(np.eye(45,dtype=int),Q)
    assert np.array_equal(S.T@Qbig,Qbig@S)

    I45=np.eye(45,dtype=int);I90=np.eye(90,dtype=int)
    assert not np.any((A-12*I45)@(A-3*I45)@(A+3*I45))
    assert not np.any(S@(S@S-36*I90))
    base_spec=spectrum_counter_symmetric(A);std_spec=spectrum_counter_general(S);lift_spec=spectrum_counter_symmetric(L)
    assert base_spec==Counter({12.0:1,3.0:20,-3.0:24})
    assert std_spec==Counter({6.0:15,0.0:60,-6.0:15})
    assert lift_spec==base_spec+std_spec

    # Regular closure Fourier: trivial A, sign -A (Pass4719 parity gauge), two Std copies.
    regular=base_spec+Counter({-k:v for k,v in base_spec.items()})+Counter({k:2*v for k,v in std_spec.items()})
    expected=Counter({12.0:1,6.0:30,3.0:44,0.0:120,-3.0:44,-6.0:30,-12.0:1})
    assert regular==expected

    out={'pass':4751,
      'selected135_fourier':{'permutation_representation':'1 + Std_2','trivial_block_dimension':45,'standard_block_dimension':90,
        'integral_standard_basis_Gram':Q.tolist(),'standard_block_is_Gram_self_adjoint':True,
        'trivial_block_polynomial':'(x-12)(x-3)(x+3)','standard_block_polynomial':'x(x^2-36)',
        'trivial_spectrum':dict(base_spec),'standard_spectrum':dict(std_spec),'full_spectrum':dict(lift_spec)},
      'regular_S3_closure':{'decomposition':'trivial + sign + 2 Std_2','spectrum':dict(regular),'matches_Pass4719':True},
      'selected270_radical_test':{'factor_x2_minus_2x_minus_12_present_in_any_S3_fourier_block':False,
        'conclusion':'the 1±sqrt(13) cold-router sector is not the direct S3-cover Fourier block; Pass4747 locates it in the multiplicity-two PSp degree-20 constituent'},
      'theorem':'The S3 voltage connection has an exact 2x2 matrix Fourier block over each GQ edge. In the integral standard lattice basis its 90x90 operator is self-adjoint for the natural Gram form and satisfies X(X^2-36I)=0 exactly, explaining the selected135 and regular-closure spectra. The selected270 radical sector is a different representation-theoretic mechanism.',
      'boundary':'Exact finite voltage/Fourier theorem. The word Fourier refers to finite-group representation decomposition, not optical frequency.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
