"""Event-ready, loss-robust four-MUB qutrit Bell-return witness.

The preceding repo witness gives S=sum_b P_match(b)=1+3F and
S<=2 for all separable two-qutrit states. Treat NO-CLICK as MISMATCH
and divide by heralded attempts, not accepted coincidences. The measured
click&match POVM must be dominated by the calibrated MUB match projector.
Then the click&match probabilities give a valid LOWER bound on S without
an unverified fair-sampling assumption.

This program is a conditional experimental design, no real hardware data.
"""
import importlib.util,json,math
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_qutrit_eventready_loss_bound.json"
sp=importlib.util.spec_from_file_location("mub",ROOT/"analysis"/"toe_20261116_qutrit_four_MUB_experiment.py")
prior=importlib.util.module_from_spec(sp);sp.loader.exec_module(prior)

def eventready_plan(v,eta,epsilon=0,alpha=.01,beta=.1):
    v,eta,epsilon=map(float,(v,eta,epsilon))
    if not (0<=v<=1 and 0<=eta<=1 and epsilon>=0):raise ValueError("invalid probability or calibration bound")
    if not (0<alpha<1 and 0<beta<1):raise ValueError("alpha,beta in (0,1)")
    ideal=4*(1+2*v)/3
    eta_min=2/ideal
    observed=eta*ideal
    # Each of 4 basis click-match POVMs is calibrated within epsilon
    # downward relative to the ideal probability. Conservatively
    # require a 4epsilon witness margin.
    gap=observed-2-4*epsilon
    row={"v":v,"pair_detection_probability":eta,
         "calibration_absolute_error_per_setting":epsilon,
         "ideal_sum_four_MUB":ideal,
         "event_ready_click_match_sum":observed,
         "necessary_eta_threshold_with_zero_calibration_error":eta_min,
         "loss_robust_detectable_at_assumed_parameters":gap>0,
         "margin_after_calibration":gap,
         "without_fair_sampling":"No-click heralded trials are explicitly recorded as failures. Accepted coincidence counts alone are insufficient."}
    if gap<=0:
        row["gross_attempts_per_basis"]=None
        row["note"]="No number of trials can prove entanglement using this conservative four-MUB witness under this model."
    else:
        z=(math.sqrt(2*math.log(1/alpha))+math.sqrt(2*math.log(1/beta)))**2
        n=math.ceil(z/(gap*gap))
        row.update({"alpha":alpha,"beta":beta,
                    "gross_attempts_per_basis":n,
                    "total_event_ready_heralded_attempts":4*n,
                    "Hoeffding_rule":"reject separability if sum click-match frequencies - 4epsilon > 2 + sqrt(2 ln(1/alpha)/n)",
                    "power_bound":"Under prespecified IID isotropic-noise model with fixed eta, failure probability <= beta."})
    return row

def verify():
    assert prior.mubs_identity_error()<1e-12
    plans=[eventready_plan(v,eta,eps) for v,eta,eps in
           [(.75,.5,0),(.75,.6,0),(.75,.7,0),(.75,.7,.01),(.9,.65,.01),(.6,.7,0),(.25,1,0)]]
    assert plans[0]["loss_robust_detectable_at_assumed_parameters"] is False
    assert plans[1]["loss_robust_detectable_at_assumed_parameters"] is False
    assert plans[2]["loss_robust_detectable_at_assumed_parameters"] is True
    assert plans[3]["gross_attempts_per_basis"]>plans[2]["gross_attempts_per_basis"]
    assert abs(plans[3]["necessary_eta_threshold_with_zero_calibration_error"]-.6)<1e-12
    assert plans[-1]["loss_robust_detectable_at_assumed_parameters"] is False
    for p in plans:
        if p["gross_attempts_per_basis"] is not None:
            assert p["gross_attempts_per_basis"]>0
    return {
        "status":"PASS_EVENT_READY_QUTRIT_LOSS_AND_CALIBRATION_WITNESS",
        "separability_bound":"Sum of 4 ideal matched-MUB probabilities <=2",
        "loss_robust_bound":"Sum of observed click-and-match probabilities - 4epsilon <= ideal sum, provided registered click effects are bounded by matched projectors up to epsilon",
        "threshold_eta":"eta>3/[2*(1+2*v)] for isotropic visibility v (no calibration uncertainty)",
        "necessary_hardware_caveat":"A priori heralded trials, phase- and setting-calibrated projective bases, and domination of click POVM are required. Detector dark counts/cross-talk must enter epsilon.",
        "all_plans_hypothetical":True,
        "cases":plans}
if __name__=="__main__":
    r=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(r["status"],[(x["v"],x["pair_detection_probability"],x["gross_attempts_per_basis"]) for x in r["cases"]])
