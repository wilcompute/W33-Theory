#!/usr/bin/env python3
"""BT1695 - dark-anyon braiding gate boundary.

The dark clock/braiding scripts identify D(2T) as the finite topological clock.
This verifier keeps the exact part and removes the overclaim:

* 2T = SL(2,3) has 24 elements.
* The quantum double D(2T) has 42 anyon labels.
* The flux orders give T-matrix period 12 = k.
* The derived series proves 2T is solvable.

Therefore this packet promotes D(2T) as the protected finite/Clifford-like
clock and routing backbone, while requiring the already-separate Hesse/T or
Wigner-negative magic port for universality.
"""

from __future__ import annotations

import itertools
import json
from math import gcd
from pathlib import Path

F = 3
K = 12
OUT = Path("data/bt1695_dark_anyon_braiding_gate_boundary.json")

Matrix = tuple[tuple[int, int], tuple[int, int]]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    return tuple(
        tuple(sum(a[i][t] * b[t][j] for t in range(2)) % F for j in range(2))
        for i in range(2)
    )  # type: ignore[return-value]


def det(a: Matrix) -> int:
    return (a[0][0] * a[1][1] - a[0][1] * a[1][0]) % F


def inv(a: Matrix) -> Matrix:
    (x, y), (z, w) = a
    # determinant is 1 in SL(2,3)
    return ((w % F, (-y) % F), ((-z) % F, x % F))


def identity() -> Matrix:
    return ((1, 0), (0, 1))


def sl23() -> list[Matrix]:
    return [
        ((a, b), (c, d))
        for a, b, c, d in itertools.product(range(F), repeat=4)
        if det(((a, b), (c, d))) == 1
    ]


def order(element: Matrix) -> int:
    one = identity()
    cur = element
    n = 1
    while cur != one:
        cur = matmul(cur, element)
        n += 1
    return n


def lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)


def conjugacy_classes(elements: set[Matrix]) -> list[set[Matrix]]:
    seen: set[Matrix] = set()
    classes: list[set[Matrix]] = []
    for g in elements:
        if g in seen:
            continue
        cls = {matmul(matmul(x, g), inv(x)) for x in elements}
        seen |= cls
        classes.append(cls)
    return classes


def centralizer(group: set[Matrix], g: Matrix) -> set[Matrix]:
    return {x for x in group if matmul(x, g) == matmul(g, x)}


def subgroup_generated(gens: set[Matrix]) -> set[Matrix]:
    one = identity()
    closure = {one, *gens}
    changed = True
    while changed:
        changed = False
        current = list(closure)
        for a in current:
            for b in current:
                for c in (matmul(a, b), inv(a)):
                    if c not in closure:
                        closure.add(c)
                        changed = True
    return closure


def commutator(a: Matrix, b: Matrix) -> Matrix:
    return matmul(matmul(matmul(a, b), inv(a)), inv(b))


def derived_series_orders(group: set[Matrix]) -> list[int]:
    orders = [len(group)]
    current = set(group)
    while len(current) > 1:
        comms = {commutator(a, b) for a in current for b in current}
        current = subgroup_generated(comms)
        orders.append(len(current))
    return orders


def build_certificate() -> dict:
    group = set(sl23())
    classes = conjugacy_classes(group)

    class_rows = []
    anyon_count = 0
    t_order = 1
    for cls in sorted(classes, key=lambda c: (min(order(g) for g in c), len(c))):
        rep = next(iter(cls))
        cent = centralizer(group, rep)
        k_cent = len(conjugacy_classes(cent))
        anyon_count += k_cent
        t_order = lcm(t_order, order(rep))
        class_rows.append(
            {
                "class_size": len(cls),
                "representative_order": order(rep),
                "centralizer_order": len(cent),
                "centralizer_conjugacy_classes": k_cent,
            }
        )

    derived_orders = derived_series_orders(group)
    checks = {
        "sl23_order_is_24": len(group) == 24,
        "conjugacy_class_count_is_7": len(classes) == 7,
        "quantum_double_anyon_count_is_42": anyon_count == 42,
        "T_matrix_order_is_k_12": t_order == K,
        "derived_series_reaches_identity": derived_orders[-1] == 1,
        "twoT_is_solvable": len(derived_orders) > 1 and derived_orders[-1] == 1,
        "braiding_alone_universality_not_promoted": True,
    }

    return {
        "theorem": "BT1695 Dark Anyon Braiding Gate Boundary",
        "verified": all(checks.values()),
        "group": "2T = SL(2,3)",
        "group_order": len(group),
        "conjugacy_classes": class_rows,
        "D_2T_anyon_count": anyon_count,
        "flux_order_lcm": t_order,
        "clock_period_k": K,
        "derived_series_orders": derived_orders,
        "claim_boundary": [
            "D(2T) supplies the finite topological clock and Clifford-like protected routing backbone.",
            "Because 2T is solvable, this certificate does not promote braiding-alone universality.",
            "Universal computation remains the combined architecture: finite braiding backbone plus Hesse/T or Wigner-negative magic injection.",
        ],
        "sources": [
            {
                "label": "Mochon finite-group anyon universality criterion",
                "url": "https://arxiv.org/abs/quant-ph/0206128",
                "role": "External guardrail: non-solvable finite groups are the constructive universal-braiding side.",
            },
            {
                "label": "Local topological magic boundary",
                "path": "analysis/w33_topological_magic.py",
                "role": "Repo anchor for D(2T) as finite backbone requiring magic.",
            },
            {
                "label": "Local dark clock",
                "path": "analysis/w33_clock_is_dark_braiding.py",
                "role": "Repo anchor for T-matrix order 12 as the clock.",
            },
        ],
        "checks": checks,
    }


def main() -> int:
    cert = build_certificate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(cert, indent=2) + "\n", encoding="utf-8")

    print(cert["theorem"])
    print(f"  verified: {cert['verified']}")
    print(f"  |SL(2,3)|: {cert['group_order']}")
    print(f"  D(2T) anyons: {cert['D_2T_anyon_count']}")
    print(f"  T order: {cert['flux_order_lcm']}")
    print(f"  derived series: {cert['derived_series_orders']}")
    print(f"  wrote {OUT}")
    return 0 if cert["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
