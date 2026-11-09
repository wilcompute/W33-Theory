#!/usr/bin/env python3
"""Structured 27-coupler analyzer extension with fixed mode permutation.

U=(F3 tensor I3) D(phi) P (F3 tensor F3)
V=(I3 tensor F3) D(psi) Q (F3 tensor F3)
where P,Q are fixed routing permutations. No general 9x9 tunable mesh
is required for these extra bases. The phase-only family with P=I
provably supplies <=4 local Bloch directions per basis and fails.
"""
import json,sys,hashlib,math
from pathlib import Path
import numpy as np
from w33_20261109_q8_structured_fourier_readout import L,LI,IL
from w33_20261109_q8_ten_context_tomography import select,projection_design

def make(phi,perm,side):
    X=LI if side==0 else IL
    return X@np.diag(np.exp(1j*phi))@np.eye(9)[perm,:]@L

def invcount(pi):
    return sum(int(pi[i]>pi[j]) for i in range(9) for j in range(i+1,9))
def local_rank(U,V,ops):
    return int(np.linalg.matrix_rank(np.vstack([
        projection_design(U,ops)[:,64:],
        projection_design(V,ops)[:,64:]]),tol=1e-9))
def cond(BM,U,V,ops):
    X=np.vstack([BM,projection_design(U,ops),projection_design(V,ops)])
    eig=np.linalg.eigvalsh(X.T@X)
    return float(math.sqrt(eig[-1]/eig[0])) if eig[0]>1e-13 else float("inf")
def adjacent_walk(rng,k):
    pi=list(range(9))
    for _ in range(k):
        j=int(rng.integers(0,8))
        pi[j],pi[j+1]=pi[j+1],pi[j]
    return pi

def main(path=None):
    _,(B,_,_,ops,_)=select(return_components=True)
    BM=projection_design(B,ops)
    rng=np.random.default_rng(20261109411)
    counts={}
    best=None
    low_best=None
    for steps in (1,2,3,4,5,6,8,12,20,36):
        full=0
        for t in range(180):
            p=adjacent_walk(rng,steps)
            q=adjacent_walk(rng,steps)
            a=rng.uniform(-math.pi,math.pi,9)
            b=rng.uniform(-math.pi,math.pi,9)
            U=make(a,p,0);V=make(b,q,1)
            rank=local_rank(U,V,ops)
            if rank<16:continue
            full+=1
            c=cond(BM,U,V,ops)
            budget=invcount(p)+invcount(q)
            val=(c,budget,steps,t,a,b,p,q)
            if best is None or c<best[0]:best=val
            if budget<=10 and (low_best is None or c<low_best[0]):low_best=val
        counts[str(steps)]={"full_rank_among_180_pairs":full}
    assert best is not None
    if low_best is not None:
        selected=low_best
        choice="minimal_routing_budget_max_10"
    else:
        selected=best
        choice="best_cond_1800_trials"
    c,cost,steps,t,a,b,p,q=selected
    initial_cond=c
    accepted=0
    for scale,num in ((.5,600),(.18,600),(.055,600)):
        for it in range(num):
            which=int(rng.integers(0,2))
            ix=int(rng.integers(0,9))
            aa=a.copy();bb=b.copy()
            (aa if which==0 else bb)[ix]+=rng.normal(0,scale)
            U=make(aa,p,0);V=make(bb,q,1)
            new=cond(BM,U,V,ops)
            if new<c:
                c=new;a=aa;b=bb;accepted+=1
    U=make(a,p,0);V=make(b,q,1)
    assert local_rank(U,V,ops)==16
    MM=np.vstack([BM,projection_design(U,ops),projection_design(V,ops)])
    assert np.linalg.matrix_rank(MM,tol=1e-9)==80
    inv=np.linalg.pinv(MM,rcond=1e-14)
    trial=[]
    r=np.random.default_rng(20261109412)
    for rank in (1,2,3,5,9):
        for k in range(8):
            x=r.normal(size=(9,rank))+1j*r.normal(size=(9,rank))
            rho=x@x.conj().T;rho/=np.trace(rho)
            probs=np.r_[np.einsum("ij,ik,kj->j",B.conj(),rho,B).real,
                        np.einsum("ij,ik,kj->j",U.conj(),rho,U).real,
                        np.einsum("ij,ik,kj->j",V.conj(),rho,V).real]
            theta=inv@(probs-1/9)
            rr=np.eye(9)/9+np.einsum("k,kij->ij",theta,ops)
            trial.append(float(np.max(abs(rr-rho))))
    assert max(trial)<1e-11
    # Classification of limited original family; 4 independent local operators.
    a0=rng.uniform(-math.pi,math.pi,9)
    idperm=list(range(9))
    single=int(np.linalg.matrix_rank(projection_design(
        make(a0,idperm,0),ops)[:,64:],tol=1e-9))
    assert single==4
    out={"status":"PASS_STRUCTURED_FOURIER_PHASE_PERMUTATION_10SETTING_TOMOGRAPHY",
         "8_W33_Q8_Bell_basis_contexts":8,
         "extra_structured_9mode_basis_contexts":2,
         "rank_after_extra":80,
         "initial_single_phase_no_permutation_local_rank_per_basis":single,
         "phase_only_two_basis_max_possible_local_rank":8,
         "physical_selection":choice,
         "candidate_counts_by_adjacent_walk_length":counts,
         "low_budget_qualified":low_best is not None,
         "selected_permutation_walk_length":steps,
         "selected_total_fixed_adjacent_routing_inversions":cost,
         "first_permutation":p,"second_permutation":q,
         "programmed_diagonal_phase_masks":[a.tolist(),b.tolist()],
         "pre_phase_optimization_condition_number":initial_cond,
         "post_phase_optimization_condition_number":c,
         "phase_optimization_moves_accepted":accepted,
         "fixed_qutrit_Fourier_blocks_per_extra_basis":9,
         "two_mode_givens_per_extra_basis_upper":27,
         "earlier_generic_Givens_per_extra_basis_upper":36,
         "tunable_optical_phases_per_extra_basis":9,
         "max_tested_reconstruction_error":max(trial),
         "reconstructed_density_samples":len(trial),
         "matrix_digest_sha256":hashlib.sha256(np.stack([U,V]).tobytes()).hexdigest(),
         "strict_hardware_scope":"Fixed nine-mode permutation crossings may be lossy and count as components on a chip. The 27 figures exclude routing as tunable couplers; actual compactness must account for crossings, path/timebin conversion and phase drift.",
         "novelty_scope":"Reproducible structured design and phase-covariance obstruction; NOT a newly discovered universal quantum computation theorem or a fabricated optical device."}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS structured permutation",json.dumps({
        "cond":c,"inv":cost,"perms":[p,q],
        "max_reconstruction_error":max(trial),"fullrank_counts":counts}))
    return out
if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else None)
