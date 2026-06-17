#!/usr/bin/env python3
from __future__ import annotations

import argparse, json
from pathlib import Path

BASE = [(0,0,0,2), (0,2,0,0), (0,0,2,2), (1,0,0,0)]


def sp(u,v):
    a,b,c,d = v
    jv = (c % 3, d % 3, (-a) % 3, (-b) % 3)
    return sum(ui*ji for ui,ji in zip(u,jv)) % 3


def build():
    zero_edges = []
    nonzero_edges = []
    for i in range(4):
        for j in range(i+1,4):
            val = sp(BASE[i], BASE[j])
            edge = [i,j]
            if val == 0:
                zero_edges.append(edge)
            else:
                nonzero_edges.append(edge)
    return {
        "bt": 1252,
        "title": "Polar path tetrahedron identifier",
        "vectors": [list(v) for v in BASE],
        "symplectic_zero_edges": zero_edges,
        "symplectic_nonzero_edges": nonzero_edges,
        "zero_edge_graph": "P4",
        "nonzero_edge_graph": "P4",
        "self_complementary_edge_split": True,
        "pair_order_pattern": "9^3 24^3",
        "triple_order_pattern": "72^2 648^2",
        "proposed_name": "polar path tetrahedron",
        "meaning": "The BT1228/BT1233 diameter-14 regime is a tetrahedron whose polar/commuting edges form a path P4; the nonpolar edges form the complementary path P4. This self-complementary path split realizes the balanced local closure law."
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("data/bt1252_polar_path_tetrahedron_identifier_summary.json"))
    ns = ap.parse_args()
    result = build()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt": 1252, "name": result["proposed_name"], "zero_graph": result["zero_edge_graph"], "out": str(ns.out)}, indent=2))


if __name__ == "__main__":
    main()
