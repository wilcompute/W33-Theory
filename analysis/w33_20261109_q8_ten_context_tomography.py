#!/usr/bin/env python3
"""Optimal 10 projective settings: W33 Q8 Bell 8-MUB + two generic 9-mode bases.
Exact projective-setting information lower bound ceil((9^2-1)/(9-1))=10.
This construction is independent of strong-unextendibility of MUB extension:
additional bases are NOT mutually unbiased; generic unitaries suffice.
"""
import hashlib
import json
import sys
from pathlib import Path
import numpy as np
from w33_20261109_q8_correlation_five import frames, frame_map
from w33_20261109_q8_12setting_completion import single_qutrit_H

def hermitian_operators():
    H=single_qutrit_H()
    op=np.array([np.kron(x,y) for x in H for y in H]+
                [np.kron(x,np.eye(3)/np.sqrt(3)) for x in H]+
                [np.kron(np.eye(3)/np.sqrt(3),x) for x in H])
    assert op.shape==(80,9,9)
    assert np.max(abs(np.einsum("kij,lji->kl",op,op)-np.eye(80)))<2e-13
    return op

def projection_design(E,op):
    # each row is tr(P_e O_k), yielding p-1/9 = M @ theta.
    return np.einsum("ij,kil,lj->jk",E.conj(),op,E).real

def random_unitary(rng):
    z=rng.normal(size=(9,9))+1j*rng.normal(size=(9,9))
    q,r=np.linalg.qr(z)
    q=q*np.conj(np.diag(r)/np.abs(np.diag(r)))[None,:]
    return q

def select(seed=2026110917,tries=250,return_components=False):
    rng=np.random.default_rng(seed)
    op=hermitian_operators()
    bell=frames()[1][0]
    mb=projection_design(bell,op)
    bgram=mb.T@mb
    assert np.linalg.matrix_rank(mb,tol=1e-10)==64
    assert np.max(abs(bgram[:64,:64]-np.eye(64)))<3e-12
    assert np.max(abs(bgram[64:,:]))<3e-12
    trials=[]
    best=None
    # Need 16 novel local directions beyond all 8 Bell contexts.
    for t in range(tries):
        U=random_unitary(rng); V=random_unitary(rng)
        P=np.vstack([projection_design(U,op),projection_design(V,op)])
        local=P[:,64:]
        singular=np.linalg.svd(local,compute_uv=False)
        score=float(min(singular))
        trials.append(score)
        if best is None or score>best[0]:
            best=(score,t,U,V,P)
    score,index,U,V,P=best
    m=np.vstack([mb,P])
    svals=np.linalg.svd(m,compute_uv=False)
    assert len(svals)==80 and min(svals)>1e-6
    assert np.linalg.matrix_rank(m,tol=1e-10)==80
    pinv=np.linalg.pinv(m,rcond=1e-14)
    rngtest=np.random.default_rng(seed+1)
    errors=[]
    for rank in (1,2,3,5,9):
        for _ in range(12):
            x=rngtest.normal(size=(9,rank))+1j*rngtest.normal(size=(9,rank))
            rho=x@x.conj().T;rho/=np.trace(rho)
            probs=np.concatenate([np.einsum("ij,ik,kj->j",e.conj(),rho,e).real
                                  for e in (bell,U,V)])
            theta=pinv@(probs-1/9)
            restored=np.eye(9)/9+np.einsum("k,kij->ij",theta,op)
            errors.append(float(np.max(abs(restored-rho))))
    assert max(errors)<3e-12
    # Baseline: 8 Bell settings alone and 1 additional generic orthobasis.
    m9=np.vstack([mb,P[:9]])
    assert np.linalg.matrix_rank(m9,tol=1e-10)<=72
    ov=np.abs(U.conj().T@V)**2
    mublike=float(np.max(abs(ov-1/9)))
    assert mublike>0.01 # generic 9d bases, not a tenth MUB
    # Extra eigenvector bases must not be locally maximally entangled all the time.
    assert min(svals)>0.02
    complex_matrix=np.ascontiguousarray(np.stack([U,V]))
    hexdigest=hashlib.sha256(complex_matrix.tobytes()).hexdigest()
    result={
      "status":"PASS_MINIMAL_TEN_PROJECTIVE_SETTINGS_W33_Q8_8PLUS2",
      "eight_W33_Q8_Bell_contexts":8,
      "additional_generic_nine_mode_projective_settings":2,
      "nine_outcomes_per_setting":9,
      "total_outcome_probabilities":90,
      "eight_bell_design_rank":64,
      "nine_setting_upper_bound_rank":72,
      "ten_setting_design_rank":80,
      "operator_parameter_count":80,
      "independent_probabilities_per_projective_setting":8,
      "global_projective_minimum_settings":10,
      "construction_meets_projective_information_lower_bound":True,
      "extra_bases_are_mutually_unbiased":False,
      "max_nonunbiased_overlap_deviation":mublike,
      "source_rng_seed":seed,
      "candidate_pair_trials":tries,
      "best_candidate_zero_based_index":index,
      "best_local_16d_singular_min":score,
      "median_candidate_local_singular_min":float(np.median(trials)),
      "combined_singular_min":float(min(svals)),
      "combined_singular_max":float(max(svals)),
      "combined_condition_number":float(max(svals)/min(svals)),
      "operator_gram_max_error":float(np.max(abs(np.einsum("kij,lji->kl",op,op)-np.eye(80)))),
      "matrix_sha256":hexdigest,
      "max_random_state_reconstruction_error":max(errors),
      "tested_random_state_count":len(errors),
      "physical_resource_scope":"Eight Bell analyzers plus two general 9-mode projective analyzers; a general 9mode unitary can cost <=36 two-mode Givens couplers, not the 3-mode product analyzers of the 12-setting alternative.",
      "novelty_scope":"10 projective settings is an elementary known information lower bound, and full two-qutrit projective tomography is known; repo-specific insight is 8 Q8 Bell MUB contexts + only 2 non-MUB settings, consistent with strong MUB unextendibility."
    }
    if return_components:
        return result,(bell,U,V,op,pinv)
    return result

def main(path=None):
    d=select()
    if path:Path(path).write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS 10 projective contexts",json.dumps({k:d[k] for k in (
        "ten_setting_design_rank","global_projective_minimum_settings",
        "combined_condition_number","best_local_16d_singular_min",
        "max_random_state_reconstruction_error","best_candidate_zero_based_index")}))
    return d

if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else None)
