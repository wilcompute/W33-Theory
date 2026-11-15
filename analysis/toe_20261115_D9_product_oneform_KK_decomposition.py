#!/usr/bin/env python3
"""Full scalar and one-form Hodge *kinematic* harmonic census on
S²(r1)xS²(r2), pre-Einstein-Maxwell mixing. For a mixed KK calculation,
the six Killing coexact modes MUST become zero-mass gauge combinations
after metric-Maxwell mixing; their raw Hodge eigenvalues are >0.
"""
import json
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261115_D9_S2S2_Hodge_vector_KK_pre_mix.json"

def run(L=8):
    t=sp.symbols("t",positive=True)
    levels=[]
    scalar_count=0;exact=0;coexact=0;killing=0
    for a in range(L+1):
        for b in range(L+1):
            g=(2*a+1)*(2*b+1)
            la=a*(a+1);lb=b*(b+1)
            lambdaL=sp.factor(20*(la+t*lb)/(1+t))
            num_exact=int(a+b>0)
            num_coexact=int(a>0)+int(b>0)+int(a>0 and b>0)
            num_oneforms=num_exact+num_coexact
            assert num_oneforms==(0 if a+b==0 else 4 if a>0 and b>0 else 2)
            if a+b>0:assert lambdaL.subs(t,sp.Rational(7,3))>0
            scalar_count+=g
            exact+=g*num_exact
            coexact+=g*num_coexact
            if (a,b) in ((1,0),(0,1)):
                assert num_coexact==1 and g==3
                killing+=g
            levels.append({"l1":a,"l2":b,"harmonic_degeneracy":g,
                           "laplace_eigenvalue_m2L2":str(lambdaL),
                           "oneform_exact_polarization_count":num_exact,
                           "oneform_coexact_polarization_count":num_coexact})
    S=(L+1)**2
    assert scalar_count==S*S
    assert exact==S*S-1
    assert coexact==3*(S-1)**2+2*(S-1)
    assert exact+coexact==4*S*(S-1)
    assert killing==6
    # The K=1 vector harmonics are * dY_1 (three rotations per
    # S2); on their sphere the Hodge eigenvalue is 2/r_i².
    # This nonzero Hodge eigenvalue is not a physical 5D vector mass.
    first_coexact_gap=40*sp.Min(1,t)/(1+t)
    assert sp.simplify(first_coexact_gap.subs(t,1)-20)==0
    return {
      "status":"EXACT_PREMIX_S2S2_ONEFORM_KK_HARMONIC_CENSUS",
      "internal_manifold":"S2(r1) x S2(r2), t=r1^2/r2^2>0",
      "l1_l2_window":[0,L],
      "scalar_harmonic_count":scalar_count,
      "exact_oneform_count_in_window":exact,
      "coexact_oneform_count_in_window":coexact,
      "total_oneform_count_in_window":exact+coexact,
      "independent_coexact_polarizations_l1l2":{"0,0":0,"a>0,0":1,"0,b>0":1,"a>0,b>0":3},
      "independent_exact_polarizations_l1l2":{"0,0":0,"all_nonconstant":1},
      "hodge_oneform_eigenvalue_L2":"20*(l1*(l1+1)+t*l2*(l2+1))/(1+t)",
      "hodge_vector_lowest_positive_eigenvalue_L2":str(first_coexact_gap),
      "six_Killing_oneforms_inside_coexact_modes":killing,
      "theory_requirement":"The 6 Killing modes have nonzero raw Hodge eigenvalue, but must generate 6 massless gauge combinations after metric-Maxwell mixing because flux is invariant under SO3 x SO3 up to gauge. Any purported physical KK mass matrix assigning all six mass^2=lambdaHodge is invalid.",
      "model_scope":"Kinematic Hodge decomposition and exact representation counts, NOT the dynamically mixed Einstein-Maxwell vector or scalar eigenmasses. No full KK stability claim.",
      "mode_table":levels
    }
if __name__=="__main__":
    result=run()
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    print("PASS",result["status"],"exact",result["exact_oneform_count_in_window"],
          "coexact",result["coexact_oneform_count_in_window"],flush=True)
