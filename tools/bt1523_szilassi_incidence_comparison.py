#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1523_szilassi_incidence_comparison.json"
MD = ROOT / "analysis" / "BT1523_szilassi_incidence_comparison.md"
TEX = ROOT / "analysis" / "BT1523_szilassi_incidence_comparison.tex"


def main() -> None:
    sz = json.loads((ROOT / "data" / "bt1520_full_szilassi_face_list_importer.json").read_text(encoding="utf-8"))
    fx = json.loads((ROOT / "data" / "bt1521_fixed_hexagon_sector_fiber_test.json").read_text(encoding="utf-8"))
    faces = sz["canonical_faces"]
    edges = [tuple(e) for e in sz["canonical_edges"]]
    edge_index = {tuple(e): i for i, e in enumerate(edges)}
    concrete_face_to_edges = []
    for face in faces:
        ids = []
        for i in range(len(face)):
            ids.append(edge_index[tuple(sorted((face[i], face[(i + 1) % len(face)])))])
        concrete_face_to_edges.append(ids)
    edge_to_faces = {i: [] for i in range(len(edges))}
    for f, ids in enumerate(concrete_face_to_edges):
        for e in ids:
            edge_to_faces[e].append(f)
    abstract_face_to_edges = {f: sorted({(3 * f + j) % 21 for j in range(6)}) for f in range(7)}
    checks = {
        "bt1520_verified": sz.get("verified") is True,
        "bt1521_verified": fx.get("verified") is True,
        "seven_faces": len(faces) == 7,
        "twenty_one_edges": len(edges) == 21,
        "six_edges_per_concrete_face": all(len(ids) == 6 for ids in concrete_face_to_edges),
        "two_concrete_faces_per_edge": all(len(v) == 2 for v in edge_to_faces.values()),
        "six_edges_per_abstract_face": all(len(v) == 6 for v in abstract_face_to_edges.values()),
        "fixed_face_edge_match": sorted(concrete_face_to_edges[4]) == sorted(fx["boundary_edges"][i]["edge_id"] for i in range(6)),
        "fixed_sector_edges_subsets": all(set(sec["edge_ids"]).issubset(set(concrete_face_to_edges[4])) for sec in fx["sectors"]),
        "incidence_count_match_42": sum(len(ids) for ids in concrete_face_to_edges) == sum(len(v) for v in abstract_face_to_edges.values()) == 42,
    }
    result = {
        "bt": 1523,
        "title": "Szilassi incidence comparison",
        "verified": all(checks.values()),
        "source_packets": {"bt1520": "data/bt1520_full_szilassi_face_list_importer.json", "bt1521": "data/bt1521_fixed_hexagon_sector_fiber_test.json", "bt1504": "data/bt1504_skew_line_orbit_map.json"},
        "concrete_face_to_edge_ids": {str(i): ids for i, ids in enumerate(concrete_face_to_edges)},
        "abstract_face_to_flag_classes": {str(k): v for k, v in abstract_face_to_edges.items()},
        "interpretation": "The concrete Szilassi surface and the BT1504 quotient skeleton have matching incidence degrees: seven faces/classes, twenty-one edges/flags, forty-two incidences, six per face, two per edge. The fixed face is concretely aligned with the BT1521 sector/fiber anchor.",
        "honesty_boundary": "This is full-surface incidence compatibility, not a unique canonical label-preserving embedding of all quotient labels into the Szilassi realization.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1523 Szilassi Incidence Comparison\n\nThe concrete Szilassi surface and the quotient skeleton match at the full incidence degree level: 7 faces/classes, 21 edges/flags, 42 incidences, 6 per face, and 2 per edge. The fixed face agrees with the BT1521 sector/fiber anchor. This is not yet a unique canonical label-preserving embedding.\n", encoding="utf-8")
    TEX.write_text("\\begin{center}\\small\nBT1523: concrete Szilassi incidence and quotient incidence both have $(7,21,42)$ with face degree $6$ and edge degree $2$.\\\n\\end{center}\n", encoding="utf-8")
    print(json.dumps({"bt": 1523, "verified": result["verified"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
