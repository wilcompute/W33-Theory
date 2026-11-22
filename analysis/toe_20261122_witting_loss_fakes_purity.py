"""A critical negative control: path-dependent Naimark optical loss fakes
the third-moment signatures of Witting pure ququart inputs.

All input states in this test remain PURE. Conditional triples after
state-dependent loss need not satisfy the exact ideal 40-ray 3-design
collision law. Uniform attenuation is a valid control.
"""
from __future__ import annotations
import json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_relational_reference_pareto as base
import toe_20261122_witting_40mode_naimark_finite_shots as optics
OUT=ROOT/"data/toe_20261122_witting_loss_fakes_purity.json"
def main():
    rays,_,_,_=base.geometry()
    V,T,gates,error=optics.compile_isometry(rays)
    assert error<1e-10
    rows=[]
    for loss in (0,.005,.01,.02):
        W=optics.propagate(T,gates,loss)
        examples=[]
        for idx in (0,5,39):
            x=rays[idx]
            raw=abs(W@x)**2
            survival=float(raw.sum())
            cond=raw/survival
            C2=float((cond**2).sum())
            C3=float((cond**3).sum())
            naive_purity=50*C2-1
            examples.append({"input_pure_ray":idx,"single_photon_survival":survival,
                 "conditioned_two_copy_collision":C2,
                 "conditioned_three_copy_collision":C3,
                 "incorrect_ideal_formula_inferred_purity":naive_purity})
        rows.append({"loss_per_active_two_mode_element":loss,
             "examples":examples})
    ideal=rows[0]["examples"]
    assert all(abs(x["conditioned_three_copy_collision"]-.002)<1e-11 for x in ideal)
    one=rows[2]["examples"]
    assert abs(one[0]["conditioned_three_copy_collision"]-.00273823)<1e-7
    assert abs(one[2]["conditioned_three_copy_collision"]-.00166987)<1e-7
    assert one[0]["incorrect_ideal_formula_inferred_purity"]>1.17
    assert one[2]["incorrect_ideal_formula_inferred_purity"]<.93
    # Global equal attenuation leaves all CONDITIONAL output probabilities
    # identical to the lossless Witting POVM.
    uniform=.7*V
    for x in (rays[0],rays[5],rays[39]):
        prob=abs(uniform@x)**2
        prob/=prob.sum()
        assert abs(sum(prob**3)-.002)<1e-11
    result={"status":"PASS","date":"2026-11-22",
      "pure_input_truth":"Tr(rho^2)=Tr(rho^3)=1 for all tested states",
      "wrong_ideal_purity_formula":"Tr(rho^2)=50 C2 -1, only valid for original calibrated Witting 40-outcome POVM",
      "loss_scan":rows,
      "uniform_loss_control_preserves_conditioned_C3":True,
      "scope":"Specific 150 active-Givens 4-to-40 isometry and equal power loss on touched rails only. No actual hardware. Explicit warning against uncalibrated postselection and false geometric purity claims."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print("PASS pure-state loss creates impossible naive Tr(rho^2)>1")
    return result
if __name__=="__main__":main()
