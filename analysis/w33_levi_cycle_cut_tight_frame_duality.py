#!/usr/bin/env python3
"""BT549: W33 Levi Cycle/Cut Tight-Frame Duality Theorem.

This continues BT545--BT548.

BT547 identified the signed simple-8-cycle frame projector as the canonical
Hodge/Kirchhoff cycle-space projector of the W33 point-line Levi graph L:

    P_cyc = (1/160) C C^T,
    P_cut = I - P_cyc.

BT548 then identified C C^T as the radial 3-adic kernel on the line graph X of
L:

    (C C^T)_{ef} = (-3)^(4-rho(e,f)),

where rho is the distance between the two Levi flag-edges in X.

BT549 normalizes the complementary projectors into explicit unit-norm tight
frames.  The cycle frame is a 160-vector centered tight frame in R^81 with
inner products

    1, -1/3, 1/9, -1/27, 1/81.

The cut frame is its complementary 160-vector tight frame in R^79 with inner
products

    1, 27/79, -9/79, 3/79, -1/79.

Thus the protected H1=81 sector is not only a projector/eigenspace; it is a
canonical 3-adic spherical code on the 160 Levi flags.  The complementary
Kirchhoff cut sector is the exact dual frame, and the two Gram matrices satisfy

    (81/160) G_cyc + (79/160) G_cut = I_160.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

import networkx as nx
import numpy as np

MOD = 3
POINTS_PER_LINE = 4
N_FLAGS = 160


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


def fracstr(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def profile_by_distance(values_by_distance: dict[int, Fraction], counts_by_distance: dict[int, int]) -> dict[str, int]:
    out: dict[str, int] = {}
    for d, count in sorted(counts_by_distance.items()):
        out[fracstr(values_by_distance[d])] = count
    return out


def main() -> dict:
    w33, points = build_w33()
    levi, lines = build_levi(w33, points)
    edges = sorted(tuple(sorted(e)) for e in levi.edges())

    # Line graph X of the Levi graph L, with vertices indexed by Levi flag-edges.
    X = nx.Graph()
    X.add_nodes_from(range(len(edges)))
    for i, a in enumerate(edges):
        sa = set(a)
        for j, b in enumerate(edges[i + 1 :], start=i + 1):
            if sa & set(b):
                X.add_edge(i, j)

    dist = dict(nx.all_pairs_shortest_path_length(X))
    distance_matrix = np.zeros((N_FLAGS, N_FLAGS), dtype=int)
    for i in range(N_FLAGS):
        for j in range(N_FLAGS):
            distance_matrix[i, j] = dist[i][j]

    distance_counts = Counter(distance_matrix[0, j] for j in range(N_FLAGS))
    all_distance_counts = {
        tuple(sorted(Counter(distance_matrix[i, j] for j in range(N_FLAGS)).items()))
        for i in range(N_FLAGS)
    }

    # BT548 signed radial kernel K = C C^T.
    K = np.zeros((N_FLAGS, N_FLAGS), dtype=int)
    for i in range(N_FLAGS):
        for j in range(N_FLAGS):
            rho = int(distance_matrix[i, j])
            K[i, j] = (-3) ** (4 - rho)

    I = np.eye(N_FLAGS, dtype=int)
    H = 160 * I - K  # 160 * P_cut, complementary to K = 160 * P_cyc.

    # Integer projector checks.
    K2 = K @ K
    H2 = H @ H

    # Exact frame data.  G_cyc=K/81 and G_cut=H/79 are unit-diagonal Gram matrices.
    cycle_inner_by_distance = {d: Fraction(((-3) ** (4 - d)), 81) for d in range(5)}
    cut_inner_by_distance = {0: Fraction(1, 1)}
    for d in range(1, 5):
        cut_inner_by_distance[d] = Fraction(-((-3) ** (4 - d)), 79)

    cycle_squared_distance_by_distance = {
        d: 2 * (Fraction(1, 1) - cycle_inner_by_distance[d]) for d in range(5)
    }
    cut_squared_distance_by_distance = {
        d: 2 * (Fraction(1, 1) - cut_inner_by_distance[d]) for d in range(5)
    }

    cycle_row_sum = sum(distance_counts[d] * cycle_inner_by_distance[d] for d in range(5))
    cut_row_sum = sum(distance_counts[d] * cut_inner_by_distance[d] for d in range(5))
    cycle_row_square_sum = sum(distance_counts[d] * cycle_inner_by_distance[d] ** 2 for d in range(5))
    cut_row_square_sum = sum(distance_counts[d] * cut_inner_by_distance[d] ** 2 for d in range(5))

    # Full frame potentials are sums of squared Gram entries.
    cycle_frame_potential = N_FLAGS * cycle_row_square_sum
    cut_frame_potential = N_FLAGS * cut_row_square_sum

    checks = {
        "w33_srg_size": w33.number_of_nodes() == 40 and w33.number_of_edges() == 240,
        "w33_lines_40": len(lines) == 40,
        "levi_size": levi.number_of_nodes() == 80 and levi.number_of_edges() == 160,
        "levi_regular_4": set(dict(levi.degree()).values()) == {4},
        "line_graph_size": X.number_of_nodes() == 160 and X.number_of_edges() == 480,
        "line_graph_regular_6": set(dict(X.degree()).values()) == {6},
        "line_graph_diameter_4": nx.diameter(X) == 4,
        "distance_distribution_uniform": len(all_distance_counts) == 1
        and dict(distance_counts) == {0: 1, 1: 6, 2: 18, 3: 54, 4: 81},
        "cycle_projector_integer_idempotent": np.array_equal(K2, 160 * K),
        "cut_projector_integer_idempotent": np.array_equal(H2, 160 * H),
        "cycle_cut_complement": np.array_equal(K + H, 160 * I),
        "cycle_rank_81": np.linalg.matrix_rank(K) == 81,
        "cut_rank_79": np.linalg.matrix_rank(H) == 79,
        "cycle_unit_diagonal": set(np.diag(K)) == {81},
        "cut_unit_diagonal": set(np.diag(H)) == {79},
        "cycle_centered": cycle_row_sum == 0 and set(K.sum(axis=1)) == {0},
        "cut_row_sum": cut_row_sum == Fraction(160, 79) and set(H.sum(axis=1)) == {160},
        "cycle_welch_equality": cycle_frame_potential == Fraction(N_FLAGS * N_FLAGS, 81),
        "cut_welch_equality": cut_frame_potential == Fraction(N_FLAGS * N_FLAGS, 79),
        "cycle_row_square_sum": cycle_row_square_sum == Fraction(160, 81),
        "cut_row_square_sum": cut_row_square_sum == Fraction(160, 79),
    }
    checks = {k: bool(v) for k, v in checks.items()}

    result = {
        "theorem": "BT549 W33 Levi Cycle/Cut Tight-Frame Duality Theorem",
        "objects": {
            "levi_flags": 160,
            "cycle_projector_rank": 81,
            "cut_projector_rank": 79,
            "line_graph_degree": 6,
            "line_graph_diameter": 4,
            "distance_distribution_per_flag": {str(k): int(v) for k, v in sorted(distance_counts.items())},
        },
        "projector_pair": {
            "cycle_integer_kernel": "K = C C^T = 160 P_cyc",
            "cut_integer_kernel": "H = 160I - K = 160 P_cut",
            "idempotents": ["K^2 = 160K", "H^2 = 160H", "K+H=160I"],
            "normalized_grams": ["G_cyc=K/81", "G_cut=H/79"],
            "weighted_complement_identity": "(81/160)G_cyc + (79/160)G_cut = I_160",
        },
        "cycle_tight_frame_R81": {
            "dimension": 81,
            "number_of_vectors": 160,
            "frame_bound": "160/81",
            "is_centered": True,
            "row_sum": fracstr(cycle_row_sum),
            "row_square_sum": fracstr(cycle_row_square_sum),
            "frame_potential": fracstr(cycle_frame_potential),
            "welch_bound": "160^2/81",
            "inner_products_by_line_graph_distance": {
                str(d): fracstr(cycle_inner_by_distance[d]) for d in range(5)
            },
            "per_vector_inner_product_profile": profile_by_distance(cycle_inner_by_distance, dict(distance_counts)),
            "squared_distances_by_line_graph_distance": {
                str(d): fracstr(cycle_squared_distance_by_distance[d]) for d in range(5)
            },
            "reading": "The protected H1=81 sector is a centered 160-vector unit-norm tight frame with 3-adic inner products (-1/3)^rho.",
        },
        "cut_tight_frame_R79": {
            "dimension": 79,
            "number_of_vectors": 160,
            "frame_bound": "160/79",
            "is_centered": False,
            "row_sum": fracstr(cut_row_sum),
            "row_square_sum": fracstr(cut_row_square_sum),
            "frame_potential": fracstr(cut_frame_potential),
            "welch_bound": "160^2/79",
            "inner_products_by_line_graph_distance": {
                str(d): fracstr(cut_inner_by_distance[d]) for d in range(5)
            },
            "per_vector_inner_product_profile": profile_by_distance(cut_inner_by_distance, dict(distance_counts)),
            "squared_distances_by_line_graph_distance": {
                str(d): fracstr(cut_squared_distance_by_distance[d]) for d in range(5)
            },
            "reading": "The Kirchhoff cut sector is the complementary 79-dimensional tight frame; it contains the all-ones direction.",
        },
        "compressed_statement": "The W33 Levi 160 flag edges carry two exact complementary unit-norm tight frames: a centered 81-dimensional 3-adic cycle frame and a 79-dimensional Kirchhoff cut frame, with weighted Gram sum equal to the identity.",
        "all_identities": checks,
        "all_identities_hold": all(checks.values()),
    }

    out = Path("data/PART_BT549_W33_LEVI_CYCLE_CUT_TIGHT_FRAME_DUALITY_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    print(f"wrote {out}")
    return result


if __name__ == "__main__":
    main()
