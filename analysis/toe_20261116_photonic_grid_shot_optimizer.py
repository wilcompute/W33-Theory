#!/usr/bin/env python3
"""Target-aware 99% photonic GHZ witness rail-calibration shot optimizer.

Instead of demanding fixed uniform .01 rail precision regardless of
the requested fidelity threshold, enumerate grid anchors and choose
largest admissible Hoeffding contrast radius r. Piecewise-linear
interpolation errors are bounded by M/(8 k^2) under |mu''|<=M or
L/(2k) under |mu'|<=L, where k=#time intervals.
All dynamic regularity, reference-preparation, and observed contrast
deviation bounds are prospective assumptions, not hardware data.
"""
from pathlib import Path
import json,math
ROOT=Path(__file__).resolve().parents[1]
OLD=ROOT/"data"/"toe_20261115_direct_witness_contrast_calibration.json"
OUT=ROOT/"data"/"toe_20261116_photonic_time_grid_calibration_optimizer.json"

def run(target=.90,observed_max_deviation_limit=.002,
        second_derivative_bound=.2,first_derivative_bound=.12):
    old=json.loads(OLD.read_text())
    R=float(old["sample_weight_range"])
    Fhat=float(old["observed_synthetic_witness_fidelity"])
    stat=float(old["statistical_half_width"])
    gain=1-sum(old["parity_flip_estimates"])
    ep=float(old["parity_flip_error_radius"])
    assert gain>0
    nParity=int(old["accepted_parity_calibrations_each"])
    aC,aP,aW=.0025,.0025,.005
    assert aC+aP+aW==.01
    assert 4*math.exp(-2*nParity*ep*ep)<=aP
    def candidate(grid,style):
        k=grid-1
        drift=(second_derivative_bound/(8*k*k)
               if style=="curvature" else first_derivative_bound/(2*k))
        # Reserve a 0.0001 strict margin in the projected lower bound.
        r=2*(Fhat-stat-ep/gain-target)-observed_max_deviation_limit-drift-0.0001
        if r<=0:return None
        n=int(math.ceil(R*R*math.log(32*grid/aC)/(2*r*r)))
        risk=32*grid*math.exp(-2*n*r*r/(R*R))
        assert risk<=aC*(1+1e-12)
        total=16*grid*n+2*nParity
        lower=Fhat-stat-.5*(observed_max_deviation_limit+r+drift)-ep/gain
        assert lower>target
        return {
         "calibration_grid_times":[j/k for j in range(grid)],
         "calibration_anchors":grid,"time_intervals":k,
         "regularity_assumption":style,
         "max_interpolation_contrast_error":drift,
         "contrast_Hoeffding_halfwidth":r,
         "max_observed_contrast_deviation_must_not_exceed":observed_max_deviation_limit,
         "accepted_calibration_shots_per_rail_per_anchor":n,
         "accepted_total_rail_contrast_calibrations":16*grid*n,
         "accepted_total_parity_references":2*nParity,
         "accepted_total_calibration_shots":total,
         "conditional_99pct_lower_witness_fidelity":lower,
         "joint_alpha_budget":[aC,aP,aW],
         "verified_rail_union_Hoeffding_failure_bound":risk
        }
    best={}
    for style in ("curvature","Lipschitz"):
        cases=[c for grid in range(2,41) if (c:=candidate(grid,style)) is not None]
        best[style]=min(cases,key=lambda c:c["accepted_total_calibration_shots"])
    assert best["curvature"]["calibration_anchors"]==3
    assert best["curvature"]["accepted_total_calibration_shots"]==444728
    assert best["Lipschitz"]["calibration_anchors"]==5
    assert best["Lipschitz"]["accepted_total_calibration_shots"]==705192
    return {
     "status":"PHOTONIC_TARGET_AWARE_DRIFT_GRID_99PCT_CALIBRATION_SHOT_OPTIMIZER",
     "source_synthetic_fidelity":Fhat,
     "source_synthetic_statistical_halfwidth":stat,
     "fidelity_threshold_requested":target,
     "confidence":.99,
     "maximum_empirical_anchor_contrast_deviation_assumed":observed_max_deviation_limit,
     "curvature_bound_M_assumed":second_derivative_bound,
     "Lipschitz_bound_L_assumed":first_derivative_bound,
     "prior_two_epoch_fixed_radius_accepted_calibration":2103112,
     "prior_one_epoch_fixed_radius_accepted_calibration":1137384,
     "optimal_separate_regularities":best,
     "actual_hardware_calibration_shots_collected":0,
     "no_regularilty_no_guarantee":"With arbitrarily time-varying detector confusion, no finite anchor grid controls the worst between-anchor bias; smooth but unbounded-curvature counterexamples exist.",
     "scope":"All numbers are accepted preparation counts for prospective planning. Require demonstrated stationarity within acquisition windows, independent known-rail preparation, true drift regularity, small observed anchor deviation, and trusted parity flips. No detector or photon was actually measured. Optimizing target >0.90 with relaxed contrast precision cannot be compared as equal-precision calibration to the earlier fixed-radius budget."
    }
if __name__=="__main__":
    d=run()
    OUT.write_text(json.dumps(d,indent=2)+"\n")
    print("PASS",d["status"],[(k,v["accepted_total_calibration_shots"]) for k,v in d["optimal_separate_regularities"].items()],flush=True)
