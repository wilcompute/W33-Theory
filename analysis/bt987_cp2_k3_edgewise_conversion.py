#!/usr/bin/env python3
"""
BT987 — CP2_9 / K3_16 edgewise conversion scaffold.

The existing curved 4D bridge uses vertex-minimal CP2_9 and K3_16 seeds, but
its refinement family is barycentric.  BT983 shows this is the wrong theorem
carrier for CMS/Dodziuk-Patodi/FEEC because barycentric refinement is not
shape-regular.  BT987 records the replacement interface for the actual seeds:
edgewise/Freudenthal-Kuhn refinement of each 4-simplex.

Important: without explicit facet lists for the published CP2_9 and K3_16
triangulations, this script does not pretend to build the full subdivided
complex.  It records the exact top-dimensional multiplier and the migration
points that downstream scripts must change.  For a 4-simplex, edgewise k=2
subdivision produces 2^4 = 16 shape-regular 4-simplices, while barycentric
subdivision produces 5! = 120 4-simplices.  Therefore all barycentric density
constants using the 120 multiplier must be rederived for edgewise refinement.
"""
from __future__ import annotations

import json
from math import comb
from pathlib import Path


def neighborly_4manifold_f_vector(n: int) -> tuple[int, int, int, int, int]:
    f0 = n
    f1 = comb(n, 2)
    f2 = comb(n, 3)
    f4 = (3 * f2 - 2 * f1) // 5
    f3 = 5 * f4 // 2
    return (f0, f1, f2, f3, f4)


def chi(fv: tuple[int, int, int, int, int]) -> int:
    return sum(((-1) ** i) * fv[i] for i in range(5))


def seed_packet(name: str, vertices: int) -> dict:
    fv = neighborly_4manifold_f_vector(vertices)
    levels = []
    for level in range(7):
        edge_top = fv[4] * (16 ** level)
        bary_top = fv[4] * (120 ** level)
        levels.append({
            "level": level,
            "edgewise_top_4simplices": edge_top,
            "barycentric_top_4simplices": bary_top,
            "barycentric_over_edgewise_ratio": (120 / 16) ** level,
        })
    return {
        "name": name,
        "vertices": vertices,
        "f_vector": fv,
        "euler_characteristic": chi(fv),
        "edgewise_top_multiplier_per_step": 16,
        "barycentric_top_multiplier_per_step": 120,
        "levels": levels,
    }


def main() -> None:
    out = {
        "theorem": "BT987 CP2_9/K3_16 edgewise conversion scaffold",
        "reason": "BT983 showed barycentric refinement is not a valid CMS/DP/FEEC theorem-carrier; edgewise refinement is the fat replacement.",
        "seeds": [seed_packet("CP2_9", 9), seed_packet("K3_16", 16)],
        "migration_patch_points": [
            "exploration/w33_minimal_triangulation_bridge.py: replace barycentric_subdivision_f_vector with edgewise facet refinement once explicit facets are loaded",
            "exploration/w33_curved_barycentric_density_bridge.py: do not reuse 120/19 and 860/19 density constants; rederive edgewise density constants",
            "exploration/w33_transport_curved_dirac_refinement_bridge.py: rename barycentric tower references and route heat-density samples through the edgewise tower",
            "w33_paper.tex / OPEN_FRONTIERS.md: state CP2_9/K3_16 R3 verification now means edgewise/fat refinement, not barycentric refinement"
        ],
        "boundary": "This scaffold records exact top-simplex growth and migration points. Full lower-dimensional f-vectors and incidence matrices require explicit CP2_9/K3_16 facet lists, not just neighborly f-vectors.",
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt987_cp2_k3_edgewise_conversion.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
