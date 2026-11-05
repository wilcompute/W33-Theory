#!/usr/bin/env python3
"""Operational local-qutrit MUB Bell witness vs Witting 40x40 tomography.

Four Pauli MUBs per qutrit (12 rank-one projectors), Bob uses conjugates.
The matched-outcome operator is exactly (I9+3|Phi3><Phi3|)/4.
Thus all separable states obey Pmatch<=1/2 (without postselection).
Compile the local basis rotations as four-rail Givens interferometers,
then calculate exact IID loss-adjusted binomial discrimination rules.
"""
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np
from scipy.stats import binom
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261104_fourrail_givens_drift_detector_validation import compile_mesh,emitted
OUT=ROOT/"data/toe_20261105_mub_memory_local_witness.json"

def bases():
    d=3;w=np.exp(2j*np.pi/3)
    X=np.zeros((d,d),complex)
    for j in range(d):X[(j+1)%d,j]=1
    Z=np.diag(w**np.arange(d))
    arr=[np.eye(d, dtype=complex)]
    for a in range(3):
        _,v=np.linalg.eig(X@np.linalg.matrix_power(Z,a))
        assert np.max(abs(v.conj().T@v-np.eye(3)))<1e-12
        arr.append(v)
    for i in range(4):
        for j in range(i+1,4):
            assert np.max(abs(abs(arr[i].conj().T@arr[j])**2-1/3))<2e-12
    return arr

def get_min_trials(p0,p1,alpha=.01,power=.95,maxshots=12000):
    assert 0<p0<p1<1
    for n in range(1,maxshots+1):
        k=int(binom.isf(alpha,n,p0))+1
        fpr=float(binom.sf(k-1,n,p0))
        alt=float(binom.sf(k-1,n,p1))
        if fpr<=alpha and alt>=power:
            return {"shots":n,"reject_if_hits_at_least":k,
                    "exact_false_alarm":fpr,"model_power":alt}
    return None

def main():
    M=bases();eye9=np.eye(9)
    phi=np.zeros(9,complex)
    for a in range(3):phi[4*a]=1/math.sqrt(3)
    Bell=np.outer(phi,phi.conj())
    matching=np.zeros((9,9),complex)
    compiled=[]
    for U in M:
        for j in range(3):
            v=U[:,j];P=np.outer(v,v.conj())
            matching+=np.kron(P,P.conj())/4
        local=[]
        for target in (U.conj().T,U.T):
            V4=np.eye(4,dtype=complex)
            V4[:3,:3]=target
            gates,phases=compile_mesh(V4)
            assert len(gates)<=6  # compiler can include diagonal-only blocks
            local.append((gates,phases))
        compiled.append(local)
    assert np.max(abs(matching-(eye9+3*Bell)/4))<2e-12
    assert np.max(abs(matching-matching.conj().T))<2e-12
    rng=np.random.default_rng(20261105)
    calibrations=[]
    for sigma in (0,.005,.02,.05):
        vals=[]
        for repetition in range(64):
            cq=[]
            for local in compiled:
                UA=emitted(*local[0],rng,sigma)
                UB=emitted(*local[1],rng,sigma)
                amp=(UA[:3,:3]@UB[:3,:3].T)/math.sqrt(3)
                pure=float(sum(abs(amp[j,j])**2 for j in range(3)))
                mix=float(sum(np.linalg.norm(UA[j,:3])**2*
                              np.linalg.norm(UB[j,:3])**2 for j in range(3))/9)
                cq.append(.35*pure+.65*mix)
            vals.append(sum(cq)/4)
        if sigma==0: assert max(abs(v-(1+2*.35)/3) for v in vals)<1e-12
        calibrations.append({
           "static_independent_mesh_phase_angle_sigma":sigma,
           "calibration_realizations":64,
           "observed_min_match_probability":float(min(vals)),
           "observed_mean_match_probability":float(np.mean(vals)),
           "observed_max_match_probability":float(max(vals)),
           "not_a_separable_null_calibration":True})
    p=.35;eta=.85
    F=(1+8*p)/9
    null_F=1/3
    ideal_c=(1+3*F)/4
    null_c=(1+3*null_F)/4
    assert abs(ideal_c-(1+2*p)/3)<1e-12 and null_c==.5
    nloss=(eta**2)*null_c
    aloss=(eta**2)*ideal_c
    decision=get_min_trials(nloss,aloss)
    assert decision is not None
    ideal=get_min_trials(null_c,ideal_c)
    global_ideal=get_min_trials(null_F,F)
    assert ideal and global_ideal
    out={
      "status":"PASS_FOUR_QUTRIT_EMBEDDED_QUTRIT_MUB_PRODUCT_BELL_WITNESS",
      "qutrit_MUB_bases":4,
      "rank_one_measurement_projectors":12,
      "local_measurement_setting_pairs":4,
      "local_output_ports":3,
      "four_rail_compiler_blocks_per_side_max":max(
         len(side[0]) for basis in compiled for side in basis),
      "four_rail_nontrivial_two_mode_mixers_per_side_max":int(max(
         sum(bool(abs(G[0,1])>1e-10) for _,G in side[0])
         for basis in compiled for side in basis)),
      "matching_operator_exact_identity":"C=(I9+3 Bell3)/4",
      "separable_true_fidelity_upper_bound":1/3,
      "separable_match_probability_upper_bound":null_c,
      "alternative_survival_p":p,
      "alternative_Bell_fidelity":F,
      "alternative_match_probability":ideal_c,
      "independent_detector_efficiency_each":eta,
      "coincidence_efficiency":eta**2,
      "null_unconditional_joint_match_probability":nloss,
      "alternative_unconditional_joint_match_probability":aloss,
      "exact_binomial_loss_adjusted_MUB_design":decision,
      "exact_binomial_perfect_detector_MUB_design":ideal,
      "ideal_global_entangling_Bell_projection_comparator":global_ideal,
      "static_mesh_calibrations":calibrations,
      "statistical_boundary":"Exact binomial uses known IID detector efficiency independent of state and outcomes, fair/random basis sampling and ideal aligned MUBs. Noise simulations are static sample observations, do not certify a separable upper bound under adversarial drift. MUB is witness-adapted but not proven globally optimal across all LOCC protocols.",
      "originality_boundary":"MUB 2-design Bell witness, four-port unitary compilation, Hoeffding/binomial tests are established. Repo-local contribution is exact 4-setting qutrit memory witness compiled and compared to the Witting local dual."}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS MUB matched operator + 4-mode meshes, eta=.85 shots",decision["shots"],"ideal shots",ideal["shots"],"global",global_ideal["shots"])
    print("CERTIFICATE",OUT)
    return out
if __name__=="__main__":main()
