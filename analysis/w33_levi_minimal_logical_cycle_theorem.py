#!/usr/bin/env python3
"""BT545: W33 Levi Minimal Logical Cycle Theorem.

Local NetworkX verifier.

Core idea
---------
Build W(3,3) as the symplectic polar graph on the 40 projective points of
F_3^4.  Its 40 maximal K4 cliques are the lines of the generalized quadrangle.
The point-line Levi graph L has

    40 point nodes + 40 line nodes = 80 vertices,
    40 lines * 4 incident points  = 160 flag edges.

Therefore

    beta_1(L) = 160 - 80 + 1 = 81.

The new structural hit is that the simple 8-cycles of this Levi graph are
exactly 1620, and every Levi flag-edge lies in exactly 81 of them:

    160 * 81 = 1620 * 8 = 12960.

This gives a purely incidence-geometric model for the previous minimal logical
surface counts:

    X_min^supp = 160  <-> point-line flags / Levi edges,
    Z_min^supp = 1620 <-> simple 8-cycles / GQ quadrangles,
    H_1 = 81          <-> cycle rank and edge-cycle degree.

The vector-level 162 also appears without extra machinery: every Levi vertex
(point or line) lies in exactly 162 simple 8-cycles.
"""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from pathlib import Path

import networkx as nx
import numpy as np

MOD = 3
Q = 3
V_W33 = 40
K_W33 = 12
LAMBDA = 2
MU = 4
LINES_W33 = 40
POINTS_PER_LINE = 4
FLAGS = 160
W33_EDGES = 240
X_MIN_SUPPORT = 160
Z_MIN_SUPPORT = 1620
H1 = 81
WE6 = 51840


def canonical_projective(v: tuple[int, ...]) -> tuple[int, ...]:
    v = tuple(x % MOD for x in v)
    for a in v:
        if a % MOD:
            inv = 1 if a == 1 else 2
            return tuple((x * inv) % MOD for x in v)
    raise ValueError("zero vector has no projective representative")


def symplectic(u: tuple[int, int, int, int], v: tuple[int, int, int, int]) -> int:
    # Standard alternating form with block matrix [[0,I],[-I,0]].
    return (u[0] * v[2] + u[1] * v[3] - u[2] * v[0] - u[3] * v[1]) % MOD


def build_w33() -> nx.Graph:
    points = sorted(
        {canonical_projective(v) for v in itertools.product(range(MOD), repeat=4) if any(v)}
    )
    g = nx.Graph()
    g.add_nodes_from(points)
    for i, u in enumerate(points):
        for v in points[i + 1 :]:
            if symplectic(u, v) == 0:
                g.add_edge(u, v)
    return g


def srg_parameters(g: nx.Graph) -> dict:
    nodes = list(g.nodes())
    common = Counter()
    for u, v in itertools.combinations(nodes, 2):
        c = len(set(g.neighbors(u)) & set(g.neighbors(v)))
        common[(g.has_edge(u, v), c)] += 1
    degrees = Counter(dict(g.degree()).values())
    return {"degrees": dict(degrees), "common_neighbor_profile": {str(k): v for k, v in common.items()}}


def extract_lines(g: nx.Graph) -> list[tuple]:
    # For GQ(3,3), each maximal clique is a line K4.
    lines = [tuple(sorted(c)) for c in nx.find_cliques(g) if len(c) == POINTS_PER_LINE]
    lines = sorted(set(lines))
    return lines


def build_levi(g: nx.Graph, lines: list[tuple]) -> nx.Graph:
    points = list(sorted(g.nodes()))
    p_index = {p: i for i, p in enumerate(points)}
    levi = nx.Graph()
    levi.add_nodes_from(("P", i) for i in range(len(points)))
    levi.add_nodes_from(("L", i) for i in range(len(lines)))
    for li, line in enumerate(lines):
        for p in line:
            levi.add_edge(("P", p_index[p]), ("L", li))
    return levi


def canonical_cycle(ids: list[int]) -> tuple[int, ...]:
    n = len(ids)
    rots = []
    for seq in (ids, list(reversed(ids))):
        for i in range(n):
            rots.append(tuple(seq[i:] + seq[:i]))
    return min(rots)


def simple_cycles_fixed_length(g: nx.Graph, k: int) -> set[tuple[int, ...]]:
    nodes = list(g.nodes())
    node_id = {n: i for i, n in enumerate(nodes)}
    cycles: set[tuple[int, ...]] = set()
    for start in nodes:
        stack = [(start, [start], {start})]
        while stack:
            u, path, seen = stack.pop()
            if len(path) == k:
                if start in g[u]:
                    cycles.add(canonical_cycle([node_id[x] for x in path]))
                continue
            for w in g[u]:
                if w == start:
                    continue
                if w not in seen:
                    stack.append((w, path + [w], seen | {w}))
    return cycles


def spectrum_counter(g: nx.Graph) -> dict[str, int]:
    a = nx.to_numpy_array(g, dtype=int)
    eig = np.linalg.eigvalsh(a)
    out: Counter = Counter()
    for x in eig:
        if abs(x) < 1e-9:
            key = "0"
        elif abs(x - 4) < 1e-9:
            key = "4"
        elif abs(x + 4) < 1e-9:
            key = "-4"
        elif abs(abs(x) - math.sqrt(6)) < 1e-9:
            key = "sqrt6" if x > 0 else "-sqrt6"
        else:
            key = f"{x:.12g}"
        out[key] += 1
    return dict(sorted(out.items()))


def main() -> dict:
    w33 = build_w33()
    lines = extract_lines(w33)
    levi = build_levi(w33, lines)

    # Line/edge uniqueness: every W33 edge belongs to exactly one K4 line.
    edge_to_lines = Counter()
    for li, line in enumerate(lines):
        for e in itertools.combinations(line, 2):
            edge_to_lines[tuple(sorted(e))] += 1

    cycles8 = simple_cycles_fixed_length(levi, 8)
    levi_nodes = list(levi.nodes())
    id_to_node = {i: n for i, n in enumerate(levi_nodes)}

    edge_cycle_counts = Counter()
    vertex_cycle_counts = Counter()
    for cyc in cycles8:
        cyc_nodes = [id_to_node[i] for i in cyc]
        for n in cyc_nodes:
            vertex_cycle_counts[n] += 1
        for a, b in zip(cyc_nodes, cyc_nodes[1:] + cyc_nodes[:1]):
            edge_cycle_counts[tuple(sorted((a, b), key=str))] += 1

    beta_1 = levi.number_of_edges() - levi.number_of_nodes() + nx.number_connected_components(levi)
    total_cycle_edge_incidence = sum(edge_cycle_counts.values())

    checks = {
        "w33_has_40_points": w33.number_of_nodes() == V_W33,
        "w33_has_240_edges": w33.number_of_edges() == W33_EDGES,
        "w33_is_12_regular": set(dict(w33.degree()).values()) == {K_W33},
        "w33_srg_common_neighbors": srg_parameters(w33)["common_neighbor_profile"] == {"(False, 4)": 540, "(True, 2)": 240},
        "w33_has_40_lines": len(lines) == LINES_W33,
        "each_line_is_K4": all(len(line) == POINTS_PER_LINE for line in lines),
        "each_w33_edge_in_unique_line": len(edge_to_lines) == W33_EDGES and Counter(edge_to_lines.values()) == {1: W33_EDGES},
        "levi_has_80_vertices": levi.number_of_nodes() == 80,
        "levi_has_160_flag_edges": levi.number_of_edges() == FLAGS,
        "levi_is_connected": nx.is_connected(levi),
        "levi_is_4_regular": set(dict(levi.degree()).values()) == {4},
        "levi_beta1_is_81": beta_1 == H1,
        "levi_simple_8_cycles_are_1620": len(cycles8) == Z_MIN_SUPPORT,
        "cycle_edge_biregularity_81": Counter(edge_cycle_counts.values()) == {H1: FLAGS},
        "cycle_vertex_biregularity_162": Counter(vertex_cycle_counts.values()) == {162: 80},
        "support_incidence_identity": total_cycle_edge_incidence == X_MIN_SUPPORT * H1 == Z_MIN_SUPPORT * 8 == 12960,
        "vector_level_162_identity": 320 * 162 == WE6,
    }

    result = {
        "theorem": "BT545 W33 Levi Minimal Logical Cycle Theorem",
        "w33_point_graph": {
            "construction": "projective points of F_3^4 adjacent when symplectically orthogonal",
            "vertices": w33.number_of_nodes(),
            "edges": w33.number_of_edges(),
            "degree_profile": dict(Counter(dict(w33.degree()).values())),
            "srg_parameters": "SRG(40,12,2,4)",
            "srg_profile": srg_parameters(w33)["common_neighbor_profile"],
            "maximal_K4_lines": len(lines),
            "edge_to_line_profile": dict(Counter(edge_to_lines.values())),
        },
        "levi_graph": {
            "vertices": levi.number_of_nodes(),
            "flag_edges": levi.number_of_edges(),
            "degree_profile": dict(Counter(dict(levi.degree()).values())),
            "connected_components": nx.number_connected_components(levi),
            "cycle_rank_beta1": beta_1,
            "adjacency_spectrum": spectrum_counter(levi),
            "spectrum_formula": "(-4)^1 + (-sqrt(6))^24 + 0^30 + (sqrt(6))^24 + 4^1",
            "symbolic_beta1": "160 - 80 + 1 = 81",
        },
        "minimal_logical_interpretation": {
            "X_min_supports": X_MIN_SUPPORT,
            "X_min_support_reading": "Levi flag edges = point-line flags = W33 line-triangles by flag complement",
            "Z_min_supports": Z_MIN_SUPPORT,
            "Z_min_support_reading": "simple 8-cycles of the point-line Levi graph = GQ quadrangles",
            "H1_reading": "cycle rank of the Levi graph and flag-edge 8-cycle degree",
            "simple_8_cycles": len(cycles8),
            "edge_cycle_degree_profile": dict(Counter(edge_cycle_counts.values())),
            "vertex_cycle_degree_profile": dict(Counter(vertex_cycle_counts.values())),
            "total_cycle_edge_incidence": total_cycle_edge_incidence,
            "support_identity": "160*81 = 1620*8 = 12960",
            "vector_identity": "320*162 = 51840 = |W(E6)|",
            "new_structural_reading": "The previous minimal logical 160/1620/81 counts are exactly the flag-edge / 8-cycle / cycle-rank data of the W33 point-line Levi graph.",
        },
        "all_identities": checks,
        "all_identities_hold": all(checks.values()),
    }

    out = Path("data/PART_BT545_W33_LEVI_MINIMAL_LOGICAL_CYCLE_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    print(f"wrote {out}")
    return result


if __name__ == "__main__":
    main()
