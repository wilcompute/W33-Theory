#!/usr/bin/env python3
"""Single-photon Bell CHSH uncertainty-envelope and power/failure gate.

Fixed displacement settings chosen at nominal high-overlap system; do NOT
silently re-optimize after a device changes. Test 16 corner devices with
uncertain eta, gamma, and source survival, plus one independently
reoptimized pessimistic device. No numerical hardware measurements.
"""
import json,sys,math,itertools
from pathlib import Path
import numpy as np
from w33_20261109_onoff_single_photon_real_detector import CHSH,optimize
ROOT=Path(__file__).resolve().parents[1]
def main(path=None):
    prev=json.loads((ROOT/"data/w33_20261109_onoff_single_photon_real_detector.json").read_text())
    nominal=prev["optimized_cases"]["realistic_2026_telecom_proxy"]
    z=np.array(nominal["displacements_real_imag"])
    assert abs(abs(CHSH(z,.86,1.,.92,1e-4)[0])-2.021790)<3e-5
    nominal_s=CHSH(z,.86,1.,.92,1e-4)[0]
    orientation=1 if nominal_s>0 else -1
    corners=[]
    for eta,gamma,src,dark in itertools.product((.85,.87),(.91,.93),(.98,1.),(0.,.0002)):
        raw,_=CHSH(z,eta,src,gamma,dark)
        corners.append({"eta":eta,"gamma":gamma,"source_survival":src,
                        "dark_mean_per_trial":dark,
                        "fixed_displacement_CHSH_oriented":float(orientation*raw)})
    values=[c["fixed_displacement_CHSH_oriented"] for c in corners]
    low=min(corners,key=lambda x:x["fixed_displacement_CHSH_oriented"])
    high=max(corners,key=lambda x:x["fixed_displacement_CHSH_oriented"])
    pess=optimize(.85,.98,.91,.0002,seed=20261109,maxiter=120)
    nominal_v=orientation*nominal_s
    # For IID random settings each trial contributes score in {-4,+4}.
    # One-sided Hoeffding epsilon_N=sqrt(32 log(1/alpha)/N).
    # This power target uses Chernoff/union-style sufficient condition
    # given a positive true mean margin Delta and bounded score.
    def needed(margin,alpha=.05,beta=.05):
        if margin<=0:return None
        return math.ceil(32*(math.sqrt(math.log(1/alpha))+
                   math.sqrt(math.log(1/beta)))**2/margin**2)
    assert nominal_v>2
    assert low["fixed_displacement_CHSH_oriented"]<2
    out={"status":"PASS_ONOFF_BELL_PARAMETER_ENVELOPE_NO_ROBUST_VIOLATION",
      "baseline_optimized_nominal_CHSH":nominal_v,
      "fixed_settings_corner_count":len(corners),
      "corners":corners,
      "worst_fixed_settings":low,
      "best_fixed_settings":high,
      "independent_pessimistic_reoptimized_device":pess,
      "nominal_95pct_power_95pct_size_sufficient_Hoeffding_trial_budget_under_perfect_IID_source_model":needed(nominal_v-2),
      "worst_corner_95pct_power_95pct_size_sufficient_Hoeffding_trial_budget":needed(low["fixed_displacement_CHSH_oriented"]-2),
      "source_heralding_and_reference_requirements":"Actual photon source survival, local detection efficiency and mode coherence must be calibrated independently, and trials must include all no-click events. Displacement amplitudes require an actual coherent reference; no measured hardware source meets these specifications in this simulation.",
      "novelty_scope":"Prior art on on/off displaced Bell tests, numerical sensitivity analysis for our constrained benchmark only.",
      "scope":"Corners are NOT rigorously the global worst values over the continuous parameter box; they are sampled parameter corners. Source eta model is independent global erasure. No instrument-independent Bell claim, no causality timing validation. The Hoeffding size/power budget is an ideal IID sufficient upper schedule, NOT an observed trial count."}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("BELL_ENVELOPE",json.dumps({"nominal":nominal_v,
        "worst_fixed":low,"pess_reopt":pess["CHSH"],
        "nominal_Hoeffding_trials":out["nominal_95pct_power_95pct_size_sufficient_Hoeffding_trial_budget_under_perfect_IID_source_model"]}))
    return out
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
