#!/usr/bin/env python3
from __future__ import annotations

import argparse, json
from pathlib import Path

ROWS = [
    {"name":"diam10_A", "order":51840, "diameter":10, "edge":"K2+2I/K4-e", "spread":67, "endpoint":"8:16"},
    {"name":"diam10_B", "order":51840, "diameter":10, "edge":"2K2/C4", "spread":0, "endpoint":"6:32,7:40,8:76"},
    {"name":"diam10_C", "order":51840, "diameter":10, "edge":"empty_4I/K4", "spread":0, "endpoint":"8:3"},
    {"name":"diam12", "order":51840, "diameter":12, "edge":"P3+I/paw", "spread":339, "endpoint":"7:4,8:1"},
    {"name":"diam14_polar_path", "order":51840, "diameter":14, "edge":"P4/P4", "spread":172, "endpoint":"8:1"},
]


def score(row):
    closure = 1 if row["order"] == 51840 else 0
    diameter = 1 if row["diameter"] == 14 else 0
    polar_path = 1 if row["edge"] == "P4/P4" else 0
    endpoint_all = 1 if row["endpoint"] == "8:1" else 0
    labelled_nonzero = 1 if row["spread"] > 0 else 0
    strict_score = closure + diameter + polar_path + endpoint_all + labelled_nonzero
    return {
        "closure51840": closure,
        "diameter14": diameter,
        "polar_path_P4P4": polar_path,
        "unique_all_channel_endpoint": endpoint_all,
        "labelled_nonzero_spread": labelled_nonzero,
        "channel_spread": row["spread"],
        "strict_score_out_of_5": strict_score,
    }


def build():
    rows = []
    for r in ROWS:
        merged = dict(r)
        merged["score_vector"] = score(r)
        rows.append(merged)
    ranked = sorted(rows, key=lambda r: (r["score_vector"]["strict_score_out_of_5"], r["diameter"], r["score_vector"]["polar_path_P4P4"]), reverse=True)
    return {
        "bt": 1264,
        "title": "Tomography score vector for full-order Clifford regimes",
        "score_components": ["closure51840", "diameter14", "polar_path_P4P4", "unique_all_channel_endpoint", "labelled_nonzero_spread"],
        "rows": rows,
        "ranked_names": [r["name"] for r in ranked],
        "winner": ranked[0]["name"],
        "interpretation": "Only the diameter-14 polar path regime satisfies all five gates. Diameter 12 has a strong labelled signal but fails the word diameter and polar path gates. Diameter-10 regimes close too fast and are rejected despite full closure."
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=Path("data/bt1264_tomography_score_vector_summary.json"))
    ns = ap.parse_args()
    result = build()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt":1264, "winner":result["winner"], "out":str(ns.out)}, indent=2))


if __name__ == "__main__":
    main()
