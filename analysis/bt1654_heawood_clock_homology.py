#!/usr/bin/env python3
"""
BT1654 — Heawood clock homology / runtime-word verifier.

Recent holonet commits identify the machine clock with the Heawood/Fano
incidence oscillator.  This verifier extracts the purely combinatorial part of
that claim using NetworkX, and it also keeps the honest boundary against the
W33 point-line Levi graph.

Main result:
  * the Heawood clock has |V|=14, |E|=21, beta_1=8;
  * it has exactly 28 simple 6-cycles and 21 simple 8-cycles;
  * its Laplacian has the oscillator spectrum
        0^1, (3-sqrt(2))^6, (3+sqrt(2))^6, 6^1;
  * its line graph has 21 vertices, is 4-regular, has 14 triangles, and carries
    the same middle oscillator shell plus an 8-dimensional top shell at 6;
  * the W33 point-line Levi graph has girth 8 and zero 6-cycles, so the Heawood
    clock is not a literal Levi subgraph.  It is a separate clock/homology
    module coupled to the W33 machine.
"""
from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from pathlib import Path
from typing import Iterable, Tuple

import networkx as nx
import numpy as np

MOD = 3
Q = 3
LAMBDA = 2


def fano_lines() -> list[tuple[int, int, int]]:
    """Cyclic Fano plane line model: {i, i+1, i+3} mod 7."""
    return [tuple(sorted((i % 7, (i + 1) % 7, (i + 3) % 7))) for i in range(7)]


def heawood_graph() -> nx.Graph:
    """Incidence graph of PG(2,2), with points 0..6 and lines 7..13."""
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
        if x % MOD:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % MOD for y in vv)
    raise AssertionError("unreachable")


def symplectic_form(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> int:
    return (a[0] * b[2] + a[1] * b[3] - a[2] * b[0] - a[3] * b[1]) % MOD


def w33_collinearity_graph() -> tuple[nx.Graph, list[tuple[int, int, int, int]]]:
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
    return graph, points


def w33_lines_from_cliques(w33: nx.Graph) -> list[tuple[int, int, int, int]]:
    lines = [tuple(sorted(c)) for c in nx.find_cliques(w33) if len(c) == 4]
    lines.sort()
    return lines


def w33_levi_graph() -> nx.Graph:
    w33, _points = w33_collinearity_graph()
    lines = w33_lines_from_cliques(w33)
    levi = nx.Graph()
    for p in range(w33.number_of_nodes()):
        levi.add_node(("p", p))
    for line_index, line in enumerate(lines):
        line_node = ("l", line_index)
        levi.add_node(line_node)
        for p in line:
            levi.add_edge(("p", p), line_node)
    return levi


def cycle_rank(graph: nx.Graph) -> int:
    return graph.number_of_edges() - graph.number_of_nodes() + nx.number_connected_components(graph)


def graph_girth(graph: nx.Graph) -> int | None:
    best: int | None = None
    for source in graph.nodes():
        dist = {source: 0}
        parent = {source: None}
        queue = [source]
        for v in queue:
            for nb in graph.neighbors(v):
                if nb not in dist:
                    dist[nb] = dist[v] + 1
                    parent[nb] = v
                    queue.append(nb)
                elif parent[v] != nb and parent[nb] != v:
                    length = dist[v] + dist[nb] + 1
                    if best is None or length < best:
                        best = length
    return best


def normalized_cycle(path: list[object]) -> tuple[object, ...]:
    n = len(path)
    reps: list[tuple[object, ...]] = []
    for seq in (path, list(reversed(path))):
        for i in range(n):
            reps.append(tuple(seq[i:] + seq[:i]))
    return min(reps, key=repr)


def count_simple_cycles_of_length(graph: nx.Graph, length: int) -> int:
    seen: set[tuple[object, ...]] = set()
    nodes = list(graph.nodes())
    for start in nodes:
        stack: list[tuple[object, list[object]]] = [(start, [start])]
        while stack:
            v, path = stack.pop()
            if len(path) == length:
                if graph.has_edge(path[-1], start):
                    seen.add(normalized_cycle(path))
                continue
            for nb in graph.neighbors(v):
                if nb == start or nb in path:
                    continue
                stack.append((nb, path + [nb]))
    return len(seen)


def spectrum_counter(matrix: np.ndarray, places: int = 6) -> dict[str, int]:
    vals = np.linalg.eigvalsh(matrix)
    counter = Counter(round(float(x), places) for x in vals)
    # Normalize negative zero in JSON keys.
    return {str(0.0 if abs(k) < 10 ** (-places) else k): int(v) for k, v in sorted(counter.items())}


def laplacian_matrix(graph: nx.Graph, nodelist: list[object]) -> np.ndarray:
    adj = nx.to_numpy_array(graph, nodelist=nodelist, dtype=float)
    return np.diag(adj.sum(axis=1)) - adj


def main() -> None:
    H = heawood_graph()
    H_nodes = list(range(14))
    H_adj = nx.to_numpy_array(H, nodelist=H_nodes, dtype=float)
    H_lap = laplacian_matrix(H, H_nodes)

    lineH = nx.line_graph(H)
    lineH_nodes = sorted(lineH.nodes(), key=repr)
    lineH_adj = nx.to_numpy_array(lineH, nodelist=lineH_nodes, dtype=float)
    lineH_lap = laplacian_matrix(lineH, lineH_nodes)

    levi = w33_levi_graph()

    result = {
        "theorem": "BT1654 Heawood Clock Homology / Runtime Word Theorem",
        "heawood_clock": {
            "vertices": H.number_of_nodes(),
            "edges": H.number_of_edges(),
            "regular_degree": sorted(set(dict(H.degree()).values())),
            "is_bipartite": nx.is_bipartite(H),
            "girth": graph_girth(H),
            "cycle_rank_beta1": cycle_rank(H),
            "simple_6_cycles": count_simple_cycles_of_length(H, 6),
            "simple_8_cycles": count_simple_cycles_of_length(H, 8),
            "adjacency_spectrum": spectrum_counter(H_adj),
            "laplacian_spectrum": spectrum_counter(H_lap),
            "oscillator_shell": {
                "middle_shell_dimension": 12,
                "lambda": LAMBDA,
                "omega": math.sqrt(LAMBDA),
                "energy_minus": Q - math.sqrt(LAMBDA),
                "energy_plus": Q + math.sqrt(LAMBDA),
            },
        },
        "heawood_line_graph_flag_clock": {
            "vertices": lineH.number_of_nodes(),
            "edges": lineH.number_of_edges(),
            "regular_degree": sorted(set(dict(lineH.degree()).values())),
            "triangles": int(sum(nx.triangles(lineH).values()) // 3),
            "girth": graph_girth(lineH),
            "cycle_rank_beta1": cycle_rank(lineH),
            "adjacency_spectrum": spectrum_counter(lineH_adj),
            "laplacian_spectrum": spectrum_counter(lineH_lap),
        },
        "w33_levi_boundary": {
            "vertices": levi.number_of_nodes(),
            "edges": levi.number_of_edges(),
            "cycle_rank_beta1": cycle_rank(levi),
            "girth": graph_girth(levi),
            "simple_6_cycles": count_simple_cycles_of_length(levi, 6),
            "simple_8_cycles": count_simple_cycles_of_length(levi, 8),
            "boundary": "Levi girth 8 and zero 6-cycles forbid a literal Heawood-clock subgraph; the Heawood/Fano clock is a separate runtime homology module, not an incidence subgraph of the W33 Levi graph.",
        },
        "constant_bridge": {
            "14": "Heawood vertices = Fano points + Fano lines = dim(G2)",
            "21": "Heawood edges = Fano flags = C(7,2) bivector/K7 carrier",
            "8": "Heawood beta_1 = runtime 8-tick word",
            "28": "Heawood simple 6-cycles = W33 externality mu = v-k = 40-12",
            "12": "Heawood oscillator middle shell dimension = W33 degree k",
            "6": "Heawood girth and top Laplacian endpoint = g2",
            "4": "Heawood line graph degree = W33 nonadjacent common-neighbor number mu_GQ",
            "81": "W33 Levi beta_1 remains the protected H1 sector, separate from the 8-dimensional clock word.",
        },
    }

    assert result["heawood_clock"]["vertices"] == 14
    assert result["heawood_clock"]["edges"] == 21
    assert result["heawood_clock"]["cycle_rank_beta1"] == 8
    assert result["heawood_clock"]["simple_6_cycles"] == 28
    assert result["heawood_clock"]["simple_8_cycles"] == 21
    assert result["heawood_clock"]["laplacian_spectrum"] == {
        "0.0": 1,
        "1.585786": 6,
        "4.414214": 6,
        "6.0": 1,
    }
    assert result["heawood_line_graph_flag_clock"]["vertices"] == 21
    assert result["heawood_line_graph_flag_clock"]["regular_degree"] == [4]
    assert result["heawood_line_graph_flag_clock"]["triangles"] == 14
    assert result["w33_levi_boundary"]["girth"] == 8
    assert result["w33_levi_boundary"]["simple_6_cycles"] == 0
    assert result["w33_levi_boundary"]["simple_8_cycles"] == 1620

    out_path = Path("data/PART_BT1654_HEAWOOD_CLOCK_HOMOLOGY_results.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
