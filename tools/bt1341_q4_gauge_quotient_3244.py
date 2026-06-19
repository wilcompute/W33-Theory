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


def in_span(x: int, basis: list[int]) -> bool:
    piv = {b.bit_length() - 1: b for b in basis}
    y = x
    while y:
        p = y.bit_length() - 1
        if p not in piv:
            return False
        y ^= piv[p]
    return True


def nullspace(row_masks: list[int], ncols: int) -> list[int]:
    basis = rref(row_masks, ncols)
    pivots = [i for i, b in enumerate(basis) if b]
    free = [i for i in range(ncols) if i not in set(pivots)]
    out = []
    for f in free:
        x = 1 << f
        for p in pivots:
            if (basis[p] & x).bit_count() & 1:
                x |= 1 << p
        assert all(dot(r, x) == 0 for r in row_masks)
        out.append(x)
    return out


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
                    support = [
                        emap[frozenset((vid[v00], vid[v10]))],
                        emap[frozenset((vid[v10], vid[v11]))],
                        emap[frozenset((vid[v01], vid[v11]))],
                        emap[frozenset((vid[v00], vid[v01]))],
                    ]
                    faces.append(sum(1 << e for e in support))
    hx = []
    for vi in range(16):
        m = 0
        for e, (a, b, _d) in enumerate(edges):
            if a == vi or b == vi:
                m |= 1 << e
        hx.append(m)
    return hx, faces


def combo(mask: int, basis: list[int]) -> int:
    x = 0
    for i, b in enumerate(basis):
        if (mask >> i) & 1:
            x ^= b
    return x


def min_distance_x(hz: list[int], hx_basis: list[int], max_w: int = 4):
    for w in range(1, max_w + 1):
        for c in itertools.combinations(range(N), w):
            m = sum(1 << i for i in c)
            if all(dot(r, m) == 0 for r in hz) and not in_span(m, hx_basis):
                return w, m
    return None, None


def min_distance_z(hx: list[int], hz_basis: list[int], max_w: int = 4):
    for w in range(1, max_w + 1):
        for c in itertools.combinations(range(N), w):
            m = sum(1 << i for i in c)
            if all(dot(r, m) == 0 for r in hx) and not in_span(m, hz_basis):
                return w, m
    return None, None


def supports(mask: int) -> list[int]:
    return [i for i in range(N) if (mask >> i) & 1]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1341_q4_gauge_quotient_3244.json")
    ns = ap.parse_args()
    hx, faces = build_cube()
    cycle_basis = basis_list(faces, N)
    hx_basis = basis_list(hx, N)
    # Four global quotient/flux functionals on the 17-dimensional cycle space.
    quotient_functionals = [0x79B8, 0x7A2E, 0x9EA1, 0xADA0]
    bad = set()
    for w in range(1, 4):
        for c in itertools.combinations(range(N), w):
            m = sum(1 << i for i in c)
            if not in_span(m, hx_basis):
                f = 0
                for j, cyc in enumerate(cycle_basis):
                    if dot(m, cyc):
                        f |= 1 << j
                if f:
                    bad.add(f)
    q_span = {combo(mask, quotient_functionals) for mask in range(1, 16)}
    kernel_coords = nullspace(quotient_functionals, len(cycle_basis))
    hz = [combo(u, cycle_basis) for u in kernel_coords]
    hz_basis = basis_list(hz, N)
    dx, xw = min_distance_x(hz, hx_basis)
    dz, zw = min_distance_z(hx, hz_basis)
    checks = {
        "raw_cycle_rank_17": rank(faces, N) == 17,
        "hx_rank_15": rank(hx, N) == 15,
        "hz_rank_13": rank(hz, N) == 13,
        "commutes": all(dot(a, b) == 0 for a in hx for b in hz),
        "quotient_rank_4": rank(quotient_functionals, len(cycle_basis)) == 4,
        "quotient_avoids_all_weight_lt4_dual_logicals": q_span.isdisjoint(bad),
        "k_is_4": N - rank(hx, N) - rank(hz, N) == 4,
        "x_distance_4": dx == 4,
        "z_distance_4": dz == 4,
    }
    result = {
        "bt": 1341,
        "title": "Q4 gauge quotient certificate for [[32,4,4]]",
        "verified": all(checks.values()),
        "n": N,
        "rank_hx": rank(hx, N),
        "rank_hz": rank(hz, N),
        "k": N - rank(hx, N) - rank(hz, N),
        "dx": dx,
        "dz": dz,
        "checks": checks,
        "quotient_functionals_hex": [hex(x) for x in quotient_functionals],
        "kernel_coordinate_basis_hex": [hex(x) for x in kernel_coords],
        "hz_rows_hex": [hex(x) for x in hz],
        "x_weight4_witness_edges": supports(xw),
        "z_weight4_witness_edges": supports(zw),
        "bad_weight_lt4_dual_functional_count": len(bad),
        "interpretation": "A four-functional gauge quotient of the Q4 cycle space yields 13 independent Z checks. Together with the 15 vertex/star X checks this gives [[32,4,4]]. This is a gauge quotient certificate; a geometric torus drawing is a further interpretation layer."
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1341, "verified": result["verified"], "k": result["k"], "dx": dx, "dz": dz}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
