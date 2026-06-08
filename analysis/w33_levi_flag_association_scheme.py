#!/usr/bin/env python3
"""BT550: W33 Levi Flag Association-Scheme Theorem.

This continues BT545--BT549.

BT548 showed that the line graph X of the W33 point-line Levi graph is a
6-regular diameter-4 distance-regular graph on the 160 Levi flags, and that

    C C^T = sum_{d=0}^4 (-3)^(4-d) A_d,

where A_d is the distance-d relation matrix in X.

BT549 normalized this kernel into a centered 160-vector tight frame in R^81,
with complementary Kirchhoff cut frame in R^79.

BT550 identifies the complete Bose--Mesner / association-scheme certificate.
The distance matrices A_0,...,A_4 form a 4-class association scheme with
intersection array

    b=[6,3,3,3],  c=[1,1,1,2],  a=[0,2,2,2,4].

The distance polynomials are

    p0=1,
    p1=x,
    p2=x^2-2x-6,
    p3=x^3-4x^2-5x+12,
    p4=(x^4-6x^3+28x-6)/2.

The first eigenmatrix is

    [1, 6,        18,        54,          81]
    [1, 2+sqrt6, 2sqrt6,    6-3sqrt6,   -9]
    [1, 2,       -6,        -6,           9]
    [1, 2-sqrt6,-2sqrt6,    6+3sqrt6,   -9]
    [1,-2,        2,        -2,           1]

with multiplicities

    1,24,30,24,81.

Consequently the signed 3-adic kernel

    K = 81A0 - 27A1 + 9A2 - 3A3 + A4

has eigenvalues

    0,0,0,0,160,

so it is exactly 160 times the primitive idempotent of the -2 eigenspace.
The unsigned kernel

    U = 81A0 + 27A1 + 9A2 + 3A3 + A4

has eigenvalues

    648, 144+36sqrt6, 72, 144-36sqrt6, 40,

recovering the BT546 unsigned overlap spectrum from the same association
scheme.
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
N_FLAGS = 160


def canonical_projective(v: tuple[int, ...]) -> tuple[int, ...]:
    v = tuple(x % MOD for x in v)
    for a in v:
        if a % MOD:
            inv = 1 if a == 1 else 2
            return tuple((x * inv) % MOD for x in v)
    raise ValueError("zero vector")


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


def rounded_spectrum(mat: np.ndarray) -> dict[str, int]:
    vals = np.linalg.eigvalsh(mat.astype(float))
    out: Counter[str] = Counter()
    for x in vals:
        if abs(x) < 1e-8:
            out["0"] += 1
        elif abs(x - 160) < 1e-8:
            out["160"] += 1
        elif abs(x - 648) < 1e-8:
            out["648"] += 1
        elif abs(x - 72) < 1e-8:
            out["72"] += 1
        elif abs(x - 40) < 1e-8:
            out["40"] += 1
        elif abs(x - (144 + 36 * math.sqrt(6))) < 1e-8:
            out["144+36sqrt6"] += 1
        elif abs(x - (144 - 36 * math.sqrt(6))) < 1e-8:
            out["144-36sqrt6"] += 1
        elif abs(x - 6) < 1e-8:
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


def main() -> dict:
    w33, points = build_w33()
    levi, lines = build_levi(w33, points)
    edges = sorted(tuple(sorted(e)) for e in levi.edges())

    # Line graph X on Levi flag-edges.
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

    A = nx.to_numpy_array(X, nodelist=range(N_FLAGS), dtype=int)
    I = np.eye(N_FLAGS, dtype=int)
    distance_matrices = [(distance_matrix == d).astype(int) for d in range(5)]
    A0, A1, A2, A3, A4 = distance_matrices

    # Distance-polynomial certificates.
    A2_poly = A @ A - 2 * A - 6 * I
    A3_poly = A @ A @ A - 4 * A @ A - 5 * A + 12 * I
    A4_poly_num = A @ A @ A @ A - 6 * A @ A @ A + 28 * A - 6 * I
    A4_poly = A4_poly_num // 2

    # Intersection array verification by local profiles.
    intersection_profiles: dict[str, dict[str, int]] = {}
    for d in range(1, 5):
        profile_counter: Counter[str] = Counter()
        for x in range(N_FLAGS):
            for y in range(N_FLAGS):
                if distance_matrix[x, y] != d:
                    continue
                local = Counter(distance_matrix[x, z] for z in X.neighbors(y))
                profile_counter[str(dict(sorted(local.items())))] += 1
        intersection_profiles[str(d)] = dict(profile_counter)

    distance_counts = Counter(distance_matrix[0, j] for j in range(N_FLAGS))
    all_distance_counts = {
        tuple(sorted(Counter(distance_matrix[i, j] for j in range(N_FLAGS)).items()))
        for i in range(N_FLAGS)
    }

    K_signed = 81 * A0 - 27 * A1 + 9 * A2 - 3 * A3 + A4
    U_unsigned = 81 * A0 + 27 * A1 + 9 * A2 + 3 * A3 + A4

    # Exact first eigenmatrix as strings; numerical checks are against spectra of matrices.
    first_eigenmatrix = [
        ["1", "6", "18", "54", "81"],
        ["1", "2+sqrt6", "2sqrt6", "6-3sqrt6", "-9"],
        ["1", "2", "-6", "-6", "9"],
        ["1", "2-sqrt6", "-2sqrt6", "6+3sqrt6", "-9"],
        ["1", "-2", "2", "-2", "1"],
    ]

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
        "distance_matrices_partition_complete_graph": np.array_equal(sum(distance_matrices), np.ones((N_FLAGS, N_FLAGS), dtype=int)),
        "A2_polynomial": np.array_equal(A2, A2_poly),
        "A3_polynomial": np.array_equal(A3, A3_poly),
        "A4_polynomial_even_numerator": bool(np.all(A4_poly_num % 2 == 0)),
        "A4_polynomial": np.array_equal(A4, A4_poly),
        "intersection_array": intersection_profiles == {
            "1": {"{0: 1, 1: 2, 2: 3}": 960},
            "2": {"{1: 1, 2: 2, 3: 3}": 2880},
            "3": {"{2: 1, 3: 2, 4: 3}": 8640},
            "4": {"{3: 2, 4: 4}": 12960},
        },
        "line_graph_spectrum": rounded_spectrum(A) == {
            "6": 1,
            "2+sqrt6": 24,
            "2": 30,
            "2-sqrt6": 24,
            "-2": 81,
        },
        "signed_kernel_spectrum": rounded_spectrum(K_signed) == {"160": 81, "0": 79},
        "unsigned_kernel_spectrum": rounded_spectrum(U_unsigned) == {
            "648": 1,
            "144+36sqrt6": 24,
            "72": 30,
            "144-36sqrt6": 24,
            "40": 81,
        },
        "signed_kernel_idempotent": np.array_equal(K_signed @ K_signed, 160 * K_signed),
    }
    checks = {k: bool(v) for k, v in checks.items()}

    result = {
        "theorem": "BT550 W33 Levi Flag Association-Scheme Theorem",
        "objects": {
            "scheme_vertices_levi_flags": 160,
            "classes": 4,
            "line_graph_degree": 6,
            "diameter": 4,
            "valencies": {"0": 1, "1": 6, "2": 18, "3": 54, "4": 81},
            "multiplicities": {"6": 1, "2+sqrt6": 24, "2": 30, "2-sqrt6": 24, "-2": 81},
        },
        "intersection_array": {
            "b": [6, 3, 3, 3],
            "c": [1, 1, 1, 2],
            "a": [0, 2, 2, 2, 4],
            "local_profiles": intersection_profiles,
        },
        "distance_polynomials": {
            "p0": "1",
            "p1": "x",
            "p2": "x^2 - 2x - 6",
            "p3": "x^3 - 4x^2 - 5x + 12",
            "p4": "(x^4 - 6x^3 + 28x - 6)/2",
            "matrix_identities": {
                "A0": "I",
                "A1": "A",
                "A2": "A^2 - 2A - 6I",
                "A3": "A^3 - 4A^2 - 5A + 12I",
                "A4": "(A^4 - 6A^3 + 28A - 6I)/2",
            },
        },
        "first_eigenmatrix_P": {
            "columns": ["A0", "A1", "A2", "A3", "A4"],
            "rows": ["theta=6", "theta=2+sqrt6", "theta=2", "theta=2-sqrt6", "theta=-2"],
            "matrix": first_eigenmatrix,
        },
        "kernel_diagonalization": {
            "signed_kernel": "K=81A0-27A1+9A2-3A3+A4",
            "signed_eigenvalues_by_P_row": ["0", "0", "0", "0", "160"],
            "signed_reading": "K=160E_{-2}; the protected H1=81 sector is the primitive idempotent for theta=-2.",
            "unsigned_kernel": "U=81A0+27A1+9A2+3A3+A4",
            "unsigned_eigenvalues_by_P_row": ["648", "144+36sqrt6", "72", "144-36sqrt6", "40"],
            "unsigned_reading": "The BT546 unsigned overlap spectrum is the same distance-scheme polynomial with signs removed.",
        },
        "compressed_statement": "The 160 Levi flags form a 4-class distance association scheme whose theta=-2 primitive idempotent is exactly the BT547/BT549 Hodge cycle projector and whose radial polynomials generate both the signed phase frame and unsigned 3-adic overlap kernel.",
        "all_identities": checks,
        "all_identities_hold": all(checks.values()),
    }

    out = Path("data/PART_BT550_W33_LEVI_FLAG_ASSOCIATION_SCHEME_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    print(f"wrote {out}")
    return result


if __name__ == "__main__":
    main()
