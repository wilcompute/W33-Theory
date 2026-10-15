"""TOE87: adversarially audited qutrit temporal-channel witness.

The original single-superposition test is not sound against arbitrary
entanglement-breaking channels. An explicit adversarial null passes with
certainty. A complete four-MUB qutrit 2-design repairs that null class
under a trusted-input/output fair-sampling protocol.
"""
from __future__ import annotations
import json
import numpy as np
from scipy.stats import binom
from analysis.w33_20261015_toe85_h2_relation_module import ROOT

D=3
W=np.exp(2j*np.pi/3)
def states():
    # The computational basis + 3 quadratic Fourier bases are all MUB.
    out=[]
    for j in range(3):
        psi=np.eye(3,dtype=complex)[:,j]
        out.append(("Z",j,psi))
    for b in range(3):
        for a in range(3):
            psi=np.array([W**((b*x*x+a*x)%3) for x in range(3)],complex)/np.sqrt(3)
            out.append((f"Q{b}",a,psi))
    assert len(out)==12
    for i,(_,_,u) in enumerate(out):
        for j,(_,_,v) in enumerate(out):
            ip=abs(np.vdot(u,v))**2
            same=(i//3)==(j//3)
            expected=float(i==j) if same else 1/3
            assert abs(ip-expected)<1e-12,(i,j,ip,expected)
    twirl=sum(np.kron(np.outer(u,u.conj()),np.outer(u,u.conj())) for _,_,u in out)/12
    flip=np.zeros((9,9),complex)
    for i in range(3):
        for j in range(3): flip[i*3+j,j*3+i]=1
    assert np.allclose(twirl,(np.eye(9)+flip)/12)
    return out,twirl

def dephasing(psi,basis):
    rho=np.outer(psi,psi.conj())
    return sum(np.outer(u,u.conj())@rho@np.outer(u,u.conj()) for u in basis)

def success(psi,basis,v):
    rho=np.outer(psi,psi.conj())
    final=v*rho+(1-v)*dephasing(psi,basis)
    return float(np.real(np.vdot(psi,final@psi)))

def confusion(p,e=0.02,leak=0.03):
    # symmetric trusted readout confusion and independently calibrated
    # random replacement due to qutrit subspace leakage.
    return (1-leak)*((1-e)*p+e/2*(1-p))+leak/3

def test_design():
    S,twirl=states()
    clock=[t[2] for t in S[3:6]] # Q0 clock MUB, eigenspace of X
    comp=[t[2] for t in S[:3]]
    probe=comp[0] # equal superposition of Q0 clock eigenstates
    p_clock_null=success(probe,clock,0)
    p_adversarial=success(probe,comp,0)
    assert abs(p_clock_null-1/3)<1e-12
    assert abs(p_adversarial-1)<1e-12
    # Arbitrary EB channel has average fidelity <= 2/(d+1)=1/2
    # for a complete projective 2-design of input states with
    # matched output projectors (Choi overlap with maximally
    # entangled ket <=1/3 for any separable Choi state).
    means={}
    for label,basis in (("clock_EB",clock),("rotated_EB",comp)):
        means[label]=sum(success(t[2],basis,0) for t in S)/12
        assert abs(means[label]-0.5)<1e-12
    v=.25
    means["coherent_v025"]=sum(success(t[2],clock,v) for t in S)/12
    assert abs(means["coherent_v025"]-0.625)<1e-12
    error=.02;leak=.03;erasure=.08
    null=confusion(.5,error,leak)
    alternative=confusion(.625,error,leak)
    assert alternative>null
    # Randomize the setting independently on every accepted shot.
    # This makes Bernoulli/binomial tails applicable, unlike fixing
    # exactly n/12 shots per setting (which is Poisson-binomial).
    accepted=1200
    alpha=.001
    threshold=next(k for k in range(accepted+1)
                   if binom.sf(k-1,accepted,null)<=alpha)
    fp=float(binom.sf(threshold-1,accepted,null))
    power=float(binom.sf(threshold-1,accepted,alternative))
    assert fp<=alpha and power>.95
    target_2design=np.eye(9,dtype=complex)
    for i in range(3):
        for j in range(3):target_2design[i*3+j,j*3+i]+=1
    target_2design/=12
    return {
        "four_MUB_two_design_states":12,
        "two_design_residual_max_abs":float(np.max(abs(twirl-target_2design))),
        "entanglement_breaking_mean_fidelity_upper_bound":.5,
        "explicit_adversarial_single_probe_EB_success":p_adversarial,
        "single_probe_clock_dephasing_EB_success":p_clock_null,
        "multiple_probe_mean_fidelities":means,
        "ideal_channel_coherence_visibility":v,
        "readout_sym_wrong_class_rate":error,
        "random_leakage_rate":leak,
        "independent_heralded_erasure_rate":erasure,
        "calibrated_detected_shot_EB_upper_bound":null,
        "calibrated_detected_shot_alternative_expectation":alternative,
        "random_uniform_MUB_settings_per_shot":True,
        "accepted_shots":accepted,
        "expected_raw_attempts_for_accepted_shots":accepted/(1-erasure),
        "reject_EB_at_success_count_at_least":threshold,
        "exact_max_null_false_positive_probability":fp,
        "exact_alternative_power":power,
        "robustness_boundaries":{
           "trusted_state_preparations":True,
           "trusted_state_matched_measurements":True,
           "stationary_iid":True,
           "state_independent_erasure":True,
           "independently_calibrated_readout_confusion":True,
           "no_adversarial_correlated_SPAM":True,
           "no_device_independence":True,
           "no_non_markovianity_claim":True,
           "no_time_arrow_claim":True
        },
        "critical_observation":"A rotated-basis entanglement-breaking channel defeats TOE86's one-probe return test with success 1, while all EB channels obey the four-MUB mean fidelity <= 1/2 under stated assumptions."
    }

if __name__=="__main__":
    d=test_design()
    p=ROOT/"data/w33_20261015_toe87_adversarial_temporal.json"
    p.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("TIME",d["multiple_probe_mean_fidelities"],
          "single-probe spoof",d["explicit_adversarial_single_probe_EB_success"],
          "threshold",d["reject_EB_at_success_count_at_least"],
          "power",d["exact_alternative_power"],flush=True)
