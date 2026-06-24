#!/usr/bin/env python3
"""BT1675 — uniform incidence-edge twirl versus Levi Hodge projector.

BT1671 showed the automorphism twirl is uniform on all 160 W33 Levi incidence
edges.  BT1675 asks whether that uniform edge idempotent has protected H1 content.
It does not: with the standard point-to-line orientation, the all-edge vector is a
pure cut/gradient mode and is annihilated by the Levi cycle-space Hodge projector.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import networkx as nx
import numpy as np

MOD = 3


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


def w33_lines() -> list[tuple[int, int, int, int]]:
    pts = []
    seen = set()
    for v in itertools.product(range(MOD), repeat=4):
        c = canonical_projective(v)
        if c is not None and c not in seen:
            seen.add(c)
            pts.append(c)  # type: ignore[arg-type]
    pts.sort()
    graph = nx.Graph()
    graph.add_nodes_from(range(len(pts)))
    for i, j in itertools.combinations(range(len(pts)), 2):
        if symplectic_form(pts[i], pts[j]) == 0:
            graph.add_edge(i, j)
    return sorted(tuple(sorted(c)) for c in nx.find_cliques(graph) if len(c) == 4)


def main() -> None:
    lines = w33_lines()
    nodes = [("p", i) for i in range(40)] + [("l", j) for j in range(40)]
    node_index = {v: i for i, v in enumerate(nodes)}
    edges = [(("p", p), ("l", li)) for li, line in enumerate(lines) for p in line]
    D = np.zeros((len(nodes), len(edges)))
    for j, (p, line) in enumerate(edges):
        D[node_index[p], j] = -1.0
        D[node_index[line], j] = 1.0

    rank_D = int(np.linalg.matrix_rank(D, tol=1e-8))
    P_cycle = np.eye(len(edges)) - D.T @ np.linalg.pinv(D @ D.T) @ D
    u = np.ones(len(edges))
    Pu = P_cycle @ u
    E_uniform = np.outer(u, u) / float(u @ u)

    result = {
        "theorem": "BT1675 Bose-Mesner/Hodge Bridge Idempotent Test",
        "levi_complex": {
            "vertices": len(nodes),
            "edges": len(edges),
            "incidence_rank": rank_D,
            "cycle_rank_beta1": len(edges) - rank_D,
            "cycle_projector_trace": float(np.trace(P_cycle)),
            "cycle_projector_idempotence_residual": float(np.linalg.norm(P_cycle @ P_cycle - P_cycle)),
        },
        "uniform_incidence_edge_idempotent": {
            "definition": "E_uniform = 1_E 1_E^T / 160",
            "rank": int(round(np.trace(E_uniform))),
            "idempotence_residual": float(np.linalg.norm(E_uniform @ E_uniform - E_uniform)),
            "mean_edge_weight_for_bt1671_64_events": 64 / 160,
        },
        "hodge_overlap": {
            "norm_uniform_edge_vector": float(np.linalg.norm(u)),
            "norm_cycle_projection_of_uniform_edge_vector": float(np.linalg.norm(Pu)),
            "normalized_h1_overlap": float((u @ P_cycle @ u) / (u @ u)),
            "cycle_projector_times_uniform_idempotent_norm": float(np.linalg.norm(P_cycle @ E_uniform)),
        },
        "boundary_operator_on_uniform_edge_vector": {
            "point_boundary_value": -4,
            "line_boundary_value": 4,
            "meaning": "with point-to-line orientation, the uniform incidence vector is a pure bipartite cut mode, not a cycle",
        },
        "conclusion": "The automorphism-twirled bridge is the uniform rank-1 incidence-edge idempotent, but it has zero H1/Hodge-cycle content. A useful clock-Levi homology bridge therefore requires gauge fixing before twirling; full symmetry averaging erases it.",
        "boundary": "This connects the uniform automorphism twirl to the Levi Hodge projector. It does not classify all higher edge-pair Bose-Mesner idempotents.",
    }
    assert result["levi_complex"]["cycle_rank_beta1"] == 81
    assert result["uniform_incidence_edge_idempotent"]["rank"] == 1
    assert result["hodge_overlap"]["norm_cycle_projection_of_uniform_edge_vector"] < 1e-10
    out = Path("data/PART_BT1675_BOSE_MESNER_HODGE_BRIDGE_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
