#!/usr/bin/env python3
from __future__ import annotations

import argparse, json
from itertools import combinations, product
from pathlib import Path

MOD = 3
SAMPLES = {
    "diam10_A": {"count": 12960, "diameter": 10, "indices": [0,16,29,37]},
    "diam10_B": {"count": 3240, "diameter": 10, "indices": [0,14,28,33]},
    "diam10_C": {"count": 6480, "diameter": 10, "indices": [0,22,30,35]},
    "diam12": {"count": 25920, "diameter": 12, "indices": [0,8,11,30]},
    "diam14_polar_path": {"count": 12960, "diameter": 14, "indices": [0,1,7,13]},
}


def canon(v):
    vv = list(v)
    first = next(x for x in vv if x % MOD)
    if first == 2:
        vv = [(2*x) % MOD for x in vv]
    else:
        vv = [x % MOD for x in vv]
    return tuple(vv)


def vecs40():
    seen, out = set(), []
    for v in product(range(MOD), repeat=4):
        if v == (0,0,0,0):
            continue
        c = canon(v)
        if c not in seen:
            seen.add(c); out.append(c)
    return out


def sp(u,v):
    a,b,c,d = v
    jv = (c % MOD, d % MOD, (-a) % MOD, (-b) % MOD)
    return sum(ui*ji for ui,ji in zip(u,jv)) % MOD


def classify_graph(edges):
    e = {tuple(sorted(x)) for x in edges}
    deg = [0,0,0,0]
    for a,b in e:
        deg[a] += 1; deg[b] += 1
    ds = sorted(deg)
    m = len(e)
    if m == 0: return "empty_4I"
    if m == 1: return "K2+2I"
    if m == 2 and ds == [0,0,1,1]: return "K2+2I_unexpected"
    if m == 2 and ds == [0,1,1,2]: return "P3+I"
    if m == 2 and ds == [1,1,1,1]: return "2K2"
    if m == 3 and ds == [1,1,2,2]: return "P4"
    if m == 3 and ds == [0,2,2,2]: return "K3+I"
    if m == 4 and ds == [1,2,2,3]: return "paw"
    if m == 4 and ds == [2,2,2,2]: return "C4"
    if m == 5: return "K4-e"
    if m == 6: return "K4"
    return f"m{m}_deg{ds}"


def build():
    vecs = vecs40()
    rows = []
    for name, meta in SAMPLES.items():
        inds = meta["indices"]
        chosen = [vecs[i] for i in inds]
        zero, nonzero = [], []
        for i,j in combinations(range(4),2):
            if sp(chosen[i], chosen[j]) == 0:
                zero.append([i,j])
            else:
                nonzero.append([i,j])
        rows.append({
            "name": name,
            "count": meta["count"],
            "diameter": meta["diameter"],
            "zero_edges": zero,
            "nonzero_edges": nonzero,
            "zero_graph": classify_graph(zero),
            "nonzero_graph": classify_graph(nonzero),
            "sample_indices": inds,
            "sample_vectors": [list(v) for v in chosen]
        })
    return {
        "bt": 1255,
        "title": "Full-order edge graph regime classifier",
        "rows": rows,
        "diameter14_globalization": "BT1248 shows diameter 14 has one full-order orbit, and its representative has zero/nonzero edge split P4/P4. Therefore every diameter-14 full-order four-set is a polar path tetrahedron up to Sp(4,3).",
        "interpretation": "Diameter 10 has three edge-graph types, diameter 12 has a P3+I / paw split, and diameter 14 is the unique self-complementary P4/P4 polar path tetrahedron regime."
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("data/bt1255_full_order_edge_graph_regime_classifier_summary.json"))
    ns = ap.parse_args()
    result = build()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt":1255, "rows":len(result["rows"]), "out":str(ns.out)}, indent=2))


if __name__ == "__main__":
    main()
