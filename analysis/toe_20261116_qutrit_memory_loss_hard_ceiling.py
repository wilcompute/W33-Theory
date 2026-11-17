"""Qutrit memory/detector loss: fundamental event-ready efficiency feasibility.

This is an OPTIMISTIC necessary-condition analysis: memory noise and
dark counts are omitted, so failure is a rigorous no-go for this specific
four-MUB gross heralded match witness under the stated device model.
An independently pre-heralded sample includes all no-click trials.

Source q(v,phase) is from committed four-MUB isotropic qutrit model.
Physical memory efficiency is separate from memory fidelity, per 2026
11-channel rare-earth integrated random-access quantum memory paper.
"""
import json,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261116_qutrit_eventready_timetag_sequential import plan
OUT=ROOT/"data"/"toe_20261116_qutrit_memory_loss_necessary_witness_budget.json"

def case(eta_memory_each=.8,number_memories=1,path=.95,f=.95):
    if number_memories not in (0,1,2):raise ValueError("0,1,2 memory arms only")
    if not all(0<=v<=1 for v in (eta_memory_each,path,f)):
        raise ValueError("efficiencies in [0,1]")
    src=plan(fR=1,fS=1,etaMem=1,etaPath=1,dark=0)
    q=src["ideal_matched_probability_given_pair"]
    p0=src["separable_null_upper"]
    detector_pair=.9**2
    mem=eta_memory_each**number_memories
    optical=detector_pair*mem*path
    max_success=optical*q
    require_product=p0/max_success if max_success else math.inf
    equal_f_min=math.sqrt(require_product)
    p_observed=max_success*f*f
    if p_observed>p0:
        D=p_observed*math.log(p_observed/p0)+(1-p_observed)*math.log((1-p_observed)/(1-p0))
        gross_n=math.log(100)/D
    else:
        gross_n=None
    return {"memory_efficiency_per_arm":eta_memory_each,
      "memory_count":number_memories,"path_throughput":path,
      "equal_router_efficiency":f,
      "mean_ideal_match_conditioned_two_click":q,
      "trusted_separable_threshold":p0,
      "maximum_gross_match_with_perfect_routers":max_success,
      "required_equal_router_efficiency":equal_f_min,
      "physically_possible_below_or_equal_100_percent_routers":equal_f_min<=1,
      "predicted_gross_match":p_observed,
      "asymptotically_violates_with_chosen_routers":p_observed>p0,
      "gross_heralded_trials_ideal_KL_mean_evalue_100":gross_n}

def verify():
    scenarios=[
      case(eta_memory_each=.8,number_memories=1,path=1,f=.95),
      case(eta_memory_each=.8,number_memories=1,path=1,f=.99),
      case(eta_memory_each=.8,number_memories=1,path=.95,f=1),
      case(eta_memory_each=.8,number_memories=2,path=1,f=1),
      case(eta_memory_each=.95,number_memories=1,path=.95,f=.95),
      case(eta_memory_each=.95,number_memories=2,path=.95,f=.95),
    ]
    one=scenarios[0];two=scenarios[2];both=scenarios[3]
    assert not one["asymptotically_violates_with_chosen_routers"]
    assert scenarios[1]["asymptotically_violates_with_chosen_routers"]
    assert not two["physically_possible_below_or_equal_100_percent_routers"]
    assert not both["physically_possible_below_or_equal_100_percent_routers"]
    assert scenarios[4]["asymptotically_violates_with_chosen_routers"]
    assert scenarios[5]["asymptotically_violates_with_chosen_routers"]
    return {"status":"PASS_QUTRIT_MEMORY_LOSS_EVENTREADY_NECESSARY_CONDITIONS",
      "null":"For trusted, independently selected 4 MUB settings, separable states have gross heralded match <=0.5+epsilon=.51, with no-click ->0.",
      "conditional_q":"Source v=0.75, sigma_phase=0.15 radians, detector per arm 0.9; q fixed to committed model",
      "necessary_feasibility_bound":"(eta_detector_R*eta_detector_S)*(eta_memory_per_arm)^n*(eta_path)*q > 0.51; if this fails, no routers of efficiency <=1 can violate this gross witness.",
      "example_scenarios":scenarios,
      "not_observed_hardware":True,
      "fidelity_vs_efficiency":"Reported conditional fidelity of stored/retrieved states is NOT storage and retrieval probability. Their product separately determines whether any heralded result registers.",
      "2026_memory_hardware_reference":"Random access and high dimensional integrated quantum memory (2026), 11-channel 151Eu:Y2SiO5; high conditional qubit/path fidelity, not an asserted 80% measured memory throughput; https://link.springer.com/article/10.1186/s43074-026-00284-w",
      "calibration_caveat":"Optimistic no-dark/no-misrouting upper bound; any real memory decoherence, basis-dependent detector errors and false triggers reduce measured witness further. This is NOT a device-independent loophole-free Bell test."}
if __name__=="__main__":
    r=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(r["status"])
    for row in r["example_scenarios"]:
        print(row["memory_count"],row["memory_efficiency_per_arm"],row["path_throughput"],row["equal_router_efficiency"],
             "max=",round(row["maximum_gross_match_with_perfect_routers"],6),
             "fmin=",round(row["required_equal_router_efficiency"],5),
             "pass=",row["asymptotically_violates_with_chosen_routers"])
