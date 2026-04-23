#!/usr/bin/env python3
"""Exact Lie-bridge audit for the W33 qutrit kernel.

This module separates what follows directly from the exact qutrit kernel from
what later sections only match numerically or through additional spectral
closure assumptions.
"""

from __future__ import annotations

from functools import lru_cache
import json
from math import lcm
from pathlib import Path
import sys
import time
from typing import Dict, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.e8_embedding_group_theoretic import build_sp43_generators, build_w33
from scripts.e6_hessian_tritangents import analyze_hessian_tritangent_split
from scripts.w33_heisenberg_qutrit import build_f3_cube, compute_local_structure


def psp43_order() -> int:
    return (3**4) * (3**2 - 1) * (3**4 - 1) // 2


def sp43_order() -> int:
    return 2 * psp43_order()


def we6_order() -> int:
    return 51840


def _permutation_order(permutation: Tuple[int, ...]) -> int:
    visited = [False] * len(permutation)
    order = 1
    for start in range(len(permutation)):
        if visited[start]:
            continue
        cycle_length = 0
        current = start
        while not visited[current]:
            visited[current] = True
            current = permutation[current]
            cycle_length += 1
        if cycle_length:
            order = lcm(order, cycle_length)
    return order


def _enumerate_group_from_generators(
    generators: Tuple[Tuple[int, ...], ...], degree: int
) -> Tuple[Tuple[int, ...], ...]:
    identity = tuple(range(degree))
    seen = {identity}
    queue = [identity]
    while queue:
        current = queue.pop()
        for generator in generators:
            image = tuple(generator[index] for index in current)
            if image not in seen:
                seen.add(image)
                queue.append(image)
    return tuple(sorted(seen))


def _vertex_orbit_size(generators: Tuple[Tuple[int, ...], ...], start: int = 0) -> int:
    reached = {start}
    queue = [start]
    while queue:
        current = queue.pop(0)
        for generator in generators:
            image = generator[current]
            if image not in reached:
                reached.add(image)
                queue.append(image)
    return len(reached)


def _edge_orbit_size(
    generators: Tuple[Tuple[int, ...], ...], edges: Tuple[Tuple[int, int], ...]
) -> int:
    start = (min(edges[0]), max(edges[0]))
    reached = {start}
    queue = [start]
    while queue:
        left, right = queue.pop(0)
        for generator in generators:
            image = tuple(sorted((generator[left], generator[right])))
            if image not in reached:
                reached.add(image)
                queue.append(image)
    return len(reached)


@lru_cache(maxsize=1)
def local_e6_bridge_summary(base_vertex: int = 0) -> Dict[str, object]:
    n_vertices, _, adjacency, _ = build_w33()
    adjacency_sets = [set(row) for row in adjacency]
    neighbors, nonneighbors, triangles, _ = compute_local_structure(
        base_vertex, n_vertices, adjacency_sets
    )
    fibers, vertex_to_xyz = build_f3_cube(
        neighbors, nonneighbors, triangles, adjacency_sets
    )

    nonneighbor_set = set(nonneighbors)
    schlafli = {vertex: set() for vertex in nonneighbors}
    for index, left in enumerate(nonneighbors):
        for right in nonneighbors[index + 1 :]:
            common = len((adjacency_sets[left] & adjacency_sets[right]) & nonneighbor_set)
            if common == 3:
                schlafli[left].add(right)
                schlafli[right].add(left)

    lambda_values = set()
    mu_values = set()
    for index, left in enumerate(nonneighbors):
        for right in nonneighbors[index + 1 :]:
            common = len(schlafli[left] & schlafli[right])
            if right in schlafli[left]:
                lambda_values.add(common)
            else:
                mu_values.add(common)

    generation_sizes = [0, 0, 0]
    for vertex in nonneighbors:
        _, _, fiber_coordinate = vertex_to_xyz[vertex]
        generation_sizes[fiber_coordinate] += 1

    missing_center_cosets = 0
    for fiber in fibers.values():
        left, middle, right = fiber
        is_triangle = (
            middle in adjacency_sets[left]
            and right in adjacency_sets[left]
            and right in adjacency_sets[middle]
        )
        if not is_triangle:
            missing_center_cosets += 1

    return {
        "base_vertex": base_vertex,
        "neighbor_count": len(neighbors),
        "nonneighbor_count": len(nonneighbors),
        "mub_class_count": len(triangles),
        "mub_class_sizes": tuple(len(triangle) for triangle in triangles),
        "fiber_count": len(fibers),
        "fiber_size": len(next(iter(fibers.values()))),
        "generation_fiber_sizes": tuple(generation_sizes),
        "schlafli_parameters": (
            len(nonneighbors),
            len(next(iter(schlafli.values()))),
            next(iter(lambda_values)),
            next(iter(mu_values)),
        ),
        "tritangent_split": {
            "classical_total": 45,
            "internal_shell": 45 - missing_center_cosets,
            "missing_center_cosets": missing_center_cosets,
        },
        "classical_e6_interpretation": {
            "local_shell_graph": "Schlafli graph",
            "cubic_surface_lines": 27,
            "weyl_group": "W(E6)",
        },
    }


@lru_cache(maxsize=1)
def projective_symplectic_action_summary() -> Dict[str, object]:
    n_vertices, vertices, adjacency, edges = build_w33()
    generators = tuple(build_sp43_generators(vertices, adjacency))
    generator_orders = tuple(sorted({_permutation_order(generator) for generator in generators}))
    group = _enumerate_group_from_generators(generators, n_vertices)

    edge_orbit_size = _edge_orbit_size(generators, tuple(edges))
    point_orbit_size = _vertex_orbit_size(generators, start=0)
    point_stabilizer_order = sum(1 for element in group if element[0] == 0)

    return {
        "generator_count": len(generators),
        "generator_order_set": generator_orders,
        "enumerated_group_order": len(group),
        "point_stabilizer_order": point_stabilizer_order,
        "point_orbit_size": point_orbit_size,
        "edge_orbit_size": edge_orbit_size,
        "acts_transitively_on_points": point_orbit_size == n_vertices,
        "acts_transitively_on_edges": edge_orbit_size == len(edges),
        "classical_orders": {
            "psp43": psp43_order(),
            "sp43": sp43_order(),
            "we6": we6_order(),
        },
    }


@lru_cache(maxsize=1)
def local_h27_affine_symmetry_summary(base_vertex: int = 0) -> Dict[str, object]:
    import tools.analyze_balanced_orbit_stabilizer as full_w33

    projective_action = projective_symplectic_action_summary()
    hessian_split = analyze_hessian_tritangent_split()

    points, adjacency, _edges = full_w33.build_w33()
    full_generators = list(full_w33.get_generators(points))
    antisymplectic = full_w33.matrix_to_vertex_perm(
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 2, 0], [0, 0, 0, 2]], points
    )
    if antisymplectic is None:
        raise RuntimeError("failed to build antisymplectic generator")
    full_group = tuple(full_w33.enumerate_group(full_generators + [antisymplectic]))
    full_stabilizer = tuple(element for element in full_group if element[base_vertex] == base_vertex)

    mapping_payload = json.loads(
        (ROOT / "artifacts" / "schlafli_e6id_to_w33_h27.json").read_text(encoding="utf-8")
    )
    h27_vertices = tuple(mapping_payload["w33"]["H27_f3"])
    h27_position = {vertex: index for index, vertex in enumerate(h27_vertices)}

    full_restrictions = {
        tuple(h27_position[element[vertex]] for vertex in h27_vertices)
        for element in full_stabilizer
    }

    affine_group = hessian_split["affine_group"]
    hessian_group = hessian_split["hessian_group"]

    return {
        "full_graph_group_order": len(full_group),
        "full_graph_point_stabilizer_order": len(full_stabilizer),
        "full_graph_h27_restriction_order": len(full_restrictions),
        "full_graph_stabilizer_restricts_faithfully": len(full_stabilizer) == len(full_restrictions),
        "projective_group_order": projective_action["enumerated_group_order"],
        "projective_point_stabilizer_order": projective_action["point_stabilizer_order"],
        "projective_h27_restriction_order": hessian_group["order"],
        "projective_stabilizer_restricts_faithfully": (
            projective_action["point_stabilizer_order"] == hessian_group["order"]
        ),
        "local_affine_group_order": affine_group["order"],
        "local_affine_point_stabilizer_order": affine_group["point_stabilizer_order"],
        "local_projective_subgroup_order": hessian_group["order"],
        "local_projective_to_affine_index": affine_group["order"] // hessian_group["order"],
        "local_affine_transitive": affine_group["transitive"],
        "local_affine_triads_invariant": affine_group["triads_invariant"],
        "local_projective_triads_invariant": hessian_group["triads_invariant"],
        "matches_full_graph_local_order": len(full_restrictions) == affine_group["order"],
        "matches_projective_local_order": projective_action["point_stabilizer_order"] == hessian_group["order"],
    }


@lru_cache(maxsize=1)
def classify_lie_bridges() -> Tuple[Dict[str, object], ...]:
    local_bridge = local_e6_bridge_summary()
    projective_action = projective_symplectic_action_summary()
    local_affine = local_h27_affine_symmetry_summary()

    return (
        {
            "name": "local_schlafli_e6_bridge",
            "support_level": "repo-exact + classical exact",
            "depends_only_on_qutrit_kernel": True,
            "statement": (
                "The local 27-point shell is the Schlafli graph, so the cubic-surface "
                "27-line/W(E6) geometry sits on an exact local consequence of the qutrit kernel."
            ),
            "evidence": {
                "schlafli_parameters": local_bridge["schlafli_parameters"],
                "generation_fiber_sizes": local_bridge["generation_fiber_sizes"],
                "tritangent_split": local_bridge["tritangent_split"],
            },
        },
        {
            "name": "local_h27_affine_symmetry",
            "support_level": "repo-exact + classical exact",
            "depends_only_on_qutrit_kernel": True,
            "statement": (
                "The full W33 graph automorphism stabilizer of a point has order 1296 and restricts "
                "faithfully to the local H27 shell, where it realizes the full affine "
                "Heisenberg-GL(2,3) symmetry of the 45 tritangents; the symplectic-only piece is "
                "the 648-element Heisenberg⋊SL(2,3) index-2 subgroup."
            ),
            "evidence": local_affine,
        },
        {
            "name": "projective_symplectic_we6_symmetry",
            "support_level": "repo-exact + classical exact",
            "depends_only_on_qutrit_kernel": True,
            "statement": (
                "The repo's symplectic transvections act transitively on W33, enumerating the "
                "25920-element projective symplectic action; at a base point this yields the "
                "648-element Heisenberg⋊SL(2,3) local subgroup visible before adjoining the "
                "antisymplectic extension."
            ),
            "evidence": {
                "enumerated_group_order": projective_action["enumerated_group_order"],
                "point_stabilizer_order": projective_action["point_stabilizer_order"],
                "point_orbit_size": projective_action["point_orbit_size"],
                "edge_orbit_size": projective_action["edge_orbit_size"],
                "classical_orders": projective_action["classical_orders"],
            },
        },
        {
            "name": "edge_count_equals_e8_root_count",
            "support_level": "count identity only",
            "depends_only_on_qutrit_kernel": False,
            "statement": (
                "The identity |E(W33)| = 240 = |Phi(E8)| is exact as a count, but the qutrit "
                "kernel alone does not yet provide a canonical E8 root-system derivation."
            ),
            "evidence": {
                "w33_edge_count": 240,
                "e8_root_count": 240,
            },
        },
        {
            "name": "spectral_248_e8_dimension",
            "support_level": "later spectral layer",
            "depends_only_on_qutrit_kernel": False,
            "statement": (
                "The appearance of 248 belongs to the later spectral-determinant closure, not to "
                "the local qutrit kernel by itself."
            ),
            "evidence": {
                "e8_dimension": 248,
                "depends_on": "spectral determinant and Taylor-expansion layer",
            },
        },
    )


@lru_cache(maxsize=1)
def analyze() -> Dict[str, object]:
    bridge_records = classify_lie_bridges()
    exact_bridge_names = tuple(
        record["name"]
        for record in bridge_records
        if record["depends_only_on_qutrit_kernel"]
    )
    non_functorial_bridge_names = tuple(
        record["name"]
        for record in bridge_records
        if not record["depends_only_on_qutrit_kernel"]
    )

    return {
        "status": "ok",
        "local_e6_bridge": local_e6_bridge_summary(),
        "local_h27_affine_symmetry": local_h27_affine_symmetry_summary(),
        "projective_symplectic_action": projective_symplectic_action_summary(),
        "bridge_records": bridge_records,
        "exact_bridge_names": exact_bridge_names,
        "non_functorial_bridge_names": non_functorial_bridge_names,
    }


def main() -> None:
    started = time.time()
    payload = analyze()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CX_exact_lie_bridge_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("Exact Lie-bridge audit")
    print(f"  Exact local bridge: {payload['local_e6_bridge']['schlafli_parameters']}")
    print(
        "  Symplectic action orbits: "
        f"points={payload['projective_symplectic_action']['point_orbit_size']}, "
        f"edges={payload['projective_symplectic_action']['edge_orbit_size']}"
    )
    print(
        "  Local affine symmetry: "
        f"full={payload['local_h27_affine_symmetry']['local_affine_group_order']}, "
        f"projective={payload['local_h27_affine_symmetry']['local_projective_subgroup_order']}"
    )
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()