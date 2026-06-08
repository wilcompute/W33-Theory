#!/usr/bin/env python3
"""BT548: W33 Levi Line-Graph 3-adic Metric Kernel Theorem.

This continues BT545--BT547.

BT545: the W33 point-line Levi graph L has 80 vertices, 160 flag edges,
beta_1=81, and 1620 simple 8-cycles.

BT546: the oriented simple-8-cycle incidence matrix C satisfies

    spec(C C^T)=160^81 + 0^79,

and the unsigned incidence matrix B has the 3-adic overlap profile
1,3,9,27.

BT547: (1/160) C C^T is exactly the Hodge/Kirchhoff cycle-space
projector of L.

This theorem identifies the hidden metric source of the 3-adic overlaps.

Let X = LineGraph(L), whose vertices are the 160 Levi flag-edges.  Then X is
distance-regular with diameter 4 and intersection array

    b = [6,3,3,3],
    c = [1,1,1,2],

with distance distribution per flag

    1^6, 2^18, 3^54, 4^81.

If rho(e,f) is the graph distance in X, then for all flag-edges e,f,

    (C C^T)_{ef} = (-3)^(4-rho(e,f)),
    (B B^T)_{ef} =   3^(4-rho(e,f)),

where rho(e,e)=0.  Thus the signed Hodge phase kernel and the unsigned
minimal-logical visibility kernel are both pure 3-adic distance kernels on the
Levi line graph.

Equivalently, the Hodge cycle projector is the spectral projector onto the
-2 eigenspace of X:

    (1/160) C C^T = E_{-2}(A_X),

and

    spec(A_X)=6^1 + (2+sqrt(6))^24 + 2^30 + (2-sqrt(6))^24 + (-2)^81.

The integer polynomial certificate is

    C C^T =
      1/2 (A_X-6I)(A_X-2I)(A_X^2-4A_X-2I).

So the protected H_1=81 sector is exactly the -2 eigenspace of the Levi
flag-adjacency graph.
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
POINTS_PER_LINE = 4
LEVI_EDGES = 160
CYCLES8 = 1620


def canonical_projective(v: tuple[int, ...]) -> tuple[int, ...]:
    v = tuple(x % MOD for x in v)
    for a in v:
        if a % MOD:
            inv = 1 if a == 1 else 2
            return tuple((x * inv) % MOD for x in v)
    raise ValueError("zero vector has no projective representative")


def symplectic(u: tuple[int, int, int, int], v: tuple[int, int, int, int]) -> int:
    return (u[0] * v[2] + u[1] * v[3] - u[2] * v[0] - u[3] * v[1]) % MOD


def build_w33() -> tuple[nx.Graph, list[tuple[int, int, int, int]]]:
    points = sorted(
        {canonical_projective(v) for v in itertools.product(range(MOD), repeat=4) if any(v)}
    )
    g = nx.Graph()
    g.add_nodes_from(points)
    for i, u in enumerate(points):
        for v in points[i + 1 :]:
            if symplectic(u, v) == 0:
                g.add_edge(u, v)
    return g, points


def build_levi(g: nx.Graph, points: list[tuple[int, int, int, int]]) -> tuple[nx.Graph, list[tuple]]:
    lines = sorted(set(tuple(sorted(c)) for c in nx.find_cliques(g) if len(c) == POINTS_PER_LINE))
    p_index = {p: i for i, p in enumerate(points)}
    levi = nx.Graph()
    levi.add_nodes_from(range(len(points) + len(lines)))
    for li, line in enumerate(lines):
        line_node = len(points) + li
        for p in line:
            levi.add_edge(p_index[p], line_node)
    return levi, lines


def canonical_cycle(path: list[int]) -> tuple[int, ...]:
    out: list[tuple[int, ...]] = []
    for seq in (path, list(reversed(path))):
        for i in range(len(seq)):
            out.append(tuple(seq[i:] + seq[:i]))
    return min(out)


def simple_cycles_fixed_length(g: nx.Graph, k: int) -> list[tuple[int, ...]]:
    cycles: set[tuple[int, ...]] = set()
    for start in g.nodes():
        stack = [(start, [start], {start})]
        while stack:
            u, path, seen = stack.pop()
            if len(path) == k:
                if g.has_edge(u, start):
                    cycles.add(canonical_cycle(path))
                continue
            for w in g.neighbors(u):
                if w == start:
                    continue
                if w not in seen:
                    stack.append((w, path + [w], seen | {w}))
    return sorted(cycles)


def spectrum_counter(mat: np.ndarray) -> dict[str, int]:
    vals = np.linalg.eigvalsh(mat.astype(float))
    out: Counter[str] = Counter()
    for x in vals:
        if abs(x - 6) < 1e-8:
            out["6"] += 1
        elif abs(x - 2) < 1e-8:
            out["2"] += 1
        elif abs(x + 2) < 1e-8:
            out["-2"] += 1
        elif abs(x - (2 + math.sqrt(6))) < 1e-8:
            out["2+sqrt6"] += 1
        elif abs(x - (2 - math.sqrt(6))) < 1e-8:
            out["2-sqrt6"] += 1
        else:
            out[f"{x:.12g}"] += 1
    return dict(out)


def matrix_profile(mat: np.ndarray, diagonal: bool = False) -> dict[str, int]:
    vals = []
    n = mat.shape[0]
    for i in range(n):
        for j in range(n):
            if diagonal or i != j:
                vals.append(int(round(mat[i, j])))
    return {str(k): v for k, v in sorted(Counter(vals).items())}


def main() -> dict:
    w33, points = build_w33()
    levi, lines = build_levi(w33, points)
    edges = sorted(tuple(sorted(e)) for e in levi.edges())
    edge_index = {e: i for i, e in enumerate(edges)}
    cycles = simple_cycles_fixed_length(levi, 8)

    B = np.zeros((LEVI_EDGES, CYCLES8), dtype=int)
    C = np.zeros((LEVI_EDGES, CYCLES8), dtype=int)

    for j, cyc in enumerate(cycles):
        for a, b in zip(cyc, cyc[1:] + cyc[:1]):
            e = tuple(sorted((a, b)))
            point, line = (e[0], e[1]) if e[0] < 40 else (e[1], e[0])
            sign = +1 if (a, b) == (point, line) else -1
            idx = edge_index[e]
            B[idx, j] = 1
            C[idx, j] = sign

    BBt = B @ B.T
    CCt = C @ C.T

    # Build the line graph of the Levi graph on the same sorted flag-edge labels.
    X = nx.Graph()
    X.add_nodes_from(edges)
    for a, b in itertools.combinations(edges, 2):
        if set(a) & set(b):
            X.add_edge(a, b)

    dist = dict(nx.all_pairs_shortest_path_length(X))
    distance_matrix = np.zeros((LEVI_EDGES, LEVI_EDGES), dtype=int)
    for i, e in enumerate(edges):
        for j, f in enumerate(edges):
            distance_matrix[i, j] = dist[e][f]

    # 3-adic distance kernels.
    signed_metric_kernel = np.zeros_like(CCt)
    unsigned_metric_kernel = np.zeros_like(BBt)
    for i in range(LEVI_EDGES):
        for j in range(LEVI_EDGES):
            rho = int(distance_matrix[i, j])
            signed_metric_kernel[i, j] = (-3) ** (4 - rho)
            unsigned_metric_kernel[i, j] = 3 ** (4 - rho)

    # Distance-regular intersection data.
    intersection_profiles: dict[str, dict[str, int]] = {}
    for d in range(1, 5):
        profile_counter: Counter[str] = Counter()
        for x in edges:
            for y in edges:
                if dist[x][y] != d:
                    continue
                local = Counter(dist[x][z] for z in X.neighbors(y))
                profile_counter[str(dict(sorted(local.items())))] += 1
        intersection_profiles[str(d)] = dict(profile_counter)

    distance_distribution = Counter(distance_matrix[0, j] for j in range(LEVI_EDGES))
    all_distance_distributions = {
        tuple(sorted(Counter(distance_matrix[i, j] for j in range(LEVI_EDGES)).items()))
        for i in range(LEVI_EDGES)
    }

    A = nx.to_numpy_array(X, nodelist=edges, dtype=int)
    I = np.eye(LEVI_EDGES)
    polynomial_CCt = ((A - 6 * I) @ (A - 2 * I) @ (A @ A - 4 * A - 2 * I)) / 2

    # Distance matrices A_0...A_4.
    distance_matrices = []
    for d in range(5):
        distance_matrices.append((distance_matrix == d).astype(int))
    distance_expansion_signed = sum(((-3) ** (4 - d)) * distance_matrices[d] for d in range(5))
    distance_expansion_unsigned = sum((3 ** (4 - d)) * distance_matrices[d] for d in range(5))

    checks = {
        "w33_srg_size": w33.number_of_nodes() == 40 and w33.number_of_edges() == 240,
        "w33_lines_40": len(lines) == 40,
        "levi_size": levi.number_of_nodes() == 80 and levi.number_of_edges() == 160,
        "levi_regular_4": set(dict(levi.degree()).values()) == {4},
        "cycles8_1620": len(cycles) == 1620,
        "line_graph_size": X.number_of_nodes() == 160 and X.number_of_edges() == 480,
        "line_graph_regular_6": set(dict(X.degree()).values()) == {6},
        "line_graph_diameter_4": nx.diameter(X) == 4,
        "distance_distribution_uniform": len(all_distance_distributions) == 1
        and dict(distance_distribution) == {0: 1, 1: 6, 2: 18, 3: 54, 4: 81},
        "intersection_array": intersection_profiles == {
            "1": {"{0: 1, 1: 2, 2: 3}": 960},
            "2": {"{1: 1, 2: 2, 3: 3}": 2880},
            "3": {"{2: 1, 3: 2, 4: 3}": 8640},
            "4": {"{3: 2, 4: 4}": 12960},
        },
        "signed_kernel_is_3adic_distance_kernel": np.array_equal(CCt, signed_metric_kernel),
        "unsigned_kernel_is_3adic_distance_kernel": np.array_equal(BBt, unsigned_metric_kernel),
        "signed_distance_expansion": np.array_equal(CCt, distance_expansion_signed),
        "unsigned_distance_expansion": np.array_equal(BBt, distance_expansion_unsigned),
        "line_graph_spectrum": spectrum_counter(A) == {
            "6": 1,
            "2+sqrt6": 24,
            "2": 30,
            "2-sqrt6": 24,
            "-2": 81,
        },
        "minus_two_projector_rank_81": int(np.linalg.matrix_rank(CCt)) == 81,
        "polynomial_projector_certificate": np.max(np.abs(polynomial_CCt - CCt)) < 1e-8,
        "signed_idempotent": np.array_equal(CCt @ CCt, 160 * CCt),
    }
    checks = {k: bool(v) for k, v in checks.items()}

    result = {
        "theorem": "BT548 W33 Levi Line-Graph 3-adic Metric Kernel Theorem",
        "objects": {
            "levi_vertices": levi.number_of_nodes(),
            "levi_edges_flags": levi.number_of_edges(),
            "simple_8_cycles": len(cycles),
            "line_graph_vertices": X.number_of_nodes(),
            "line_graph_edges": X.number_of_edges(),
            "line_graph_degree": 6,
            "line_graph_diameter": nx.diameter(X),
        },
        "distance_regular_structure": {
            "distance_distribution_per_flag": {str(k): int(v) for k, v in sorted(distance_distribution.items())},
            "intersection_array": "b=[6,3,3,3], c=[1,1,1,2]",
            "intersection_profiles": intersection_profiles,
            "reading": "The 160 Levi flags form a diameter-4 distance-regular line graph with shells 6,18,54,81.",
        },
        "metric_kernel_law": {
            "signed_law": "(C C^T)_{ef}=(-3)^(4-rho(e,f))",
            "unsigned_law": "(B B^T)_{ef}=3^(4-rho(e,f))",
            "rho": "line-graph distance between Levi flag-edges, with rho(e,e)=0",
            "signed_values_by_distance": {
                "0": 81,
                "1": -27,
                "2": 9,
                "3": -3,
                "4": 1,
            },
            "unsigned_values_by_distance": {
                "0": 81,
                "1": 27,
                "2": 9,
                "3": 3,
                "4": 1,
            },
            "compressed_reading": "The BT546 3-adic overlap profile is exactly a radial distance kernel on the Levi line graph.",
        },
        "spectral_projector": {
            "line_graph_adjacency_spectrum": spectrum_counter(A),
            "protected_sector": "-2 eigenspace with multiplicity 81",
            "projector_identity": "(1/160) C C^T = E_{-2}(A_X)",
            "integer_polynomial_certificate": "C C^T = 1/2 (A_X-6I)(A_X-2I)(A_X^2-4A_X-2I)",
            "hodge_link": "By BT547 this same -2 eigenspace projector is the Kirchhoff/Hodge cycle-space projector.",
        },
        "profiles": {
            "signed_full_matrix_profile": matrix_profile(CCt, diagonal=True),
            "unsigned_full_matrix_profile": matrix_profile(BBt, diagonal=True),
        },
        "compressed_statement": "The minimal logical signed phase frame, the Hodge cycle projector, and the 3-adic overlap scheme are the same radial kernel on the distance-regular line graph of the W33 Levi graph.",
        "all_identities": checks,
        "all_identities_hold": all(checks.values()),
    }

    out = Path("data/PART_BT548_W33_LEVI_LINE_GRAPH_3ADIC_METRIC_KERNEL_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    print(f"wrote {out}")
    return result


if __name__ == "__main__":
    main()
