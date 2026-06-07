#!/usr/bin/env python3
"""BT503: Tetrahelix Axis Chirality Codec Theorem.

The uploaded BC/Qi Men paper records R. Gray's result:
  * a tetrahelix axis passes through the (7,3) coordinate on a tetrahedron face,
  * there are 12 tetrahelix axes through a single tetrahedron,
  * six are clockwise and six counterclockwise.

This theorem gives the finite combinatorial codec behind that geometry.

A tetrahelix through a tetrahedron visits the four tetrahedron vertices in
some order.  There are 4! = 24 ordered vertex paths.  Reversing a path gives
the same unoriented axis, so there are 24/2 = 12 axis classes.

Because reversal on four letters is an even permutation, permutation parity is
well-defined on the reversal class.  Hence the 12 axes split canonically into:
    6 even + 6 odd,
matching the clockwise/counterclockwise split.

Each axis has two (7,3) face-coordinate endpoints.  Therefore the endpoint
incidence count is:
    12 axes * 2 endpoints = 24,
which is exactly the tetrahedron flag count |S4|.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

VERTICES = tuple(range(4))


def canonical_axis(path: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    rev = tuple(reversed(path))
    return min(path, rev)


def parity(path: tuple[int, ...]) -> str:
    inversions = 0
    for i in range(len(path)):
        for j in range(i + 1, len(path)):
            if path[i] > path[j]:
                inversions += 1
    return "even" if inversions % 2 == 0 else "odd"


def face_point_key(a: int, b: int, c: int) -> tuple[int, int, int]:
    # The (7,3) point has barycentric weights (3,4,3)/10, so exchanging
    # the two outer vertices a,c gives the same point.
    return min((a, b, c), (c, b, a))


def main() -> dict:
    ordered_paths = list(itertools.permutations(VERTICES))
    assert len(ordered_paths) == 24

    axes = sorted({canonical_axis(p) for p in ordered_paths})
    assert len(axes) == 12

    # Reversal preserves parity for length 4 because reversal has 6 inversions.
    for p in ordered_paths:
        assert parity(p) == parity(tuple(reversed(p)))

    chirality_profile = Counter(parity(axis) for axis in axes)
    assert chirality_profile == Counter({"even": 6, "odd": 6})

    # Each axis has a middle tetrahedron edge.  The 12 axes form two sheets over
    # the six K4 edges.
    middle_edge_profile = Counter(tuple(sorted((a[1], a[2]))) for a in axes)
    assert middle_edge_profile == Counter({e: 2 for e in itertools.combinations(VERTICES, 2)})

    # Axis endpoints are the (7,3) face points P(a,b,c) and P(b,c,d).
    endpoint_counter: Counter[tuple[int, int, int]] = Counter()
    endpoints_by_axis = {}
    for axis in axes:
        a, b, c, d = axis
        endpoints = [face_point_key(a, b, c), face_point_key(b, c, d)]
        endpoint_counter.update(endpoints)
        endpoints_by_axis["".join(map(str, axis))] = endpoints

    assert len(endpoint_counter) == 12
    assert Counter(endpoint_counter.values()) == Counter({2: 12})
    assert sum(endpoint_counter.values()) == 24

    # Four faces, three (7,3) points per face.
    face_point_profile = Counter(tuple(sorted(fp)) for fp in endpoint_counter)
    assert face_point_profile == Counter({face: 3 for face in itertools.combinations(VERTICES, 3)})

    # Flags: a tetrahedron has 4 faces * 3 edges per face * 2 vertices per edge = 24.
    tetra_flags = 4 * 3 * 2
    assert tetra_flags == 24 == sum(endpoint_counter.values())

    # Chirality sheets over middle edges: each K4 edge receives one even and one odd axis.
    sheet_by_edge: defaultdict[tuple[int, int], Counter[str]] = defaultdict(Counter)
    for axis in axes:
        edge = tuple(sorted((axis[1], axis[2])))
        sheet_by_edge[edge][parity(axis)] += 1
    assert all(profile == Counter({"even": 1, "odd": 1}) for profile in sheet_by_edge.values())

    results = {
        "theorem": "BT503 Tetrahelix Axis Chirality Codec Theorem",
        "axis_count": {
            "ordered_vertex_paths": 24,
            "reversal_classes": 12,
            "clockwise_counterclockwise_split": {"even": 6, "odd": 6},
        },
        "codec_structure": {
            "axes": ["".join(map(str, a)) for a in axes],
            "middle_edge_profile": {str(k): v for k, v in sorted(middle_edge_profile.items())},
            "chirality_by_middle_edge": {str(k): dict(v) for k, v in sorted(sheet_by_edge.items())},
            "reading": "12 axes = two chirality sheets over the six K4 edges",
        },
        "face_coordinate_structure": {
            "face_points": [str(k) for k in sorted(endpoint_counter)],
            "face_point_count": 12,
            "endpoint_incidence_count": sum(endpoint_counter.values()),
            "endpoint_profile": {str(k): v for k, v in sorted(endpoint_counter.items())},
            "face_point_profile": {str(k): v for k, v in sorted(face_point_profile.items())},
            "endpoints_by_axis": {k: [str(x) for x in v] for k, v in endpoints_by_axis.items()},
        },
        "tetrahedron_flag_identity": {
            "axis_endpoint_incidences": sum(endpoint_counter.values()),
            "tetrahedron_flags": tetra_flags,
            "identity": "12 axes * 2 endpoints = 24 = |S4|",
        },
        "substrate_reading": {
            "12": "local BC-axis codec / d_X*d_Z / W33 valency",
            "6_plus_6": "two chirality sheets over K4 edges",
            "24": "ordered vertex paths / tetrahedron flags / S4",
            "7_3": "face-coordinate gate: 7+3=10-frequency triangular address",
        },
    }

    out = Path("data/PART_BT503_TETRAHELIX_AXIS_CHIRALITY_CODEC_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return results

if __name__ == "__main__":
    main()
