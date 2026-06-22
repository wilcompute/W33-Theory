#!/usr/bin/env python3
"""BT1530: orientation/sign refinement for the K4 24-flag carrier."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1530_tetrahedral_orientation_sign_refinement.json"
MD = ROOT / "analysis" / "BT1530_tetrahedral_orientation_sign_refinement.md"
TEX = ROOT / "analysis" / "BT1530_tetrahedral_orientation_sign_refinement.tex"

VERTICES = list(range(4))
EDGES = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
FACES = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]


def incident_faces(a: int, b: int) -> list[int]:
    return [i for i, f in enumerate(FACES) if a in f and b in f]


def boundary_sign(edge: tuple[int, int], face: tuple[int, int, int]) -> int:
    a, b = edge
    cyclic = [(face[0], face[1]), (face[1], face[2]), (face[2], face[0])]
    if (a, b) in cyclic:
        return 1
    if (b, a) in cyclic:
        return -1
    raise ValueError((edge, face))


def flags() -> list[dict]:
    rows = []
    for ei, edge in enumerate(EDGES):
        a, b = edge
        for vertex in edge:
            vertex_sign = 1 if vertex == a else -1
            for fi in incident_faces(a, b):
                bsign = boundary_sign(edge, FACES[fi])
                flag_sign = vertex_sign * bsign
                rows.append({
                    "flag_id": len(rows),
                    "vertex": vertex,
                    "edge_id": ei,
                    "edge": list(edge),
                    "face_id": fi,
                    "face": list(FACES[fi]),
                    "vertex_sign": vertex_sign,
                    "boundary_sign": bsign,
                    "flag_sign": flag_sign,
                    "star": "Csaszar_pointed" if len(rows) < 12 else "Szilassi_pointed",
                })
    return rows


def sign_profile(rows: list[dict]) -> dict[str, int]:
    return {"positive": sum(1 for r in rows if r["flag_sign"] == 1), "negative": sum(1 for r in rows if r["flag_sign"] == -1)}


def main() -> None:
    src = json.loads((ROOT / "data" / "bt1528_tetrahedral_carrier_realization.json").read_text(encoding="utf-8"))
    rows = flags()
    cs = [r for r in rows if r["star"] == "Csaszar_pointed"]
    sz = [r for r in rows if r["star"] == "Szilassi_pointed"]
    edge_profiles = {str(ei): sign_profile([r for r in rows if r["edge_id"] == ei]) for ei in range(6)}
    checks = {
        "bt1528_verified": src.get("verified") is True,
        "flag_count_24": len(rows) == 24,
        "csaszar_star_12": len(cs) == 12,
        "szilassi_star_12": len(sz) == 12,
        "each_star_balanced_6_6": sign_profile(cs) == {"positive": 6, "negative": 6} and sign_profile(sz) == {"positive": 6, "negative": 6},
        "whole_carrier_balanced_12_12": sign_profile(rows) == {"positive": 12, "negative": 12},
        "each_edge_balanced_2_2": all(p == {"positive": 2, "negative": 2} for p in edge_profiles.values()),
        "signs_are_plus_minus_one": sorted({r["flag_sign"] for r in rows}) == [-1, 1],
    }
    result = {
        "bt": 1530,
        "title": "Tetrahedral orientation/sign refinement",
        "verified": all(checks.values()),
        "source": "data/bt1528_tetrahedral_carrier_realization.json",
        "sign_rule": "flag_sign = vertex_orientation_sign * oriented_face_boundary_sign",
        "profiles": {"carrier": sign_profile(rows), "csaszar_star": sign_profile(cs), "szilassi_star": sign_profile(sz), "edge_profiles": edge_profiles},
        "sample_flags": rows[:12],
        "interpretation": "The K4 24-flag carrier admits a balanced orientation/sign refinement. Both 12-flag pointed-star halves have six positive and six negative flags, and every tetrahedral edge contributes two positive and two negative flags.",
        "honesty_boundary": "This supplies a consistent sign refinement for the tetrahedral carrier; it does not prove a unique physical orientation convention for the toroidal realizations.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1530 Tetrahedral Orientation/Sign Refinement\n\nThe K4 24-flag carrier receives a balanced sign rule: flag_sign = vertex orientation sign times oriented face-boundary sign. Each pointed 12-flag half has six positive and six negative flags, and each tetrahedral edge has a 2/2 sign split.\n", encoding="utf-8")
    TEX.write_text("\\begin{center}\\small\nBT1530: the $K_4$ carrier has sign profile $(12_+,12_-)$, split as $(6_+,6_-)+(6_+,6_-)$.\\\n\\end{center}\n", encoding="utf-8")
    print(json.dumps({"bt": 1530, "verified": result["verified"], "profile": result["profiles"]["carrier"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
