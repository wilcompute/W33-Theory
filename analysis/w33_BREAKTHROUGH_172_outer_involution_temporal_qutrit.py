"""W(3,3) BREAKTHROUGH 172: outer involution temporal qutrit.

BT171 found the missing order-2 outer involution that lifts the projective
compiler action to the full W(E6) action on the 45-point GQ(4,2) quotient.

BT172 analyzes that involution internally.  Its fixed geometry is not random:

    fixed points = 7 = 2q + 1
    fixed lines  = 3 = q
    fixed graph  = three triangles sharing one central point

The central fixed point is the unique fixed point adjacent to all six other
fixed points.  It is the "now" point.  The three fixed lines through it are
the q=3 temporal axes.  Each fixed line contains three fixed points and one
swapped pair, so each axis carries a past/future conjugate pair.

The 19 swapped point-pairs split exactly into substrate classes:

    19 = 3 + 4 + 12 = q + mu + k.

This is the first concrete finite signature of the user's self-entangled
qutrit picture: the full-W(E6) outer reflection acts as temporal conjugation,
with a fixed "now" fan and past/future pairs around it.
"""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_168_f4_e6_gq42_line_geometry import (  # noqa: E402
    five_cliques,
    quotient_adjacency,
)
from analysis.w33_BREAKTHROUGH_171_gap_full_e6_outer_lift import (  # noqa: E402
    gap_full_e6_outer_lift_packet,
)


Q = 3
MU = 4
K = 12


def _outer_permutation() -> list[int]:
    artifact = ROOT / "data" / "w33_BREAKTHROUGH_171_gap_full_e6_outer_lift.json"
    if artifact.exists():
        packet = json.loads(artifact.read_text(encoding="utf-8"))
    else:
        packet = gap_full_e6_outer_lift_packet()
    return packet["outer_permutation_zero_based"]


def _cycles(permutation: list[int]) -> list[list[int]]:
    seen = set()
    cycles = []
    for start in range(len(permutation)):
        if start in seen:
            continue
        cycle = []
        current = start
        while current not in seen:
            seen.add(current)
            cycle.append(current)
            current = permutation[current]
        cycles.append(cycle)
    return cycles


def outer_involution_temporal_qutrit_packet() -> dict:
    outer = _outer_permutation()
    adjacency, _reps = quotient_adjacency()
    lines = [tuple(line) for line in five_cliques(adjacency)]
    line_sets = [frozenset(line) for line in lines]
    line_to_id = {line: index for index, line in enumerate(line_sets)}
    line_image = [
        line_to_id[frozenset(outer[point] for point in line)]
        for line in line_sets
    ]

    point_cycles = _cycles(outer)
    fixed_points = [cycle[0] for cycle in point_cycles if len(cycle) == 1]
    swapped_pairs = [tuple(cycle) for cycle in point_cycles if len(cycle) == 2]
    fixed_set = set(fixed_points)

    fixed_degrees = {
        point: sum(adjacency[point][other] for other in fixed_points if other != point)
        for point in fixed_points
    }
    now_points = [point for point, degree in fixed_degrees.items() if degree == 2 * Q]
    now_point = now_points[0] if len(now_points) == 1 else None

    fixed_edges = [
        [left, right]
        for index, left in enumerate(fixed_points)
        for right in fixed_points[index + 1 :]
        if adjacency[left][right]
    ]
    fixed_lines = [
        line_id
        for line_id, image_id in enumerate(line_image)
        if line_id == image_id and len(set(lines[line_id]) & fixed_set) == Q
    ]
    fixed_line_fixed_points = {
        line_id: sorted(set(lines[line_id]) & fixed_set)
        for line_id in fixed_lines
    }

    line_cycles = _cycles(line_image)
    line_orbit_signature = Counter(
        (
            len(cycle),
            tuple(len(set(lines[line_id]) & fixed_set) for line_id in cycle),
        )
        for cycle in line_cycles
    )

    pair_classes = Counter()
    pair_class_examples = {}
    for pair in swapped_pairs:
        left, right = pair
        shared_fixed = tuple(
            point for point in fixed_points if adjacency[left][point] and adjacency[right][point]
        )
        fixed_neighbor_incidences = sum(
            1 for point in pair for fixed in fixed_points if adjacency[point][fixed]
        )
        key = (
            adjacency[left][right],
            fixed_neighbor_incidences,
            len(shared_fixed),
            now_point in shared_fixed,
        )
        pair_classes[key] += 1
        pair_class_examples.setdefault(key, []).append(pair)

    named_pair_classes = {
        "axis_past_future_pairs_q": pair_classes[(True, 2 * Q, Q, True)],
        "off_axis_rich_pairs_mu": pair_classes[(False, 2 * Q, Q, False)],
        "residual_pairs_k": pair_classes[(False, 2, 1, False)],
    }

    checks = {
        "outer_is_involution": all(outer[outer[point]] == point for point in range(45)),
        "outer_cycle_shape_is_7_fixed_19_pairs": Counter(len(cycle) for cycle in point_cycles)
        == {1: 2 * Q + 1, 2: 19},
        "fixed_point_count_is_2q_plus_1": len(fixed_points) == 2 * Q + 1 == 7,
        "unique_now_point_has_degree_2q": len(now_points) == 1 and fixed_degrees[now_point] == 2 * Q,
        "other_fixed_points_have_degree_2": Counter(fixed_degrees.values()) == {2: 2 * Q, 2 * Q: 1},
        "fixed_edge_count_is_q_squared": len(fixed_edges) == Q**2 == 9,
        "fixed_lines_are_q": len(fixed_lines) == Q,
        "fixed_lines_all_pass_through_now": all(now_point in fixed_line_fixed_points[line_id] for line_id in fixed_lines),
        "fixed_lines_have_q_fixed_points": all(len(points) == Q for points in fixed_line_fixed_points.values()),
        "fixed_lines_cover_fixed_edges_as_three_triangles": sum(Q for _line in fixed_lines) == len(fixed_edges),
        "point_pairs_split_as_q_mu_k": named_pair_classes
        == {"axis_past_future_pairs_q": Q, "off_axis_rich_pairs_mu": MU, "residual_pairs_k": K},
        "pair_class_sum_is_19": sum(named_pair_classes.values()) == len(swapped_pairs) == 19,
        "line_orbits_are_3_fixed_12_pairs": Counter(len(cycle) for cycle in line_cycles) == {1: Q, 2: K},
        "line_pair_orbits_split_qfact_qfact": line_orbit_signature[(2, (1, 1))] == 6
        and line_orbit_signature[(2, (0, 0))] == 6,
        "fixed_line_orbits_have_three_fixed_points": line_orbit_signature[(1, (Q,))] == Q,
    }

    return {
        "breakthrough": 172,
        "title": "Outer involution temporal qutrit",
        "outer_permutation_zero_based": outer,
        "fixed_points": fixed_points,
        "now_point": now_point,
        "fixed_degrees": fixed_degrees,
        "fixed_edges": fixed_edges,
        "fixed_lines": fixed_lines,
        "fixed_line_fixed_points": fixed_line_fixed_points,
        "point_cycle_length_distribution": dict(sorted(Counter(len(cycle) for cycle in point_cycles).items())),
        "line_cycle_length_distribution": dict(sorted(Counter(len(cycle) for cycle in line_cycles).items())),
        "line_orbit_signature": {str(key): value for key, value in sorted(line_orbit_signature.items())},
        "pair_class_counts": {str(key): value for key, value in sorted(pair_classes.items())},
        "named_pair_classes": named_pair_classes,
        "pair_class_examples": {str(key): value for key, value in sorted(pair_class_examples.items())},
        "architectural_reading": (
            "The BT171 outer involution acts like a finite time-reversal "
            "operator on the 45-point quotient. It fixes a 7-point heptad "
            "organized as three triangles through a unique central now-point; "
            "the three fixed GQ lines through that point are the q=3 temporal "
            "axes. The 19 past/future swapped pairs split as q + mu + k = "
            "3 + 4 + 12. This turns the self-entangled qutrit idea into a "
            "checkable quotient-geometry statement rather than a metaphor."
        ),
        "boundary": (
            "This packet analyzes the GAP-derived outer involution from BT171. "
            "It does not yet construct the involution intrinsically from W(3,3); "
            "that remains the next target."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = outer_involution_temporal_qutrit_packet()

    print("=" * 78)
    print("W(3,3) BREAKTHROUGH 172: OUTER INVOLUTION TEMPORAL QUTRIT")
    print("=" * 78)
    print()
    print(f"fixed points           = {packet['fixed_points']}")
    print(f"now point              = {packet['now_point']}")
    print(f"fixed lines            = {packet['fixed_lines']}")
    print(f"named pair classes     = {packet['named_pair_classes']}")
    print(f"line cycle distribution= {packet['line_cycle_length_distribution']}")
    print(f"verified               = {packet['n_verified']} / {len(packet['checks'])}")
    print()
    print("ARCHITECTURAL READING:")
    print(f"  {packet['architectural_reading']}")

    out = Path("data") / "w33_BREAKTHROUGH_172_outer_involution_temporal_qutrit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print()
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
