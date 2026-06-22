#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1478_triangle_channel_bridge.json"
TEX = ROOT / "analysis" / "BT1478_triangle_channel_bridge.tex"


def main() -> None:
    strands = list(range(12))
    channels = {f"channel_{c}": [4 * c + b for b in range(4)] for c in range(3)}
    triangles = {f"triangle_{b}": [4 * c + b for c in range(3)] for b in range(4)}
    incidence = []
    for cname, cvals in channels.items():
        for tname, tvals in triangles.items():
            inter = sorted(set(cvals) & set(tvals))
            incidence.append({"channel": cname, "triangle": tname, "intersection": inter, "size": len(inter)})
    checks = {
        "three_channels_partition_12": sorted(sum(channels.values(), [])) == strands,
        "four_triangles_partition_12": sorted(sum(triangles.values(), [])) == strands,
        "channels_have_size_4": all(len(v) == 4 for v in channels.values()),
        "triangles_have_size_3": all(len(v) == 3 for v in triangles.values()),
        "incidence_is_3_by_4_grid": len(incidence) == 12 and all(row["size"] == 1 for row in incidence),
        "each_strand_unique": sorted(row["intersection"][0] for row in incidence) == strands,
    }
    tex = [r"\begin{center}\small", r"\begin{tabular}{c|cccc}", r"\toprule", r" & $T_0$ & $T_1$ & $T_2$ & $T_3$\\", r"\midrule"]
    for c in range(3):
        tex.append(" & ".join([f"$P_{c}$"] + [str(4 * c + b) for b in range(4)]) + r"\\")
    tex.extend([r"\bottomrule", r"\end{tabular}", r"\end{center}"])
    TEX.write_text("\n".join(tex) + "\n", encoding="utf-8")
    result = {
        "bt": 1478,
        "title": "Triangle/channel bridge",
        "verified": all(checks.values()),
        "channels": channels,
        "triangles": triangles,
        "incidence": incidence,
        "tex_table": "analysis/BT1478_triangle_channel_bridge.tex",
        "interpretation": "The 12 closure strands are simultaneously three size-4 channels and four size-3 triangles. The two partitions are transverse and form a 3x4 grid.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1478, "verified": result["verified"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
