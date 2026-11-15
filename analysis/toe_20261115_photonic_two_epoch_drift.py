#!/usr/bin/env python3
"""Photonic calibration: impossibility without stationarity/drift control,
and a two-epoch curvature-bounded interpolation certificate.

The single-observable 16-rail contrast is recalibrated both before and
after a signal run, and its time interpolation error is bounded by
M*t*(1-t)/2 when |mu_j''(t)|<=M for EVERY rail.
No claims about actual hardware drift or measured fidelity.
"""
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/"data"/"toe_20261115_direct_witness_contrast_calibration.json"
OUT=ROOT/"data"/"toe_20261115_photonic_two_epoch_drift_certificates.json"

def run(r=.01,curvature_bound=.2):
  old=json.loads(OLD.read_text())
  assert old["status"]=="MODEL_FREE_16_RAIL_WITNESS_CONTRAST_JOINT_99PCT_CALIBRATION"
  aC=.0025;aP=.0025;aW=.005
  R=old["sample_weight_range"]
  n_each=math.ceil(R*R*math.log(2*32/aC)/(2*r*r))
  n_parity=old["accepted_parity_calibrations_each"]
  assert 2*32*math.exp(-2*n_each*r*r/(R*R))<=aC*(1+1e-10)
  total=32*n_each+2*n_parity
  assert total>old["accepted_total_calibration"]
  # At t=1/2, linear interpolation error <= M/8;
  # the endpoint empirical errors each <= r simultaneously.
  t=.5
  interpolation_curvature_error=curvature_bound*t*(1-t)/2
  interp_contrast_bias=r+interpolation_curvature_error
  # Assume ideal endpoint empirical readout contrasts in this
  # illustration (0 observed deviation), but preserve finite
  # Hoeffding radius r and existing parity reference radius.
  gain=1-sum(old["parity_flip_estimates"])
  assert gain>0
  parity_bias_half=old["parity_flip_error_radius"]/gain
  lower=old["observed_synthetic_witness_fidelity"]-old["statistical_half_width"]-.5*interp_contrast_bias-parity_bias_half
  assert 0<lower<=1
  # Adversarial smooth one-column drift that is completely invisible
  # in perfect t=0 and t=1 calibrations, but at t=1/2 moves all rail0
  # events to rail1 (w=e0+e15). No unbounded-drift confidence theorem
  # can exclude it, regardless of shots.
  def bump(t):return math.sin(math.pi*t)**2
  assert abs(bump(0))<1e-15 and abs(bump(1))<1e-15 and abs(bump(.5)-1)<1e-15
  times=[k/20 for k in range(21)]
  observed_mid_bias=max(bump(t) for t in times)
  assert observed_mid_bias==1
  # The extremal bump has exact |second derivative|<=2*pi²;
  # cannot invoke illustrative M=.2 for this drift.
  assert 2*math.pi**2>curvature_bound
  return {
   "status":"TWO_EPOCH_WITNESS_CONTRAST_DRIFT_THEOREM_AND_NO_GO",
   "model_free_unbounded_drift_impossibility":True,
   "indistinguishable_endpoint_channels_with_middle_rail_error":observed_mid_bias,
   "adversarial_smooth_single_column_drift":"C00(t)=cos²(pi t), C10(t)=sin²(pi t), other columns identity; both endpoints C=I but at mid e0->e1",
   "drift_bump_max_abs_second_derivative":2*math.pi**2,
   "curvature_assumption":"For each contrast mu_j(t)=w^T C(t)[:,j], |mu_j''(t)|<=M in normalized interval [0,1]. Must be independently justified.",
   "confidence_level":.99,
   "confidence_failure_budget":{"64_endpoint_tail_events":aC,
          "2_parity_flip_rates":aP,"5_witness_settings":aW},
   "two_epoch_16rail_calibrations":32,
   "accepted_calibration_per_rail_per_epoch":n_each,
   "accepted_calibration_across_32_rail_epochs":32*n_each,
   "accepted_parity_reference_each":n_parity,
   "total_accepted_two_epoch_calibrations":total,
   "illustrative_curvature_bound_M":curvature_bound,
   "signal_time_t":t,
   "linear_interpolation_max_curvature_error_midpoint":interpolation_curvature_error,
   "midpoint_worst_contrast_bias_given_zero_endpoint_empirical_deviation":interp_contrast_bias,
   "synthetic_fidelity_99pct_lower_with_illustrative_drift_bound":lower,
   "confidence_scope":"Union of simultaneous Hoeffding endpoint estimates, parity calibration and witness sampling plus deterministic interpolation remainder under the stated M. Not valid for nonstationary detectors without bounded curvature.",
   "hardware_scope":"No experimental drift or hardware curvature was measured. The example M=.2 is assumed, not inferred. The negative control proves endpoint-only checks cannot imply any interior guarantee without regularity."
  }
if __name__=="__main__":
 o=run();OUT.write_text(json.dumps(o,indent=2)+"\n")
 print("PASS",o["status"],"accepted",o["total_accepted_two_epoch_calibrations"],"F99",o["synthetic_fidelity_99pct_lower_with_illustrative_drift_bound"])
