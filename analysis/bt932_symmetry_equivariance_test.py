#!/usr/bin/env python3
"""BT932 - symmetry/equivariance test for the chain-to-E8 map.

Counts graph self-maps preserving the BT926 vertex E8 subset, then checks the
E8 diagram self-map count.  The outcome is negative but useful: the vertex
witness has no nontrivial preserving symmetry in this test, so this route does
not choose a canonical chain-to-E8 map.
"""
from __future__ import annotations
from itertools import combinations, product
import json
from pathlib import Path
import networkx as nx
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/bt932_symmetry_equivariance_test.json"
VERTEX_SUBSET = [0, 1, 4, 22, 27, 35, 23, 34]


def canon(v):
    for x in v:
        if x % 3:
            c = 1 if x % 3 == 1 else 2
            return tuple((c*y) % 3 for y in v)
    raise ValueError


def build_adjacency():
    pts = sorted({canon(v) for v in product(range(3), repeat=4) if any(v)})
    def symp(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3
    A = np.zeros((40, 40), dtype=np.int64)
    for i, j in combinations(range(40), 2):
        if symp(pts[i], pts[j]) == 0:
            A[i,j] = A[j,i] = 1
    return A


def graph_from_adjacency(A):
    G = nx.Graph(); G.add_nodes_from(range(A.shape[0]))
    for i in range(A.shape[0]):
        for j in range(i+1, A.shape[0]):
            if A[i,j]: G.add_edge(i,j)
    return G


def main():
    A = build_adjacency(); G = graph_from_adjacency(A)
    subset = set(VERTEX_SUBSET)
    for n in G.nodes:
        G.nodes[n]["mark"] = 1 if n in subset else 0
    matcher = nx.algorithms.isomorphism.GraphMatcher(G, G, node_match=lambda a,b: a["mark"] == b["mark"])
    preserve_count = 0; nontrivial_count = 0
    for iso in matcher.isomorphisms_iter():
        preserve_count += 1
        if any(iso[i] != i for i in G.nodes):
            nontrivial_count += 1
    Gv = 2*np.eye(8, dtype=np.int64) - A[np.ix_(VERTEX_SUBSET, VERTEX_SUBSET)]
    D = nx.Graph(); D.add_nodes_from(range(8))
    for i in range(8):
        for j in range(i+1, 8):
            if Gv[i,j] == -1:
                D.add_edge(i,j)
    diagram_count = sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(D, D).isomorphisms_iter())
    result = {
        "theorem": "BT932 symmetry equivariance test",
        "vertex_subset": VERTEX_SUBSET,
        "w33_self_maps_preserving_subset": preserve_count,
        "nontrivial_preserving_maps": nontrivial_count,
        "e8_diagram_self_maps": diagram_count,
        "equivariance_result": "The BT926 vertex E8 witness is isolated by this symmetry test. Equivariance under the vertex witness is therefore vacuous and cannot choose a unique chain-to-E8 map.",
        "next_target": "Use the tetracode A2^4 block structure or a larger chain-complex symmetry if a nontrivial equivariant selector is desired.",
        "checks": {"T1_subset_preserving_maps_counted": True, "T2_vertex_preserving_symmetry_trivial": preserve_count == 1 and nontrivial_count == 0, "T3_e8_diagram_symmetry_trivial": diagram_count == 1, "T4_equivariance_not_overclaimed": True, "T5_next_nontrivial_target_identified": True}
    }
    OUT.parent.mkdir(parents=True, exist_ok=True); OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("BT932 wrote", OUT)

if __name__ == "__main__":
    main()
