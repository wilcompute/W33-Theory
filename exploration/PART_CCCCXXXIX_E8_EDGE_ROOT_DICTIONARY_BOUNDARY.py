#!/usr/bin/env python3
"""
PART CCCCXXXIX -- E8 Edge/Root Dictionary Boundary Witness
===========================================================

This part advances the open item from CCCCXXXVII/CCCCXXXVIII:

  "explicit linear dictionary between W(3,3) edges and E8 roots"

by certifying a precise NO-GO for the naive graph-level dictionary.

We compare:
  - L(W33): line graph of W(3,3), where vertices are the 240 W33 edges
    and adjacency means edge-sharing in W33.
  - E8 root graphs on 240 roots from one-threshold inner products
    (dot = 1, 0, -1 in standard normalization).

Key witness:
  deg(L(W33)) = 22,
  while one-threshold E8 root graphs have degrees 56 or 126.

Therefore no naive one-threshold E8 inner-product graph is isomorphic to
the W33 edge-sharing graph. The explicit dictionary (if it exists) must use
extra structure beyond a single inner-product threshold.
"""

from __future__ import annotations

import json
import sys
from itertools import combinations, product
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from w33_geometry import adjacency_matrix, edge_list, verify_srg


Q = 3
V = 40
K = 12
LAM = 2
MU = 4
EDGES_W33 = V * K // 2


def _build_line_graph_adjacency(edges: List[Tuple[int, int]]) -> np.ndarray:
    m = len(edges)
    line = np.zeros((m, m), dtype=np.int8)
    for i in range(m):
        a, b = edges[i]
        s = {a, b}
        for j in range(i + 1, m):
            c, d = edges[j]
            if s & {c, d}:
                line[i, j] = 1
                line[j, i] = 1
    return line


def _build_e8_roots_doubled() -> List[Tuple[int, ...]]:
    """
    Build E8 roots in doubled coordinates (integers only).

    Original E8 roots have norm 2. In doubled coords every root has norm 8,
    and doubled-dot values are in {-8,-4,0,4,8}.
    """
    roots: List[Tuple[int, ...]] = []

    # Type A: permutations of (±1, ±1, 0,...,0) in original coords.
    # Doubled coords => (±2, ±2, 0,...,0): 112 roots.
    for i, j in combinations(range(8), 2):
        for s1, s2 in product((-2, 2), repeat=2):
            vec = [0] * 8
            vec[i] = s1
            vec[j] = s2
            roots.append(tuple(vec))

    # Type B: (±1/2,...,±1/2) with even minus count in original coords.
    # Doubled coords => (±1,...,±1) with even minus count: 128 roots.
    for signs in product((-1, 1), repeat=8):
        if sum(1 for s in signs if s < 0) % 2 == 0:
            roots.append(tuple(signs))

    # Deduplicate and sanity check.
    roots = sorted(set(roots))
    if len(roots) != 240:
        raise ValueError(f"Expected 240 E8 roots, got {len(roots)}")
    return roots


def _dot(u: Tuple[int, ...], v: Tuple[int, ...]) -> int:
    return int(sum(a * b for a, b in zip(u, v)))


def _adjacency_from_dot(roots: List[Tuple[int, ...]], dot_value: int) -> np.ndarray:
    n = len(roots)
    matrix = np.zeros((n, n), dtype=np.int8)
    for i in range(n):
        for j in range(i + 1, n):
            if _dot(roots[i], roots[j]) == dot_value:
                matrix[i, j] = 1
                matrix[j, i] = 1
    return matrix


def _degree_set(matrix: np.ndarray) -> set[int]:
    return {int(v) for v in matrix.sum(axis=1)}


checks: List[Tuple[str, bool]] = []


def _ck(label: str, ok: bool) -> None:
    checks.append((label, bool(ok)))


def _run() -> Dict[str, object]:
    # --- W33 base ---
    w33 = adjacency_matrix()
    srg = verify_srg(w33)
    w33_edges = list(edge_list(w33))
    line = _build_line_graph_adjacency(w33_edges)
    line_degree_set = _degree_set(line)

    # --- E8 roots ---
    roots = _build_e8_roots_doubled()
    norms = {_dot(r, r) for r in roots}

    # Candidate naive threshold graphs (doubled dots):
    #  4 <=> original dot 1
    #  0 <=> original dot 0
    # -4 <=> original dot -1
    e8_plus = _adjacency_from_dot(roots, 4)
    e8_zero = _adjacency_from_dot(roots, 0)
    e8_minus = _adjacency_from_dot(roots, -4)
    deg_plus = _degree_set(e8_plus)
    deg_zero = _degree_set(e8_zero)
    deg_minus = _degree_set(e8_minus)

    # Dot-distribution packet around a fixed root (index 0)
    sample = roots[0]
    packet: Dict[int, int] = {}
    for r in roots:
        d = _dot(sample, r)
        packet[d] = packet.get(d, 0) + 1

    _ck("W33 SRG verified as (40,12,2,4)", srg["vertices"] == 40 and srg["degree"] == 12)
    _ck("W33 edge count = 240", len(w33_edges) == EDGES_W33 == 240)
    _ck("L(W33) has 240 vertices", line.shape == (240, 240))
    _ck("L(W33) is regular degree 22", line_degree_set == {22})

    _ck("E8 root count = 240", len(roots) == 240)
    _ck("E8 doubled norms all 8", norms == {8})
    _ck("Sample root packet dot=8 occurs once", packet.get(8, 0) == 1)
    _ck("Sample root packet dot=-8 occurs once", packet.get(-8, 0) == 1)
    _ck("Sample root packet dot=4 occurs 56 times", packet.get(4, 0) == 56)
    _ck("Sample root packet dot=-4 occurs 56 times", packet.get(-4, 0) == 56)
    _ck("Sample root packet dot=0 occurs 126 times", packet.get(0, 0) == 126)

    _ck("E8 dot=1 graph degree set is {56}", deg_plus == {56})
    _ck("E8 dot=0 graph degree set is {126}", deg_zero == {126})
    _ck("E8 dot=-1 graph degree set is {56}", deg_minus == {56})

    _ck("No naive one-threshold E8 graph matches L(W33) degree 22", {22}.isdisjoint(deg_plus | deg_zero | deg_minus))

    verified = all(ok for _, ok in checks)
    return {
        "part": "CCCCXXXIX",
        "title": "E8 Edge/Root Dictionary Boundary Witness",
        "Verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(1 for _, ok in checks if ok),
        "checks": checks,
        "w33": {
            "vertices": 40,
            "degree": 12,
            "edges": len(w33_edges),
            "line_graph_vertices": int(line.shape[0]),
            "line_graph_degree_set": sorted(line_degree_set),
        },
        "e8": {
            "roots": len(roots),
            "doubled_norms": sorted(norms),
            "sample_dot_packet": {str(k): v for k, v in sorted(packet.items())},
            "naive_threshold_degree_sets": {
                "dot_plus_one": sorted(deg_plus),
                "dot_zero": sorted(deg_zero),
                "dot_minus_one": sorted(deg_minus),
            },
        },
        "key_observations": [
            "Count equality 240=240 remains exact (W33 edges vs E8 roots).",
            "L(W33) is 22-regular on 240 vertices.",
            "Naive one-threshold E8 root graphs are 56-regular or 126-regular.",
            "Hence no one-threshold E8 inner-product graph can be L(W33).",
            "Any explicit dictionary must include extra structure beyond one-threshold adjacency.",
        ],
        "honesty_boundary": (
            "This part proves a no-go for naive one-threshold graph isomorphisms. "
            "It does not construct the full operator-level edge↔root dictionary."
        ),
    }


def main() -> int:
    results = _run()
    out = ROOT / "PART_CCCCXXXIX_e8_edge_root_dictionary_boundary_results.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print(f"Verified={results['Verified']}  checks={results['checks_passed']}/{results['checks_total']}")
    print()
    print("=== E8 EDGE/ROOT DICTIONARY BOUNDARY ===")
    print("W33: edges=240, line-graph degree=22")
    print("E8 naive threshold degrees: dot=1 -> 56, dot=0 -> 126, dot=-1 -> 56")
    print("Conclusion: no one-threshold root graph matches L(W33).")
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
