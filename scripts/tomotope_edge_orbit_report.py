#!/usr/bin/env python3
"""Tomotope edge-orbit and generator alignment report.

This script refines `scripts/analyze_tomotope_edges.py` by:

1. Reconstructing the 96-element symmetry group acting on 192 flags.
2. Computing edge orbits (12 edges) as flag orbits under r0, r2, r3.
3. Computing the induced permutation of r1 on the 12 edges.
4. Loading the published tomotope generators p0..p3 from
   `data/maniplex_tables/tomotope_permutation_summary.json`.
5. Writing a JSON report that can be used to match the internal edge
   model to the published maniplex generators up to relabeling.

This does not assume any particular relabeling; it just exposes the data
needed to finish the isomorphism by eye or with further group code.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
BUNDLE_DIR = ROOT / "TOE_tomotope_flag_model_conjugacy_v01_20260228_bundle" / "TOE_tomotope_flag_model_conjugacy_v01_20260228"


def load_H_elements() -> list[dict[str, Any]]:
    path = ROOT / "axis_line_stabilizer_192.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["elements"]


def load_orbit96() -> dict[int, int]:
    path = BUNDLE_DIR / "flag_orbits_under_symmetry96.csv"
    orbit96: dict[int, int] = {}
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            orbit96[int(row["flag_index"])] = int(row["orbit96"])
    return orbit96


def build_H_regular(H_perms: list[dict[str, Any]]) -> list[tuple[int, ...]]:
    index_map: dict[tuple[tuple[int, ...], tuple[int, ...]], int] = {}
    for i, g in enumerate(H_perms):
        key = (tuple(g["perm"]), tuple(g["signs"]))
        index_map[key] = i

    regular: list[tuple[int, ...]] = []
    for g in H_perms:
        perm1, sign1 = g["perm"], g["signs"]
        img: list[int] = []
        for h in H_perms:
            perm2, sign2 = h["perm"], h["signs"]
            newperm = [None] * len(perm1)
            newsign = [None] * len(sign1)
            for i in range(len(perm1)):
                j = perm2[i] - 1
                newperm[i] = perm1[j]
                newsign[i] = sign1[j] * sign2[i]
            img.append(index_map[(tuple(newperm), tuple(newsign))])
        regular.append(tuple(img))
    return regular


def extract_sym96(H_regular: list[tuple[int, ...]], orbit96: dict[int, int]) -> list[int]:
    sym96: list[int] = []
    for idx, perm in enumerate(H_regular):
        ok = True
        for f, orb in orbit96.items():
            if orbit96[perm[f]] != orb:
                ok = False
                break
        if ok:
            sym96.append(idx)
    return sym96


def load_flag_adjacency() -> dict[str, list[int]]:
    path = BUNDLE_DIR / "flag_adjacency_r0_r3_permutations.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    result: dict[str, list[int]] = {}
    for key in ["r0", "r1", "r2", "r3"]:
        perm = data[key]
        result[key] = [int(x) for x in perm]
    return result


def orbit_under(start: int, generators: list[list[int]]) -> set[int]:
    O = {start}
    stack = [start]
    while stack:
        u = stack.pop()
        for g in generators:
            v = g[u]
            if v not in O:
                O.add(v)
                stack.append(v)
    return O


def compute_edges(flag_adj: dict[str, list[int]]) -> list[list[int]]:
    r0, r2, r3 = flag_adj["r0"], flag_adj["r2"], flag_adj["r3"]
    edges: list[list[int]] = []
    visited: set[int] = set()

    for f in range(192):
        if f in visited:
            continue
        orb = orbit_under(f, [r0, r2, r3])
        visited.update(orb)
        edges.append(sorted(orb))

    return edges


def induced_perm_on_edges(generator: list[int], edges: list[list[int]]) -> list[int]:
    perm_edges: list[int] = []
    for ei, orb in enumerate(edges):
        image = generator[orb[0]]
        target_idx = None
        for ej, o2 in enumerate(edges):
            if image in o2:
                target_idx = ej
                break
        if target_idx is None:
            raise RuntimeError("generator does not map edge to an edge orbit")
        perm_edges.append(target_idx)
    return perm_edges


def load_published_tomotope_generators() -> dict[str, list[int]]:
    path = DATA_DIR / "maniplex_tables" / "tomotope_permutation_summary.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    parsed = data["parsed_generators"]
    p_maps: dict[str, list[int]] = {}
    for name, mp in parsed.items():
        perm = [int(mp.get(str(i + 1), i + 1)) - 1 for i in range(12)]
        p_maps[name] = perm
    return p_maps


def build_report() -> dict[str, Any]:
    H_perms = load_H_elements()
    orbit96 = load_orbit96()
    H_reg = build_H_regular(H_perms)
    sym96 = extract_sym96(H_reg, orbit96)

    flag_adj = load_flag_adjacency()
    edges = compute_edges(flag_adj)
    sizes = Counter(len(o) for o in edges)

    r1_edges = induced_perm_on_edges(flag_adj["r1"], edges)
    p_maps = load_published_tomotope_generators()

    return {
        "summary": {
            "H_size": len(H_perms),
            "H_regular_size": len(H_reg),
            "sym96_size": len(sym96),
            "edge_count": len(edges),
            "edge_orbit_sizes": dict(sizes),
        },
        "sym96_indices": sym96,
        "edges_as_flag_orbits": edges,
        "r1_on_edges": r1_edges,
        "published_generators": p_maps,
        "notes": (
            "Edges are orbits of flags under <r0, r2, r3>. r1_on_edges is the induced "
            "permutation of r1 on the 12 edges. published_generators are the maniplex "
            "p0..p3 permutations on 12 edges from tomotope_permutation_summary.json. "
            "Matching r1_on_edges to one of p_maps[name] up to relabeling completes the "
            "edge-generator isomorphism."
        ),
    }


def main() -> None:
    report = build_report()
    out_path = DATA_DIR / "tomotope_edge_orbits_report.json"
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("Tomotope edge-orbit report written to", out_path)
    print("Summary:")
    for k, v in report["summary"].items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
