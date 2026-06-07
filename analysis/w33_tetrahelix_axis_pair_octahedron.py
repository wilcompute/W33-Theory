#!/usr/bin/env python3
"""BT507: Tetrahelix Axis-Pair Octahedron Theorem.

The uploaded BC/Qi Men paper states that the 12 green tetrahelix axes through
one tetrahedron come in crossing pairs, and that the six intersection points
define an octahedron.

This theorem verifies the exact coordinate version.

Use the standard tetrahedron:
    (1,1,1), (-1,-1,1), (-1,1,-1), (1,-1,-1).
The (7,3) face coordinate has barycentric weights (3,4,3)/10.
The 12 axes are 4! vertex paths modulo reversal.
The two axes with the same middle K4 edge intersect at one point.
The six such points are exactly:
    ±(2/5)e_x, ±(2/5)e_y, ±(2/5)e_z.
Therefore they form a regular octahedron.

The radius 2/5 is also sqrt(2)/10 * EL for EL=2sqrt(2), matching the
paper's tangent-sphere radius from tetrahedron center of volume to axis.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

import sympy as sp

V = {
    0: sp.Matrix([1, 1, 1]),
    1: sp.Matrix([-1, -1, 1]),
    2: sp.Matrix([-1, 1, -1]),
    3: sp.Matrix([1, -1, -1]),
}


def face_point(a: int, b: int, c: int) -> sp.Matrix:
    return sp.Rational(3, 10) * V[a] + sp.Rational(4, 10) * V[b] + sp.Rational(3, 10) * V[c]


def face_key(a: int, b: int, c: int) -> tuple[int, int, int]:
    return min((a, b, c), (c, b, a))


def canonical_axis(path: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return min(path, tuple(reversed(path)))


def parity(path: tuple[int, ...]) -> str:
    inv = 0
    for i in range(len(path)):
        for j in range(i + 1, len(path)):
            if path[i] > path[j]:
                inv += 1
    return "even" if inv % 2 == 0 else "odd"


def line_intersection(p1: sp.Matrix, d1: sp.Matrix, p2: sp.Matrix, d2: sp.Matrix) -> sp.Matrix:
    s, t = sp.symbols("s t")
    eq = p1 + s * d1 - p2 - t * d2
    sol = sp.solve(list(eq), (s, t), dict=True)
    assert sol, (p1, d1, p2, d2)
    return sp.simplify(p1 + sol[0][s] * d1)


def norm2(v: sp.Matrix) -> sp.Expr:
    return sp.simplify(v.dot(v))


def main() -> dict:
    EL2 = norm2(V[0] - V[1])
    assert EL2 == 8
    EL = 2 * sp.sqrt(2)
    tangent_radius = sp.sqrt(2) / 10 * EL
    assert tangent_radius == sp.Rational(2, 5)

    axes = sorted({canonical_axis(p) for p in itertools.permutations(range(4))})
    assert len(axes) == 12

    by_middle_edge: defaultdict[tuple[int, int], list[dict]] = defaultdict(list)
    for axis in axes:
        a, b, c, d = axis
        u = face_point(*face_key(a, b, c))
        v = face_point(*face_key(b, c, d))
        by_middle_edge[tuple(sorted((b, c)))].append({
            "axis": axis,
            "chirality": parity(axis),
            "point": u,
            "direction": sp.simplify(v - u),
        })

    assert len(by_middle_edge) == 6
    assert all(len(v) == 2 for v in by_middle_edge.values())
    assert all(Counter(a["chirality"] for a in arr) == Counter({"even": 1, "odd": 1}) for arr in by_middle_edge.values())

    intersections = {}
    for edge, arr in by_middle_edge.items():
        p = line_intersection(arr[0]["point"], arr[0]["direction"], arr[1]["point"], arr[1]["direction"])
        intersections[str(edge)] = [sp.simplify(x) for x in p]

    expected = {
        (sp.Rational(2, 5), 0, 0),
        (-sp.Rational(2, 5), 0, 0),
        (0, sp.Rational(2, 5), 0),
        (0, -sp.Rational(2, 5), 0),
        (0, 0, sp.Rational(2, 5)),
        (0, 0, -sp.Rational(2, 5)),
    }
    actual = {tuple(v) for v in intersections.values()}
    assert actual == expected

    # Build octahedron graph by joining points at minimal nonzero distance.
    points = [sp.Matrix(v) for v in sorted(actual, key=str)]
    distances = sorted({norm2(points[i] - points[j]) for i, j in itertools.combinations(range(6), 2)})
    assert distances == [sp.Rational(8, 25), sp.Rational(16, 25)]
    G_edges = []
    for i, j in itertools.combinations(range(6), 2):
        if norm2(points[i] - points[j]) == sp.Rational(8, 25):
            G_edges.append((i, j))
    assert len(G_edges) == 12

    # Octahedron f-vector and scale.
    V_count, E_count, F_count = 6, 12, 8
    assert V_count - E_count + F_count == 2
    oct_edge_length = sp.sqrt(sp.Rational(8, 25))
    assert oct_edge_length == 2 * sp.sqrt(2) / 5
    assert oct_edge_length == EL / 5

    results = {
        "theorem": "BT507 Tetrahelix Axis-Pair Octahedron Theorem",
        "input_geometry": {
            "tetrahedron_edge_length": "2*sqrt(2)",
            "face_coordinate": "(7,3) = barycentric weights (3,4,3)/10",
            "axis_count": 12,
            "axis_pairing": "two chirality axes over each of the six K4 middle edges",
        },
        "intersection_octahedron": {
            "vertices": {k: [str(x) for x in v] for k, v in sorted(intersections.items())},
            "point_set": [str(p) for p in sorted(actual, key=str)],
            "radius": "2/5",
            "radius_identity": "sqrt(2)/10 * EL = 2/5",
            "edge_length": "2*sqrt(2)/5 = EL/5",
            "f_vector": [V_count, E_count, F_count],
            "euler_characteristic": V_count - E_count + F_count,
        },
        "codec_reading": {
            "6": "six K4 edges / six axis-pair intersections / octahedron vertices",
            "12": "twelve tetrahelix axes / octahedron edges",
            "8": "octahedron triangular faces",
            "2/5": "axis tangent-sphere radius from the paper",
            "chirality_pairing": "each K4 edge carries one even and one odd tetrahelix axis that cross at one octahedron vertex",
        },
        "substrate_reading": {
            "Richter_kernel": "the local 12-axis BC switchboard has an octahedral intersection core",
            "K4_to_O6": "tetrahedral axis codec collapses to the octahedron vertices at radius 2/5",
            "memory_now": "each tetrahedral now contains an internal octahedral crossing kernel for possible axis exchange",
        },
    }

    out = Path("data/PART_BT507_TETRAHELIX_AXIS_PAIR_OCTAHEDRON_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return results

if __name__ == "__main__":
    main()
