#!/usr/bin/env python3
"""Build a consolidated feature table for the 8 W(E6) pattern classes.

Outputs:
- artifacts/pattern_class_feature_table.json
- artifacts/pattern_class_feature_table.md
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_json(name):
    return json.loads((ROOT / "artifacts" / name).read_text())


def main():
    # Load artifacts
    inter = load_json("we6_coxeter6_intersection.json")
    h12 = load_json("pattern_class_h12_h27_profile.json")
    k4 = load_json("pattern_class_k4_profile.json")
    exc = load_json("exceptional_we6_patterns.json")
    quotient = load_json("pattern_quotient_graph.json")
    support = load_json("pattern_class_support_sizes.json")

    # Build class feature summary
    classes = sorted(int(k) for k in h12["class_summary"].keys())
    summary = {}
    for c in classes:
        ckey = str(c)
        size = h12["class_summary"][ckey]["size"]
        avg_neighbors = h12["class_summary"][ckey]["avg_neighbor_class_counts"]

        # K4 participation
        outer_count = k4["outer_class_counts"].get(ckey, 0)
        center_count = k4["center_class_counts"].get(ckey, 0)

        summary[ckey] = {
            "size": size,
            "support_size_counts": support.get(ckey, {}),
            "avg_neighbor_class_counts": avg_neighbors,
            "k4_outer_count": outer_count,
            "k4_center_count": center_count,
        }

    out = {
        "class_count": len(classes),
        "class_summary": summary,
        "exceptional_orbits": exc["exceptional_orbits"],
        "quotient_graph": {
            "num_classes": quotient["num_classes"],
            "class_sizes": quotient["class_sizes"],
            "adjacency_counts": quotient["adjacency_counts"],
        },
    }

    (ROOT / "artifacts" / "pattern_class_feature_table.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )

    # Markdown table
    lines = []
    lines.append("# Pattern Class Feature Table")
    lines.append("")
    lines.append("| Class | Size | Support sizes | K4 outer count | K4 center count | Avg neighbor class counts |")
    lines.append("|---|---:|---|---:|---:|---|")
    for c in classes:
        ckey = str(c)
        s = summary[ckey]
        support_str = ",".join(f"{k}:{v}" for k,v in sorted(s["support_size_counts"].items()))
        avg = ",".join(f"{x:.2f}" for x in s["avg_neighbor_class_counts"])
        lines.append(f"| {ckey} | {s['size']} | {support_str} | {s['k4_outer_count']} | {s['k4_center_count']} | {avg} |")

    (ROOT / "artifacts" / "pattern_class_feature_table.md").write_text("\n".join(lines), encoding="utf-8")

    print("Wrote artifacts/pattern_class_feature_table.json")
    print("Wrote artifacts/pattern_class_feature_table.md")


if __name__ == "__main__":
    main()
