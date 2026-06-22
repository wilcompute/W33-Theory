#!/usr/bin/env python3
"""BT1425: retwined CSS frame correction for the D4 guard shear.

BT1424 showed that the D4 guard shear is not a silent automorphism of the
identity-intertwined W33 CSS carrier.  This verifier gives the exact companion
frame update: apply the same guard-tail column permutation to the tracked Pauli
coordinate frame and retwine both stabilizer matrices.  The operational invariant
is syndrome equivariance.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1425_retwined_css_frame_correction.json"
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
    edges = [(i, j) for i, j in itertools.combinations(range(len(points)), 2) if omega(points[i], points[j]) == 0]
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


def permute_vector(vec: list[int], old_to_new: list[int]) -> list[int]:
    out = [0] * len(vec)
    for old, new in enumerate(old_to_new):
        out[new] = vec[old]
    return out


def syndrome(rows: list[list[int]], vec: list[int]) -> tuple[int, ...]:
    return tuple(sum(row[i] * vec[i] for i in range(len(vec))) % P3 for row in rows)


def equivariant_on_basis(rows: list[list[int]], retwined_rows: list[list[int]], perm: list[int]) -> bool:
    n = len(perm)
    for col in range(n):
        for value in (1, 2):
            vec = [0] * n
            vec[col] = value
            if syndrome(rows, vec) != syndrome(retwined_rows, permute_vector(vec, perm)):
                return False
    return True


def rowspace_equal(a: list[list[int]], b: list[list[int]]) -> bool:
    return gf_rank(a) == gf_rank(b) == gf_rank(a + b)


def moved_cycles(perm: list[int]) -> list[list[int]]:
    seen: set[int] = set()
    cycles: list[list[int]] = []
    for i in range(len(perm)):
        if i in seen or perm[i] == i:
            seen.add(i)
            continue
        cur: list[int] = []
        j = i
        while j not in seen:
            seen.add(j)
            cur.append(j)
            j = perm[j]
        cycles.append(cur)
    return cycles


def main() -> None:
    points, edges, triangles = build_w33()
    hx = dense_hx(edges)
    hz = dense_hz(edges, triangles)
    perm = guard_shear_perm()
    hx_r = permute_columns(hx, perm)
    hz_r = permute_columns(hz, perm)
    moved = [i for i in range(240) if perm[i] != i]
    cycles = moved_cycles(perm)

    checks = {
        "css_carrier_is_w33_240_81_3": len(points) == 40 and len(edges) == 240 and len(triangles) == 160 and gf_rank(hx) == 39 and gf_rank(hz) == 120 and 240 - gf_rank(hx) - gf_rank(hz) == 81,
        "original_css_commutes": commute_zero(hx, hz),
        "guard_shear_tail_only_order3": len(moved) == 12 and min(moved) >= 216 and max(moved) < 240 and len(cycles) == 4 and sorted(len(c) for c in cycles) == [3, 3, 3, 3],
        "identity_rowspaces_are_not_preserved": not rowspace_equal(hx, hx_r) and not rowspace_equal(hz, hz_r),
        "retwined_css_commutes": commute_zero(hx_r, hz_r),
        "retwined_css_has_same_ranks_and_k": gf_rank(hx_r) == 39 and gf_rank(hz_r) == 120 and 240 - gf_rank(hx_r) - gf_rank(hz_r) == 81,
        "x_syndrome_equivariant_on_basis": equivariant_on_basis(hx, hx_r, perm),
        "z_syndrome_equivariant_on_basis": equivariant_on_basis(hz, hz_r, perm),
        "one_sided_commutation_fails": not commute_zero(hx_r, hz) and not commute_zero(hx, hz_r),
    }

    result = {
        "bt": 1425,
        "title": "Retwined CSS frame correction for the D4 guard shear",
        "verified": all(checks.values()),
        "companion_frame_update": {
            "type": "tracked Pauli/CSS coordinate-frame permutation",
            "rule": "If the guard shear sends old edge coordinate i to J(i), update every tracked Pauli/error coordinate by the same old_to_new map and use retwined stabilizers H_X J^{-1}, H_Z J^{-1}.",
            "moved_coordinates": moved,
            "nontrivial_cycles": cycles,
            "fixed_coordinates": 240 - len(moved),
            "order": 3,
        },
        "css_invariants": {
            "original": {"rank_HX": gf_rank(hx), "rank_HZ": gf_rank(hz), "k": 240 - gf_rank(hx) - gf_rank(hz), "commuting": commute_zero(hx, hz)},
            "retwined": {"rank_HX": gf_rank(hx_r), "rank_HZ": gf_rank(hz_r), "k": 240 - gf_rank(hx_r) - gf_rank(hz_r), "commuting": commute_zero(hx_r, hz_r)},
            "one_sided_HX_retwin_commutes_with_old_HZ": commute_zero(hx_r, hz),
            "old_HX_commutes_with_one_sided_HZ_retwin": commute_zero(hx, hz_r),
        },
        "syndrome_equivariance": {
            "x_basis_errors": "verified for all 240 coordinates and nonzero F3 values 1,2",
            "z_basis_errors": "verified for all 240 coordinates and nonzero F3 values 1,2",
            "statement": "For every basis error e, syndrome_H(e) equals syndrome_H_retwin(J e).",
        },
        "interpretation": "The legitimate operation is not a bare one-sided D4 shear. It is a retwined CSS frame transition: move the guard-tail coordinates, retwine both stabilizer matrices, and update the tracked Pauli frame by the same permutation.",
        "boundary": "This supplies the exact companion frame update. It does not yet choose a physical recovery pulse schedule; it proves the algebraic frame-tracking rule required by the injection rail.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1425, "verified": result["verified"], "moved": len(moved), "k": result["css_invariants"]["retwined"]["k"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
