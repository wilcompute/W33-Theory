"""A falsifiable labeled-detector 27-port hypothesis test: optimize known input.

For fully CALIBRATED 27 physical output detectors and one chosen known
input j, binary equal-prior Bayes error obeys P_err(n)<=Bhattacharyya(p,q)^n/2.
Select input j minimizing worst-case affinity across coherent detunings.
With n successes guaranteeing conditional P_err <=.025, invert independent
binomial photon survival for P(successes>=n)>=.975, so total failure
<=.05 by union bound. NOT valid for unknown detector permutations or
unmeasured coherent drift; no actual photonic device.
"""
from pathlib import Path
import sys,json,math
import numpy as np
from scipy.stats import binom
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_dual_27_electrical_transport import build_graphs
from w33_20261008_photon_likelihood_information import design
from w33_20261008_27port_correlated_coherent_drift import unitary_shared
OUT=ROOT/"data/w33_20261008_27port_known_source_95percent_Bhattacharyya_cert.json"
def threshold(n,p):
 lo=max(n,1);hi=max(n+1,int(n/p*2)+100)
 while binom.sf(n-1,hi,p)<.975:hi*=2
 while lo<hi:
  mid=(lo+hi)//2
  if binom.sf(n-1,mid,p)>=.975:hi=mid
  else:lo=mid+1
 assert binom.sf(n-1,lo,p)>=.975
 if lo>n:assert binom.sf(n-1,lo-1,p)<.975
 return lo
def main():
 graphs=build_graphs();names=sorted(graphs)
 offsets=(-.002,-.001,0,.001,.002)
 out=[]
 for reps in (4,8,16):
  bc=np.zeros((len(offsets),27))
  for k,delta in enumerate(offsets):
   a,b=[np.abs(unitary_shared(design[name]["nine_layer_schedule"],reps,delta))**2 for name in names]
   assert max(np.max(abs(x.sum(axis=0)-1)) for x in (a,b))<1e-10
   bc[k]=np.sum(np.sqrt(np.maximum(a*b,0)),axis=0)
  worst=bc.max(axis=0)
  best=int(np.argmin(worst));B=float(worst[best])
  assert 0<B<1 and np.all(bc[:,best]<=B+1e-12)
  n=math.ceil(math.log(.05)/math.log(B))
  assert .5*B**n<=.025
  eta=.99**(9*reps);N=threshold(n,eta)
  out.append({"layers":9*reps,"input_port_optimal_for_minimax_calibrated_detuning":best,
    "worst_case_Bhattacharyya_affinity":B,
    "N_successful_detections_for_conditional_binary_Bayes_error_leq_point025":n,
    "minimal_launched_photons_for_detection_count_probability_geq_point975":N,
    "binomial_success_probability":float(binom.sf(n-1,N,eta)),
    "binomial_previous_N_minus_one":float(binom.sf(n-1,N-1,eta)),
    "survival_per_photon":eta,
    "all_27_input_port_worst_affinities":[float(x) for x in worst],
    "optimal_input_Bhattacharyya_affinity_for_each_detuning":[float(x) for x in bc[:,best]],
    "source_is_known_detector_channels_labeled":True,
    "binary_equal_prior_Bayes_error_bound":.5*B**n})
 bestoverall=min(out,key=lambda v:v["minimal_launched_photons_for_detection_count_probability_geq_point975"])
 return {"hypotheses":names,"coherent_detuning_grid_radians":list(offsets),
  "experiments":out,"best_stages_in_tested_models":bestoverall["layers"],
  "guarantee":"At fixed device-calibrated known common detuning from grid, known input and labeled detector modes, equal prior binary ML error <= .025 conditional n detected photons; binomial probability n successes from N launches >= .975, total misclassification-or-insufficient-survival probability <= .05 by union bound.",
  "NOT_anonymous_input_or_output_port_protocol":True,
  "unmeasured_device_or_adversarial_jitter_guaranteed":False,
  "no_physical_experiment_conducted":True}
if __name__=="__main__":
 x=main();OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
 for r in x["experiments"]:
  print("layers",r["layers"],"source",r["input_port_optimal_for_minimax_calibrated_detuning"],"BC",round(r["worst_case_Bhattacharyya_affinity"],7),"successes",r["N_successful_detections_for_conditional_binary_Bayes_error_leq_point025"],"launches",r["minimal_launched_photons_for_detection_count_probability_geq_point975"],flush=True)
 print("PHOTON_CALIBRATED_BHATTACHARYYA_95_PASS")
