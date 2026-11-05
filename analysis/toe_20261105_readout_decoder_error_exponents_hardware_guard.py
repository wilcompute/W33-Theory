#!/usr/bin/env python3
"""Finite-shot 440-state MLE error certificate versus average mutual information.

The Bhattacharyya/Chernoff-style elementary union inequality for
known IID 440-hypothesis likelihoods:
P(ML error | label i) <= sum_(j!=i) BC(p_i,p_j)^N
                      <= 439 * (max_pair BC)^N .
This gives an actual conservative SUFFICIENT sample budget, unlike
Fano's NECESSARY lower bound. Compare full 40 Witting, optimized
4 outcome U4 basis, independent erasure eta, and uniform background.
At N incident trials with no-click, BC'=(1-eta)+eta*BC.

For state PREPARATION with at most 6 passive Givens, calibrated
absolute angle and differential-phase deviations |a|,|b|<=delta
yield ||Uactual-Uideal||op <= 6*[2sin(delta/2)+2sin(delta/4)].
Any ideal measured output TV changes by at most that amount
assuming identical input eigenmode mixing distribution and ideal
readout. A SUFFICIENT, likely loose 440-codeword separation
bound follows from 2*TV_drift_bound < minimum-pair TV.
No actual measured 0.001-radian calibration has occurred.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
from scipy.spatial.distance import pdist
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_readout_decoder_error_exponents_hardware_guard.json"
def allpairs(P):
 D=pdist(np.sqrt(P),"sqeuclidean")
 d=float(np.min(D))
 BC=1-d/2
 return BC,float(-math.log(BC))
def enough(exponent,epsilon=.05,M=440):
 if exponent<=0:return None
 return math.ceil(math.log((M-1)/epsilon)/exponent)
def rng_mle(P,N,runs,seed):
 logs=np.log(P)
 rng=np.random.default_rng(seed)
 samples=rng.integers(len(P),size=runs)
 right=0
 for truth in samples:
  counts=rng.multinomial(N,P[truth])
  best=int(np.argmax(logs@counts))
  right+=int(best==truth)
 return right/runs
def main():
 j=json.loads((ROOT/"data/toe_20261105_a5_tetrad_orbits_bhattacharyya.json").read_text())
 h=json.loads((ROOT/"data/toe_20261104_ququart_povm_local_unitary_optimizer.json").read_text())
 k=json.loads((ROOT/"data/toe_20261104_two_e8_root_to_witting_density_codebook.json").read_text())
 g=json.loads((ROOT/"data/toe_20261104_witting_operator_dark_spectral_A5_duality.json").read_text())
 theta=np.array(k["eight_real_parameters_for_440_states"])
 E=np.array(g["A5_classes"][1]["explicit_W33_40x8_observable_coefficient_map"])
 OPS=np.array(g["A5_classes"][1]["explicit_8_Hermitian_ququart_observables_real"])+1j*np.array(g["A5_classes"][1]["explicit_8_Hermitian_ququart_observables_imag"])
 R=np.eye(4)[None,:,:]/4+np.einsum("ij,jab->iab",theta,OPS)
 full=1/40+theta@E.T/5
 winner=max(h["epsilon_results"][0]["local_restart_optimization_results"],key=lambda x:x["information_bits"])
 U=np.array(winner["physical_ququart_basis_columns_real"])+1j*np.array(winner["physical_ququart_basis_columns_imag"])
 single=np.einsum("ai,nab,bi->ni",U.conj(),R,U).real
 assert abs(full.sum(axis=1)-1).max()<1e-11
 assert abs(single.sum(axis=1)-1).max()<1e-11
 models={}
 for name,P in (("Witting_40",full),("optimized_4outcome_basis",single)):
  BC,exp=allpairs(P)
  eta=.85
  lossy=np.c_[eta*P,np.ones(len(P))*(1-eta)]
  eb,el=allpairs(lossy)
  assert abs(eb-(1-eta+eta*BC))<1e-10
  # Loss-independent uniform output contamination on detected events.
  dark=.005
  contam=(1-dark)*P+dark/P.shape[1]
  cbd,ed=allpairs(contam)
  models[name]=dict(single_copy_worst_pair_Bhattacharyya_coefficient=BC,
     worst_pair_Bhattacharyya_exponent_per_detected_photon=exp,
     exact_union_bound_sufficient_detected_photons_for_max_5pct_ML_error=enough(exp),
     independent_85percent_heralded_no_click_BC=eb,
     exact_union_bound_sufficient_incident_photons_eta085=enough(el),
     uniform_background_fraction=.005,
     uniform_background_contaminated_worst_pair_BC=cbd,
     worst_pair_exponent_with_background=ed,
     sufficient_detected_photons_with_background=enough(ed),
     observed_seeded_100trials_ML_success_rate_700_shots=rng_mle(P,700,100,20261105),
     observed_seeded_100trials_ML_success_rate_12000_shots=rng_mle(P,12000,100,20261106))
 assert models["Witting_40"]["exact_union_bound_sufficient_detected_photons_for_max_5pct_ML_error"] < models["optimized_4outcome_basis"]["exact_union_bound_sufficient_detected_photons_for_max_5pct_ML_error"]
 from scipy.spatial.distance import pdist
 min_tv=float(np.min(pdist(full,metric="cityblock"))/2)
 assert abs(min_tv-k["Witting_POVM_440_state_min_pair_total_variation"])<1e-10
 err=lambda delta:6*(2*math.sin(delta/2)+2*math.sin(delta/4))
 delta_crit=brentq(lambda x:2*err(x)-min_tv,0,.01)
 assert 0<delta_crit<.002
 controls=[]
 for delta in (0,.0001,.0005,.001,.002,.005,.01):
  bound=err(delta)
  controls.append(dict(max_abs_gate_mixing_angle_and_differential_phase_error_rad=delta,
    conservative_preparation_TV_deviation_upper_bound=bound,
    worst_pair_codeword_separation_certified_by_this_bound=bool(2*bound<min_tv)))
 result=dict(status="PASS_440ROOT_WITTING_ML_SUFFICIENT_BHATTACHARYYA_AND_CALIBRATION_GUARDS",
  labels=440,root_prior="uniform",
  target_max_ML_classification_error_probability=.05,
  exact_prior_Fano_necessary_detected_photon_lower_bound_at_epsilon_point_one=694,
  decoder_models=models,
  ideal_full_Witting_min_pair_TV=min_tv,
  six_2mode_gate_preparation_static_error_bound="TV(Pρideal,Pρactual)<=||U-V||op<=6*(2sin(delta/2)+2sin(delta/4)) for all six gates with both errors bounded by delta, fixed source mixture weights, fixed ideal POVM.",
  sufficient_max_per_gate_absolute_phase_and_mixing_error_radians_for_nonoverlap=delta_crit,
  static_calibration_bound_scan=controls,
  interpretation="Fano 694 is necessary, union-Bhattacharyya N upper budget is a SUFFICIENT worst-label maximum-likelihood error guarantee assuming all 440 exact IID likelihoods, trusted calibrated known POVM and state preparation. Numerical 100-trial MLE success is synthetic and not a confidence bound.",
  prior_art="Classical Bhattacharyya Markov and union likelihood ratios; no new quantum discrimination theorem. Specific finite 440-root Witting and optimized basis information geometry is calculated here.")
 OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
 print(result["status"],"N Witting",models["Witting_40"]["exact_union_bound_sufficient_detected_photons_for_max_5pct_ML_error"],"N optimized",models["optimized_4outcome_basis"]["exact_union_bound_sufficient_detected_photons_for_max_5pct_ML_error"],"delta",delta_crit,flush=True)
 return result
if __name__=="__main__":main()
