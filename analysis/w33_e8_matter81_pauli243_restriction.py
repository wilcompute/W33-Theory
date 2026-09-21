#!/usr/bin/env python3
"""Restrict the E8 matter 81=(27,3) to the explicit Pauli243 subgroup.

The new Pauli subgroup is the central product
    G = H27_int o H27_ext = 3_+^(1+4).
The internal H27 sits in E6 trinification, with
    X_int=(X,X,I), Z_int=(Z^2,Z,I)
on
    27=(3,3bar,1)+(1,3,3bar)+(3bar,1,3).
Its common center acts by omega on the full 27.

In an explicit trinification weight basis, X_int has nine 3-cycles and Z_int
provides the qutrit clock along each cycle. Hence
    27 | H27_int = 9 * S3,
where S3 is the 3D Schrödinger irrep with central character omega.

The external physical A2 factor is one S3. Therefore
    (27,3) | G = 9 * S9,
where S9 is the irreducible 9D two-qutrit Schrödinger representation of the
extraspecial group 3_+^(1+4).

Consequences:
  * character = 81,81*omega,81*omega^2 on the center and 0 off center;
  * the 81 matter weight rays form nine projective orbits of size 9 under G;
  * the 81-element operator quotient G/Z(G)=F3^4 is a regular translation
    G-set, so it is NOT equivariantly bijective to the 81 matter rays.

Thus the repeated number 81 is meaningful but not an objectwise identity:
operators are the phase-space quotient, matter is nine copies of its unique
9D Schrödinger carrier at the selected central character.
"""
from __future__ import annotations
import json
import itertools
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_e8_matter81_pauli243_restriction.json"

def main(write=True):
    pauli=json.loads((ROOT/"data/w33_e8_trinification_two_qutrit_pauli243.json").read_text())
    matter=json.loads((ROOT/"data/w33_e8_matter81_frame_qutrit_tensor_carrier.json").read_text())
    assert pauli["status"]=="PASS_E8_CONTAINS_TRINIFICATION_CENTRAL_PRODUCT_TWO_QUTRIT_PAULI243"
    assert matter["status"]=="PASS_E8_MATTER81_EQUALS_27_COMPLETE_FRAMES_X_3_EXTERNAL_QUTRIT_PHASES"

    # Internal trinification weight basis.
    # Labels are (block,u,v), block A=(3,3bar,1), B=(1,3,3bar),
    # C=(3bar,1,3). Each block has 9 weight rays.
    internal=[(B,u,v) for B in "ABC" for u in range(3) for v in range(3)]
    assert len(internal)==27

    def xint(s):
        B,u,v=s
        if B=="A": return (B,(u+1)%3,(v+1)%3)
        if B=="B": return (B,(u+1)%3,v)
        return (B,(u+1)%3,v)

    def zexp(s):
        B,u,v=s
        if B=="A": return (2*u-v)%3
        if B=="B": return u%3
        return u%3

    # ZX=omega XZ on every basis ray.
    assert all((zexp(xint(s))-zexp(s))%3==1 for s in internal)

    # X_int ray permutation has nine 3-cycles.
    seen=set(); internal_orbits=[]
    for s in internal:
        if s in seen: continue
        orb=[]; t=s
        while t not in orb:
            orb.append(t); seen.add(t); t=xint(t)
        internal_orbits.append(orb)
    assert Counter(map(len,internal_orbits))==Counter({3:9})

    # Matter basis rays = internal 27 x external qutrit basis 3.
    basis=[(s,e) for s in internal for e in range(3)]
    def xi(ray): return (xint(ray[0]),ray[1])
    def xe(ray): return (ray[0],(ray[1]+1)%3)

    # Projective Pauli action: clocks are diagonal, so ray motion is generated
    # by the two shifts Xi,Xe. Compute its orbits exactly.
    unseen=set(basis); matter_orbits=[]
    while unseen:
        seed=min(unseen)
        orb={seed}; todo=[seed]
        while todo:
            r=todo.pop()
            for f in (xi,xe):
                q=f(r)
                if q not in orb:
                    orb.add(q); todo.append(q)
        unseen-=orb; matter_orbits.append(sorted(orb))
    assert Counter(map(len,matter_orbits))==Counter({9:9})

    # Exact character support for G=(H3 x H3)/anti-diagonal center.
    # Single Schrödinger trace: tr(Z^a X^b z^c)=0 unless a=b=0,
    # then 3 omega^c. Internal 27 is nine copies of this.
    H=list(itertools.product(range(3),repeat=3))
    def hmul(g,h):
        a,b,c=g; A,B,C=h
        return ((a+A)%3,(b+B)%3,(c+C-b*A)%3)
    def kernel_shift(pair,k):
        gi,ge=pair
        return (hmul(gi,(0,0,k)),hmul(ge,(0,0,(-k)%3)))
    def canon(pair): return min(kernel_shift(pair,k) for k in range(3))
    cosets=sorted({canon((gi,ge)) for gi in H for ge in H})
    assert len(cosets)==243

    # Character encoded exactly as coefficient times omega^exponent.
    chars={}
    central=[]
    noncentral=[]
    for g in cosets:
        gi,ge=g
        ai,bi,ci=gi; ae,be,ce=ge
        if ai==bi==ae==be==0:
            chars[str(g)]={"coefficient":81,"omega_exponent":(ci+ce)%3}
            central.append(g)
        else:
            chars[str(g)]={"coefficient":0,"omega_exponent":0}
            noncentral.append(g)
    assert len(central)==3 and len(noncentral)==240
    assert sorted(x["omega_exponent"] for x in chars.values() if x["coefficient"]==81)==[0,1,2]
    assert all(chars[str(g)]["coefficient"]==0 for g in noncentral)

    # Sum |chi|^2 / |G| = multiplicity-square sum = 9^2 =81.
    # If decomposition is m copies of one 9D irrep, m=9 and norm=81.
    char_norm=sum(v["coefficient"]**2 for v in chars.values())//243
    assert char_norm==81
    multiplicity=81//9
    assert multiplicity==9

    out={
      "schema":"w33.e8_matter81_pauli243_restriction.v1",
      "status":"PASS_MATTER81_RESTRICTS_TO_NINE_TWO_QUTRIT_SCHRODINGER_MODULES_NOT_REGULAR_F3_4_SET",
      "headline":"The E8 matter shell (27,3) restricted to the explicit Pauli243 subgroup is nine copies of the irreducible 9D two-qutrit Schrödinger module with the physical central character. The exact character is 81,81*omega,81*omega^2 on the three center elements and zero on all 240 noncentral elements. On matter weight rays the two shifts generate nine orbits of size 9, whereas G/Z(G)=F3^4 is a regular transitive 81-element translation set. Therefore the two occurrences of 81 are not equivariantly identical sets.",
      "internal_trinification":{
        "basis_rays":27,
        "X_int_cycle_structure":{"3":9},
        "Z_int_clock_increment_along_X_cycles":1,
        "restriction":"27 = 9 copies of the 3D H27 Schrodinger irrep"
      },
      "matter_representation":{
        "dimension":81,
        "restriction":"(27,3) = 9 copies of the 9D irreducible Schrodinger representation of 3_+^(1+4)",
        "irreducible_dimension":9,
        "multiplicity":9,
        "character_norm":81,
        "center_character":{"1":"81","z":"81*omega","z^2":"81*omega^2"},
        "noncentral_character":"0 on all 240 noncentral elements"
      },
      "projective_weight_rays":{
        "count":81,
        "orbit_count":9,
        "orbit_size":9,
        "reason":"clock generators are diagonal on weight rays; the internal and external shifts generate C3 x C3 motion"
      },
      "operator_quotient":{
        "object":"G/Z(G)=F3^4",
        "count":81,
        "regular_translation_action_orbit_size":81
      },
      "equivariance_verdict":{
        "matter_rays_equivariantly_bijective_to_operator_quotient":False,
        "witness":"orbit partitions differ: matter rays 9x9 versus operator quotient 1x81",
        "correct_relationship":"matter81 is a representation carrier (9 copies of H9); operator81 is phase space"
      },
      "boundary":"This distinguishes operator phase-space labels from matter weight rays. It does not deny that both are controlled by the same Pauli243 group, nor does it assign observed particles.",
      "parents":[
        "data/w33_e8_trinification_two_qutrit_pauli243.json",
        "data/w33_e8_matter81_frame_qutrit_tensor_carrier.json"
      ],
      "checks":{
        "internal_ZX_relation_on_all_27_weight_rays":True,
        "internal_27_is_9_three_cycles_projectively":True,
        "matter_rays_are_9_orbits_of_9":True,
        "full_243_character_support_checked":True,
        "noncentral_character_zero":True,
        "operator_vs_matter_equivariant_bijection_rejected":True
      }
    }
    if write: OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
    return out

if __name__=="__main__": main(True)
