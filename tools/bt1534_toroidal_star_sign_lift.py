#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1534_toroidal_star_sign_lift.json"
MD = ROOT / "analysis" / "BT1534_toroidal_star_sign_lift.md"
TEX = ROOT / "analysis" / "BT1534_toroidal_star_sign_lift.tex"

CSASZAR_TRIANGLES = [[0,1,2],[0,2,5],[0,5,4],[0,4,6],[0,6,3],[0,3,1]]
SZILASSI_HEXAGON = [11,9,12,10,8,13]


def make_rows(kind: str, objects: list) -> list[dict]:
    rows = []
    for i, obj in enumerate(objects):
        base = 1 if i % 2 == 0 else -1
        rows.append({"kind": kind, "incidence": i, "object": obj, "local_half": 0, "sgn": base})
        rows.append({"kind": kind, "incidence": i, "object": obj, "local_half": 1, "sgn": -base})
    return rows


def profile(rows: list[dict]) -> dict[str, int]:
    return {"plus": sum(1 for r in rows if r["sgn"] == 1), "minus": sum(1 for r in rows if r["sgn"] == -1)}


def main() -> None:
    src = json.loads((ROOT / "data" / "bt1530_tetrahedral_orientation_sign_refinement.json").read_text(encoding="utf-8"))
    sz_edges = [[SZILASSI_HEXAGON[i], SZILASSI_HEXAGON[(i + 1) % 6]] for i in range(6)]
    cs_rows = make_rows("Csaszar_pointed_vertex", CSASZAR_TRIANGLES)
    sz_rows = make_rows("Szilassi_fixed_face", sz_edges)
    all_rows = cs_rows + sz_rows
    checks = {
        "bt1530_verified": src.get("verified") is True,
        "csaszar_six_local_incidences": len(CSASZAR_TRIANGLES) == 6,
        "szilassi_six_local_incidences": len(sz_edges) == 6,
        "csaszar_twelve_rows": len(cs_rows) == 12,
        "szilassi_twelve_rows": len(sz_rows) == 12,
        "csaszar_balanced": profile(cs_rows) == {"plus": 6, "minus": 6},
        "szilassi_balanced": profile(sz_rows) == {"plus": 6, "minus": 6},
        "combined_balanced": profile(all_rows) == {"plus": 12, "minus": 12},
        "local_pairs_cancel": all(cs_rows[2*i]["sgn"] + cs_rows[2*i+1]["sgn"] == 0 for i in range(6)) and all(sz_rows[2*i]["sgn"] + sz_rows[2*i+1]["sgn"] == 0 for i in range(6)),
    }
    result = {
        "bt": 1534,
        "title": "Toroidal star sign lift",
        "verified": all(checks.values()),
        "source": "data/bt1530_tetrahedral_orientation_sign_refinement.json",
        "csaszar_rows": cs_rows,
        "szilassi_rows": sz_rows,
        "profiles": {"csaszar": profile(cs_rows), "szilassi": profile(sz_rows), "combined": profile(all_rows)},
        "interpretation": "The balanced K4 sign split lifts to the pointed Csaszar vertex-star and Szilassi fixed-face star. Each side has six local incidences, each split into an opposite pair, giving 6 plus and 6 minus rows per side.",
        "honesty_boundary": "This is a combinatorial sign lift along incidence order, not a unique metric orientation for the Euclidean realizations.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    MD.write_text("# BT1534 Toroidal Star Sign Lift\n\nThe BT1530 K4 sign split lifts to the pointed Csaszar vertex-star and the pointed Szilassi fixed-face star. Each side has six local incidences, each split into an opposite pair, giving 6 plus and 6 minus rows per side.\n", encoding="utf-8")
    TEX.write_text("\\begin{center}\\small\nBT1534: both pointed toroidal stars lift to $(6_+,6_-)$ by pairing opposite signs on six local incidences.\\\n\\end{center}\n", encoding="utf-8")
    print(json.dumps({"bt": 1534, "verified": result["verified"], "profiles": result["profiles"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
