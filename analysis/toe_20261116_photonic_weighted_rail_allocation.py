#!/usr/bin/env python3
"""Optimal targeted detector-contrast calibration allocation.

Suppose the actual 16-rail distribution p has independently certified
coordinatewise bounds p_j<=u_j. For fixed simultaneous Hoeffding budget
alphaC, weight range R, and target aggregate contrast radius e, minimize
total accepted calibration shots across 16 input rails:
    sum_j u_j R sqrt(log(32/alphaC)/(2 n_j)) <= e.
The CONTINUOUS minimizer is n_j proportional to (u_j R)^(2/3),
and integer ceiling retains a valid bound. This can beat equal
calibration allocation when u is sparse, but u MUST be certified;
nominal GHZ preparation alone does not prove it.
"""
from pathlib import Path
import math,json
ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/"data"/"toe_20261115_direct_witness_contrast_calibration.json"
OUT=ROOT/"data"/"toe_20261116_photonic_occupancy_weighted_calibration.json"

def optimize(u,R,eps,alpha):
    assert len(u)==16 and all(x>=0 for x in u) and sum(u)>=1
    k=math.log(2*16/alpha)/2
    s=sum((x*R)**(2/3) for x in u if x)
    ns=[math.ceil((k*s*s/(eps*eps))*(x*R)**(2/3)) if x>0 else 0 for x in u]
    assert all((n>0)==(x>0) for x,n in zip(u,ns))
    bias=sum(x*R*math.sqrt(k/n) for x,n in zip(u,ns) if x)
    assert bias<=eps*(1+1e-12)
    continuous_n_total=k*s**3/(eps*eps)
    assert sum(ns)>=continuous_n_total
    return dict(
       certified_upper_envelope_u=u,
       sum_upper_envelope=sum(u),
       accepted_shots_by_prepared_rail=ns,
       accepted_total_rail_calibration=sum(ns),
       continuous_lower_bound_accepted_rail_shots=continuous_n_total,
       aggregate_contrast_calibration_radius=bias,
       optimizer="n_j=ceil[(log(32/alpha)/(2 eps^2))*(sum_k (u_k R)^(2/3))^2*(u_j R)^(2/3)]",
       fixed_union_failure_budget=alpha
    )

def run():
    old=json.loads(OLD.read_text())
    R=float(old["sample_weight_range"]); eps=.01;alpha=.0025
    equal_shots=16*math.ceil(R*R*math.log(32/alpha)/(2*eps**2))
    assert equal_shots==842272
    design=optimize([.5]+[.005]*14+[.5],R,eps,alpha)
    assert design["accepted_total_rail_calibration"]==244874
    uniform=optimize([F:=1/16]*16,R,eps,alpha)
    assert uniform["accepted_total_rail_calibration"]==842272
    exact2=optimize([.5]+[0.0]*14+[.5],R,eps,alpha)
    assert exact2["accepted_total_rail_calibration"]==105284
    # Three distinct upper-envelope cases separate what follows from
    # a certified sparse population from a merely hoped-for sparse one.
    pop=[.48]+[.04/14]*14+[.48]
    assert all(x<=u for x,u in zip(pop,design["certified_upper_envelope_u"]))
    synthetic_D=.002
    nominal_D_bound=synthetic_D*sum(design["certified_upper_envelope_u"])
    total_Z_contrast_bias=nominal_D_bound+design["aggregate_contrast_calibration_radius"]
    Fhat=old["observed_synthetic_witness_fidelity"]
    sig=old["statistical_half_width"]
    parity=old["parity_flip_error_radius"]/(1-sum(old["parity_flip_estimates"]))
    conditional_99_lower=Fhat-sig-.5*total_Z_contrast_bias-parity
    assert .91<conditional_99_lower<.93
    result={
      "status":"EXACT_CONDITIONAL_OPTIMAL_WEIGHTED_CONTRAST_SHOT_ALLOCATION",
      "source_R":R,"Hoeffding_alphaC":alpha,
      "target_aggregate_contrast_radius":eps,
      "previous_equal16_accepted_rail_calibrations":equal_shots,
      "illustrative_independently_certified_envelope":design,
      "uniform_occupancy_with_exact_upper_bounds_control":uniform,
      "exact_two_rail_occupancy_control":exact2,
      "percent_saving_vs_equal16_for_illustrative_certified_envelope":
         100*(1-design["accepted_total_rail_calibration"]/equal_shots),
      "illustrative_population":[float(x) for x in pop],
      "all_population_entries_bounded_by_u":True,
      "illustrative_max_absolute_rail_anchor_nominal_mismatch":synthetic_D,
      "conditional_total_Z_observable_bias_bound":total_Z_contrast_bias,
      "accepted_parity_references_preserved":2*old["accepted_parity_calibrations_each"],
      "conditional_total_calibration_with_parity":design["accepted_total_rail_calibration"]+2*old["accepted_parity_calibrations_each"],
      "conditional_synthetic_99pct_witness_fidelity_lower":conditional_99_lower,
      "scope":"The minimizer is exact for the fixed alphaC, R and prescribed coordinatewise occupancy upper envelope u. The u_j bounds must be independently validated; without them use worst-case max_j contrast calibration instead. All values are accepted SHOTS, not actual data; the 99% fidelity threshold is a conditional re-evaluation of the prior synthetic Fhat, preserving prior statistic and parity allocations. No claim of optimal allocation over time or arbitrary unknown input populations."
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    return result
if __name__=="__main__":
    r=run()
    print("PASS",r["status"],"rail shots",r["illustrative_independently_certified_envelope"]["accepted_total_rail_calibration"],flush=True)
