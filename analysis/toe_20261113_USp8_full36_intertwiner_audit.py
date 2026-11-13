#!/usr/bin/env python3
"""Audits whether the currently committed 28x27 Cartan isometry already
intertwines the FULL 36-generator compact USp8 algebra.

Rebuild all 36 Hermitian-compatible, complex symplectic 8x8 Lie
generators in block form [[X,Y],[-Y*,X*]], with X†=-X,Y^T=Y.
Induce them on Λ²(C8) exactly from basis wedges, project repo's
36 skew cubic generators through existing 28x27 T, and perform
full-rank real least-squares. This is a quantitative falsifier:
Cartan isometry is not assumed to match root phases.
"""
from pathlib import Path
from itertools import combinations
import json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261113_e6_root_matching_projection_clock as R
OUT=ROOT/"data/toe_20261113_USp8_all36_intertwiner_residual_audit.json"

def defining_basis():
    eye=np.eye(4,dtype=complex)
    basis=[]
    for i in range(4):
        X=np.zeros((4,4),dtype=complex);X[i,i]=1j
        basis.append((X,np.zeros_like(X)))
    for i,j in combinations(range(4),2):
        X=np.zeros((4,4),dtype=complex)
        X[i,j]=1;X[j,i]=-1
        basis.append((X,np.zeros_like(X)))
        X=np.zeros((4,4),dtype=complex)
        X[i,j]=1j;X[j,i]=1j
        basis.append((X,np.zeros_like(X)))
    for i in range(4):
        Y=np.zeros((4,4),dtype=complex);Y[i,i]=1
        basis.append((np.zeros_like(Y),Y))
        Y=np.zeros((4,4),dtype=complex);Y[i,i]=1j
        basis.append((np.zeros_like(Y),Y))
    for i,j in combinations(range(4),2):
        Y=np.zeros((4,4),dtype=complex);Y[i,j]=Y[j,i]=1
        basis.append((np.zeros_like(Y),Y))
        Y=np.zeros((4,4),dtype=complex);Y[i,j]=Y[j,i]=1j
        basis.append((np.zeros_like(Y),Y))
    assert len(basis)==36
    J=np.block([[np.zeros((4,4)),np.eye(4)],[-np.eye(4),np.zeros((4,4))]]).astype(complex)
    matrices=[]
    for X,Y in basis:
        A=np.block([[X,Y],[-Y.conj(),X.conj()]])
        assert np.max(abs(A.conj().T+A))<1e-13
        assert np.max(abs(A.T@J+J@A))<1e-13
        matrices.append(A)
    return matrices

def wedge_action(A):
    pairs=list(combinations(range(8),2))
    ix={p:i for i,p in enumerate(pairs)}
    W=np.zeros((28,28),dtype=np.complex128)
    for col,(i,j) in enumerate(pairs):
        for k in range(8):
            if k!=j and abs(A[k,i]):
                pair=tuple(sorted((k,j)))
                W[ix[pair],col]+=A[k,i]*(1 if k<j else -1)
            if k!=i and abs(A[k,j]):
                pair=tuple(sorted((i,k)))
                W[ix[pair],col]+=A[k,j]*(1 if i<k else -1)
    assert np.max(abs(W.conj().T+W))<1e-12
    omega=np.zeros(28,dtype=complex)
    for i in range(4):omega[ix[i,i+4]]=1/2
    assert np.max(abs(W@omega))<1e-12
    return W

def main():
    js=json.loads((ROOT/"data/toe_20261113_usp8_27_Cartan_isometric_intertwiner.json").read_text())
    T=np.asarray(js["matrix_real"])+1j*np.asarray(js["matrix_imag"])
    assert T.shape==(28,27)
    gen=defining_basis()
    wedge=[wedge_action(a) for a in gen]
    bm=np.stack([np.concatenate([z.real.ravel(),z.imag.ravel()]) for z in wedge],axis=1)
    rank=np.linalg.matrix_rank(bm)
    assert rank==36
    _,_,_,_,roots=R.load()
    _,Ks=R.pack_roots(roots)
    residuals=[]
    coefficients=[]
    for K in Ks:
        B=T@K@T.conj().T
        target=np.concatenate([B.real.ravel(),B.imag.ravel()])
        alpha,_,_,_=np.linalg.lstsq(bm,target,rcond=None)
        fit=sum((a*w for a,w in zip(alpha,wedge)),np.zeros((28,28),dtype=complex))
        relative=float(np.linalg.norm(B-fit)/np.linalg.norm(B))
        residuals.append(relative)
        coefficients.append([float(a) for a in alpha])
    cartan=json.loads((ROOT/"data/toe_20261113_e6_c4_compact_translation_holography.json").read_text())["lie_type"]["Cartan_commuting_basis_indices"]
    assert all(residuals[k]<1e-9 for k in cartan)
    # If nonCartan residuals are positive, an additional consistent
    # root weight phase / zero-weight U(3) unitary map is necessary.
    full=bool(max(residuals)<1e-9)
    out={
       "status":"PASS_FULL_36_INTERTWINER" if full else "CARTAN_ONLY_INTERTWINER_NONCARTAN_PHASES_NOT_YET_FIXED",
       "standard_USp8_defining_8x8_real_Lie_dim":36,
       "standard_wedge_28x28_real_Lie_dim":int(rank),
       "all_defining_generators_antiHermitian_and_symplectic":True,
       "full_36_lie_intertwiner_already_present":full,
       "repo_Cartan_generator_indices":cartan,
       "Cartan_relative_lstsq_residuals":[residuals[i] for i in cartan],
       "all_36_relative_lstsq_residuals":residuals,
       "maximum_nonCartan_relative_residual":max(z for i,z in enumerate(residuals) if i not in cartan),
       "number_generators_fit_below_1e_minus_9":sum(z<1e-9 for z in residuals),
       "Lie_projection_coefficients_36_by_36":coefficients,
       "next_target":"Find the Cartan-centralizing U(1)^24 x U(3) unitary adjustment on the 27 weight spaces so that ALL K_i transform into the standard 36D wedge Lie algebra.",
       "scope":"This script PROBES the existing Cartan isometry, not the existence of any full USp8 intertwiner. A large residual only means this chosen eigenbasis fails to synchronize root phases."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({k:out[k] for k in ["status","full_36_lie_intertwiner_already_present","number_generators_fit_below_1e_minus_9","maximum_nonCartan_relative_residual"]},indent=2),flush=True)
    return out
if __name__=="__main__":main()
