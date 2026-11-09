#!/usr/bin/env python3
"""One-CZ rank obstruction and constructive two-CZ W33 Q8 completion.

A product U3⊗U3 analyzer spans at most 2+2=4 of the 16 invisible
local Bloch directions per basis, so two purely local analyzers fail.
For every one-CZ (CZ @ U3⊗U3) pair in 950 seeded controls, rank is 76.
With TWO diagonal CZ layers interleaved with local U3 factors the tested
950 pairs ALL reach rank 80. CZ is a single-carrier internal-mode passive
phase mask, NOT a deterministic gate between independently housed photons.
"""
import json,hashlib,sys,math
from pathlib import Path
import numpy as np
from w33_20261109_q8_ten_context_tomography import (
    select,hermitian_operators,projection_design,random_unitary)

def qutrit_haar(rng):
    z=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3))
    q,r=np.linalg.qr(z)
    return q*np.conj(np.diag(r)/np.abs(np.diag(r)))[None,:]

def entangler():
    w=np.exp(2j*np.pi/3)
    return np.diag([w**(a*b) for a in range(3) for b in range(3)])

def candidate(rng,with_cz=True,twice=False):
    A,B=qutrit_haar(rng),qutrit_haar(rng)
    if not with_cz:return np.kron(A,B)
    if twice:
        C,D=qutrit_haar(rng),qutrit_haar(rng)
        return entangler()@np.kron(A,B)@entangler()@np.kron(C,D)
    return entangler()@np.kron(A,B)

def cond(design):
    sv=np.linalg.svd(design,compute_uv=False)
    return float(sv[0]/sv[-1]),float(sv[-1])

def mean_entanglement(U):
    ps=[]
    for v in U.T:
        X=v.reshape(3,3)
        r=X@X.conj().T
        ps.append(1-float(np.trace(r@r).real))
    return float(np.mean(ps)),float(min(ps)),float(max(ps))

def main(path=None):
    orig,(Bell,_,__,ops,___)=select(return_components=True)
    Mb=projection_design(Bell,ops)
    assert np.linalg.matrix_rank(Mb,tol=1e-10)==64
    rng=np.random.default_rng(20261109673)
    max_local_rank=0
    local_sums=[]
    for i in range(20):
        U,V=candidate(rng,False),candidate(rng,False)
        design=np.vstack([Mb,projection_design(U,ops),projection_design(V,ops)])
        rank=int(np.linalg.matrix_rank(design,tol=1e-10))
        max_local_rank=max(max_local_rank,rank)
        local_sums.append(rank)
    assert max_local_rank<=72
    best=None
    rank_counts={}
    # Negative control: one CZ layer after local U3 tensor U3.
    # Positive control: two CZ layers and four local U3 stages;
    # each 3mode stage replicated across 3 spectator rails costs 9
    # two-mode Givens, so two bases require 72 in sum.
    trials=950
    for i in range(trials):
        U,V=candidate(rng,True),candidate(rng,True)
        mat=np.vstack([Mb,projection_design(U,ops),projection_design(V,ops)])
        C,small=cond(mat)
        rank=int(np.linalg.matrix_rank(mat,tol=1e-9))
        rank_counts[str(rank)]=rank_counts.get(str(rank),0)+1
        if best is None or C<best[0]:
            best=(C,i,small,U,V)
    single_rank_counts=rank_counts.copy()
    assert single_rank_counts=={'76':trials}
    two_CZ_counts={}
    best=None
    for i in range(trials):
        U,V=candidate(rng,True,twice=True),candidate(rng,True,twice=True)
        mat=np.vstack([Mb,projection_design(U,ops),projection_design(V,ops)])
        C,small=cond(mat)
        rank=int(np.linalg.matrix_rank(mat,tol=1e-9))
        two_CZ_counts[str(rank)]=two_CZ_counts.get(str(rank),0)+1
        if rank==80 and (best is None or C<best[0]):
            best=(C,i,small,U,V)
    print('CZ_DIAG',single_rank_counts,two_CZ_counts,flush=True)
    assert best is not None,'Two-CZ structured family also rank deficient'
    C,index,mins,U,V=best
    actualrank=int(np.linalg.matrix_rank(np.vstack([Mb,projection_design(U,ops),projection_design(V,ops)]),tol=1e-9))
    assert actualrank==80
    assert C<200
    avg1=mean_entanglement(U)
    avg2=mean_entanglement(V)
    assert avg1[0]>0 and avg2[0]>0
    M=np.vstack([Mb,projection_design(U,ops),projection_design(V,ops)])
    pinv=np.linalg.pinv(M,rcond=1e-13)
    rngstate=np.random.default_rng(20261109817)
    errs=[]
    for rank in (1,2,3,5,9):
        for _ in range(8):
            X=rngstate.normal(size=(9,rank))+1j*rngstate.normal(size=(9,rank))
            rho=X@X.conj().T;rho/=np.trace(rho)
            prob=np.concatenate([np.einsum("ij,ik,kj->j",E.conj(),rho,E).real for E in
                   [Bell[:,9*k:9*(k+1)] for k in range(8)]+[U,V]])
            coeff=pinv@(prob-1/9)
            restored=np.eye(9)/9+np.einsum("k,kij->ij",coeff,ops)
            errs.append(float(np.max(abs(restored-rho))))
    assert max(errs)<5e-11
    # Every local U3⊗U3 stage uses at most 18 two-mode rotations.
    # A two-CZ analyzer has two such stages (<=36 rotations) and
    # two nine-mode diagonal phase masks. Neither global-optimal
    # gate count nor practical component losses are established.
    out={"status":"PASS_STRUCTURED_CZ_TWO_GLOBAL_BASES_W33_Q8_FULL_RANK",
         "Bell_contexts":8,"extra_contexts":2,"total_projective_contexts":10,
         "local_only_two_contexts_ranks":local_sums,
         "max_local_only_rank":max_local_rank,
         "max_two_local_basis_added_local_dimension":8,
         "needed_local_dimension":16,
         "entangler":"CZ=diag(omega^(a*b)), omega=exp(2pi*i/3), internal qutrit modes a,b",
         "structured_candidates_evaluated_per_CZ_family":trials,
         "single_CZ_rank_histogram":single_rank_counts,
         "two_CZ_rank_histogram":two_CZ_counts,
         "CZ_layers_per_extra_analyzer":2,
         "best_candidate_index":index,
         "best_condition":C,
         "best_min_singular":mins,
         "first_basis_linear_entropy":avg1,
         "second_basis_linear_entropy":avg2,
         "full_operator_rank":80,
         "max_test_density_reconstruction_error":max(errs),
         "two_basis_complex_sha256":hashlib.sha256(np.ascontiguousarray(np.stack([U,V])).tobytes()).hexdigest(),
         "upper_two_mode_givens_per_extra_context":36,
         "upper_total_two_mode_givens_over_two_extra_programs":72,
         "extra_programmed_internal_joint_phases_per_basis":18,
         "subsystem_scope":"All operations act on two encoded qutrit factors inside ONE nine-mode optical carrier. The diagonal phase mask does not implement an inter-photon nonlinear gate or spatial Bell nonlocality.",
         "engineering_scope":"Block-local U3 transformations and one joint-diagonal phase. Real routing, cross-talk, switching, losses, and fabrication constraints need a calibrated physical chip."}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("STRUCTURED W33",json.dumps({
        "local_max_rank":max_local_rank,
        "structured_full_rank":out["full_operator_rank"],
        "best_cond":C,
        "single_CZ_rank_hist":single_rank_counts,
        "two_CZ_rank_hist":two_CZ_counts,
        "mean_linear_entropies":[avg1[0],avg2[0]],
        "max_reconstruction_error":max(errs)}))
    return out

if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else None)
