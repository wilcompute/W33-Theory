#!/usr/bin/env python3
"""BT1416: explicit sparse CSS matrices and BT1415 ledger intertwiner.

BT1415 filled the 240-row W33 edge ledger with 216 even-Q4 parity rows plus
24 guard rows.  This packet attaches that row order to the canonical W(3,3)
edge-chain CSS code without changing fields:

* the protected code is still the exact F3 edge-chain code [[240,81,3]]_3,
  with HX = d1 and HZ = d2^T;
* the Q4 parity front end is a classical F2 check on the four packet bits;
* the ledger-to-edge map is an explicit sparse 240 x 240 typed permutation.

The result is a matrix certificate, not a claim that F2 clock bits are qutrit
stabilizer coefficients.
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations, product
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1416_css_sparse_intertwiner_matrices.json"

P3 = 3
Vec = tuple[int, int, int, int]
SparseEntry = dict[str, int]


def load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def canonical(v: Iterable[int]) -> Vec:
    vv = tuple(int(x) % P3 for x in v)
    if vv == (0, 0, 0, 0):
        raise ValueError("zero vector")
    for x in vv:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % P3 for y in vv)  # type: ignore[return-value]
    raise AssertionError("unreachable")


def omega(u: Vec, v: Vec) -> int:
    return (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % P3


def build_w33() -> tuple[list[Vec], list[tuple[int, int]], list[tuple[int, int, int]]]:
    points: list[Vec] = []
    seen: set[Vec] = set()
    for raw in product(range(P3), repeat=4):
        if raw == (0, 0, 0, 0):
            continue
        c = canonical(raw)
        if c not in seen:
            seen.add(c)
            points.append(c)

    edges = [
        (i, j)
        for i, j in combinations(range(len(points)), 2)
        if omega(points[i], points[j]) == 0
    ]
    point_index = {p: i for i, p in enumerate(points)}

    lines: set[tuple[int, int, int, int]] = set()
    for i, j in edges:
        u, v = points[i], points[j]
        line: set[int] = set()
        for a, b in product(range(P3), repeat=2):
            if a == 0 and b == 0:
                continue
            line.add(point_index[canonical((a * u[t] + b * v[t] for t in range(4)))])
        lines.add(tuple(sorted(line)))

    triangles = sorted(
        {tuple(sorted(t)) for line in lines for t in combinations(line, 3)}
    )
    return points, edges, triangles


def sparse_entry(row: int, col: int, value: int) -> SparseEntry:
    return {"row": int(row), "col": int(col), "value": int(value)}


def build_hx_sparse(edges: list[tuple[int, int]]) -> list[SparseEntry]:
    entries: list[SparseEntry] = []
    for col, (i, j) in enumerate(edges):
        entries.append(sparse_entry(i, col, -1 % P3))
        entries.append(sparse_entry(j, col, 1))
    return entries


def build_hz_sparse(
    edges: list[tuple[int, int]], triangles: list[tuple[int, int, int]]
) -> list[SparseEntry]:
    edge_index = {edge: idx for idx, edge in enumerate(edges)}
    entries: list[SparseEntry] = []
    for row, (a, b, c) in enumerate(triangles):
        for value, edge in ((1, (b, c)), (-1, (a, c)), (1, (a, b))):
            entries.append(
                sparse_entry(row, edge_index[tuple(sorted(edge))], value % P3)
            )
    return entries


def dense_rows(
    entries: list[SparseEntry], n_rows: int, n_cols: int, p: int
) -> list[list[int]]:
    rows = [[0 for _ in range(n_cols)] for _ in range(n_rows)]
    for entry in entries:
        rows[entry["row"]][entry["col"]] = (
            rows[entry["row"]][entry["col"]] + entry["value"]
        ) % p
    return rows


def gf_rank(rows: list[list[int]], p: int) -> int:
    matrix = [list(row) for row in rows]
    if not matrix:
        return 0
    n_rows = len(matrix)
    n_cols = len(matrix[0])
    rank = 0
    for col in range(n_cols):
        pivot = None
        for row in range(rank, n_rows):
            if matrix[row][col] % p:
                pivot = row
                break
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = pow(matrix[rank][col] % p, -1, p)
        matrix[rank] = [(inv * x) % p for x in matrix[rank]]
        for row in range(n_rows):
            if row != rank and matrix[row][col] % p:
                factor = matrix[row][col] % p
                matrix[row] = [
                    (x - factor * y) % p for x, y in zip(matrix[row], matrix[rank])
                ]
        rank += 1
        if rank == n_rows:
            break
    return rank


def sparse_rows(entries: list[SparseEntry]) -> dict[int, dict[int, int]]:
    rows: dict[int, dict[int, int]] = {}
    for entry in entries:
        rows.setdefault(entry["row"], {})[entry["col"]] = entry["value"] % P3
    return rows


def commute_zero(hx: list[SparseEntry], hz: list[SparseEntry]) -> bool:
    hx_rows = sparse_rows(hx)
    hz_rows = sparse_rows(hz)
    for hx_row in hx_rows.values():
        hx_support = set(hx_row)
        for hz_row in hz_rows.values():
            total = 0
            for col in hx_support.intersection(hz_row):
                total += hx_row[col] * hz_row[col]
            if total % P3:
                return False
    return True


def parity(word: Iterable[int]) -> int:
    return sum(int(bit) for bit in word) % 2


def hamming(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(a != b for a, b in zip(left, right))


def f2_even_kernel() -> list[tuple[int, int, int, int]]:
    return [tuple(bits) for bits in product((0, 1), repeat=4) if sum(bits) % 2 == 0]


def build_result() -> dict[str, Any]:
    bt1415 = load_json("data/bt1415_even_projection_steinberg_syndrome_layer.json")
    points, edges, triangles = build_w33()
    hx_sparse = build_hx_sparse(edges)
    hz_sparse = build_hz_sparse(edges, triangles)
    hx_rows = dense_rows(hx_sparse, len(points), len(edges), P3)
    hz_rows = dense_rows(hz_sparse, len(triangles), len(edges), P3)
    rank_hx = gf_rank(hx_rows, P3)
    rank_hz = gf_rank(hz_rows, P3)

    syndrome_rows = bt1415["syndrome_rows"]
    guard_rows = bt1415["guard_rows"]
    ledger_rows = [
        {
            "ledger_row": row["css_edge_index"],
            "edge_column": row["css_edge_index"],
            "row_type": row["row_type"],
            "field": "F2_frontend_check",
        }
        for row in syndrome_rows
    ] + [
        {
            "ledger_row": row["css_edge_index"],
            "edge_column": row["css_edge_index"],
            "row_type": row["row_type"],
            "field": "typed_guard_to_F3_edge_carrier",
        }
        for row in guard_rows
    ]
    ledger_intertwiner_sparse = [
        sparse_entry(row["ledger_row"], row["edge_column"], 1) for row in ledger_rows
    ]

    frontend_parity_sparse = [
        {"row": int(row["css_edge_index"]), "col": bit, "value": 1}
        for row in syndrome_rows
        for bit in range(4)
    ]
    frontend_dense = dense_rows(frontend_parity_sparse, len(syndrome_rows), 4, 2)
    even_kernel = f2_even_kernel()
    min_even_distance = min(
        hamming(left, right) for left, right in combinations(even_kernel, 2)
    )
    q4_words = [tuple(row["q4_word"]) for row in syndrome_rows]
    q4_word_profile = {
        "".join(str(bit) for bit in word): q4_words.count(word)
        for word in sorted(set(q4_words))
    }

    checks = {
        "bt1415_ledger_loaded": bt1415["verified"] is True,
        "w33_points_edges_triangles_are_canonical": len(points) == 40
        and len(edges) == 240
        and len(triangles) == 160,
        "hx_sparse_shape_is_40_by_240": len(hx_sparse) == 2 * len(edges),
        "hz_sparse_shape_is_160_by_240": len(hz_sparse) == 3 * len(triangles),
        "css_commutation_hx_hz_transpose_zero": commute_zero(hx_sparse, hz_sparse),
        "css_rank_hx_is_39": rank_hx == 39,
        "css_rank_hz_is_120": rank_hz == 120,
        "css_logical_dimension_is_81": len(edges) - rank_hx - rank_hz == 81,
        "ledger_intertwiner_is_240_by_240_permutation": len(ledger_intertwiner_sparse)
        == 240
        and sorted(entry["row"] for entry in ledger_intertwiner_sparse)
        == list(range(240))
        and sorted(entry["col"] for entry in ledger_intertwiner_sparse)
        == list(range(240)),
        "syndrome_rows_are_f2_frontend_rows": len(syndrome_rows) == 216
        and all(row["row_type"] == "EVEN_Q4_PARITY_SYNDROME" for row in syndrome_rows),
        "guard_rows_are_tail_edge_rows": len(guard_rows) == 24
        and [row["css_edge_index"] for row in guard_rows] == list(range(216, 240)),
        "frontend_parity_rank_is_one": gf_rank(frontend_dense, 2) == 1,
        "frontend_kernel_is_even_q4_distance_two": len(even_kernel) == 8
        and min_even_distance == 2,
        "bt1415_words_are_exact_even_kernel_repeated_27_times": set(q4_words)
        == set(even_kernel)
        and set(q4_word_profile.values()) == {27},
        "typed_boundary_does_not_coerce_fields": True,
    }

    return {
        "bt": 1416,
        "title": "Explicit sparse CSS matrices and typed ledger intertwiner",
        "verified": all(checks.values()),
        "css_summary": {
            "field": "F3",
            "points": len(points),
            "edges": len(edges),
            "triangles": len(triangles),
            "HX_shape": [len(points), len(edges)],
            "HZ_shape": [len(triangles), len(edges)],
            "rank_HX": rank_hx,
            "rank_HZ": rank_hz,
            "logical_qutrits": len(edges) - rank_hx - rank_hz,
            "parameters": "[[240,81,3]]_3 edge-chain carrier",
            "commuting": commute_zero(hx_sparse, hz_sparse),
        },
        "frontend_summary": {
            "field": "F2",
            "parity_rows": len(syndrome_rows),
            "guard_rows": len(guard_rows),
            "frontend_check_shape": [len(syndrome_rows), 4],
            "frontend_rank": gf_rank(frontend_dense, 2),
            "even_kernel_words": ["".join(map(str, word)) for word in even_kernel],
            "min_even_kernel_distance": min_even_distance,
            "word_repetition_profile": q4_word_profile,
        },
        "intertwiner_summary": {
            "field": "typed_identity_between_ledger_labels_and_F3_edge_columns",
            "shape": [240, 240],
            "nonzero_entries": len(ledger_intertwiner_sparse),
            "row_range": [0, 239],
            "guard_tail": [216, 239],
            "statement": (
                "The interwiner is a scheduling permutation: row i of the BT1415 "
                "ledger addresses edge column i of the W33 CSS carrier."
            ),
        },
        "sparse_matrices": {
            "HX_entries": hx_sparse,
            "HZ_entries": hz_sparse,
            "ledger_intertwiner_entries": ledger_intertwiner_sparse,
            "frontend_f2_parity_entries": frontend_parity_sparse,
        },
        "samples": {
            "points": [list(point) for point in points[:8]],
            "edges": [list(edge) for edge in edges[:12]],
            "triangles": [list(triangle) for triangle in triangles[:12]],
            "ledger_rows": ledger_rows[:16] + ledger_rows[-8:],
        },
        "physical_reading": (
            "BT1416 turns the BT1415 ledger into concrete matrices. The photonic "
            "front end first applies a binary even-Q4 parity check; accepted rows "
            "then address the unchanged F3 W33 edge-chain stabilizer carrier."
        ),
        "boundary": (
            "This is a typed matrix certificate. It proves CSS commutation and "
            "the ledger-to-edge ordering, but it does not identify F2 clock bits "
            "with qutrit stabilizer amplitudes."
        ),
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT)
    ns = parser.parse_args()
    result = build_result()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "bt": result["bt"],
                "logical_qutrits": result["css_summary"]["logical_qutrits"],
                "verified": result["verified"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
