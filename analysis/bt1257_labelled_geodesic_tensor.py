#!/usr/bin/env python3
from __future__ import annotations

import argparse, json
from collections import Counter, defaultdict, deque
from pathlib import Path

MOD = 3
I4 = (1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1)
BASE = [(0,0,0,2), (0,2,0,0), (0,0,2,2), (1,0,0,0)]
LABELS = ["g1p", "g1m", "g2p", "g2m", "g3p", "g3m", "g4p", "g4m"]


def mm(a,b):
    return tuple(sum(a[4*i+k]*b[4*k+j] for k in range(4)) % MOD for i in range(4) for j in range(4))


def tv(v):
    a,b,c,d = v
    jv = (c % MOD, d % MOD, (-a) % MOD, (-b) % MOD)
    outer = [(vi * wj) % MOD for vi in v for wj in jv]
    return tuple((I4[i] + outer[i]) % MOD for i in range(16))


def build():
    gens = []
    for v in BASE:
        g = tv(v)
        gens.extend([g, mm(g,g)])
    dist = {I4: 0}
    q = deque([I4])
    while q:
        x = q.popleft()
        for g in gens:
            y = mm(x,g)
            if y not in dist:
                dist[y] = dist[x] + 1
                q.append(y)
    diameter = max(dist.values())
    by_dist = defaultdict(list)
    for x,d in dist.items():
        by_dist[d].append(x)
    first = {I4: set()}
    last = {I4: set()}
    invs = [mm(g,g) for g in gens]
    for d in range(1, diameter + 1):
        for y in by_dist[d]:
            fs, ls = set(), set()
            for lab,g,ginv in zip(LABELS, gens, invs):
                x = mm(y, ginv)
                if dist.get(x) == d - 1 and mm(x,g) == y:
                    if d == 1:
                        fs.add(lab)
                    else:
                        fs.update(first[x])
                    ls.add(lab)
            first[y] = fs
            last[y] = ls
    sphere = Counter(dist.values())
    first_counts = {str(d): {lab:0 for lab in LABELS} for d in range(1, diameter + 1)}
    last_counts = {str(d): {lab:0 for lab in LABELS} for d in range(1, diameter + 1)}
    first_set_size_hist = {str(d): {} for d in range(1, diameter + 1)}
    for x,d in dist.items():
        if d == 0:
            continue
        ds = str(d)
        first_set_size_hist[ds][str(len(first[x]))] = first_set_size_hist[ds].get(str(len(first[x])), 0) + 1
        for lab in first[x]:
            first_counts[ds][lab] += 1
        for lab in last[x]:
            last_counts[ds][lab] += 1
    first_total = {lab: sum(first_counts[str(d)][lab] for d in range(1, diameter + 1)) for lab in LABELS}
    last_total = {lab: sum(last_counts[str(d)][lab] for d in range(1, diameter + 1)) for lab in LABELS}
    selected = {str(d): first_counts[str(d)] for d in [1,2,3,4,8,12,14]}
    return {
        "bt": 1257,
        "title": "Labelled geodesic first/last channel tensor",
        "group_order": len(dist),
        "diameter": diameter,
        "sphere_histogram": [sphere[i] for i in range(diameter + 1)],
        "labels": LABELS,
        "first_channel_counts_selected_distances": selected,
        "last_channel_counts_selected_distances": {str(d): last_counts[str(d)] for d in [1,2,3,4,8,12,14]},
        "first_channel_totals": first_total,
        "last_channel_totals": last_total,
        "first_set_size_histogram_selected_distances": {str(d): first_set_size_hist[str(d)] for d in [1,2,3,4,8,12,14]},
        "label_sensitive": True,
        "interpretation": "The unlabelled sphere is unchanged, but anchored shortest-geodesic first/last-channel incidences distinguish the labelled gate channels. In this BT1228 ordering, g1/g4 channels have total incidence 16197 each while g2/g3 channels have 16025 each."
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("data/bt1257_labelled_geodesic_tensor_summary.json"))
    ns = ap.parse_args()
    result = build()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt":1257, "order":result["group_order"], "diameter":result["diameter"], "out":str(ns.out)}, indent=2))


if __name__ == "__main__":
    main()
