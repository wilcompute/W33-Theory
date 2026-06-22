#!/usr/bin/env python3
"""BT1424: test the D4 quartic guard shear against the W33 CSS carrier."""
from __future__ import annotations

import itertools
import json
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1424_d4_shear_css_logical_action.json"
P3 = 3
Vec = tuple[int, int, int, int]


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
    for raw in itertools.product(range(P3), repeat=4):
        if raw == (0, 0, 0, 0):
            continue
        c = canonical(raw)
        if c not in seen:
            seen.add(c)
            points.append(c)

    edges = [
        (i, j)
        for i, j in itertools.combinations(range(len(points)), 2)
        if omega(points[i], points[j]) == 0
    ]
    point_index = {p: i for i, p in enumerate(points)}
    lines: set[tuple[int, int, int, int]] = set()
    for i, j in edges:
        u, v = points[i], points[j]
        line: set[int] = set()
        for a, b in itertools.product(range(P3), repeat=2):
            if a == 0 and b == 0:
                continue
            line.add(point_index[canonical((a * u[t] + b * v[t] for t in range(4)))])
        lines.add(tuple(sorted(line)))
    triangles = sorted({tuple(sorted(t)) for line in lines for t in itertools.combinations(line, 3)})
    return points, edges, triangles


def dense_hx(edges: list[tuple[int, int]]) -> list[list[int]]:
    rows = [[0 for _ in edges] for _ in range(40)]
    for col, (i, j) in enumerate(edges):
        rows[i][col] = 2
        rows[j][col] = 1
    return rows


def dense_hz(edges: list[tuple[int, int]], triangles: list[tuple[int, int, int]]) -> list[list[int]]:
    edge_index = {edge: idx for idx, edge in enumerate(edges)}
    rows = [[0 for _ in edges] for _ in triangles]
    for row, (a, b, c) in enumerate(triangles):
        for value, edge in ((1, (b, c)), (2, (a, c)), (1, (a, b))):
            rows[row][edge_index[tuple(sorted(edge))]] = value % P3
    return rows


def gf_rank(rows: list[list[int]], p: int = P3) -> int:
    matrix = [list(row) for row in rows]
    if not matrix:
        return 0
    n_rows, n_cols = len(matrix), len(matrix[0])
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
                matrix[row] = [(x - factor * y) % p for x, y in zip(matrix[row], matrix[rank])]
        rank += 1
        if rank == n_rows:
            break
    return rank


def commute_zero(left: list[list[int]], right: list[list[int]]) -> bool:
    for a in left:
        support = [i for i, x in enumerate(a) if x % P3]
        for b in right:
            if sum(a[i] * b[i] for i in support) % P3:
                return False
    return True


def guard_shear_perm() -> list[int]:
    perm = list(range(240))
    for atom in range(2):
        for branch in range(4):
            for phase in range(3):
                old = 216 + atom * 12 + branch * 3 + phase
                new = 216 + atom * 12 + branch * 3 + ((phase + branch) % 3)
                perm[old] = new
    return perm


def permute_columns(rows: list[list[int]], old_to_new: list[int]) -> list[list[int]]:
    inv = [0] * len(old_to_new)
    for old, new in enumerate(old_to_new):
        inv[new] = old
    return [[row[inv[col]] for col in range(len(row))] for row in rows]


def moved_cycles(perm: list[int]) -> list[list[int]]:
    seen = set()
    cycles = []
    for i in range(len(perm)):
        if i in seen or perm[i] == i:
            seen.add(i)
            continue
        cur = []
        j = i
        while j not in seen:
            seen.add(j)
            cur.append(j)
            j = perm[j]
        cycles.append(cur)
    return cycles


def rowspace_equal(a: list[list[int]], b: list[list[int]]) -> bool:
    return gf_rank(a) == gf_rank(b) == gf_rank(a + b)


def main() -> None:
    points, edges, triangles = build_w33()
    hx = dense_hx(edges)
    hz = dense_hz(edges, triangles)
    perm = guard_shear_perm()
    hx_s = permute_columns(hx, perm)
    hz_s = permute_columns(hz, perm)
    cycles = moved_cycles(perm)
    moved = [i for i in range(240) if perm[i] != i]

    rank_hx = gf_rank(hx)
    rank_hz = gf_rank(hz)
    rank_hx_join = gf_rank(hx + hx_s)
    rank_hz_join = gf_rank(hz + hz_s)
    checks = {
        "w33_css_carrier_shape": len(points) == 40 and len(edges) == 240 and len(triangles) == 160,
        "original_css_parameters": rank_hx == 39 and rank_hz == 120 and len(edges) - rank_hx - rank_hz == 81,
        "original_css_commutes": commute_zero(hx, hz),
        "shear_moves_only_guard_tail": moved and min(moved) >= 216 and max(moved) < 240 and len(moved) == 12,
        "shear_has_four_three_cycles": len(cycles) == 4 and sorted(len(c) for c in cycles) == [3, 3, 3, 3],
        "permuted_pair_still_css_equivalent": gf_rank(hx_s) == 39 and gf_rank(hz_s) == 120 and commute_zero(hx_s, hz_s),
        "hx_rowspace_not_preserved_by_guard_shear": not rowspace_equal(hx, hx_s) and rank_hx_join > rank_hx,
        "hz_rowspace_not_preserved_by_guard_shear": not rowspace_equal(hz, hz_s) and rank_hz_join > rank_hz,
        "one_sided_shear_breaks_css_commutation": not commute_zero(hx_s, hz) and not commute_zero(hx, hz_s),
    }

    result = {
        "bt": 1424,
        "title": "D4 quartic guard shear action on the W33 CSS carrier",
        "verified": all(checks.values()),
        "css_carrier": {
            "field": "F3",
            "HX_shape": [40, 240],
            "HZ_shape": [160, 240],
            "rank_HX": rank_hx,
            "rank_HZ": rank_hz,
            "logical_qutrits": len(edges) - rank_hx - rank_hz,
            "commuting": commute_zero(hx, hz),
        },
        "guard_shear": {
            "definition": "on tail index 216 + atom*12 + branch*3 + phase, send phase -> phase + branch mod 3",
            "moved_coordinates": len(moved),
            "fixed_coordinates": 240 - len(moved),
            "nontrivial_cycles": cycles,
            "order": 3,
        },
        "css_action_test": {
            "rank_HX_plus_sheared_HX": rank_hx_join,
            "rank_HZ_plus_sheared_HZ": rank_hz_join,
            "preserves_HX_rowspace": rowspace_equal(hx, hx_s),
            "preserves_HZ_rowspace": rowspace_equal(hz, hz_s),
            "permuting_both_sides_preserves_commutation": commute_zero(hx_s, hz_s),
            "one_sided_HX_shear_commutes_with_original_HZ": commute_zero(hx_s, hz),
            "original_HX_commutes_with_one_sided_HZ_shear": commute_zero(hx, hz_s),
        },
        "interpretation": "The D4 guard shear is not a free logical automorphism of the current identity-intertwined [[240,81,3]]_3 CSS carrier. It defines an equivalent retwined CSS frame if both stabilizer sides are permuted together, but a one-sided injection must be accompanied by a CSS frame update/correction.",
        "boundary": "This is an exact finite carrier-action test. It does not rule out a retwined logical non-Clifford gate; it shows that the current identity ledger cannot treat the guard shear as an unannounced stabilizer automorphism.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1424, "verified": result["verified"], "hx_join_rank": rank_hx_join, "hz_join_rank": rank_hz_join}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
