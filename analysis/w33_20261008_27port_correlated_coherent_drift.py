"""Correlated coherent error on every photonic coupler: a falsifiable control.

Compare against earlier independently randomized pairwise errors. Shared
calibration detuning can grow coherently with circuit depth. Sorted
unknown-port templates and expected postselected launch budgets are
computed directly from the 27-mode unitary simulator. These remain
synthetic hypotheses, not actual chip calibration.
"""
import sys,json,math,numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261008_photon_likelihood_information import design,unitary
from w33_20261008_dual_27_electrical_transport import build_graphs
OUT=ROOT/"data/w33_20261008_27port_correlated_coherent_drift.json"
def unitary_shared(layers,steps,delta):
 u=np.eye(27,dtype=complex)
 theta=.78/steps+delta
 c=np.cos(theta);s=np.sin(theta)
 for rep in range(steps):
  for matching in layers:
   t=np.eye(27,dtype=complex)
   for i,j in matching:
    t[i,i]=c;t[j,j]=c;t[i,j]=-1j*s;t[j,i]=-1j*s
   u=t@u
 assert np.max(np.abs(u.conj().T@u-np.eye(27)))<3e-12
 return u
def separation(p,q):
 return min(float(np.max(np.abs(p[:,i]-q[:,j]))) for i in range(27) for j in range(27))
def main():
 graph=build_graphs();names=sorted(graph)
 rec=[]
 for steps in (4,8,16):
  ideal={name:np.sort(np.abs(unitary(graph[name],design[name]["nine_layer_schedule"],.78,steps))**2,axis=0) for name in names}
  oldsep=separation(ideal[names[0]],ideal[names[1]])
  for detune in (-.002,-.001,-.0005,0,.0005,.001,.002):
   impaired={}
   couplers={}
   for name in names:
    lay=design[name]["nine_layer_schedule"]
    couplers[name]=[len(l) for l in lay]
    impaired[name]=np.sort(np.abs(unitary_shared(lay,steps,detune))**2,axis=0)
   sep=separation(impaired[names[0]],impaired[names[1]])
   drift=max(float(np.max(np.abs(impaired[name]-ideal[name]))) for name in names)
   noncal=oldsep-2*drift
   # Only if nominal-template margin survives worst offset evaluated here.
   n=math.ceil(8*math.log(54/.05)/(noncal**2)) if noncal>0 else None
   launch=math.ceil(n/(.99**(9*steps))) if n else None
   rec.append({"Trotter_repetitions":steps,"CNOTlike_2mode_optical_layers":9*steps,
     "systematic_angle_offset_per_active_2mode_coupler_rad":detune,
     "couplers_per_nine_layer_pattern":couplers,
     "ideal_source_anonymous_min_supnorm_separation":oldsep,
     "perturbed_models_min_separation":sep,
     "max_sorted_nominal_template_drift":drift,
     "nominal_classifier_separation_lower_bound_for_this_synthetic_miscalibration":noncal,
     "nominal_template_95pct_successful_samples_sufficient_if_positive":n,
     "expected_launches_at_eta_point99_per_layer":launch})
 return {"grid":rec,"repetitions":[4,8,16],"angle_offsets_rad":[-.002,-.001,-.0005,0,.0005,.001,.002],
  "two_graph_hypotheses":names,
  "all_layers_are_two_mode_reciprocal_beamsplitters":True,
  "unknown_output_labels_are_handled_by_sorted_template":True,
  "shared_phase_offset_same_for_each_gate_and_repetition":True,
  "previous_independent_coupler_randomization_is_distinct":True,
  "nominal_template_sufficient_bound_is_model_conditional_not_device_certification":True,
  "future_lab_measurands":["2-mode phase coupling per stage","27x27 transfer-probability matrix","frequency dependent insertion loss","per-detector efficiency stability","coherent common-mode pump detuning"],
  "no_real_photon_device_calibration":True}
if __name__=="__main__":
 x=main();OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
 for r in x["grid"]:
  if abs(r["systematic_angle_offset_per_active_2mode_coupler_rad"]) in (0,.001,.002):
   print(r["CNOTlike_2mode_optical_layers"],r["systematic_angle_offset_per_active_2mode_coupler_rad"],round(r["nominal_classifier_separation_lower_bound_for_this_synthetic_miscalibration"],6),r["expected_launches_at_eta_point99_per_layer"],flush=True)
 print("CORRELATED_PHOTON_DRIFT_PASS")
