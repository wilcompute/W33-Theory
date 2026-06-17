#!/usr/bin/env python3
from __future__ import annotations

import argparse, json
from collections import Counter, defaultdict, deque
from itertools import combinations, product
from pathlib import Path

MOD = 3
I4 = (1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1)
LABELS = ["g1p", "g1m", "g2p", "g2m", "g3p", "g3m", "g4p", "g4m"]
SAMPLES = {
    "diam10_A": {"edge_zero_graph": "K2+2I", "indices": [0,16,29,37]},
    "diam10_B": {"edge_zero_graph": "2K2", "indices": [0,14,28,33]},
    "diam10_C": {"edge_zero_graph": "empty_4I", "indices": [0,22,30,35]},
    "diam12": {"edge_zero_graph": "P3+I", "indices": [0,8,11,30]},
    "diam14_polar_path": {"edge_zero_graph": "P4", "indices": [0,1,7,13]},
}


def mm(a,b):
    return tuple(sum(a[4*i+k]*b[4*k+j] for k in range(4)) % MOD for i in range(4) for j in range(4))


def canon(v):
    vv = list(v)
    first = next(x for x in vv if x % MOD)
    return tuple((2*x) % MOD for x in vv) if first == 2 else tuple(x % MOD for x in vv)


def vecs40():
    seen, out = set(), []
    for v in product(range(MOD), repeat=4):
        if v == (0,0,0,0):
            continue
        c = canon(v)
        if c not in seen:
            seen.add(c); out.append(c)
    return out


def tv(v):
    a,b,c,d = v
    jv = (c % MOD, d % MOD, (-a) % MOD, (-b) % MOD)
    outer = [(vi * wj) % MOD for vi in v for wj in jv]
    return tuple((I4[i] + outer[i]) % MOD for i in range(16))


def profile(indices):
    vecs = vecs40()
    gens = []
    for i in indices:
        g = tv(vecs[i])
        gens.extend([g, mm(g,g)])
    dist = {I4: 0}; q = deque([I4])
    while q:
        x = q.popleft()
        for g in gens:
            y = mm(x,g)
            if y not in dist:
                dist[y] = dist[x] + 1; q.append(y)
    diameter = max(dist.values())
    by_dist = defaultdict(list)
    for x,d in dist.items(): by_dist[d].append(x)
    first = {I4: set()}; invs = [mm(g,g) for g in gens]
    for d in range(1, diameter + 1):
        for y in by_dist[d]:
            fs = set()
            for lab,g,ginv in zip(LABELS, gens, invs):
                x = mm(y, ginv)
                if dist.get(x) == d - 1 and mm(x,g) == y:
                    fs.add(lab) if d == 1 else fs.update(first[x])
            first[y] = fs
    first_total = {lab: 0 for lab in LABELS}
    for x,d in dist.items():
        if d:
            for lab in first[x]: first_total[lab] += 1
    vals = list(first_total.values())
    dia_hist = Counter(len(first[x]) for x in by_dist[diameter])
    sphere = Counter(dist.values())
    return {
        "order": len(dist),
        "diameter": diameter,
        "sphere_histogram": [sphere[i] for i in range(diameter + 1)],
        "first_channel_totals": first_total,
        "channel_total_multiset": sorted(vals),
        "distinct_channel_totals": sorted(set(vals)),
        "channel_total_spread": max(vals) - min(vals),
        "diameter_first_set_size_histogram": {str(k): v for k,v in sorted(dia_hist.items())},
    }


def build():
    rows = []
    for name, meta in SAMPLES.items():
        row = {"name": name, "edge_zero_graph": meta["edge_zero_graph"]}
        row.update(profile(meta["indices"]))
        rows.append(row)
    return {
        "bt": 1260,
        "title": "Cross-regime labelled geodesic comparison",
        "rows": rows,
        "interpretation": "Labelled geodesic tensors refine both the unlabelled sphere and edge graph regimes. Some fast diameter-10 regimes are total-channel balanced, diameter-12 has the largest spread, and the polar-path diameter-14 regime has a unique all-channel endpoint with nonzero total-channel imbalance."
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("data/bt1260_cross_regime_labelled_geodesic_comparison_summary.json"))
    ns = ap.parse_args()
    result = build(); ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt":1260, "rows":len(result["rows"]), "out":str(ns.out)}, indent=2))


if __name__ == "__main__":
    main()
