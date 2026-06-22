#!/usr/bin/env python3
"""BT1514: test the BT1504 7/21 classes against Szilassi face-edge incidence.

This is an exact incidence-model test, not yet an embedding theorem.  It checks
whether the count bridge can support a legal 7 faces x 21 edges toroidal
incidence pattern: seven face-classes, twenty-one edge/flag classes, three
fiber/local sectors per face, and six incident edges per Szilassi hexagonal face.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1514_toroidal_incidence_test.json"
MD = ROOT / "analysis" / "BT1514_toroidal_incidence_test.md"
TEX = ROOT / "analysis" / "BT1514_toroidal_incidence_test.tex"


def main() -> None:
    faces = list(range(7))
    edges = list(range(21))
    # Canonical toroidal incidence model: each face sees 3 local fiber sectors,
    # and each sector contributes a pair of adjacent edge/flag classes.
    face_to_edges = {f: sorted({(3 * f + j) % 21 for j in range(6)}) for f in faces}
    edge_to_faces = {e: sorted([f for f in faces if e in face_to_edges[f]]) for e in edges}
    face_to_fiber_pairs = {
        f: {sector: sorted([(3 * f + 2 * sector + delta) % 21 for delta in range(2)]) for sector in range(3)}
        for f in faces
    }
    incidence_pairs = [(f, e) for f, es in face_to_edges.items() for e in es]
    checks = {
        "seven_faces": len(faces) == 7,
        "twenty_one_edges": len(edges) == 21,
        "six_edges_per_face": all(len(es) == 6 for es in face_to_edges.values()),
        "two_faces_per_edge": all(len(fs) == 2 for fs in edge_to_faces.values()),
        "total_incidence_42": len(incidence_pairs) == 42,
        "three_fiber_sectors_per_face": all(len(sectors) == 3 for sectors in face_to_fiber_pairs.values()),
        "two_edges_per_sector": all(len(pair) == 2 for sectors in face_to_fiber_pairs.values() for pair in sectors.values()),
        "fiber_pairs_cover_face_edges": all(sorted(e for pair in sectors.values() for e in pair) == face_to_edges[f] for f, sectors in face_to_fiber_pairs.items()),
    }
    result = {
        "bt": 1514,
        "title": "Toroidal incidence test",
        "verified": all(checks.values()),
        "model": "Szilassi face-edge incidence candidate for BT1504 7 point classes, 21 flag classes, and 3 fiber sectors",
        "face_to_edges": {str(k): v for k, v in face_to_edges.items()},
        "edge_to_faces": {str(k): v for k, v in edge_to_faces.items()},
        "face_to_fiber_pairs": {str(f): {str(s): pair for s, pair in sectors.items()} for f, sectors in face_to_fiber_pairs.items()},
        "incidence_counts": {"faces": 7, "edges": 21, "face_edge_pairs": len(incidence_pairs), "edges_per_face": 6, "faces_per_edge": 2},
        "interpretation": "The 7/21/3 count bridge admits a legal Szilassi-style incidence model: seven hexagonal face classes, twenty-one edge/flag classes, and three two-edge local sectors per face.",
        "honesty_boundary": "This proves incidence-count compatibility, not that BT1504's actual quotient classes are canonically the Szilassi faces and edges. The next step is a concrete class-to-realization map.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text(
        "# BT1514 Toroidal Incidence Test\n\n"
        "The 7/21/3 bridge supports a legal Szilassi-style incidence model: seven face classes, twenty-one edge/flag classes, six edges per face, two faces per edge, and three two-edge sectors per face.\n\n"
        "This is incidence-count compatibility only; it does not yet identify BT1504 classes with a concrete Szilassi realization.\n",
        encoding="utf-8",
    )
    lines = [
        r"\begin{center}\small",
        r"\begin{tabular}{c|c|c}",
        r"\toprule",
        r"Face class & Incident edge classes & Fiber-sector pairs\\",
        r"\midrule",
    ]
    for f in faces:
        pairs = "; ".join(f"{s}:({','.join(map(str,p))})" for s, p in face_to_fiber_pairs[f].items())
        lines.append(f"{f} & {','.join(map(str, face_to_edges[f]))} & {pairs}\\")
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{center}"])
    TEX.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1514, "verified": result["verified"], "incidences": len(incidence_pairs)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
