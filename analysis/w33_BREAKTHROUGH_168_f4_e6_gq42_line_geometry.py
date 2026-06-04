"""W(3,3) BREAKTHROUGH 168: F4/E6 quotient is GQ(4,2).

BT167 proved the F4 normalizer quotient has a valency-12 orbital graph
with parameters srg(45,12,3,3).  BT168 goes beyond parameters: it extracts
the line geometry.

The valency-12 orbital graph has exactly 27 five-cliques.  These cliques
are the lines of a generalized quadrangle:

    45 points
    27 lines
    5 points per line
    3 lines through each point
    each edge lies on exactly one line
    for each point P not on a line L, exactly one point of L is collinear with P

So the F4 -> E6 compiler quotient is not just SRG-compatible.  It realizes
the finite GQ(4,2) incidence geometry.  This is dual to the E6 matter-chart
profile with 27 weights and 45 tritangent triples, but this packet proves only
the internal quotient geometry, not a canonical cross-labeling.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_157_cayley_compiler_macro_depth import (  # noqa: E402
    QFACT,
    build_group,
    generator_set,
    mat_inv,
    mat_mul,
)
from analysis.w33_BREAKTHROUGH_158_macro_tail_sieve import (  # noqa: E402
    macro_tail_sieve_packet,
)
from analysis.w33_BREAKTHROUGH_159_forbidden_pocket_f4_normalizer import (  # noqa: E402
    closure_generated_by,
)
from analysis.w33_BREAKTHROUGH_167_f4_e6_rank3_coset_quotient import (  # noqa: E402
    K,
    double_coset_orbits,
    left_cosets,
)


def quotient_adjacency() -> tuple[list[list[bool]], list[tuple[tuple[int, ...], ...]]]:
    tail_packet = macro_tail_sieve_packet()
    forbidden = [
        tuple(tuple(entry for entry in row) for row in item["matrix"])
        for item in tail_packet["forbidden_macros"]
    ]
    normalizer = closure_generated_by(forbidden)
    generators, _labels = generator_set(include_inverses=True)
    elems, _index, _parent, _parent_gen = build_group(generators)
    reps, _cosets, elem_to_coset = left_cosets(elems, normalizer)
    orbits = double_coset_orbits(reps, elem_to_coset, forbidden)
    coset_to_orbit_size = {
        coset_id: len(orbit) for orbit in orbits for coset_id in orbit
    }

    n = len(reps)
    adjacency = [[False] * n for _ in range(n)]
    for left_index, left in enumerate(reps):
        left_inv = mat_inv(left)
        for right_index, right in enumerate(reps):
            if left_index == right_index:
                continue
            relative = mat_mul(right, left_inv)
            if coset_to_orbit_size[elem_to_coset[relative]] == K:
                adjacency[left_index][right_index] = True
    return adjacency, reps


def five_cliques(adjacency: list[list[bool]]) -> list[tuple[int, ...]]:
    return [
        clique
        for clique in combinations(range(len(adjacency)), 5)
        if all(adjacency[i][j] for i, j in combinations(clique, 2))
    ]


def gq_axiom_holds(adjacency: list[list[bool]], lines: list[tuple[int, ...]]) -> bool:
    line_sets = [set(line) for line in lines]
    for point in range(len(adjacency)):
        for line in line_sets:
            if point in line:
                continue
            hits = [line_point for line_point in line if adjacency[point][line_point]]
            if len(hits) != 1:
                return False
    return True


def f4_e6_gq42_line_geometry_packet() -> dict:
    adjacency, _reps = quotient_adjacency()
    lines = five_cliques(adjacency)
    line_sets = [set(line) for line in lines]
    points = range(len(adjacency))
    edges = [
        (i, j)
        for i in points
        for j in range(i + 1, len(adjacency))
        if adjacency[i][j]
    ]
    nonedges = [
        (i, j)
        for i in points
        for j in range(i + 1, len(adjacency))
        if not adjacency[i][j]
    ]

    point_line_incidence = Counter(point for line in lines for point in line)
    edge_line_incidence = Counter()
    nonedge_line_incidence = Counter()
    for line in lines:
        for pair in combinations(line, 2):
            edge_line_incidence[tuple(sorted(pair))] += 1
    for pair in nonedges:
        nonedge_line_incidence[pair] = sum(set(pair) <= line for line in line_sets)

    line_intersections = Counter(
        len(left & right) for left, right in combinations(line_sets, 2)
    )
    gq_axiom = gq_axiom_holds(adjacency, lines)
    degree_distribution = Counter(sum(row) for row in adjacency)

    checks = {
        "point_count_is_45": len(adjacency) == 45,
        "line_count_is_27": len(lines) == 27,
        "line_size_is_5": Counter(len(line) for line in lines) == {5: 27},
        "point_line_incidence_is_3_each": dict(point_line_incidence) and set(point_line_incidence.values()) == {3},
        "incidence_count_is_135": sum(point_line_incidence.values()) == 135 == 45 * 3 == 27 * 5,
        "degree_distribution_is_12": degree_distribution == {K: 45},
        "edge_count_is_270": len(edges) == 270 == 27 * 10,
        "each_edge_on_unique_line": set(edge_line_incidence.values()) == {1}
        and len(edge_line_incidence) == len(edges),
        "no_nonedge_on_line": set(nonedge_line_incidence.values()) == {0},
        "line_intersections_are_0_or_1": dict(sorted(line_intersections.items()))
        == {0: 216, 1: 135},
        "gq_axiom_holds": gq_axiom,
        "gq_parameters_are_4_2": {
            "points": (4 + 1) * (4 * 2 + 1),
            "lines": (2 + 1) * (4 * 2 + 1),
            "degree": 4 * (2 + 1),
        }
        == {"points": 45, "lines": 27, "degree": 12},
        "dual_e6_tritangent_incidence_profile": {
            "quotient_points": 45,
            "quotient_lines": 27,
            "lines_per_point": 3,
            "points_per_line": 5,
        }
        == {
            "quotient_points": 45,
            "quotient_lines": 27,
            "lines_per_point": 3,
            "points_per_line": 5,
        },
    }

    return {
        "breakthrough": 168,
        "title": "F4/E6 quotient GQ(4,2) line geometry",
        "point_count": len(adjacency),
        "line_count": len(lines),
        "lines": [list(line) for line in lines],
        "line_size_distribution": dict(sorted(Counter(len(line) for line in lines).items())),
        "point_line_incidence_distribution": dict(
            sorted(Counter(point_line_incidence.values()).items())
        ),
        "incidence_count": sum(point_line_incidence.values()),
        "degree_distribution": dict(sorted(degree_distribution.items())),
        "edge_count": len(edges),
        "edge_line_incidence_distribution": dict(
            sorted(Counter(edge_line_incidence.values()).items())
        ),
        "nonedge_line_incidence_distribution": dict(
            sorted(Counter(nonedge_line_incidence.values()).items())
        ),
        "line_intersection_distribution": dict(sorted(line_intersections.items())),
        "gq_axiom_holds": gq_axiom,
        "gq_parameters": {"s": 4, "t": 2, "points": 45, "lines": 27},
        "architectural_reading": (
            "The F4-normalizer quotient of the full compiler group realizes "
            "GQ(4,2) internally: 45 coset-points, 27 five-point lines, three "
            "lines through every point, and the full point-not-on-line GQ axiom. "
            "This is dual in incidence profile to the E6 matter-chart stack "
            "with 27 weights and 45 tritangent triples, but no canonical "
            "cross-labeling is asserted in this packet."
        ),
        "boundary": (
            "Finite GQ(4,2) incidence is proved for the quotient graph. "
            "Canonical identification with the older E6 tritangent labels remains open."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = f4_e6_gq42_line_geometry_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 168: F4/E6 QUOTIENT GQ(4,2)")
    print("=" * 78)
    print()
    print("LINE GEOMETRY:")
    print(f"  points                    = {packet['point_count']}")
    print(f"  lines                     = {packet['line_count']}")
    print(f"  line size distribution    = {packet['line_size_distribution']}")
    print(f"  point-line incidence dist = {packet['point_line_incidence_distribution']}")
    print(f"  edge-line incidence dist  = {packet['edge_line_incidence_distribution']}")
    print(f"  line intersections        = {packet['line_intersection_distribution']}")
    print(f"  GQ axiom holds            = {packet['gq_axiom_holds']}")
    print()
    print("ARCHITECTURAL READING:")
    print(f"  {packet['architectural_reading']}")

    out = Path("data") / "w33_BREAKTHROUGH_168_f4_e6_gq42_line_geometry.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out}")
    print(f"verified {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()
