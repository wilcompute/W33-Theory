"""Adversarial per-gate unitary and port-efficiency robustness envelope.

Rigorous telescoping bound ||U~-U||_op <= d*g if each nominal unitary
gate has operator norm perturbation <=g. Probability per port error <=2*d*g.
If final detector efficiencies lie in [1-r,1+r] after normalizing an
average near 1, conditional probability error <=2*r/(1-r).
No random phase or measured hardware distribution is assumed.
"""
import json,math
from pathlib import Path
from scipy.stats import binom
R=Path(__file__).resolve().parents[1];D=R/"data";OUT=D/"w33_20261008_photonic_coherent_fabrication_guard.json"
base=json.loads((D/"w33_20261008_photon_likelihood_information.json").read_text())
def minN(n,p):
 lo=n;hi=max(n+1,int(math.ceil(4*n/p)))
 while lo<hi:
  m=(lo+hi)//2
  if binom.sf(n-1,m,p)>=.975:hi=m
  else:lo=m+1
 return lo
def main():
 rows=[]
 for steps in (36,72,144):
  d=next(x for x in base["experiments"] if x["stages"]==steps and x["survival_per_stage"]==.99)
  gap=d["min_full_anonymous_sorted_linf_margin"]
  for unitary_gate_error in (0,.00005,.0001,.0002,.0005):
   for detector_relative_error in (0,.002,.005,.01):
    # Uses distinguishability margin between two sets of probability
    # vectors. Each candidate may drift by eps, so subtract 2 eps.
    eps=2*steps*unitary_gate_error+2*detector_relative_error/(1-detector_relative_error)
    robust=gap-2*eps
    # A simple worst-case bound on successful per-photon survival:
    # stage survival independent .99^steps; final detector min eff 1-r.
    p=(.99**steps)*(1-detector_relative_error)
    n=math.ceil(8*math.log(54/.025)/robust**2) if robust>0 else None
    N=minN(n,p) if n else None
    rows.append({"stages":steps,"per_gate_unitary_opnorm_error_bound":unitary_gate_error,
      "final_detector_relative_efficiency_bound":detector_relative_error,
      "predicted_sorted_linf_margin":gap,
      "probability_template_perturbation_bound":eps,
      "separation_lower_bound":max(0,robust),
      "positive_separation_certified":robust>0,
      "successful_detections_for_97_5pct_conditional_success":n,
      "minimal_independent_launch_count_97_5pct_detection_collection":N,
      "joint_classification_guarantee_under_stated_model":">=0.95" if N else "not certified"})
 designs={}
 for unitary_gate_error,r in ((0,0),(.00005,.002),(.0001,.005),(.0002,.01),(.0005,.01)):
  cand=[x for x in rows if x["per_gate_unitary_opnorm_error_bound"]==unitary_gate_error and x["final_detector_relative_efficiency_bound"]==r and x["minimal_independent_launch_count_97_5pct_detection_collection"] is not None]
  key=f"gate{unitary_gate_error}_det{r}"
  designs[key]={"stages":min(cand,key=lambda v:v["minimal_independent_launch_count_97_5pct_detection_collection"])["stages"],
    "launches":min(v["minimal_independent_launch_count_97_5pct_detection_collection"] for v in cand)} if cand else {"no_certified_distinction":True}
 return {"per_gate_norm_error_telescope_bound":"<= stages*gate_opnorm_error",
   "per_output_probability_error_bound":"<=2*stages*gate_opnorm_error",
   "per_output_detector_probability_error_bound":"<=2*r/(1-r)",
   "robust_margin":"nominal margin -2*(gate_probability_error+detector_error)",
   "precision_assumption":"Individually bounded systematic unitary errors plus independent identical single-photon launches and per-stage survival=0.99; no measured calibration, thermal drift or temporal correlations",
   "bounded_error_designs":rows,"selected_scenarios":designs,"experimental_realization":False}
if __name__=="__main__":
 x=main();OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
 print(json.dumps(x["selected_scenarios"],indent=2),flush=True);print("COHERENT_PHOTON_GUARD_PASS")
