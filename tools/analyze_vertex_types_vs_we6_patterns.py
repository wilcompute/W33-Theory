#!/usr/bin/env python3
"""Analyze W33 vertex types vs W(E6) orbit intersection patterns.

Uses:
- artifacts/we6_coxeter6_intersection.json (40 Coxeter‑6 orbits and patterns)
- artifacts/e8_orbit_to_f3_point.json (orbit -> F3^4 point)

Outputs a summary table mapping:
- pattern -> counts of F3^4 support sizes
- pattern -> list of orbit ids
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def support_size(p):
    return sum(1 for x in p if x != 0)


def main():
    inter = json.loads((ROOT / "artifacts" / "we6_coxeter6_intersection.json").read_text())
    orbit_map = json.loads((ROOT / "artifacts" / "e8_orbit_to_f3_point.json").read_text())
    mapping = orbit_map["mapping"]

    matrix = inter["matrix"]  # list of 40 rows

    pattern_to_orbits = defaultdict(list)
    pattern_to_sizes = defaultdict(Counter)

    for orb_id, row in enumerate(matrix):
        pat = tuple(row)
        pattern_to_orbits[pat].append(orb_id)

        point = mapping[str(orb_id)]
        sz = support_size(point)
        pattern_to_sizes[pat][sz] += 1

    # Build summary
    summary = []
    for pat, orbs in sorted(pattern_to_orbits.items(), key=lambda x: (-len(x[1]), x[0])):
        sizes = dict(pattern_to_sizes[pat])
        summary.append({
            "pattern": pat,
            "count": len(orbs),
            "support_size_counts": sizes,
            "orbits": orbs,
        })

    out = {
        "patterns": summary,
        "note": "support_size counts are over F3^4 projective points for each Coxeter‑6 orbit",
    }

    (ROOT / "artifacts" / "vertex_type_vs_we6_pattern.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )

    # Print a compact summary
    print("Pattern summary (count -> support sizes):")
    for item in summary:
        print(f"{item['count']} orbits, sizes={item['support_size_counts']}, pattern={item['pattern']}")

    print("Wrote artifacts/vertex_type_vs_we6_pattern.json")


if __name__ == "__main__":
    main()
