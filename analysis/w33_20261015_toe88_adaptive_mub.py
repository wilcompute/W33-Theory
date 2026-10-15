"""TOE88: adaptive entanglement-breaking qutrit memory nulls and loopholes.

Four MUB randomized state-matched returns bound adaptive EB strategies only
with secret iid inputs, trusted SPAM, and a fair acceptance rule. Explicit
basis-side-channel + state-dependent loss defeats naive postselection.
"""
from __future__ import annotations
import collections, json, math, random
from scipy.stats import binom
from analysis.w33_20261015_toe85_h2_relation_module import ROOT
from analysis.w33_20261015_toe87_adversarial_temporal import states,confusion

def threshold(n,p0,alpha):
    k=next(x for x in range(n+1) if binom.sf(x-1,n,p0)<=alpha)
    return k,float(binom.sf(k-1,n,p0))

def acceptance_spoof(epsilon):
    # EB chosen-basis dephasing if basis selector is leaked to the device.
    # Admit probability 1 for chosen-basis states and epsilon for others.
    # This is a side-channel/postselection attack, not a fair CPTP channel.
    rate=(3+9*epsilon)/12
    return {"acceptance_other_basis":epsilon,
            "total_accepted_fraction":rate,
            "accepted_state_mean_fidelity":(1+epsilon)/(1+3*epsilon),
            "setting_dependency_max_minus_min":1-epsilon}

def adaptive_hidden_settings(n,trials,seed):
    rng=random.Random(seed)
    records=[]
    for _ in range(trials):
        prior=0;correct=0;frequencies=[0]*4
        for t in range(n):
            # Classic past-dependent choice, chosen BEFORE new secret input.
            guess=(prior+3*frequencies.index(min(frequencies)))%4
            incoming=rng.randrange(12)
            actual_basis=incoming//3
            prob=1 if actual_basis==guess else 1/3
            is_ok=rng.random()<prob
            correct+=is_ok
            frequencies[guess]+=1
            prior=(prior+int(is_ok)+actual_basis)%4
        records.append(correct)
    return {"strategy":"adaptive past-only basis choice, no access to next secret setting",
            "trials":trials,"shots_per_trial":n,
            "min":min(records),"max":max(records),
            "mean":sum(records)/trials,
            "count_ge_calibrated_threshold":None}

def certificate():
    s,_=states()
    assert len(s)==12
    eps_state=.01;eta_measurement=.01
    # Worst-case trace-distance input deviation eps and matched-POVM
    # expectation error eta contribute additively to each survival p.
    ebreak=.5
    robust_eb=min(1,ebreak+eps_state+eta_measurement)
    coherence_v=.25
    coherent=.5+.5*coherence_v
    alt_conservative=coherent-eps_state-eta_measurement
    e_readout=.02;uniform_leak=.03
    p0=confusion(robust_eb,e=e_readout,leak=uniform_leak)
    p1=confusion(alt_conservative,e=e_readout,leak=uniform_leak)
    assert p1>p0
    n=1200;alpha=.001
    k,fp=threshold(n,p0,alpha)
    power=float(binom.sf(k-1,n,p1))
    assert fp<=alpha and power>.95
    attack=acceptance_spoof(.1)
    assert attack["accepted_state_mean_fidelity"]>.8
    fair=acceptance_spoof(1)
    assert fair["accepted_state_mean_fidelity"]==.5
    adaptive=adaptive_hidden_settings(n,96,8804)
    # Under conditional success probability <=p0 each round, coupling with
    # iid uniforms gives stochastic domination by Binomial(n,p0).
    adaptive["count_ge_calibrated_threshold"]="Do not compare raw 0.5 strategy to p0 calibrated threshold as a p-value; use exact supermartingale binomial bound."
    return {
        "quantum_design":"Four qutrit mutually unbiased bases, 12 independently secret randomized input states",
        "adaptive_EB_conditional_per_round_survival_bound":.5,
        "adaptive_nonIID_binomial_tail_valid_if_conditional_success_bound":True,
        "proof_note":"For conditional success probability q_t <= p0, couple each Bernoulli trial to U_t < q_t using fresh iid uniforms: its success count is stochastically bounded by iid Binomial(n,p0), even with adaptive classical history.",
        "input_state_trace_distance_calibration_bound":eps_state,
        "POVM_effect_expectation_calibration_bound":eta_measurement,
        "conservative_true_EB_survival_bound":robust_eb,
        "coherent_v025_ideal_return_mean":coherent,
        "conservative_true_coherent_return_mean":alt_conservative,
        "readout_confusion_rate":e_readout,
        "uniform_replacement_leak_rate":uniform_leak,
        "calibrated_postnoise_EB_bound":p0,
        "calibrated_postnoise_alternative_lower_mean":p1,
        "accepted_shots":n,
        "reject_at_successes_at_least":k,
        "exact_max_EB_tail_alpha":fp,
        "alternative_power_under_ideal_conditional_independence":power,
        "secret_setting_past_adaptive_null_simulation":adaptive,
        "state_dependent_heralding_attacks":[fair,attack,acceptance_spoof(0)],
        "loophole":"Basis metadata leakage combined with setting-dependent acceptance can drive postselected fidelity to 1 for an entanglement-breaking process. Measure per-setting survival rates, keep inputs secret, and bound loss to apply the witness.",
        "limits":"Analytical error envelopes and toy adaptive simulation, not a hardware calibration or device-independent optical observation."
    }
if __name__=="__main__":
    d=certificate()
    p=ROOT/"data/w33_20261015_toe88_adaptive_mub.json"
    p.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("MUB",d["calibrated_postnoise_EB_bound"],d["reject_at_successes_at_least"],
          d["alternative_power_under_ideal_conditional_independence"],
          d["state_dependent_heralding_attacks"][1],flush=True)
