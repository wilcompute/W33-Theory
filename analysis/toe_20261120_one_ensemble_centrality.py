#!/usr/bin/env python3
"""Single maximally mixed target centrality certificate for a unitary relative-order K.

Existing DQC1/normalized trace methods are prior art. We test exact geometry,
SPAM bias, coherent vs incoherent order, and finite-shot guaranteed bounds.
"""
import json,math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from toe_20261120_symplectic_order_sic_switch import OMEGA, pauli, points, symp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261120_one_ensemble_centrality.json"
D=9
I=np.eye(D,dtype=complex)

def trial_operators():
    ps=points()
    u,v=next((a,b) for a in ps for b in ps if symp(a,b)==1)
    A,B=pauli(u),pauli(v)
    ideal=(B@A).conj().T@(A@B)
    assert np.max(abs(ideal-OMEGA*I))<1e-12
    rng=np.random.default_rng(32)
    H=rng.normal(size=(D,D))+1j*rng.normal(size=(D,D))
    H=(H+H.conj().T)/2
    H-=np.trace(H).real/D*I
    perturbed=expm(.27j*H)@A
    flawed=(B@perturbed).conj().T@(perturbed@B)
    return ideal,flawed

def noncentrality(K):
    assert np.max(abs(K.conj().T@K-I))<1e-11
    c=np.trace(K)/D
    direct=float(np.linalg.norm(K-c*I)**2)
    traceform=D*(1-abs(c)**2)
    assert abs(direct-traceform)<2e-11
    return {"trace_real":float(c.real),"trace_imag":float(c.imag),
            "trace_abs":float(abs(c)),"noncentrality_Frobenius_squared":direct,
            "one_ensemble_formula_residual":float(abs(direct-traceform))}

def one_ensemble():
    ideal,flawed=trial_operators()
    r0=noncentrality(ideal)
    r1=noncentrality(flawed)
    assert r0["noncentrality_Frobenius_squared"]<1e-20
    assert r1["noncentrality_Frobenius_squared"]>.02
    comps=np.diag(flawed)
    assert abs(np.mean(comps)-np.trace(flawed)/D)<1e-12
    # One control input and a classical uniform randomization of nine basis
    # preparations gives rho=I9/9, no quantum entanglement or SIC needed.
    rng=np.random.default_rng(14)
    shots=400000
    draws=rng.integers(D,size=shots)
    emulated=np.mean(comps[draws])
    assert abs(emulated-np.trace(flawed)/D)<.008
    # Strong failure: an adversarially biased target may hide noncentral K.
    bad=np.diag([1]*8+[-1]).astype(complex)
    unif=noncentrality(bad)
    biased_rho=np.diag([1/8]*8+[0.]).astype(complex)
    fooled=np.trace(biased_rho@bad)
    assert abs(fooled-1)<1e-12 and unif["noncentrality_Frobenius_squared"]>3.5
    prep_bound=float(np.linalg.norm(biased_rho-I/D,ord="nuc"))
    assert abs(prep_bound-2/9)<1e-12
    return {"d":D,"ideal_center":r0,"seeded_noncentral":r1,
            "uniform_basis_ensemble_equals_maximally_mixed":True,
            "random_basis_prep_samples":shots,
            "sampled_complex_amplitude":list(map(float,(emulated.real,emulated.imag))),
            "biased_preparation_counterexample":{
                "true_unitary_noncentral_Frobenius_squared":unif["noncentrality_Frobenius_squared"],
                "biased_target_amplitude_abs":float(abs(fooled)),
                "target_trace_norm_distance_to_uniform":prep_bound},
            "physical_scope":"Requires independently warranted unitary K, coherent order control and a randomized 9-basis ensemble. Not a measurement of physical SU3 colour."}

def sample_bound(eps=.25,delta=.01):
    assert 0<eps<math.sqrt(D) and 0<delta<1
    required_p=(1-math.sqrt(1-eps*eps/D))/2
    zero_fail_trials=math.ceil(math.log(delta)/math.log(1-required_p))
    p_up=1-delta**(1/zero_fail_trials)
    cert_sq=D*(1-max(0,1-2*p_up)**2)
    assert cert_sq<=eps*eps+1e-12
    # Two-quadrature Hoeffding, uniformly randomized basis and calibrated state:
    # |c-hat c|<=sqrt(2) sqrt(2 log(4/delta)/N).
    critical=(1-math.sqrt(1-eps**2/D))/math.sqrt(2)
    N=math.ceil(2*math.log(4/delta)/(critical*critical))
    radius=math.sqrt(4*math.log(4/delta)/N)
    assert D*(1-max(0,1-radius)**2)<=eps**2+1e-12
    # Conservative bound under target trace-distance error and additive
    # statistical complex error, assuming dephasing v<=1 and no readout bias.
    def upper(obs_abs,stat_err,prep_trace_norm):
        lower=max(0,min(1,obs_abs-stat_err-prep_trace_norm))
        return D*(1-lower**2)
    assert upper(1,0,0)<1e-12
    assert upper(1,0,2/9)>3.5
    # Simulate target-calibrated phase-locked iid heralded failures.
    rng=np.random.default_rng(704)
    Nsim=3000
    model_failure_p=.01
    failures=int(rng.binomial(Nsim,model_failure_p))
    fail_frac=failures/Nsim
    return {
        "dimension":D,"confidence":1-delta,
        "centrality_Frobenius_tolerance":eps,
        "phase_matched_zero_failure_Clopper_Pearson_accepted_shots":zero_fail_trials,
        "phase_matched_zero_failure_exact_CP_p_upper":p_up,
        "phase_matched_zero_failure_squared_Frobenius_upper":cert_sq,
        "unknown_center_phase_two_quadrature_accepted_shots_each":N,
        "unknown_phase_two_quadrature_total_shots":2*N,
        "target_trace_norm_calibration_guard":"||K - (Tr K/d)I||_F^2 <= d[1-max(0,|a_obs|-complex_stat_error-||rho-I/d||_1)^2], provided visibility <=1 and no additive readout artifact",
        "seeded_driftless_failures_at_1pct_reference":failures,
        "seeded_trials":Nsim,
        "seeded_observed_failure_rate":fail_frac,
        "loss_warning":"For phase-matched zero-failure certificate, 1% physical detector flips generally prevent a noncentrality <=0.25 certificate without independent noise calibration. No device results."
        }

def nonunitary_no_go():
    K=np.diag([1]*8+[0]).astype(complex)
    c=np.trace(K)/D
    true=float(np.linalg.norm(K-c*I)**2)
    wrong=D*(1-abs(c)**2)
    assert abs(true-8/9)<1e-12 and abs(wrong-17/9)<1e-12
    return {"rank_eight_contraction_true_noncentrality_square":true,
            "false_unitary_formula_result":wrong,
            "formula_requires_unitarity":True}

def main(write=True):
    result={
       "status":"PASS_ONE_ENSEMBLE_UNITARY_CENTRALITY_WITH_SPAM_FALSIFIERS",
       "prior_art":"DQC1 one-clean-qubit normalized trace estimate; standard Cauchy-Schwarz equality condition. Increment is a concrete coherent-order centrality audit with calibrated failure bounds against the prior 81-SIC protocol.",
       "centrality":one_ensemble(),
       "finite_shot":sample_bound(),
       "nonunitary_failure":nonunitary_no_go()
    }
    if write: OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    return result

if __name__=="__main__":print(json.dumps(main(),indent=2))
