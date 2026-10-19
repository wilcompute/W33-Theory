"""Front5: no parameter-free gauge-scale ratio from W33/E8 without
UV coupling and symmetry-breaking threshold inputs.
Shows one-loop matching and a quantitative threshold deformation
of the trivial equal-gauge-coupling ratio.
"""
from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round8_rg_threshold_nogo.json"
PI=math.pi
def Lambda(mu,g,b):
    return mu*math.exp(-8*PI**2/(b*g*g))
def g_running(g0,mu0,mu,b):
    # 1/g^2(mu)=1/g0^2+(b/8pi2)ln(mu/mu0)
    return 1/math.sqrt(1/g0**2+(b/(8*PI**2))*math.log(mu/mu0))
def matched_IR_scale(mu0,g0,threshold,bU=9,bIR=11):
    gM=g_running(g0,mu0,threshold,bU)
    return Lambda(threshold,gM,bIR)
def run():
    mu=1e12; bU=9; bIR=11;g0=.62
    base=Lambda(mu,g0,bU)
    vals=[]
    for M in (1e3,1e4,1e6,1e9,1e11):
        L=matched_IR_scale(mu,g0,M,bU,bIR)
        closed=(M**(1-bU/bIR))*(base**(bU/bIR))
        vals.append({"matching_threshold_GeV":M,
                     "IR_one_loop_Lambda_GeV":L,
                     "closed_form_Lambda_GeV":closed,
                     "relative_closed_form_residual":abs(L/closed-1)})
    # Three identical SU3s unified with equal g and beta have
    # identical Lambda. But unequal charged-matter threshold scales
    # spoil this equality.
    ratio=matched_IR_scale(mu,g0,1e9)/matched_IR_scale(mu,g0,1e3)
    expected=(1e9/1e3)**(1-bU/bIR)
    # One-loop coupling g must be supplied at UV; finite incidence
    # and normalized invariant form cannot set its numerical value.
    gvals=[]
    for g in (.42,.5,.62,.75):
        gvals.append({"UV_g":g,"UV_Lambda_GeV":Lambda(mu,g,bU)})
    # An E8 simple algebra has an invariant bilinear form unique
    # up to scaling. Fixing its Chevalley generator normalization
    # does not select the coefficient of F_{mu nu}F^{mu nu}.
    # The kinetic action (4g^2)^-1 K(F,F) is invariant under
    # K->cK and g²->c g² as bare quadratic functional.
    normalizations=[]
    for c in (.1,1,3,13):
        K=2.3;g=.62
        action=K/(4*g*g)
        new=c*K/(4*c*g*g)
        normalizations.append({"K_rescale":c,"quadratic_action_difference":abs(new-action)})
    checks={
      "all_one_loop_threshold_match_closed_form":max(v["relative_closed_form_residual"] for v in vals)<1e-12,
      "unification_unequal_thresholds_break_equal_Lambda":abs(ratio-1)>1,
      "threshold_ratio_analytic_law":abs(ratio/expected-1)<1e-12,
      "free_UV_g_changes_generated_scale_by_orders":gvals[-1]["UV_Lambda_GeV"]>1e5*gvals[0]["UV_Lambda_GeV"],
      "kinetic_normalization_scalar_redundancy":max(x["quadratic_action_difference"] for x in normalizations)<1e-12}
    out={"schema":"w33.round8.rg_threshold_scale_nogo.v1",
      "model":"Illustrative one-loop SU3 with bUV=9 (3 Dirac flavors) and bIR=11 (0 active flavors) below a matter threshold M, matching continuous g at mu=M. This is conditional gauge-model analysis, NOT a derived W33/E8 field action.",
      "UV_gauge_reference_GeV":mu,"UV_g":g0,
      "UV_Lambda_b9_GeV":base,
      "thresholds":vals,
      "two_sector_threshold_ratio":ratio,
      "analytic_ratio_power":1-bU/bIR,
      "UV_coupling_variation":gvals,
      "kinetic_form_normalization_examples":normalizations,
      "parameter_identifiability":"Even if E8 forces g_C=g_L=g_R at a single UV reference, equality of dimensionless tree-level couplings only predicts matching 1-loop Lambda ratios if beta functions AND thresholds match. Unknown symmetry-breaking masses M_i make Lambda_i/Lambda_j=(M_i/M_j)^(1-bUV/bIR) variable. The simple algebra fixes the invariant quadratic form only up to normalization; neither its Cartan integers nor W33 counts determine the action's positive kinetic coefficient or the UV reference energy.",
      "physical_limits":"Single-coupling one-loop decoupling toy model; ignores threshold matching finite corrections, Yukawa/scalar multiplets, higher loops and gravity. Realistic unified E8(-24) noncompact gauge sectors require separate unitarity/ghost analysis before a physical interpretation.",
      "checks":{k:bool(v) for k,v in checks.items()},
      "all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":out["checks"],"threshold_ratio":ratio,"UV_Lambda":base},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
