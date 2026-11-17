"""Quantitative robustness of the E6 Higgs-leg polynomial triplet filter.

Parallel agent's tree filter F(t)=(t²-4)/5 exactly vanishes on
both triplet weights t=+2 and -2 while F(-3)=1 on up doublet.
This is a unique quadratic interpolation (Vandermonde determinant20).
Nothing yet protects its coefficients or VEV eigenvalues quantumly.

For commuting diagonal detuning t_triplet=±2+delta,
the worst-case leakage relative to fixed doublet normalization is
s(delta)=(4|delta|+delta²)/5. For one operator the
proton-decay rate is multiplied by s², lifetime by 1/s².
This is a sensitivity analysis, not a full flavor calculation.
"""
import math,json,sys
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261116_proton_Knu_dressing_bounds import model,LIMIT
OUT=ROOT/"data"/"toe_20261116_E6_triplet_filter_misalignment_tolerance.json"
def polynomial():
    x=sp.Symbol("x")
    mat=sp.Matrix([[1,t,t*t] for t in (-3,-2,2)])
    vals=sp.Matrix([1,0,0])
    c=mat.inv()*vals
    F=sp.expand(c[0]+c[1]*x+c[2]*x*x)
    assert mat.det()==20
    assert F==(x*x-4)/5
    return {"coefficients":[str(v) for v in c],"Vandermonde_determinant":20,
        "polynomial":str(F),"values_at_minus3_minus2_plus2":[int(F.subs(x,t)) for t in (-3,-2,2)]}
def tolerance(ymul=1e-6,M=5e16):
    base=model(ymul=ymul,Mtriplet=M)
    if base["passes_single_operator_bound"]:
        required=1.
    else:
        required=math.sqrt(base["lifetime_years"]/LIMIT)
    # Worst-case common magnitude δ on both triplet weights:
    # (4d+d²)/5 <= required.
    maxd=math.sqrt(4+5*required)-2
    checks=[]
    for d in (0.,.01,.05,.1,.2,.25,.5):
        leak=(4*d+d*d)/5
        lifetime=(math.inf if leak==0 else base["lifetime_years"]/leak**2)
        checks.append({"eigenvalue_detuning_magnitude":d,
            "worst_case_up_triplet_coupling_fraction":leak,
            "single_operator_lifetime_years":str(lifetime),
            "passes_experimental_limit":lifetime>=LIMIT})
    assert checks[0]["passes_experimental_limit"]
    return {"unsuppressed_reference":base,
       "required_amplitude_fraction_below":required,
       "max_commuting_eigenvalue_detuning_for_both_triplets":maxd,
       "cases":checks}
def verify():
    p=polynomial()
    high=tolerance(ymul=1e-6)
    low=tolerance(ymul=1e-8)
    assert high["max_commuting_eigenvalue_detuning_for_both_triplets"]<.3
    assert low["max_commuting_eigenvalue_detuning_for_both_triplets"]>.2
    return {"status":"PASS_E6_TRIPLET_FILTER_VEV_DETUNING_STRESS_TEST",
      "unique_quadratic_filter":p,
      "proton_bound_high_yukawa":high,
      "proton_bound_low_yukawa":low,
      "linear_sensitivity":"For t=+/-2+delta, F(t)=(+/-4delta+delta²)/5. A generic detuning reintroduces triplet exchange at first order; rate scales delta² to leading order.",
      "coefficient_tuning":"The exact cancellation requires the three interpolation conditions to persist after threshold corrections and RG running. Without an exact symmetry, no all-orders protection has been demonstrated.",
      "scope":"Only commuting diagonal VEV detuning and one effective decay operator. Full E6 adjoint mixing, flavor, messenger renormalization, alternative gauge exchange and proton dressing may dominate."}
if __name__=="__main__":
    x=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(x["status"],x["proton_bound_high_yukawa"]["max_commuting_eigenvalue_detuning_for_both_triplets"])
