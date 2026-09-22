#!/usr/bin/env python3
"""Normalize the explicit E8-derived Pauli243 representation by full Sp(4,3).

This theorem is deliberately representation-level.

The E8 construction supplies G=3_+^(1+4) with distinguished projective basis
    (X_int, X_ext, Z_int, Z_ext)
and commutator symplectic form on F3^4.  Independently, the repository's exact
two-qutrit Clifford ABI supplies transvection matrices and 9x9 phase-specified
unitaries U(v,lambda) satisfying
    U D_x U^dagger = D_{T(v,lambda)x}
with no residual Pauli phase.

We use the four compressed transvection axes from BT1228 and verify:
  * they generate Sp(4,3), order 51840;
  * each preserves the exact E8-derived commutator form;
  * each 9x9 unitary conjugates all 81 Weyl labels according to its matrix;
  * their projective action on the 40 E8-derived W33 rays matches the canonical
    W33 symplectic action.

Therefore the representation normalizer is
    3_+^(1+4) : Sp(4,3)
(up to the scalar phase convention of the Clifford representation).

Firewall: this does NOT prove every Clifford lift is an element of compact E8,
nor that N_E8(G) equals this full semidirect product.
"""
from __future__ import annotations
import importlib.util, json, sys
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
for p in (ROOT,ROOT/"analysis"):
    if str(p) not in sys.path: sys.path.insert(0,str(p))
OUT=ROOT/"data/w33_e8_pauli243_sp43_representation_normalizer.json"

from w33_exact_eisenstein import (
    identity_matrix,
    matrix_add,
    matrix_dagger,
    matrix_multiply,
    matrix_scale,
    omega_power,
    zero_matrix,
)

Q=3
HALF=2
DIM=9

def load(path,name):
    s=importlib.util.spec_from_file_location(name,path); assert s and s.loader
    m=importlib.util.module_from_spec(s); sys.modules[name]=m; s.loader.exec_module(m); return m

def exact_weyl(v):
    """Odd-prime two-qutrit Weyl matrix over Q(omega), exactly."""
    q1,q2,p1,p2=(int(x)%Q for x in v)
    phase=omega_power(HALF*(q1*p1+q2*p2))
    matrix=zero_matrix(DIM,DIM)
    for x1 in range(Q):
        for x2 in range(Q):
            source=Q*x1+x2
            target=Q*((x1+q1)%Q)+(x2+q2)%Q
            matrix[target][source]=phase*omega_power(p1*x1+p2*x2)
    return matrix

def exact_transvection_unitary(v,lam):
    """Spectral-projector transvection lift over Q(omega), exactly."""
    if int(lam) not in (1,2): raise ValueError("lambda must be 1 or 2")
    displacement=exact_weyl(v)
    powers=(
        identity_matrix(DIM),
        displacement,
        matrix_multiply(displacement,displacement),
    )
    unitary=zero_matrix(DIM,DIM)
    for k in range(Q):
        projector=zero_matrix(DIM,DIM)
        for t in range(Q):
            projector=matrix_add(
                projector,
                matrix_scale(omega_power(-k*t),powers[t]),
            )
        projector=matrix_scale(Fraction(1,Q),projector)
        eigenphase=omega_power(HALF*int(lam)*k*k)
        unitary=matrix_add(unitary,matrix_scale(eigenphase,projector))
    return unitary

def main(write=True):
    bridge=json.loads((ROOT/"data/w33_e8_pauli243_projective_w33_bridge.json").read_text())
    assert bridge["status"]=="PASS_EXPLICIT_E8_PAULI243_PROJECTIVE_QUOTIENT_IS_CANONICAL_W33"

    bt=load(ROOT/"analysis/bt1228_sp43_compressed_generators.py","bt1228_sp43")
    cliff=load(ROOT/"analysis/w33_qutrit_clifford_phase_displacement_lift.py","cliffphase")

    axes=list(bt.GENERATOR_VECTORS)
    mats=[bt.transvection(v) for v in axes]
    group=bt.generate(mats)
    assert len(group)==51840

    # Convert BT row-major matrices to Clifford tuple-of-tuples.
    def nested(M): return tuple(tuple(M[4*i+j] for j in range(4)) for i in range(4))

    points=[tuple(p) for p in cliff.GEOMETRY.points]
    assert len(points)==40

    # Exact E8-derived symplectic form is the same canonical form used by ABI.
    def omega(u,v):
        return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%3
    assert all(omega(u,v)==cliff.symplectic(u,v) for u in points for v in points)

    # Every compressed generator preserves omega on all 81x81 vector pairs.
    vectors=[(a,b,c,d) for a in range(3) for b in range(3) for c in range(3) for d in range(3)]
    for Mflat in mats:
        M=nested(Mflat)
        assert all(omega(cliff.act(M,u),cliff.act(M,v))==omega(u,v) for u in vectors for v in vectors)

    # Phase-specified unitary lift: use lambda=1 transvection around each axis.
    # BT1228 and the ABI use the same formula I+v(Jv)^T in this coordinate gauge.
    unitary_checks=0
    exact_unitarity_checks=0
    for axis,Mflat in zip(axes,mats):
        M=nested(Mflat)
        Mabi=cliff.transvection(axis,1)
        assert M==Mabi
        U=exact_transvection_unitary(axis,1)
        Ud=matrix_dagger(U)
        assert matrix_multiply(Ud,U)==identity_matrix(DIM)
        exact_unitarity_checks+=1
        for x in vectors:
            lhs=matrix_multiply(matrix_multiply(U,exact_weyl(x)),Ud)
            rhs=exact_weyl(cliff.act(M,x))
            assert lhs==rhs
            unitary_checks+=1
    assert unitary_checks==4*81
    assert exact_unitarity_checks==4

    # Projective ray permutations from each generator.
    def norm(v):
        for x in v:
            if x%3:
                inv=1 if x%3==1 else 2
                return tuple(inv*y%3 for y in v)
        raise ValueError
    pindex={p:i for i,p in enumerate(points)}
    perms=[]
    for Mflat in mats:
        M=nested(Mflat)
        perm=tuple(pindex[norm(cliff.act(M,p))] for p in points)
        assert sorted(perm)==list(range(40))
        perms.append(perm)

    out={
      "schema":"w33.e8_pauli243_sp43_representation_normalizer.v1",
      "status":"PASS_E8_DERIVED_PAULI243_REPRESENTATION_NORMALIZED_BY_FULL_SP43_CLIFFORD",
      "headline":"The specific E8-derived Pauli243 representation, in its inherited basis (X_int,X_ext,Z_int,Z_ext), is normalized by the full two-qutrit Clifford symplectic group Sp(4,3). Four explicit BT1228 transvections generate all 51840 symplectic matrices; each preserves the E8-derived commutator form and its phase-specified 9x9 unitary conjugates every one of the 81 Weyl labels exactly to the transformed label. Their projective permutations act on the same 40 rays as the certified E8->W33 bridge.",
      "basis":["X_int","X_ext","Z_int","Z_ext"],
      "compressed_generators":{
        "axes":[list(v) for v in axes],
        "count":4,
        "generated_Sp43_order":len(group),
        "projective_permutations_on_40":[list(p) for p in perms]
      },
      "unitary_lift":{
        "dimension":9,
        "coefficient_field":"Q(omega), omega^2+omega+1=0, exact Fraction pairs",
        "weyl_labels_checked_per_generator":81,
        "total_conjugation_checks":unitary_checks,
        "exact_unitarity_checks":exact_unitarity_checks,
        "all_matrix_residuals_exactly_zero":True,
        "rule":"U_T D_x U_T^dagger = D_{T x}",
        "residual_pauli_phase":"none in the certified odd-prime Weyl convention"
      },
      "normalizer":{
        "representation_level_structure":"3_+^(1+4) : Sp(4,3)",
        "Pauli_order":243,
        "Sp43_order":51840,
        "semidirect_order":243*51840,
        "projective_clifford_action":"Sp(4,3) on F3^4; center +/-I acts trivially on W33 rays"
      },
      "E8_firewall":{
        "full_clifford_representation_normalizer_proved":True,
        "all_clifford_lifts_proved_inside_compact_E8":False,
        "N_E8_of_this_specific_Pauli243_identified":False,
        "statement":"The Pauli subgroup was constructed inside E8. The full Sp(4,3) Clifford action is proved as a normalizer of its 9D Schrödinger representation and of the E8-derived projective phase space. An internal-E8 realization of every Clifford lift remains a separate subgroup-embedding problem."
      },
      "parents":[
        "data/w33_e8_pauli243_projective_w33_bridge.json",
        "analysis/bt1228_sp43_compressed_generators.py",
        "analysis/w33_qutrit_clifford_phase_displacement_lift.py"
      ],
      "checks":{
        "four_transvections_generate_Sp43":True,
        "all_generators_preserve_E8_commutator_form":True,
        "all_324_unitary_Weyl_conjugations_checked":True,
        "all_four_transvection_lifts_exactly_unitary_over_Qomega":True,
        "projective_actions_are_W33_ray_permutations":True,
        "internal_E8_normalizer_overclaim_blocked":True
      }
    }
    if write: OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
    return out

if __name__=="__main__": main(True)
