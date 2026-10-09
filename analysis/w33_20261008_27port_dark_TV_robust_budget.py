"""27-port controlled photon likelihood test under uniform dark/background
admixture and *adversarial calibration total variation* uncertainty.

Exact modeled Bhattacharyya affinity after beta-uniform mixing.
If l1(P_measured-P_model)<=eps for each of two hypotheses, then
Hellinger triangle gives:
sqrt(1-BC_true)>=max(0,sqrt(1-BC_model)-sqrt(2eps))
since H=sqrt(1-BC) and H(P,P')<=sqrt(TV)<=sqrt(eps/2).
Conditional equal-prior discrimination ≤BC_bound^n / 2;
binomial success probability P>=.975 yields joint ≥.95.
"""
from pathlib import Path
import sys,json,math
import numpy as np
from scipy.stats import binom
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_photon_likelihood_information import design
from w33_20261008_dual_27_electrical_transport import build_graphs
from w33_20261008_27port_correlated_coherent_drift import unitary_shared
from w33_20261008_27port_calibrated_Bhattacharyya_test import threshold
OUT=ROOT/"data/w33_20261008_27port_darkcounts_TV_robust_binomial_budgets.json"
def model_affinities(reps,beta):
 names=sorted(build_graphs())
 vals=[]
 for delta in (-.002,-.001,0,.001,.002):
  models=[np.abs(unitary_shared(design[name]["nine_layer_schedule"],reps,delta))**2 for name in names]
  p,q=[(1-beta)*v+beta/27 for v in models]
  assert max(np.max(abs(v.sum(axis=0)-1)) for v in (p,q))<1e-10
  vals.append(np.sum(np.sqrt(p*q),axis=0))
 return np.max(np.array(vals),axis=0)
def main():
 rows=[];epsilons=(0.,.001,.01);betas=(0.,.01,.05,.1)
 for reps in (4,8,16):
  survival=.99**(reps*9)
  for beta in betas:
   affinity=model_affinities(reps,beta)
   for eps in epsilons:
    bc=np.minimum(1.,1.-np.maximum(0,np.sqrt(np.maximum(0,1-affinity))-math.sqrt(2*eps))**2)
    best=int(np.argmin(bc));B=float(bc[best])
    assert 0<B<1
    n=math.ceil(math.log(.05)/math.log(B));N=threshold(n,survival)
    assert .5*B**n<=.025
    assert binom.sf(n-1,N,survival)>=.975
    if N>n:assert binom.sf(n-1,N-1,survival)<.975
    rows.append({"optical_layers":9*reps,"uniform_dark_background_fraction":beta,
       "maximum_l1_model_to_true_per_hypothesis":eps,
       "chosen_calibrated_known_input":best,
       "worst_Bhattacharyya_upper_bound_with_bounded_errors":B,
       "successful_photon_detections_required":n,
       "joint_95percent_minimum_source_launches":N,
       "binomial_success_probability":float(binom.sf(n-1,N,survival))})
 baseline=next(r for r in rows if r["optical_layers"]==36 and r["uniform_dark_background_fraction"]==0 and r["maximum_l1_model_to_true_per_hypothesis"]==0)
 assert baseline["joint_95percent_minimum_source_launches"]==18
 return {"number_of_model_conditional_scenarios":len(rows),"rows":rows,
  "coherent_coupler_drift_grid_rad":[-.002,-.001,0,.001,.002],
  "background_model":"uniform admixture q_i=(1-beta)p_i + beta/27",
  "calibration_norm":"l1 error of each two hypothesis output distribution <= epsilon (not TV epsilon); both distributions independently perturbed",
  "robust_affinity_formula":"BC <= 1 - max(0,sqrt(1-BC_model)-sqrt(2 epsilon))**2",
  "joint_guarantee":"Labeled known source/detectors, equal priors, independent survives and outputs; conditional likelihood error <=.025 via BC bound and >=.975 chance of n detections via exact binomial inversion. Union bound failure <=.05.",
  "only_grid_calibrated_common_detuning":True,
  "not_anonymous_port_or_any_real_device_measurement":True,
  "no_nonuniform_time_dependent_loss_or_correlated_detection":True}
if __name__=="__main__":
 v=main();OUT.write_text(json.dumps(v,indent=2,sort_keys=True)+"\n")
 for r in v["rows"]:
  if r["optical_layers"]==36:print(r,flush=True)
 print("PHOTON_BOUNDED_TV_BACKGROUND_36_SCENARIOS_PASS")
