#!/usr/bin/env python3
"""Export the root->edge mapping to CSV/Markdown tables.

Reads artifacts_archive/e8_root_to_w33_edge.json and writes:
- artifacts_archive/e8_root_to_w33_edge.csv
- artifacts_archive/e8_root_to_w33_edge.md
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    src = ROOT / "artifacts_archive" / "e8_root_to_w33_edge.json"
    if not src.exists():
        raise SystemExit("Missing artifacts_archive/e8_root_to_w33_edge.json")

    data = json.loads(src.read_text(encoding="utf-8"))
    root_to_edge = data.get("root_to_edge", {})

    rows = []
    for root_str, edge in root_to_edge.items():
        # root_str is like "[0, 1, ...]"
        root_vec = root_str.strip()
        u, v = edge
        rows.append((u, v, root_vec))

    # Sort by edge then root
    rows.sort(key=lambda r: (r[0], r[1], r[2]))

    out_csv = ROOT / "artifacts_archive" / "e8_root_to_w33_edge.csv"
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["w33_u", "w33_v", "root_vector"])
        w.writerows(rows)

    out_md = ROOT / "artifacts_archive" / "e8_root_to_w33_edge.md"
    with out_md.open("w", encoding="utf-8") as f:
        f.write("# E8 Root -> W33 Edge Mapping\n\n")
        f.write("| w33_u | w33_v | root_vector |\n")
        f.write("| --- | --- | --- |\n")
        for u, v, root_vec in rows:
            f.write(f"| {u} | {v} | `{root_vec}` |\n")

    print(f"Wrote {out_csv}")
    print(f"Wrote {out_md}")


if __name__ == "__main__":
    main()
