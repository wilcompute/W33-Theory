#!/usr/bin/env python3
"""Reproduce evaluation for the exported best mapping.

Loads:
- W33 line incidence
- N12 candidate point masks
- 360 four-center triads (computed from W33 incidence)
- 5 nontrivial 2T cycles supports

Then:
- computes cover-size histogram on four-center triads under mapping
- computes per-cycle minimal cover12 usage + reconstructs witness walks (saved already in outputs)
"""

from __future__ import annotations

import itertools
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

W33_CSV = Path(
    r"/mnt/data/repo_extract/data/_workbench/02_geometry/W33_line_phase_map.csv"
)
N12_CAND = Path(
    r"/mnt/data/repo_extract/data/_n12/n12_58_candidate_w33_points_40_from_tau_cycles_and_fixed_complements_20260109t134000z.csv"
)
TWO_T = Path(
    r"/mnt/data/repo_extract/data/_n12/n12_58_2t_holonomy_nontrivial_cycles.csv"
)
MAP_W33_TO_N12 = Path("outputs/w33_to_n12_mapping.csv")

ALLMASK = (1 << 12) - 1


def tri_to_mask(tri: str) -> int:
    m = 0
    for ch in tri.strip():
        if ch == "a":
            v = 10
        elif ch == "b":
            v = 11
        else:
            v = int(ch)
        m |= 1 << v
    return m


def parse_supports(s: str):
    parts = str(s).split("|")
    out = []
    for part in parts:
        nums = [int(x) for x in part.strip().split()]
        if len(nums) == 4:
            out.append(nums)
    return out


def main():
    w33 = pd.read_csv(W33_CSV)
    w33["pts"] = (
        w33["point_ids"].astype(str).apply(lambda s: tuple(int(x) for x in s.split()))
    )
    lines = {int(r.line_id): frozenset(r.pts) for r in w33.itertuples(index=False)}

    # collinearity
    col_neighbors = [set() for _ in range(40)]
    for pts in lines.values():
        pts = list(pts)
        for i in range(4):
            for j in range(i + 1, 4):
                a, b = pts[i], pts[j]
                col_neighbors[a].add(b)
                col_neighbors[b].add(a)

    non_neighbors = [
        set(p for p in range(40) if p != i and p not in col_neighbors[i])
        for i in range(40)
    ]
    triads = []
    for a in range(40):
        for b in [x for x in non_neighbors[a] if x > a]:
            cand = non_neighbors[a].intersection(non_neighbors[b])
            for c in [x for x in cand if x > b]:
                triads.append((a, b, c))

    four_center = []
    for a, b, c in triads:
        centers = col_neighbors[a].intersection(col_neighbors[b], col_neighbors[c])
        if len(centers) == 4:
            four_center.append((a, b, c))
    assert len(four_center) == 360

    # triad adjacency (share 2 points)
    pair_to_triads = {}
    for idx, (a, b, c) in enumerate(four_center):
        for u, v in [(a, b), (a, c), (b, c)]:
            key = (min(u, v), max(u, v))
            pair_to_triads.setdefault(key, []).append(idx)
    neighbors = [set() for _ in range(360)]
    for ids in pair_to_triads.values():
        if len(ids) > 1:
            for i in ids:
                neighbors[i].update([j for j in ids if j != i])
    neighbors_arr = np.array([sorted(list(s)) for s in neighbors], dtype=np.int16)

    # N12 masks
    cand = pd.read_csv(N12_CAND)
    cand["tri_list"] = (
        cand["members"]
        .fillna("")
        .apply(lambda s: [t for t in re.split(r"[,\s]+", str(s)) if t])
    )
    cand["mask"] = cand["tri_list"].apply(
        lambda tris: (
            int(np.bitwise_or.reduce([tri_to_mask(t) for t in tris])) if tris else 0
        )
    )
    mask_by_point = dict(zip(cand["point_id"], cand["mask"].astype(int)))

    mdf = pd.read_csv(MAP_W33_TO_N12)
    mapping = dict(zip(mdf["w33_point"].astype(int), mdf["n12_point"]))

    pm = np.array([mask_by_point[mapping[i]] for i in range(40)], dtype=np.int32)
    triad_arr = np.array(four_center, dtype=np.int16)
    tm = pm[triad_arr[:, 0]] | pm[triad_arr[:, 1]] | pm[triad_arr[:, 2]]
    cover12 = tm == ALLMASK
    hist = pd.Series([int(x).bit_count() for x in tm]).value_counts().sort_index()
    print("four-center triad cover-size histogram:")
    print(hist.to_string())
    print("cover12:", int(cover12.sum()), "/ 360")

    two = pd.read_csv(TWO_T)
    two["support_list"] = two["supports"].apply(parse_supports)
    two["support_masks"] = two["support_list"].apply(
        lambda lst: [sum(1 << n for n in nums) for nums in lst]
    )

    cost = cover12.astype(np.int16)

    def reconstruct(support_masks):
        L = len(support_masks)
        allowed = [(tm & sm) == sm for sm in support_masks]
        starts = np.nonzero(allowed[0])[0]
        INF = 10**9
        best = INF
        for s in starts:
            dp = np.full((L, 360), INF, dtype=np.int32)
            prev = np.full((L, 360), -1, dtype=np.int16)
            dp[0, s] = cost[s]
            for t in range(1, L):
                vs = np.nonzero(allowed[t])[0]
                for v in vs:
                    u_nei = neighbors_arr[v]
                    vals = dp[t - 1, u_nei]
                    m = vals.min()
                    if m >= INF:
                        continue
                    dp[t, v] = cost[v] + m
                    prev[t, v] = u_nei[vals.argmin()]
            for u in np.nonzero(allowed[L - 1])[0]:
                if s in neighbors_arr[u] and dp[L - 1, u] < best:
                    best = int(dp[L - 1, u])
        return best

    totals = []
    for i, row in two.iterrows():
        c = reconstruct(row["support_masks"])
        totals.append(c)
    print("per-cycle minimal cover12:", totals, "total:", sum(totals))


if __name__ == "__main__":
    main()
