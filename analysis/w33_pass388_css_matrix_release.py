#!/usr/bin/env python3
"""Pass 388: release-lock the canonical 240-edge qutrit CSS matrices.

This script emits the actual GF(3) stabilizer matrices in Matrix Market
coordinate format:

    HX = d1       : 40 x 240
    HZ = d2^T     : 160 x 240

where the 160 faces are the four oriented triangles in each of the 40
isotropic projective lines of W(3,3). It verifies d1*d2=0, ranks 39 and
120, k=81, exact asymmetric distances dX=3 and dZ=4, and SHA-256 hashes.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Iterable

P = 3
Vec4 = tuple[int, int, int, int]
Sparse = list[tuple[int, int, int]]


def canonical(v: Iterable[int]) -> Vec4:
    vv = tuple(int(x) % P for x in v)
    if vv == (0, 0, 0, 0):
        raise ValueError("zero vector")
    for x in vv:
        if x:
            inv = pow(x, -1, P)
            return tuple((inv * y) % P for y in vv)  # type: ignore[return-value]
    raise AssertionError("unreachable")


def omega(u: Vec4, v: Vec4) -> int:
    return (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % P


def build_complex() -> tuple[
    list[Vec4],
    list[tuple[int, int]],
    list[tuple[int, int, int, int]],
    list[tuple[int, int, int]],
]:
    points: list[Vec4] = []
    seen: set[Vec4] = set()
    for raw in itertools.product(range(P), repeat=4):
        if raw == (0, 0, 0, 0):
            continue
        point = canonical(raw)
        if point not in seen:
            seen.add(point)
            points.append(point)

    point_index = {point: index for index, point in enumerate(points)}
    edges = [
        (i, j)
        for i, j in itertools.combinations(range(len(points)), 2)
        if omega(points[i], points[j]) == 0
    ]
    lines: set[tuple[int, int, int, int]] = set()
    for i, j in edges:
        u, v = points[i], points[j]
        line = {
            point_index[
                canonical((a * u[t] + b * v[t] for t in range(4)))
            ]
            for a, b in itertools.product(range(P), repeat=2)
            if (a, b) != (0, 0)
        }
        lines.add(tuple(sorted(line)))
    triangles = sorted(
        {
            tuple(sorted(triangle))
            for line in lines
            for triangle in itertools.combinations(line, 3)
        }
    )
    return points, edges, sorted(lines), triangles


def build_sparse(
    points: list[Vec4],
    edges: list[tuple[int, int]],
    triangles: list[tuple[int, int, int]],
) -> tuple[Sparse, Sparse]:
    edge_index = {edge: index for index, edge in enumerate(edges)}
    hx: Sparse = []
    for col, (i, j) in enumerate(edges):
        hx.append((i, col, -1 % P))
        hx.append((j, col, 1))

    hz: Sparse = []
    for row, (a, b, c) in enumerate(triangles):
        for value, edge in ((1, (b, c)), (-1, (a, c)), (1, (a, b))):
            hz.append((row, edge_index[tuple(sorted(edge))], value % P))
    return hx, hz


def dense(entries: Sparse, n_rows: int, n_cols: int) -> list[list[int]]:
    matrix = [[0] * n_cols for _ in range(n_rows)]
    for row, col, value in entries:
        matrix[row][col] = (matrix[row][col] + value) % P
    return matrix


def gf_rref(matrix: list[list[int]], p: int = P) -> tuple[list[list[int]], list[int]]:
    rows = [list(map(lambda x: x % p, row)) for row in matrix]
    if not rows:
        return rows, []
    n_rows = len(rows)
    n_cols = len(rows[0])
    rank = 0
    pivots: list[int] = []
    for col in range(n_cols):
        pivot = next((r for r in range(rank, n_rows) if rows[r][col] % p), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col] % p, -1, p)
        rows[rank] = [(inv * x) % p for x in rows[rank]]
        for r in range(n_rows):
            if r != rank and rows[r][col] % p:
                factor = rows[r][col] % p
                rows[r] = [
                    (x - factor * y) % p
                    for x, y in zip(rows[r], rows[rank])
                ]
        pivots.append(col)
        rank += 1
        if rank == n_rows:
            break
    return rows, pivots


def gf_rank(matrix: list[list[int]], p: int = P) -> int:
    return len(gf_rref(matrix, p)[1])


def in_rowspace(vector: list[int], rows: list[list[int]], p: int = P) -> bool:
    rank = gf_rank(rows, p)
    return gf_rank(rows + [[x % p for x in vector]], p) == rank


def matmul_zero(hx: list[list[int]], hz: list[list[int]]) -> bool:
    for xrow in hx:
        xsupport = [i for i, value in enumerate(xrow) if value]
        for zrow in hz:
            total = sum(xrow[i] * zrow[i] for i in xsupport if zrow[i])
            if total % P:
                return False
    return True


def matrix_market(entries: Sparse, n_rows: int, n_cols: int, name: str) -> str:
    ordered = sorted((r + 1, c + 1, v % P) for r, c, v in entries if v % P)
    lines = [
        "%%MatrixMarket matrix coordinate integer general",
        f"% {name}; entries are representatives in {{0,1,2}} of GF(3)",
        f"{n_rows} {n_cols} {len(ordered)}",
    ]
    lines.extend(f"{r} {c} {v}" for r, c, v in ordered)
    return "\n".join(lines) + "\n"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def vector_from_edges(
    support: list[tuple[tuple[int, int], int]],
    edge_index: dict[tuple[int, int], int],
    n_edges: int,
) -> list[int]:
    vector = [0] * n_edges
    for edge, coeff in support:
        vector[edge_index[tuple(sorted(edge))]] = coeff % P
    return vector


def matrix_vector(matrix: list[list[int]], vector: list[int]) -> list[int]:
    return [sum(a * b for a, b in zip(row, vector)) % P for row in matrix]


def graph_triangles(edges: list[tuple[int, int]], n_vertices: int) -> set[tuple[int, int, int]]:
    edge_set = set(edges)
    return {
        (a, b, c)
        for a, b, c in itertools.combinations(range(n_vertices), 3)
        if (a, b) in edge_set and (a, c) in edge_set and (b, c) in edge_set
    }


def no_x_cocycle_below_three(hz: list[list[int]], n_edges: int) -> bool:
    # Weight one requires a zero HZ column. Weight two requires proportional columns.
    normalized: set[tuple[int, ...]] = set()
    for edge in range(n_edges):
        column = tuple(hz[row][edge] % P for row in range(len(hz)))
        if not any(column):
            return False
        first = next(value for value in column if value)
        inv = pow(first, -1, P)
        key = tuple((inv * value) % P for value in column)
        if key in normalized:
            return False
        normalized.add(key)
    return True


def build_release(output_dir: Path) -> dict:
    points, edges, lines, triangles = build_complex()
    edge_index = {edge: index for index, edge in enumerate(edges)}
    hx_sparse, hz_sparse = build_sparse(points, edges, triangles)
    hx = dense(hx_sparse, len(points), len(edges))
    hz = dense(hz_sparse, len(triangles), len(edges))

    hx_text = matrix_market(hx_sparse, 40, 240, "HX=d1 for W(3,3)")
    hz_text = matrix_market(hz_sparse, 160, 240, "HZ=d2^T for W(3,3)")

    z_support = [
        ((0, 1), 1),
        ((0, 13), 2),
        ((1, 4), 1),
        ((4, 13), 1),
    ]
    z_vector = vector_from_edges(z_support, edge_index, len(edges))

    x_support = [
        ((0, 1), 1),
        ((0, 2), 1),
        ((0, 3), 1),
    ]
    x_vector = vector_from_edges(x_support, edge_index, len(edges))

    rank_hx = gf_rank(hx)
    rank_hz = gf_rank(hz)
    graph_triangle_set = graph_triangles(edges, len(points))

    checks = {
        "complex_counts_40_240_40_160": (
            len(points), len(edges), len(lines), len(triangles)
        ) == (40, 240, 40, 160),
        "matrix_shapes": (
            len(hx), len(hx[0]), len(hz), len(hz[0])
        ) == (40, 240, 160, 240),
        "matrix_nnz": (len(hx_sparse), len(hz_sparse)) == (480, 480),
        "boundary_squared_zero": matmul_zero(hx, hz),
        "rank_HX_39": rank_hx == 39,
        "rank_HZ_120": rank_hz == 120,
        "logical_dimension_81": len(edges) - rank_hx - rank_hz == 81,
        "all_graph_triangles_are_2_faces": graph_triangle_set == set(triangles),
        "z_witness_is_cycle": all(value == 0 for value in matrix_vector(hx, z_vector)),
        "z_witness_not_boundary": not in_rowspace(z_vector, hz),
        "z_lower_bound_four": graph_triangle_set == set(triangles),
        "x_no_cocycle_weight_one_or_two": no_x_cocycle_below_three(hz, len(edges)),
        "x_witness_is_cocycle": all(value == 0 for value in matrix_vector(hz, x_vector)),
        "x_witness_not_exact": not in_rowspace(x_vector, hx),
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    hx_path = output_dir / "w33_HX_40x240_GF3.mtx"
    hz_path = output_dir / "w33_HZ_160x240_GF3.mtx"
    hx_path.write_text(hx_text, encoding="utf-8")
    hz_path.write_text(hz_text, encoding="utf-8")

    manifest = {
        "pass": 388,
        "title": "Canonical 240-edge qutrit CSS matrix release lock",
        "verified": all(checks.values()),
        "field": "GF(3)",
        "complex": {
            "C0_vertices": 40,
            "C1_edges": 240,
            "C2_triangles": 160,
            "isotropic_lines": 40,
        },
        "matrices": {
            "HX": {
                "path": "matrices/w33_HX_40x240_GF3.mtx",
                "shape": [40, 240],
                "nnz": len(hx_sparse),
                "rank": rank_hx,
                "sha256": sha256_text(hx_text),
            },
            "HZ": {
                "path": "matrices/w33_HZ_160x240_GF3.mtx",
                "shape": [160, 240],
                "nnz": len(hz_sparse),
                "rank": rank_hz,
                "sha256": sha256_text(hz_text),
            },
        },
        "css": {
            "commuting": checks["boundary_squared_zero"],
            "n": 240,
            "k": 81,
            "dX": 3,
            "dZ": 4,
            "parameters": "[[240,81,3]]_3 with asymmetric distances dX=3,dZ=4",
        },
        "distance_certificates": {
            "dZ": {
                "lower_bound_argument": (
                    "No support-1/2 graph cycle exists; every support-3 cycle is a "
                    "graph triangle, and the enumerated graph triangles equal the 160 "
                    "columns of d2. The listed non-boundary 4-cycle is therefore minimal."
                ),
                "witness": [
                    {"edge": list(edge), "coefficient": coeff}
                    for edge, coeff in z_support
                ],
            },
            "dX": {
                "lower_bound_argument": (
                    "All GF(3) vectors of support one or two were exhaustively tested "
                    "against HZ and none is a cocycle. The listed weight-3 cocycle is "
                    "not in row(HX)."
                ),
                "witness": [
                    {"edge": list(edge), "coefficient": coeff}
                    for edge, coeff in x_support
                ],
            },
        },
        "checks": checks,
    }
    manifest_text = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    manifest["manifest_sha256"] = sha256_text(manifest_text)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix-dir", type=Path, default=Path("matrices"))
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("data/w33_pass388_css_matrix_release.json"),
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    if args.check:
        import tempfile
        with tempfile.TemporaryDirectory() as temporary:
            temp_dir = Path(temporary)
            manifest = build_release(temp_dir)
            expected_hx = (temp_dir / "w33_HX_40x240_GF3.mtx").read_text(encoding="utf-8")
            expected_hz = (temp_dir / "w33_HZ_160x240_GF3.mtx").read_text(encoding="utf-8")
            if (args.matrix_dir / "w33_HX_40x240_GF3.mtx").read_text(encoding="utf-8") != expected_hx:
                raise SystemExit("HX matrix drift")
            if (args.matrix_dir / "w33_HZ_160x240_GF3.mtx").read_text(encoding="utf-8") != expected_hz:
                raise SystemExit("HZ matrix drift")
            committed = json.loads(args.manifest.read_text(encoding="utf-8"))
            if committed != manifest:
                raise SystemExit("Pass 388 manifest drift")
    else:
        manifest = build_release(args.matrix_dir)
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    print(json.dumps({
        "verified": manifest["verified"],
        "parameters": manifest["css"]["parameters"],
        "HX_sha256": manifest["matrices"]["HX"]["sha256"],
        "HZ_sha256": manifest["matrices"]["HZ"]["sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
