#!/usr/bin/env python3
"""
BT1827 -- Cyclic Residue / Winding Protection Theorem.

This is the hardware/operator continuation of BT1824-BT1826.

BT1824 identified the fourth commuting finite operator

    C(x0,x1,x2)=sum_i (x_i - x_{i+1}) mod 12

on the local 12-symbol fibre.  This verifier proves that C is not just an
arithmetic tie-breaker: it is exactly 12 times the discrete winding number of
an ordered 3-point loop on the 12-clock.

The NetworkX test builds the collision-free ordered configuration graph of
three distinct clock points.  Edges move one point by one step on C12 while
avoiding collisions.  The graph has two connected components of size 660, and
C/12 is constant on each component.  Thus C is a topological sector label:
changing it requires a collision/phase-slip boundary.

This gives the missing physical interpretation of the BT1824 term C: it can be
implemented as a winding/phase-slip syndrome on a 12-bin optical clock/ring.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1827_cyclic_residue_winding_protection.json"
N = 12


def cyclic_residue(loop: tuple[int, int, int]) -> int:
    """BT1824 cyclic residue on an ordered 3-loop in Z/12."""
    return sum((loop[i] - loop[(i + 1) % 3]) % N for i in range(3))


def winding(loop: tuple[int, int, int]) -> int:
    """Discrete winding number.  The residue is always divisible by 12."""
    return cyclic_residue(loop) // N


def collision_type(loop: tuple[int, int, int]) -> str:
    n = len(set(loop))
    if n == 1:
        return "diagonal_collision"
    if n == 2:
        return "double_collision"
    return "distinct"


def build_collision_free_graph() -> nx.Graph:
    """Ordered 3-point configurations on C12, with collision-free one-step moves."""
    vertices = [
        loop
        for loop in itertools.product(range(N), repeat=3)
        if collision_type(loop) == "distinct"
    ]
    graph = nx.Graph()
    graph.add_nodes_from(vertices)

    for loop in vertices:
        for i in range(3):
            for step in (-1, 1):
                new_loop = list(loop)
                new_loop[i] = (new_loop[i] + step) % N
                new_loop = tuple(new_loop)
                if collision_type(new_loop) == "distinct":
                    graph.add_edge(loop, new_loop)
    return graph


def one_step_full_graph_jump_stats(all_loops: list[tuple[int, int, int]]):
    """Count residue-changing one-step moves on the full 12^3 cube."""
    jumps = []
    total_edges = 0
    for loop in all_loops:
        for i in range(3):
            for step in (-1, 1):
                new_loop = list(loop)
                new_loop[i] = (new_loop[i] + step) % N
                new_loop = tuple(new_loop)
                if loop < new_loop:  # undirected de-duplication
                    total_edges += 1
                    if cyclic_residue(loop) != cyclic_residue(new_loop):
                        jumps.append(
                            {
                                "from": list(loop),
                                "to": list(new_loop),
                                "from_residue": cyclic_residue(loop),
                                "to_residue": cyclic_residue(new_loop),
                                "from_type": collision_type(loop),
                                "to_type": collision_type(new_loop),
                            }
                        )
    return total_edges, jumps


def main() -> int:
    all_loops = list(itertools.product(range(N), repeat=3))
    cfg = build_collision_free_graph()
    comps = [set(c) for c in nx.connected_components(cfg)]

    component_profiles = []
    for idx, comp in enumerate(sorted(comps, key=lambda c: min(c))):
        component_profiles.append(
            {
                "component": idx,
                "size": len(comp),
                "winding_profile": dict(sorted(Counter(winding(x) for x in comp).items())),
                "residue_profile": dict(
                    sorted(Counter(cyclic_residue(x) for x in comp).items())
                ),
            }
        )

    total_edges, residue_jumps = one_step_full_graph_jump_stats(all_loops)
    all_jumps_touch_collision = all(
        j["from_type"] != "distinct" or j["to_type"] != "distinct" for j in residue_jumps
    )

    rotation_preserves = all(
        winding((x[1], x[2], x[0])) == winding(x)
        for x in cfg.nodes
    )
    reversal_swaps = Counter(
        (winding(x), winding((x[0], x[2], x[1]))) for x in cfg.nodes
    )

    checks = {
        "basis_size_12_cubed": len(all_loops) == 12**3 == 1728,
        "residue_always_multiple_of_12": all(cyclic_residue(x) % 12 == 0 for x in all_loops),
        "residue_values_are_0_12_24": set(cyclic_residue(x) for x in all_loops) == {0, 12, 24},
        "collision_free_nodes": cfg.number_of_nodes() == 1320,
        "collision_free_edges": cfg.number_of_edges() == 3240,
        "two_collision_free_components": len(comps) == 2,
        "components_are_660_660": sorted(len(c) for c in comps) == [660, 660],
        "each_component_has_constant_winding": all(
            len(set(winding(x) for x in comp)) == 1 for comp in comps
        ),
        "component_windings_are_1_and_2": sorted(
            next(iter(set(winding(x) for x in comp))) for comp in comps
        )
        == [1, 2],
        "collision_free_edges_preserve_residue": all(
            cyclic_residue(a) == cyclic_residue(b) for a, b in cfg.edges
        ),
        "full_one_step_residue_jumps_touch_collision": all_jumps_touch_collision,
        "cyclic_rotation_preserves_winding": rotation_preserves,
        "orientation_reversal_swaps_winding": dict(reversal_swaps)
        == {(1, 2): 660, (2, 1): 660},
    }

    payload = {
        "bt": "BT1827",
        "title": "Cyclic Residue / Winding Protection Theorem",
        "verified": all(checks.values()),
        "summary": (
            "The BT1824 cyclic-residue operator C is exactly 12 times a discrete "
            "winding number on the local 12-clock.  The collision-free ordered "
            "configuration graph of three clock points has two connected components "
            "of size 660, with winding 1 and winding 2.  Every collision-free local "
            "move preserves C; every one-step C-changing move in the full cube touches "
            "a collision/phase-slip state.  Thus C is a genuine topological syndrome, "
            "not an arbitrary cyclic tie-breaker."
        ),
        "operator": "C(x0,x1,x2)=sum_i (x_i-x_{i+1}) mod 12 = 12*winding",
        "counts": {
            "total_basis": len(all_loops),
            "collision_profile": dict(sorted(Counter(collision_type(x) for x in all_loops).items())),
            "residue_profile": dict(sorted(Counter(cyclic_residue(x) for x in all_loops).items())),
            "winding_profile": dict(sorted(Counter(winding(x) for x in all_loops).items())),
            "collision_free_graph_nodes": cfg.number_of_nodes(),
            "collision_free_graph_edges": cfg.number_of_edges(),
            "collision_free_component_sizes": sorted(len(c) for c in comps),
            "full_one_step_graph_edges": total_edges,
            "residue_changing_one_step_edges": len(residue_jumps),
        },
        "component_profiles": component_profiles,
        "orientation_symmetry": {
            "cyclic_rotation": "preserves winding",
            "orientation_reversal": "swaps winding 1 and winding 2",
            "reversal_profile": {f"{a}->{b}": n for (a, b), n in sorted(reversal_swaps.items())},
        },
        "phase_slip_boundary": {
            "all_residue_changing_one_step_edges_touch_collision": all_jumps_touch_collision,
            "example_jumps": residue_jumps[:8],
        },
        "physical_interpretation": (
            "C is the natural topological readout for a 12-bin photonic/OAM/time-bin ring. "
            "A collision-free perturbation cannot change the winding sector; a phase slip "
            "through a collision state is required.  This supplies the missing hardware "
            "interpretation of the BT1824 commuting term C in the finite law stack."
        ),
        "boundary": (
            "This proves the topological status of the cyclic-residue term.  It does not yet "
            "construct the full optical circuit for the remaining P,G,E terms; those remain "
            "as the next Hamiltonian/syndrome realization targets."
        ),
        "checks": checks,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True))
    print(json.dumps({"verified": payload["verified"], "counts": payload["counts"]}, indent=2))
    return 0 if payload["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
