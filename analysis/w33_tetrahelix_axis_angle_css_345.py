#!/usr/bin/env python3
"""BT505: Tetrahelix Axis Angle CSS 3-4-5 Theorem.

The uploaded BC/Qi Men paper follows R. Gray's calculation for axes through
(7,3) tetrahedron face coordinates.  It gives the crossing angle:
    beta = 2 asin(1/sqrt(10)) = 36.86989765... degrees.

This theorem extracts the exact substrate content:
    cos(beta)=4/5 and sin(beta)=3/5.
Thus the tetrahelix-axis crossing angle is precisely the 3-4-5 triangle,
matching the CSS-genus roots d_X=3 and d_Z=4.

It also verifies the two table-slope angles in the paper:
    asin(sqrt(3/5)) = 50.76847952... degrees
    asin(1/sqrt(15)) = 14.96321744... degrees
and shows the 12 tetrahelix axes split 6+6 with respect to either slope.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import sympy as sp

VERTICES = {
    0: sp.Matrix([1, 1, 1]),
    1: sp.Matrix([-1, -1, 1]),
    2: sp.Matrix([-1, 1, -1]),
    3: sp.Matrix([1, -1, -1]),
}


def face_point(a: int, b: int, c: int) -> sp.Matrix:
    # (7,3) coordinate has barycentric weights (3,4,3)/10.
    return sp.Rational(3, 10) * VERTICES[a] + sp.Rational(4, 10) * VERTICES[b] + sp.Rational(3, 10) * VERTICES[c]


def face_key(a: int, b: int, c: int) -> tuple[int, int, int]:
    return min((a, b, c), (c, b, a))


def canonical_axis(path: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return min(path, tuple(reversed(path)))


def norm(v: sp.Matrix) -> sp.Expr:
    return sp.sqrt(sp.simplify(v.dot(v)))


def main() -> dict:
    # Regular tetrahedron edge length in this coordinate model.
    edge_lengths = {sp.simplify(norm(VERTICES[i] - VERTICES[j])) for i, j in itertools.combinations(range(4), 2)}
    assert edge_lengths == {2 * sp.sqrt(2)}
    EL = 2 * sp.sqrt(2)

    axes = sorted({canonical_axis(p) for p in itertools.permutations(range(4))})
    assert len(axes) == 12

    # Axis segment lengths between the two (7,3) endpoints.
    axis_segments = []
    axis_dirs = []
    for a, b, c, d in axes:
        u = face_point(*face_key(a, b, c))
        v = face_point(*face_key(b, c, d))
        axis_segments.append(sp.simplify(norm(v - u)))
        axis_dirs.append(sp.simplify(v - u))
    assert set(axis_segments) == {sp.Rational(2, 1) / sp.sqrt(5)}

    small_triangle_edge = EL / 10
    half_angle_sin = sp.simplify((small_triangle_edge / 2) / ((sp.Rational(2, 1) / sp.sqrt(5)) / 2))
    assert half_angle_sin == 1 / sp.sqrt(10)

    beta = 2 * sp.asin(1 / sp.sqrt(10))
    cos_beta = sp.simplify(sp.cos(beta))
    sin_beta = sp.simplify(sp.sin(beta))
    assert cos_beta == sp.Rational(4, 5)
    assert sin_beta == sp.Rational(3, 5)

    # Face-normal slope split.  Relative to a fixed face, the twelve axis directions
    # have absolute dot products sqrt(3/5) and 1/sqrt(15), six each.
    face = (0, 1, 2)
    normal = VERTICES[0] + VERTICES[1] + VERTICES[2]
    slope_cosines = []
    for d in axis_dirs:
        slope_cosines.append(sp.simplify(abs(d.dot(normal)) / (norm(d) * norm(normal))))
    slope_profile = Counter(str(x) for x in slope_cosines)
    assert slope_profile == Counter({"sqrt(15)/5": 6, "sqrt(15)/15": 6})

    high_angle = sp.asin(sp.sqrt(sp.Rational(3, 5)))
    low_angle = sp.asin(1 / sp.sqrt(15))

    # Numeric certificates.
    beta_deg = float(sp.N(beta * 180 / sp.pi, 15))
    high_deg = float(sp.N(high_angle * 180 / sp.pi, 15))
    low_deg = float(sp.N(low_angle * 180 / sp.pi, 15))

    results = {
        "theorem": "BT505 Tetrahelix Axis Angle CSS 3-4-5 Theorem",
        "coordinate_model": {
            "tetrahedron_vertices": {str(k): list(map(str, v)) for k, v in VERTICES.items()},
            "edge_length": "2*sqrt(2)",
            "face_coordinate": "(7,3) = barycentric weights (3,4,3)/10",
        },
        "axis_geometry": {
            "axis_count": len(axes),
            "axis_segment_length": "2/sqrt(5)",
            "small_red_triangle_edge": "EL/10 = sqrt(2)/5",
            "half_crossing_sine": "1/sqrt(10)",
            "crossing_angle_beta": "2*asin(1/sqrt(10))",
            "crossing_angle_degrees": beta_deg,
        },
        "css_345_identity": {
            "sin_beta": str(sin_beta),
            "cos_beta": str(cos_beta),
            "triangle": "3-4-5",
            "reading": "d_X=3 and d_Z=4 appear as the exact sine/cosine legs of the tetrahelix-axis crossing angle",
        },
        "table_slope_split": {
            "cosine_profile_against_fixed_face_normal": dict(slope_profile),
            "high_angle": "asin(sqrt(3/5))",
            "high_angle_degrees": high_deg,
            "low_angle": "asin(1/sqrt(15))",
            "low_angle_degrees": low_deg,
            "reading": "the 12 axes split 6+6 into the two slope classes recorded by R. Gray",
        },
        "substrate_reading": {
            "7_3": "10-frequency face coordinate gate",
            "12": "tetrahelix axes through one tetrahedron",
            "3_4_5": "CSS/percolation roots embedded as axis crossing trigonometry",
            "6_plus_6": "two slope/chirality sheets of the local BC-axis codec",
        },
    }

    out = Path("data/PART_BT505_TETRAHELIX_AXIS_ANGLE_CSS_345_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return results

if __name__ == "__main__":
    main()
