#!/usr/bin/env python3
"""Exact bridge: retained-phase extended qutrit Clifford = Pass-408 Heisenberg automorphisms.

This file closes the 1296-element boundary left by
w33_hesse_affine_spinor_parity.py.

Three independently frozen structures are compared:

1. qutrit Pauli/Heisenberg normal form
       Z^a X^b omega^c,
   with multiplication
       (a,b,c)(A,B,C)=(a+A,b+B,c+C-bA);

2. the extended Hesse/Clifford linear action GL(2,3), with determinant -1
   supplying the anti-linear coset;

3. Pass 408's exhaustive graph-automorphism action on the 27-vertex
   Heisenberg bulk graph Gamma_3.

The non-obvious gauge change
       (a,b,c) -> ((a,b), z=c+2ab)
puts the qutrit Heisenberg law into the alternating-voltage coordinates used
by Pass 408. In those coordinates every M in GL(2,3) acts by
       (u,z) -> (Mu, det(M) z),
and left Heisenberg translation gives exactly the Pass-408 formula
       (u,z) -> (Mu+a, det(M)z - omega(Mu,a) + c).

Consequently the finite retained-phase extended qutrit Clifford lift is
literally H_27 : GL(2,3), order 1296, and its action equals the complete
Aut(Gamma_3) action certified in Pass 408.

Important boundary: this is an exact finite group/action theorem. It does not
identify this group with every unrelated order-1296 carrier in the repository,
nor does the spinor-parity C2 become physical spacetime parity/CPT.
"""
from __future__ import annotations

import importlib.util
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PASS408_SCRIPT = ROOT / "analysis/w33_pass408_full_automorphism_theorem.py"
EXTENDED_DATA = ROOT / "data/w33_extended_clifford_hesse_null_cone.json"
PARITY_DATA = ROOT / "data/w33_hesse_affine_spinor_parity.json"
CLIFFORD_DATA = ROOT / "data/PART_W33_20260829_CLIFFORD_C3_CIRCUIT_COVER.json"
PASS408_DATA = ROOT / "data/w33_pass408_full_automorphism_theorem.json"
OUT = ROOT / "data/w33_extended_clifford_pass408_intertwiner.json"
MOD = 3


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def mod(x: int) -> int:
    return int(x) % MOD


def hmul_raw(x, y):
    """Repository qutrit normal form Z^a X^b omega^c."""
    a, b, c = x
    A, B, C = y
    return (mod(a + A), mod(b + B), mod(c + C - b * A))


def raw_to_voltage(h):
    """Gauge into Pass-408 alternating-voltage coordinates."""
    a, b, c = h
    return ((a, b), mod(c + 2 * a * b))


def voltage_to_raw(vz):
    (a, b), z = vz
    return (a, b, mod(z - 2 * a * b))


def vadd(u, v):
    return (mod(u[0] + v[0]), mod(u[1] + v[1]))


def hmul_voltage(x, y, p408):
    u, z = x
    v, w = y
    return (vadd(u, v), mod(z + w + p408.omega(u, v, 3)))


def mmul(A, B):
    a, b, c, d = A
    e, f, g, h = B
    return (
        mod(a * e + b * g),
        mod(a * f + b * h),
        mod(c * e + d * g),
        mod(c * f + d * h),
    )


def minv(M):
    a, b, c, d = M
    det = mod(a * d - b * c)
    assert det in (1, 2)
    invdet = 1 if det == 1 else 2
    return (
        mod(invdet * d),
        mod(-invdet * b),
        mod(-invdet * c),
        mod(invdet * a),
    )


def alpha_raw(M, h, p408):
    """GL(2,3) similitude action pulled back to qutrit normal coordinates."""
    u, z = raw_to_voltage(h)
    Mu = p408.apply_matrix(M, u, 3)
    return voltage_to_raw((Mu, mod(p408.det(M, 3) * z)))


def hinv_raw(h):
    u, z = raw_to_voltage(h)
    return voltage_to_raw(((-u[0] % 3, -u[1] % 3), -z % 3))


I2 = (1, 0, 0, 1)
HID = (0, 0, 0)
E = (HID, I2)


def gmul(x, y, p408):
    h, M = x
    k, N = y
    return (hmul_raw(h, alpha_raw(M, k, p408)), mmul(M, N))


def ginv(x, p408):
    h, M = x
    Mi = minv(M)
    return (alpha_raw(Mi, hinv_raw(h), p408), Mi)


def comm(x, y, p408):
    return gmul(gmul(gmul(ginv(x, p408), ginv(y, p408), p408), x, p408), y, p408)


def subgroup_generated(generators, p408):
    gens = list(dict.fromkeys(generators))
    steps = gens + [ginv(g, p408) for g in gens]
    seen = {E}
    frontier = [E]
    while frontier:
        x = frontier.pop()
        for s in steps:
            y = gmul(x, s, p408)
            if y not in seen:
                seen.add(y)
                frontier.append(y)
    return seen


def derived_from_generators(ambient, ambient_gens, p408):
    seeds = {
        comm(s, x, p408)
        for s in ambient_gens
        for x in ambient
    }
    return subgroup_generated(seeds, p408)


def affine_mul(x, y, p408):
    u, M = x
    v, N = y
    return (vadd(u, p408.apply_matrix(M, v, 3)), mmul(M, N))


def project_to_affine(g):
    h, M = g
    return ((h[0], h[1]), M)


def act_from_group(g, vertex, p408):
    """Left H27 translation after the GL2 linear action."""
    h, M = g
    hv = raw_to_voltage(h)
    u = vertex[:2]
    z = vertex[2]
    Mu = p408.apply_matrix(M, u, 3)
    linear = (Mu, mod(p408.det(M, 3) * z))
    out = hmul_voltage(hv, linear, p408)
    return (out[0][0], out[0][1], out[1])


def main(write=True):
    p408 = load_module(PASS408_SCRIPT, "w33_pass408_bridge_parent")
    extended = json.loads(EXTENDED_DATA.read_text())
    parity = json.loads(PARITY_DATA.read_text())
    clifford = json.loads(CLIFFORD_DATA.read_text())
    pass408 = json.loads(PASS408_DATA.read_text())

    assert extended["clifford_extension"]["physical_clifford_lift_order"] == 648
    assert extended["clifford_extension"]["extended_projective_order"] == 432
    assert extended["clifford_extension"]["extended_with_C3_center_order"] == 1296
    assert parity["groups"]["AGL_order"] == 432
    assert parity["groups"]["ASL_order"] == 216
    assert clifford["centralExtension"]["orderK"] == 648
    assert clifford["centralExtension"]["orderQuotient"] == 216
    assert clifford["centralExtension"]["center"] == "C3"
    assert clifford["centralExtension"]["split"] is False
    assert pass408["instances"]["3"]["full_automorphism_order"] == 1296
    assert pass408["instances"]["3"]["central_orientation_fixed_subgroup_order"] == 648
    assert pass408["instances"]["3"]["exhaustive_no_extra_automorphisms"] is True

    H = list(itertools.product(range(3), repeat=3))
    GL2 = p408.gl2(3)
    SL2 = [M for M in GL2 if p408.det(M, 3) == 1]
    vertices = list(itertools.product(range(3), repeat=3))
    assert (len(H), len(GL2), len(SL2), len(vertices)) == (27, 48, 24, 27)

    # Exact qutrit-Heisenberg gauge weld.
    gauge_pairs_checked = 0
    for x in H:
        for y in H:
            assert raw_to_voltage(hmul_raw(x, y)) == hmul_voltage(
                raw_to_voltage(x), raw_to_voltage(y), p408
            )
            gauge_pairs_checked += 1
    assert gauge_pairs_checked == 27 * 27

    # All 48 linear similitudes act by Heisenberg automorphisms after the
    # determinant action on the centre.
    gl_automorphism_checks = 0
    for M in GL2:
        for x in H:
            for y in H:
                assert alpha_raw(M, hmul_raw(x, y), p408) == hmul_raw(
                    alpha_raw(M, x, p408), alpha_raw(M, y, p408)
                )
                gl_automorphism_checks += 1
    assert gl_automorphism_checks == 48 * 27 * 27

    # The latest anti-linear generator is exactly the determinant-minus-one
    # similitude in the retained-centre Heisenberg lift.
    kappa = (2, 0, 0, 1)
    assert p408.det(kappa, 3) == 2
    assert all(
        alpha_raw(kappa, (a, b, c), p408) == ((-a) % 3, b, (-c) % 3)
        for a, b, c in H
    )

    G = {(h, M) for h in H for M in GL2}
    K = {(h, M) for h in H for M in SL2}
    assert (len(G), len(K)) == (1296, 648)

    # Compare the action point-for-point with Pass 408.
    action_evaluations = 0
    our_perms = set()
    pass408_perms = set()
    for h, M in G:
        shift, central = raw_to_voltage(h)
        ours = []
        theirs = []
        for vertex in vertices:
            a = act_from_group((h, M), vertex, p408)
            b = p408.graph_automorphism_map(3, M, shift, central, vertex)
            assert a == b
            ours.append(a)
            theirs.append(b)
            action_evaluations += 1
        our_perms.add(tuple(ours))
        pass408_perms.add(tuple(theirs))
    assert action_evaluations == 1296 * 27
    assert our_perms == pass408_perms
    assert len(our_perms) == 1296

    # Quotient by the Pauli scalar centre is exactly AGL(2,3).
    affine_image = {project_to_affine(g) for g in G}
    kernel = {
        g for g in G
        if project_to_affine(g) == ((0, 0), I2)
    }
    assert len(affine_image) == 432
    assert kernel == {((0, 0, c), I2) for c in range(3)}
    projection_checks = 0
    # A generating-set-by-all-elements check is enough after the generators
    # below are independently shown to generate G.
    X = ((1, 0, 0), I2)
    Y = ((0, 1, 0), I2)
    F = (HID, (0, 2, 1, 0))
    S = (HID, (1, 1, 0, 1))
    A = (HID, kappa)
    full_gens = [X, Y, F, S, A]
    unitary_gens = [X, Y, F, S]
    assert subgroup_generated(full_gens, p408) == G
    assert subgroup_generated(unitary_gens, p408) == K
    for s in full_gens:
        for x in G:
            assert project_to_affine(gmul(s, x, p408)) == affine_mul(
                project_to_affine(s), project_to_affine(x), p408
            )
            projection_checks += 1
    assert projection_checks == len(full_gens) * len(G)

    # Exact group invariants. The odd coset destroys centrality of the old C3.
    full_center = {
        x for x in G
        if all(gmul(x, s, p408) == gmul(s, x, p408) for s in full_gens)
    }
    unitary_center = {
        x for x in K
        if all(gmul(x, s, p408) == gmul(s, x, p408) for s in unitary_gens)
    }
    assert full_center == {E}
    assert unitary_center == {((0, 0, c), I2) for c in range(3)}

    unitary_derived = derived_from_generators(K, unitary_gens, p408)
    full_derived = derived_from_generators(G, full_gens, p408)
    assert len(unitary_derived) == 216
    assert unitary_center <= unitary_derived
    assert full_derived == K

    z = ((0, 0, 1), I2)
    assert gmul(gmul(A, z, p408), ginv(A, p408), p408) == ((0, 0, 2), I2)

    # The new spinor-parity character is the abelianization character of the
    # retained-phase 1296 group.
    assert all(
        (1 if p408.det(M, 3) == 1 else 2)
        == (1 if (h, M) in full_derived else 2)
        for h, M in G
    )

    checks = {
        "qutrit_raw_to_voltage_gauge_all_729_pairs": True,
        "GL2_similitude_action_all_34992_products": True,
        "kappa_matches_certified_qutrit_conjugation": True,
        "retained_phase_extended_group_order_1296": True,
        "unitary_index_two_subgroup_order_648": True,
        "action_equals_pass408_all_34992_vertex_evaluations": True,
        "pass408_permutation_set_exactly_equal": True,
        "pass408_no_extra_automorphisms_imported": True,
        "quotient_by_scalar_C3_is_AGL23_order432": True,
        "unitary_quotient_is_ASL23_order216": True,
        "full_center_trivial": True,
        "unitary_center_exact_C3": True,
        "unitary_derived_order216": True,
        "unitary_center_contained_in_derived": True,
        "full_derived_equals_unitary_648": True,
        "full_abelianization_is_C2": True,
        "odd_kappa_inverts_scalar_center": True,
        "spinor_parity_is_full_abelianization_character": True,
    }

    out = {
        "schema": "w33.extended_clifford_pass408_intertwiner.v1",
        "status": "PASS_EXTENDED_QUTRIT_CLIFFORD_LIFT_EQUALS_PASS408_HEISENBERG_AUTOMORPHISM_GROUP",
        "headline": (
            "The previously open 1296-element retained-phase extension is now "
            "identified by an explicit coordinate/action intertwiner. The gauge "
            "(a,b,c)->((a,b),c+2ab) sends the qutrit Pauli H27 law to the Pass-408 "
            "Heisenberg voltage law. Under it GL(2,3) acts by (u,z)->(Mu,det(M)z), "
            "and left H27 translation reproduces Pass 408's complete graph action "
            "point-for-point. Hence the finite retained-phase extended qutrit "
            "Clifford lift is H27:GL(2,3) ~= Aut(Gamma_3), order 1296."
        ),
        "coordinate_intertwiner": {
            "qutrit_coordinates": "(a,b,c) representing Z^a X^b omega^c",
            "qutrit_product": "(a,b,c)(A,B,C)=(a+A,b+B,c+C-bA)",
            "pass408_coordinates": "((a,b),z)",
            "gauge": "z=c+2ab mod 3",
            "inverse_gauge": "c=z-2ab mod 3",
            "voltage_product": "(u,z)(v,w)=(u+v,z+w+omega(u,v))",
            "pass408_omega": "omega(u,v)=u_1 v_0-u_0 v_1",
            "pair_checks": gauge_pairs_checked,
        },
        "group_structure": {
            "full_group": "H27 : GL(2,3)",
            "full_order": 1296,
            "unitary_subgroup": "H27 : SL(2,3)",
            "unitary_order": 648,
            "projective_full_quotient": "AGL(2,3)",
            "projective_full_order": 432,
            "projective_unitary_quotient": "ASL(2,3)",
            "projective_unitary_order": 216,
            "scalar_C3_kernel_order": 3,
            "full_center_order": len(full_center),
            "unitary_center_order": len(unitary_center),
            "full_derived_order": len(full_derived),
            "unitary_derived_order": len(unitary_derived),
            "full_abelianization": "C2",
            "scalar_C3_is_normal_but_not_central_in_full_group": True,
            "odd_coset_inverts_scalar_C3": True,
        },
        "pass408_weld": {
            "theorem": pass408["theorem"],
            "explicit_action": pass408["explicit_prime_field_action"],
            "q3_exhaustive_full_order": pass408["instances"]["3"]["full_automorphism_order"],
            "q3_no_extras": pass408["instances"]["3"]["exhaustive_no_extra_automorphisms"],
            "our_action_permutations": len(our_perms),
            "pointwise_action_evaluations": action_evaluations,
            "permutation_sets_equal": True,
            "conclusion": "retained-phase extended qutrit Clifford lift ~= Aut(Gamma_3) by explicit action equality",
        },
        "parity_weld": {
            "projective_character": "det(M)=spinor_norm(rho(M))",
            "retained_phase_character": "G -> G/G' ~= C2",
            "kernel": "H27 : SL(2,3), order 648",
            "anti_linear_generator": "kappa=diag(-1,1)",
            "kappa_inverts_Pauli_center": True,
        },
        "old_648_certificate_match": {
            "order": clifford["centralExtension"]["orderK"],
            "center": clifford["centralExtension"]["center"],
            "quotient_order": clifford["centralExtension"]["orderQuotient"],
            "derived_order": clifford["centralExtension"]["derivedSubgroupOrder"],
            "center_contained_in_derived": clifford["centralExtension"]["centerContainedInDerived"],
            "nonsplit": not clifford["centralExtension"]["split"],
            "all_invariants_reproduced": True,
        },
        "literature_context": {
            "extended_Clifford_definition": (
                "Appleby defines the extended Clifford group as unitary and anti-unitary "
                "normalizers of the Weyl-Heisenberg group; the projective action is the "
                "extended symplectic/affine action."
            ),
            "note": (
                "The repo theorem is stronger for this internal comparison because it "
                "matches the older Pass-408 27-point graph permutations exactly."
            ),
        },
        "boundary": (
            "This identifies the specific Pass-408 Heisenberg bulk automorphism carrier "
            "with the finite retained-Pauli-phase extended qutrit Clifford lift. It does "
            "not identify every unrelated order-1296 subgroup elsewhere in W33/E6, and "
            "the C2/spinor-parity character is not continuum spacetime parity, fermion "
            "parity, CPT, or a Lorentzian Pin/Spin structure."
        ),
        "parents": [
            "data/PART_W33_20260829_CLIFFORD_C3_CIRCUIT_COVER.json",
            "data/w33_extended_clifford_hesse_null_cone.json",
            "data/w33_hesse_affine_spinor_parity.json",
            "data/w33_pass408_full_automorphism_theorem.json",
        ],
        "checks": checks,
    }
    assert all(checks.values())
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    return out


if __name__ == "__main__":
    print(json.dumps(main(True), indent=2))
