#!/usr/bin/env python3
"""Robust and honest single-source photon classifier budgets.

Uniform dark-count mixing admits an exact margin rescaling. Arbitrary
calibration drift bounded by epsilon per observed conditional probability
reduces the *nominal* binary margin by at most 2epsilon. The design
is conditional on n successful detections; launches are expectation only.
"""
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];D=ROOT/"data"
OUT=D/"w33_20261008_photon_robust_decision_guards.json"

def build():
 src=json.loads((D/"w33_20261008_photon_likelihood_information.json").read_text())
 H=math.log(2*27/.05)
 rows=[]
 for stage in (36,72,144):
  r=next(x for x in src["experiments"] if x["stages"]==stage and x["survival_per_stage"]==.99)
  delta=r["min_full_anonymous_sorted_linf_margin"]
  for dark in (0,.01,.05,.10,.20):
   for systematic in (0,.005,.01,.02,.05):
    observed=(1-dark)*delta
    effective=observed-2*systematic
    valid=effective>0
    n=math.ceil(8*H/effective**2) if valid else None
    launched=math.ceil(n/.99**stage) if valid else None
    rows.append({"stages":stage,"per_layer_survival":.99,
                 "uniform_conditional_dark_count_fraction":dark,
                 "bounded_adversarial_conditional_probability_error_each_hypothesis":systematic,
                 "nominal_sorted_linf_margin":delta,
                 "provable_observed_cross_class_margin_lower_bound":max(0,effective),
                 "guarantee_applicable":valid,
                 "successful_detections_sufficient_for_95pct":n,
                 "expected_launches_under_independent_loss":launched})
 opt={}
 for dark in (0,.01,.05,.10,.20):
  for system in (0,.005,.01,.02,.05):
   available=[x for x in rows if x["uniform_conditional_dark_count_fraction"]==dark
              and x["bounded_adversarial_conditional_probability_error_each_hypothesis"]==system
              and x["guarantee_applicable"]]
   opt[f"dark{dark}_sys{system}"]=(
     {"best_stages":min(available,key=lambda x:x["expected_launches_under_independent_loss"])["stages"],
      "min_expected_launches":min(x["expected_launches_under_independent_loss"] for x in available)}
     if available else {"infeasible_for_tested_stages":True})
 assert opt["dark0_sys0"]["best_stages"]==72
 return {"model":"sorted source-port and detector-permutation-invariant binary classification under uniform dark-count mixing and arbitrary bounded per-outcome calibration errors",
         "guarantee_definition":"With n independent successful detections, nominal class-set margin Delta>2epsilon, Hoeffding ensures >=95% correct using exact baseline templates. Expected launches n/eta^depth only, not a guaranteed number of launches.",
         "assumptions":"Calibration difference is bounded in infinity norm for both candidate distributions and uniform dark background known; coherent correlations and unknown error bounds excluded",
         "guarded_rows":rows,"optimal_among_three_tested_depths":opt,
         "hardware_realized":False}

if __name__=="__main__":
 x=build();OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
 for k in ("dark0_sys0","dark0.05_sys0.01","dark0.1_sys0.02","dark0.2_sys0.05"):print(k,x["optimal_among_three_tested_depths"][k],flush=True)
 print("PHOTON_ROBUST_PASS",flush=True)
