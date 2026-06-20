#!/usr/bin/env python3
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def gf2_rank(rows: list[list[int]]) -> int:
    a = [r[:] for r in rows]
    if not a:
        return 0
    m, n = len(a), len(a[0])
    rank = 0
    for col in range(n):
        pivot = None
        for row in range(rank, m):
            if a[row][col] & 1:
                pivot = row
                break
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        for row in range(m):
            if row != rank and (a[row][col] & 1):
                a[row] = [x ^ y for x, y in zip(a[row], a[rank])]
        rank += 1
        if rank == m:
            break
    return rank


def build() -> dict:
    verts = list(itertools.product([0, 1], repeat=4))
    vid = {v: i for i, v in enumerate(verts)}
    edges = []
    for v in verts:
        for d in range(4):
            if v[d] == 0:
                w = list(v)
                w[d] = 1
                edges.append((vid[v], vid[tuple(w)], d))
    emap = {frozenset((a, b)): i for i, (a, b, _d) in enumerate(edges)}
    faces = []
    for i in range(4):
        for j in range(i + 1, 4):
            for v in verts:
                if v[i] == 0 and v[j] == 0:
                    v00 = v
                    v10 = list(v)
                    v10[i] = 1
                    v10 = tuple(v10)
                    v01 = list(v)
                    v01[j] = 1
                    v01 = tuple(v01)
                    v11 = list(v)
                    v11[i] = 1
                    v11[j] = 1
                    v11 = tuple(v11)
                    support = [
                        emap[frozenset((vid[v00], vid[v10]))],
                        emap[frozenset((vid[v10], vid[v11]))],
                        emap[frozenset((vid[v01], vid[v11]))],
                        emap[frozenset((vid[v00], vid[v01]))],
                    ]
                    faces.append((i, j, vid[v00], support))
    d1 = [[0] * len(edges) for _ in verts]
    for e, (a, b, _d) in enumerate(edges):
        d1[a][e] = 1
        d1[b][e] = 1
    d2 = [[0] * len(faces) for _ in edges]
    for f, (_i, _j, _base, support) in enumerate(faces):
        for e in support:
            d2[e][f] = 1
    r1 = gf2_rank(d1)
    r2 = gf2_rank(d2)
    k = len(edges) - r1 - r2
    return {
        "bt": 1338,
        "title": "Explicit Q4 chain check matrix extraction",
        "verified": True,
        "vertices": ["".join(map(str, v)) for v in verts],
        "edges": [
            {"id": i, "u": a, "v": b, "dir": d, "support_vertices": [a, b]}
            for i, (a, b, d) in enumerate(edges)
        ],
        "faces": [
            {"id": i, "dims": [di, dj], "base_vertex": base, "support_edges": support}
            for i, (di, dj, base, support) in enumerate(faces)
        ],
        "ranks": {
            "rank_boundary_1": r1,
            "rank_boundary_2": r2,
            "n_edges": len(edges),
            "css_k_naive_n_minus_ranks": k,
        },
        "needed_for_w33_32_4_4": {
            "target_n": len(edges),
            "target_k": 4,
            "target_d": 4,
            "raw_q4_k": k,
            "additional_logical_modes_needed": 4 - k,
            "required_certificate": "toroidal/gauge quotient",
            "status": "not certified by the raw cubical Q4 chain checks alone",
        },
        "verdict": "The raw cubical Q4 chain checks give k=0. The claimed [[32,4,4]] object requires an additional toroidal/gauge quotient certificate.",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out",
        type=Path,
        default=ROOT / "data" / "bt1338_q4_chain_check_matrices.json",
    )
    ns = ap.parse_args()
    result = build()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "bt": 1338,
                "verified": True,
                "k_naive": result["ranks"]["css_k_naive_n_minus_ranks"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
