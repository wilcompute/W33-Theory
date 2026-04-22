"""Exact qutrit foundation of W(3,3): Pauli geometry, Heisenberg shell, and H_can.

This bridge compresses the exact finite-qutrit core already scattered across
the repo into one theorem package:

1. W(3,3) is exactly the commutation graph of the 40 projective non-identity
   two-qutrit Pauli observables.
2. Around every base vertex, the 12 neighbors split into four triangles, and
   the 27 non-neighbors split into nine fibers of size 3 with uniform
   inter-fiber coupling 3. This is the finite Heisenberg/MUB shell.
3. The 40 totally isotropic lines of W(3,3) give a 40x40 point-line incidence
   matrix B satisfying

       B B^T = A + 4 I,
       H_can := 12 I - A = 16 I - B B^T,

   so H_can is positive semidefinite with spectrum 0^1, 10^24, 16^15.

The point is not novelty of the raw ingredients; it is exact closure of the
latest paper's qutrit foundation in one self-contained, reproducible bridge.
"""

from __future__ import annotations

import json
from itertools import product
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_qutrit_foundation_bridge_summary.json"

SCRIPTS = ROOT / "scripts"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_homology import build_w33
from w33_two_qutrit_pauli import (
    build_commutation_graph,
    build_pauli_operators,
    find_isomorphism,
    symplectic_form,
    verify_commutation,
)


J = np.array(
    [[0, 1, 0, 0], [2, 0, 0, 0], [0, 0, 0, 1], [0, 0, 2, 0]],
    dtype=int,
)


def _local_shell(v0: int, adj_s: list[set[int]], n: int) -> dict[str, Any]:
    n12 = sorted(adj_s[v0])
    h27 = [v for v in range(n) if v != v0 and v not in adj_s[v0]]

    visited: set[int] = set()
    triangles: list[list[int]] = []
    for u in n12:
        if u in visited:
            continue
        comp = {u}
        queue = [u]
        while queue:
            cur = queue.pop(0)
            for w in n12:
                if w not in comp and w in adj_s[cur]:
                    comp.add(w)
                    queue.append(w)
        triangles.append(sorted(comp))
        visited.update(comp)

    t0, t1 = triangles[0], triangles[1]
    x_slices = {xi: set(v for v in h27 if v in adj_s[u]) for xi, u in enumerate(t0)}
    y_slices = {yi: set(v for v in h27 if v in adj_s[u]) for yi, u in enumerate(t1)}

    fibers: dict[tuple[int, int], list[int]] = {}
    for x in range(3):
        for y in range(3):
            fibers[(x, y)] = sorted(x_slices[x] & y_slices[y])

    inter_fiber_counts = []
    items = list(fibers.items())
    for i, (_, fa) in enumerate(items):
        for j, (_, fb) in enumerate(items):
            if j <= i:
                continue
            c = sum(1 for u in fa for v in fb if v in adj_s[u])
            inter_fiber_counts.append(c)

    tri_count = 0
    for u in h27:
        for v in h27:
            if v <= u or v not in adj_s[u]:
                continue
            for w in h27:
                if w <= v or w not in adj_s[u] or w not in adj_s[v]:
                    continue
                tri_count += 1

    return {
        "base_vertex": v0,
        "N12_size": len(n12),
        "H27_size": len(h27),
        "triangle_sizes": [len(t) for t in triangles],
        "fiber_sizes": sorted(len(f) for f in fibers.values()),
        "inter_fiber_counts": sorted(set(inter_fiber_counts)),
        "h27_triangle_count": tri_count,
    }


def _canonical_line(u: np.ndarray, v: np.ndarray) -> tuple[tuple[int, int, int, int], ...]:
    members = []
    for a, b in product(range(3), repeat=2):
        if a == 0 and b == 0:
            continue
        w = (a * u + b * v) % 3
        for k in range(4):
            if w[k] != 0:
                if w[k] == 2:
                    w = (2 * w) % 3
                members.append(tuple(int(x) for x in w.tolist()))
                break
    return tuple(sorted(set(members)))


def _build_isotropic_lines(vertices: list[tuple[int, int, int, int]]) -> list[tuple[tuple[int, int, int, int], ...]]:
    lines = set()
    for i, u in enumerate(vertices):
        u_arr = np.array(u, dtype=int)
        for j in range(i + 1, len(vertices)):
            v_arr = np.array(vertices[j], dtype=int)
            if symplectic_form(u, tuple(v_arr.tolist())) != 0:
                continue
            lines.add(_canonical_line(u_arr, v_arr))
    return sorted(lines)


def _incidence_and_operator(vertices: list[tuple[int, int, int, int]], adj: list[list[int]]) -> dict[str, Any]:
    lines = _build_isotropic_lines(vertices)
    idx = {p: i for i, p in enumerate(vertices)}
    n = len(vertices)
    b = np.zeros((n, len(lines)), dtype=int)
    a = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in adj[i]:
            a[i, j] = 1
    for j, line in enumerate(lines):
        for p in line:
            b[idx[p], j] = 1

    bbt = b @ b.T
    h_can = 12 * np.eye(n, dtype=int) - a
    vals = np.linalg.eigvalsh(h_can.astype(float)).round(8)
    uniq, counts = np.unique(vals, return_counts=True)
    spectrum = {str(int(round(e))): int(c) for e, c in zip(uniq, counts)}

    return {
        "line_count": len(lines),
        "line_sizes": sorted({len(line) for line in lines}),
        "rank_B": int(np.linalg.matrix_rank(b)),
        "bbt_equals_a_plus_4i": bool(np.array_equal(bbt, a + 4 * np.eye(n, dtype=int))),
        "h_can_equals_16i_minus_bbt": bool(np.array_equal(h_can, 16 * np.eye(n, dtype=int) - bbt)),
        "h_can_spectrum": spectrum,
    }


def build_summary() -> dict[str, Any]:
    n, vertices_raw, adj, edges = build_w33()
    vertices = [tuple(int(x) for x in v) for v in vertices_raw]
    adj_s = [set(adj[i]) for i in range(n)]

    reps, matrices = build_pauli_operators()
    checked, matched = verify_commutation(reps, matrices)
    pauli_adj = build_commutation_graph(reps)
    identity_iso, mismatches = find_isomorphism(reps, pauli_adj)

    shell_rows = [_local_shell(v0, adj_s, n) for v0 in range(n)]
    incidence = _incidence_and_operator(vertices, adj)

    theorem = {
        "the_40_projective_two_qutrit_pauli_observables_realise_w33_exactly": (
            len(reps) == 40 and checked == matched and identity_iso and mismatches == 0
        ),
        "every_vertex_has_the_exact_local_qutrit_shell_12_27_4triangles_9fibers": (
            all(
                row["N12_size"] == 12
                and row["H27_size"] == 27
                and row["triangle_sizes"] == [3, 3, 3, 3]
                and row["fiber_sizes"] == [3] * 9
                for row in shell_rows
            )
        ),
        "every_pair_of_distinct_fibers_has_exactly_3_edges_between_them": (
            all(row["inter_fiber_counts"] == [3] for row in shell_rows)
        ),
        "every_h27_shell_contains_exactly_36_internal_triangles": (
            all(row["h27_triangle_count"] == 36 for row in shell_rows)
        ),
        "w33_has_exactly_40_totally_isotropic_lines_of_size_4": (
            incidence["line_count"] == 40 and incidence["line_sizes"] == [4]
        ),
        "the_point_line_incidence_operator_satisfies_bbt_equals_a_plus_4i": (
            incidence["bbt_equals_a_plus_4i"]
        ),
        "the_canonical_quadratic_operator_is_hcan_equals_12i_minus_a_equals_16i_minus_bbt": (
            incidence["h_can_equals_16i_minus_bbt"]
        ),
        "the_canonical_quadratic_operator_has_spectrum_0_1_10_24_16_15": (
            incidence["h_can_spectrum"] == {"0": 1, "10": 24, "16": 15}
        ),
    }
    theorem["the_qutrit_foundation_bridge_is_fully_closed"] = all(theorem.values())

    return {
        "qutrit_foundation_dictionary": {
            "n_vertices": n,
            "n_edges": len(edges),
            "pauli_commutation_checks": checked,
            "local_shell_rows": shell_rows,
            "incidence": incidence,
        },
        "qutrit_foundation_theorem": theorem,
        "interpretation": (
            "The latest paper's qutrit foundation is now closed computationally "
            "in one place: W(3,3) is exactly the two-qutrit Pauli commutation "
            "geometry, every local shell is the 12+27 Heisenberg/MUB package, "
            "and the point-line incidence operator produces the canonical "
            "quadratic Hamiltonian with spectrum 0,10,16."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 QUTRIT FOUNDATION BRIDGE")
    print("=" * 72)
    for key, value in summary["qutrit_foundation_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
