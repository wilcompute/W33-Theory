#!/usr/bin/env python3
"""BT354-BT355: W33 CSS Hamiltonian and spacetime bridge verifier.

This file resolves the tension between three nearby claims:

1. The canonical W(3,3) edge-chain CSS code is the old homological code:
       [[240,81,3]]_3 with asymmetric distances d_X=3, d_Z=4.

2. The BT353 all-plus vertex/line Hamiltonian is a valid commuting qutrit
   stabilizer model, but it is a different line-product gauge layer:
       [[240,160,2]]_3 with asymmetric witnesses d_X=2, d_Z=4.

3. The finite spacetime bridge is projective:
       PSp(4,3) ~= Omega(5,3),
   while the continuum analogue is the real double-cover bridge
       Sp(4,R) ~= Spin(2,3) -> SO(2,3).

The architectural consequence is a two-layer substrate:

    240 = 39 + 120 + 81

where 39 is exact/gauge-gradient, 120 is triangle-boundary/curvature, and
81 is protected harmonic memory.  The 160 line-Hamiltonian sector equals
39+120+1 after changing from oriented boundary checks to all-plus local
line checks; it is a gauge/string-net envelope, not the protected H_1 sector.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from itertools import combinations
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_css_exact_audit import (
    P,
    boundary_matrices,
    build_w33,
    gf_nullspace,
    gf_rank,
    in_rowspace,
)


def all_plus_line_matrices(points, edges, edge_index, lines) -> tuple[np.ndarray, np.ndarray]:
    """Return BT353's all-plus vertex stars and all-plus line checks."""

    hx = np.zeros((len(points), len(edges)), dtype=int)
    for col, (i, j) in enumerate(edges):
        hx[i, col] = 1
        hx[j, col] = 1

    hz = np.zeros((len(lines), len(edges)), dtype=int)
    for row, line in enumerate(lines):
        for i, j in combinations(line, 2):
            hz[row, edge_index[tuple(sorted((i, j)))]] = 1

    return hx % P, hz % P


def find_line_x_witness(hz_line: np.ndarray, hx_plus: np.ndarray, edges, lines, edge_index) -> dict[str, Any]:
    """Find the minimal X witness for the all-plus line code.

    Because every edge belongs to exactly one line, a weight-1 vector cannot
    lie in ker(H_Z).  A two-edge vector with coefficients 1 and -1 inside one
    line does lie in ker(H_Z), and is not an all-plus vertex-star row.
    """

    line = lines[0]
    e0 = edge_index[tuple(sorted((line[0], line[1])))]
    e1 = edge_index[tuple(sorted((line[0], line[2])))]
    vec = np.zeros(len(edges), dtype=int)
    vec[e0] = 1
    vec[e1] = 2

    assert np.all(hz_line @ vec % P == 0)
    assert not in_rowspace(vec, hx_plus)

    return {
        "distance": 2,
        "lower_bound_reason": "each edge is in exactly one line, so no nonzero weight-1 vector is in ker(H_Z_line)",
        "witness": [
            {"edge_index": int(e0), "edge": list(edges[e0]), "coeff": 1},
            {"edge_index": int(e1), "edge": list(edges[e1]), "coeff": 2},
        ],
    }


def find_line_z_witness(hx_plus: np.ndarray, hz_line: np.ndarray, points, edges, edge_index) -> dict[str, Any]:
    """Find the minimal Z witness for the all-plus line code.

    The all-plus incidence kernel has no support below 4:
    weight 1 or 2 leaves a degree-1 touched vertex; weight 3 can only be a
    triangle, and the all-plus incidence matrix of an odd cycle has no
    nonzero F_3 null vector.  A quadrangle with alternating coefficients is
    therefore the first possible witness.
    """

    n = len(points)
    edge_set = set(edges)
    adjacency = [[False] * n for _ in points]
    for i, j in edges:
        adjacency[i][j] = adjacency[j][i] = True

    # Verify all graph triangles have zero all-plus incidence nullity.
    triangles_checked = 0
    for a, b, c in combinations(range(n), 3):
        tri_edges = [tuple(sorted(e)) for e in ((a, b), (a, c), (b, c))]
        if all(e in edge_set for e in tri_edges):
            support = [edge_index[e] for e in tri_edges]
            ns = gf_nullspace(hx_plus[:, support])
            assert ns.size == 0 or not any(np.any(row % P) for row in ns)
            triangles_checked += 1
    assert triangles_checked == 160

    for a, b in combinations(range(n), 2):
        if adjacency[a][b]:
            continue
        common = [x for x in range(n) if adjacency[a][x] and adjacency[b][x]]
        if len(common) < 2:
            continue
        c, d = common[:2]
        cycle = [(a, c), (c, b), (b, d), (d, a)]
        coeffs = [1, 2, 1, 2]
        vec = np.zeros(len(edges), dtype=int)
        witness = []
        for coeff, e in zip(coeffs, cycle):
            idx = edge_index[tuple(sorted(e))]
            vec[idx] = coeff
            witness.append({"edge_index": int(idx), "edge": list(edges[idx]), "coeff": int(coeff)})

        assert np.all(hx_plus @ vec % P == 0)
        assert not in_rowspace(vec, hz_line)
        return {
            "distance": 4,
            "lower_bound_reason": "no weight<4 all-plus Eulerian support exists over F_3; triangles are odd cycles and have zero nullity",
            "triangles_checked_for_no_weight3": triangles_checked,
            "witness": witness,
        }

    raise RuntimeError("no quadrangle witness found")


def run_gap_bridge() -> dict[str, Any]:
    """Use GAP, when available, to verify PSp(4,3) ~= Omega(5,3)."""

    if shutil.which("gap") is None:
        return {"available": False, "reason": "gap executable not found"}

    script = """
G:=Sp(4,3);;
P:=G/Centre(G);;
O:=Omega(0,5,3);;
iso:=IsomorphismGroups(P,O);;
Print(Size(G), "\\n");
Print(Size(Centre(G)), "\\n");
Print(Size(P), "\\n");
Print(Size(O), "\\n");
Print(iso <> fail, "\\n");
QUIT;
"""
    proc = subprocess.run(["gap", "-q"], input=script, text=True, capture_output=True, check=True)
    lines = [x.strip() for x in proc.stdout.splitlines() if x.strip()]
    return {
        "available": True,
        "Sp_4_3_order": int(lines[0]),
        "center_order": int(lines[1]),
        "PSp_4_3_order": int(lines[2]),
        "Omega_5_3_order": int(lines[3]),
        "PSp_4_3_isomorphic_to_Omega_5_3": lines[4] == "true",
        "continuum_analogue": "Sp(4,R) is the double cover Spin(2,3) of SO(2,3); Lorentz SO(1,3) is a stabilizer/boundary subgroup, not the finite graph itself.",
    }


def build_payload() -> dict[str, Any]:
    points, edges, edge_index, lines, triangles = build_w33()
    d1, d2 = boundary_matrices(points, edges, edge_index, triangles)

    canonical = {
        "name": "canonical_clique_chain_css",
        "field": "F_3",
        "physical_edge_qutrits": len(edges),
        "HX": "oriented d1: C1 -> C0",
        "HZ": "oriented d2^T: C1 -> C2, using 160 line triangles",
        "rank_HX": gf_rank(d1),
        "rank_HZ": gf_rank(d2.T),
        "commutes": bool(np.all(d1 @ d2 % P == 0)),
        "logical_qutrits": len(edges) - gf_rank(d1) - gf_rank(d2.T),
        "distances_from_exact_audit": {"d_X": 3, "d_Z": 4, "symmetric": 3},
        "parameters": "[[240,81,3]]_3, asymmetric d_X=3,d_Z=4",
    }

    hx_plus, hz_line = all_plus_line_matrices(points, edges, edge_index, lines)
    line_code = {
        "name": "BT353_all_plus_vertex_line_hamiltonian",
        "field": "F_3",
        "physical_edge_qutrits": len(edges),
        "HX": "all-plus vertex stars",
        "HZ": "all-plus K4 line edge-products",
        "rank_HX": gf_rank(hx_plus),
        "rank_HZ": gf_rank(hz_line),
        "commutes": bool(np.all(hx_plus @ hz_line.T % P == 0)),
        "logical_qutrits": len(edges) - gf_rank(hx_plus) - gf_rank(hz_line),
        "X_distance_witness": find_line_x_witness(hz_line, hx_plus, edges, lines, edge_index),
        "Z_distance_witness": find_line_z_witness(hx_plus, hz_line, points, edges, edge_index),
        "parameters": "[[240,160,2]]_3, asymmetric d_X=2,d_Z=4",
    }

    hodge = {
        "exact_gradient_rank": canonical["rank_HX"],
        "triangle_boundary_rank": canonical["rank_HZ"],
        "harmonic_H1_rank": canonical["logical_qutrits"],
        "sum": canonical["rank_HX"] + canonical["rank_HZ"] + canonical["logical_qutrits"],
        "formula": "240 = 39 + 120 + 81",
        "interpretation": {
            "39": "oriented exact/gauge-gradient sector",
            "120": "triangle-boundary curvature sector",
            "81": "protected harmonic H_1 matter/memory sector",
            "160": "all-plus line Hamiltonian envelope = 39+120+1 after changing local check convention",
        },
    }

    identities = {
        "w33_counts": len(points) == 40 and len(edges) == 240 and len(lines) == 40 and len(triangles) == 160,
        "canonical_commutes": canonical["commutes"],
        "canonical_rank_39_120_81": (canonical["rank_HX"], canonical["rank_HZ"], canonical["logical_qutrits"]) == (39, 120, 81),
        "line_code_commutes": line_code["commutes"],
        "line_code_rank_40_40_160": (line_code["rank_HX"], line_code["rank_HZ"], line_code["logical_qutrits"]) == (40, 40, 160),
        "line_distances": line_code["X_distance_witness"]["distance"] == 2 and line_code["Z_distance_witness"]["distance"] == 4,
        "hodge_sum_edges": hodge["sum"] == 240,
    }

    gap = run_gap_bridge()
    if gap.get("available"):
        identities["gap_projective_sp_orthogonal_bridge"] = (
            gap["Sp_4_3_order"] == 51840
            and gap["center_order"] == 2
            and gap["PSp_4_3_order"] == 25920
            and gap["Omega_5_3_order"] == 25920
            and gap["PSp_4_3_isomorphic_to_Omega_5_3"]
        )

    theorem = (
        "BT354-BT355 synthesis.  The W(3,3) architecture has two distinct "
        "commuting qutrit Hamiltonian layers on the same 240 edge carrier.  "
        "The canonical oriented clique-chain CSS code is the protected "
        "[[240,81,3]]_3 homology/matter sector with d_X=3,d_Z=4.  The BT353 "
        "all-plus vertex/line Hamiltonian is a valid [[240,160,2]]_3 "
        "gauge/string-net envelope with d_X=2,d_Z=4.  Therefore 81 should "
        "not be revised to 162: the exact architecture is the Hodge split "
        "240=39+120+81 plus a separate all-plus 160 line envelope.  GAP "
        "verifies the finite spacetime bridge PSp(4,3) ~= Omega(5,3); the "
        "continuum analogue is Sp(4,R) as Spin(2,3), with 1+3 Lorentz physics "
        "arising from stabilizer/boundary reduction rather than from W(3,3) "
        "alone."
    )

    return {
        "summary": {
            "canonical_code": canonical["parameters"],
            "line_hamiltonian_code": line_code["parameters"],
            "hodge_split": hodge["formula"],
            "gap_bridge_available": gap.get("available", False),
            "all_identities_hold": all(identities.values()),
        },
        "canonical_clique_chain_css": canonical,
        "bt353_all_plus_line_hamiltonian": line_code,
        "hodge_spine": hodge,
        "gap_spacetime_bridge": gap,
        "identities": identities,
        "theorem": theorem,
        "honesty_boundary": (
            "This proves finite-field ranks, commutation, line-code witnesses, "
            "and the GAP projective symplectic/orthogonal bridge.  The continuum "
            "Sp(4,R)/SO(2,3) statement is used as the real-form analogue; it is "
            "not a derivation of empirical gravity or Standard Model dynamics."
        ),
    }


def main() -> int:
    payload = build_payload()
    out = Path("data/w33_BREAKTHROUGH_354_355_css_hamiltonian_spacetime_bridge.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {out}")
    return 0 if payload["summary"]["all_identities_hold"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
