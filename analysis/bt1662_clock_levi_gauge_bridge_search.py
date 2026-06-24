#!/usr/bin/env python3
"""BT1662 — concrete gauge bridge from the 8-clock cycle basis to 8 of 81 Levi cycles."""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import networkx as nx

MOD = 3


def fano_lines() -> list[tuple[int, int, int]]:
    return [tuple(sorted((i % 7, (i + 1) % 7, (i + 3) % 7))) for i in range(7)]


def heawood_graph() -> nx.Graph:
    graph = nx.Graph()
    graph.add_nodes_from(range(14))
    for line_index, line in enumerate(fano_lines()):
        line_node = 7 + line_index
        for point in line:
            graph.add_edge(point, line_node)
    return graph


def canonical_projective(v: tuple[int, ...]) -> tuple[int, ...] | None:
    vv = tuple(x % MOD for x in v)
    if all(x == 0 for x in vv):
        return None
    for x in vv:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % MOD for y in vv)
    raise AssertionError("unreachable")


def symplectic_form(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> int:
    return (a[0] * b[2] + a[1] * b[3] - a[2] * b[0] - a[3] * b[1]) % MOD


def w33_collinearity_graph() -> nx.Graph:
    points: list[tuple[int, int, int, int]] = []
    seen: set[tuple[int, int, int, int]] = set()
    for v in itertools.product(range(MOD), repeat=4):
        c = canonical_projective(v)
        if c is not None and c not in seen:
            seen.add(c)
            points.append(c)  # type: ignore[arg-type]
    points.sort()
    graph = nx.Graph()
    graph.add_nodes_from(range(len(points)))
    for i, j in itertools.combinations(range(len(points)), 2):
        if symplectic_form(points[i], points[j]) == 0:
            graph.add_edge(i, j)
    return graph


def w33_levi_graph() -> nx.Graph:
    w33 = w33_collinearity_graph()
    lines = [tuple(sorted(c)) for c in nx.find_cliques(w33) if len(c) == 4]
    lines.sort()
    levi = nx.Graph()
    for p in range(w33.number_of_nodes()):
        levi.add_node(("p", p))
    for li, line in enumerate(lines):
        ln = ("l", li)
        levi.add_node(ln)
        for p in line:
            levi.add_edge(("p", p), ln)
    return levi


def format_cycle(cycle: list[object]) -> list[str]:
    return [f"{kind}{idx}" if isinstance(kind, str) else str((kind, idx)) for kind, idx in cycle]


def main() -> None:
    H = heawood_graph()
    L = w33_levi_graph()
    clock_basis = nx.cycle_basis(H, root=0)
    levi_basis = nx.cycle_basis(L, root=("p", 0))

    # Gauge datum: choose the eight shortest cycles from one deterministic Levi basis.
    selected_levi = sorted(levi_basis, key=lambda c: (len(c), repr(c)))[:8]
    bridge = []
    for i, (hc, lc) in enumerate(zip(clock_basis, selected_levi)):
        bridge.append({
            "slot": i,
            "clock_cycle_length": len(hc),
            "clock_cycle": list(hc),
            "levi_cycle_length": len(lc),
            "levi_cycle": format_cycle(lc),
        })

    result = {
        "theorem": "BT1662 Clock-Levi Gauge Bridge Search",
        "input_boundary": "BT1659 forbids a literal Heawood subgraph inside the W33 Levi graph because girth 6 cannot embed into girth 8.",
        "gauge_datum": {
            "clock_basis": "NetworkX deterministic cycle_basis rooted at clock node 0",
            "levi_basis": "NetworkX deterministic cycle_basis rooted at Levi node p0",
            "bridge_selector": "the eight shortest cycles in that Levi basis, sorted by length then representation",
        },
        "dimensions": {
            "clock_beta1": len(clock_basis),
            "levi_beta1": len(levi_basis),
            "bridge_rank": len(bridge),
            "levi_unselected_rank": len(levi_basis) - len(bridge),
        },
        "bridge": bridge,
        "bridge_matrix_description": "8x81 matrix [I_8 | 0_8x73] in the chosen clock/Levi cycle bases; this is an injective homology-coordinate bridge, not a graph embedding.",
        "boundary": "The bridge is concrete only after choosing a spanning-tree/cycle-basis gauge. Without that gauge, BT1659's natural object remains the full 8*81 Hodge tensor coupling."
    }

    assert result["dimensions"] == {"clock_beta1": 8, "levi_beta1": 81, "bridge_rank": 8, "levi_unselected_rank": 73}
    assert all(item["levi_cycle_length"] == 8 for item in bridge)

    out = Path("data/PART_BT1662_CLOCK_LEVI_GAUGE_BRIDGE_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
