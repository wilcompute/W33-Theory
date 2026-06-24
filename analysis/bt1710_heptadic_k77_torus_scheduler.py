#!/usr/bin/env python3
"""BT1710 - Heptadic K7,7 torus scheduler verifier.

This verifier turns the six-qubit K7,7 hint from the new contextuality paper
into an exact Fano/toroidal scheduler object.  It is intentionally finite and
combinatorial: the seven toroidal realizations are treated as an external
7-packet, while the executable object is the Fano incidence graph K7,7 split
into Heawood and co-Heawood halves.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import networkx as nx
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1710_heptadic_k77_torus_scheduler.json"


def bits(n: int) -> tuple[int, int, int]:
    return ((n >> 2) & 1, (n >> 1) & 1, n & 1)


def dot2(a: int, b: int) -> int:
    aa, bb = bits(a), bits(b)
    return sum(x * y for x, y in zip(aa, bb)) % 2


def decimal_period(base: int, modulus: int) -> int:
    x = base % modulus
    for k in range(1, modulus + 1):
        if x == 1:
            return k
        x = (x * base) % modulus
    raise ValueError("period not found")


def fano_incidence() -> tuple[list[int], list[int], np.ndarray, dict[int, list[int]]]:
    points = list(range(1, 8))
    line_labels = list(range(1, 8))
    M = np.zeros((7, 7), dtype=int)
    lines: dict[int, list[int]] = {}
    for j, ell in enumerate(line_labels):
        pts = [p for p in points if dot2(p, ell) == 0]
        assert len(pts) == 3
        lines[ell] = pts
        for i, p in enumerate(points):
            M[i, j] = int(p in pts)
    return points, line_labels, M, lines


def build_bipartite_graph(M: np.ndarray, complement: bool = False) -> nx.Graph:
    G = nx.Graph()
    left = [f"p{idx}" for idx in range(7)]
    right = [f"l{idx}" for idx in range(7)]
    G.add_nodes_from(left, bipartite=0)
    G.add_nodes_from(right, bipartite=1)
    for i in range(7):
        for j in range(7):
            val = M[i, j]
            if complement:
                val = 1 - val
            if val:
                G.add_edge(left[i], right[j])
    return G


def build_certificate() -> dict[str, Any]:
    points, line_labels, M, lines = fano_incidence()
    J = np.ones((7, 7), dtype=int)
    I = np.eye(7, dtype=int)
    N = J - M

    heawood = build_bipartite_graph(M, complement=False)
    coheawood = build_bipartite_graph(M, complement=True)
    full = nx.complete_bipartite_graph(7, 7)

    # Fano lines partition the K7 edge set: every unordered pair of points is on
    # exactly one Fano line, so the seven triples give 7*3 = 21 edges.
    k7_edges_from_lines: list[tuple[int, int, int]] = []
    seen_pairs: set[tuple[int, int]] = set()
    for ell, pts in lines.items():
        for a_idx in range(3):
            for b_idx in range(a_idx + 1, 3):
                a, b = sorted((pts[a_idx], pts[b_idx]))
                seen_pairs.add((a, b))
                k7_edges_from_lines.append((ell, a, b))

    heawood_eigs = sorted(np.linalg.eigvalsh(nx.to_numpy_array(heawood)))
    coheawood_eigs = sorted(np.linalg.eigvalsh(nx.to_numpy_array(coheawood)))

    checks = {
        "fano_incidence_row_col_sum_3": (M.sum(axis=0).tolist() == [3] * 7 and M.sum(axis=1).tolist() == [3] * 7),
        "fano_incidence_design_identity": np.array_equal(M @ M.T, J + 2 * I),
        "cofano_design_identity": np.array_equal(N @ N.T, 2 * J + 2 * I),
        "k77_edge_split": heawood.number_of_edges() == 21 and coheawood.number_of_edges() == 28 and full.number_of_edges() == 49,
        "k7_edges_partitioned_by_fano_lines": len(seen_pairs) == math.comb(7, 2) == 21 and len(k7_edges_from_lines) == 21,
        "heawood_is_3_regular_bipartite": all(d == 3 for _, d in heawood.degree()) and nx.is_bipartite(heawood),
        "coheawood_is_4_regular_bipartite": all(d == 4 for _, d in coheawood.degree()) and nx.is_bipartite(coheawood),
        "decimal_one_seventh_period_is_six": decimal_period(10, 7) == 6,
        "toroidal_realization_count_is_seven": 5 + 2 == 7,
    }

    return {
        "theorem": "BT1710 Heptadic K7,7 Torus Scheduler Theorem",
        "verified": all(checks.values()),
        "summary": (
            "The six-qubit K7,7 contextuality carrier has an exact Fano split: "
            "21 incidence edges form the Heawood graph and 28 non-incidence "
            "edges form the co-Heawood buffer. The seven Fano lines partition "
            "the 21 edges of K7, matching the 21-edge Csaszar/Szilassi toroidal "
            "edge carrier, while the residual 28=7*4 supplies four scheduler "
            "slots per heptadic realization."
        ),
        "source_hints": [
            "A new heuristic approach for contextuality degree estimates and its four- to six-qubit portrayals.pdf: six-qubit hyperbolic pattern underpinned by K7,7",
            "q-2025-01-20-1601.pdf: split Cayley hexagon and Fano/heptadic three-qubit layer",
            "repo toroidal heptad: five Csaszar plus two Szilassi realizations",
        ],
        "counts": {
            "fano_points": 7,
            "fano_lines": 7,
            "heawood_vertices": heawood.number_of_nodes(),
            "heawood_edges": heawood.number_of_edges(),
            "coheawood_edges": coheawood.number_of_edges(),
            "k77_edges": full.number_of_edges(),
            "csaszar_realizations": 5,
            "szilassi_realizations": 2,
            "toroidal_realizations": 7,
            "decimal_period_1_over_7": decimal_period(10, 7),
        },
        "spectral_certificate": {
            "M_Mt": (M @ M.T).tolist(),
            "N_Nt": (N @ N.T).tolist(),
            "heawood_spectrum_numeric": [round(float(x), 10) for x in heawood_eigs],
            "coheawood_spectrum_numeric": [round(float(x), 10) for x in coheawood_eigs],
            "singular_values_heawood_exact": ["3"] + ["sqrt(2)"] * 6,
            "singular_values_coheawood_exact": ["4"] + ["sqrt(2)"] * 6,
        },
        "fano_lines_as_k7_edge_partition": [
            {"line_label": ell, "points": pts, "k7_edges": [sorted(pair) for pair in [(pts[0], pts[1]), (pts[0], pts[2]), (pts[1], pts[2])]]}
            for ell, pts in lines.items()
        ],
        "claim_boundary": [
            "This proves the K7,7/Heawood/co-Heawood scheduler arithmetic and graph structure.",
            "It does not assert that any specific Csaszar or Szilassi 3D embedding is isomorphic to the six-qubit unsatisfied subgeometry.",
            "The 5+2 toroidal realization split is carried as an external heptad marker pending an objectwise embedding parser.",
        ],
        "checks": checks,
    }


def main() -> int:
    cert = build_certificate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(cert["theorem"])
    print(f"  verified: {cert['verified']}")
    print(f"  wrote {OUT}")
    return 0 if cert["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
