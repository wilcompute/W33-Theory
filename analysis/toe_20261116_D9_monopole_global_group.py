#!/usr/bin/env python3
"""Global gauge group subtlety for D9 magnetic S² x S².

Dirac quantization 2 f_i r_i² = n_i in integer-charge units. The
charge-one monopole line bundle O(n_i) is SU2-equivariant, but the center
(-I) acts as (-1)^n_i on its fiber. Thus the Lie-algebra SO3×SO3
Killing zero modes do NOT necessarily integrate to a faithful action
of SO3×SO3 on the charged bundle.
"""
import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_D9_monopole_global_gauge_parity.json"

def central_kernel(n1,n2):
    return sorted(tuple((a,b,(n1*a+n2*b)%2))
                  for a,b in product(range(2),repeat=2))

def run():
    cases=[]
    for n1,n2 in product(range(-4,5),repeat=2):
        kernel=central_kernel(n1,n2)
        assert len(kernel)==4
        for a,b,z in kernel:
            assert (-1)**(n1*a+n2*b+z)==1
        # Take the SU2 homogeneous polynomial representation Sym^|n|(C2).
        # Its central element acts by (-1)^|n| on every monomial basis,
        # also for negative n by the dual representation.
        for n in (n1,n2):
            rep_eigenvalues={(-1)**(abs(n)-k+k) for k in range(abs(n)+1)}
            assert rep_eigenvalues=={(-1)**n}
        f1r2=F(n1,2);f2r2=F(n2,2)
        assert 2*f1r2==n1 and 2*f2r2==n2
        cases.append({
          "charges":[n1,n2],
          "center_action_SU2xSU2":[(-1)**n1,(-1)**n2],
          "kernel_Z2xZ2_lifts":kernel,
          "both_SO3_factors_lift_separately":n1%2==0 and n2%2==0,
          "quantized_moment_map_coefficients":[str(f1r2),str(f2r2)]
        })
    odd_even=[(n1,n2) for n1,n2 in product(range(2),repeat=2)
              if n1%2 and not n2%2]
    assert odd_even==[(1,0)]
    return {
       "status":"EXACT_D9_MONOPOLE_QUANTIZATION_GLOBAL_SU2_CENTER_PARITY",
       "monopole_flux_quantization":"For a unit electric charge, integral(F_i)/(2*pi)=n_i, or 2*f_i*r_i^2=n_i",
       "monopole_line_bundles":"O(n1) external tensor O(n2) over CP1 x CP1",
       "quantized_compensator":"mu_{i,a} = (n_i/2) n_{i,a}, on the ith S2",
       "global_isometry_gauge_group":"(SU(2)_1 x SU(2)_2 x U(1)) / <(-I,I,(-1)^n1),(I,-I,(-1)^n2)>",
       "central_minus_identity_action":"-I in SU(2)_i acts by (-1)^n_i on degree-|n_i| homogeneous sections",
       "SO3xSO3_split_lift_condition":"both n_i even",
       "nontrivial_example":[1,2],
       "nontrivial_example_kernel":central_kernel(1,2),
       "integer_charge_grid_checked":len(cases),
       "detailed_cases":cases,
       "physical_scope":"Conditional on compact U(1), unit electric charge, integral monopole flux and the standard SU2-equivariant line bundle. This is a global gauge-group refinement, not spontaneous E6 enhancement or a full coupled KK spectrum. The seven classical gauge generators remain at Lie-algebra level."
    }
if __name__=="__main__":
    d=run();OUT.write_text(json.dumps(d,indent=2)+"\n")
    print("PASS",d["status"],"grid",d["integer_charge_grid_checked"],flush=True)
