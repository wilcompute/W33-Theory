#!/usr/bin/env python3
"""Explicit GL(2,3) adjoint lift of the Hesse/hull null-cone S4 action.

Parent certificate:
    data/w33_extended_clifford_hesse_null_cone.json

The parent proves equality of the permutation images on:
  * four affine/Hesse directions in F3^2, and
  * four isotropic rays of a 3D quadratic quotient.

This verifier upgrades that projective equality to a linear intertwiner.

Let sl2(F3) have coordinates (a,b,c) for
    X(a,b,c) = [[a,b],[c,-a]].
Then
    q_sl2(a,b,c) = -det X = a^2 + bc
has polar Gram
    B = [[2,0,0],[0,0,1],[0,1,0]].

The explicit matrix
    P = [[1,1,0],[1,0,2],[2,0,0]]
satisfies
    P^T Q_hull P = 2 B.

For g in GL(2,3), define
    rho(g) = P Ad(g^{-T}) P^{-1}.
The inverse-transpose is forced by the parent's normal-vector convention for
affine directions. The verifier proves:
  * rho(g)^T Q_hull rho(g)=Q_hull and det rho(g)=1;
  * im rho = SO(Q_hull), order 24;
  * ker rho = {+I,-I};
  * im(SL(2,3)) has order 12 and induces A4;
  * im(GL(2,3)) induces the parent's full S4 action;
  * the nilpotent-cone Veronese map
        nu(u,v)=(-uv,u^2,-v^2)
    is sent by P to the parent's four direction/null-ray dictionary exactly;
  * the determinant-minus-one qutrit reflection diag(-1,1) maps to the
    parent's odd transposition on null rays.

Important boundary:
rho lands in SO(3,3) even when det(g)=-1. Therefore "odd" in the four-ray S4
action is NOT the same notion as determinant -1 in the 3D orthogonal module.
This is finite quadratic geometry over F3, not a continuum Lorentz/spin
structure or a physical CPT theorem.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "data/w33_extended_clifford_hesse_null_cone.json"
OUT = ROOT / "data/w33_hesse_nullcone_adjoint_intertwiner.json"
MOD = 3


def mod(x: int) -> int:
    return int(x) % MOD


def matmul(A, B):
    return tuple(
        tuple(mod(sum(A[i][k] * B[k][j] for k in range(len(B))))
              for j in range(len(B[0])))
        for i in range(len(A))
    )


def transpose(A):
    return tuple(tuple(A[j][i] for j in range(len(A))) for i in range(len(A[0])))


def matvec(A, v):
    return tuple(mod(sum(A[i][j] * v[j] for j in range(len(v)))) for i in range(len(A)))


def det2(M):
    return mod(M[0][0] * M[1][1] - M[0][1] * M[1][0])


def inv2(M):
    d = det2(M)
    assert d
    di = 1 if d == 1 else 2
    return (
        (mod(di * M[1][1]), mod(-di * M[0][1])),
        (mod(-di * M[1][0]), mod(di * M[0][0])),
    )


def det3(M):
    return mod(
        M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
        - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
        + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0])
    )


def inv3(M):
    # Gauss-Jordan over F3.
    A = [list(row) + [1 if i == j else 0 for j in range(3)]
         for i, row in enumerate(M)]
    for col in range(3):
        pivot = next(r for r in range(col, 3) if A[r][col] % MOD)
        A[col], A[pivot] = A[pivot], A[col]
        scale = 1 if A[col][col] % MOD == 1 else 2
        A[col] = [mod(scale * x) for x in A[col]]
        for r in range(3):
            if r != col and A[r][col] % MOD:
                f = A[r][col] % MOD
                A[r] = [mod(A[r][j] - f * A[col][j]) for j in range(6)]
    return tuple(tuple(A[i][j] for j in range(3, 6)) for i in range(3))


def projective(v):
    v = tuple(mod(x) for x in v)
    lead = next(x for x in v if x)
    scale = 1 if lead == 1 else 2
    return tuple(mod(scale * x) for x in v)


def sl2_matrix(v):
    a, b, c = v
    return ((mod(a), mod(b)), (mod(c), mod(-a)))


def sl2_coords(X):
    return (mod(X[0][0]), mod(X[0][1]), mod(X[1][0]))


def ad_matrix(g):
    """Columns of conjugation X -> g X g^{-1} on sl2 coordinates."""
    gi = inv2(g)
    basis = (
        ((1, 0), (0, 2)),
        ((0, 1), (0, 0)),
        ((0, 0), (1, 0)),
    )
    cols = []
    for E in basis:
        cols.append(sl2_coords(matmul(matmul(g, E), gi)))
    return tuple(tuple(cols[j][i] for j in range(3)) for i in range(3))


def rho(g, P, Pinv):
    # Parent directions are covectors, hence the inverse-transpose action.
    git = transpose(inv2(g))
    return matmul(matmul(P, ad_matrix(git)), Pinv)


def direction_perm(g, directions):
    dindex = {projective(v): i for i, v in enumerate(directions)}
    gi = inv2(g)
    out = []
    for n in directions:
        # row covector n -> n g^{-1}
        w = (
            mod(n[0] * gi[0][0] + n[1] * gi[1][0]),
            mod(n[0] * gi[0][1] + n[1] * gi[1][1]),
        )
        out.append(dindex[projective(w)])
    return tuple(out)


def ray_perm(M, rays):
    rindex = {projective(v): i for i, v in enumerate(rays)}
    return tuple(rindex[projective(matvec(M, v))] for v in rays)


def perm_parity(p):
    return sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p))) % 2


def nu(u, v):
    """Nilpotent/rank-one Veronese point in sl2 coordinates."""
    return (mod(-u * v), mod(u * u), mod(-v * v))


def main(write=True):
    parent = json.loads(PARENT.read_text())
    Q = tuple(tuple(int(x) for x in row)
              for row in parent["affine_hull_null_cone"]["gram"])
    directions = tuple(tuple(int(x) for x in v)
                       for v in parent["four_direction_action"]["directions"])
    rays = tuple(tuple(int(x) for x in v)
                 for v in parent["affine_hull_null_cone"]["isotropic_projective_rays"])
    parent_perm = tuple(parent["four_direction_action"]["conjugation_permutation"])

    assert Q == ((0, 1, 1), (1, 0, 1), (1, 1, 0))
    assert directions == ((1, 0), (0, 1), (1, 1), (1, 2))
    assert set(map(projective, rays)) == {
        (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)
    }

    B = ((2, 0, 0), (0, 0, 1), (0, 1, 0))
    P = ((1, 1, 0), (1, 0, 2), (2, 0, 0))
    Pinv = inv3(P)

    # Exact equivalence of the hull form and the sl2 determinant polar form,
    # up to the irrelevant nonzero scalar 2.
    form_pullback = matmul(matmul(transpose(P), Q), P)
    twoB = tuple(tuple(mod(2 * x) for x in row) for row in B)
    assert form_pullback == twoB

    # q=-det on sl2, checked exhaustively.
    for v in itertools.product(range(3), repeat=3):
        X = sl2_matrix(v)
        qdet = mod(-det2(X))
        qpoly = mod(v[0] * v[0] + v[1] * v[2])
        assert qdet == qpoly

    # The four P1(F3) directions map exactly, not merely up to a permutation.
    veronese_dictionary = {}
    for d, expected in zip(directions, rays):
        image = projective(matvec(P, nu(*d)))
        assert image == projective(expected)
        veronese_dictionary[str(tuple(d))] = list(image)

    # Build GL2(3), its SL2(3) subgroup, and the adjoint lift.
    GL2 = []
    for e in itertools.product(range(3), repeat=4):
        g = ((e[0], e[1]), (e[2], e[3]))
        if det2(g):
            GL2.append(g)
    SL2 = [g for g in GL2 if det2(g) == 1]
    assert len(GL2) == 48 and len(SL2) == 24

    image = {}
    kernel = []
    direction_actions = set()
    ray_actions = set()
    identity3 = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    for g in GL2:
        R = rho(g, P, Pinv)
        assert matmul(matmul(transpose(R), Q), R) == Q
        assert det3(R) == 1
        pd = direction_perm(g, directions)
        pr = ray_perm(R, rays)
        assert pd == pr
        direction_actions.add(pd)
        ray_actions.add(pr)
        image[tuple(x for row in R for x in row)] = R
        if R == identity3:
            kernel.append(g)

    assert len(image) == 24
    assert len(kernel) == 2
    assert set(kernel) == {((1, 0), (0, 1)), ((2, 0), (0, 2))}
    assert direction_actions == ray_actions
    assert len(direction_actions) == 24

    image_SL = {
        tuple(x for row in rho(g, P, Pinv) for x in row)
        for g in SL2
    }
    sl_perms = {direction_perm(g, directions) for g in SL2}
    assert len(image_SL) == 12
    assert len(sl_perms) == 12
    assert all(perm_parity(p) == 0 for p in sl_perms)

    # Exhaust SO(Q) independently and prove surjectivity, not just image size.
    O = []
    SO = []
    for e in itertools.product(range(3), repeat=9):
        M = (e[0:3], e[3:6], e[6:9])
        d = det3(M)
        if d and matmul(matmul(transpose(M), Q), M) == Q:
            O.append(M)
            if d == 1:
                SO.append(M)
    assert len(O) == 48 and len(SO) == 24
    assert set(image) == {tuple(x for row in M for x in row) for M in SO}

    phase_reflection = ((2, 0), (0, 1))
    Rk = rho(phase_reflection, P, Pinv)
    kperm = ray_perm(Rk, rays)
    assert det2(phase_reflection) == 2
    assert det3(Rk) == 1
    assert kperm == parent_perm == (0, 1, 3, 2)
    assert perm_parity(kperm) == 1

    out = {
        "schema": "w33.hesse_nullcone_adjoint_intertwiner.v1",
        "status": "PASS_EXPLICIT_GL23_ADJOINT_LIFT_IDENTIFIES_HESSE_DIRECTIONS_WITH_HULL_NULL_CONE",
        "headline": (
            "The parent certificate's equality of two S4 permutation actions lifts to "
            "an explicit 3-dimensional linear intertwiner.  The traceless-matrix "
            "adjoint representation of GL(2,3), transported by P, surjects onto "
            "SO(Q_hull) with kernel {+I,-I}.  The nilpotent cone maps point-for-point "
            "to the four certified Hesse/hull null rays."
        ),
        "sl2_model": {
            "coordinates": "X(a,b,c)=[[a,b],[c,-a]]",
            "quadratic_form": "q=-det(X)=a^2+b*c",
            "polar_gram": [list(row) for row in B],
            "hull_gram": [list(row) for row in Q],
            "basis_change_P": [list(row) for row in P],
            "basis_change_P_inverse": [list(row) for row in Pinv],
            "identity": "P^T Q_hull P = 2 B_sl2",
        },
        "null_cone": {
            "veronese_map": "nu(u,v)=(-u*v,u^2,-v^2)",
            "direction_to_ray_exact": veronese_dictionary,
            "dictionary_matches_parent_without_relabeling": True,
        },
        "adjoint_lift": {
            "formula": "rho(g)=P*Ad(g^{-T})*P^{-1}",
            "GL2_order": 48,
            "SL2_order": 24,
            "rho_image_order": 24,
            "rho_kernel_order": 2,
            "rho_kernel": ["+I2", "-I2"],
            "rho_image": "SO(Q_hull)",
            "SO_Q_order": 24,
            "O_Q_order": 48,
            "SL2_image_order": 12,
            "SL2_projective_image": "PSL(2,3) ~= A4",
            "GL2_projective_image": "PGL(2,3) ~= S4",
            "all_48_direction_actions_match_rho_null_ray_actions": True,
        },
        "antilinear_reflection": {
            "phase_space_matrix": [[2, 0], [0, 1]],
            "phase_space_determinant_mod3": 2,
            "rho_matrix": [list(row) for row in Rk],
            "rho_determinant_mod3": 1,
            "null_ray_permutation": list(kperm),
            "permutation_parity": "odd",
            "clarification": (
                "The determinant-minus-one phase-space reflection maps into SO(Q_hull). "
                "Its oddness is parity on the four-ray S4 set, not determinant -1 in "
                "the 3D orthogonal representation."
            ),
        },
        "parallel_e8_real_form_boundary": (
            "A parallel certificate identifies an anti-linear real structure of the exact "
            "248D compiler with fixed real form E8(8). That characteristic-zero real-form "
            "theorem is logically separate from this F3 null-cone theorem; no homomorphism, "
            "spacetime interpretation, or physical identification between the two is asserted here."
        ),
        "theorem_boundary": (
            "This is a finite F3 adjoint/quadratic-form theorem. It supplies an exact "
            "linear lift of the Hesse/null-cone S4 dictionary. It does not identify "
            "the finite quadratic space with Lorentzian spacetime, nor derive Spin(3,1), "
            "CPT, CP violation, a continuum metric, or a physical spin structure."
        ),
        "parent": "data/w33_extended_clifford_hesse_null_cone.json",
        "checks": {
            "hull_form_equivalent_to_sl2_determinant_form": True,
            "sl2_quadratic_form_equals_minus_determinant_exhaustively": True,
            "veronese_dictionary_exact": True,
            "GL2_order_48": True,
            "SL2_order_24": True,
            "rho_preserves_Q_for_all_GL2": True,
            "rho_determinant_one_for_all_GL2": True,
            "rho_kernel_exactly_plus_minus_identity": True,
            "rho_surjects_SOQ": True,
            "SL2_image_A4_order12": True,
            "GL2_image_S4_order24": True,
            "all_direction_and_ray_permutations_match": True,
            "phase_reflection_matches_parent_odd_transposition": True,
            "phase_reflection_still_has_3d_orthogonal_determinant_one": True,
            "continuum_physics_not_overclaimed": True,
        },
    }
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    return out


if __name__ == "__main__":
    print(json.dumps(main(True), indent=2))
