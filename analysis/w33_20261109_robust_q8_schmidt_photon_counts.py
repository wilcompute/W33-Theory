#!/usr/bin/env python3
"""Calibrated eight-Q8-MUB mixed Schmidt number witness, finite accepted pairs.

Assumptions: each of 8 settings yields exactly nine complete accepted
outcomes; uniform classical depolarizing mislabeling r in [rmin,rmax],
and independent verified per-outcome residual |qactual-qbase|<=eps.
Accepted-pair collision Hoeffding is IID. Postselection is INVALID if
detection efficiency depends on measurement outcome. All source
preparations for lost pairs count in expected launch cost.
"""
import json,sys,math
from pathlib import Path
import numpy as np
from w33_20261109_q8_schmidt_witness import families,schmidt_state,probabilities,collision
from scipy.stats import binom

def centered(P):
    return float(sum(np.dot(q,q) for q in P)-8/9)
def deterministic_budget(Fq,rmin,epsilon,threshold,alpha=.05,power=.95):
    floor=72*epsilon
    target=(1-rmin)**2*threshold + floor
    margin=Fq-target
    if margin<=0:return {"feasible":False,"margin":margin}
    # One-sided Hoeffding alpha threshold. A second same radius
    # ensures >=1-power probability under the specified IID model.
    A=math.sqrt(4*math.log(1/alpha))
    B=math.sqrt(4*math.log(1/(1-power)))
    M=int(math.ceil(((A+B)/margin)**2))
    rad=A/math.sqrt(M)
    probbound=1-math.exp(-M*(margin-rad)**2/4)
    assert probbound>=power-1e-7
    return {"feasible":True,"M_accepted_pairs_per_basis":M,
       "Q8_total_accepted_pairs":8*M,
       "lower_confidence_radius_for_Fobs":rad,
       "epsilon_calibration_worst_case_72eps":floor,
       "true_expected_vs_null_gap_after_errors":margin,
       "Hoeffding_power_lower_bound":probbound}
def main(path=None):
    bases=families()[0]
    pure=schmidt_state(3)
    mix=np.eye(9)/9
    detection_eta=.85
    r=.01;rmin=.0095;eps=2e-5
    scenarios=[]
    for eta in (.65,.8,.94,.95,.99):
        rho=eta*pure+(1-eta)*mix
        Ps=[probabilities(E,rho) for E in bases]
        ideal=centered(Ps)
        closed=8*eta*eta/9
        assert abs(ideal-closed)<3e-12
        Qs=[(1-r)*p+r*np.ones(9)/9 for p in Ps]
        measured=centered(Qs)
        assert abs(measured-(1-r)**2*ideal)<3e-12
        cases=[]
        for k,threshold in ((1,4/9),(2,7/9)):
            budget=deterministic_budget(measured,rmin,eps,threshold)
            if budget.get("feasible"):
                budget["expected_launched_signal_photons_if_pair_detection_independent"]=float(
                    2*8*budget["M_accepted_pairs_per_basis"]/detection_eta**2)
            cases.append({"certified_Schmidt_number_at_least":k+1,"null_SN_leq":k,
                          "threshold":threshold,"budget":budget})
        scenarios.append({"isotropic_eta":eta,
             "ideal_F8":ideal,
             "uniform_mislabel_r":r,
             "observed_F8_after_known_response":measured,
             "rank_witnesses":cases})
    # Calibration drift proof: for complete probability vectors p,q,
    # |sum p² -sum q²|≤||p-q||_1, as sum(p-q)=0.
    rng=np.random.default_rng(20261109)
    maxratio=0
    for i in range(2000):
        p=rng.dirichlet(np.ones(9)*.5)
        q=rng.dirichlet(np.ones(9)*.5)
        l1=np.linalg.norm(p-q,ord=1)
        ratio=abs(p@p-q@q)/l1
        assert ratio<=1+1e-12
        maxratio=max(maxratio,ratio)
    # Real-world alternative: detection efficiency depends on outcome;
    # the conditional accepted distribution is reweighted and the model
    # above is invalid without separately verified calibration.
    bad=Ps[0]
    ej=np.array([.64+.04*j for j in range(9)])
    bad_post=bad*ej/(bad@ej)
    tv=float(np.linalg.norm(bad_post-bad,ord=1))
    assert tv>eps*9
    result={"status":"PASS_Q8_SCHMIDT_WITNESS_MIXED_FINITE_SHOTS_CALIBRATED_READOUT",
      "readout":"8 MUB bases per coset, each has 9 COMPLETE mutually exclusive accepted outcomes",
      "calibration_model":"Independent uniform classical outcome mislabel r=0.01 with certified r in [.0095, .0105]; residual absolute per-outcome difference <=2e-5 relative to this response in each basis and any state (not measured here). Outcome-independent detected-pair survival eta=0.85. These are hypothetical stipulated controls, not proven detector calibrations.",
      "rigorous_L1_lipschitz":"For two complete probability distributions p,q, |sum_j p_j²-sum_j q_j²|≤||p-q||_1. For eight bases with 9 effects and independently bounded |qactual_bj-qbase_bj|≤eps, the bias |F8(qactual)-F8(qbase)|≤72eps. Under uniform mislabel F8(qbase)=(1-r)^2 F8(ideal).",
      "finite_sampling":"Each accepted pair in a fixed basis gives one Bernoulli match of two independent source preparations. M accepted pairs per basis in 8 bases, with separate independent calibration. Hoeffding: Pr(Fhat8-F8>=z)≤exp(-M z²/4). Two such tails give a conservative 95%-size and >=95%-power threshold using alpha=.05 and beta=.05 under the specified IID alternative.",
      "null_thresholds":{"separable_SN1":4/9,"Schmidt_leq2":7/9},
      "parameters":{"hypothetical_detector_efficiency":detection_eta,"uniform_response_r_true":r,
          "certified_response_r_min":rmin,"certified_response_r_max":.0105,
          "independent_per_outcome_residual_bound_eps":eps,
          "source_photons_per_successful_pair_expected_if_uniform_losses":2/detection_eta**2},
      "results":scenarios,
      "simulated_simplex_L1_bound_random_controls":2000,
      "largest_observed_ratio_collision_over_l1":maxratio,
      "outcome_dependent_detector_postselection_attack_l1_shift":tv,
      "outcome_dependent_attack_exceeds_certified_max_l1":bool(tv>9*eps),
      "scope":"Purely conditional finite-shot *theoretical* certificate, not live measured calibration or PPT state certification. Schmidt-number proof and Q8 2-design identities are prior repo results. This extension explicitly carries hypothetical readout drift and complete source launch count. Lost events depending on outcome, detector efficiency correlations, heralding loopholes and source-model errors invalidate the bound. For isotropic states the witness is weaker than aligned fidelity tests.",
      "prior_art":["https://doi.org/10.1038/s41534-025-00990-6",
        "https://doi.org/10.1103/PhysRevA.109.062417"]}
    if path:Path(path).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("ROBUST_SCHMIDT",json.dumps({"eta":[(x["isotropic_eta"],[
      (y["null_SN_leq"],y["budget"].get("M_accepted_pairs_per_basis"))
      for y in x["rank_witnesses"]]) for x in scenarios],"attack_tv":tv}))
    return result
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
