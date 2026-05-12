#!/usr/bin/env python3
"""Export Tomotope → internal Reye-style mapping.

This script takes the incidence data produced by
`scripts/tomotope_edges_faces_incidence.py` and exports a simple JSON
mapping that treats the 12 edge orbits and 16 face orbits as a labeled
Reye 12₄16₃ configuration:

  - edge orbit i  ↔  point P_i
  - face orbit j  ↔  line  L_j

together with the 12×16 incidence matrix M[i][j].

This is an "internal" Reye labeling: it does not try to match a
canonical Reye from the literature, but it fixes a concrete, stable
labeling that can be composed later with any external Reye labeling.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
INC_PATH = DATA_DIR / "tomotope_edges_faces_incidence.json"
OUT_PATH = DATA_DIR / "tomotope_reye_mapping_internal.json"


def main() -> None:
    if not INC_PATH.exists():
        raise SystemExit(f"Incidence file not found: {INC_PATH}. Run scripts/tomotope_edges_faces_incidence.py first.")

    data = json.loads(INC_PATH.read_text(encoding="utf-8"))
    M = data["incidence"]
    edge_count = data["edge_count"]
    face_count = data["face_count"]

    # Sanity checks on sizes
    if edge_count != 12:
        print(f"[warning] expected 12 edges, found {edge_count}")
    if face_count != 16:
        print(f"[warning] expected 16 faces, found {face_count}")

    edges_to_points = {f"E{i}": f"P{i}" for i in range(edge_count)}
    faces_to_lines = {f"F{j}": f"L{j}" for j in range(face_count)}

    out = {
        "edge_count": edge_count,
        "face_count": face_count,
        "edges_to_reye_points": edges_to_points,
        "faces_to_reye_lines": faces_to_lines,
        "incidence": M,
        "note": (
            "This is an internal Reye labeling: edge orbit i is labeled as point P_i, "
            "face orbit j as line L_j. The 12x16 incidence matrix M is copied from "
            "tomotope_edges_faces_incidence.json. External canonical Reye labelings "
            "can be related to this one by permutations of the 12 points and 16 lines."
        ),
    }

    OUT_PATH.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("Tomotope→internal Reye mapping written to", OUT_PATH)


if __name__ == "__main__":
    main()
