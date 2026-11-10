#!/usr/bin/env python3
"""End-to-end W33 four-optic optimistic PPT witness sensitivity ledger.

A Fisher bound is a LOWER bound on estimator variance, not a guaranteed
confidence certificate. For 95% one-sided size and 95% power a Gaussian
*efficient known-dual* estimator would need >=(z_alpha+z_power)^2 c/gap²
launched source photons. Separately quantify phase-only 95% worst-case
systematics; if larger than gap, no valid 95% certificate follows.
"""
import json,math,sys
from pathlib import Path
from scipy.stats import norm
ROOT=Path(__file__).resolve().parents[1]
def data(n):
    return json.loads((ROOT/"data"/(n+".json")).read_text(encoding="utf8"))
def main(path=None):
    designs=data("w33_20261109_four_architectures_full_loss_povm")
    calibr=data("w33_20261109_phase25_structured_calibration")
    old=data("w33_20261109_full_povm_calibration_bound")
    gap=float(old["source_controls"]["Horodecki_a0p236"]["true_CCNR"]-1)
    dual=float(old["source_controls"]["Horodecki_a0p236"]["calibration_tests"][0]["dual_l1"])
    z=float(norm.ppf(.95))
    rows=[]
    for scen,models in designs["full_POVM_results"].items():
        for name,v in models.items():
            c=v["mean_true_full_POVM_CCNR_CRLB"]
            lower=math.ceil((2*z)**2*c/(gap**2))
            rows.append({"scenario":scen,"architecture":name,
                "optimistic_gaussian_known_witness_95pct_size_95pct_power_launched_photon_budget":lower,
                "oracle_CCNR_CRLB_coefficient":c,
                "source_click_survival_fraction":v["mean_click_survival"]})
    # Actual finite-shot robust effect-norm radius at 10^10 launches
    # in phase-only model is order 1e-2; exceeds CCNR gap by >4x.
    # Dual is a stricter systematic gate; ordinary gap itself insufficient.
    delta_needed=gap/dual
    maxdelta=calibr["finite_trials"][str(10**10)]["simultaneous_95pct_effect_error_bound_conditioned_on_model"]
    assert maxdelta>delta_needed
    out={"status":"PASS_OPTIMISTIC_ORACLE_FISHER_PPT_POWER_LEDGER_WITH_SYSTEMATICS_NO_GO",
         "target":"mixed Horodecki PPT entangled two-qutrit rho(a=.236) via fixed oracle CCNR polar witness",
         "true_CCN_norm_separability_excess":gap,
         "optical_architecture_sample_budgets":rows,
         "one_sided_type_I_alpha":.05,"required_nominal_power":.95,
         "gaussian_normal_quantile_one_sided":z,
         "confidence_calibration":{
             "true_oracle_dual_l1":dual,
             "effect_operator_error_radius_below_required_necessary_even_infinite_physics_shots":delta_needed,
             "phase_only_at_1e10_calibration_trials_each_rigorous_radius":maxdelta,
             "phase_only_1e10_rigorous_radius_over_required":maxdelta/delta_needed,
             "calibration_sufficient_for_CCNR_at_1e10_trials_each":False},
         "scope":"Fisher Cramér-Rao supplies a MINIMUM optimistic asymptotic photon count if an unbiased efficient oracle-dual estimator exists. It is not an achievable sample-complexity result, not a finite-shot confidence certificate, ignores dual selection bias, stationary-source calibration uncertainty and unmodeled systematic errors. The effect calibration separately fails its necessary statistical gate. No lab result."}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("OPTIMISTIC_BUDGET",json.dumps({"gap":gap,"needed_delta":delta_needed,
      "worst_cal_delta":maxdelta,
      "ideal":{v["architecture"]:v["optimistic_gaussian_known_witness_95pct_size_95pct_power_launched_photon_budget"] for v in rows if v["scenario"]=="ideal"}}))
    return out
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
