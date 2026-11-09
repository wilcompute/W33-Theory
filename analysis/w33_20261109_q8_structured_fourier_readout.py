#!/usr/bin/env python3
"""Structured two-qutrit nine-mode readout with fixed qutrit Fourier stages.

Search pairs of U=(F3⊗I3) D(phi) (F3⊗F3)
and V=(I3⊗F3) D(psi) (F3⊗F3),
or symmetric L D L. Only diagonal phases are programmable; Fourier
mixers may be manufactured as fixed devices. We never claim that routing,
phase precision or loss is free.
"""
import json,math,sys,hashlib
from pathlib import Path
import numpy as np
from w33_20261109_q8_ten_context_tomography import (
    select,projection_design
)
from w33_20261109_q8_12setting_completion import single_qutrit_H

w=np.exp(2j*np.pi/3)
F3=np.array([[w**(i*j) for j in range(3)] for i in range(3)],complex)/np.sqrt(3)
L=np.kron(F3,F3)
LI=np.kron(F3,np.eye(3))
IL=np.kron(np.eye(3),F3)

def make(phi,which,mode):
    D=np.diag(np.exp(1j*phi))
    if mode=="asymmetric":
        return (LI if which==0 else IL)@D@L
    return L@D@L

def score(Mbell,op,phi,psi,mode):
    U,V=make(phi,0,mode),make(psi,1,mode)
    MM=np.vstack([Mbell,projection_design(U,op),projection_design(V,op)])
    vals=np.linalg.eigvalsh(MM.T@MM)
    small=float(min(vals))
    return float(math.sqrt(max(vals)/small)) if small>1e-13 else float("inf"),small,U,V

def run_family(mode,Mbell,op,rng,n_trials=900):
    best=(float("inf"),None)
    fullrank=0
    record=[]
    for it in range(n_trials):
        a=rng.uniform(-np.pi,np.pi,9)
        b=rng.uniform(-np.pi,np.pi,9)
        cond,s,U,V=score(Mbell,op,a,b,mode)
        if s>1e-12:fullrank+=1
        if cond<best[0]:best=(cond,(a,b,U,V,it,s))
        if it in (9,99,299,n_trials-1):record.append({"trial":it+1,"best_condition":best[0],
                                                      "fullrank_candidates":fullrank})
    if best[1] is None:return {"mode":mode,"full_rank_found":False,"trials":n_trials,"snapshots":record}
    cond,(a,b,U,V,index,smin)=best
    # one-coordinate diagonal phase search
    accepted=0
    for sc,n in ((.7,500),(.25,500),(.06,500)):
        for _ in range(n):
            which=int(rng.integers(0,2)); j=int(rng.integers(0,9))
            aa,bb=a.copy(),b.copy()
            (aa if which==0 else bb)[j]+=rng.normal(scale=sc)
            new,sm,uu,vv=score(Mbell,op,aa,bb,mode)
            if new<cond:
                cond=new;smin=sm;a=aa;b=bb;U=uu;V=vv;accepted+=1
    MM=np.vstack([Mbell,projection_design(U,op),projection_design(V,op)])
    rank=int(np.linalg.matrix_rank(MM,tol=1e-9))
    assert rank==80
    pinv=np.linalg.pinv(MM,rcond=1e-13)
    errors=[]
    B=select(return_components=True)[1][0]
    rng2=np.random.default_rng(2026110911)
    for rank_state in (1,2,4,9):
        for k in range(8):
            X=rng2.normal(size=(9,rank_state))+1j*rng2.normal(size=(9,rank_state))
            rho=X@X.conj().T;rho/=np.trace(rho)
            p=np.r_[np.einsum("ij,ik,kj->j",B.conj(),rho,B).real,
                    np.einsum("ij,ik,kj->j",U.conj(),rho,U).real,
                    np.einsum("ij,ik,kj->j",V.conj(),rho,V).real]
            c=pinv@(p-1/9)
            restored=np.eye(9)/9+np.einsum("k,kij->ij",c,op)
            errors.append(float(np.max(abs(restored-rho))))
    assert max(errors)<5e-12
    return {"mode":mode,"full_rank_found":True,"fullrank_first_stage":fullrank,
            "trials":n_trials,"best_pre_refinement":record[-1]["best_condition"],
            "best_refined_condition":cond,"min_gram_eigenvalue":smin,
            "accepted_phase_search_moves":accepted,
            "two_masks_radians":[a.tolist(),b.tolist()],
            "two_bases_sha256":hashlib.sha256(np.ascontiguousarray(np.stack([U,V])).tobytes()).hexdigest(),
            "max_reconstruction_error":max(errors),
            "two_mode_generic_elements_extra_per_basis_upper":27 if mode=="asymmetric" else 36,
            "fixed_3mode_Fourier_blocks_per_basis":9 if mode=="asymmetric" else 12,
            "tunable_phase_mask_entries_per_basis":9,
            "extra_basis_programming":"Only 9 diagonal phase masks; fixed Fourier blocks. Switching/rail crossings/loss of the 3-mode Fourier networks are NOT accounted for.",
            "snapshots":record}

def main(path=None):
    _,(B,_,_,op,_)=select(return_components=True)
    MB=projection_design(B,op)
    rng=np.random.default_rng(2026110926)
    fam=[run_family(x,MB,op,rng) for x in ("asymmetric","symmetric")]
    out={"status":"STRUCTURED_FOURIER_10_SETTING_PHASE_MASK_SEARCH",
         "families":fam,
         "extra_modes":9,"Bell_contexts":8,
         "reference_generic_tunable_Givens_per_basis":36,
         "optical_scope":"Symmetric and asymmetric structured Fourier-phase Fourier designs are fixed-phase physical network proposals, not proof of hardware feasibility or globally optimal condition numbers.",
         "no_novelty_claim":True}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("STRUCTURED",[(x["mode"],x["full_rank_found"],x.get("best_refined_condition"),x.get("fullrank_first_stage")) for x in fam])
    return out
if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else None)
