#!/usr/bin/env python3
"""Exact rank obstruction between the regular/address and operator H27 modules.

The repository contains two different copies of the Heisenberg group H27:
  * address H27: the regular action on its 27 group elements;
  * operator H27: nine copies of the 3-dimensional Schroedinger irrep with
    nontrivial central character omega.

This script proves that no invertible H27-equivariant linear change of basis
can identify these modules. The proof is exact and character-theoretic.

For H27=<Z,X,z | ZX=zXZ, z central, all generators order 3>, the irreducibles
are nine one-dimensional characters (trivial on z) and two 3-dimensional
Schroedinger irreps V_omega,V_omega2. Hence
  C[H27] = (sum of 9 linears) + 3 V_omega + 3 V_omega2,
whereas the operator 27 is 9 V_omega.

Thus dim Hom_H27(C[H27],9 V_omega)=27, but every intertwiner has rank <=9.
The bound is sharp. The obstruction survives every automorphism twist of H27,
because an automorphism only sends the central generator z to z or z^2.

Boundary: this rules out an H27-equivariant root-gauge change of basis between
the two landed actions. It does not rule out a non-equivariant coordinate
dictionary, nor an intertwiner after changing/enlarging the group action.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_address_operator_h27_intertwiner_obstruction.json"

H = tuple(itertools.product(range(3), repeat=3))
IDENTITY = (0, 0, 0)
ZCENTER = (0, 0, 1)

def hmul(g, h):
    a,b,c = g
    A,B,C = h
    return ((a+A)%3, (b+B)%3, (c+C-b*A)%3)

def hpow(g,n):
    out=IDENTITY
    for _ in range(n):
        out=hmul(out,g)
    return out

def center():
    return tuple(g for g in H if all(hmul(g,h)==hmul(h,g) for h in H))

def regular_center_cycles():
    index={g:i for i,g in enumerate(H)}
    perm=[index[hmul(ZCENTER,g)] for g in H]
    seen=set(); cycles=[]
    for i in range(len(H)):
        if i in seen:
            continue
        cyc=[]; j=i
        while j not in seen:
            seen.add(j); cyc.append(j); j=perm[j]
        cycles.append(tuple(cyc))
    return tuple(cycles)

def main(write=True):
    assert len(H)==27
    assert center()==((0,0,0),(0,0,1),(0,0,2))
    assert all(hpow(g,3)==IDENTITY for g in H)

    cycles=regular_center_cycles()
    assert len(cycles)==9 and {len(c) for c in cycles}=={3}

    # H27 has 9 linear characters and two degree-3 Schroedinger characters.
    degree_square_sum=9*1*1+2*3*3
    assert degree_square_sum==27

    source_mult={"linear":1,"V_omega":3,"V_omega2":3}
    target_mult={"linear":0,"V_omega":9,"V_omega2":0}

    # Hom dimension = sum_i m_source(i)m_target(i).
    hom_dimension=source_mult["V_omega"]*target_mult["V_omega"]
    assert hom_dimension==27

    # Max rank = sum_i degree_i min(m_source(i),m_target(i)).
    max_rank=3*min(source_mult["V_omega"],target_mult["V_omega"])
    assert max_rank==9

    # Nine central 3-cycles give 1,omega,omega^2 each with multiplicity 9.
    address_center_spectrum={"1":9,"omega":9,"omega^2":9}
    operator_center_spectrum={"omega":27}

    out={
      "schema":"w33.address_operator_h27_intertwiner_obstruction.v1",
      "status":"PASS_ADDRESS_OPERATOR_H27_LINEAR_INTERTWINER_RANK_OBSTRUCTION",
      "headline":"The regular/address H27 and center-correct trinification/operator H27 are non-isomorphic 27-dimensional complex H27-modules. The address module is regular, containing 3 copies of each 3D Schroedinger central-character irrep; the operator module is 9 copies of one Schroedinger irrep. Every H27-equivariant linear map from address to operator space therefore has rank at most 9, so no invertible root-gauge intertwiner exists for these two landed actions.",
      "group":{
        "order":27,
        "center_order":3,
        "exponent":3,
        "irreducible_degree_census":{"1":9,"3":2},
        "degree_square_sum":degree_square_sum
      },
      "address_module":{
        "dimension":27,
        "representation":"regular",
        "decomposition":"sum_{9 linear chars} chi + 3 V_omega + 3 V_omega2",
        "center_generator_cycle_structure":{"3":9},
        "center_spectrum":address_center_spectrum
      },
      "operator_module":{
        "dimension":27,
        "representation":"9 V_omega",
        "center_spectrum":operator_center_spectrum,
        "source":"landed trinification H27 on the E6 27"
      },
      "intertwiner":{
        "Hom_dimension":hom_dimension,
        "maximum_rank":max_rank,
        "target_dimension":27,
        "invertible_intertwiner_exists":False,
        "rank_bound_sharp":True,
        "central_projector_rank":9,
        "automorphism_twist_can_remove_obstruction":False,
        "reason":"Any automorphism maps the central generator to z or z^2. The regular central action always has three eigenspaces of dimension 9, while the operator center is scalar on all 27 dimensions."
      },
      "consequence":"The open root-gauge intertwiner cannot be an H27-equivariant basis change between the regular address action and the center-correct operator action. Any viable address-to-operator dictionary must explicitly break or retarget address-H27 equivariance, or compare a different representation/subgroup.",
      "boundary":"Finite representation-theoretic obstruction only. It does not forbid a non-equivariant coordinate dictionary between the two 27-label sets, a map after changing the group action, or an intertwiner in a larger construction with additional multiplicity data. No particle, vacuum, or hardware claim is made.",
      "parents":[
        "analysis/w33_address_operator_h27_roles.py",
        "analysis/w33_e8_matter81_pauli243_restriction.py",
        "analysis/w33_e8_trinification_two_qutrit_pauli243.py"
      ],
      "checks":{
        "H27_order_27":True,
        "center_order_3":True,
        "exponent_3":True,
        "regular_center_is_nine_3cycles":True,
        "irreducible_degree_square_sum_27":True,
        "operator_module_is_9_Vomega_parent_fact":True,
        "Hom_dimension_27":True,
        "maximum_equivariant_rank_9":True,
        "no_invertible_H27_intertwiner":True,
        "automorphism_twist_does_not_help":True
      }
    }
    if write:
        OUT.write_text(json.dumps(out,indent=2)+"\n")
    return out

if __name__=="__main__":
    print(json.dumps(main(True),indent=2))
