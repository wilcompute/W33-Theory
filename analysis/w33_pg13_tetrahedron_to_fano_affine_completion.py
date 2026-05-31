#!/usr/bin/env python3
"""PG(1,3) / tetrahedron as AG(2,2), completed to the Fano plane.

Previous theorem:
    The C3 overlap A4∩S3 is the cyclic orientation of the three non-anchor
    points on PG(1,3), and can be modeled as the oriented Fano-line triple of
    the three nonzero vectors of F2^2.

This verifier lifts that local triangle to the full Fano plane.

Key construction:
    Identify the four points of PG(1,3) / tetrahedron with the four affine
    points of AG(2,2)=F2^2.

For each anchor p in AG(2,2), the three other affine points q determine the
three nonzero direction vectors q-p.  These directions are the three points on
one distinguished Fano line at infinity.

Thus the local qutrit/tetrahedral triangle at any anchor is the line-at-infinity
Fano triple after translating the anchor to the affine origin.

Full completion:
    Fano plane PG(2,2) = AG(2,2) affine points + 3 directions at infinity.
    The seven lines are:
        1 line at infinity with the three directions;
        6 affine lines, grouped as 3 parallel classes of 2 lines.

This gives the exact bridge:
    four-point tetrahedral geometry = affine chart AG(2,2),
    three non-anchor local choices = directions to line at infinity,
    C3 overlap = cyclic orientation of that infinity/Fano line.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

Vec2 = tuple[int, int]

AFFINE_POINTS: list[Vec2] = [(0, 0), (1, 0), (0, 1), (1, 1)]
DIRECTIONS: list[Vec2] = [(1, 0), (0, 1), (1, 1)]


def add(a: Vec2, b: Vec2) -> Vec2:
    return ((a[0] + b[0]) % 2, (a[1] + b[1]) % 2)


def sub(a: Vec2, b: Vec2) -> Vec2:
    # same as addition over F2
    return add(a, b)


def affine_line(base: Vec2, direction: Vec2) -> tuple[Vec2, Vec2]:
    return tuple(sorted({base, add(base, direction)}))  # type: ignore[return-value]


def all_affine_lines() -> list[tuple[Vec2, Vec2]]:
    return sorted({affine_line(p, d) for p in AFFINE_POINTS for d in DIRECTIONS})


def fano_points() -> list[str]:
    return [f"A{p}" for p in AFFINE_POINTS] + [f"I{d}" for d in DIRECTIONS]


def fano_lines() -> list[tuple[str, str, str]]:
    lines = []
    # line at infinity
    lines.append(tuple(sorted(f"I{d}" for d in DIRECTIONS)))
    for L in all_affine_lines():
        direction = sub(L[0], L[1])
        lines.append(tuple(sorted([f"A{L[0]}", f"A{L[1]}", f"I{direction}"])))
    return sorted(lines)


def cyclic_orientations(triple: tuple[Vec2, Vec2, Vec2]) -> list[tuple[Vec2, Vec2, Vec2]]:
    a, b, c = triple
    return [(a, b, c), (b, c, a), (c, a, b)]


def build_payload() -> dict:
    anchor_records = []
    for p in AFFINE_POINTS:
        nonanchors = [q for q in AFFINE_POINTS if q != p]
        directions = [sub(q, p) for q in nonanchors]
        direction_set = set(directions)
        # map nonanchor q -> direction q-p
        records = [{"nonanchor": q, "direction_to_infinity": sub(q, p)} for q in nonanchors]
        anchor_records.append(
            {
                "anchor": p,
                "nonanchors": nonanchors,
                "direction_records": records,
                "direction_set": sorted(direction_set),
                "directions_are_all_nonzero_F2_2": direction_set == set(DIRECTIONS),
            }
        )

    lines = fano_lines()
    points = fano_points()
    point_line_counts = Counter()
    pair_line_counts = Counter()
    for L in lines:
        for p in L:
            point_line_counts[p] += 1
        for a, b in itertools.combinations(L, 2):
            pair_line_counts[tuple(sorted((a, b)))] += 1

    affine_lines = all_affine_lines()
    parallel_classes = {}
    for d in DIRECTIONS:
        cls = sorted({affine_line(p, d) for p in AFFINE_POINTS})
        parallel_classes[str(d)] = cls

    # C3 orientation on directions: choose (1,0)->(0,1)->(1,1)->(1,0).
    oriented_direction_cycle = ((1, 0), (0, 1), (1, 1))
    oriented_triples = cyclic_orientations(oriented_direction_cycle)
    fano_sum_law = {
        str((a, b)): add(a, b)
        for a, b in itertools.combinations(DIRECTIONS, 2)
    }

    identities = {
        "AG22_has_4_points": len(AFFINE_POINTS) == 4,
        "directions_are_3_nonzero_vectors": len(DIRECTIONS) == 3 and set(DIRECTIONS) == set(p for p in AFFINE_POINTS if p != (0, 0)),
        "each_anchor_sees_all_three_directions": all(r["directions_are_all_nonzero_F2_2"] for r in anchor_records),
        "affine_lines_6": len(affine_lines) == 6,
        "parallel_classes_3_each_size_2": all(len(v) == 2 for v in parallel_classes.values()) and len(parallel_classes) == 3,
        "fano_points_7": len(points) == 7,
        "fano_lines_7": len(lines) == 7,
        "each_fano_line_has_3_points": all(len(L) == 3 for L in lines),
        "each_point_on_3_lines": set(point_line_counts.values()) == {3},
        "each_pair_on_one_line": len(pair_line_counts) == 21 and set(pair_line_counts.values()) == {1},
        "line_at_infinity_present": tuple(sorted(f"I{d}" for d in DIRECTIONS)) in lines,
        "fano_sum_law_on_infinity_line": set(fano_sum_law.values()) == set(DIRECTIONS),
        "oriented_cycle_has_three_rotations": len(oriented_triples) == 3,
    }
    return {
        "theorem": "pg13_tetrahedron_to_fano_affine_completion",
        "construction": {
            "tetrahedron_or_PG13_points": "identified with AG(2,2)=F2^2 affine points",
            "affine_points": AFFINE_POINTS,
            "line_at_infinity_directions": DIRECTIONS,
            "fano_completion": "PG(2,2)=AG(2,2) plus the three directions at infinity",
        },
        "anchor_local_triangles": anchor_records,
        "fano_plane": {
            "points": points,
            "lines": lines,
            "point_line_counts": dict(point_line_counts),
            "affine_lines": affine_lines,
            "parallel_classes": {k: [list(x) for x in v] for k, v in parallel_classes.items()},
            "line_at_infinity": tuple(sorted(f"I{d}" for d in DIRECTIONS)),
        },
        "orientation": {
            "chosen_C3_direction_cycle": oriented_direction_cycle,
            "cyclic_rotations": oriented_triples,
            "fano_sum_law_on_directions": fano_sum_law,
            "interpretation": "The C3 overlap orients the line at infinity; from any affine anchor, the three non-anchor tetrahedral points are translated into this oriented Fano-line direction triple.",
        },
        "conclusion": "The four-point PG(1,3)/tetrahedral object is best modeled as the affine chart AG(2,2) of the Fano plane. The three non-anchor points at a chosen anchor are the three directions to the Fano line at infinity. Thus the local C3 qutrit triangle selects the oriented line-at-infinity triple inside the full seven-point Fano wedge-dot codec.",
        "identities": identities,
        "all_identities_hold": all(identities.values()),
    }


def main() -> None:
    payload = build_payload()
    out = Path("data/w33_pg13_tetrahedron_to_fano_affine_completion.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
