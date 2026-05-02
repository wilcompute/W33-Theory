#!/usr/bin/env python3
"""
PART CLXXIII - Eisenstein Torus Map Bridge
==========================================

The bottom of Abstract Polytope Tables Final.pdf lists toroidal maps:

    {3,6}_{(1,0)}, {3,6}_{(2,0)}, {3,6}_{(1,1)}, {3,6}_{(2,1)}
    {6,3}_{(1,0)}, {6,3}_{(2,0)}, {6,3}_{(1,1)}, {6,3}_{(2,1)}

The two relevant maps are:

    {3,6}_{(2,1)}: V=7,  E=21, F=14   -> Csaszar K7 triangulated torus
    {6,3}_{(2,1)}: V=14, E=21, F=7    -> Szilassi dual hexagonal torus

The hidden rule is the Eisenstein / triangular-lattice norm

    N(b,c) = b^2 + b c + c^2.

For a {3,6}_{(b,c)} torus map:

    V=N, E=3N, F=2N.

For its dual {6,3}_{(b,c)} torus map:

    V=2N, E=3N, F=N.

At (b,c)=(2,1):

    N = 2^2 + 2*1 + 1^2 = 7 = Phi6.

This is exactly the Csaszar/Szilassi pair:

    {3,6}_{(2,1)} = (7,21,14),
    {6,3}_{(2,1)} = (14,21,7).

In W33 variables, (b,c)=(q-1,1), so

    N(q-1,1) = (q-1)^2 + (q-1) + 1 = q^2 - q + 1 = Phi6.

Thus the toroidal map parameter itself generates Phi6 by an Eisenstein norm.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Tuple

ROOT = Path(__file__).resolve().parent

Q = 3
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
K = 12
J = 5
J_INV = 8

MAP_PARAMS = [(1, 0), (2, 0), (1, 1), (2, 1)]


def eisenstein_norm(b: int, c: int) -> int:
    return b * b + b * c + c * c


def map_36_counts(b: int, c: int) -> Tuple[int, int, int]:
    n = eisenstein_norm(b, c)
    return (n, 3 * n, 2 * n)


def map_63_counts(b: int, c: int) -> Tuple[int, int, int]:
    n = eisenstein_norm(b, c)
    return (2 * n, 3 * n, n)


@dataclass(frozen=True)
class TorusMapRow:
    symbol: str
    b: int
    c: int
    norm: int
    vertices: int
    edges: int
    faces: int
    role: str


def torus_map_rows() -> List[TorusMapRow]:
    roles = {
        (1, 0): "origin/fundamental one-cell torus quotient",
        (2, 0): "q+1=4 tetrahedral/quarter seed quotient",
        (1, 1): "q=3 axis seed quotient",
        (2, 1): "Phi6=7 Csaszar/Szilassi torus quotient",
    }
    rows: List[TorusMapRow] = []
    for b, c in MAP_PARAMS:
        v, e, f = map_36_counts(b, c)
        rows.append(TorusMapRow("{3,6}", b, c, eisenstein_norm(b, c), v, e, f, roles[(b, c)]))
        v, e, f = map_63_counts(b, c)
        rows.append(TorusMapRow("{6,3}", b, c, eisenstein_norm(b, c), v, e, f, "dual of " + roles[(b, c)]))
    return rows


def eisenstein_torus_map_bridge_audit() -> Dict[str, object]:
    rows = torus_map_rows()
    norms = {param: eisenstein_norm(*param) for param in MAP_PARAMS}
    cs = map_36_counts(2, 1)
    sz = map_63_counts(2, 1)
    checks = {
        "norm_values_match_bottom_pdf_sequence": [norms[p] for p in MAP_PARAMS] == [1, 4, 3, 7],
        "phi6_from_2_1_norm": eisenstein_norm(2, 1) == PHI6 == 7,
        "phi6_from_q_minus_one_one_norm": eisenstein_norm(Q - 1, 1) == PHI6,
        "csaszar_counts_from_36_2_1": cs == (7, 21, 14),
        "szilassi_counts_from_63_2_1": sz == (14, 21, 7),
        "dual_swap_preserves_edges": cs[1] == sz[1] == 21,
        "dual_swap_vertices_faces": cs[0] == sz[2] and cs[2] == sz[0],
        "torus_euler_characteristic_cs": cs[0] - cs[1] + cs[2] == 0,
        "torus_euler_characteristic_sz": sz[0] - sz[1] + sz[2] == 0,
        "edge_count_is_three_phi6": cs[1] == 3 * PHI6 == 21,
        "face_count_cs_is_two_phi6": cs[2] == 2 * PHI6 == 14,
        "vertex_count_sz_is_two_phi6": sz[0] == 2 * PHI6 == 14,
        "one_four_three_seven_contains_origin_qp1_q_phi6": set(norms.values()) == {1, Q + 1, Q, PHI6},
        "phi6_is_norm_after_q_middle": PHI6 == 7,
    }
    assert all(checks.values())

    return {
        "module": "PART_CLXXIII_EISENSTEIN_TORUS_MAP_BRIDGE",
        "source_pdf": "Abstract Polytope Tables Final.pdf bottom map tables for {3,6}_{(b,c)} and {6,3}_{(b,c)}",
        "w33_atoms": {
            "q": Q,
            "Phi3": PHI3,
            "Phi4": PHI4,
            "Phi6": PHI6,
            "k": K,
            "J": J,
            "J_inverse": J_INV,
        },
        "norm_rule": {
            "formula": "N(b,c)=b^2+bc+c^2",
            "map_36_counts": "{3,6}_{(b,c)} has (V,E,F)=(N,3N,2N)",
            "map_63_counts": "{6,3}_{(b,c)} has (V,E,F)=(2N,3N,N)",
            "w33_specialization": "N(q-1,1)=q^2-q+1=Phi6",
        },
        "map_rows": [asdict(r) for r in rows],
        "csaszar_szilassi_identification": {
            "Csaszar": "{3,6}_{(2,1)}=(7,21,14)",
            "Szilassi": "{6,3}_{(2,1)}=(14,21,7)",
            "shared_edge_count": 21,
            "dual_swap": "V and F swap; E is preserved",
        },
        "checks": checks,
        "theorem_statement": (
            "The bottom PDF's {3,6}/{6,3} maps are Eisenstein-norm torus quotients.  "
            "For N(b,c)=b^2+bc+c^2, {3,6}_{(b,c)} has (N,3N,2N) and its dual {6,3}_{(b,c)} "
            "has (2N,3N,N).  At (b,c)=(2,1)=(q-1,1), N=7=Phi6, giving Csaszar (7,21,14) "
            "and Szilassi (14,21,7)."
        ),
        "interpretive_note": (
            "This is the missing map-level generator for Phi6.  The toroidal realization count, the decimal denominator, "
            "and the Csaszar/Szilassi map size all arise from the same triangular-lattice/Eisenstein norm N(q-1,1)."
        ),
    }


def main() -> int:
    audit = eisenstein_torus_map_bridge_audit()
    out = ROOT / "PART_CLXXIII_eisenstein_torus_map_bridge_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
