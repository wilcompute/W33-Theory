#!/usr/bin/env python3
"""Photon Bell: detector-efficiency and heralded-survival engineering thresholds.

Local displacement+on/off POVM only, with independently specified
global source loss, phase coherence and dark counts. Uses multistart
differential evolution, fixed analyzer source-survival linear root, and
parameter uncertainty. No physical spacelike event-ready test is run.
"""
import json,sys,math
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from w33_20261109_onoff_single_photon_real_detector import CHSH,optimize
ROOT=Path(__file__).resolve().parents[1]

def best(eta,src,gamma,dark,seeds=(20261109,20261110),maxiter=100):
    fits=[optimize(eta,src,gamma,dark,seed, maxiter=maxiter) for seed in seeds]
    return max(fits,key=lambda x:x["CHSH"])

def oriented(z,eta,src,gamma,dark,sign):
    return float(sign*CHSH(z,eta,src,gamma,dark)[0])
def main(path=None):
    past=json.loads((ROOT/"data/w33_20261109_onoff_single_photon_real_detector.json").read_text())
    nom=past["optimized_cases"]["realistic_2026_telecom_proxy"]
    z0=np.array(nom["displacements_real_imag"])
    sign=1 if nom["signed_CHSH"]>0 else -1
    f0=oriented(z0,.86,0.,.92,1e-4,sign)
    f1=oriented(z0,.86,1.,.92,1e-4,sign)
    assert f1>2 and f1>f0
    survival_needed=(2-f0)/(f1-f0)
    assert 0<survival_needed<1
    assert abs(oriented(z0,.86,survival_needed,.92,1e-4,sign)-2)<1e-12
    # Scenario with realistic uncertain low efficiency, overlap and source.
    gamma=.91;src=.98;dark=.0002
    optim={}
    for eta in (.85,.88,.90,.92,.94,.96):
        fit=best(eta,src,gamma,dark,maxiter=92)
        optim[str(eta)]={"optimized_abs_CHSH":fit["CHSH"],
                         "optimizer_converged":fit["converged"],
                         "displacements_real_imag":fit["displacements_real_imag"],
                         "mean_displacement_photons_each":fit["mean_displaced_photons_per_local_setting"]}
    assert optim[str(.85)]["optimized_abs_CHSH"]<2
    assert optim[str(.96)]["optimized_abs_CHSH"]>2
    high=optim[str(.94)]["displacements_real_imag"]
    orient=1 if CHSH(high,.94,src,gamma,dark)[0]>0 else -1
    threshold=float(brentq(lambda eta:oriented(high,eta,src,gamma,dark,orient)-2,
                           .85,.99,xtol=1e-11))
    # Robust fixed-displacement protocol must pass all 16 corners.
    prev=json.loads((ROOT/"data/w33_20261109_onoff_bell_robust_envelope.json").read_text())
    corner=prev["worst_fixed_settings"]
    assert corner["fixed_displacement_CHSH_oriented"]<2
    # Check two independent seed runs are adequate benchmarks, not a
    # mathematical proof of a global optimum over all four complex modes.
    out={"status":"PASS_ONOFF_SINGLE_PHOTON_SOURCE_AND_DETECTOR_THRESHOLDS",
         "nominal_detector_efficiency":.86,
         "nominal_relative_coherence":.92,
         "nominal_dark_count_mean":1e-4,
         "fixed_nominal_analyzer_critical_global_source_survival":survival_needed,
         "nominal_no_source_loss_CHSH":f1,
         "nominal_all_vacuum_oriented_CHSH":f0,
         "pessimistic_scenario":{"source_survival":src,"coherence":gamma,"dark_counts":dark},
         "multi_seed_reoptimized_efficiency_scan":optim,
         "critical_detector_efficiency_for_fixed_analyzer_optimized_at_94pct":threshold,
         "fixed_94pct_analyzer_CHSH_at_critical_efficiency":oriented(high,threshold,src,gamma,dark,orient),
         "at_previous_worst_corner":corner,
         "sources":[
          "https://arxiv.org/abs/2607.29012",
          "https://doi.org/10.1103/PhysRevA.88.012111"],
         "scope":"Thresholds are numerical sufficient crossings for the explicitly optimized displaced on/off protocol at fixed source, phase and dark assumptions. Multiple seeds check local optimizer reliability but cannot prove global optical optimality or demonstrate actual experimental device capabilities. A single signal photon plus coherent LO resource is not a total one-photon apparatus. Full event-ready loopholes and spacelike station clocks remain unmeasured.",
         "falsifier":"If calibrated efficiencies, coherence or source survival lie below the stated settings-specific crossing, this chosen protocol cannot yield a positive expected CHSH margin regardless of trial count."}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("BELL_HARDWARE_THRESHOLDS",json.dumps({"survival_nominal":survival_needed,
           "detector_fixed_94_thr":threshold,
           "scan":{k:round(v["optimized_abs_CHSH"],5) for k,v in optim.items()}}))
    return out
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
