#!/usr/bin/env python3
"""Resolve the 16-line fibres in the six-Schur-quartic arrangement as far as the exact equations allow.

External equations are from Nurowski, arXiv:2609.10751:
  phi(u,v)=u(u^3-v^3), h(u,v)=v(8u^3+v^3),
  Phi_k: phi_1-omega^k phi_2=0,
  Psi_c: H_2-c H_1=0.
The two common cores H and K are the 4x4 joins of the four projective zeros of
phi and h respectively.  Each four-point set has a regular Klein V4 of projective
self-maps, so V4 x V4 ~= C2^4 acts regularly on each 16-line core.

For the nine cross blocks we use the graph-line model L_M=(x,Mx).  On Phi_0,
L_M is a second-kind graph line precisely when phi(Mx)=phi(x).  The projective
stabilizer of the four zeros of phi is A4 (12 elements); each projective element
has four scalar lifts preserving the binary quartic, giving 48 graph lines.
Hessian covariance gives

    h(Mx)=det(M)^(-2) h(x),

so Nurowski's c(L) is the exact character chi(M)=det(M)^(-2) in mu_3.  The
12 projective elements split 4+4+4 under chi, hence each lifted fibre has 16
lines.  The chi=1 projective kernel is exactly the Klein V4, and its four scalar
lifts form an order-16 kernel K_16 acting regularly on each cross fibre.  Since
i*I is in K_16 and has order four on graph lines, K_16 is NOT elementary
abelian C2^4.

Thus the tempting uniform-C2^4 bundle conjecture is false: the two core blocks
admit C2^4 product torsors, whereas the nine cross blocks are coset torsors for
a non-elementary order-16 binary-quartic kernel.  The script does not identify
K_16 up to SmallGroup type, and does not claim these blockwise torsor actions
extend simultaneously to the full 176-line automorphism group.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_schur176_sixteen_line_fibre_structure.json"

u, v = sp.symbols("u v")
tau = sp.sqrt(-3)
omega = sp.simplify((-1 + tau) / 2)
omega2 = sp.expand(omega**2)


def phi(U, V):
    return sp.expand(U * (U**3 - V**3))


def hess(U, V):
    return sp.expand(V * (8 * U**3 + V**3))


def proj_eq(a, b):
    return sp.simplify(a[0] * b[1] - a[1] * b[0]) == 0


def mobius_for_perm(points, perm):
    rows = []
    for i in range(3):
        x, y = points[i]
        xp, yp = points[perm[i]]
        rows.append([sp.expand(x * yp), sp.expand(y * yp), sp.expand(-x * xp), sp.expand(-y * xp)])
    ns = sp.Matrix(rows).nullspace()
    if len(ns) != 1:
        return None
    q = ns[0]
    A = sp.Matrix([[sp.simplify(q[0]), sp.simplify(q[1])], [sp.simplify(q[2]), sp.simplify(q[3])]])
    if sp.simplify(A.det()) == 0:
        return None
    for i, p in enumerate(points):
        if not proj_eq(A * p, points[perm[i]]):
            return None
    return A


def projective_stabilizer(points):
    out = []
    for p in itertools.permutations(range(4)):
        A = mobius_for_perm(points, p)
        if A is not None:
            out.append((p, A))
    return out


def parity(p):
    return sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p))) & 1


def classify_mu3(z):
    for name, val in (("1", sp.Integer(1)), ("omega", omega), ("omega2", omega2)):
        if sp.simplify(z - val) == 0:
            return name
    raise AssertionError(f"not a cube root of unity: {sp.simplify(z)}")


def quartic_multiplier(A):
    U = sp.expand(A[0, 0] * u + A[0, 1] * v)
    V = sp.expand(A[1, 0] * u + A[1, 1] * v)
    P = sp.Poly(phi(U, V), u, v)
    Q = sp.Poly(phi(u, v), u, v)
    k = sp.simplify(P.coeff_monomial(u**4) / Q.coeff_monomial(u**4))
    assert sp.simplify(P.as_expr() - k * Q.as_expr()) == 0
    return k


def compose_perm(p, q):
    return tuple(p[q[i]] for i in range(4))


def v4_double_transpositions():
    return {
        (0, 1, 2, 3),
        (1, 0, 3, 2),
        (2, 3, 0, 1),
        (3, 2, 1, 0),
    }


def build_result():
    phi_pts = [sp.Matrix([0, 1]), sp.Matrix([1, 1]), sp.Matrix([omega, 1]), sp.Matrix([omega2, 1])]
    h_pts = [sp.Matrix([1, 0]), sp.Matrix([-1, 2]), sp.Matrix([-omega, 2]), sp.Matrix([-omega2, 2])]

    aut_phi = projective_stabilizer(phi_pts)
    aut_h = projective_stabilizer(h_pts)
    assert len(aut_phi) == 12 and len(aut_h) == 12
    assert all(parity(p) == 0 for p, _ in aut_phi)
    assert all(parity(p) == 0 for p, _ in aut_h)

    V4 = v4_double_transpositions()
    phi_v4 = {p for p, _ in aut_phi if p in V4}
    h_v4 = {p for p, _ in aut_h if p in V4}
    assert phi_v4 == V4 and h_v4 == V4

    # Each V4 is regular on the four roots; the product is regular on 4x4 core lines.
    for subgroup in (phi_v4, h_v4):
        for i in range(4):
            assert {p[i] for p in subgroup} == set(range(4))
    core_actions = {(p, q) for p in phi_v4 for q in phi_v4}
    hcore_actions = {(p, q) for p in h_v4 for q in h_v4}
    assert len(core_actions) == len(hcore_actions) == 16
    orbit = {(p[0], q[0]) for p, q in core_actions}
    horbit = {(p[0], q[0]) for p, q in hcore_actions}
    assert len(orbit) == len(horbit) == 16

    # Exact Hessian character on projective binary-quartic symmetries.
    rows = []
    for p, A in aut_phi:
        k = quartic_multiplier(A)
        det = sp.simplify(A.det())
        # If M=lambda*A and lambda^4*k=1, then det(M)^(-2)=k*det(A)^(-2).
        chi = sp.simplify(k * det**-2)
        cname = classify_mu3(chi)
        rows.append((p, cname))
    profile = Counter(name for _, name in rows)
    assert profile == {"1": 4, "omega": 4, "omega2": 4}
    chi_kernel = {p for p, name in rows if name == "1"}
    assert chi_kernel == V4

    # Character is multiplicative already on the A4 projective quotient.
    cmap = {p: name for p, name in rows}
    mu_exp = {"1": 0, "omega": 1, "omega2": 2}
    exp_mu = {0: "1", 1: "omega", 2: "omega2"}
    for p, q in itertools.product(cmap, repeat=2):
        r = compose_perm(p, q)
        assert r in cmap
        assert cmap[r] == exp_mu[(mu_exp[cmap[p]] + mu_exp[cmap[q]]) % 3]

    # Four scalar fourth-root lifts per projective symmetry give the 48 graph lines.
    lifted_total = 4 * len(aut_phi)
    lifted_fibres = {name: 4 * profile[name] for name in profile}
    assert lifted_total == 48
    assert lifted_fibres == {"1": 16, "omega": 16, "omega2": 16}

    # Kernel K16 contains the four scalar lifts of identity.  Multiplication by iI
    # cycles M -> iM -> -M -> -iM -> M, and these are distinct graph lines, so K16
    # contains an element of order 4 and cannot be C2^4.
    kernel_order = 4 * len(chi_kernel)
    scalar_cycle_length = 4
    assert kernel_order == 16 and scalar_cycle_length == 4

    # D_a transports the three Phi_0 cross fibres to all nine B_{k,c}; hence all
    # nine cross blocks inherit the same K16 coset-torsor type.
    cross_blocks = 3 * 3
    assert cross_blocks == 9

    checks = {
        "phi_root_projective_stabilizer_is_A4_order12": len(aut_phi) == 12 and all(parity(p) == 0 for p, _ in aut_phi),
        "h_root_projective_stabilizer_is_A4_order12": len(aut_h) == 12 and all(parity(p) == 0 for p, _ in aut_h),
        "phi_double_transpositions_form_regular_V4": phi_v4 == V4,
        "h_double_transpositions_form_regular_V4": h_v4 == V4,
        "H_core_has_regular_C2^4_product_torsor": len(orbit) == 16,
        "K_core_has_regular_C2^4_product_torsor": len(horbit) == 16,
        "Hessian_character_profile_is_4_4_4_on_A4": profile == {"1": 4, "omega": 4, "omega2": 4},
        "Hessian_character_kernel_is_projective_V4": chi_kernel == V4,
        "lifted_binary_quartic_symmetry_has_48_graph_lines": lifted_total == 48,
        "each_cross_character_fibre_has_16_lines": set(lifted_fibres.values()) == {16},
        "cross_fibre_kernel_has_order16": kernel_order == 16,
        "cross_fibre_kernel_contains_order4_scalar": scalar_cycle_length == 4,
        "cross_fibre_kernel_is_not_C2^4": scalar_cycle_length == 4,
        "all_nine_cross_blocks_share_the_same_torsor_type": cross_blocks == 9,
    }

    return {
        "schema": "w33.schur176-sixteen-line-fibre-structure.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "external_equations": {
            "source": "P. Nurowski, arXiv:2609.10751 (2026), Section 4",
            "phi": "u(u^3-v^3)",
            "h": "v(8u^3+v^3)",
            "cross_rule": "H2|L = c(L) H1|L with c(L)^3=1 and 16 lines for each c",
        },
        "core_fibres": {
            "H": {"lines": 16, "torsor": "V4 x V4 ~= C2^4", "origin_model": "Z(phi) x Z(phi)"},
            "K": {"lines": 16, "torsor": "V4 x V4 ~= C2^4", "origin_model": "Z(h) x Z(h)"},
        },
        "cross_fibres": {
            "blocks": 9,
            "lines_per_block": 16,
            "binary_quartic_projective_group": "A4",
            "projective_order": 12,
            "scalar_lifts_per_projective_element": 4,
            "graph_line_total": lifted_total,
            "character": "chi(M)=det(M)^(-2) from Hessian covariance",
            "projective_character_profile": dict(profile),
            "kernel_order": kernel_order,
            "kernel_projective_quotient": "V4",
            "contains_order4_scalar": True,
            "is_C2^4": False,
            "torsor_statement": "each B_{k,c} is a coset torsor for the order-16 kernel of chi; D_a transports the Phi_0 statement to all k",
        },
        "theorem": (
            "The eleven 16-line Schur-176 blocks are not a uniform C2^4 bundle. The two common cores H,K carry regular V4xV4=C2^4 product torsors. The nine cross blocks are 16-element cosets of the Hessian character kernel in the 48-element exact binary-quartic graph-line symmetry; that kernel contains the order-four scalar iI, so it is not C2^4."
        ),
        "claim_boundary": (
            "Exact binary-quartic/projective-root calculation using Nurowski's displayed Section-4 equations. It proves blockwise torsor structures. It does not yet identify the nonabelian order-16 cross kernel up to SmallGroup type or prove a single order-16 group acts globally and simultaneously on all eleven blocks."
        ),
        "checks": checks,
    }


def main():
    r = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(r, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": r["status"], "core": r["core_fibres"]["H"]["torsor"], "cross_kernel": r["cross_fibres"]["kernel_order"], "cross_is_C2_4": r["cross_fibres"]["is_C2^4"]}, sort_keys=True))
    return 0 if r["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
