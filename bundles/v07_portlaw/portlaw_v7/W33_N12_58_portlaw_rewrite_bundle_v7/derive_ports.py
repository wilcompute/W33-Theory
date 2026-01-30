#!/usr/bin/env python3
"""
Derive canonical K4 "port labels" for W33 four-center triads.

- Loads W33 incidence from: data/_workbench/02_geometry/W33_line_phase_map.csv
- Enumerates the 360 four-center triads and their 90 K4 components (center quads).
- For each component:
  * computes the outer quad P (4 mutually noncollinear points),
  * labels each triad state by its excluded point in P,
  * labels each edge in K4 by a matching index (0/1/2) on P.

Also computes the directed Bargmann 4-cycle commutator phase from the C^4 ray solution:
  comm_k4 = k(c,a)+k(a,d)+k(d,b)+k(b,c) mod 12,
which comes out identically 6 for all directed moves (phase = -1).

Outputs (to output_dir):
- w33_k4_components.csv
- w33_k4_edges_undirected.csv
- w33_k4_moves_directed_commutator.csv
- w33_four_center_triads_with_ray_holonomy.csv

Usage:
  python derive_ports.py --root /path/to/proj_data/data --out ./out
"""

from __future__ import annotations

import argparse
import itertools
import math
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

SYM = {**{str(i): i for i in range(10)}, "a": 10, "b": 11}


def parse_complex(s: str) -> complex:
    return complex(str(s).replace(" ", ""))


def quant_k(z: complex) -> int:
    twopi = 2 * math.pi
    ang = math.atan2(z.imag, z.real)
    return int(round((12 * ang / twopi))) % 12


def matchings_for_P(P):
    p0, p1, p2, p3 = P
    return [((p0, p1), (p2, p3)), ((p0, p2), (p1, p3)), ((p0, p3), (p1, p2))]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=str, required=True, help="Path to proj_data/data")
    ap.add_argument("--out", type=str, required=True, help="Output directory")
    args = ap.parse_args()

    ROOT = Path(args.root)
    OUT = Path(args.out)
    OUT.mkdir(parents=True, exist_ok=True)

    w33_csv = ROOT / "_workbench/02_geometry/W33_line_phase_map.csv"
    df = pd.read_csv(w33_csv)
    lines = [tuple(map(int, s.split())) for s in df["point_ids"].astype(str)]
    points = sorted({p for L in lines for p in L})

    col = {p: set() for p in points}
    for L in lines:
        for i in range(4):
            for j in range(i + 1, 4):
                a, b = L[i], L[j]
                col[a].add(b)
                col[b].add(a)

    # enumerate four-center triads and components
    four_triads = []
    centers = []
    for a, b, c in itertools.combinations(points, 3):
        if (b in col[a]) or (c in col[a]) or (c in col[b]):
            continue
        cs = col[a] & col[b] & col[c]
        if len(cs) == 4:
            t = tuple(sorted((a, b, c)))
            four_triads.append(t)
            centers.append(tuple(sorted(cs)))
    assert len(four_triads) == 360

    tri_index = {t: i for i, t in enumerate(four_triads)}

    comp_to_triads = defaultdict(list)
    for t, cs in zip(four_triads, centers):
        comp_to_triads[cs].append(t)
    assert len(comp_to_triads) == 90

    comp_records = []
    edge_records = []
    for comp_id, (cs, triads) in enumerate(sorted(comp_to_triads.items())):
        P = sorted(set().union(*[set(t) for t in triads]))
        assert len(P) == 4
        all3 = set(map(tuple, itertools.combinations(P, 3)))
        assert set(triads) == all3

        exc_map = {}
        for t in triads:
            exc = next(iter(set(P) - set(t)))
            exc_map[t] = exc
            comp_records.append(
                dict(
                    component_id=comp_id,
                    center_quad=" ".join(map(str, cs)),
                    outer_quad=" ".join(map(str, P)),
                    triad=" ".join(map(str, t)),
                    triad_index=tri_index[t],
                    excluded_point=exc,
                )
            )

        ms = matchings_for_P(P)
        pair_to_idx = {}
        for midx, m in enumerate(ms):
            for pair in m:
                pair_to_idx[frozenset(pair)] = midx

        tri_list = sorted(triads)
        for t1, t2 in itertools.combinations(tri_list, 2):
            x = exc_map[t1]
            y = exc_map[t2]
            midx = pair_to_idx[frozenset((x, y))]
            edge_records.append(
                dict(
                    component_id=comp_id,
                    center_quad=" ".join(map(str, cs)),
                    outer_quad=" ".join(map(str, P)),
                    triad_a=" ".join(map(str, t1)),
                    triad_b=" ".join(map(str, t2)),
                    triad_a_idx=tri_index[t1],
                    triad_b_idx=tri_index[t2],
                    excluded_a=x,
                    excluded_b=y,
                    edge_matching_idx=midx,
                    matching_pairs=str(ms[midx]),
                )
            )

    pd.DataFrame(comp_records).to_csv(OUT / "w33_k4_components.csv", index=False)
    pd.DataFrame(edge_records).to_csv(OUT / "w33_k4_edges_undirected.csv", index=False)

    # rays + holonomy + commutator
    ray_csv = (
        ROOT
        / "_toe/w33_orthonormal_phase_solution_20260110/W33_point_rays_C4_complex.csv"
    )
    df_r = pd.read_csv(ray_csv)
    V = np.zeros((40, 4), dtype=np.complex128)
    for _, r in df_r.iterrows():
        pid = int(r["point_id"])
        V[pid] = [parse_complex(r[f"v{i}"]) for i in range(4)]

    edge_k = {}
    for p in points:
        for q in points:
            if p == q:
                continue
            if q in col[p]:
                continue
            edge_k[(p, q)] = quant_k(np.vdot(V[p], V[q]))

    tri_h = []
    for t in four_triads:
        a, b, c = t
        tri_h.append((edge_k[(a, b)] + edge_k[(b, c)] + edge_k[(c, a)]) % 12)
    tri_h = np.array(tri_h, dtype=np.int8)
    assert set(tri_h.tolist()) == {3, 9}

    # directed moves commutator
    directed = []
    for cs, triads in comp_to_triads.items():
        P = sorted(set().union(*map(set, triads)))
        tri_by_exc = {next(iter(set(P) - set(t))): t for t in triads}
        for x in P:
            for y in P:
                if x == y:
                    continue
                sh = sorted(set(P) - {x, y})
                a, b = sh[0], sh[1]
                c = y
                d = x
                comm = (
                    edge_k[(c, a)] + edge_k[(a, d)] + edge_k[(d, b)] + edge_k[(b, c)]
                ) % 12
                directed.append(
                    dict(
                        center_quad=" ".join(map(str, cs)),
                        outer_quad=" ".join(map(str, P)),
                        from_excluded=x,
                        to_excluded=y,
                        shared_pair=f"{a} {b}",
                        comm_k4_mod12=comm,
                    )
                )
    df_dir = pd.DataFrame(directed)
    df_dir.to_csv(OUT / "w33_k4_moves_directed_commutator.csv", index=False)

    # four-center triads with holonomy
    tri_df = pd.DataFrame(
        {
            "triad_index": list(range(360)),
            "triad": [" ".join(map(str, t)) for t in four_triads],
            "center_quad": [" ".join(map(str, centers[i])) for i in range(360)],
            "triad_hol_mod12": tri_h.astype(int),
        }
    )
    tri_df.to_csv(OUT / "w33_four_center_triads_with_ray_holonomy.csv", index=False)

    print("Wrote outputs to:", OUT)


if __name__ == "__main__":
    main()
