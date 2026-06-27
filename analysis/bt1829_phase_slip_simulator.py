#!/usr/bin/env python3
"""
BT1829 -- Phase-Slip Simulator.

BT1827 proved the cyclic-residue C is a winding sector label.  BT1828
incorporated it as a commuting Hamiltonian/syndrome term.  This simulator tests
the dynamics implied by that theorem.

Two dynamics are compared on ordered triples of 12-clock positions:

1. collision-free local noise:
      move one occupied point by one clock step, rejecting collisions.
   Result: winding is invariant for long random walks.

2. controlled phase slip:
      allow a single collision boundary crossing.
   Result: the minimal transition from winding 2 to winding 1 is a two-step path
      distinct -> double collision -> distinct.

The script is deterministic and writes a reproducible falsifier payload.
"""
from __future__ import annotations

import itertools
import json
import random
from collections import Counter
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1829_phase_slip_simulator.json"
N = 12


def cyclic_residue(loop: tuple[int, int, int]) -> int:
    return sum((loop[i] - loop[(i + 1) % 3]) % N for i in range(3))


def winding(loop: tuple[int, int, int]) -> int:
    return cyclic_residue(loop) // N


def collision_type(loop: tuple[int, int, int]) -> str:
    n = len(set(loop))
    if n == 1:
        return "diagonal_collision"
    if n == 2:
        return "double_collision"
    return "distinct"


def neighbors(loop: tuple[int, int, int], allow_collision: bool) -> list[tuple[int, int, int]]:
    out = []
    for i in range(3):
        for step in (-1, 1):
            new = list(loop)
            new[i] = (new[i] + step) % N
            new = tuple(new)
            if allow_collision or collision_type(new) == "distinct":
                out.append(new)
    return out


def collision_free_graph() -> nx.Graph:
    vertices = [
        loop
        for loop in itertools.product(range(N), repeat=3)
        if collision_type(loop) == "distinct"
    ]
    graph = nx.Graph()
    graph.add_nodes_from(vertices)
    for loop in vertices:
        for nb in neighbors(loop, allow_collision=False):
            graph.add_edge(loop, nb)
    return graph


def full_graph() -> nx.Graph:
    vertices = list(itertools.product(range(N), repeat=3))
    graph = nx.Graph()
    graph.add_nodes_from(vertices)
    for loop in vertices:
        for nb in neighbors(loop, allow_collision=True):
            graph.add_edge(loop, nb)
    return graph


def random_walk(start: tuple[int, int, int], steps: int, seed: int) -> dict:
    rng = random.Random(seed)
    x = start
    seen = Counter()
    winding_trace = []
    rejected = 0
    for _ in range(steps):
        i = rng.randrange(3)
        step = rng.choice([-1, 1])
        y = list(x)
        y[i] = (y[i] + step) % N
        y = tuple(y)
        if collision_type(y) == "distinct":
            x = y
        else:
            rejected += 1
        seen[x] += 1
        winding_trace.append(winding(x))
    return {
        "start": list(start),
        "end": list(x),
        "steps": steps,
        "seed": seed,
        "rejected_collision_moves": rejected,
        "winding_start": winding(start),
        "winding_end": winding(x),
        "winding_values_seen": dict(sorted(Counter(winding_trace).items())),
        "states_visited": len(seen),
    }


def shortest_phase_slip(source: tuple[int, int, int], target_winding: int) -> list[tuple[int, int, int]]:
    graph = full_graph()
    targets = [
        v
        for v in graph.nodes
        if collision_type(v) == "distinct" and winding(v) == target_winding
    ]
    target = min(targets, key=lambda t: nx.shortest_path_length(graph, source, t))
    return nx.shortest_path(graph, source, target)


def main() -> int:
    cfg = collision_free_graph()
    full = full_graph()

    start_w2 = (0, 1, 2)
    start_w1 = (0, 11, 1)

    walk_w2 = random_walk(start_w2, steps=4096, seed=1829)
    walk_w1 = random_walk(start_w1, steps=4096, seed=1830)

    slip = shortest_phase_slip(start_w2, target_winding=1)
    slip_profile = [
        {
            "state": list(x),
            "type": collision_type(x),
            "residue": cyclic_residue(x),
            "winding": winding(x),
        }
        for x in slip
    ]

    # Exhaustive invariance/falsifier checks.
    collision_free_edges_preserve = all(winding(a) == winding(b) for a, b in cfg.edges)
    full_residue_changers = [
        (a, b)
        for a, b in full.edges
        if cyclic_residue(a) != cyclic_residue(b)
    ]
    all_changers_touch_collision = all(
        collision_type(a) != "distinct" or collision_type(b) != "distinct"
        for a, b in full_residue_changers
    )

    checks = {
        "collision_free_graph_nodes": cfg.number_of_nodes() == 1320,
        "collision_free_graph_edges": cfg.number_of_edges() == 3240,
        "collision_free_walk_w2_preserves_winding": walk_w2["winding_values_seen"] == {2: 4096},
        "collision_free_walk_w1_preserves_winding": walk_w1["winding_values_seen"] == {1: 4096},
        "collision_free_edges_preserve_winding": collision_free_edges_preserve,
        "full_graph_residue_changers_touch_collision": all_changers_touch_collision,
        "minimal_phase_slip_length_two": len(slip) - 1 == 2,
        "minimal_phase_slip_profile": [p["type"] for p in slip_profile]
        == ["distinct", "double_collision", "distinct"],
        "minimal_phase_slip_changes_winding": slip_profile[0]["winding"] == 2
        and slip_profile[-1]["winding"] == 1,
    }

    payload = {
        "bt": "BT1829",
        "title": "Phase-Slip Simulator",
        "verified": all(checks.values()),
        "summary": (
            "Collision-free local noise on the 12-clock preserves the BT1827 winding syndrome, "
            "while a controlled phase slip changes winding only by passing through a collision "
            "boundary.  The shortest explicit transition is (0,1,2)->(0,1,1)->(0,2,1), "
            "i.e. distinct -> double collision -> distinct, changing winding 2 to winding 1."
        ),
        "noise_model": "one coordinate moves by +/-1 on C12; collision-free simulator rejects collisions",
        "walks": {
            "winding_2_walk": walk_w2,
            "winding_1_walk": walk_w1,
        },
        "controlled_phase_slip": {
            "source": list(start_w2),
            "target_winding": 1,
            "path": slip_profile,
        },
        "exhaustive_counts": {
            "collision_free_nodes": cfg.number_of_nodes(),
            "collision_free_edges": cfg.number_of_edges(),
            "full_nodes": full.number_of_nodes(),
            "full_edges": full.number_of_edges(),
            "full_residue_changing_edges": len(full_residue_changers),
        },
        "interpretation": (
            "The winding syndrome is robust under ordinary collision-free perturbations. "
            "A hardware phase-slip gate is therefore exactly a controlled excursion through "
            "the collision manifold, not an uncontrolled local drift."
        ),
        "boundary": (
            "The simulator is a finite-state falsifier for the winding term C.  It does not "
            "include optical loss, detector dark counts, or continuous wavepacket deformation."
        ),
        "checks": checks,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True))
    print(json.dumps({"verified": payload["verified"], "slip": slip_profile, "walks": payload["walks"]}, indent=2))
    return 0 if payload["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
