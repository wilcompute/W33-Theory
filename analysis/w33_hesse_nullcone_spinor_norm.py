#!/usr/bin/env python3
"""Determinant / spinor-norm character weld for the Hesse null-cone module.

Parent:
    data/w33_hesse_nullcone_adjoint_intertwiner.json

The explicit adjoint lift rho: GL(2,3) -> SO(Q) has kernel {+I,-I}.
This verifier resolves the apparent parity mismatch:
    det(g)=-1 in 2D phase space
but
    det(rho(g))=+1 in the 3D orthogonal module.

The correct 3D index-two invariant is the spinor norm.

For the quadratic form q(v)=(1/2) v^T Q v over F3, a reflection r_v has
spinor square-class q(v). Every element of SO(Q) is exhaustively decomposed
as a product of two reflections, and all such decompositions are checked to
give the same square-class. The result is

    spinor_norm(rho(g)) = det(g) in F3^*/(F3^*)^2 = {1,2}

for all 48 elements g of GL(2,3).

Consequently:
    rho(SL(2,3)) = Omega(Q), order 12 ~= A4,
    rho(GL(2,3)) = SO(Q),    order 24 ~= S4.

The anti-linear qutrit reflection therefore has nontrivial spinor norm even
though its 3D determinant is +1. This is finite orthogonal geometry, not a
continuum Lorentzian Spin/Pin or spacetime claim.
"""
from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT_SCRIPT = ROOT / "analysis/w33_hesse_nullcone_adjoint_intertwiner.py"
PARENT_DATA = ROOT / "data/w33_hesse_nullcone_adjoint_intertwiner.json"
OUT = ROOT / "data/w33_hesse_nullcone_spinor_norm.json"
MOD = 3


def load_parent_module():
    spec = importlib.util.spec_from_file_location("w33_hesse_adjoint", PARENT_SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def flatten(M):
    return tuple(x for row in M for x in row)


def q_value(v, Q, m):
    # 1/2 = 2 in F3.
    return m.mod(2 * sum(v[i] * Q[i][j] * v[j] for i in range(3) for j in range(3)))


def reflection(v, Q, m):
    q = q_value(v, Q, m)
    assert q in (1, 2)
    iq = 1 if q == 1 else 2
    # Column convention:
    # r_v(x)=x-(B(x,v)/q(v))*v, B(x,v)=x^T Q v.
    return tuple(
        tuple(
            m.mod(
                (1 if i == j else 0)
                - iq * v[i] * sum(v[k] * Q[k][j] for k in range(3))
            )
            for j in range(3)
        )
        for i in range(3)
    )


def main(write=True):
    m = load_parent_module()
    parent = json.loads(PARENT_DATA.read_text())
    replay = m.main(write=False)
    assert replay == parent

    Q = tuple(tuple(row) for row in parent["sl2_model"]["hull_gram"])
    P = tuple(tuple(row) for row in parent["sl2_model"]["basis_change_P"])
    Pinv = tuple(tuple(row) for row in parent["sl2_model"]["basis_change_P_inverse"])
    rays = tuple(tuple(v) for v in json.loads(
        (ROOT / "data/w33_extended_clifford_hesse_null_cone.json").read_text()
    )["affine_hull_null_cone"]["isotropic_projective_rays"])

    GL2 = []
    for e in itertools.product(range(3), repeat=4):
        g = ((e[0], e[1]), (e[2], e[3]))
        if m.det2(g):
            GL2.append(g)
    assert len(GL2) == 48

    lift_det = {}
    for g in GL2:
        R = m.rho(g, P, Pinv)
        key = flatten(R)
        d = m.det2(g)
        if key in lift_det:
            assert lift_det[key] == d
        lift_det[key] = d
    assert len(lift_det) == 24
    assert list(lift_det.values()).count(1) == 12
    assert list(lift_det.values()).count(2) == 12

    nonsingular = []
    reflection_by_key = {}
    for v in itertools.product(range(3), repeat=3):
        if v == (0, 0, 0):
            continue
        q = q_value(v, Q, m)
        if q:
            R = reflection(v, Q, m)
            assert m.matmul(m.matmul(m.transpose(R), Q), R) == Q
            assert m.det3(R) == 2
            nonsingular.append((v, q, R))
            reflection_by_key.setdefault(flatten(R), (v, q, R))
    assert len(nonsingular) == 18
    assert len(reflection_by_key) == 9
    reflections = list(reflection_by_key.values())

    SO = []
    for e in itertools.product(range(3), repeat=9):
        M = (e[0:3], e[3:6], e[6:9])
        if m.det3(M) == 1 and m.matmul(m.matmul(m.transpose(M), Q), M) == Q:
            SO.append(M)
    assert len(SO) == 24
    assert {flatten(M) for M in SO} == set(lift_det)

    spinor = {}
    decomposition_counts = {}
    I3 = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    for M in SO:
        key = flatten(M)
        values = []
        decs = []
        if M == I3:
            values.append(1)
            decs.append(("identity",))
        for v, qv, Rv in reflections:
            for w, qw, Rw in reflections:
                if m.matmul(Rv, Rw) == M:
                    values.append(m.mod(qv * qw))
                    decs.append((v, qv, w, qw))
        assert values
        assert len(set(values)) == 1
        spinor[key] = values[0]
        decomposition_counts[key] = len(decs)

    assert list(spinor.values()).count(1) == 12
    assert list(spinor.values()).count(2) == 12
    assert spinor == lift_det

    omega = {k for k, value in spinor.items() if value == 1}
    sl_image = {
        flatten(m.rho(g, P, Pinv))
        for g in GL2
        if m.det2(g) == 1
    }
    assert len(omega) == len(sl_image) == 12
    assert omega == sl_image

    kappa = ((2, 0), (0, 1))
    Rk = m.rho(kappa, P, Pinv)
    kkey = flatten(Rk)
    assert m.det2(kappa) == 2
    assert m.det3(Rk) == 1
    assert spinor[kkey] == 2
    assert m.ray_perm(Rk, rays) == (0, 1, 3, 2)

    v = (1, 1, 0)
    w = (1, 2, 0)
    Rv = reflection(v, Q, m)
    Rw = reflection(w, Q, m)
    assert q_value(v, Q, m) == 1
    assert q_value(w, Q, m) == 2
    assert m.matmul(Rv, Rw) == Rk

    out = {
        "schema": "w33.hesse_nullcone_spinor_norm.v1",
        "status": "PASS_QUTRIT_DETERMINANT_CHARACTER_EQUALS_HULL_SPINOR_NORM",
        "headline": (
            "The factor-two Clifford/Hesse extension has an exact orthogonal meaning. "
            "Under the explicit adjoint lift rho: GL(2,3)->SO(Q), the 2D determinant "
            "character equals the 3D spinor-norm square-class for every lift. Hence "
            "SL(2,3)/{+/-I}=Omega(Q)~=A4 and GL(2,3)/{+/-I}=SO(Q)~=S4."
        ),
        "quadratic_form": {
            "gram": [list(row) for row in Q],
            "q_definition": "q(v)=(1/2) v^T Q v over F3, with 1/2=2",
            "nonzero_square_classes": {"square": 1, "nonsquare": 2},
            "nonsingular_vector_count": len(nonsingular),
            "projective_reflection_count": len(reflections),
        },
        "spinor_norm": {
            "definition_used": (
                "For a reflection r_v, theta(r_v) is the square-class of q(v); "
                "theta is multiplicative on reflection products."
            ),
            "SO_order": 24,
            "trivial_class_count": list(spinor.values()).count(1),
            "nontrivial_class_count": list(spinor.values()).count(2),
            "every_SO_element_has_two_reflection_decomposition": True,
            "all_decompositions_consistent": True,
            "minimum_decomposition_count": min(decomposition_counts.values()),
            "maximum_decomposition_count": max(decomposition_counts.values()),
        },
        "character_weld": {
            "identity": "spinor_norm(rho(g)) = det(g) mod (F3^*)^2 for all g in GL(2,3)",
            "GL2_elements_checked": 48,
            "rho_image_elements_checked": 24,
            "kernel_spinor_norm_order": len(omega),
            "kernel_equals_SL2_image_mod_center": True,
            "Omega_Q": "rho(SL(2,3)) ~= PSL(2,3) ~= A4",
            "SO_Q": "rho(GL(2,3)) ~= PGL(2,3) ~= S4",
        },
        "antilinear_reflection": {
            "kappa": [[2, 0], [0, 1]],
            "det_kappa_mod3": 2,
            "rho_kappa": [list(row) for row in Rk],
            "det_rho_kappa_mod3": 1,
            "spinor_norm_rho_kappa": 2,
            "null_ray_permutation": [0, 1, 3, 2],
            "explicit_reflection_factorization": {
                "v": list(v),
                "q_v": 1,
                "w": list(w),
                "q_w": 2,
                "identity": "rho(kappa)=r_v r_w",
                "spinor_product": 2,
            },
        },
        "interpretation": (
            "The determinant-minus-one anti-linear qutrit operation becomes a "
            "determinant-one orthogonal transformation whose nontrivial C2 label is "
            "the spinor norm. This is the correct finite-orthogonal replacement for "
            "the earlier loose phrase 'orientation reversal'."
        ),
        "boundary": (
            "Spinor norm here is the standard square-class invariant of a 3D quadratic "
            "space over F3. It does not by itself define physical fermionic spin, a "
            "continuum Spin/Pin structure, Lorentz symmetry, CPT, or spacetime parity."
        ),
        "parents": [
            "data/w33_hesse_nullcone_adjoint_intertwiner.json",
            "data/w33_extended_clifford_hesse_null_cone.json",
        ],
        "checks": {
            "nine_projective_reflections": True,
            "all_24_SO_elements_decompose_into_reflection_pairs": True,
            "spinor_norm_well_defined_across_all_pair_decompositions": True,
            "spinor_norm_distribution_12_plus_12": True,
            "determinant_character_descends_through_plus_minus_I": True,
            "spinor_norm_equals_GL2_determinant_all_48": True,
            "Omega_equals_SL2_projective_image_order12": True,
            "kappa_has_nontrivial_spinor_norm": True,
            "kappa_has_3d_determinant_plus_one": True,
            "explicit_kappa_reflection_factorization": True,
            "continuum_spin_not_overclaimed": True,
        },
    }
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    return out


if __name__ == "__main__":
    print(json.dumps(main(True), indent=2))
