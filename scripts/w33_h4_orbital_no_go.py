"""PSp(4,3)-invariant obstruction for a 600-cell graph on M_120.

Supplement L constructs the 120 line-matching states M_120.  A tempting
next step is to declare a 600-cell graph on these states.  The 600-cell
skeleton is 12-regular, so a fully W(3,3)-canonical construction would
need a PSp(4,3)-invariant 12-regular relation on M_120.

This script computes the unordered pair orbitals of the full PSp(4,3)
action on M_120.  Their degrees are:

    2, 27, 36, 54.

No subset of these degrees sums to 12, so no full-symmetry invariant
600-cell adjacency exists on M_120.  Any H4/600-cell adjacency must
therefore choose extra structure, i.e. break PSp(4,3) to a smaller
icosahedral/golden subgroup.
"""
from __future__ import annotations

import json
import sys
from collections import Counter, deque
from functools import lru_cache
from itertools import combinations
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.w33_algebra_qca import build_w33_geometry
from scripts.w33_h4_line_matching_shadow import (
    _matching_key,
    build_h4_shadow,
    build_lines_from_w33,
)


DEFAULT_OUTPUT = ROOT / "data" / "w33_h4_orbital_no_go_summary.json"


def _line_intersection_graph() -> tuple[list[tuple[int, int, int, int]], dict[int, set[int]]]:
    """Return the 40-line intersection graph of W(3,3)."""
    lines, _edge_set, _adj = build_lines_from_w33()
    line_adjacency = {line_id: set() for line_id in range(len(lines))}
    for left, right in combinations(range(len(lines)), 2):
        if set(lines[left]) & set(lines[right]):
            line_adjacency[left].add(right)
            line_adjacency[right].add(left)
    return lines, line_adjacency


def _symplectic_matrix_for_w33() -> np.ndarray:
    """Matrix S with B(x,y)=x^T S y for build_w33_geometry's symplectic form."""
    S = np.zeros((4, 4), dtype=int)
    S[0, 3] = 1
    S[1, 2] = -1
    S[2, 1] = 1
    S[3, 0] = -1
    return S % 3


def _normalize_projective(v: np.ndarray) -> tuple[int, int, int, int]:
    vals = [int(x) % 3 for x in v]
    for x in vals:
        pass
    for x in vals:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % 3 for y in vals)
    raise ValueError("zero vector has no projective representative")


def _transvection_matrix(u: tuple[int, int, int, int], S: np.ndarray) -> np.ndarray:
    """Symplectic transvection T_u(v)=v+B(v,u)u over F3."""
    col = np.array(u, dtype=int).reshape((4, 1))
    return (np.eye(4, dtype=int) + col @ (S @ col).T) % 3


def _vertex_permutation(M: np.ndarray, points: list[tuple[int, int, int, int]]) -> tuple[int, ...]:
    out: list[int] = []
    for point in points:
        image = _normalize_projective(M @ np.array(point, dtype=int))
        out.append(points.index(image))
    return tuple(out)


def build_state_generators() -> list[tuple[int, ...]]:
    """Return PSp(4,3) transvection generators acting on M_120 states."""
    summary = build_h4_shadow()
    states = summary["states"]
    lines, _edge_set, _adj = build_lines_from_w33()
    points, _edges, _adj0, _triangles, _J = build_w33_geometry()

    state_lookup = {
        (tuple(state["line"]), tuple(tuple(e) for e in state["matching"])): state["state_id"]
        for state in states
    }

    def map_state_perm(vperm: tuple[int, ...]) -> tuple[int, ...]:
        out: list[int] = []
        for state in states:
            img_line = tuple(sorted(vperm[x] for x in state["line"]))
            img_matching = _matching_key(
                (
                    tuple(vperm[x] for x in state["matching"][0]),
                    tuple(vperm[x] for x in state["matching"][1]),
                )
            )
            out.append(state_lookup[(img_line, img_matching)])
        return tuple(out)

    S = _symplectic_matrix_for_w33()
    generators: list[tuple[int, ...]] = []
    for point in points:
        vertex_perm = _vertex_permutation(_transvection_matrix(point, S), points)
        state_perm = map_state_perm(vertex_perm)
        if state_perm not in generators:
            generators.append(state_perm)
    return generators


@lru_cache(maxsize=1)
def _full_vertex_permutation_group() -> list[tuple[int, ...]]:
    """Return the full PSp(4,3) action on the 40 W(3,3) points."""
    points, _edges, _adj, _triangles, _J = build_w33_geometry()
    S = _symplectic_matrix_for_w33()
    generators = [
        _vertex_permutation(_transvection_matrix(point, S), points)
        for point in points
    ]

    identity = tuple(range(len(points)))
    group = [identity]
    seen = {identity}
    queue = deque([identity])
    while queue:
        current = queue.popleft()
        for gen in generators:
            new_perm = tuple(gen[i] for i in current)
            if new_perm not in seen:
                seen.add(new_perm)
                group.append(new_perm)
                queue.append(new_perm)
    return group


@lru_cache(maxsize=1)
def _full_line_permutation_group() -> list[tuple[int, ...]]:
    """Return the induced PSp(4,3) action on the 40 isotropic lines."""
    lines, _line_adjacency = _line_intersection_graph()
    line_lookup = {tuple(line): line_id for line_id, line in enumerate(lines)}
    return [
        tuple(line_lookup[tuple(sorted(vertex_perm[x] for x in line))] for line in lines)
        for vertex_perm in _full_vertex_permutation_group()
    ]


def _canonical_cycle(cycle: tuple[int, ...]) -> tuple[int, ...]:
    """Canonicalize an undirected cycle up to rotation and reversal."""
    n = len(cycle)
    forward = tuple(cycle)
    backward = tuple(reversed(cycle))
    candidates: list[tuple[int, ...]] = []
    for index in range(n):
        candidates.append(forward[index:] + forward[:index])
        candidates.append(backward[index:] + backward[:index])
    return min(candidates)


def _simple_line_graph_cycles(length: int) -> list[tuple[int, ...]]:
    """Enumerate simple undirected cycles of a fixed length in the line graph."""
    _lines, line_adjacency = _line_intersection_graph()
    found: set[tuple[int, ...]] = set()
    for start in range(len(line_adjacency)):
        stack: list[tuple[int, list[int], set[int]]] = [(start, [start], {start})]
        while stack:
            current, path, seen = stack.pop()
            if len(path) == length:
                if start in line_adjacency[current]:
                    found.add(_canonical_cycle(tuple(path)))
                continue
            for nxt in line_adjacency[current]:
                if nxt == start or nxt in seen or nxt < start:
                    continue
                stack.append((nxt, path + [nxt], seen | {nxt}))
    return sorted(found)


def _simple_point_graph_cycles(length: int) -> list[tuple[int, ...]]:
    """Enumerate simple undirected cycles of a fixed length in the point graph."""
    points, _edges, adjacency, _triangles, _J = build_w33_geometry()
    adjacency_sets = {point_id: set(neighbours) for point_id, neighbours in adjacency.items()}
    found: set[tuple[int, ...]] = set()
    for start in range(len(points)):
        stack: list[tuple[int, list[int], set[int]]] = [(start, [start], {start})]
        while stack:
            current, path, seen = stack.pop()
            if len(path) == length:
                if start in adjacency_sets[current]:
                    found.add(_canonical_cycle(tuple(path)))
                continue
            for nxt in adjacency_sets[current]:
                if nxt == start or nxt in seen or nxt < start:
                    continue
                stack.append((nxt, path + [nxt], seen | {nxt}))
    return sorted(found)


def _cycle_orbit_partition(
    cycles: list[tuple[int, ...]], line_group: list[tuple[int, ...]]
) -> list[list[tuple[int, ...]]]:
    """Partition cycles into full PSp(4,3) orbits on the line graph."""
    unseen = set(cycles)
    orbits: list[list[tuple[int, ...]]] = []
    while unseen:
        seed = unseen.pop()
        orbit = {
            _canonical_cycle(tuple(line_perm[vertex] for vertex in seed))
            for line_perm in line_group
        }
        for cycle in orbit:
            unseen.discard(cycle)
        orbits.append(sorted(orbit))
    return sorted(orbits, key=len)


def _square_dihedral_position_permutations() -> set[tuple[int, int, int, int]]:
    """Return the 8 permutations preserving the cyclic square on positions 0..3."""
    square = (0, 1, 2, 3)
    reverse = tuple(reversed(square))
    perms: set[tuple[int, int, int, int]] = set()
    for index in range(4):
        forward = square[index:] + square[:index]
        backward = reverse[index:] + reverse[:index]
        perms.add(tuple(forward.index(position) for position in square))
        perms.add(tuple(backward.index(position) for position in square))
    return perms


def compute_pair_orbitals() -> dict[str, Any]:
    """Compute unordered pair orbitals for PSp(4,3) on M_120."""
    summary = build_h4_shadow()
    states = summary["states"]
    generators = build_state_generators()

    unseen = {(i, j) for i in range(120) for j in range(i + 1, 120)}
    orbitals: list[set[tuple[int, int]]] = []
    while unseen:
        seed = unseen.pop()
        orbit = {seed}
        queue = deque([seed])
        while queue:
            a, b = queue.popleft()
            for gen in generators:
                x, y = gen[a], gen[b]
                if x > y:
                    x, y = y, x
                pair = (x, y)
                if pair not in orbit:
                    orbit.add(pair)
                    queue.append(pair)
                    unseen.discard(pair)
        orbitals.append(orbit)

    records: list[dict[str, Any]] = []
    for orbital in sorted(orbitals, key=len):
        degree_counter: Counter[int] = Counter()
        same_line = intersecting_line = disjoint_line = 0
        for i, j in orbital:
            degree_counter[i] += 1
            degree_counter[j] += 1
            li, lj = states[i]["line_id"], states[j]["line_id"]
            if li == lj:
                same_line += 1
            elif set(states[i]["line"]) & set(states[j]["line"]):
                intersecting_line += 1
            else:
                disjoint_line += 1
        degrees = sorted(set(degree_counter.values()))
        assert len(degrees) == 1
        records.append(
            {
                "size": len(orbital),
                "degree": degrees[0],
                "same_line_pairs": same_line,
                "intersecting_line_pairs": intersecting_line,
                "disjoint_line_pairs": disjoint_line,
            }
        )

    orbital_degrees = [r["degree"] for r in records]
    possible_invariant_degrees = sorted(
        {
            sum(deg for bit, deg in enumerate(orbital_degrees) if mask & (1 << bit))
            for mask in range(1 << len(orbital_degrees))
        }
    )

    checks = {
        "state_count_is_120": len(states) == 120,
        "generator_count_is_40": len(generators) == 40,
        "pair_orbital_count_is_4": len(records) == 4,
        "orbital_degrees_are_2_27_36_54": orbital_degrees == [2, 27, 36, 54],
        "pair_sizes_sum_to_all_pairs": sum(r["size"] for r in records) == 120 * 119 // 2,
        "no_invariant_degree_12_relation": 12 not in possible_invariant_degrees,
    }

    theorem = {
        "no_full_psp43_invariant_600_cell_skeleton_on_M120": checks[
            "no_invariant_degree_12_relation"
        ],
        "reason": "The only invariant orbital degrees are 2, 27, 36, and 54; no subset sums to 12.",
        "required_next_structure": "A 600-cell/H4 adjacency must break PSp(4,3) to a smaller icosahedral or golden-ratio subgroup.",
    }

    return {
        "orbitals": records,
        "orbital_degrees": orbital_degrees,
        "possible_invariant_degrees": possible_invariant_degrees,
        "checks": checks,
        "theorem": theorem,
    }


def compute_local_selector_reduction() -> dict[str, Any]:
    """Reduce the local H4-selector problem to S3 transport on the line graph.

    The 120 matching states form a 3-state fibre above each of the 40 isotropic
    lines. The intersecting-line orbital has degree 36, and the 40-line
    intersection graph is itself SRG(40,12,2,4). Therefore any local 12-regular
    selector supported on the intersecting orbital must choose exactly one state
    on each of the 12 adjacent lines. On each adjacent pair of lines, the 3x3
    block is consequently a perfect matching, i.e. a permutation in S3.
    """
    shadow = build_h4_shadow()
    pair_orbitals = compute_pair_orbitals()
    lines, line_adjacency = _line_intersection_graph()

    states = shadow["states"]
    line_to_states: dict[int, list[int]] = {line_id: [] for line_id in range(len(lines))}
    for state in states:
        line_to_states[int(state["line_id"])].append(int(state["state_id"]))

    line_degrees = sorted(len(neighbours) for neighbours in line_adjacency.values())
    line_edges = sum(line_degrees) // 2

    adjacent_common_counts: list[int] = []
    disjoint_common_counts: list[int] = []
    for left, right in combinations(range(len(lines)), 2):
        shared = len(line_adjacency[left] & line_adjacency[right])
        if right in line_adjacency[left]:
            adjacent_common_counts.append(shared)
        else:
            disjoint_common_counts.append(shared)

    fibre_size = len(line_to_states[0])
    intersecting_state_degree = pair_orbitals["orbitals"][2]["degree"]

    checks = {
        "forty_lines_each_carry_three_matching_states": (
            len(lines) == 40 and sorted(len(state_ids) for state_ids in line_to_states.values()) == [3] * 40
        ),
        "line_intersection_graph_is_srg_40_12_2_4": (
            len(lines) == 40
            and line_degrees == [12] * 40
            and line_edges == 240
            and set(adjacent_common_counts) == {2}
            and set(disjoint_common_counts) == {4}
        ),
        "intersecting_state_degree_is_12_times_3": (
            intersecting_state_degree == 36 and len(line_adjacency[0]) == 12 and fibre_size == 3
        ),
        "one_state_per_adjacent_line_gives_degree_12": 12 * fibre_size == intersecting_state_degree,
        "each_local_selector_block_is_a_permutation_in_s3": 3 * 2 * 1 == 6,
    }

    theorem = {
        "the_h4_selector_base_graph_is_the_self_dual_line_copy_of_w33": (
            checks["line_intersection_graph_is_srg_40_12_2_4"]
            and shadow["constants"]["w33_lines"] == 40
            and shadow["constants"]["w33_edges"] == 240
        ),
        "any_local_12_neighborhood_selector_on_M120_is_equivalent_to_s3_transport_on_that_base_graph": (
            checks["forty_lines_each_carry_three_matching_states"]
            and checks["line_intersection_graph_is_srg_40_12_2_4"]
            and checks["intersecting_state_degree_is_12_times_3"]
            and checks["one_state_per_adjacent_line_gives_degree_12"]
            and checks["each_local_selector_block_is_a_permutation_in_s3"]
        ),
        "interpretation": (
            "The missing 600-cell datum is a ternary transport law: one S3 "
            "permutation for each adjacent pair of isotropic lines in the self-dual "
            "40-line W33 graph."
        ),
    }

    return {
        "line_graph": {
            "vertex_count": len(lines),
            "degree": line_degrees[0],
            "edge_count": line_edges,
            "adjacent_common_neighbor_count": adjacent_common_counts[0],
            "disjoint_common_neighbor_count": disjoint_common_counts[0],
        },
        "matching_fibres": {
            "fibre_size": fibre_size,
            "state_count": len(states),
            "states_per_intersecting_line_block": fibre_size,
            "intersecting_state_degree": intersecting_state_degree,
        },
        "selector_reduction": {
            "adjacent_lines_per_base_vertex": len(line_adjacency[0]),
            "one_state_choice_per_adjacent_line": len(line_adjacency[0]),
            "local_block_shape": [fibre_size, fibre_size],
            "local_permutation_count": 6,
            "undirected_transport_edges": line_edges,
            "directed_transport_edges": 2 * line_edges,
        },
        "checks": checks,
        "theorem": theorem,
    }


def compute_point_residue_transport_reduction() -> dict[str, Any]:
    """Refine the selector problem to point-anchored transport on W(3,3) residues.

    If two isotropic lines are adjacent in the 40-line graph, then they meet in a
    unique W(3,3) point. Relative to that anchor point, each of the three matching
    states on an incident line is canonically the choice of which of the three
    remaining points on the line is paired with the anchor. The missing H4 datum
    therefore lives on the K4 residue of lines through each point, not just on an
    abstract three-state fibre.
    """
    shadow = build_h4_shadow()
    lines, line_adjacency = _line_intersection_graph()
    points, _edges, _adj, _triangles, _J = build_w33_geometry()

    states = shadow["states"]
    line_to_states: dict[int, list[int]] = {line_id: [] for line_id in range(len(lines))}
    for state in states:
        line_to_states[int(state["line_id"])].append(int(state["state_id"]))

    point_to_lines: dict[int, list[int]] = {point_id: [] for point_id in range(len(points))}
    for line_id, line in enumerate(lines):
        for point_id in line:
            point_to_lines[point_id].append(line_id)

    incident_partner_sets: list[tuple[int, int, list[int], list[int]]] = []
    for point_id, incident_lines in point_to_lines.items():
        for line_id in incident_lines:
            partner_choices: list[int] = []
            for state_id in line_to_states[line_id]:
                state = states[state_id]
                partner = None
                for left, right in state["matching"]:
                    if left == point_id:
                        partner = right
                        break
                    if right == point_id:
                        partner = left
                        break
                if partner is None:
                    raise AssertionError(
                        f"state {state_id} on line {line_id} does not pair anchor point {point_id}"
                    )
                partner_choices.append(int(partner))
            incident_partner_sets.append(
                (
                    point_id,
                    line_id,
                    sorted(partner_choices),
                    sorted(vertex for vertex in lines[line_id] if vertex != point_id),
                )
            )

    anchor_points: list[int] = []
    uniform_block_patterns: set[tuple[tuple[tuple[int, tuple[int, ...], int], ...], ...]] = set()
    uniform_cell_signatures: set[tuple[int, tuple[int, ...], int]] = set()
    for left in range(len(lines)):
        for right in line_adjacency[left]:
            if left >= right:
                continue
            shared_points = set(lines[left]) & set(lines[right])
            if len(shared_points) != 1:
                raise AssertionError(
                    f"adjacent lines {left} and {right} share {len(shared_points)} points"
                )
            point_id = next(iter(shared_points))
            anchor_points.append(point_id)

            residue_lines = sorted(point_to_lines[point_id])
            other_residue_lines = [line_id for line_id in residue_lines if line_id not in (left, right)]
            left_points = [vertex for vertex in lines[left] if vertex != point_id]
            right_points = [vertex for vertex in lines[right] if vertex != point_id]
            forbidden_vertices = set(lines[left]) | set(lines[right]) | {point_id}

            block_signature: list[tuple[tuple[int, tuple[int, ...], int], ...]] = []
            for left_vertex in left_points:
                row_signature: list[tuple[int, tuple[int, ...], int]] = []
                for right_vertex in right_points:
                    common_neighbors = set(_adj[left_vertex]) & set(_adj[right_vertex])
                    signature = (
                        len(common_neighbors),
                        tuple(
                            sum(
                                1
                                for vertex in common_neighbors
                                if vertex in lines[line_id] and vertex != point_id
                            )
                            for line_id in other_residue_lines
                        ),
                        sum(1 for vertex in common_neighbors if vertex not in forbidden_vertices),
                    )
                    row_signature.append(signature)
                    uniform_cell_signatures.add(signature)
                block_signature.append(tuple(row_signature))
            uniform_block_patterns.add(tuple(block_signature))

    lines_per_point = sorted(len(incident_lines) for incident_lines in point_to_lines.values())
    undirected_pairs_per_point = [len(incident_lines) * (len(incident_lines) - 1) // 2 for incident_lines in point_to_lines.values()]
    directed_pairs_per_point = [len(incident_lines) * (len(incident_lines) - 1) for incident_lines in point_to_lines.values()]
    residue_triangle_count = sum(
        len(incident_lines) * (len(incident_lines) - 1) * (len(incident_lines) - 2) // 6
        for incident_lines in point_to_lines.values()
    )

    checks = {
        "each_point_lies_on_four_isotropic_lines": lines_per_point == [4] * len(points),
        "each_incident_line_fibre_is_the_three_partner_choices_at_the_anchor_point": all(
            partner_choices == line_without_anchor
            for _point_id, _line_id, partner_choices, line_without_anchor in incident_partner_sets
        ),
        "each_adjacent_line_pair_has_a_unique_anchor_point": len(anchor_points) == 240,
        "point_residue_transport_slots_match_line_graph_edges": (
            sum(undirected_pairs_per_point) == 240 and sum(directed_pairs_per_point) == 480
        ),
        "each_point_residue_is_a_k4_of_incident_lines": all(
            all(
                right in line_adjacency[left]
                for left, right in combinations(incident_lines, 2)
            )
            for incident_lines in point_to_lines.values()
        ),
        "every_adjacent_line_block_has_one_uniform_first_order_signature": (
            len(uniform_block_patterns) == 1 and len(uniform_cell_signatures) == 1
        ),
    }

    theorem = {
        "each_transport_edge_is_anchored_at_a_unique_w33_point": (
            checks["each_adjacent_line_pair_has_a_unique_anchor_point"]
            and checks["point_residue_transport_slots_match_line_graph_edges"]
        ),
        "the_s3_selector_problem_refines_to_point_residue_transport_on_40_k4_stars": (
            checks["each_point_lies_on_four_isotropic_lines"]
            and checks["each_incident_line_fibre_is_the_three_partner_choices_at_the_anchor_point"]
            and checks["each_adjacent_line_pair_has_a_unique_anchor_point"]
            and checks["point_residue_transport_slots_match_line_graph_edges"]
            and checks["each_point_residue_is_a_k4_of_incident_lines"]
        ),
        "bare_point_residue_geometry_does_not_single_out_a_transport_permutation": (
            checks["every_adjacent_line_block_has_one_uniform_first_order_signature"]
        ),
        "interpretation": (
            "The missing H4 datum is a point-anchored S3 connection: at each W33 "
            "point the four incident isotropic lines form a K4 residue, and each "
            "ordered line pair in that residue carries one ternary transport map."
        ),
    }

    return {
        "point_residues": {
            "point_count": len(points),
            "lines_per_point": lines_per_point[0],
            "undirected_line_pairs_per_point": undirected_pairs_per_point[0],
            "directed_line_pairs_per_point": directed_pairs_per_point[0],
            "triangles_per_point": 4,
            "total_residue_triangles": residue_triangle_count,
        },
        "fibre_indexing": {
            "states_per_line": len(line_to_states[0]),
            "partner_choices_per_incident_point": 3,
            "incident_point_line_records": len(incident_partner_sets),
        },
        "transport_slots": {
            "undirected_line_graph_edges": len(anchor_points),
            "directed_line_graph_edges": 2 * len(anchor_points),
            "undirected_residue_slots": sum(undirected_pairs_per_point),
            "directed_residue_slots": sum(directed_pairs_per_point),
        },
        "local_block_uniformity": {
            "distinct_adjacent_line_block_patterns": len(uniform_block_patterns),
            "distinct_cell_signatures": len(uniform_cell_signatures),
            "cell_signature": {
                "common_neighbor_count": next(iter(uniform_cell_signatures))[0],
                "other_residue_line_counts": list(next(iter(uniform_cell_signatures))[1]),
                "outside_residue_common_neighbor_count": next(iter(uniform_cell_signatures))[2],
            },
        },
        "checks": checks,
        "theorem": theorem,
    }


def compute_anchored_local_symmetry_obstruction() -> dict[str, Any]:
    """Show anchored local symmetry still leaves the 3x3 choice block undistinguished.

    The group PSp(4,3) is transitive on the 480 ordered anchored transport slots
    (point p together with an ordered pair of distinct isotropic lines through p).
    By orbit-stabilizer, a canonical anchored slot has stabilizer size 54. That
    stabilizer acts transitively on the 9 possible state-pairs above the ordered
    line pair, so even fixing the anchor point and transport direction does not
    canonically distinguish a local bijection.
    """
    points, _edges, _adj, _triangles, _J = build_w33_geometry()
    lines, _line_adjacency = _line_intersection_graph()
    point_to_lines: dict[int, list[int]] = {point_id: [] for point_id in range(len(points))}
    for line_id, line in enumerate(lines):
        for point_id in line:
            point_to_lines[point_id].append(line_id)

    vertex_group = _full_vertex_permutation_group()
    line_group = _full_line_permutation_group()

    ordered_anchored_slots = [
        (point_id, left, right)
        for point_id, incident_lines in point_to_lines.items()
        for left in incident_lines
        for right in incident_lines
        if left != right
    ]
    seed_slot = ordered_anchored_slots[0]

    slot_orbit = {
        (vertex_perm[seed_slot[0]], line_perm[seed_slot[1]], line_perm[seed_slot[2]])
        for vertex_perm, line_perm in zip(vertex_group, line_group)
    }

    anchor_point, left_line, right_line = seed_slot
    left_points = [vertex for vertex in lines[left_line] if vertex != anchor_point]
    right_points = [vertex for vertex in lines[right_line] if vertex != anchor_point]
    local_choice_pairs = [(left, right) for left in left_points for right in right_points]

    anchored_stabilizer = [
        vertex_perm
        for vertex_perm, line_perm in zip(vertex_group, line_group)
        if vertex_perm[anchor_point] == anchor_point
        and line_perm[left_line] == left_line
        and line_perm[right_line] == right_line
    ]

    unseen = set(local_choice_pairs)
    local_orbits: list[list[tuple[int, int]]] = []
    while unseen:
        orbit_seed = unseen.pop()
        orbit = {orbit_seed}
        queue = deque([orbit_seed])
        while queue:
            left, right = queue.popleft()
            for vertex_perm in anchored_stabilizer:
                image = (vertex_perm[left], vertex_perm[right])
                if image not in orbit:
                    orbit.add(image)
                    queue.append(image)
                    unseen.discard(image)
        local_orbits.append(sorted(orbit))

    checks = {
        "full_psp43_group_has_order_25920": len(vertex_group) == 25_920,
        "ordered_anchored_transport_slots_total_480": len(ordered_anchored_slots) == 480,
        "psp43_is_transitive_on_ordered_anchored_slots": len(slot_orbit) == len(ordered_anchored_slots),
        "anchored_slot_stabilizer_has_order_54": len(anchored_stabilizer) == 54,
        "orbit_stabilizer_identity_holds": len(vertex_group) == len(slot_orbit) * len(anchored_stabilizer),
        "anchored_stabilizer_is_transitive_on_the_nine_local_choices": sorted(len(orbit) for orbit in local_orbits) == [9],
    }

    theorem = {
        "even_after_fixing_a_point_and_an_ordered_transport_edge_the_nine_local_choices_remain_symmetry_equivalent": (
            checks["psp43_is_transitive_on_ordered_anchored_slots"]
            and checks["anchored_slot_stabilizer_has_order_54"]
            and checks["anchored_stabilizer_is_transitive_on_the_nine_local_choices"]
        ),
        "interpretation": (
            "The missing H4 datum does not live in any point-local or edge-local "
            "canonical decoration. Even after fixing the anchor point and an ordered "
            "transport slot, local PSp(4,3) symmetry still sees the full 3x3 choice "
            "block as a single orbit."
        ),
    }

    return {
        "group_action": {
            "group_order": len(vertex_group),
            "ordered_anchored_slot_count": len(ordered_anchored_slots),
            "seed_slot_orbit_size": len(slot_orbit),
            "seed_slot_stabilizer_size": len(anchored_stabilizer),
        },
        "local_choice_block": {
            "shape": [len(left_points), len(right_points)],
            "choice_count": len(local_choice_pairs),
            "stabilizer_orbit_sizes": sorted(len(orbit) for orbit in local_orbits),
        },
        "checks": checks,
        "theorem": theorem,
    }


def compute_cycle_holonomy_carrier() -> dict[str, Any]:
    """Identify the first line-graph cycle carrier where symmetry splits.

    Triangles in the 40-line graph are still a single PSp(4,3) orbit, so they do
    not provide a canonical holonomy distinction. The first split appears on
    4-cycles: there is a local orbit of size 120 given by Hamiltonian cycles in
    the K4 residue at a point, and a nonlocal orbit of size 1620 whose four edge
    anchors are distinct and whose opposite line pairs are disjoint.
    """
    lines, _line_adjacency = _line_intersection_graph()
    line_group = _full_line_permutation_group()

    triangle_cycles = _simple_line_graph_cycles(3)
    quadrangle_cycles = _simple_line_graph_cycles(4)
    triangle_orbits = _cycle_orbit_partition(triangle_cycles, line_group)
    quadrangle_orbits = _cycle_orbit_partition(quadrangle_cycles, line_group)

    quadrangle_records: list[dict[str, Any]] = []
    for orbit in quadrangle_orbits:
        seed = orbit[0]
        edge_anchors = [
            tuple(sorted(set(lines[seed[index]]) & set(lines[seed[(index + 1) % 4]])))
            for index in range(4)
        ]
        all_four_intersection = sorted(
            set(lines[seed[0]]) & set(lines[seed[1]]) & set(lines[seed[2]]) & set(lines[seed[3]])
        )
        opposite_intersections = [
            tuple(sorted(set(lines[seed[index]]) & set(lines[seed[(index + 2) % 4]])))
            for index in range(2)
        ]
        quadrangle_records.append(
            {
                "orbit_size": len(orbit),
                "seed_cycle": list(seed),
                "distinct_edge_anchor_count": len(set(edge_anchors)),
                "all_four_line_intersection_size": len(all_four_intersection),
                "opposite_intersection_sizes": [len(shared) for shared in opposite_intersections],
                "is_local_residue_cycle": len(all_four_intersection) == 1,
            }
        )

    local_quadrangle_orbit = next(record for record in quadrangle_records if record["is_local_residue_cycle"])
    nonlocal_quadrangle_orbit = next(record for record in quadrangle_records if not record["is_local_residue_cycle"])

    checks = {
        "triangle_cycles_total_160": len(triangle_cycles) == 160,
        "triangles_form_one_psp43_orbit": [len(orbit) for orbit in triangle_orbits] == [160],
        "quadrangle_cycles_total_1740": len(quadrangle_cycles) == 1_740,
        "quadrangles_split_into_two_orbits_120_and_1620": sorted(
            len(orbit) for orbit in quadrangle_orbits
        ) == [120, 1_620],
        "small_quadrangle_orbit_is_exactly_the_local_residue_k4_cycles": (
            local_quadrangle_orbit["orbit_size"] == 120
            and local_quadrangle_orbit["distinct_edge_anchor_count"] == 1
            and local_quadrangle_orbit["all_four_line_intersection_size"] == 1
            and local_quadrangle_orbit["opposite_intersection_sizes"] == [1, 1]
        ),
        "large_quadrangle_orbit_is_nonlocal_with_four_distinct_anchors": (
            nonlocal_quadrangle_orbit["orbit_size"] == 1_620
            and nonlocal_quadrangle_orbit["distinct_edge_anchor_count"] == 4
            and nonlocal_quadrangle_orbit["all_four_line_intersection_size"] == 0
            and nonlocal_quadrangle_orbit["opposite_intersection_sizes"] == [0, 0]
        ),
    }

    theorem = {
        "the_first_nontrivial_holonomy_carrier_appears_on_four_cycles": (
            checks["triangle_cycles_total_160"]
            and checks["triangles_form_one_psp43_orbit"]
            and checks["quadrangle_cycles_total_1740"]
            and checks["quadrangles_split_into_two_orbits_120_and_1620"]
        ),
        "the_local_120_orbit_is_residue_tetrahedral_and_the_1620_orbit_is_the_first_global_quadrangle_carrier": (
            checks["small_quadrangle_orbit_is_exactly_the_local_residue_k4_cycles"]
            and checks["large_quadrangle_orbit_is_nonlocal_with_four_distinct_anchors"]
        ),
        "interpretation": (
            "Local residue loops remain symmetry-forced, but nonlocal quadrangles "
            "already split off as a distinct orbit. Any genuine finite holonomy law "
            "can therefore first register on the 1620 global 4-cycles."
        ),
    }

    return {
        "triangle_cycles": {
            "cycle_count": len(triangle_cycles),
            "orbit_sizes": [len(orbit) for orbit in triangle_orbits],
        },
        "quadrangle_cycles": {
            "cycle_count": len(quadrangle_cycles),
            "orbit_sizes": [len(orbit) for orbit in quadrangle_orbits],
            "orbit_records": quadrangle_records,
        },
        "checks": checks,
        "theorem": theorem,
    }


def compute_quadrangle_self_duality() -> dict[str, Any]:
    """Show the first global 4-cycle carrier is canonically self-dual.

    The 1620 nonlocal 4-cycles on the line graph map to the 1620 nonlocal
    4-cycles on the point graph by sending each line-edge to its unique anchor
    point. The inverse map sends a nonlocal point 4-cycle to the 4-cycle of
    unique isotropic lines joining adjacent point pairs. The local 120 cycles on
    each side are excluded for the same reason: they lie entirely inside a single
    residue K4 (on the line side) or a single isotropic line K4 (on the point side).
    """
    lines, _line_adjacency = _line_intersection_graph()
    line_quadrangles = _simple_line_graph_cycles(4)
    point_quadrangles = _simple_point_graph_cycles(4)
    point_orbits = _cycle_orbit_partition(point_quadrangles, _full_vertex_permutation_group())

    local_point_quadrangles: list[tuple[int, ...]] = []
    nonlocal_point_quadrangles: list[tuple[int, ...]] = []
    for cycle in point_quadrangles:
        containing_lines = [line_id for line_id, line in enumerate(lines) if all(vertex in line for vertex in cycle)]
        if containing_lines:
            local_point_quadrangles.append(cycle)
        else:
            nonlocal_point_quadrangles.append(cycle)

    nonlocal_line_quadrangles: list[tuple[int, ...]] = []
    anchor_map: dict[tuple[int, ...], tuple[int, ...]] = {}
    anchor_collisions = 0
    for cycle in line_quadrangles:
        edge_anchors = [
            next(iter(set(lines[cycle[index]]) & set(lines[cycle[(index + 1) % 4]])))
            for index in range(4)
        ]
        if len(set(edge_anchors)) != 4:
            continue
        all_four_intersection = set(lines[cycle[0]])
        for index in range(1, 4):
            all_four_intersection &= set(lines[cycle[index]])
        if all_four_intersection:
            continue
        opposite_intersections = [
            set(lines[cycle[index]]) & set(lines[cycle[(index + 2) % 4]])
            for index in range(2)
        ]
        if any(opposite_intersections):
            continue
        nonlocal_line_quadrangles.append(cycle)
        anchor_cycle = _canonical_cycle(tuple(edge_anchors))
        if anchor_cycle in anchor_map and anchor_map[anchor_cycle] != cycle:
            anchor_collisions += 1
        anchor_map.setdefault(anchor_cycle, cycle)

    line_for_edge: dict[tuple[int, int], int] = {}
    for line_id, line in enumerate(lines):
        for left, right in combinations(line, 2):
            line_for_edge[tuple(sorted((left, right)))] = line_id

    inverse_failures = 0
    nonlocal_line_set = set(nonlocal_line_quadrangles)
    for cycle in nonlocal_point_quadrangles:
        line_cycle = _canonical_cycle(
            tuple(
                line_for_edge[tuple(sorted((cycle[index], cycle[(index + 1) % 4])))]
                for index in range(4)
            )
        )
        if line_cycle not in nonlocal_line_set:
            inverse_failures += 1
            continue
        recovered_anchor_cycle = _canonical_cycle(
            tuple(
                next(iter(set(lines[line_cycle[index]]) & set(lines[line_cycle[(index + 1) % 4]])))
                for index in range(4)
            )
        )
        if recovered_anchor_cycle != cycle:
            inverse_failures += 1

    checks = {
        "point_quadrangles_total_1740": len(point_quadrangles) == 1_740,
        "point_quadrangles_split_into_local_120_and_nonlocal_1620": (
            len(local_point_quadrangles) == 120 and len(nonlocal_point_quadrangles) == 1_620
        ),
        "point_quadrangles_form_two_psp43_orbits_120_and_1620": sorted(
            len(orbit) for orbit in point_orbits
        ) == [120, 1_620],
        "anchor_map_from_nonlocal_line_quadrangles_is_injective": anchor_collisions == 0,
        "anchor_map_hits_all_nonlocal_point_quadrangles": len(anchor_map) == len(nonlocal_point_quadrangles) == 1_620,
        "inverse_edge_line_map_recovers_every_nonlocal_point_quadrangle": inverse_failures == 0,
    }

    theorem = {
        "the_first_global_holonomy_carrier_is_a_self_dual_1620_quadrangle_correspondence": (
            checks["point_quadrangles_total_1740"]
            and checks["point_quadrangles_split_into_local_120_and_nonlocal_1620"]
            and checks["point_quadrangles_form_two_psp43_orbits_120_and_1620"]
            and checks["anchor_map_from_nonlocal_line_quadrangles_is_injective"]
            and checks["anchor_map_hits_all_nonlocal_point_quadrangles"]
            and checks["inverse_edge_line_map_recovers_every_nonlocal_point_quadrangle"]
        ),
        "interpretation": (
            "The first nonlocal carrier is canonically self-dual: each global line "
            "quadrangle determines a unique global point quadrangle of anchors, and "
            "each global point quadrangle reconstructs the unique line quadrangle of "
            "its adjacent-point joins."
        ),
    }

    return {
        "point_quadrangles": {
            "cycle_count": len(point_quadrangles),
            "orbit_sizes": sorted(len(orbit) for orbit in point_orbits),
            "local_cycle_count": len(local_point_quadrangles),
            "nonlocal_cycle_count": len(nonlocal_point_quadrangles),
        },
        "line_point_duality": {
            "nonlocal_line_quadrangle_count": len(nonlocal_line_quadrangles),
            "nonlocal_point_quadrangle_count": len(nonlocal_point_quadrangles),
            "anchor_image_size": len(anchor_map),
            "anchor_collision_count": anchor_collisions,
            "inverse_failure_count": inverse_failures,
        },
        "checks": checks,
        "theorem": theorem,
    }


def compute_quadrangle_stabilizer_structure() -> dict[str, Any]:
    """Resolve the symmetry type of the first global quadrangle carrier.

    A nonlocal quadrangle in the 1620-orbit has stabilizer size 16 inside
    PSp(4,3). Its visible action on both the line square and the anchor square is
    the full dihedral group D4 of order 8. The remaining factor is a 2-element
    kernel invisible on both squares.
    """
    cycle_summary = compute_cycle_holonomy_carrier()
    seed_cycle = tuple(
        next(record for record in cycle_summary["quadrangle_cycles"]["orbit_records"] if record["orbit_size"] == 1_620)["seed_cycle"]
    )
    lines, _line_adjacency = _line_intersection_graph()
    anchor_cycle = tuple(
        next(iter(set(lines[seed_cycle[index]]) & set(lines[seed_cycle[(index + 1) % 4]])))
        for index in range(4)
    )

    stabilizer: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
    for vertex_perm, line_perm in zip(_full_vertex_permutation_group(), _full_line_permutation_group()):
        if _canonical_cycle(tuple(line_perm[line_id] for line_id in seed_cycle)) == seed_cycle:
            stabilizer.append((vertex_perm, line_perm))

    line_position_perms = {
        tuple(seed_cycle.index(line_perm[seed_cycle[index]]) for index in range(4))
        for _vertex_perm, line_perm in stabilizer
    }
    anchor_position_perms = {
        tuple(anchor_cycle.index(vertex_perm[anchor_cycle[index]]) for index in range(4))
        for vertex_perm, _line_perm in stabilizer
    }

    line_kernel_size = sum(
        1
        for _vertex_perm, line_perm in stabilizer
        if all(line_perm[line_id] == line_id for line_id in seed_cycle)
    )
    anchor_kernel_size = sum(
        1
        for vertex_perm, _line_perm in stabilizer
        if all(vertex_perm[point_id] == point_id for point_id in anchor_cycle)
    )

    expected_d4 = _square_dihedral_position_permutations()
    checks = {
        "nonlocal_quadrangle_stabilizer_has_order_16": len(stabilizer) == 16,
        "visible_line_square_action_has_order_8": len(line_position_perms) == 8,
        "visible_anchor_square_action_has_order_8": len(anchor_position_perms) == 8,
        "visible_actions_match_the_full_dihedral_square_group": (
            line_position_perms == expected_d4 and anchor_position_perms == expected_d4
        ),
        "hidden_kernel_has_order_2_on_line_and_anchor_squares": (
            line_kernel_size == 2 and anchor_kernel_size == 2
        ),
        "orbit_stabilizer_for_global_quadrangles_holds": 25_920 == 1_620 * len(stabilizer),
    }

    theorem = {
        "the_first_global_quadrangle_carrier_has_visible_d4_square_symmetry_with_a_hidden_c2_kernel": (
            checks["nonlocal_quadrangle_stabilizer_has_order_16"]
            and checks["visible_line_square_action_has_order_8"]
            and checks["visible_anchor_square_action_has_order_8"]
            and checks["visible_actions_match_the_full_dihedral_square_group"]
            and checks["hidden_kernel_has_order_2_on_line_and_anchor_squares"]
            and checks["orbit_stabilizer_for_global_quadrangles_holds"]
        ),
        "interpretation": (
            "The first nonlocal holonomy carrier is a self-dual square with full D4 "
            "visible symmetry, together with an additional 2-fold symmetry that is "
            "invisible on both the line square and the anchor square."
        ),
    }

    return {
        "stabilizer": {
            "size": len(stabilizer),
            "visible_line_square_action_size": len(line_position_perms),
            "visible_anchor_square_action_size": len(anchor_position_perms),
            "hidden_line_kernel_size": line_kernel_size,
            "hidden_anchor_kernel_size": anchor_kernel_size,
        },
        "visible_square_symmetry": {
            "position_permutation_count": len(expected_d4),
            "position_permutations": [list(perm) for perm in sorted(expected_d4)],
        },
        "checks": checks,
        "theorem": theorem,
    }


def compute_quadrangle_kernel_fibre_action() -> dict[str, Any]:
    """Resolve the hidden C2 on the four ternary fibres of a nonlocal quadrangle.

    For a seed nonlocal quadrangle, the unique nontrivial element of the hidden
    kernel fixes the line square and the anchor square pointwise. On each of the
    four line fibres (3 matching states over that line), it fixes the unique state
    pairing the two anchor points together and swaps the other two mixed states.
    So the hidden ambiguity is not amorphous: fibrewise it is exactly a 1+2 split.
    """
    cycle_summary = compute_cycle_holonomy_carrier()
    seed_cycle = tuple(
        next(record for record in cycle_summary["quadrangle_cycles"]["orbit_records"] if record["orbit_size"] == 1_620)["seed_cycle"]
    )
    lines, _line_adjacency = _line_intersection_graph()
    anchor_cycle = tuple(
        next(iter(set(lines[seed_cycle[index]]) & set(lines[seed_cycle[(index + 1) % 4]])))
        for index in range(4)
    )

    stabilizer: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
    for vertex_perm, line_perm in zip(_full_vertex_permutation_group(), _full_line_permutation_group()):
        if _canonical_cycle(tuple(line_perm[line_id] for line_id in seed_cycle)) == seed_cycle:
            stabilizer.append((vertex_perm, line_perm))

    hidden_kernel = [
        (vertex_perm, line_perm)
        for vertex_perm, line_perm in stabilizer
        if all(line_perm[line_id] == line_id for line_id in seed_cycle)
        and all(vertex_perm[point_id] == point_id for point_id in anchor_cycle)
    ]
    identity_vertex = tuple(range(len(_full_vertex_permutation_group()[0])))
    nontrivial_kernel_vertex = next(vertex_perm for vertex_perm, _line_perm in hidden_kernel if vertex_perm != identity_vertex)

    shadow = build_h4_shadow()
    states = shadow["states"]
    state_lookup = {
        (tuple(state["line"]), tuple(tuple(edge) for edge in state["matching"])): int(state["state_id"])
        for state in states
    }
    line_to_states: dict[int, list[int]] = {line_id: [] for line_id in range(len(lines))}
    for state in states:
        line_to_states[int(state["line_id"])].append(int(state["state_id"]))

    def map_state(state_id: int) -> int:
        state = states[state_id]
        image_line = tuple(sorted(nontrivial_kernel_vertex[vertex] for vertex in state["line"]))
        image_matching = _matching_key(
            (
                tuple(nontrivial_kernel_vertex[vertex] for vertex in state["matching"][0]),
                tuple(nontrivial_kernel_vertex[vertex] for vertex in state["matching"][1]),
            )
        )
        return state_lookup[(image_line, image_matching)]

    fibre_records: list[dict[str, Any]] = []
    fixed_state_count = 0
    transposition_count = 0
    for line_id in seed_cycle:
        line_points = tuple(lines[line_id])
        line_anchors = tuple(sorted(point for point in line_points if point in anchor_cycle))
        line_nonanchors = tuple(sorted(point for point in line_points if point not in anchor_cycle))
        local_states = sorted(line_to_states[line_id])

        fixed_state_ids: list[int] = []
        swapped_pairs: list[list[int]] = []
        seen_states: set[int] = set()
        anchor_pair_state_id = -1
        for state_id in local_states:
            image_state_id = map_state(state_id)
            if image_state_id == state_id:
                fixed_state_ids.append(state_id)
                matching_edges = {tuple(edge) for edge in states[state_id]["matching"]}
                if tuple(sorted(line_anchors)) in {tuple(sorted(edge)) for edge in matching_edges}:
                    anchor_pair_state_id = state_id
            elif state_id not in seen_states:
                swapped_pairs.append(sorted([state_id, image_state_id]))
                seen_states.add(state_id)
                seen_states.add(image_state_id)

        fixed_state_count += len(fixed_state_ids)
        transposition_count += len(swapped_pairs)
        fibre_records.append(
            {
                "line_id": line_id,
                "anchors": list(line_anchors),
                "nonanchors": list(line_nonanchors),
                "fixed_state_ids": fixed_state_ids,
                "anchor_pair_state_id": anchor_pair_state_id,
                "swapped_state_pairs": swapped_pairs,
            }
        )

    checks = {
        "hidden_kernel_has_two_elements": len(hidden_kernel) == 2,
        "nontrivial_hidden_kernel_fixes_the_four_line_ids": all(
            nontrivial_kernel_vertex[anchor] == anchor for anchor in anchor_cycle
        ),
        "each_quadrangle_line_has_two_anchor_points_and_two_nonanchors": all(
            len(record["anchors"]) == 2 and len(record["nonanchors"]) == 2 for record in fibre_records
        ),
        "each_line_fibre_has_exactly_one_fixed_state": all(
            len(record["fixed_state_ids"]) == 1 for record in fibre_records
        ),
        "the_unique_fixed_state_is_the_anchor_pair_matching": all(
            record["fixed_state_ids"] == [record["anchor_pair_state_id"]] for record in fibre_records
        ),
        "each_line_fibre_has_one_swapped_pair": all(
            len(record["swapped_state_pairs"]) == 1 and len(record["swapped_state_pairs"][0]) == 2
            for record in fibre_records
        ),
        "kernel_cycle_type_on_the_twelve_quadrangle_states_is_1^4_2^4": (
            fixed_state_count == 4 and transposition_count == 4
        ),
    }

    theorem = {
        "the_hidden_c2_acts_fibrewise_as_anchor_pair_fixing_and_cross_state_swap": (
            checks["hidden_kernel_has_two_elements"]
            and checks["each_quadrangle_line_has_two_anchor_points_and_two_nonanchors"]
            and checks["each_line_fibre_has_exactly_one_fixed_state"]
            and checks["the_unique_fixed_state_is_the_anchor_pair_matching"]
            and checks["each_line_fibre_has_one_swapped_pair"]
            and checks["kernel_cycle_type_on_the_twelve_quadrangle_states_is_1^4_2^4"]
        ),
        "interpretation": (
            "The hidden twofold ambiguity on a global quadrangle is fibrewise exact: "
            "on each of the four ternary line fibres, one anchor-pair state is fixed "
            "and the other two mixed states are exchanged."
        ),
    }

    return {
        "kernel": {
            "size": len(hidden_kernel),
            "fixed_anchor_count": len(anchor_cycle),
            "quadrangle_line_count": len(seed_cycle),
        },
        "fibre_action": {
            "fixed_state_count": fixed_state_count,
            "swapped_pair_count": transposition_count,
            "cycle_type": [1, 1, 1, 1, 2, 2, 2, 2],
            "line_records": fibre_records,
        },
        "checks": checks,
        "theorem": theorem,
    }


_COVER_ACTION_IDENTITY = ((0, 1, 2, 3), (0, 0, 0, 0))
_COVER_ACTION_DECK = ((0, 1, 2, 3), (1, 1, 1, 1))


def _cover_action_record(action: tuple[tuple[int, ...], tuple[int, ...]]) -> dict[str, list[int]]:
    return {
        "block_permutation": list(action[0]),
        "within_block_flips": list(action[1]),
    }


def _compose_cover_action(
    left: tuple[tuple[int, int, int, int], tuple[int, int, int, int]],
    right: tuple[tuple[int, int, int, int], tuple[int, int, int, int]],
) -> tuple[tuple[int, int, int, int], tuple[int, int, int, int]]:
    left_blocks, left_bits = left
    right_blocks, right_bits = right
    block_part = tuple(left_blocks[index] for index in right_blocks)
    bit_part = tuple(right_bits[index] ^ left_bits[right_blocks[index]] for index in range(4))
    return block_part, bit_part


def _inverse_cover_action(
    action: tuple[tuple[int, int, int, int], tuple[int, int, int, int]],
    action_group: list[tuple[tuple[int, int, int, int], tuple[int, int, int, int]]],
) -> tuple[tuple[int, int, int, int], tuple[int, int, int, int]]:
    for candidate in action_group:
        if (
            _compose_cover_action(action, candidate) == _COVER_ACTION_IDENTITY
            and _compose_cover_action(candidate, action) == _COVER_ACTION_IDENTITY
        ):
            return candidate
    raise AssertionError("cover action is not invertible inside its stabilizer group")


def _cover_action_order(
    action: tuple[tuple[int, int, int, int], tuple[int, int, int, int]],
    action_group: list[tuple[tuple[int, int, int, int], tuple[int, int, int, int]]],
) -> int:
    current = _COVER_ACTION_IDENTITY
    for exponent in range(1, len(action_group) + 1):
        current = _compose_cover_action(action, current)
        if current == _COVER_ACTION_IDENTITY:
            return exponent
    raise AssertionError("cover action order exceeds the stabilizer action size")


def _quadrangle_mixed_cover_action_data() -> dict[str, Any]:
    cycle_summary = compute_cycle_holonomy_carrier()
    seed_cycle = tuple(
        next(record for record in cycle_summary["quadrangle_cycles"]["orbit_records"] if record["orbit_size"] == 1_620)["seed_cycle"]
    )
    lines, _line_adjacency = _line_intersection_graph()
    anchor_cycle = tuple(
        next(iter(set(lines[seed_cycle[index]]) & set(lines[seed_cycle[(index + 1) % 4]])))
        for index in range(4)
    )

    stabilizer: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
    for vertex_perm, line_perm in zip(_full_vertex_permutation_group(), _full_line_permutation_group()):
        if _canonical_cycle(tuple(line_perm[line_id] for line_id in seed_cycle)) == seed_cycle:
            stabilizer.append((vertex_perm, line_perm))

    shadow = build_h4_shadow()
    states = shadow["states"]
    state_lookup = {
        (tuple(state["line"]), tuple(tuple(edge) for edge in state["matching"])): int(state["state_id"])
        for state in states
    }
    line_to_states: dict[int, list[int]] = {line_id: [] for line_id in range(len(lines))}
    for state in states:
        line_to_states[int(state["line_id"])].append(int(state["state_id"]))

    def map_state(vertex_perm: tuple[int, ...], state_id: int) -> int:
        state = states[state_id]
        image_line = tuple(sorted(vertex_perm[vertex] for vertex in state["line"]))
        image_matching = _matching_key(
            (
                tuple(vertex_perm[vertex] for vertex in state["matching"][0]),
                tuple(vertex_perm[vertex] for vertex in state["matching"][1]),
            )
        )
        return state_lookup[(image_line, image_matching)]

    fixed_states: list[int] = []
    mixed_blocks: list[tuple[int, int]] = []
    mixed_state_to_block: dict[int, int] = {}
    for line_id in seed_cycle:
        line_anchors = tuple(sorted(point for point in lines[line_id] if point in anchor_cycle))
        anchor_pair = tuple(sorted(line_anchors))
        block: list[int] = []
        for state_id in sorted(line_to_states[line_id]):
            matching_edges = {tuple(sorted(edge)) for edge in states[state_id]["matching"]}
            if anchor_pair in matching_edges:
                fixed_states.append(state_id)
            else:
                block.append(state_id)
        block_tuple = tuple(sorted(block))
        mixed_blocks.append(block_tuple)
        for state_id in block_tuple:
            mixed_state_to_block[state_id] = len(mixed_blocks) - 1

    action_group: set[tuple[tuple[int, int, int, int], tuple[int, int, int, int]]] = set()
    visible_action_counts: Counter[tuple[int, int, int, int]] = Counter()
    for vertex_perm, _line_perm in stabilizer:
        block_permutation: list[int] = []
        within_bits: list[int] = []
        for block in mixed_blocks:
            image_left = map_state(vertex_perm, block[0])
            image_right = map_state(vertex_perm, block[1])
            target_block_index = mixed_state_to_block[image_left]
            if mixed_state_to_block[image_right] != target_block_index:
                raise AssertionError("mixed block image left the 2-state block partition")
            target_block = mixed_blocks[target_block_index]
            block_permutation.append(target_block_index)
            within_bits.append(0 if (image_left, image_right) == target_block else 1)
        action_pair = (tuple(block_permutation), tuple(within_bits))
        action_group.add(action_pair)
        visible_action_counts[tuple(block_permutation)] += 1

    return {
        "fixed_states": fixed_states,
        "mixed_blocks": mixed_blocks,
        "action_group": action_group,
        "visible_action_counts": visible_action_counts,
        "deck_involution": _COVER_ACTION_DECK if _COVER_ACTION_DECK in action_group else None,
    }


def compute_quadrangle_mixed_cover_structure() -> dict[str, Any]:
    """Resolve the 8 mixed states as a 2-sheeted cover of the visible square.

    The 12 states over a nonlocal quadrangle split into a 4-state fixed orbit and
    an 8-state mixed orbit. The mixed orbit is partitioned into four 2-state
    blocks, one block per quadrangle line. The quadrangle stabilizer acts on the
    blocks through the visible D4 square symmetry, and each visible D4 element has
    exactly two lifts to the mixed orbit, differing by the hidden deck involution.
    """
    data = _quadrangle_mixed_cover_action_data()
    fixed_states = data["fixed_states"]
    mixed_blocks = data["mixed_blocks"]
    mixed_action_pairs = data["action_group"]
    visible_action_counts = data["visible_action_counts"]
    deck_involution = data["deck_involution"]

    checks = {
        "quadrangle_bundle_splits_into_fixed_4_and_mixed_8": (
            len(fixed_states) == 4 and sum(len(block) for block in mixed_blocks) == 8
        ),
        "mixed_orbit_is_partitioned_into_four_2_state_blocks": (
            len(mixed_blocks) == 4 and sorted(len(block) for block in mixed_blocks) == [2, 2, 2, 2]
        ),
        "visible_block_action_is_exactly_d4": set(visible_action_counts) == _square_dihedral_position_permutations(),
        "each_visible_d4_element_has_exactly_two_lifts_to_the_mixed_cover": set(visible_action_counts.values()) == {2},
        "mixed_cover_action_has_size_16": len(mixed_action_pairs) == 16,
        "global_deck_involution_exists": deck_involution == ((0, 1, 2, 3), (1, 1, 1, 1)),
    }

    theorem = {
        "the_mixed_8_state_orbit_is_a_two_sheeted_cover_of_the_visible_square": (
            checks["quadrangle_bundle_splits_into_fixed_4_and_mixed_8"]
            and checks["mixed_orbit_is_partitioned_into_four_2_state_blocks"]
            and checks["visible_block_action_is_exactly_d4"]
            and checks["each_visible_d4_element_has_exactly_two_lifts_to_the_mixed_cover"]
            and checks["mixed_cover_action_has_size_16"]
            and checks["global_deck_involution_exists"]
        ),
        "interpretation": (
            "The 8 mixed quadrangle states form an exact 2-sheeted cover of the "
            "visible D4 square. The hidden C2 is the global deck involution that "
            "swaps the two sheets simultaneously on all four line blocks."
        ),
    }

    return {
        "bundle_split": {
            "fixed_state_count": len(fixed_states),
            "mixed_state_count": sum(len(block) for block in mixed_blocks),
            "mixed_block_count": len(mixed_blocks),
            "mixed_block_size": len(mixed_blocks[0]),
        },
        "mixed_cover": {
            "visible_block_action_size": len(visible_action_counts),
            "lifted_action_size": len(mixed_action_pairs),
            "lifts_per_visible_element": sorted(set(visible_action_counts.values())),
            "deck_involution": _cover_action_record(_COVER_ACTION_DECK),
        },
        "checks": checks,
        "theorem": theorem,
    }


def compute_quadrangle_cover_nonsplitting_obstruction() -> dict[str, Any]:
    """Show the mixed 2-cover does not split over the visible D4 square.

    The 16-element symmetry group on the mixed 8-state orbit is a central
    extension of the visible D4 square symmetry by the deck involution. This
    extension is non-split: there is no subgroup of order 8 complementary to the
    deck involution, so there is no D4-equivariant global choice of sheet.
    """
    action_group = sorted(_quadrangle_mixed_cover_action_data()["action_group"])
    complement_exists = False
    for subset in combinations([action for action in action_group if action != _COVER_ACTION_DECK], 7):
        candidate = {_COVER_ACTION_IDENTITY, *subset}
        if _COVER_ACTION_DECK in candidate:
            continue
        if all(_compose_cover_action(left, right) in candidate for left in candidate for right in candidate):
            complement_exists = True
            break

    checks = {
        "mixed_cover_action_has_order_16": len(action_group) == 16,
        "deck_involution_is_present": _COVER_ACTION_DECK in action_group,
        "deck_involution_is_central": all(
            _compose_cover_action(_COVER_ACTION_DECK, action) == _compose_cover_action(action, _COVER_ACTION_DECK)
            for action in action_group
        ),
        "visible_quotient_has_order_8": len({action[0] for action in action_group}) == 8,
        "no_order_8_complement_to_the_deck_involution_exists": not complement_exists,
    }

    theorem = {
        "the_mixed_cover_is_a_non_split_central_extension_of_visible_d4_by_the_deck_c2": (
            checks["mixed_cover_action_has_order_16"]
            and checks["deck_involution_is_present"]
            and checks["deck_involution_is_central"]
            and checks["visible_quotient_has_order_8"]
            and checks["no_order_8_complement_to_the_deck_involution_exists"]
        ),
        "interpretation": (
            "There is no D4-equivariant global choice of sheet on the mixed 2-cover. "
            "The hidden deck involution is central but non-split, so the first global "
            "carrier already contains an irreducible twofold ambiguity."
        ),
    }

    return {
        "extension": {
            "action_order": len(action_group),
            "visible_quotient_order": len({action[0] for action in action_group}),
            "deck_involution": _cover_action_record(_COVER_ACTION_DECK),
            "complement_exists": complement_exists,
        },
        "checks": checks,
        "theorem": theorem,
    }


def compute_quadrangle_cover_group_structure() -> dict[str, Any]:
    """Resolve the exact 16-element group acting on the mixed quadrangle cover.

    The mixed cover action is stronger than a bare non-splitting statement. Its
    center is a Klein four group generated by the deck involution and a second
    central half-turn lift. The commutator subgroup has order 2, and there are
    order-4 lifts of a visible reflection and quarter-turn satisfying an exact
    conjugation relation twisted by the deck involution.
    """
    action_group = sorted(_quadrangle_mixed_cover_action_data()["action_group"])

    center = sorted(
        action for action in action_group if all(_compose_cover_action(action, other) == _compose_cover_action(other, action) for other in action_group)
    )

    def commutator(
        left: tuple[tuple[int, int, int, int], tuple[int, int, int, int]],
        right: tuple[tuple[int, int, int, int], tuple[int, int, int, int]],
    ) -> tuple[tuple[int, int, int, int], tuple[int, int, int, int]]:
        return _compose_cover_action(
            _compose_cover_action(
                _compose_cover_action(
                    _inverse_cover_action(left, action_group),
                    _inverse_cover_action(right, action_group),
                ),
                left,
            ),
            right,
        )

    derived = {commutator(left, right) for left in action_group for right in action_group}
    changed = True
    while changed:
        changed = False
        for left in tuple(derived):
            for right in tuple(derived):
                product = _compose_cover_action(left, right)
                if product not in derived:
                    derived.add(product)
                    changed = True

    order_distribution = Counter(_cover_action_order(action, action_group) for action in action_group)
    square_set = sorted({_compose_cover_action(action, action) for action in action_group})
    square_half_turn_lift = next(
        square
        for square in square_set
        if square not in {_COVER_ACTION_IDENTITY, _COVER_ACTION_DECK}
    )
    commutator_half_turn_lift = next(
        action
        for action in center
        if action not in {_COVER_ACTION_IDENTITY, _COVER_ACTION_DECK, square_half_turn_lift}
    )

    presentation = None
    order_4_actions = [action for action in action_group if _cover_action_order(action, action_group) == 4]
    for reflection_lift in order_4_actions:
        if _compose_cover_action(reflection_lift, reflection_lift) != _COVER_ACTION_DECK:
            continue
        reflection_inverse = _inverse_cover_action(reflection_lift, action_group)
        for rotation_lift in order_4_actions:
            if _compose_cover_action(rotation_lift, rotation_lift) != square_half_turn_lift:
                continue
            rotation_inverse = _inverse_cover_action(rotation_lift, action_group)
            generated = {_COVER_ACTION_IDENTITY}
            frontier = {reflection_lift, reflection_inverse, rotation_lift, rotation_inverse}
            while frontier:
                current = frontier.pop()
                if current in generated:
                    continue
                generated.add(current)
                for known in tuple(generated):
                    for product in (_compose_cover_action(current, known), _compose_cover_action(known, current)):
                        if product not in generated:
                            frontier.add(product)
            conjugate = _compose_cover_action(
                _compose_cover_action(reflection_lift, rotation_lift),
                reflection_inverse,
            )
            if len(generated) == 16 and conjugate == _compose_cover_action(rotation_inverse, _COVER_ACTION_DECK):
                presentation = {
                    "reflection_lift": _cover_action_record(reflection_lift),
                    "rotation_lift": _cover_action_record(rotation_lift),
                    "reflection_square": _cover_action_record(_COVER_ACTION_DECK),
                    "rotation_square": _cover_action_record(square_half_turn_lift),
                    "conjugate_of_rotation_by_reflection": _cover_action_record(conjugate),
                }
                break
        if presentation is not None:
            break

    checks = {
        "mixed_cover_group_has_order_16": len(action_group) == 16,
        "the_center_has_order_4": len(center) == 4,
        "the_center_is_klein_four": all(_cover_action_order(action, action_group) in {1, 2} for action in center),
        "the_commutator_subgroup_has_order_2": len(derived) == 2,
        "all_group_elements_have_order_dividing_4": max(order_distribution) == 4,
        "the_square_set_has_size_3": len(square_set) == 3,
        "the_deck_and_one_visible_half_turn_lift_are_exactly_the_nontrivial_squares": square_set == [
            _COVER_ACTION_IDENTITY,
            _COVER_ACTION_DECK,
            square_half_turn_lift,
        ],
        "the_other_central_half_turn_lift_is_not_a_square": commutator_half_turn_lift not in square_set,
        "there_is_a_reflection_rotation_presentation_twisted_by_the_deck": presentation is not None,
    }

    theorem = {
        "the_mixed_cover_group_has_center_v4_commutator_c2_and_a_deck_twisted_order_4_presentation": (
            checks["mixed_cover_group_has_order_16"]
            and checks["the_center_has_order_4"]
            and checks["the_center_is_klein_four"]
            and checks["the_commutator_subgroup_has_order_2"]
            and checks["all_group_elements_have_order_dividing_4"]
            and checks["the_square_set_has_size_3"]
            and checks["the_deck_and_one_visible_half_turn_lift_are_exactly_the_nontrivial_squares"]
            and checks["the_other_central_half_turn_lift_is_not_a_square"]
            and checks["there_is_a_reflection_rotation_presentation_twisted_by_the_deck"]
        ),
        "interpretation": (
            "The mixed-cover symmetry is not just non-split. It has center V4, with "
            "the deck involution and one distinguished central lift of the visible "
            "square half-turn, while the remaining central half-turn is the commutator "
            "and is not a square. A reflection lift squares to the deck, a quarter-turn "
            "lift squares to the distinguished half-turn, and conjugation twists by the deck."
        ),
    }

    return {
        "group": {
            "action_order": len(action_group),
            "center_order": len(center),
            "commutator_subgroup_order": len(derived),
            "order_distribution": dict(sorted(order_distribution.items())),
            "square_count": len(square_set),
        },
        "central_elements": {
            "deck_involution": _cover_action_record(_COVER_ACTION_DECK),
            "square_half_turn_lift": _cover_action_record(square_half_turn_lift),
            "commutator_half_turn_lift": _cover_action_record(commutator_half_turn_lift),
        },
        "presentation": presentation,
        "checks": checks,
        "theorem": theorem,
    }


def compute_quadrangle_adjacent_transport_heisenberg_packet() -> dict[str, Any]:
    """Resolve the 27 global quadrangles over an ordered adjacent line pair.

    Fix an ordered adjacent pair of isotropic lines in the 40-line graph. The
    1620 nonlocal quadrangles containing that ordered pair form a 27-point
    packet. Projecting each quadrangle to the two anchor-pair states on the two
    fixed lines yields the full 3x3 local transport block with fibre size 3. The
    order-3 part of the packet stabilizer is a regular nonabelian group of order
    27 whose center is exactly the 3-point fibre over each local state cell.
    """
    lines, _line_adjacency = _line_intersection_graph()
    cycle_summary = compute_cycle_holonomy_carrier()
    seed_cycle = tuple(
        next(record for record in cycle_summary["quadrangle_cycles"]["orbit_records"] if record["orbit_size"] == 1_620)["seed_cycle"]
    )
    left_line_id, right_line_id = seed_cycle[0], seed_cycle[1]

    shadow = build_h4_shadow()
    states = shadow["states"]
    line_state_by_partition: dict[tuple[int, tuple[tuple[int, int], tuple[int, int]]], int] = {}
    states_on_line: dict[int, list[int]] = {line_id: [] for line_id in range(len(lines))}
    for state in states:
        line_id = int(state["line_id"])
        partition = tuple(sorted(tuple(sorted(edge)) for edge in state["matching"]))
        line_state_by_partition[(line_id, partition)] = int(state["state_id"])
        states_on_line[line_id].append(int(state["state_id"]))
    left_state_ids = sorted(states_on_line[left_line_id])
    right_state_ids = sorted(states_on_line[right_line_id])

    def anchor_pair_on_cycle(cycle: tuple[int, int, int, int], index: int) -> tuple[int, int]:
        line_id = cycle[index]
        previous_line = cycle[(index - 1) % 4]
        next_line = cycle[(index + 1) % 4]
        previous_anchor = next(iter(set(lines[line_id]) & set(lines[previous_line])))
        next_anchor = next(iter(set(lines[line_id]) & set(lines[next_line])))
        return tuple(sorted((previous_anchor, next_anchor)))

    def state_for_anchor_pair(line_id: int, anchor_pair: tuple[int, int]) -> int:
        complementary_pair = tuple(sorted(set(lines[line_id]) - set(anchor_pair)))
        partition = tuple(sorted((tuple(sorted(anchor_pair)), complementary_pair)))
        return line_state_by_partition[(line_id, partition)]

    packet_cycles: list[tuple[int, int, int, int]] = []
    cell_of_cycle: dict[tuple[int, int, int, int], tuple[int, int]] = {}
    cell_counts: Counter[tuple[int, int]] = Counter()
    for cycle in _simple_line_graph_cycles(4):
        edge_anchors = [
            next(iter(set(lines[cycle[index]]) & set(lines[cycle[(index + 1) % 4]])))
            for index in range(4)
        ]
        if len(set(edge_anchors)) != 4:
            continue
        if set(lines[cycle[0]]) & set(lines[cycle[1]]) & set(lines[cycle[2]]) & set(lines[cycle[3]]):
            continue
        if any((set(lines[cycle[index]]) & set(lines[cycle[(index + 2) % 4]])) for index in range(2)):
            continue
        if left_line_id not in cycle or right_line_id not in cycle:
            continue

        left_index = cycle.index(left_line_id)
        if cycle[(left_index + 1) % 4] == right_line_id:
            right_index = (left_index + 1) % 4
        elif cycle[(left_index - 1) % 4] == right_line_id:
            right_index = (left_index - 1) % 4
        else:
            continue

        left_state = state_for_anchor_pair(left_line_id, anchor_pair_on_cycle(cycle, left_index))
        right_state = state_for_anchor_pair(right_line_id, anchor_pair_on_cycle(cycle, right_index))
        cell = (left_state_ids.index(left_state), right_state_ids.index(right_state))
        canonical_cycle = _canonical_cycle(cycle)
        packet_cycles.append(canonical_cycle)
        cell_of_cycle[canonical_cycle] = cell
        cell_counts[cell] += 1

    packet_cycles = sorted(set(packet_cycles))
    packet_index = {cycle: index for index, cycle in enumerate(packet_cycles)}

    packet_image: set[tuple[int, ...]] = set()
    for line_perm in _full_line_permutation_group():
        if line_perm[left_line_id] != left_line_id or line_perm[right_line_id] != right_line_id:
            continue
        packet_image.add(
            tuple(
                packet_index[_canonical_cycle(tuple(line_perm[line_id] for line_id in cycle))]
                for cycle in packet_cycles
            )
        )

    packet_identity = tuple(range(len(packet_cycles)))

    def compose_packet(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(left[index] for index in right)

    def inverse_packet(perm: tuple[int, ...]) -> tuple[int, ...]:
        inverse = [0] * len(perm)
        for source, target in enumerate(perm):
            inverse[target] = source
        return tuple(inverse)

    def packet_order(perm: tuple[int, ...]) -> int:
        current = packet_identity
        for exponent in range(1, 128):
            current = compose_packet(perm, current)
            if current == packet_identity:
                return exponent
        raise AssertionError("packet permutation order exceeded search bound")

    def packet_commutator(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
        return compose_packet(
            compose_packet(
                compose_packet(inverse_packet(left), inverse_packet(right)),
                left,
            ),
            right,
        )

    heisenberg_packet = {perm for perm in packet_image if packet_order(perm) in {1, 3}}
    packet_center = {
        perm for perm in heisenberg_packet if all(compose_packet(perm, other) == compose_packet(other, perm) for other in heisenberg_packet)
    }
    packet_derived = {packet_commutator(left, right) for left in heisenberg_packet for right in heisenberg_packet}
    changed = True
    while changed:
        changed = False
        for left in tuple(packet_derived):
            for right in tuple(packet_derived):
                product = compose_packet(left, right)
                if product not in packet_derived:
                    packet_derived.add(product)
                    changed = True

    cell_blocks_by_pair: dict[tuple[int, int], list[int]] = {}
    for cycle in packet_cycles:
        cell_blocks_by_pair.setdefault(cell_of_cycle[cycle], []).append(packet_index[cycle])
    cell_blocks = [tuple(sorted(block)) for _cell, block in sorted(cell_blocks_by_pair.items())]
    packet_fibre_group = {
        perm
        for perm in heisenberg_packet
        if all(tuple(sorted(perm[index] for index in block)) == block for block in cell_blocks)
    }

    cell_block_index = {block: index for index, block in enumerate(cell_blocks)}
    cell_identity = tuple(range(len(cell_blocks)))
    cell_quotient_image = {
        tuple(cell_block_index[tuple(sorted(perm[index] for index in block))] for block in cell_blocks)
        for perm in heisenberg_packet
    }

    def packet_to_cell_perm(perm: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(cell_block_index[tuple(sorted(perm[index] for index in block))] for block in cell_blocks)

    def compose_cell(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(left[index] for index in right)

    def inverse_cell(perm: tuple[int, ...]) -> tuple[int, ...]:
        inverse = [0] * len(perm)
        for source, target in enumerate(perm):
            inverse[target] = source
        return tuple(inverse)

    def cell_order(perm: tuple[int, ...]) -> int:
        current = cell_identity
        for exponent in range(1, 32):
            current = compose_cell(perm, current)
            if current == cell_identity:
                return exponent
        raise AssertionError("cell quotient permutation order exceeded search bound")

    full_cell_image = {packet_to_cell_perm(perm) for perm in packet_image}
    reflection_witness = None
    outside_involutions = sorted(perm for perm in packet_image - heisenberg_packet if packet_order(perm) == 2)
    for involution in outside_involutions:
        if not all(
            compose_packet(compose_packet(involution, perm), involution) in heisenberg_packet
            for perm in heisenberg_packet
        ):
            continue
        generated = set(heisenberg_packet)
        frontier = set(heisenberg_packet | {involution})
        while frontier:
            current = frontier.pop()
            if current not in generated:
                generated.add(current)
            for known in tuple(generated):
                for product in (compose_packet(current, known), compose_packet(known, current)):
                    if product not in generated:
                        frontier.add(product)
        cell_involution = packet_to_cell_perm(involution)
        if (
            len(generated) == len(packet_image)
            and {compose_packet(compose_packet(involution, perm), involution) for perm in packet_center} == packet_center
            and all(
                compose_cell(compose_cell(cell_involution, perm), cell_involution) == inverse_cell(perm)
                for perm in cell_quotient_image
            )
        ):
            reflection_witness = {
                "packet_order": packet_order(involution),
                "cell_action": list(cell_involution),
                "generated_group_order": len(generated),
            }
            break

    checks = {
        "ordered_adjacent_pair_supports_exactly_27_nonlocal_quadrangles": len(packet_cycles) == 27,
        "local_state_shadow_is_a_full_3x3_block_with_fibre_size_3": (
            len(cell_counts) == 9 and sorted(cell_counts.values()) == [3] * 9
        ),
        "ordered_adjacent_pair_stabilizer_image_has_order_54": len(packet_image) == 54,
        "order_1_and_order_3_packet_elements_form_a_subgroup_of_order_27": (
            len(heisenberg_packet) == 27
            and all(compose_packet(left, right) in heisenberg_packet for left in heisenberg_packet for right in heisenberg_packet)
        ),
        "packet_order_27_subgroup_is_nonabelian_of_exponent_3": (
            any(compose_packet(left, right) != compose_packet(right, left) for left in heisenberg_packet for right in heisenberg_packet)
            and all(packet_order(perm) == 3 for perm in heisenberg_packet if perm != packet_identity)
        ),
        "packet_center_and_commutator_both_have_order_3": len(packet_center) == 3 and len(packet_derived) == 3,
        "packet_center_is_exactly_the_cellwise_fibre_group": packet_center == packet_fibre_group,
        "packet_order_27_subgroup_acts_regularly_on_the_27_quadrangles": (
            len({perm[0] for perm in heisenberg_packet}) == 27
            and sum(1 for perm in heisenberg_packet if perm[0] == 0) == 1
        ),
        "central_quotient_is_a_regular_elementary_abelian_group_of_order_9": (
            len(cell_quotient_image) == 9
            and all(compose_cell(left, right) == compose_cell(right, left) for left in cell_quotient_image for right in cell_quotient_image)
            and all(cell_order(perm) in {1, 3} for perm in cell_quotient_image)
            and len({perm[0] for perm in cell_quotient_image}) == 9
        ),
        "the_full_packet_symmetry_acts_on_the_9_cell_shadow_through_a_group_of_order_18": len(full_cell_image) == 18,
        "a_reflection_involution_extends_the_heisenberg_packet_to_the_full_order_54_symmetry": reflection_witness is not None,
    }

    theorem = {
        "the_27_global_quadrangles_over_an_ordered_adjacent_line_pair_form_a_heisenberg_packet": (
            checks["ordered_adjacent_pair_supports_exactly_27_nonlocal_quadrangles"]
            and checks["local_state_shadow_is_a_full_3x3_block_with_fibre_size_3"]
            and checks["ordered_adjacent_pair_stabilizer_image_has_order_54"]
            and checks["order_1_and_order_3_packet_elements_form_a_subgroup_of_order_27"]
            and checks["packet_order_27_subgroup_is_nonabelian_of_exponent_3"]
            and checks["packet_center_and_commutator_both_have_order_3"]
            and checks["packet_center_is_exactly_the_cellwise_fibre_group"]
            and checks["packet_order_27_subgroup_acts_regularly_on_the_27_quadrangles"]
            and checks["central_quotient_is_a_regular_elementary_abelian_group_of_order_9"]
        ),
        "the_full_packet_symmetry_is_the_heisenberg_packet_extended_by_a_reflection_involution": (
            checks["ordered_adjacent_pair_stabilizer_image_has_order_54"]
            and checks["the_full_packet_symmetry_acts_on_the_9_cell_shadow_through_a_group_of_order_18"]
            and checks["a_reflection_involution_extends_the_heisenberg_packet_to_the_full_order_54_symmetry"]
        ),
        "interpretation": (
            "The 27 nonlocal quadrangles above an ordered adjacent line pair are not a "
            "featureless multiplicity. They form a canonical Heisenberg packet of order 27. "
            "The visible 3x3 local state block is the central quotient by the 3-point fibre, "
            "and the full 54-element packet symmetry is obtained by adjoining a reflection "
            "involution that inverts the 9-cell shadow. So the remaining selector problem is "
            "exactly a Heisenberg lift above the local S3 shadow."
        ),
    }

    return {
        "ordered_adjacent_pair": {
            "line_ids": [left_line_id, right_line_id],
            "packet_size": len(packet_cycles),
            "stabilizer_image_order": len(packet_image),
        },
        "local_shadow": {
            "left_line_state_count": len(left_state_ids),
            "right_line_state_count": len(right_state_ids),
            "cell_count": len(cell_counts),
            "cell_fibre_size": min(cell_counts.values()),
            "cell_counts": {
                f"{left_state},{right_state}": count for (left_state, right_state), count in sorted(cell_counts.items())
            },
        },
        "heisenberg_packet": {
            "group_order": len(heisenberg_packet),
            "center_order": len(packet_center),
            "commutator_order": len(packet_derived),
            "cell_fibre_group_order": len(packet_fibre_group),
            "central_quotient_order": len(cell_quotient_image),
            "nonidentity_element_order": 3,
        },
        "semidirect_extension": {
            "full_packet_symmetry_order": len(packet_image),
            "full_cell_shadow_symmetry_order": len(full_cell_image),
            "reflection_count": len(outside_involutions),
            "reflection_witness": reflection_witness,
        },
        "checks": checks,
        "theorem": theorem,
    }


def _quadrangle_adjacent_transport_packet_action_data() -> dict[str, Any]:
    lines, _line_adjacency = _line_intersection_graph()
    cycle_summary = compute_cycle_holonomy_carrier()
    seed_cycle = tuple(
        next(record for record in cycle_summary["quadrangle_cycles"]["orbit_records"] if record["orbit_size"] == 1_620)["seed_cycle"]
    )
    left_line_id, right_line_id = seed_cycle[0], seed_cycle[1]

    shadow = build_h4_shadow()
    states = shadow["states"]
    line_state_by_partition: dict[tuple[int, tuple[tuple[int, int], tuple[int, int]]], int] = {}
    states_on_line: dict[int, list[int]] = {line_id: [] for line_id in range(len(lines))}
    for state in states:
        line_id = int(state["line_id"])
        partition = tuple(sorted(tuple(sorted(edge)) for edge in state["matching"]))
        line_state_by_partition[(line_id, partition)] = int(state["state_id"])
        states_on_line[line_id].append(int(state["state_id"]))
    left_state_ids = sorted(states_on_line[left_line_id])
    right_state_ids = sorted(states_on_line[right_line_id])

    def anchor_pair_on_cycle(cycle: tuple[int, int, int, int], index: int) -> tuple[int, int]:
        line_id = cycle[index]
        previous_line = cycle[(index - 1) % 4]
        next_line = cycle[(index + 1) % 4]
        previous_anchor = next(iter(set(lines[line_id]) & set(lines[previous_line])))
        next_anchor = next(iter(set(lines[line_id]) & set(lines[next_line])))
        return tuple(sorted((previous_anchor, next_anchor)))

    def state_for_anchor_pair(line_id: int, anchor_pair: tuple[int, int]) -> int:
        complementary_pair = tuple(sorted(set(lines[line_id]) - set(anchor_pair)))
        partition = tuple(sorted((tuple(sorted(anchor_pair)), complementary_pair)))
        return line_state_by_partition[(line_id, partition)]

    packet_cycles: list[tuple[int, int, int, int]] = []
    cell_of_cycle: dict[tuple[int, int, int, int], tuple[int, int]] = {}
    for cycle in _simple_line_graph_cycles(4):
        edge_anchors = [
            next(iter(set(lines[cycle[index]]) & set(lines[cycle[(index + 1) % 4]])))
            for index in range(4)
        ]
        if len(set(edge_anchors)) != 4:
            continue
        if set(lines[cycle[0]]) & set(lines[cycle[1]]) & set(lines[cycle[2]]) & set(lines[cycle[3]]):
            continue
        if any((set(lines[cycle[index]]) & set(lines[cycle[(index + 2) % 4]])) for index in range(2)):
            continue
        if left_line_id not in cycle or right_line_id not in cycle:
            continue

        left_index = cycle.index(left_line_id)
        if cycle[(left_index + 1) % 4] == right_line_id:
            right_index = (left_index + 1) % 4
        elif cycle[(left_index - 1) % 4] == right_line_id:
            right_index = (left_index - 1) % 4
        else:
            continue

        left_state = state_for_anchor_pair(left_line_id, anchor_pair_on_cycle(cycle, left_index))
        right_state = state_for_anchor_pair(right_line_id, anchor_pair_on_cycle(cycle, right_index))
        cell = (left_state_ids.index(left_state), right_state_ids.index(right_state))
        canonical_cycle = _canonical_cycle(cycle)
        packet_cycles.append(canonical_cycle)
        cell_of_cycle[canonical_cycle] = cell

    packet_cycles = sorted(set(packet_cycles))
    packet_index = {cycle: index for index, cycle in enumerate(packet_cycles)}
    packet_identity = tuple(range(len(packet_cycles)))

    packet_image: set[tuple[int, ...]] = set()
    for line_perm in _full_line_permutation_group():
        if line_perm[left_line_id] != left_line_id or line_perm[right_line_id] != right_line_id:
            continue
        packet_image.add(
            tuple(
                packet_index[_canonical_cycle(tuple(line_perm[line_id] for line_id in cycle))]
                for cycle in packet_cycles
            )
        )

    def compose_packet(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(left[index] for index in right)

    def inverse_packet(perm: tuple[int, ...]) -> tuple[int, ...]:
        inverse = [0] * len(perm)
        for source, target in enumerate(perm):
            inverse[target] = source
        return tuple(inverse)

    def packet_order(perm: tuple[int, ...]) -> int:
        current = packet_identity
        for exponent in range(1, 128):
            current = compose_packet(perm, current)
            if current == packet_identity:
                return exponent
        raise AssertionError("packet permutation order exceeded search bound")

    def packet_commutator(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
        return compose_packet(
            compose_packet(
                compose_packet(inverse_packet(left), inverse_packet(right)),
                left,
            ),
            right,
        )

    heisenberg_packet = {perm for perm in packet_image if packet_order(perm) in {1, 3}}
    packet_center = {
        perm
        for perm in heisenberg_packet
        if all(compose_packet(perm, other) == compose_packet(other, perm) for other in heisenberg_packet)
    }
    packet_derived = {packet_commutator(left, right) for left in heisenberg_packet for right in heisenberg_packet}
    changed = True
    while changed:
        changed = False
        for left in tuple(packet_derived):
            for right in tuple(packet_derived):
                product = compose_packet(left, right)
                if product not in packet_derived:
                    packet_derived.add(product)
                    changed = True

    cell_blocks_by_pair: dict[tuple[int, int], list[int]] = {}
    for cycle in packet_cycles:
        cell_blocks_by_pair.setdefault(cell_of_cycle[cycle], []).append(packet_index[cycle])
    cell_blocks = [tuple(sorted(block)) for _cell, block in sorted(cell_blocks_by_pair.items())]
    cell_block_index = {block: index for index, block in enumerate(cell_blocks)}
    full_cell_image = {
        tuple(cell_block_index[tuple(sorted(perm[index] for index in block))] for block in cell_blocks)
        for perm in packet_image
    }

    return {
        "ordered_adjacent_pair": [left_line_id, right_line_id],
        "packet_cycles": packet_cycles,
        "packet_identity": packet_identity,
        "packet_image": packet_image,
        "heisenberg_packet": heisenberg_packet,
        "packet_center": packet_center,
        "packet_derived": packet_derived,
        "full_cell_image": full_cell_image,
    }


def compute_quadrangle_adjacent_transport_section_obstruction() -> dict[str, Any]:
    """Show the visible 9-cell transport shadow has no equivariant local section.

    Over an ordered adjacent line pair, the 27-point Heisenberg packet projects to
    a visible 9-cell local transport shadow with central fibre of size 3. This
    central extension is non-split twice over: there is no order-9 subgroup of the
    Heisenberg packet complementary to the centre, and even after adjoining the
    reflection involution to form the full order-54 packet symmetry there is no
    order-18 complement to the same central fibre. So no packet-equivariant local
    selector can exist at the ordered-pair level.
    """
    data = _quadrangle_adjacent_transport_packet_action_data()
    full_group = sorted(data["packet_image"])
    heisenberg_packet = sorted(data["heisenberg_packet"])
    packet_center = set(data["packet_center"])
    packet_identity = data["packet_identity"]
    full_cell_image = data["full_cell_image"]

    def compose_packet(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(left[index] for index in right)

    def inverse_packet(perm: tuple[int, ...]) -> tuple[int, ...]:
        inverse = [0] * len(perm)
        for source, target in enumerate(perm):
            inverse[target] = source
        return tuple(inverse)

    def packet_order(perm: tuple[int, ...]) -> int:
        current = packet_identity
        for exponent in range(1, 128):
            current = compose_packet(perm, current)
            if current == packet_identity:
                return exponent
        raise AssertionError("packet permutation order exceeded search bound")

    def closure(generators: set[tuple[int, ...]]) -> set[tuple[int, ...]]:
        subgroup = {packet_identity}
        frontier = set(generators)
        while frontier:
            current = frontier.pop()
            if current in subgroup:
                continue
            subgroup.add(current)
            for known in tuple(subgroup):
                for product in (
                    compose_packet(current, known),
                    compose_packet(known, current),
                    inverse_packet(current),
                ):
                    if product not in subgroup:
                        frontier.add(product)
        return subgroup

    heisenberg_complement_exists = False
    heisenberg_noncentral = [perm for perm in heisenberg_packet if perm not in packet_center]
    for left_generator, right_generator in combinations(heisenberg_noncentral, 2):
        candidate = closure({left_generator, right_generator})
        if len(candidate) == 9 and candidate.isdisjoint(packet_center - {packet_identity}):
            heisenberg_complement_exists = True
            break

    full_complement_exists = False
    order_2_generators = [perm for perm in full_group if perm not in packet_center and packet_order(perm) == 2]
    order_3_generators = [perm for perm in full_group if perm not in packet_center and packet_order(perm) == 3]
    for involution in order_2_generators:
        for left_generator, right_generator in combinations(order_3_generators, 2):
            candidate = closure({involution, left_generator, right_generator})
            if len(candidate) == 18 and candidate.isdisjoint(packet_center - {packet_identity}):
                full_complement_exists = True
                break
        if full_complement_exists:
            break

    checks = {
        "heisenberg_packet_has_order_27": len(heisenberg_packet) == 27,
        "central_fibre_has_order_3": len(packet_center) == 3,
        "visible_local_shadow_has_order_9": len(heisenberg_packet) // len(packet_center) == 9,
        "full_ordered_pair_symmetry_has_order_54": len(full_group) == 54,
        "full_local_shadow_symmetry_has_order_18": len(full_cell_image) == 18,
        "no_order_9_complement_to_the_central_fibre_exists_in_the_heisenberg_packet": not heisenberg_complement_exists,
        "no_order_18_complement_to_the_central_fibre_exists_in_the_full_packet_symmetry": not full_complement_exists,
    }

    theorem = {
        "the_visible_9_cell_adjacent_transport_shadow_has_no_packet_equivariant_section": (
            checks["heisenberg_packet_has_order_27"]
            and checks["central_fibre_has_order_3"]
            and checks["visible_local_shadow_has_order_9"]
            and checks["full_ordered_pair_symmetry_has_order_54"]
            and checks["full_local_shadow_symmetry_has_order_18"]
            and checks["no_order_9_complement_to_the_central_fibre_exists_in_the_heisenberg_packet"]
            and checks["no_order_18_complement_to_the_central_fibre_exists_in_the_full_packet_symmetry"]
        ),
        "interpretation": (
            "Even at a fixed ordered adjacent transport slot, the visible 9-cell local state block "
            "admits no packet-equivariant lift into the 27-point Heisenberg packet. Any selector must "
            "therefore either break the local packet symmetry or appear as genuinely nonlocal holonomy."
        ),
    }

    return {
        "obstruction": {
            "heisenberg_packet_order": len(heisenberg_packet),
            "central_fibre_order": len(packet_center),
            "visible_local_shadow_order": len(heisenberg_packet) // len(packet_center),
            "full_packet_symmetry_order": len(full_group),
            "full_local_shadow_symmetry_order": len(full_cell_image),
            "heisenberg_complement_exists": heisenberg_complement_exists,
            "full_symmetry_complement_exists": full_complement_exists,
        },
        "checks": checks,
        "theorem": theorem,
    }


def compute_quadrangle_ordered_path_s3_carrier() -> dict[str, Any]:
    """Show ordered nonlocal 2-paths carry the first exact S3 completion law.

    An ordered nonlocal 2-path is an ordered triple of line-graph vertices
    (A,B,C) with A adjacent to B, B adjacent to C, A disjoint from C, and the
    two edge anchors distinct. Every such path extends to exactly three nonlocal
    quadrangles. For a seed path, the path stabilizer has order 6 and acts as the
    full symmetric group S3 on the three completions. This is the first exact S3
    carrier in the H4 transport problem.
    """
    lines, line_adjacency = _line_intersection_graph()
    cycle_summary = compute_cycle_holonomy_carrier()
    seed_quadrangle = tuple(
        next(record for record in cycle_summary["quadrangle_cycles"]["orbit_records"] if record["orbit_size"] == 1_620)["seed_cycle"]
    )
    seed_path = tuple(seed_quadrangle[:3])
    line_group = _full_line_permutation_group()

    ordered_nonlocal_paths: list[tuple[int, int, int]] = []
    for middle in range(len(lines)):
        for left in sorted(line_adjacency[middle]):
            for right in sorted(line_adjacency[middle]):
                if left == right:
                    continue
                if set(lines[left]) & set(lines[right]):
                    continue
                left_anchor = next(iter(set(lines[left]) & set(lines[middle])))
                right_anchor = next(iter(set(lines[middle]) & set(lines[right])))
                if left_anchor == right_anchor:
                    continue
                ordered_nonlocal_paths.append((left, middle, right))
    ordered_nonlocal_paths = sorted(set(ordered_nonlocal_paths))

    seed_path_orbit = {tuple(line_perm[line_id] for line_id in seed_path) for line_perm in line_group}
    seed_path_stabilizer = [line_perm for line_perm in line_group if tuple(line_perm[line_id] for line_id in seed_path) == seed_path]

    path_to_completions: dict[tuple[int, int, int], set[tuple[int, int, int, int]]] = {
        path: set() for path in ordered_nonlocal_paths
    }
    for cycle in _simple_line_graph_cycles(4):
        edge_anchors = [
            next(iter(set(lines[cycle[index]]) & set(lines[cycle[(index + 1) % 4]])))
            for index in range(4)
        ]
        if len(set(edge_anchors)) != 4:
            continue
        if set(lines[cycle[0]]) & set(lines[cycle[1]]) & set(lines[cycle[2]]) & set(lines[cycle[3]]):
            continue
        if any((set(lines[cycle[index]]) & set(lines[cycle[(index + 2) % 4]])) for index in range(2)):
            continue
        canonical_cycle = _canonical_cycle(cycle)
        for index in range(4):
            path_to_completions[(canonical_cycle[index], canonical_cycle[(index + 1) % 4], canonical_cycle[(index + 2) % 4])].add(canonical_cycle)
            path_to_completions[(canonical_cycle[index], canonical_cycle[(index - 1) % 4], canonical_cycle[(index - 2) % 4])].add(canonical_cycle)

    completion_count_distribution = Counter(len(completions) for completions in path_to_completions.values())
    seed_completions = sorted(path_to_completions[seed_path])
    completion_index = {cycle: index for index, cycle in enumerate(seed_completions)}
    seed_completion_action = {
        tuple(completion_index[_canonical_cycle(tuple(line_perm[line_id] for line_id in cycle))] for cycle in seed_completions)
        for line_perm in seed_path_stabilizer
    }

    all_s3_permutations = {
        (0, 1, 2),
        (0, 2, 1),
        (1, 0, 2),
        (1, 2, 0),
        (2, 0, 1),
        (2, 1, 0),
    }

    checks = {
        "ordered_nonlocal_2_paths_form_one_psp43_orbit_of_size_4320": len(seed_path_orbit) == len(ordered_nonlocal_paths) == 4_320,
        "seed_path_stabilizer_has_order_6": len(seed_path_stabilizer) == 6,
        "orbit_stabilizer_identity_holds_for_ordered_nonlocal_2_paths": len(line_group) == len(seed_path_orbit) * len(seed_path_stabilizer),
        "every_ordered_nonlocal_2_path_has_exactly_three_nonlocal_quadrangle_completions": completion_count_distribution == {3: 4_320},
        "seed_path_completion_action_is_exactly_s3": seed_completion_action == all_s3_permutations,
    }

    theorem = {
        "ordered_nonlocal_2_paths_are_the_first_exact_s3_completion_carrier": (
            checks["ordered_nonlocal_2_paths_form_one_psp43_orbit_of_size_4320"]
            and checks["seed_path_stabilizer_has_order_6"]
            and checks["orbit_stabilizer_identity_holds_for_ordered_nonlocal_2_paths"]
            and checks["every_ordered_nonlocal_2_path_has_exactly_three_nonlocal_quadrangle_completions"]
            and checks["seed_path_completion_action_is_exactly_s3"]
        ),
        "interpretation": (
            "The first exact S3 object in the H4 transport problem is an ordered nonlocal 2-path. "
            "Such a path admits exactly three nonlocal quadrangle completions, and local symmetry acts "
            "as the full symmetric group on those three completions. The remaining selector problem is "
            "to choose these S3 fibres compatibly over larger holonomy carriers."
        ),
    }

    return {
        "ordered_path_action": {
            "path_count": len(ordered_nonlocal_paths),
            "seed_orbit_size": len(seed_path_orbit),
            "seed_stabilizer_size": len(seed_path_stabilizer),
            "completion_fibre_size": len(seed_completions),
        },
        "seed_path": {
            "line_ids": list(seed_path),
            "completion_quadrangles": [list(cycle) for cycle in seed_completions],
            "completion_action_size": len(seed_completion_action),
        },
        "checks": checks,
        "theorem": theorem,
    }


def compute_ordered_path_completion_section_obstruction() -> dict[str, Any]:
    """Show the S3 completion bundle has no PSp(4,3)-equivariant section.

    For a transitive group action on base paths, an equivariant section of the
    completion bundle exists only if the stabilizer of one base path fixes at
    least one completion.  The previous computation shows that the seed path
    stabilizer is the full S3 on its three completions; the common fixed set is
    empty.  Thus even the first exact S3 carrier does not provide a canonical
    branch choice.  The golden/icosahedral selector must break this S3 symmetry.
    """
    lines, line_adjacency = _line_intersection_graph()
    cycle_summary = compute_cycle_holonomy_carrier()
    seed_quadrangle = tuple(
        next(record for record in cycle_summary["quadrangle_cycles"]["orbit_records"] if record["orbit_size"] == 1_620)["seed_cycle"]
    )
    seed_path = tuple(seed_quadrangle[:3])
    line_group = _full_line_permutation_group()

    ordered_nonlocal_paths: list[tuple[int, int, int]] = []
    for middle in range(len(lines)):
        for left in sorted(line_adjacency[middle]):
            for right in sorted(line_adjacency[middle]):
                if left == right:
                    continue
                if set(lines[left]) & set(lines[right]):
                    continue
                left_anchor = next(iter(set(lines[left]) & set(lines[middle])))
                right_anchor = next(iter(set(lines[middle]) & set(lines[right])))
                if left_anchor != right_anchor:
                    ordered_nonlocal_paths.append((left, middle, right))
    ordered_nonlocal_paths = sorted(set(ordered_nonlocal_paths))

    path_to_completions: dict[tuple[int, int, int], set[tuple[int, int, int, int]]] = {
        path: set() for path in ordered_nonlocal_paths
    }
    nonlocal_quadrangles: set[tuple[int, int, int, int]] = set()
    for cycle in _simple_line_graph_cycles(4):
        edge_anchors = [
            next(iter(set(lines[cycle[index]]) & set(lines[cycle[(index + 1) % 4]])))
            for index in range(4)
        ]
        if len(set(edge_anchors)) != 4:
            continue
        if set(lines[cycle[0]]) & set(lines[cycle[1]]) & set(lines[cycle[2]]) & set(lines[cycle[3]]):
            continue
        if any((set(lines[cycle[index]]) & set(lines[cycle[(index + 2) % 4]])) for index in range(2)):
            continue
        canonical_cycle = _canonical_cycle(cycle)
        nonlocal_quadrangles.add(canonical_cycle)
        for index in range(4):
            path_to_completions[(canonical_cycle[index], canonical_cycle[(index + 1) % 4], canonical_cycle[(index + 2) % 4])].add(canonical_cycle)
            path_to_completions[(canonical_cycle[index], canonical_cycle[(index - 1) % 4], canonical_cycle[(index - 2) % 4])].add(canonical_cycle)

    seed_path_stabilizer = [line_perm for line_perm in line_group if tuple(line_perm[line_id] for line_id in seed_path) == seed_path]
    seed_completions = sorted(path_to_completions[seed_path])
    completion_index = {cycle: index for index, cycle in enumerate(seed_completions)}
    seed_completion_action = sorted(
        {
            tuple(completion_index[_canonical_cycle(tuple(line_perm[line_id] for line_id in cycle))] for cycle in seed_completions)
            for line_perm in seed_path_stabilizer
        }
    )
    fixed_by_all = [
        completion_id
        for completion_id in range(len(seed_completions))
        if all(action[completion_id] == completion_id for action in seed_completion_action)
    ]
    fixed_count_distribution = Counter(
        sum(1 for index, image in enumerate(action) if image == index)
        for action in seed_completion_action
    )
    branch_stabilizers = {
        completion_id: [
            action
            for action in seed_completion_action
            if action[completion_id] == completion_id
        ]
        for completion_id in range(len(seed_completions))
    }
    branch_fixed_completion_sets = [
        [
            completion_id
            for completion_id in range(len(seed_completions))
            if all(action[completion_id] == completion_id for action in stabilizer)
        ]
        for stabilizer in branch_stabilizers.values()
    ]
    branch_stabilizer_common_core = set(seed_completion_action)
    for stabilizer in branch_stabilizers.values():
        branch_stabilizer_common_core &= set(stabilizer)
    completion_orbit_from_seed_branch = {
        action[0] for action in seed_completion_action
    }
    completion_incidence_count = sum(len(completions) for completions in path_to_completions.values())
    quadrangle_to_path_count = Counter()
    for completions in path_to_completions.values():
        for quadrangle in completions:
            quadrangle_to_path_count[quadrangle] += 1

    checks = {
        "ordered_path_completion_bundle_has_4320_base_points": len(ordered_nonlocal_paths) == 4_320,
        "completion_fibre_has_size_3": set(len(completions) for completions in path_to_completions.values()) == {3},
        "nonlocal_quadrangle_count_is_1620": len(nonlocal_quadrangles) == 1_620,
        "each_nonlocal_quadrangle_contains_eight_ordered_2_paths": set(quadrangle_to_path_count.values()) == {8},
        "incidence_count_matches_both_sides": completion_incidence_count == 4_320 * 3 == 1_620 * 8,
        "seed_stabilizer_completion_action_is_s3": (
            len(seed_completion_action) == 6
            and fixed_count_distribution == {0: 2, 1: 3, 3: 1}
        ),
        "no_completion_is_fixed_by_the_seed_path_stabilizer": fixed_by_all == [],
        "completion_action_is_transitive_on_three_branches": completion_orbit_from_seed_branch == {0, 1, 2},
        "choosing_one_branch_breaks_s3_to_c2": sorted(len(stabilizer) for stabilizer in branch_stabilizers.values()) == [2, 2, 2],
        "each_branch_stabilizer_fixes_exactly_its_branch": branch_fixed_completion_sets == [[0], [1], [2]],
        "three_branch_stabilizers_have_trivial_common_core": branch_stabilizer_common_core == {(0, 1, 2)},
        "branch_choice_has_index_three": len(seed_completion_action) == 3 * len(branch_stabilizers[0]),
    }

    theorem = {
        "the_ordered_path_completion_bundle_has_no_psp43_equivariant_section": (
            checks["ordered_path_completion_bundle_has_4320_base_points"]
            and checks["completion_fibre_has_size_3"]
            and checks["incidence_count_matches_both_sides"]
            and checks["seed_stabilizer_completion_action_is_s3"]
            and checks["no_completion_is_fixed_by_the_seed_path_stabilizer"]
        ),
        "a_completion_branch_choice_is_exactly_an_s3_to_c2_symmetry_break": (
            checks["completion_action_is_transitive_on_three_branches"]
            and checks["choosing_one_branch_breaks_s3_to_c2"]
            and checks["each_branch_stabilizer_fixes_exactly_its_branch"]
            and checks["three_branch_stabilizers_have_trivial_common_core"]
            and checks["branch_choice_has_index_three"]
        ),
        "interpretation": (
            "The first exact S3 completion carrier is a genuine obstruction, not a selector. "
            "A PSp(4,3)-equivariant branch choice would require one of the three completions "
            "to be fixed by the path stabilizer, but the stabilizer acts as full S3. The "
            "golden/icosahedral step must therefore break this completion symmetry. Choosing "
            "one branch is precisely an S3-to-C2 reduction with trivial common core across "
            "the three branches."
        ),
    }

    return {
        "completion_bundle": {
            "ordered_path_count": len(ordered_nonlocal_paths),
            "completion_fibre_size": len(seed_completions),
            "nonlocal_quadrangle_count": len(nonlocal_quadrangles),
            "quadrangle_ordered_path_count": sorted(set(quadrangle_to_path_count.values())),
            "path_completion_incidence_count": completion_incidence_count,
        },
        "seed_stabilizer_action": {
            "stabilizer_order": len(seed_path_stabilizer),
            "completion_action_order": len(seed_completion_action),
            "fixed_count_distribution": dict(sorted(fixed_count_distribution.items())),
            "common_fixed_completions": fixed_by_all,
        },
        "branch_symmetry_breaking": {
            "full_completion_symmetry_order": len(seed_completion_action),
            "completion_orbit_size": len(completion_orbit_from_seed_branch),
            "chosen_branch_stabilizer_orders": sorted(len(stabilizer) for stabilizer in branch_stabilizers.values()),
            "branch_fixed_completion_sets": branch_fixed_completion_sets,
            "symmetry_break_index": len(seed_completion_action) // len(branch_stabilizers[0]),
            "branch_stabilizer_common_core_order": len(branch_stabilizer_common_core),
        },
        "checks": checks,
        "theorem": theorem,
    }


def write_summary(path: Path = DEFAULT_OUTPUT) -> dict[str, Any]:
    summary = compute_pair_orbitals()
    summary["local_selector_reduction"] = compute_local_selector_reduction()
    summary["point_residue_transport_reduction"] = compute_point_residue_transport_reduction()
    summary["anchored_local_symmetry_obstruction"] = compute_anchored_local_symmetry_obstruction()
    summary["cycle_holonomy_carrier"] = compute_cycle_holonomy_carrier()
    summary["quadrangle_self_duality"] = compute_quadrangle_self_duality()
    summary["quadrangle_stabilizer_structure"] = compute_quadrangle_stabilizer_structure()
    summary["quadrangle_kernel_fibre_action"] = compute_quadrangle_kernel_fibre_action()
    summary["quadrangle_mixed_cover_structure"] = compute_quadrangle_mixed_cover_structure()
    summary["quadrangle_cover_nonsplitting_obstruction"] = compute_quadrangle_cover_nonsplitting_obstruction()
    summary["quadrangle_cover_group_structure"] = compute_quadrangle_cover_group_structure()
    summary["quadrangle_adjacent_transport_heisenberg_packet"] = compute_quadrangle_adjacent_transport_heisenberg_packet()
    summary["quadrangle_adjacent_transport_section_obstruction"] = compute_quadrangle_adjacent_transport_section_obstruction()
    summary["quadrangle_ordered_path_s3_carrier"] = compute_quadrangle_ordered_path_s3_carrier()
    summary["ordered_path_completion_section_obstruction"] = compute_ordered_path_completion_section_obstruction()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


if __name__ == "__main__":
    print(json.dumps(write_summary()["theorem"], indent=2))
