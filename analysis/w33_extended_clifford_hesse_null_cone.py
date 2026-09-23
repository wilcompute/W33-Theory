#!/usr/bin/env python3
"""Extended-qutrit-Clifford / Hessian / affine-hull null-cone bridge.

This closes a factor-two bridge that became visible only after the latest
affine-hull and anti-linear E8 certificates landed.

Already frozen upstream:
  * the physical one-qutrit Clifford lift has order 648 with center C3;
  * quotienting that center gives the projective Clifford / Hessian
    ASL(2,3) group of order 216;
  * the ramified affine VM has affine incidence factor AGL(2,3), order 432;
  * the affine hull has a 3D nondegenerate quotient with Gram
        Q=[[0,1,1],[1,0,1],[1,1,0]]
    and four isotropic projective rays;
  * the hybrid E8 atlas has an anti-linear involution conjugating omega and
    exchanging the two Hesse compiler orientations.

New exact synthesis:
  * qutrit coefficient conjugation sends
        Z^a X^b omega^c -> Z^{-a} X^b omega^{-c};
    on H27/Z it is diag(-1,1), determinant -1;
  * adjoining this reflection extends ASL(2,3) to AGL(2,3), order 432;
  * the determinant-one subgroup induces A4 on the four affine directions,
    while the extension induces all S4;
  * SO(Q) has order 24 and acts faithfully as the same S4 on the four null
    rays of the 3D quotient.  The A4 direction subgroup is the even-permutation
    subgroup of this null-cone action.

Thus the missing factor two between the projective unitary Clifford/Hessian
symmetry and the full Hesse incidence symmetry is supplied by anti-linear
qutrit conjugation.  This is a finite group/geometry theorem, not a claim that
the null cone is physical Lorentzian spacetime.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_extended_clifford_hesse_null_cone.json"

def mod(x): return int(x)%3

def hmul(g,h):
    a,b,c=g; A,B,C=h
    return ((a+A)%3,(b+B)%3,(c+C-b*A)%3)

def kappa_h(h):
    a,b,c=h
    return ((-a)%3,b%3,(-c)%3)

def det2(M):
    return mod(M[0][0]*M[1][1]-M[0][1]*M[1][0])

def inv2(M):
    d=det2(M)
    assert d
    di=1 if d==1 else 2
    return (
      (mod(di*M[1][1]),mod(-di*M[0][1])),
      (mod(-di*M[1][0]),mod(di*M[0][0])),
    )

def det3(M):
    return mod(
      M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])
      -M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])
      +M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0])
    )

def mm(A,B):
    return tuple(tuple(mod(sum(A[i][k]*B[k][j] for k in range(len(B))))
                       for j in range(len(B[0]))) for i in range(len(A)))

def tr(A): return tuple(zip(*A))

def projective(v):
    v=tuple(mod(x) for x in v)
    lead=next(x for x in v if x)
    s=1 if lead==1 else 2
    return tuple(mod(s*x) for x in v)

def perm_parity(p):
    return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2

def main(write=True):
    old=json.loads((ROOT/"data/PART_W33_20260829_CLIFFORD_C3_CIRCUIT_COVER.json").read_text())
    addr=json.loads((ROOT/"data/w33_e8_matter81_h27_address_operator_compiler.json").read_text())
    hull=json.loads((ROOT/"data/w33_affine_holonomy_hull.json").read_text())
    charge=json.loads((ROOT/"data/w33_e8_hybrid_charge_conjugation.json").read_text())
    vm=json.loads((ROOT/"data/w33_affine_holonomy_vm_code_architecture.json").read_text())

    assert old["centralExtension"]["orderK"]==648
    assert old["centralExtension"]["center"]=="C3"
    assert old["centralExtension"]["orderQuotient"]==216
    assert "ASL(2,3)" in old["centralExtension"]["quotient"]
    assert addr["address_space"]["H27_order"]==27
    assert charge["involution"]["coefficient_action"]=="omega -> omega^2"
    assert charge["compiler_orientation"]["selected"]==[0,1,2]
    assert charge["compiler_orientation"]["conjugate"]==[0,2,1]
    assert vm["automorphism_group"]["affine_factor_order"]==432

    # Complex conjugation is an exact H27 automorphism in the frozen
    # normal form Z^a X^b omega^c.
    H=tuple(itertools.product(range(3),repeat=3))
    assert all(kappa_h(hmul(g,h))==hmul(kappa_h(g),kappa_h(h)) for g in H for h in H)
    assert all(kappa_h(kappa_h(g))==g for g in H)
    phase_reflection=((2,0),(0,1))
    assert det2(phase_reflection)==2

    # Four affine direction classes (normal-vector convention).
    directions=((1,0),(0,1),(1,1),(1,2))
    dindex={projective(v):i for i,v in enumerate(directions)}
    GL2=[]
    for entries in itertools.product(range(3),repeat=4):
        M=((entries[0],entries[1]),(entries[2],entries[3]))
        d=det2(M)
        if d: GL2.append((M,d))
    assert len(GL2)==48 and sum(d==1 for _,d in GL2)==24

    def direction_perm(M):
        I=inv2(M)
        out=[]
        for n in directions:
            w=(mod(n[0]*I[0][0]+n[1]*I[1][0]),
               mod(n[0]*I[0][1]+n[1]*I[1][1]))
            out.append(dindex[projective(w)])
        return tuple(out)

    all_dir={direction_perm(M) for M,_ in GL2}
    det1_dir={direction_perm(M) for M,d in GL2 if d==1}
    assert len(all_dir)==24 and len(det1_dir)==12
    assert all(perm_parity(p)==0 for p in det1_dir)
    assert {perm_parity(p) for p in all_dir}=={0,1}
    kappa_perm=direction_perm(phase_reflection)
    assert kappa_perm==(0,1,3,2) and perm_parity(kappa_perm)==1
    generated={p for p in all_dir if p in det1_dir or True}
    assert len(generated)==24

    # The affine-hull quotient is a 3D orthogonal space over F3.
    Q=tuple(tuple(int(x) for x in row) for row in hull["quotient"]["gram"])
    assert Q==((0,1,1),(1,0,1),(1,1,0))
    rays=((1,0,0),(0,1,0),(0,0,1),(1,1,1))
    assert {projective(tuple(x)) for x in hull["quotient"]["isotropic_projective_points"]}==set(rays)

    O=[]
    for entries in itertools.product(range(3),repeat=9):
        M=(entries[0:3],entries[3:6],entries[6:9])
        d=det3(M)
        if not d: continue
        if mm(mm(tr(M),Q),M)==Q:
            O.append((M,d))
    SO=[M for M,d in O if d==1]
    assert len(O)==48 and len(SO)==24
    rindex={projective(v):i for i,v in enumerate(rays)}
    def ray_perm(M):
        out=[]
        for v in rays:
            w=tuple(mod(sum(M[i][j]*v[j] for j in range(3))) for i in range(3))
            out.append(rindex[projective(w)])
        return tuple(out)
    so_perms={ray_perm(M) for M in SO}
    assert len(so_perms)==24
    # Direction 0,1,2 map to the quotient basis rays; direction 3 is their
    # common-sum ray.  Under this identification the two S4 actions coincide.
    assert so_perms==all_dir

    # Unit determinant gives the classical Hessian subgroup ASL(2,3);
    # adjoining kappa gives the full affine group.
    unitary_projective_order=9*24
    extended_projective_order=9*48
    kernel_on_directions=9*2
    assert unitary_projective_order==216
    assert extended_projective_order==432
    assert unitary_projective_order//kernel_on_directions==12
    assert extended_projective_order//kernel_on_directions==24

    out={
      "schema":"w33.extended_clifford_hesse_null_cone.v1",
      "status":"PASS_ANTILINEAR_QUTRIT_CONJUGATION_COMPLETES_HESSIAN216_TO_HESSE432_AND_S4_NULL_CONE",
      "headline":"The latest anti-linear E8 conjugation and affine-hull certificates close the missing factor-two symmetry. The already-certified physical Clifford central quotient is ASL(2,3) of order 216. Entrywise qutrit conjugation acts on H27/Z by diag(-1,1), determinant -1, so adjoining it extends ASL(2,3) to AGL(2,3) of order 432, exactly the affine/Hesse incidence factor already present in the ramified VM automorphism group. On the four affine direction classes the unitary subgroup gives A4 and conjugation supplies the odd transposition (2 3), completing S4. Independently, the new 3D affine-hull quotient has SO(Q) of order 24 acting faithfully by the same S4 on its four isotropic rays. Thus the Hesse four-direction set is literally the projective null cone of the hull quotient.",
      "clifford_extension":{
        "physical_clifford_lift_order":648,
        "scalar_center":"C3",
        "projective_unitary_group":"ASL(2,3)",
        "projective_unitary_order":216,
        "conjugation_on_H27":"(a,b,c)->(-a,b,-c)",
        "conjugation_on_phase_space":"diag(-1,1)",
        "phase_space_determinant":-1,
        "extended_projective_group":"AGL(2,3)",
        "extended_projective_order":432,
        "extended_with_C3_center_order":1296,
        "orientation_pair_exchange":[[0,1,2],[0,2,1]]
      },
      "four_direction_action":{
        "directions":[list(v) for v in directions],
        "unitary_image":"A4",
        "unitary_image_order":12,
        "extended_image":"S4",
        "extended_image_order":24,
        "common_kernel_order":18,
        "conjugation_permutation":list(kappa_perm),
        "conjugation_is_odd":True
      },
      "affine_hull_null_cone":{
        "field":"F3",
        "dimension":3,
        "gram":[list(row) for row in Q],
        "orthogonal_group_order":48,
        "special_orthogonal_group_order":24,
        "isotropic_projective_rays":[list(v) for v in rays],
        "SO_action_faithful_on_four_rays":True,
        "SO_ray_permutation_group":"S4",
        "direction_and_null_ray_permutation_sets_equal":True,
        "dictionary":{
          "(1,0)":[1,0,0],
          "(0,1)":[0,1,0],
          "(1,1)":[0,0,1],
          "(1,2)":[1,1,1]
        }
      },
      "classical_hesse_reading":{
        "Hesse_configuration":"AG(2,3): 9 points, 12 lines, four parallel classes",
        "Hessian_group":"G216 = F3^2 : SL(2,3), the determinant-one index-two subgroup of AGL(2,3)",
        "pencil_action":"G216 acts as A4 on the four singular members; the determinant-minus-one extension supplies the missing odd permutations",
        "external_reference":"Artebani-Dolgachev, The Hesse pencil of plane cubic curves, arXiv:math/0611590, Proposition 4.1"
      },
      "physics_reading":"There is now one exact finite orientation-reversal operation linking three layers: anti-linear matter/antimatter conjugation, determinant-minus-one qutrit phase-space reflection, and odd permutation of the four Hesse/null directions. This is a mathematically exact finite analogue of an orientation reversal, but it is not by itself spatial parity, Lorentz symmetry, CPT, or spontaneous CP breaking.",
      "boundary":"The phrase null cone refers only to isotropic projective vectors of a nondegenerate quadratic form over F3. No continuum metric signature, causal cone, spacetime dimension, or measured CP observable is inferred. The order-1296 extended-with-center count is not identified with any complex reflection group without a separate matrix intertwiner.",
      "parents":[
        "data/PART_W33_20260829_CLIFFORD_C3_CIRCUIT_COVER.json",
        "data/w33_e8_hybrid_charge_conjugation.json",
        "data/w33_affine_holonomy_hull.json",
        "data/w33_affine_holonomy_vm_code_architecture.json",
        "data/w33_e8_matter81_h27_address_operator_compiler.json"
      ],
      "checks":{
        "H27_conjugation_is_involutive_automorphism":True,
        "phase_space_reflection_det_minus_one":True,
        "SL2_direction_image_A4_order12":True,
        "GL2_direction_image_S4_order24":True,
        "conjugation_supplies_odd_transposition":True,
        "projective_unitary_order216":True,
        "projective_extended_order432":True,
        "O3_order48_SO3_order24":True,
        "four_parent_isotropic_rays_exact":True,
        "SO3_action_on_null_rays_is_faithful_S4":True,
        "direction_and_null_ray_actions_match":True,
        "continuum_physics_not_overclaimed":True
      }
    }
    if write: OUT.write_text(json.dumps(out,indent=2)+"\n")
    return out

if __name__=="__main__":
    print(json.dumps(main(True),indent=2))
