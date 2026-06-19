#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
N = 32


def dot(a: int, b: int) -> int:
    return (a & b).bit_count() & 1


def rref(rows: list[int], n: int) -> list[int]:
    basis = [0] * n
    for x in rows:
        y = x
        while y:
            p = y.bit_length() - 1
            if basis[p]:
                y ^= basis[p]
            else:
                basis[p] = y
                for q, b in enumerate(basis):
                    if q != p and b and ((b >> p) & 1):
                        basis[q] = b ^ y
                break
    return basis


def basis_list(rows: list[int], n: int) -> list[int]:
    return [b for b in rref(rows, n) if b]


def rank(rows: list[int], n: int) -> int:
    return len(basis_list(rows, n))


def coords_in_basis(v: int, basis: list[int], n: int = 32) -> int:
    m = len(basis)
    rows = []
    for bit in range(n):
        row = 0
        for j, b in enumerate(basis):
            if (b >> bit) & 1:
                row |= 1 << j
        if (v >> bit) & 1:
            row |= 1 << m
        rows.append(row)
    r = 0
    piv = []
    for c in range(m):
        pr = None
        for i in range(r, len(rows)):
            if (rows[i] >> c) & 1:
                pr = i
                break
        if pr is None:
            continue
        rows[r], rows[pr] = rows[pr], rows[r]
        for i in range(len(rows)):
            if i != r and ((rows[i] >> c) & 1):
                rows[i] ^= rows[r]
        piv.append((c, r))
        r += 1
    sol = 0
    for c, ri in piv:
        if (rows[ri] >> m) & 1:
            sol |= 1 << c
    return sol


def mat_vec(cols: list[int], x: int) -> int:
    y = 0
    while x:
        lb = x & -x
        i = lb.bit_length() - 1
        y ^= cols[i]
        x ^= lb
    return y


def invert_matrix_cols(cols: list[int], m: int) -> list[int]:
    inv = []
    for target in [1 << i for i in range(m)]:
        rows = []
        for rowbit in range(m):
            row = 0
            for j, col in enumerate(cols):
                if (col >> rowbit) & 1:
                    row |= 1 << j
            if (target >> rowbit) & 1:
                row |= 1 << m
            rows.append(row)
        r = 0
        piv = []
        for c in range(m):
            pr = None
            for i in range(r, m):
                if (rows[i] >> c) & 1:
                    pr = i
                    break
            if pr is None:
                continue
            rows[r], rows[pr] = rows[pr], rows[r]
            for i in range(m):
                if i != r and ((rows[i] >> c) & 1):
                    rows[i] ^= rows[r]
            piv.append((c, r))
            r += 1
        sol = 0
        for c, ri in piv:
            if (rows[ri] >> m) & 1:
                sol |= 1 << c
        assert mat_vec(cols, sol) == target
        inv.append(sol)
    return inv


def transform_functional(f: int, inv_cols: list[int]) -> int:
    out = 0
    for i, col in enumerate(inv_cols):
        if dot(f, col):
            out |= 1 << i
    return out


def subspace_key(rows: list[int], n: int) -> tuple[int, ...]:
    return tuple(sorted(basis_list(rows, n)))


def build_cube():
    verts = list(itertools.product([0, 1], repeat=4))
    vid = {v: i for i, v in enumerate(verts)}
    edges = []
    for v in verts:
        for d in range(4):
            if v[d] == 0:
                w = list(v); w[d] = 1; w = tuple(w)
                edges.append((vid[v], vid[w], d))
    emap = {frozenset((a, b)): i for i, (a, b, _d) in enumerate(edges)}
    faces = []
    for i in range(4):
        for j in range(i + 1, 4):
            for v in verts:
                if v[i] == 0 and v[j] == 0:
                    v00 = v
                    v10 = list(v); v10[i] = 1; v10 = tuple(v10)
                    v01 = list(v); v01[j] = 1; v01 = tuple(v01)
                    v11 = list(v); v11[i] = 1; v11[j] = 1; v11 = tuple(v11)
                    support = [emap[frozenset((vid[v00], vid[v10]))], emap[frozenset((vid[v10], vid[v11]))], emap[frozenset((vid[v01], vid[v11]))], emap[frozenset((vid[v00], vid[v01]))]]
                    faces.append(sum(1 << e for e in support))
    edge_key = {frozenset((a, b)): i for i, (a, b, _d) in enumerate(edges)}
    return verts, edges, edge_key, faces


def apply_auto_vertex(v, perm, flip: int):
    return tuple(v[perm[i]] ^ ((flip >> i) & 1) for i in range(4))


def edge_perm(verts, edges, edge_key, perm, flip: int):
    vid = {v: i for i, v in enumerate(verts)}
    out = [0] * len(edges)
    for i, (a, b, _d) in enumerate(edges):
        na = vid[apply_auto_vertex(verts[a], perm, flip)]
        nb = vid[apply_auto_vertex(verts[b], perm, flip)]
        out[i] = edge_key[frozenset((na, nb))]
    return out


def permute_mask(mask: int, ep: list[int]) -> int:
    y = 0
    for i, j in enumerate(ep):
        if (mask >> i) & 1:
            y |= 1 << j
    return y


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1344_q4_quotient_canonicalization.json")
    ns = ap.parse_args()
    verts, edges, edge_key, faces = build_cube()
    cycle_basis = basis_list(faces, N)
    q_rows = [0x79B8, 0x7A2E, 0x9EA1, 0xADA0]
    original_key = subspace_key(q_rows, len(cycle_basis))
    min_key = None
    min_auto = None
    stabilizer = 0
    orbit = set()
    for perm in itertools.permutations(range(4)):
        for flip in range(16):
            ep = edge_perm(verts, edges, edge_key, perm, flip)
            cols = [coords_in_basis(permute_mask(b, ep), cycle_basis) for b in cycle_basis]
            inv_cols = invert_matrix_cols(cols, len(cycle_basis))
            key = subspace_key([transform_functional(f, inv_cols) for f in q_rows], len(cycle_basis))
            orbit.add(key)
            if key == original_key:
                stabilizer += 1
            if min_key is None or key < min_key:
                min_key = key
                min_auto = {"perm": list(perm), "flip": flip}
    checks = {
        "cube_automorphism_group_order_384": len(list(itertools.permutations(range(4)))) * 16 == 384,
        "orbit_stabilizer": len(orbit) * stabilizer == 384,
        "trivial_stabilizer": stabilizer == 1,
        "full_orbit_384": len(orbit) == 384,
    }
    result = {
        "bt": 1344,
        "title": "Q4 quotient canonicalization audit",
        "verified": all(checks.values()),
        "checks": checks,
        "original_subspace_key_hex": [hex(x) for x in original_key],
        "canonical_orbit_key_hex": [hex(x) for x in min_key],
        "canonical_automorphism": min_auto,
        "orbit_size": len(orbit),
        "stabilizer_size": stabilizer,
        "interpretation": "The BT1341 quotient is valid but generic under the full Q4 cube automorphism group: its stabilizer is trivial and its orbit has size 384. A more geometric quotient should search for additional symmetry or W(3,3)-compatibility."
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1344, "verified": result["verified"], "orbit_size": len(orbit), "stabilizer_size": stabilizer}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
