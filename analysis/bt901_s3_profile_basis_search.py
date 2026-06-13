#!/usr/bin/env python3
"""BT901 - S3 profile-basis search in the 9*2 layer.

BT895 located the representation home C[27]=6*1+3*1'+9*2.
BT894-BT898 located the numerical angle freedom in the q^2=9 within-grade
profile layer.  BT901 builds the clean commutant model:

    V_profile = C^9 \otimes Std(S3).

The physical profile matrices act on the multiplicity factor C^9 and hence
commute with the S3 flavor action.  This is the exact way to let Cabibbo/PMNS
profiles move without damaging the shifted-reflection skeleton.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import numpy as np

q=3; Phi3=13
N=9

# Real orthogonal standard representation of S3: rotation by 120 degrees and reflection.
rot=np.array([[-0.5, -math.sqrt(3)/2],[math.sqrt(3)/2, -0.5]])
ref=np.array([[1.0,0.0],[0.0,-1.0]])
I2=np.eye(2); I9=np.eye(N)

def embed_plane_rotation(n:int,i:int,j:int,c:float,s:float)->np.ndarray:
    r=np.eye(n)
    r[i,i]=c; r[i,j]=s; r[j,i]=-s; r[j,j]=c
    return r

def frob(a:np.ndarray)->float:
    return float(np.linalg.norm(a,"fro"))

def main()->None:
    c=Phi3/math.sqrt(Phi3*Phi3+q*q)
    s=q/math.sqrt(Phi3*Phi3+q*q)
    U=embed_plane_rotation(N,0,1,c,s)
    # Up/down profile Gram matrices in the 9-dimensional multiplicity space.
    Du=np.diag(np.arange(1,N+1,dtype=float))
    Dd=U @ Du @ U.T
    comm=Du @ Dd - Dd @ Du
    assert frob(comm)>0

    # Lift to the full 9 copies of the S3 standard doublet.
    A=np.kron(Du,I2)
    B=np.kron(Dd,I2)
    R=np.kron(I9,rot)
    C=np.kron(I9,ref)
    assert frob(A@R-R@A)<1e-10
    assert frob(B@R-R@B)<1e-10
    assert frob(A@C-C@A)<1e-10
    assert frob(B@C-C@B)<1e-10

    V=np.kron(U,I2)
    assert abs(np.linalg.det(U)-1.0)<1e-12
    assert frob(V.T@V-np.eye(18))<1e-10

    result={
        "theorem":"BT901 S3 profile-basis search",
        "representation_home":"V_profile = C^9 tensor Std(S3), the 9*2 sector of C[27]",
        "multiplicity_dimension":9,
        "standard_doublet_dimension":2,
        "full_profile_sector_dimension":18,
        "profile_basis_labels":[f"m{i}" for i in range(N)],
        "cabibbo_plane":{"multiplicity_indices":[0,1],"cos":"Phi3/sqrt(Phi3^2+q^2)=13/sqrt(178)","sin":"q/sqrt(Phi3^2+q^2)=3/sqrt(178)","numeric_sin":s,"numeric_cos":c},
        "commutator_frobenius_norm":frob(comm),
        "s3_equivariance_errors":{"up_rotation":frob(A@R-R@A),"down_rotation":frob(B@R-R@B),"up_reflection":frob(A@C-C@A),"down_reflection":frob(B@C-C@B)},
        "profile_principle":"Allowed numerical profiles are 9x9 multiplicity-space operators tensored with I_2 on the S3 standard doublet. This preserves flavor equivariance while allowing noncommuting up/down Gram profiles.",
        "exact_conclusion":"The q^2=9 profile layer is not nine extra generations; it is the multiplicity space of the 9 copies of the S3 standard doublet. CKM/PMNS profile rotations act on that multiplicity space and commute with flavor S3.",
        "checks":{"T1_full_sector_dimension_18":True,"T2_cabibbo_plane_embedded_in_C9":True,"T3_profile_lifts_commute_with_S3":True,"T4_up_down_profiles_noncommute":True,"T5_CKM_rotation_is_unitary_on_multiplicity_space":True}}
    out=Path("data/PART_BT901_S3_PROFILE_BASIS_SEARCH_results.json"); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2))
    print("BT901 passed; commutator Frobenius norm",frob(comm),"wrote",out)
if __name__=="__main__": main()
