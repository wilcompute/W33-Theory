#!/usr/bin/env python3
"""Passes 7049--7064: exact E6 27 x 78 split-Casimir / Vogel projector test.

This is an operator-level test of the 2026 Vogel literature against a native repo
carrier.  It does not use W33 cardinality matches.

Construction:
  1. build the E6 minuscule 27 from the Chevalley generators;
  2. close those generators to the full 78-dimensional E6 Lie algebra inside
     Mat_27(Z);
  3. use G_ab = Tr_27(X_a X_b) and its exact trace-dual basis;
  4. build the split Casimir Omega on 27 tensor 78, with 18*Omega integral;
  5. verify the characteristic polynomial and all three spectral projectors
     by exact sparse integer matrix identities.

For Isaev's 2026 normalization, C_hat=Omega/4.  The exact spectrum is
  (1/24)^1728 + (-1/6)^351 + (-1/2)^27,
which is precisely the E6 n=1 characteristic identity for 27 tensor ad.

Primary literature target:
  A. P. Isaev, "Vogel universality and beyond", arXiv:2601.01612v2 (2026).

Boundary:
  this verifies an E6 split-Casimir theorem on the repo-native E6 27 carrier.
  It is not evidence that Vogel's conjectural universal Lie algebra exists, nor
  does it identify W33 itself with a Vogel object.
"""
from __future__ import annotations

from collections import deque
from fractions import Fraction
import json
from pathlib import Path

import numpy as np
import scipy.sparse as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7049_7064_VOGEL_E6_SPLIT_CASIMIR.json'
P=1000003

A=np.array([
 [2,-1,0,0,0,0],
 [-1,2,-1,0,0,0],
 [0,-1,2,-1,-1,0],
 [0,0,-1,2,0,0],
 [0,0,-1,0,2,-1],
 [0,0,0,0,-1,2],
],dtype=np.int64)


def refl(mu,i):
    return tuple(int(mu[j]-mu[i]*A[j,i]) for j in range(6))


def orbit(start):
    seen={start}; q=deque([start])
    while q:
        mu=q.popleft()
        for i in range(6):
            nu=refl(mu,i)
            if nu not in seen:
                seen.add(nu); q.append(nu)
    return sorted(seen)


def comm(x,y): return x@y-y@x


class ModBasis:
    """Independence oracle over a large prime; original matrices stay integral."""
    def __init__(self,p=P): self.p=p; self.piv={}
    def add(self,arr):
        v=np.asarray(arr,dtype=np.int64).reshape(-1)%self.p
        for piv in sorted(self.piv):
            if v[piv]: v=(v-v[piv]*self.piv[piv])%self.p
        nz=np.flatnonzero(v)
        if not len(nz): return False
        piv=int(nz[0]); inv=pow(int(v[piv]),-1,self.p)
        self.piv[piv]=(v*inv)%self.p
        return True


def e6_27_chevalley():
    weights=orbit((1,0,0,0,0,0)); assert len(weights)==27
    wi={w:i for i,w in enumerate(weights)}
    E=np.zeros((6,27,27),dtype=np.int64)
    F=np.zeros_like(E); H=np.zeros_like(E)
    for a,mu in enumerate(weights):
        for i in range(6):
            H[i,a,a]=mu[i]
            if mu[i]==1:
                nu=tuple(int(mu[j]-A[j,i]) for j in range(6))
                b=wi[nu]; F[i,b,a]=1; E[i,a,b]=1
    for i in range(6):
        for j in range(6):
            assert np.array_equal(comm(H[i],E[j]),A[i,j]*E[j])
            assert np.array_equal(comm(H[i],F[j]),-A[i,j]*F[j])
            tgt=H[i] if i==j else np.zeros((27,27),dtype=np.int64)
            assert np.array_equal(comm(E[i],F[j]),tgt)
    return weights,E,F,H


def close_e6(E,F,H):
    mb=ModBasis(); basis=[]
    for X in list(E)+list(F)+list(H):
        if mb.add(X): basis.append(X.copy())
    i=0
    while i<len(basis):
        X=basis[i]
        for j in range(len(basis)):
            C=comm(X,basis[j])
            if np.any(C) and mb.add(C): basis.append(C.copy())
        i+=1
        assert len(basis)<=78, f"closure exceeded E6 dimension: {len(basis)}"
    assert len(basis)==78
    return basis


def structure_constants(basis):
    B=np.stack([X.reshape(-1) for X in basis],axis=1).astype(float)
    assert np.linalg.matrix_rank(B)==78
    pinv=np.linalg.pinv(B)
    ad=[]
    for X in basis:
        M=np.zeros((78,78),dtype=np.int64)
        for c,Y in enumerate(basis):
            z=comm(X,Y).reshape(-1)
            coeff=np.rint(pinv@z.astype(float)).astype(np.int64)
            assert np.array_equal(B.astype(np.int64)@coeff,z)
            M[:,c]=coeff
        ad.append(M)
    return np.stack(ad)


def main():
    weights,E,F,H=e6_27_chevalley()
    basis=close_e6(E,F,H)
    ad=structure_constants(basis)

    G=np.array([[int(np.trace(X@Y)) for Y in basis] for X in basis],dtype=np.int64)
    assert np.linalg.matrix_rank(G.astype(float))==78
    # For this integral basis 18 G^{-1} is integral; verify it as an exact inverse.
    Ginv18=np.rint(18*np.linalg.inv(G.astype(float))).astype(np.int64)
    assert np.array_equal(G@Ginv18,18*np.eye(78,dtype=np.int64))
    assert np.array_equal(Ginv18@G,18*np.eye(78,dtype=np.int64))

    # ad of the trace-dual basis, scaled by 18.
    addual18=np.einsum('ab,bij->aij',Ginv18,ad).astype(np.int64)
    N=27*78
    O18=sp.csr_matrix((N,N),dtype=np.int64)
    for a,X in enumerate(basis):
        O18 = O18 + sp.kron(sp.csr_matrix(X),sp.csr_matrix(addual18[a]),format='csr')
    # O18 = 18*Omega.  The exact Vogel-normalized operator is C_hat=O18/72.
    I=sp.identity(N,dtype=np.int64,format='csr')

    # Exact characteristic identity.  Omega eigenvalues are 1/6,-2/3,-2.
    poly=(O18-3*I)@(O18+12*I)@(O18+36*I)
    assert poly.nnz==0

    # Exact spectral projectors, represented by integer numerator / denominator.
    # 1728 eigenspace, Omega=1/6:
    P1728_num=(O18+12*I)@(O18+36*I); P1728_den=585
    # 351 eigenspace, Omega=-2/3:
    P351_num=-(O18-3*I)@(O18+36*I); P351_den=360
    # 27 eigenspace, Omega=-2:
    P27_num=(O18-3*I)@(O18+12*I); P27_den=936
    projectors=[(P1728_num,P1728_den,1728),(P351_num,P351_den,351),(P27_num,P27_den,27)]
    for Num,den,rk in projectors:
        assert (Num@Num-den*Num).nnz==0
        assert int(Num.diagonal().sum())==den*rk
    lcm=4680
    assert ((lcm//P1728_den)*P1728_num+(lcm//P351_den)*P351_num+(lcm//P27_den)*P27_num-lcm*I).nnz==0
    assert (P1728_num@P351_num).nnz==0
    assert (P1728_num@P27_num).nnz==0
    assert (P351_num@P27_num).nnz==0

    # Trace moments of C_hat=O18/72, checked directly on the integer operator.
    tr1=int(O18.diagonal().sum())
    O2=O18@O18; tr2=int(O2.diagonal().sum())
    tr3=int((O2@O18).diagonal().sum())
    moments=[Fraction(tr1,72),Fraction(tr2,72**2),Fraction(tr3,72**3)]
    assert moments==[Fraction(0),Fraction(39,2),Fraction(-39,8)]
    assert moments[2]==-Fraction(1,4)*moments[1]

    report={
      "passes":list(range(7049,7065)),
      "literature_target":"A.P. Isaev, Vogel universality and beyond, arXiv:2601.01612v2 (2026)",
      "repo_native_construction":{
        "E6_minuscule_dimension":27,
        "E6_lie_closure_dimension":78,
        "tensor_dimension":2106,
        "invariant_form":"G_ab=Tr_27(X_a X_b)",
        "exact_dual_denominator":18,
        "integral_split_casimir":"O18=18*Omega",
        "vogel_normalization":"C_hat=Omega/4=O18/72"
      },
      "exact_characteristic_identity":"(O18-3I)(O18+12I)(O18+36I)=0",
      "vogel_normalized_spectrum":{
        "1/24":1728,
        "-1/6":351,
        "-1/2":27
      },
      "decomposition":"27 tensor 78 = 1728 + 351 + 27",
      "projectors":{
        "1728":"(O18+12I)(O18+36I)/585",
        "351":"-(O18-3I)(O18+36I)/360",
        "27":"(O18-3I)(O18+12I)/936"
      },
      "projector_checks":{"idempotent":True,"pairwise_orthogonal":True,"sum_to_identity":True,"ranks":[1728,351,27]},
      "trace_moments":{"Tr_C":"0","Tr_C2":"39/2","Tr_C3":"-39/8","Tr_C3_eq_minus_quarter_Tr_C2":True},
      "status":"EXACT_OPERATOR_LEVEL_VOGEL_E6_MATCH",
      "boundary":"This verifies the E6 split-Casimir/projector identity on a repo-native E6 carrier. It does not prove Vogel's conjectural universal Lie algebra exists and does not identify W33 itself with a Vogel object."
    }
    OUT.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))
    return report

if __name__=='__main__':
    main()
