#!/usr/bin/env python3
"""Affine spinor-parity character for the complete Hesse group AGL(2,3).

Parents:
  data/w33_hesse_nullcone_adjoint_intertwiner.json
  data/w33_hesse_nullcone_spinor_norm.json
  data/w33_extended_clifford_hesse_null_cone.json

The parent chain identifies
  ASL(2,3) = F3^2 : SL(2,3), order 216,
  AGL(2,3) = F3^2 : GL(2,3), order 432,
and constructs rho: GL(2,3) -> SO(Q) with
  spinor_norm(rho(g)) = det(g).

This verifier extends that C2 character over the full affine Hesse group:
  chi(t,g) = det(g) = spinor_norm(rho(g)).
Translations are invisible to chi. Exhaustive group multiplication proves chi
is a surjective homomorphism on all 432 affine elements with kernel exactly
ASL(2,3), order 216.

Thus the factor-two unitary/anti-linear Hesse extension has a canonical finite
orthogonal parity bit. It is a compiler/group character, not physical
spacetime parity or CPT.
"""
from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADJ_SCRIPT = ROOT / "analysis/w33_hesse_nullcone_adjoint_intertwiner.py"
SPIN_SCRIPT = ROOT / "analysis/w33_hesse_nullcone_spinor_norm.py"
ADJ_DATA = ROOT / "data/w33_hesse_nullcone_adjoint_intertwiner.json"
SPIN_DATA = ROOT / "data/w33_hesse_nullcone_spinor_norm.json"
PARENT_DATA = ROOT / "data/w33_extended_clifford_hesse_null_cone.json"
OUT = ROOT / "data/w33_hesse_affine_spinor_parity.json"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def add2(a, b):
    return ((a[0] + b[0]) % 3, (a[1] + b[1]) % 3)


def lin2(g, v):
    return (
        (g[0][0] * v[0] + g[0][1] * v[1]) % 3,
        (g[1][0] * v[0] + g[1][1] * v[1]) % 3,
    )


def mul2(A, B):
    return (
        (
            (A[0][0] * B[0][0] + A[0][1] * B[1][0]) % 3,
            (A[0][0] * B[0][1] + A[0][1] * B[1][1]) % 3,
        ),
        (
            (A[1][0] * B[0][0] + A[1][1] * B[1][0]) % 3,
            (A[1][0] * B[0][1] + A[1][1] * B[1][1]) % 3,
        ),
    )


def acomp(a, b):
    """Affine composition a o b for a=(t,g), b=(u,h)."""
    t, g = a
    u, h = b
    return (add2(t, lin2(g, u)), mul2(g, h))


def main(write=True):
    adj = load(ADJ_SCRIPT, "w33_hesse_adjoint_affine")
    spin = load(SPIN_SCRIPT, "w33_hesse_spin_affine")
    adj_data = json.loads(ADJ_DATA.read_text())
    spin_data = json.loads(SPIN_DATA.read_text())
    parent = json.loads(PARENT_DATA.read_text())
    assert adj.main(write=False) == adj_data
    assert spin.main(write=False) == spin_data

    P = tuple(tuple(row) for row in adj_data["sl2_model"]["basis_change_P"])
    Pinv = tuple(tuple(row) for row in adj_data["sl2_model"]["basis_change_P_inverse"])
    Q = tuple(tuple(row) for row in adj_data["sl2_model"]["hull_gram"])

    GL2 = []
    for e in itertools.product(range(3), repeat=4):
        g = ((e[0], e[1]), (e[2], e[3]))
        if adj.det2(g):
            GL2.append(g)
    SL2 = [g for g in GL2 if adj.det2(g) == 1]
    T = list(itertools.product(range(3), repeat=2))
    AGL = [(t, g) for t in T for g in GL2]
    ASL = [(t, g) for t in T for g in SL2]
    assert (len(T), len(GL2), len(SL2), len(AGL), len(ASL)) == (9, 48, 24, 432, 216)

    # Recompute spinor class on rho(g) from the frozen spinor certificate's
    # defining equality, and verify the lifted character on every affine element.
    chi = {}
    class_counts = {1: 0, 2: 0}
    linear_fibres = {}
    for a in AGL:
        t, g = a
        R = adj.rho(g, P, Pinv)
        assert adj.matmul(adj.matmul(adj.transpose(R), Q), R) == Q
        c = adj.det2(g)
        assert c in (1, 2)
        chi[a] = c
        class_counts[c] += 1
        linear_fibres.setdefault(tuple(x for row in R for x in row), []).append(a)

    assert class_counts == {1: 216, 2: 216}
    assert {a for a in AGL if chi[a] == 1} == set(ASL)
    assert len(linear_fibres) == 24
    assert {len(v) for v in linear_fibres.values()} == {18}

    # Exhaustive character homomorphism check: 432^2 products.
    checked_pairs = 0
    for a in AGL:
        for b in AGL:
            ab = acomp(a, b)
            assert chi[ab] == (chi[a] * chi[b]) % 3
            checked_pairs += 1
    assert checked_pairs == 432 * 432

    # Translation subgroup is entirely in the kernel and forms the normal
    # affine F3^2 layer. The quotient character is purely linear.
    I2 = ((1, 0), (0, 1))
    translations = [((u, v), I2) for u, v in T]
    assert all(chi[a] == 1 for a in translations)
    for a in AGL:
        for tr in translations:
            assert acomp(acomp(a, tr), inverse_affine(a, adj)) in translations

    # The determinant-minus-one qutrit conjugation is the nontrivial coset.
    kappa = ((2, 0), (0, 1))
    anti = ((0, 0), kappa)
    assert chi[anti] == 2
    assert acomp(anti, anti) == ((0, 0), I2)

    # The projective Clifford/Hessian subgroup recorded upstream is exactly
    # the chi=+1 half; adjoining anti generates both character classes.
    assert parent["clifford_extension"]["projective_unitary_order"] == 216
    assert parent["clifford_extension"]["extended_projective_order"] == 432
    assert parent["clifford_extension"]["projective_unitary_group"] == "ASL(2,3)"
    assert parent["clifford_extension"]["extended_projective_group"] == "AGL(2,3)"
    assert parent["four_direction_action"]["unitary_image"] == "A4"
    assert parent["four_direction_action"]["extended_image"] == "S4"

    out = {
        "schema": "w33.hesse_affine_spinor_parity.v1",
        "status": "PASS_FULL_HESSE_AFFINE_EXTENSION_HAS_CANONICAL_SPINOR_PARITY_CHARACTER",
        "headline": (
            "The complete 432-element Hesse affine group carries a canonical C2 "
            "character chi(t,g)=det(g)=spinor_norm(rho(g)). Its kernel is exactly "
            "ASL(2,3), order 216, the projective unitary qutrit Clifford/Hessian "
            "group. The other 216 elements are the anti-linear/determinant-minus-one "
            "coset. Translations are spinor-parity neutral."
        ),
        "groups": {
            "translation_group": "F3^2",
            "translation_order": 9,
            "linear_group": "GL(2,3)",
            "linear_order": 48,
            "special_linear_order": 24,
            "AGL_order": 432,
            "ASL_order": 216,
        },
        "character": {
            "definition": "chi(t,g)=det(g)=spinor_norm(rho(g)) in F3^*/(F3^*)^2={1,2}",
            "homomorphism_pairs_checked": checked_pairs,
            "trivial_class_elements": class_counts[1],
            "nontrivial_class_elements": class_counts[2],
            "surjective_to_C2": True,
            "kernel_order": 216,
            "kernel": "ASL(2,3)=F3^2:SL(2,3)",
            "translation_subgroup_in_kernel": True,
            "orthogonal_image_fibre_size": 18,
            "orthogonal_image_order": 24,
        },
        "compiler_reading": {
            "unitary_projective_group": "ASL(2,3)",
            "unitary_order": 216,
            "extended_affine_group": "AGL(2,3)",
            "extended_order": 432,
            "unitary_direction_image": "A4",
            "extended_direction_image": "S4",
            "anti_linear_generator": "kappa=diag(-1,1)",
            "anti_linear_character": 2,
            "anti_linear_generator_order": 2,
        },
        "central_lift_boundary": (
            "The upstream Clifford certificate has a nonsplit central C3 lift of "
            "ASL(2,3) of order 648 and records an extended-with-center count 1296. "
            "This theorem does not identify a particular 1296 permutation stabilizer "
            "with that semilinear lift; the repo contains multiple 1296 carriers. "
            "An explicit central-extension intertwiner is still required."
        ),
        "physics_boundary": (
            "chi is a finite compiler/group character. Calling it spinor parity means "
            "only that it is pulled back from the finite orthogonal spinor norm. It is "
            "not physical spacetime parity, fermion parity, CPT, or a continuum Pin/Spin structure."
        ),
        "parents": [
            "data/w33_hesse_nullcone_adjoint_intertwiner.json",
            "data/w33_hesse_nullcone_spinor_norm.json",
            "data/w33_extended_clifford_hesse_null_cone.json",
        ],
        "checks": {
            "AGL_order432": True,
            "ASL_order216": True,
            "character_balanced_216_216": True,
            "character_homomorphism_all_186624_pairs": True,
            "kernel_exactly_ASL": True,
            "all_translations_character_trivial": True,
            "orthogonal_fibres_all_size18": True,
            "anti_linear_generator_nontrivial_character": True,
            "anti_linear_generator_involution": True,
            "projective_Clifford_is_character_kernel": True,
            "central_1296_not_overidentified": True,
            "physical_parity_not_claimed": True,
        },
    }
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    return out


def inverse_affine(a, adj):
    t, g = a
    gi = adj.inv2(g)
    gt = lin2(gi, t)
    return (((-gt[0]) % 3, (-gt[1]) % 3), gi)


if __name__ == "__main__":
    print(json.dumps(main(True), indent=2))
