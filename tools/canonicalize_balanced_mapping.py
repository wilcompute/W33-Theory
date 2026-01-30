#!/usr/bin/env python3
"""Canonicalize the balanced-orbit Schlaefli labeling using anchors.

Anchors:
1) The unique all-integral triangle is labeled as (E1, C2, L12).
2) The axis V-shape lines are labeled as (E1, E4, C2).
We search over S6 permutations and optional E<->C swap to enforce this.
"""

from __future__ import annotations

import json
from itertools import permutations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def apply_perm(line, perm, swap_ec):
    t = line[0]
    if t in ("E", "C"):
        idx = perm[line[1] - 1]
        t2 = t
        if swap_ec:
            t2 = "C" if t == "E" else "E"
        return (t2, idx)
    # L lines
    i, j = perm[line[1] - 1], perm[line[2] - 1]
    if i > j:
        i, j = j, i
    return ("L", i, j)


def main():
    iso = json.loads(
        (ROOT / "artifacts" / "balanced_orbit_schlafli_isomorphism.json").read_text()
    )
    mapping_full = iso["mapping_full"]

    tri = json.loads(
        (ROOT / "artifacts" / "balanced_triangle_phase_alignment.json").read_text()
    )
    triangles = tri["triangles"]

    # Identify the unique all-integral triangle
    all_int = None
    for t in triangles:
        if all(rt == "integral" for rt in t["root_types"]):
            all_int = [tuple(L) for L in t["lines"]]
            break
    if all_int is None:
        print("No all-integral triangle found")
        return

    # Axis V-shape lines from subgraph component nodes
    sub = json.loads((ROOT / "artifacts" / "balanced_orbit_subgraph.json").read_text())
    nodes = sub["component_summaries"][0]["nodes"]
    vshape_lines = [tuple(mapping_full[str(n)]["line"]) for n in nodes]

    # Canonical target for the unique all-integral triangle
    target_triangle = {("E", 1), ("C", 2), ("L", 1, 2)}

    solutions = []
    for perm in permutations([1, 2, 3, 4, 5, 6]):
        for swap in [False, True]:
            tri_mapped = {apply_perm(L, perm, swap) for L in all_int}
            if tri_mapped != target_triangle:
                continue
            v_mapped = {apply_perm(L, perm, swap) for L in vshape_lines}
            # Require V-shape to be {C2, E_a, E_b} with distinct E's
            if ("C", 2) not in v_mapped:
                continue
            e_indices = sorted([x[1] for x in v_mapped if x[0] == "E"])
            if len(e_indices) != 2 or e_indices[0] == e_indices[1]:
                continue
            solutions.append({"perm": perm, "swap": swap, "vshape_E": tuple(e_indices)})
        if solutions:
            break

    if not solutions:
        print("No canonicalization found with given anchors")
        return

    # Choose solution with lexicographically smallest E-pair in V-shape
    sol = sorted(solutions, key=lambda s: s["vshape_E"])[0]
    perm = sol["perm"]
    swap = sol["swap"]

    # Produce canonical mapping
    canonical = {}
    for k, info in mapping_full.items():
        line = tuple(info["line"])
        line2 = apply_perm(line, perm, swap)
        canonical[k] = {
            "line": line2,
            "phase": info["phase"],
            "root_type": info["root_type"],
        }

    results = {
        "perm": perm,
        "swap_ec": swap,
        "all_integral_triangle": all_int,
        "vshape_lines": vshape_lines,
        "canonical_mapping": canonical,
    }

    out_path = ROOT / "artifacts" / "balanced_orbit_canonical_mapping.json"
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(results)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
