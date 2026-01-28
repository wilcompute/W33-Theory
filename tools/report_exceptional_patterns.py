#!/usr/bin/env python3
"""Report Coxeter‑6 orbits that intersect W(E6) size‑1 roots (exceptional patterns)."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    inter = json.loads((ROOT / "artifacts" / "we6_coxeter6_intersection.json").read_text())
    orbit_map = json.loads((ROOT / "artifacts" / "e8_orbit_to_f3_point.json").read_text())
    mapping = orbit_map["mapping"]

    matrix = inter["matrix"]
    # size-1 orbits are columns 7..12 (after 72 + 6x27)
    # We flag any row with a 1 in these columns.
    exceptional = []
    for i, row in enumerate(matrix):
        if any(row[j] == 1 for j in range(7, 13)):
            exceptional.append((i, row))

    print(f"Exceptional Coxeter‑6 orbits (involving size‑1 roots): {len(exceptional)}")
    for i, row in exceptional:
        point = mapping[str(i)]
        print(f"  orbit {i}: row={row}  point={point}")

    out = {
        "exceptional_orbits": [{"orbit": i, "row": row, "point": mapping[str(i)]} for i, row in exceptional]
    }
    (ROOT / "artifacts" / "exceptional_we6_patterns.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print("Wrote artifacts/exceptional_we6_patterns.json")


if __name__ == "__main__":
    main()
