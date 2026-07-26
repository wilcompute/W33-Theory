#!/usr/bin/env python3
"""Pass 1047: distinguish the two order-648 stabilizers in PSp(4,3).

Build W(3,3) from F_3^4, generate PSp(4,3) by symplectic
transvections, and compare the stabilizers in its 40-point and induced
40-line actions.  The calculation is exact; SymPy's Schreier-Sims
algorithms are used only for finite permutation-group operations.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path
from typing import Iterable

import numpy as np
from sympy.combinatorics import Permutation, PermutationGroup

Q = 3
J = np.array(
    [[0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, 0, 1], [0, 0, -1, 0]],
    dtype=int,
) % Q


def normalize(vector: Iterable[int]) -> tuple[int, ...]:
    v = np.array(tuple(vector), dtype=int) % Q
    for coordinate in v:
        if int(coordinate) != 0:
            return tuple(int(x) for x in (v * pow(int(coordinate), -1, Q)) % Q)
    raise ValueError("the zero vector has no projective representative")


def symplectic(x: tuple[int, ...], y: tuple[int, ...]) -> int:
    return int((np.array(x, dtype=int) @ J @ np.array(y, dtype=int)) % Q)


def group_invariants(group: PermutationGroup) -> dict[str, int]:
    derived = group.derived_subgroup()
    center = group.center()
    return {
        "order": int(group.order()),
        "center_order": int(center.order()),
        "derived_order": int(derived.order()),
        "abelianization_order": int(group.order() // derived.order()),
    }


def main() -> dict[str, object]:
    points = sorted(
        {
            normalize(v)
            for v in itertools.product(range(Q), repeat=4)
            if any(v)
        }
    )
    point_index = {p: i for i, p in enumerate(points)}

    lines_set: set[tuple[int, ...]] = set()
    for i, x in enumerate(points):
        for y in points[i + 1 :]:
            if symplectic(x, y) != 0:
                continue
            span = {
                point_index[
                    normalize(
                        (a * np.array(x, dtype=int) + b * np.array(y, dtype=int)) % Q
                    )
                ]
                for a, b in itertools.product(range(Q), repeat=2)
                if (a, b) != (0, 0)
            }
            if len(span) == Q + 1:
                lines_set.add(tuple(sorted(span)))
    lines = sorted(lines_set)
    line_index = {line: i for i, line in enumerate(lines)}

    def transvection(v: tuple[int, ...]) -> Permutation:
        vv = np.array(v, dtype=int)
        images: list[int] = []
        for x in points:
            xx = np.array(x, dtype=int)
            image = (xx + symplectic(x, v) * vv) % Q
            images.append(point_index[normalize(image)])
        return Permutation(images)

    point_generators = [transvection(v) for v in points]
    point_group = PermutationGroup(point_generators)

    def on_lines(g: Permutation) -> Permutation:
        return Permutation(
            [
                line_index[tuple(sorted(g(point) for point in line))]
                for line in lines
            ]
        )

    line_group = PermutationGroup([on_lines(g) for g in point_generators])
    point_stabilizer = point_group.stabilizer(0)
    line_stabilizer = line_group.stabilizer(0)

    point_inv = group_invariants(point_stabilizer)
    line_inv = group_invariants(line_stabilizer)

    checks = {
        "projective_points_40": len(points) == 40,
        "isotropic_lines_40": len(lines) == 40,
        "four_points_per_line": all(len(line) == 4 for line in lines),
        "four_lines_per_point": all(sum(p in line for line in lines) == 4 for p in range(40)),
        "PSp43_point_action_order_25920": point_group.order() == 25920,
        "PSp43_line_action_order_25920": line_group.order() == 25920,
        "point_stabilizer_order_648": point_inv["order"] == 648,
        "line_stabilizer_order_648": line_inv["order"] == 648,
        "point_center_C3": point_inv["center_order"] == 3,
        "point_derived_216": point_inv["derived_order"] == 216,
        "point_abelianization_C3": point_inv["abelianization_order"] == 3,
        "line_center_trivial": line_inv["center_order"] == 1,
        "line_derived_324": line_inv["derived_order"] == 324,
        "line_abelianization_C2": line_inv["abelianization_order"] == 2,
        "stabilizers_nonisomorphic": point_inv != line_inv,
        "Springer_G25_fingerprint_selects_point_side": (
            point_inv
            == {
                "order": 648,
                "center_order": 3,
                "derived_order": 216,
                "abelianization_order": 3,
            }
            and line_inv
            != {
                "order": 648,
                "center_order": 3,
                "derived_order": 216,
                "abelianization_order": 3,
            }
        ),
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise AssertionError(f"Pass 1047 failed: {failed}")

    return {
        "schema": "w33.pass1047.two_648_stabilizers.v1",
        "status": "PASS",
        "headline": (
            "PSp(4,3) has two nonconjugate degree-40 stabilizer classes of order 648. "
            "The W(3,3) point stabilizer has center C3, derived subgroup 216, and "
            "abelianization C3, while the dual line stabilizer has trivial center, "
            "derived subgroup 324, and abelianization C2. The Pass-1046 Springer/G25 "
            "fingerprint therefore selects the W(3,3) point action and excludes the dual action."
        ),
        "geometry": {
            "points": len(points),
            "lines": len(lines),
            "points_per_line": 4,
            "lines_per_point": 4,
        },
        "group_order": int(point_group.order()),
        "point_stabilizer": point_inv,
        "line_stabilizer": line_inv,
        "conclusion": {
            "matching_class": "W(3,3) point stabilizer; ATLAS structure 3^(1+2)+:2A4",
            "excluded_class": "dual Q(4,3) point / W(3,3) line stabilizer; ATLAS structure 3^3:S4",
            "strengthening": (
                "Pass 1046's invariant-level G25 identification is now also a side-selection theorem: "
                "the Eisenstein/Springer tower lands on the symplectic point action, not its non-self-dual orthogonal dual."
            ),
        },
        "check_count": len(checks),
        "checks": checks,
        "scope": (
            "Exact finite permutation-group computation. It distinguishes the two order-648 classes "
            "and matches the Pass-1046 fingerprint. It does not replace the explicit complex "
            "reflection representation of G25 or construct a matrix-level conjugacy."
        ),
    }


if __name__ == "__main__":
    result = main()
    output = Path(__file__).resolve().parents[1] / "data" / "w33_pass1047_two_648_stabilizers.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
