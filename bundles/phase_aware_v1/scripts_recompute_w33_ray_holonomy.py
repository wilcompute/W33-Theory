#!/usr/bin/env python3
"""Recompute W33 ray-induced Z12 edge phases and four-center triad holonomies.

Inputs:
  - data/_workbench/02_geometry/W33_line_phase_map.csv
  - data/_toe/w33_orthonormal_phase_solution_20260110/W33_point_rays_C4_complex.csv

Outputs (in --outdir):
  - w33_noncollinear_edge_phases_k_mod12.csv
  - w33_four_center_triads_with_ray_holonomy.csv
"""

import argparse
import itertools
import math
from collections import Counter

import numpy as np
import pandas as pd

ALL12 = (1 << 12) - 1
OMEGA = np.exp(2j * np.pi / 12)


def parse_c(s: str) -> complex:
    return complex(str(s).replace("i", "j"))


def quantize_phase(z: complex) -> int:
    ang = np.angle(z)
    if ang < 0:
        ang += 2 * np.pi
    return int(np.round(ang / (2 * np.pi / 12))) % 12


def popcount(x: int) -> int:
    return bin(x).count("1")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--w33_csv", required=True)
    ap.add_argument("--rays_csv", required=True)
    ap.add_argument("--outdir", required=True)
    args = ap.parse_args()

    w33 = pd.read_csv(args.w33_csv)
    rays = pd.read_csv(args.rays_csv)

    # vectors
    vecs = {}
    for r in rays.itertuples(index=False):
        pid = int(r.point_id)
        v = np.array(
            [parse_c(r.v0), parse_c(r.v1), parse_c(r.v2), parse_c(r.v3)],
            dtype=np.complex128,
        )
        vecs[pid] = v

    # lines & collinearity
    lines = {}
    for r in w33.itertuples(index=False):
        lid = int(r.line_id)
        pts = tuple(int(x) for x in str(r.point_ids).split())
        lines[lid] = pts
    col = {p: set() for p in range(40)}
    for pts in lines.values():
        for a, b in itertools.combinations(pts, 2):
            col[a].add(b)
            col[b].add(a)
    noncol = {p: set(range(40)) - {p} - col[p] for p in range(40)}

    # edge phases
    k_edge = {}
    rows = []
    for p in range(40):
        vp = vecs[p]
        for q in noncol[p]:
            ip = np.vdot(vp, vecs[q])
            k = quantize_phase(ip)
            k_edge[(p, q)] = k
            rows.append(dict(p=p, q=q, k_mod12=k))
    pd.DataFrame(rows).to_csv(
        f"{args.outdir}/w33_noncollinear_edge_phases_k_mod12.csv", index=False
    )

    # four-center triads and holonomy
    # compute centers using col sets
    def centers(a, b, c):
        return col[a] & col[b] & col[c]

    tri_rows = []
    for a in range(40):
        for b in range(a + 1, 40):
            if b in col[a]:
                continue
            for c in range(b + 1, 40):
                if c in col[a] or c in col[b]:
                    continue
                ctr = centers(a, b, c)
                if len(ctr) != 4:
                    continue
                hol = (k_edge[(a, b)] + k_edge[(b, c)] + k_edge[(c, a)]) % 12
                tri_rows.append(dict(triad=f"{a} {b} {c}", holonomy_z12=hol))
    df = pd.DataFrame(tri_rows)
    df.to_csv(
        f"{args.outdir}/w33_four_center_triads_with_ray_holonomy.csv", index=False
    )
    print("four-center triads:", len(df), "hol_counts:", dict(Counter(df.holonomy_z12)))


if __name__ == "__main__":
    main()
