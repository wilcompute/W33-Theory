#!/usr/bin/env python3
"""Sample disjoint K6 pairs (double-six candidates) and compute stabilizer orbits in Aut(W33).

Looking for a stabilizer that has a 27-point orbit (candidate Schlaefli embedding).
"""
from __future__ import annotations

import random
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ART = ROOT / "artifacts"
ART.mkdir(exist_ok=True)

from tools.find_k6_double_sixes_w33_fast import bron_kerbosch_bounded
from tools.find_schlafli_embedding_in_w33 import (compute_w33_lines,
                                                  construct_w33_points)
from tools.w33_aut_group_construct import build_points, generate_group


def compute_stabilizer_for_pair(A, B, group):
    Aset = set(A)
    Bset = set(B)
    stab = []
    for g in group:
        Ag = {g[i] for i in Aset}
        Bg = {g[i] for i in Bset}
        if (Ag == Aset and Bg == Bset) or (Ag == Bset and Bg == Aset):
            stab.append(g)
    return stab


def sample(n_samples=200):
    pts = construct_w33_points()
    lines = compute_w33_lines(pts)
    n = len(lines)
    G = {i: set() for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if set(lines[i]).isdisjoint(set(lines[j])):
                G[i].add(j)
                G[j].add(i)

    # find all K6 cliques
    cliques = []
    bron_kerbosch_bounded(G, set(), set(range(n)), set(), 6, cliques)
    print("Total K6 cliques:", len(cliques))

    # build group
    pts = build_points()
    group, gens = generate_group(pts)
    group = list(group)
    print("Loaded group of size", len(group))

    found = []
    for it in range(n_samples):
        a = set(random.choice(cliques))
        b = set(random.choice(cliques))
        if a & b:
            continue
        stab = compute_stabilizer_for_pair(a, b, group)
        order = len(stab)
        # compute orbit sizes on points under this stabilizer
        orbits = []
        seen = set()
        for i in range(n):
            if i in seen:
                continue
            # orbit of i
            orb = {g[i] for g in stab}
            for x in orb:
                seen.add(x)
            orbits.append(len(orb))
        if 27 in orbits:
            print("Found stabilizer with orbit 27; order", order)
            return {
                "A": sorted(list(a)),
                "B": sorted(list(b)),
                "stab_order": order,
                "orbits": orbits,
            }
        found.append(order)
    print("Sampled stabilizer orders (Counter):", Counter(found))
    return None


if __name__ == "__main__":
    res = sample(300)
    print("Result:", res)
