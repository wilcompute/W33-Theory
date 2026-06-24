#!/usr/bin/env python3
"""
BT1659 — Clock/Levi Hodge coupling boundary theorem.

The request was to build an explicit clock-to-Levi coupling matrix while respecting
the BT1654 girth boundary.  The key result is negative/positive:

  negative: there is no injective edge-preserving Heawood-clock subgraph inside the
            W33 point-line Levi graph, because Heawood has girth 6 while the Levi
            graph has girth 8.

  positive: the canonical functorial coupling is the Hodge tensor projector
            P_clock_cycle \otimes P_Levi_cycle on edge-chain tensors.  It has rank
            8*81=648 and requires no coordinate selector.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import networkx as nx
import numpy as np

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


def w33_lines_from_cliques(w33: nx.Graph) -> list[tuple[int, int, int, int]]:
    lines = [tuple(sorted(c)) for c in nx.find_cliques(w33) if len(c) == 4]
    lines.sort()
    return lines


def w33_levi_graph() -> nx.Graph:
    w33 = w33_collinearity_graph()
    lines = w33_lines_from_cliques(w33)
    levi = nx.Graph()
    for p in range(w33.number_of_nodes()):
        levi.add_node(("p", p))
    for li, line in enumerate(lines):
        ln = ("l", li)
        levi.add_node(ln)
        for p in line:
            levi.add_edge(("p", p), ln)
    return levi


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


def oriented_incidence_matrix(graph: nx.Graph, nodelist: list[object], edgelist: list[tuple[object, object]]) -> np.ndarray:
    row = {v: i for i, v in enumerate(nodelist)}
    D = np.zeros((len(nodelist), len(edgelist)), dtype=float)
    for j, (u, v) in enumerate(edgelist):
        D[row[u], j] = -1.0
        D[row[v], j] = 1.0
    return D


def rank(A: np.ndarray) -> int:
    return int(np.linalg.matrix_rank(A, tol=1e-8))


def main() -> None:
    H = heawood_graph()
    L = w33_levi_graph()

    H_nodes = list(range(14))
    H_edges = sorted([tuple(sorted(e)) for e in H.edges()], key=repr)
    L_nodes = sorted(list(L.nodes()), key=repr)
    L_edges = sorted([tuple(sorted(e, key=repr)) for e in L.edges()], key=repr)

    DH = oriented_incidence_matrix(H, H_nodes, H_edges)
    DL = oriented_incidence_matrix(L, L_nodes, L_edges)

    H_rank = rank(DH)
    L_rank = rank(DL)
    H_beta = H.number_of_edges() - H_rank
    L_beta = L.number_of_edges() - L_rank

    assert H_rank == H.number_of_nodes() - 1 == 13
    assert L_rank == L.number_of_nodes() - 1 == 79
    assert H_beta == 8
    assert L_beta == 81

    H_girth = graph_girth(H)
    L_girth = graph_girth(L)
    assert H_girth == 6
    assert L_girth == 8

    # Hodge cycle projectors have rank beta_1.  The tensor projector is the
    # coordinate-free coupling on edge-chain tensor space.
    coupling_rank = H_beta * L_beta
    edge_tensor_dim = H.number_of_edges() * L.number_of_edges()
    cut_or_mixed_dim = edge_tensor_dim - coupling_rank

    result = {
        "theorem": "BT1659 Clock/Levi Hodge Coupling Boundary Theorem",
        "clock_complex": {
            "graph": "Heawood/Fano incidence clock",
            "vertices": H.number_of_nodes(),
            "edges": H.number_of_edges(),
            "incidence_rank": H_rank,
            "cycle_rank_beta1": H_beta,
            "girth": H_girth,
        },
        "levi_complex": {
            "graph": "W33 point-line Levi graph",
            "vertices": L.number_of_nodes(),
            "edges": L.number_of_edges(),
            "incidence_rank": L_rank,
            "cycle_rank_beta1": L_beta,
            "girth": L_girth,
        },
        "subgraph_boundary": {
            "injective_edge_preserving_clock_embedding": false,
            "reason": "An injective edge-preserving image of any Heawood 6-cycle would be a 6-cycle in the W33 Levi graph, but the W33 Levi graph has girth 8.",
        },
        "functorial_coupling": {
            "operator": "P_clock_cycle ⊗ P_Levi_cycle",
            "ambient_edge_tensor_dimension": edge_tensor_dim,
            "rank": coupling_rank,
            "rank_factorization": "8 * 81 = 648",
            "complement_dimension": cut_or_mixed_dim,
            "meaning": "This is the canonical selector-free Hodge coupling of the Heawood runtime word to the protected W33 Levi H1 sector.",
        },
        "boundary": "A direct clock-to-Levi subgraph transfer is forbidden. The natural coupling is homological/tensorial unless an additional gauge or embedding datum is supplied.",
    }

    out_path = Path("data/PART_BT1659_CLOCK_LEVI_HODGE_COUPLING_results.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
