#!/usr/bin/env python3
"""Falsify naive 9-versus-7 readout claims with actual 4-port KS detection model.

The old sign-flip epsilon<0.0304 was an artificial model of four
INDEPENDENT dichotomic signs. One physical 4-port one-hot
interferometer outputs exactly one click, making the product of
four 2P-I signs identically -1 irrespective of its phase errors!
Without verifying operational ray equivalences ACROSS contexts,
beta=9 is a tautology even in a context-dependent classical device.

This code: replays all 9 Peres and 40 Witting unitary gate blocks,
independent coherent phase/rotation drift, measured cross-context
ray-projector overlap, and an explicit no-click assignment/shot budget.
Assumptions reported; NOT loophole-free noncontextuality witness.
"""
from __future__ import annotations
import json,math,sys,collections
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
OUT=ROOT/"data"/"toe_20261104_contextuality_compatibility_detection_budget.json"
PREV=ROOT/"data"/"toe_20261104_ks18_witting_interferometer_compiler.json"
def block(g):
    return np.array(g["exact_Givens_block_real"],dtype=float)+1j*np.array(g["exact_Givens_block_imag"],dtype=float)
def analyzer(raycontext,rng,sigma_angle,sigma_phase):
    A=np.diag(np.exp(1j*np.array(raycontext["phases"])))
    for rec in reversed(raycontext["blocks"]):
        i,j=rec["modes"]
        G=block(rec)
        a=rng.normal(0,sigma_angle)
        b=rng.normal(0,sigma_phase)
        R=np.array([[math.cos(a),math.sin(a)],[-math.sin(a),math.cos(a)]],dtype=complex)
        Z=np.diag([np.exp(1j*b/2),np.exp(-1j*b/2)])
        U=np.eye(4,dtype=complex)
        U[np.ix_([i,j],[i,j])]=Z@R@G
        A=U.conj().T@A
    assert np.max(abs(A.conj().T@A-np.eye(4)))<1e-12
    labels=raycontext.get("rays",raycontext.get("ray_labels"))
    return {int(labels[idx]):A[:,i] for i,idx in enumerate(raycontext["permutation"])}
def mismatches(contexts,rng,sigma_angle,sigma_phase):
    rays=collections.defaultdict(list)
    for context in contexts:
        for ray,v in analyzer(context,rng,sigma_angle,sigma_phase).items():
            rays[ray].append(v)
    mism=[]
    for entries in rays.values():
        assert len(entries)>=2
        for i in range(len(entries)):
            for j in range(i+1,len(entries)):
                val=1-abs(np.vdot(entries[i],entries[j]))**2
                assert -1e-12<=val<=1+1e-12
                mism.append(max(0,float(val)))
    return float(np.mean(mism)),float(np.max(mism)),len(mism)
def run():
    data=json.loads(PREV.read_text(encoding="utf8"))
    nine=data["best_18ray_contexts"]
    witting=data["Witting_all_40_contexts"]
    assert len(nine)==9 and len(witting)==40
    rng=np.random.default_rng(20261104)
    measured=[]
    for sig in (0,.005,.02,.05,.1):
        rows=[]
        for _ in range(96):
            ks=mismatches(nine,rng,sig,sig)
            wi=mismatches(witting,rng,sig,sig)
            assert ks[2]==18
            assert wi[2]==240  # each of 40 rays occurs 4 times, C(4,2)=6
            rows.append((ks,wi))
        for name,j in (("KS18",0),("Witting40",1)):
            measured.append(dict(protocol=name,sigma_angle_and_phase_rad=sig,
                monte_carlo_independent_reconfigurations=96,
                avg_shared_ray_projector_infidelity=float(np.mean([row[j][0] for row in rows])),
                worst_pair_per_run_infidelity_p95=float(np.quantile([row[j][1] for row in rows],.95)),
                max_observed_shared_ray_infidelity=float(max(row[j][1] for row in rows)),
                pair_comparisons_per_run=rows[0][j][2]))
    assert all(v["avg_shared_ray_projector_infidelity"]<1e-12
               for v in measured if v["sigma_angle_and_phase_rad"]==0)
    assert all(v["avg_shared_ray_projector_infidelity"]>0
               for v in measured if v["sigma_angle_and_phase_rad"]>.0)
    # Deterministic contextual classical model if "same ray" not required
    # to have same response across different contexts:
    # choose exactly one active detector index j per context, independent.
    deterministic_context_indices=(0,1,2,3,0,1,2,3,0)
    assert len(deterministic_context_indices)==9
    classical_contextual_beta=9
    # If no click is assigned all four dichotomic signs -1, then product
    # +1 rather than the one-hot -1. No-click probability 1-eta.
    eta_rows=[]
    for eta in (.7,.8,8/9,.9,.95,.98,1):
        expected_beta=9*(2*eta-1)
        gap=expected_beta-7
        shots_for_5sigma=None
        if gap>1e-12 and 0<eta<1:
            shots_for_5sigma=math.ceil(25*36*eta*(1-eta)/(gap*gap))
        eta_rows.append(dict(total_single_photon_detection_probability=eta,
            unconditional_beta_under_all_minus_no_click_assignment=expected_beta,
            exceeds_standard_7_bound_under_perfect_context_equivalence=gap>0,
            independent_Bernoulli_5sigma_shots_per_context=shots_for_5sigma,
            independent_Bernoulli_5sigma_total_trials=None if shots_for_5sigma is None else 9*shots_for_5sigma))
    assert abs(eta_rows[3]["independent_Bernoulli_5sigma_shots_per_context"]-2025)<=1
    result=dict(status="PASS_KS18_WITTING_COMPATIBILITY_AND_NOCLICK_FALSIFIER",
        ideal_single_click_four_port_context_product=-1,
        ideal_nine_context_parity_sum_is_9_for_ANY_9_orthonormal_bases_even_when_miscalibrated=True,
        context_dependent_classical_one_hot_hidden_variable_model_attains_beta9=True,
        contextual_model_proves_no_compatibility_free_witness=True,
        previous_independent_4_dichotomic_sign_flip_threshold_is_not_physical_single_click_noise_threshold=True,
        exact_nine_contexts=9,exact_Witting_contexts=40,
        simulated_phase_and_beamsplitter_drift=measured,
        sample_no_click_and_trial_budget=eta_rows,
        detection_assignment="Every four-port single-photon detection outcome has one +1 and three -1 ray signs => product -1. No click assigned four -1 => product +1; beta=9(2eta-1), not a universal detection-efficiency bound.",
        noncontextual_threshold_in_specific_no_click_assignment_eta_greater_than=8/9,
        compatibility_test="For each nominal ray shared across contexts, compare rank-one POVM projector tr(P_from_context_a P_from_context_b) with calibrated coherent device. Monte Carlo reports mismatch in independent mixing-angle and relative-phase perturbations; has no claim of an experimentally demonstrated operational-equivalence error budget.",
        experimental_limit="This demonstrates why beta9 after one-hot outcome postselection proves nothing without contexts defining the SAME projector. Estimated shot requirements assume iid detection, exact eta, independent events, no adverse memory, accurate cross-context equivalence and specified no-click assignment; not a loophole-free KCBS/KS test.",
        prior_art="Peres/Cabello contextuality, established experimental compatibility/detection loopholes and repo 4-mode compiler. Falsifies overstrong use of epsilon 3 percent sign-flip figure as physical detector threshold.")
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(result["status"],"eta=.9 shot per context",eta_rows[3]["independent_Bernoulli_5sigma_shots_per_context"],flush=True)
    return result
if __name__=="__main__":run()
