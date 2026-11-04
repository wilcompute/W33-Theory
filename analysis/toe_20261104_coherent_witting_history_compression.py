#!/usr/bin/env python3
"""Four-mode *coherent heralded* compression of 9D qutrit process Choi history.

Earlier output-only 120-Kraus measure/prepare map erases input-output
correlations and has no process distinguishability. We explicitly
construct rank-4 K:C9->C4, its 5D orthogonal failure complement,
place ideal identity Choi |Phi3> on a chosen Witting ray, and calculate
all 40 Witting effects with a heralded failure event. CPTP as a
flagged 4+5 direct sum, strictly probabilistic as 9->4.

Finite-dimensional QIT exact construction, NOT retrocausal self
entanglement; state-selective action and heralded postselection assumed.
"""
from __future__ import annotations
import sys,math,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
OUT=ROOT/"data"/"toe_20261104_coherent_witting_history_compression.json"
from exploration.w33_witting_srg_bridge import construct_witting_rays
def orthoframe(seed,dim):
    vectors=[]
    for col in [seed]+list(np.eye(dim,dtype=complex)):
        v=np.asarray(col,dtype=complex).copy()
        for u in vectors:v-=u*np.vdot(u,v)
        n=np.linalg.norm(v)
        if n>1e-10:vectors.append(v/n)
        if len(vectors)==dim:break
    M=np.column_stack(vectors)
    assert M.shape==(dim,dim) and np.max(abs(M.conj().T@M-np.eye(dim)))<1e-12
    return M
def j(t):
    phi=np.eye(3,dtype=complex).reshape(-1)/math.sqrt(3)
    return t*np.outer(phi,phi.conj())+(1-t)*np.eye(9)/9
def run():
    W=np.asarray(construct_witting_rays())
    assert W.shape==(40,4)
    I9=np.eye(9)
    phi=np.eye(3,dtype=complex).reshape(-1)/math.sqrt(3)
    H=orthoframe(phi,9)
    U=orthoframe(W[0],4)
    K=U@H[:,:4].conj().T
    F=H[:,4:].conj().T
    assert K.shape==(4,9) and F.shape==(5,9)
    assert np.max(abs(K.conj().T@K+F.conj().T@F-I9))<1e-12
    assert np.max(abs(K@K.conj().T-np.eye(4)))<1e-12
    assert np.max(abs(K@phi-W[0]))<1e-12
    assert np.linalg.matrix_rank(K)==4
    Pi=np.array([np.outer(v,v.conj()) for v in W])
    assert np.max(abs(Pi.sum(axis=0)-10*np.eye(4)))<1e-12
    def probabilities(t):
        rho=j(t)
        survivor=K@rho@K.conj().T
        outcome=[float(np.trace(P@survivor).real/10) for P in Pi]
        failure=float(np.trace(F@rho@F.conj().T).real)
        assert abs(sum(outcome)+failure-1)<1e-12
        assert min(outcome)>-1e-13 and failure>-1e-13
        return np.array(outcome+[failure])
    p0=probabilities(1)
    p1=probabilities(0)
    orth=np.sum(abs(W@W[0].conj())<1e-9)
    assert orth==12
    assert abs(p0[0]-.1)<1e-12
    assert sum(abs(p0[i]-0)<1e-12 for i in range(1,40))==12
    assert sum(abs(p0[i]-1/30)<1e-12 for i in range(1,40))==27
    assert np.max(abs(p1[:40]-1/90))<1e-12
    assert abs(p1[-1]-5/9)<1e-12
    TV=.5*sum(abs(p0-p1))
    assert abs(TV-31/45)<1e-12
    success=.5*(1+TV)
    assert abs(success-38/45)<1e-12
    assert abs(np.trace(K@j(1)@K.conj().T).real-1)<1e-12
    assert abs(np.trace(K@j(0)@K.conj().T).real-4/9)<1e-12
    assert abs(np.trace(K.conj().T@K@I9/9).real-4/9)<1e-12
    samples=[]
    for m in (0,1,4,8,13,14,20):
        t=.9**m
        pm=probabilities(t)
        for eta in (1,.7,.2,0):
            TV_eta=.5*eta*sum(abs(pm-p1))
            assert abs(TV_eta-eta*t*31/45)<1e-12
            samples.append(dict(exchange_count=m,t=t,external_survival_eta=eta,
                post_herald_outcomes_total=40,
                all_outcomes_variational_distance_to_depolarized_with_extra_vacuum=TV_eta,
                optimal_equal_prior_success_vs_fully_depolarized=.5*(1+TV_eta),
                Choi_entanglement_negativity=max(0,(4*t-1)/3)))
    assert next(x for x in samples if x["exchange_count"]==14 and x["external_survival_eta"]==1)["Choi_entanglement_negativity"]==0
    assert next(x for x in samples if x["exchange_count"]==14 and x["external_survival_eta"]==1)["optimal_equal_prior_success_vs_fully_depolarized"]>.5
    result=dict(status="PASS_COHERENT_HERALDED_WITTING_TEMPORAL_9_TO_4_COMPRESSION",
        input_history_dimension=9,success_output_dimension=4,failure_subspace_dimension=5,
        projection_success_rank=4,
        isometry_4_to_9_in_success_subspace=True,
        quantum_map_deterministic_faithful_9_to_4_impossible_by_dimension=True,
        flagged_total_4plus5_map_isometry_exact=True,
        success_probability_maximally_mixed_history=4/9,
        success_probability_ideal_identity_Choi=1,
        Witting_40ray_POVM_success_operator_count=40,
        orthogonal_to_ideal_Witting_ray_count=12,
        ideal_first_Witting_ray_probability=0.1,
        ideal_remaining_nonorthogonal_ray_probabilities=1/30,
        fully_depolarized_every_ray_unconditional_probability=1/90,
        fully_depolarized_failure_probability=5/9,
        full_joint_Helstrom_success_identity_vs_depolarizing=17/18,
        heralded_Witting_success_identity_vs_depolarizing=success,
        heralded_Witting_total_variation=TV,
        preceding_output_only_Witting_success=.5,
        absolute_heralded_gain_over_output_only=success-.5,
        ideal_identity_outcome_probabilities=[round(float(x),12) for x in p0],
        fully_depolarized_outcome_probabilities=[round(float(x),12) for x in p1],
        repeated_exchange_and_erasure_samples=samples,
        crucial_no_go="A 9-dimensional unknown process history cannot be compressed reversibly/deterministically into 4 dimensions. The 4D success branch is a projector with average success 4/9 on a uniform 9D input, with a 5D failure flag. A tailored Choi identity state succeeds with probability one: state-specific, not universal.",
        witness_warning="Process distinguishability survives even when Choi entanglement has vanished (m>=14 in this noise model). A difference from fully depolarized is NOT an entanglement witness.",
        source_owner="Temporal qutrit Choi and Witting 2-design previous repo work; here operational coherent selective 4D compression with exact 40 outcomes and flags.",
        physical_scope="Ideal mathematical quantum instrument. No optical circuit for 9->4 coherent compression, time-bin single photon experiment, memory process tensor, causal intervention or hardware noise calibration.")
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(result["status"],"success",success,"uniform pass",4/9,flush=True)
    return result
if __name__=="__main__":run()
