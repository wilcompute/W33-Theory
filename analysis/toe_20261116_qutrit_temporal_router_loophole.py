"""Two-analyzer time-bin routing budget and fair-sampling loophole control.

Previous code implements arbitrary U(3) using three 2-mode couplers in
a simultaneous three-SPATIAL-mode network. That DOES NOT, by itself,
implement a deterministic three-TIME-BIN measurement. A coherent
time-to-space demultiplexer, optical buffer/delay, or equivalent
programmable temporal-mode device is REQUIRED and adds loss.

For event-ready 4-MUB witness, p0=.5+eps+settingLeakageTV,
q(v,sigma)=(1+3F)/4 with
F=v(1+2exp(-sigma^2))/3+(1-v)/9.
Gross clicks η=η_R η_S η_mem η_path f_R f_S.
Requirement ηq>p0. Show numerical routing-efficiency threshold.

A setting-dependent, postselected coincidence 'herald' can falsely
show 100% correlations from a fully separable computational state.
Counting all independent prebasis heralds avoids this artifact.
"""
import math,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261116_qutrit_F3_optical_budget import case as original
OUT=ROOT/"data"/"toe_20261116_qutrit_temporal_router_loophole_and_thresholds.json"

def budget(v=.75,sigma=.15,etaR=.9,etaS=.9,etaMem=.95,etaPath=.95,
           error=.01,leakage=0):
    base=original(v,sigma,etaR,etaS,etaMem,etaPath,eps=error,leak=leakage)
    q=base["matched_probability_given_perfect_detection"]
    eta0=base["total_eventready_pair_detection"]
    p0=base["calibrated_separable_null_p0"]
    routing_equal=math.sqrt(p0/(q*eta0))
    cases=[]
    for f in (1,.95,.92,.90,.75,.70,.50,1/3):
        eta=eta0*f*f
        measured=eta*q
        cases.append({"temporal_demultiplexer_efficiency_each_analyzer":f,
                      "gross_heralded_pair_detection_efficiency":eta,
                      "gross_random_MUB_match":measured,
                      "witness_asymptotically_detectable":measured>p0})
    assert cases[0]["witness_asymptotically_detectable"]
    assert not cases[-1]["witness_asymptotically_detectable"]
    assert .9<routing_equal<.95
    minv= (6*(p0/eta0-1/3))/(1+3*math.exp(-sigma*sigma))
    return {"source_visibility":v,"phase_sigma":sigma,
        "ideal_match_q":q,"gross_efficiency_without_temporal_routing":eta0,
        "separable_null_p0":p0,
        "minimum_equal_side_temporal_routing_efficiency":routing_equal,
        "minimum_source_visibility_no_extra_router":minv,
        "sweep":cases}

def fake_coincidence_test():
    # Separable two-qutrit computational-basis state |0>|0>.
    # In the Z basis both matched outcomes are certain, in any of
    # the three other MUBs they match with probability 1/3.
    probs=[1.,1/3,1/3,1/3]
    p0=sum(probs)/4
    # Malicious 'herald' issued only when setting=Z after basis choice.
    # Conditional on this selection P(match)=1. Yet counting every
    # genuine pre-basis prepared trial with no-click 0 gives 1/4.
    postselect=[1,0,0,0]
    accepted=sum(r for r in postselect)/4
    joined=sum(p*r for p,r in zip(probs,postselect))/4
    assert abs(p0-.5)<1e-12
    assert abs(accepted-.25)<1e-12
    assert joined/accepted==1.
    assert joined<=.5
    return {"separable_source":"|0>_R tensor |0>_S",
        "matched_probabilities_by_four_MUB":probs,
        "unconditioned_four_basis_average":p0,
        "basis_dependent_acceptance":[1,0,0,0],
        "postselected_coincidence_matching":1.,
        "valid_eventready_all_trial_matching":joined,
        "false_positive_if_acceptance_defined_after_basis":True}

def verify():
    a=budget()
    b=fake_coincidence_test()
    assert not next(x for x in a["sweep"] if x["temporal_demultiplexer_efficiency_each_analyzer"]==.9)["witness_asymptotically_detectable"]
    return {"status":"PASS_QUTRIT_TEMPORAL_DEMULTIPLEXER_AND_POSTSELECTION_NO_GO",
       "temporal_mode_no_go":"A spatial 3x3 Reck decomposition is not alone a physical deterministic 3-time-bin unitary. The coherent time-to-spatial routing and inverse, optical buffer, and routing efficiencies must be included.",
       "trusted_device_noise_budget":a,
       "postselection_control":b,
       "hardware_path":"Event-ready pair-source herald before setting draw; route each time-bin coherently into parallel spatial rails; three-mode Fourier multiport with D_b phase; detect all 3 outputs; record all no-click outcomes; calibration and phase feedforward; analyze with predeclared four-MUB e-process.",
       "references":["arXiv:2601.14565 temporal-mode arbitrary 11-dimensional projection","Nature Communications 2024 d4 time-bin implementation central-bin selection","Light Science Applications 2026 multi-level temporal-interferometer losses"],
       "no_hardware_claim":True}
if __name__=="__main__":
    r=verify()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(r["status"],r["trusted_device_noise_budget"]["minimum_equal_side_temporal_routing_efficiency"])
