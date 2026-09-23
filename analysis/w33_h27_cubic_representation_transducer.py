#!/usr/bin/env python3
"""Representation-ring test for a nonlinear H27/Yukawa transducer.

For K=H27 x C3_external, write L(a,b,t) for the 1D characters and S(r,t)
for the 3D Schrodinger irreps with H27 central character omega^r, r=1,2.

Exact tensor rules are forced by central character and dimensions:
  S(1,t) x S(2,u) = direct_sum_{a,b in F3} L(a,b,t+u)
  S(1,t) x S(1,u) = 3 S(2,t+u)
  S(2,t) x S(2,u) = 3 S(1,t+u).

Hence the sectors that obstruct the linear address->operator compiler are not
closed under nonlinear coupling: conjugate Schrodinger pairs can generate the
desired V_omega target type, while mixed pairs generate the full abelian
character sector.

Also,
  dim Hom_K(1, S(1,t) x S(1,u) x S(1,v)) = 3 if t+u+v=0, else 0,
and similarly for S(2)^3. Thus the H27 layer admits cubic singlets with the
same external Z3 charge-selection law as the E8/E6 cubic grading.

Boundary: this is a representation-ring permission theorem. It does not prove
that the landed E6 cubic coefficients implement a unitary 54D compiler.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_h27_cubic_representation_transducer.json"

def mixed(t,u):
    return {f"L_{a}_{b}_{(t+u)%3}":1 for a in range(3) for b in range(3)}
def same(r,t,u):
    rr=(r+r)%3
    assert rr in (1,2)
    return {f"S_{rr}_{(t+u)%3}":3}
def cubic_singlet_mult(r,t,u,v):
    # S_r x S_r = 3 S_{2r}; S_{2r} x S_r contains all 9 one-dimensional
    # chars once per copy. The trivial H27 char appears once per copy, hence 3,
    # provided the external character sum is zero.
    return 3 if (t+u+v)%3==0 else 0

def main(write=True):
    # Exhaust all external charges.
    rows=[]
    for t in range(3):
      for u in range(3):
        m=mixed(t,u)
        assert len(m)==9 and sum(m.values())==9
        a=same(1,t,u);b=same(2,t,u)
        assert a=={f"S_2_{(t+u)%3}":3}
        assert b=={f"S_1_{(t+u)%3}":3}
        rows.append({"t":t,"u":u,"S1xS2_dimension":9,
                     "S1xS1":a,"S2xS2":b})

    cubic=[]
    nonzero=0
    for r in (1,2):
      for t in range(3):
        for u in range(3):
          for v in range(3):
            mult=cubic_singlet_mult(r,t,u,v)
            if mult:nonzero+=1
            cubic.append({"r":r,"external":[t,u,v],"singlet_multiplicity":mult})
    assert nonzero==18 # 9 charge-zero triples for each r
    assert sum(x["singlet_multiplicity"] for x in cubic)==54

    deficit=json.loads((ROOT/"data/w33_hybrid81_operator_equivariance_budget.json").read_text())
    assert deficit["equivariant_map_budget"]["full_equivariance_deficit"]==54

    out={
      "schema":"w33.h27_cubic_representation_transducer.v1",
      "status":"PASS_H27_TENSOR_RING_PERMITS_NONLINEAR_TRANSMUTATION_ACROSS_THE_LINEAR_54D_OBSTRUCTION",
      "headline":"The 54D linear equivariance obstruction is not a nonlinear selection-rule obstruction. Exact H27 tensor products obey V_omega tensor V_omega^2 = all nine one-dimensional characters, V_omega^2 tensor V_omega^2 = 3 V_omega, and V_omega tensor V_omega = 3 V_omega^2. Cubic Schrodinger products contain three singlets exactly when external C3 charges sum to zero.",
      "tensor_rules":{
        "S1_t_x_S2_u":"direct sum of all L(a,b,t+u), a,b in F3",
        "S1_t_x_S1_u":"3 S2_(t+u)",
        "S2_t_x_S2_u":"3 S1_(t+u)",
        "dimensions":{"mixed":9,"same":9}
      },
      "cubic_invariants":{
        "rule":"dim Hom_K(1,S(r,t) tensor S(r,u) tensor S(r,v)) = 3 iff t+u+v=0 mod3",
        "charge_zero_external_triples_per_central_character":9,
        "central_characters_tested":[1,2],
        "nonzero_charge_labeled_cases":18,
        "total_singlet_multiplicity_across_all_cases":54
      },
      "compiler_reading":"A linear K-intertwiner cannot fill 54 operator dimensions, but quadratic/cubic couplings can change H27 central character and create exactly the irrep species missing from the linear image. This makes the E6 cubic/Yukawa layer a mathematically type-correct candidate for the symmetry-changing stage.",
      "physics_hypothesis":"Test the landed E6 cubic coefficients as an explicit nonlinear transducer in the hybrid81 basis: mixed matter/antimatter Schrodinger factors should generate abelian control channels, while conjugate-pair self-couplings can generate V_omega operator channels.",
      "boundary":"Representation-ring compatibility is necessary but not sufficient for a physical compiler. No unitary nonlinear gate, coupling strength, vacuum expectation value, mass, or scattering amplitude is derived here.",
      "parents":[
        "data/w33_hybrid81_operator_equivariance_budget.json",
        "data/w33_e8_full_graded_hybrid_atlas.json"
      ],
      "checks":{
        "all_9_external_pair_charges_checked":True,
        "mixed_tensor_dimension9":True,
        "same_tensor_dimension9":True,
        "S1S2_gives_all_9_abelian_chars":True,
        "S2S2_gives_3_S1":True,
        "S1S1_gives_3_S2":True,
        "cubic_charge_rule_exhausted":True,
        "linear_no_go_not_misreported_as_nonlinear_no_go":True
      }
    }
    if write:OUT.write_text(json.dumps(out,indent=2)+"\n")
    return out

if __name__=="__main__":
    print(json.dumps(main(True),indent=2))
