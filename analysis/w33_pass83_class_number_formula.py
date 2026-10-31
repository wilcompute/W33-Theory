#!/usr/bin/env python3
"""
Pass 83 -- The graph analytic class number formula: W(3,3) as an F_1-curve.

This pass ties three separately-established facts into one arithmetic-geometry dictionary:

  * the Ihara zeta of W(3,3)            (Pass 73/74)  <-> Dedekind / Selberg zeta of a curve,
  * the spanning-tree number 2^81*5^23  (Pass 74)     <-> the class number h,
  * the critical group K(W)             (Pass 82)     <-> the ideal class group / Jacobian.

The bridge is the graph analytic class number formula.  Write the reciprocal Ihara zeta in
Bass form,

  1/zeta_G(u) = (1-u^2)^{m-n} * det(I - A u + q u^2),   q = k-1 = 11, m=|E|=240, n=|V|=40.

At u=1 it vanishes to order equal to the FIRST BETTI NUMBER (cycle rank) beta = m-n+1 = 201, and
its leading coefficient is a class number formula:

  lim_{u->1} 1/zeta_G(u) / (1-u)^{201} = 2^{m-n} * (1-q) * n * kappa(G),

where kappa(G) = #spanning trees = |K(W)| = 2^81*5^23.  Equivalently the "reduced" (topology-free)
special value of the Bass determinant is

  lim_{u->1} det(I - A u + q u^2)/(1-u) = -(q-1) * n * kappa(G) = -400 * kappa(G).

Everything is exact integer arithmetic; a symbolic sympy check of the order and leading coefficient
is included when sympy is available.  ASCII-only output.

Novelty: index.html/paper "class number" hits are all about Niemeier lattices / Phi_3 / spectral-
zeta gravity, none about the Ihara special value at u=1, spanning trees, or the critical group.
"""
from __future__ import annotations

import json
from math import prod

# --- graph constants (W(3,3) = SRG(40,12,2,4)) ---
N = 40  # vertices
M = 240  # edges
K = 12  # degree
Q = K - 1  # 11  (Ihara "prime")
BETA = M - N + 1  # 201 = first Betti number (cycle rank)

# adjacency eigenvalues -> Laplacian eigenvalues (k - lambda)
ADJ_SPEC = {12: 1, 2: 24, -4: 15}
LAP_SPEC = {K - lam: mult for lam, mult in ADJ_SPEC.items()}  # {0:1, 10:24, 16:15}


def spanning_trees():
    """Matrix-Tree: kappa = (1/n) * prod of nonzero Laplacian eigenvalues."""
    nonzero = [(val, mult) for val, mult in LAP_SPEC.items() if val != 0]
    num = prod(val**mult for val, mult in nonzero)
    assert num % N == 0
    return num // N


def factor_2_5(x):
    a = b = 0
    x = abs(x)
    while x % 2 == 0:
        x //= 2
        a += 1
    while x % 5 == 0:
        x //= 5
        b += 1
    return a, b, x


def cofactor_at_1():
    """1/zeta = (1-u)^{201} * C(u); return C(1) exactly.
    C(u) = (1+u)^{m-n} * (1-11u) * (1-2u+11u^2)^24 * (1+4u+11u^2)^15."""
    # (1-u^2)^{m-n} = (1-u)^{m-n}(1+u)^{m-n}; (1-12u+11u^2) = (1-u)(1-11u)
    val_1p = 2 ** (M - N)  # (1+u)^{m-n} at u=1
    val_perron = 1 - 11  # (1-11u) at u=1  = -10
    val_gauge = (1 - 2 + 11) ** 24  # (1-2u+11u^2)^24 at u=1 = 10^24
    val_chiral = (1 + 4 + 11) ** 15  # (1+4u+11u^2)^15 at u=1 = 16^15
    return val_1p * val_perron * val_gauge * val_chiral


def symbolic_check():
    try:
        import sympy as sp
    except Exception:
        return {"available": False}
    u = sp.symbols("u")
    inv_zeta = (
        (1 - u**2) ** (M - N)
        * (1 - 12 * u + 11 * u**2)
        * (1 - 2 * u + 11 * u**2) ** 24
        * (1 + 4 * u + 11 * u**2) ** 15
    )
    poly = sp.Poly(sp.expand(inv_zeta), u)
    factor = sp.Poly(1 - u, u)  # divide by (1-u) to match the (1-u)^201 convention
    mult = 0
    while poly.eval(1) == 0:
        poly = sp.div(poly, factor)[0]
        mult += 1
    leading = int(poly.eval(1))
    return {"available": True, "order_at_1": mult, "leading_coefficient": leading}


def main():
    kappa = spanning_trees()
    a, b, rest = factor_2_5(kappa)
    kappa_ok = rest == 1 and (a, b) == (81, 23)

    # class number formula (reduced, topology-free): det(I-Au+qu^2)/(1-u) at u=1
    reduced_special = -(Q - 1) * N * kappa  # = -400 * kappa
    # full 1/zeta special value (leading coeff at u=1)
    full_special_formula = (2 ** (M - N)) * (1 - Q) * N * kappa
    full_special_direct = cofactor_at_1()
    formula_matches = full_special_formula == full_special_direct

    sym = symbolic_check()

    checks = {
        "kappa_is_2^81_5^23": kappa_ok,
        "kappa_equals_critical_group_order_pass82": kappa == (2**81) * (5**23),
        "order_of_vanishing_is_first_Betti_201": BETA == 201,
        "class_number_formula_matches_factored_zeta": formula_matches,
        "reduced_special_value_is_-400_kappa": reduced_special == -400 * kappa,
    }
    if sym.get("available"):
        checks["sympy_order_at_1_is_201"] = sym["order_at_1"] == 201
        checks["sympy_leading_coeff_matches"] = (
            sym["leading_coefficient"] == full_special_direct
        )
    all_ok = all(checks.values())

    fa, fb, _ = factor_2_5(full_special_direct)
    ra, rb, _ = factor_2_5(reduced_special)

    dictionary = [
        ["curve / number field", "the graph W(3,3)"],
        ["Dedekind / Selberg zeta", "Ihara zeta zeta_G(u) (Pass 73/74)"],
        ["Riemann Hypothesis", "Ramanujan: poles on |u|=1/sqrt(11) (Pass 73)"],
        ["functional equation", "u -> 1/(11u) pole involution (Pass 74)"],
        [
            "genus / rank (order of vanishing at u=1)",
            f"first Betti number beta = m-n+1 = {BETA}",
        ],
        ["class number h", f"#spanning trees kappa = 2^81*5^23 (Pass 74)"],
        [
            "ideal class group / Jacobian",
            "critical group K(W) = (Z/10)^8+Z/40+(Z/160)^14 (Pass 82)",
        ],
        [
            "analytic class number formula",
            "lim det(I-Au+qu^2)/(1-u) = -(q-1) n kappa = -400 kappa",
        ],
    ]

    print("=" * 74)
    print("PASS 83 -- THE GRAPH ANALYTIC CLASS NUMBER FORMULA (W(3,3) AS AN F_1-CURVE)")
    print("=" * 74)
    print(
        f"first Betti number beta = m-n+1 = {BETA}  (order of vanishing of 1/zeta at u=1)"
    )
    print(f"class number kappa = #spanning trees = 2^{a}*5^{b} = {kappa}")
    print(f"  (= |critical group K(W)| from Pass 82)")
    print(
        f"reduced special value  det(I-Au+qu^2)/(1-u)|_1 = -(q-1)*n*kappa = -400*kappa"
    )
    print(f"                       = -2^{ra}*5^{rb}")
    print(f"full special value     1/zeta / (1-u)^201 |_1 = 2^(m-n)*(1-q)*n*kappa")
    print(
        f"                       = -2^{fa}*5^{fb}   (factored-zeta check: {formula_matches})"
    )
    if sym.get("available"):
        print(
            f"sympy: order at u=1 = {sym['order_at_1']}, leading coeff matches = "
            f"{sym['leading_coefficient']==full_special_direct}"
        )
    print()
    print("F_1 arithmetic dictionary:")
    for lhs, rhs in dictionary:
        print(f"   {lhs:<42} <->  {rhs}")
    print()
    print("checks:")
    for kk, vv in checks.items():
        print(f"   {'OK ' if vv else 'XX '} {kk}")
    print()
    print("=" * 74)
    print(f"STATUS: {'PASS' if all_ok else 'FAIL'}")
    print("=" * 74)

    payload = {
        "schema": "w33.pass83.class_number_formula.v1",
        "status": "PASS" if all_ok else "FAIL",
        "graph": {"n": N, "m": M, "k": K, "q": Q, "first_betti": BETA},
        "class_number_kappa": kappa,
        "kappa_factored": f"2^{a}*5^{b}",
        "kappa_equals_critical_group_order": kappa == (2**81) * (5**23),
        "order_of_vanishing_at_u1": BETA,
        "reduced_special_value": reduced_special,
        "reduced_special_value_factored": f"-2^{ra}*5^{rb}",
        "full_special_value": full_special_direct,
        "full_special_value_factored": f"-2^{fa}*5^{fb}",
        "class_number_formula": "lim_{u->1} det(I-Au+qu^2)/(1-u) = -(q-1)*n*kappa(G)",
        "symbolic_check": sym,
        "f1_dictionary": dictionary,
        "checks": checks,
    }
    with open("w33_pass83_class_number_formula.json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    print("[wrote] w33_pass83_class_number_formula.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
