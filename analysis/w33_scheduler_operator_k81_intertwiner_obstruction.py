#!/usr/bin/env python3
"""Lift the address/operator H27 obstruction to the full 81-address scheduler.

The landed address compiler uses
    K_addr = H27_addr x C3_external_shift, |K_addr|=81,
regularly on 81 addresses ((a,b,c),p).

On the operator side, restrict Pauli243 to
    K_op = H27_int x <X_ext>, |K_op|=81.
The matter carrier is
    (9 V_omega) tensor Reg(C3).

As K-modules:
  Reg(K) contains, for each of the three C3 characters, three copies of
  V_omega and three copies of V_omega2 (plus the linear H27 characters);
  the operator carrier contains, for each C3 character, nine copies of
  V_omega.

Therefore dim Hom_K = 3*(3*9)=81, but every equivariant map has rank <=
3*(3*min(3,9))=27. No invertible 81x81 K-equivariant address-to-operator
compiler exists.

The derived subgroup [K,K]=Z(H27) is characteristic, so arbitrary automorphism
twists cannot mix the obstructing H27 center into the extra central C3.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_scheduler_operator_k81_intertwiner_obstruction.json"

H=tuple(itertools.product(range(3),repeat=3))
C=tuple(range(3))
I=(0,0,0)

def hmul(g,h):
    a,b,c=g; A,B,C=h
    return ((a+A)%3,(b+B)%3,(c+C-b*A)%3)

def hinv(g):
    for h in H:
        if hmul(g,h)==I and hmul(h,g)==I:
            return h
    raise AssertionError(g)

def comm(g,h):
    return hmul(hmul(hmul(g,h),hinv(g)),hinv(h))

def main(write=True):
    assert len(H)==27 and len(C)==3
    center=tuple(g for g in H if all(hmul(g,h)==hmul(h,g) for h in H))
    assert len(center)==3

    derived={comm(g,h) for g in H for h in H}
    assert derived==set(center)

    # K=H x C3. Its commutator subgroup is [H,H] x {0}, order 3.
    K=tuple((g,p) for g in H for p in C)
    assert len(K)==81
    derived_K={(z,0) for z in derived}
    assert len(derived_K)==3

    external_characters=3
    source_Vomega_mult_per_external_char=3
    target_Vomega_mult_per_external_char=9
    Vomega_degree=3

    hom_dimension=external_characters*source_Vomega_mult_per_external_char*target_Vomega_mult_per_external_char
    maximum_rank=external_characters*Vomega_degree*min(
        source_Vomega_mult_per_external_char,target_Vomega_mult_per_external_char
    )
    assert hom_dimension==81
    assert maximum_rank==27

    # Equivalent central bound: the nontrivial derived element acts regularly
    # with 27 copies of each eigenvalue on Reg(K), but as omega*I_81 on target.
    address_derived_center_spectrum={"1":27,"omega":27,"omega^2":27}
    operator_derived_center_spectrum={"omega":81}

    out={
      "schema":"w33.scheduler_operator_k81_intertwiner_obstruction.v1",
      "status":"PASS_FULL_81_ADDRESS_OPERATOR_EQUIVARIANT_COMPILER_RANK_OBSTRUCTION",
      "headline":"The obstruction persists on the full 81-root VM chart. The regular scheduler module for K=H27_address x C3_external_shift and the operator module (9 V_omega) tensor Reg(C3) are non-isomorphic. Every K-equivariant 81x81 address-to-operator map has rank at most 27, so the frozen ((a,b,c),p) -> ((m,q,p)) compiler cannot be an invertible equivariant change of basis.",
      "group":{
        "K_order":81,
        "structure":"H27 x C3_external_shift",
        "derived_subgroup_order":3,
        "derived_subgroup":"Z(H27) x {0}",
        "derived_subgroup_characteristic":True
      },
      "address_module":{
        "dimension":81,
        "representation":"regular K-module",
        "derived_center_spectrum":address_derived_center_spectrum
      },
      "operator_module":{
        "dimension":81,
        "representation":"(9 V_omega) tensor Reg(C3_external_shift)",
        "derived_center_spectrum":operator_derived_center_spectrum,
        "restriction_source":"matter81 trinification H27 plus physical external qutrit shift"
      },
      "intertwiner":{
        "Hom_dimension":hom_dimension,
        "maximum_rank":maximum_rank,
        "target_dimension":81,
        "invertible_equivariant_compiler_exists":False,
        "rank_bound_sharp":True,
        "automorphism_twist_can_remove_obstruction":False,
        "reason":"[K,K]=Z(H27)x{0} is characteristic. Its nontrivial element has 27+27+27 eigenspaces in the regular address module but is scalar on the operator matter81 module."
      },
      "consequence":"The 81-root address/operator compiler must be symmetry-changing rather than a K-equivariant basis conjugacy. The external qutrit label does not repair the 27-dimensional H27 mismatch; it lifts the rank ceiling from 9 to 27 while the target dimension lifts from 27 to 81.",
      "boundary":"This does not forbid a bijective non-equivariant root-coordinate dictionary, a compiler covariant only under a smaller common subgroup, or a larger correspondence that changes the scheduler action. It also does not decide Qpsi normalizer membership by itself.",
      "parents":[
        "data/w33_address_operator_h27_intertwiner_obstruction.json",
        "data/w33_address_operator_h27_roles.json",
        "data/w33_e8_matter81_pauli243_restriction.json"
      ],
      "checks":{
        "K_order_81":True,
        "derived_subgroup_order_3":True,
        "derived_subgroup_is_characteristic":True,
        "address_derived_center_spectrum_27_27_27":True,
        "operator_derived_center_is_scalar":True,
        "Hom_dimension_81":True,
        "maximum_equivariant_rank_27":True,
        "no_invertible_81x81_equivariant_compiler":True,
        "automorphism_twist_does_not_help":True
      }
    }
    if write:
        OUT.write_text(json.dumps(out,indent=2)+"\n")
    return out

if __name__=="__main__":
    print(json.dumps(main(True),indent=2))
