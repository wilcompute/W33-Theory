"""Continuous coherent detuning interval certification for known-input
27port photon discrimination. Previous model only checks five detuning
grid points. For each optical layer a disjoint-pair mixing unitary
U(theta+delta) obeys ||dU/d_delta||_op<=1. For L layers, ||dUtot||<=L.
Born distribution l1 error <=2L*grid_radius; continuous interval
survival-likelihood certified via Hellinger triangle, if positive.
"""
from pathlib import Path
import math,sys,json
import numpy as np
from scipy.stats import binom
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_27port_dark_TV_robust_budget import model_affinities
from w33_20261008_27port_calibrated_Bhattacharyya_test import threshold
OUT=ROOT/"data/w33_20261008_photon_continuous_detuning_dark_TV_certificates.json"
def main():
 rows=[];r=.0005
 for L in (36,72,144):
  step=L//9;p=.99**L
  for b in (0.,.05,.10):
   models=model_affinities(step,b)
   for eps in (0.,.001,.01):
    ell1=eps+2*L*r
    BC=np.minimum(1.,1.-np.maximum(0.,np.sqrt(np.maximum(0.,1-models))-math.sqrt(2*ell1))**2)
    j=int(np.argmin(BC));v=float(BC[j])
    can=v<1.
    n=math.ceil(math.log(.05)/math.log(v)) if can else None
    N=threshold(n,p) if can else None
    if can:
     assert .5*v**n<=.025 and binom.sf(n-1,N,p)>=.975
    rows.append({"layers":L,"uniform_noise_fraction":b,"independently_adversarial_l1_error":eps,
      "source_port_minimax_over_entire_continuous_detuning_interval":j,
      "total_per_hypothesis_l1_uncertainty_bound":ell1,
      "worst_continuous_interval_Bhattacharyya_bound":v,
      "conditional_detected_photons":n,
      "minimum_launched_photons_for_joint_95percent":N,
      "model_bound_remains_nontrivial":can})
 assert len(rows)==27
 return {"offset_interval_radians":[-.002,.002],
  "uniform_detuning_grid_spacing":.001,
  "nearest_grid_point_max_distance":r,
  "number_of_scenarios":len(rows),
  "per_layer_unitary_derivative_operator_norm_bound":1,
  "full_L_layer_unitary_derivative_bound":"L",
  "born_output_distribution_l1_interpolation_bound":"2*L*0.0005",
  "Hellinger_continuous_BC_upper_bound":"1-max(0,sqrt(1-BC_grid_max)-sqrt(2*(epsilon+2*L*0.0005)))**2",
  "rows":rows,
  "device_calibration_must_establish_independent_l1_error_and_background":True,
  "not_actual_physical_device_or_unknown_source":True,
  "finite_grid_baseline_cannot_be_claimed_continuous_without_interpolation_guard":True}
if __name__=="__main__":
 r=main();OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 for x in r["rows"]:
  if x["layers"]==36:print(x,flush=True)
 print("PHOTON_CONTINUOUS_INTERVAL_HOEF_BHAT_GUARD_PASS")
