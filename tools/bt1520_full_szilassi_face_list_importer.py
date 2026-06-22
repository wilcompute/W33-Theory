#!/usr/bin/env python3
"""BT1520: import the full Szilassi face list and exact 21-edge table.

This extends BT1517 from the fixed hexagon anchor to all seven concrete hexagonal
faces in both Szilassi realization versions from Toroidal-Polyhedra-Realizations.
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "Toroidal-Polyhedra-Realizations.txt"
OUT = ROOT / "data" / "bt1520_full_szilassi_face_list_importer.json"
MD = ROOT / "analysis" / "BT1520_full_szilassi_face_list_importer.md"
TEX = ROOT / "analysis" / "BT1520_full_szilassi_face_list_importer.tex"


def parse_szilassi_faces() -> list[dict]:
    txt = DATA.read_text(encoding="utf-8")
    blocks = re.split(r"\n(?=(?:Csaszar|Szilassi) Polyhedron \(version \d\))", txt)
    rows = []
    for block in blocks:
        m = re.match(r"(Csaszar|Szilassi) Polyhedron \(version (\d)\)", block)
        if not m or m.group(1) != "Szilassi":
            continue
        version = int(m.group(2))
        faces_part = block.split("Faces:", 1)[-1]
        faces = [[int(x) for x in fm.group(1).split(",")] for fm in re.finditer(r"\{([^}]+)\}", faces_part)]
        rows.append({"version": version, "faces": faces})
    return rows


def edge_table(faces: list[list[int]]) -> tuple[list[tuple[int, int]], dict[tuple[int, int], list[int]]]:
    edge_to_faces: dict[tuple[int, int], list[int]] = defaultdict(list)
    for fi, face in enumerate(faces):
        n = len(face)
        for i in range(n):
            edge = tuple(sorted((face[i], face[(i + 1) % n])))
            edge_to_faces[edge].append(fi)
    edges = sorted(edge_to_faces)
    return edges, edge_to_faces


def main() -> None:
    versions = parse_szilassi_faces()
    imported = []
    for row in versions:
        faces = row["faces"]
        edges, edge_to_faces = edge_table(faces)
        face_to_edge_ids = []
        edge_index = {e: i for i, e in enumerate(edges)}
        for face in faces:
            ids = []
            for i in range(len(face)):
                ids.append(edge_index[tuple(sorted((face[i], face[(i + 1) % len(face)])))])
            face_to_edge_ids.append(ids)
        imported.append({
            "version": row["version"],
            "faces": faces,
            "edges": [list(e) for e in edges],
            "edge_to_faces": {str(list(e)): fs for e, fs in edge_to_faces.items()},
            "face_to_edge_ids": face_to_edge_ids,
            "degree_profile": dict(Counter(len(fs) for fs in edge_to_faces.values())),
        })
    reference_faces = imported[0]["faces"] if imported else []
    reference_edges = imported[0]["edges"] if imported else []
    checks = {
        "two_szilassi_versions": len(imported) == 2,
        "seven_faces_each": all(len(r["faces"]) == 7 for r in imported),
        "all_faces_hexagons": all(all(len(face) == 6 for face in r["faces"]) for r in imported),
        "twenty_one_edges_each": all(len(r["edges"]) == 21 for r in imported),
        "each_edge_two_faces": all(r["degree_profile"] == {2: 21} or r["degree_profile"] == {"2": 21} for r in imported),
        "total_face_edge_incidences_42": all(sum(len(ids) for ids in r["face_to_edge_ids"]) == 42 for r in imported),
        "versions_have_same_face_lists": all(r["faces"] == reference_faces for r in imported),
        "versions_have_same_edges": all(r["edges"] == reference_edges for r in imported),
        "fixed_face_present": all(r["faces"][4] == [11, 9, 12, 10, 8, 13] for r in imported),
    }
    result = {
        "bt": 1520,
        "title": "Full Szilassi face-list importer",
        "verified": all(checks.values()),
        "source": "data/Toroidal-Polyhedra-Realizations.txt",
        "versions": imported,
        "canonical_faces": reference_faces,
        "canonical_edges": reference_edges,
        "interpretation": "All seven Szilassi hexagons and the exact 21-edge table are now imported concretely. Both realization versions share the same combinatorial face and edge lists, with every edge incident to exactly two faces.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1520 Full Szilassi Face-list Importer\n\nImported both Szilassi realization versions. Each has seven hexagonal faces, twenty-one edges, forty-two face-edge incidences, and every edge is incident to exactly two faces. The two versions share the same combinatorial face and edge lists.\n", encoding="utf-8")
    lines = [r"\begin{center}\small", r"\begin{tabular}{c|c}", r"\toprule", r"Face & Boundary vertices\\", r"\midrule"]
    for i, face in enumerate(reference_faces):
        lines.append(f"{i} & {face}\\")
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{center}"])
    TEX.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1520, "verified": result["verified"], "faces": len(reference_faces), "edges": len(reference_edges)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
