#!/usr/bin/env python3
"""
PART CLXX - Simplex Count / Toroidal Flag Carrier Compiler
==========================================================

The fuller toroidal-triad page emphasizes:

    Csaszar / Szilassi edges: 21 = C(7,2)
    flag orbits:             42 = 6*7
    flag count:              84 = 2*42 = 12*7
    next h=6 shared edges:   66 = C(12,2)

CLXIX showed that one W33 edge color is

    80 = q^4 - 1,

and completion gives

    80 + 1 = 81 = q^4 = H1(W33).

CLXX integrates the W33 simplex counts with the toroidal flag counts.

W33 side:
    triangles = 160 = 2(q^4 - 1)
    edges     = 240 = q(q^4 - 1)
    directed  = 480 = 2q(q^4 - 1)

Toroidal side:
    torus edges        = C(Phi6,2) = C(7,2) = 21
    flag orbits        = (2q)*Phi6 = 6*7 = 42
    flag count         = k*Phi6 = 12*7 = 84
    next h=2q edges    = C(k,2) = C(12,2) = 66

Bridge identities:
    42 = 2*C(Phi6,2)
    84 = 4*C(Phi6,2)
    66 = C(k,2) = k(k-1)/2
    66 = Phi3*J + 1 = 13*5+1

So the W33 carrier counts and toroidal flag counts are two projections of the
same q=3 compiler: q^4-1 governs W33 simplex counts, while Phi6 and k govern
toroidal minimal-triangulation flags and the next h=2q closure.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parent

Q = 3
V = 40
K = 12
LAM = 2
MU = 4
PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
RANK_SEED = 2 * Q
J = 5
J_INV = 8
Q4 = Q ** 4
NONZERO_Q4 = Q4 - 1
H1_DIM = Q4
GEN_DIM = Q ** 3

W33_TRIANGLES = V * K * LAM // 6
W33_EDGES = V * K // 2
W33_DIRECTED_EDGES = 2 * W33_EDGES
EDGES_PER_COLOR = W33_EDGES // Q

TORUS_EDGE = math.comb(PHI6, 2)
FLAG_ORBITS = RANK_SEED * PHI6
FLAG_COUNT = K * PHI6
NEXT_H = RANK_SEED
NEXT_EDGE = math.comb(K, 2)
NEXT_VERTEX_COMPLETE_FACES = 44
NEXT_FACE_COMPLETE_VERTICES = 44


@dataclass(frozen=True)
class CarrierCount:
    name: str
    value: int
    formula: str
    interpretation: str


def carrier_counts() -> List[CarrierCount]:
    return [
        CarrierCount("completed_q4_carrier", Q4, "q^4", "completed color/H1 carrier"),
        CarrierCount("nonzero_q4_carrier", NONZERO_Q4, "q^4-1", "one W33 edge color"),
        CarrierCount("w33_triangles", W33_TRIANGLES, "2(q^4-1)", "2D simplex faces of W33 clique complex"),
        CarrierCount("w33_edges", W33_EDGES, "q(q^4-1)", "three edge colors"),
        CarrierCount("w33_directed_edges", W33_DIRECTED_EDGES, "2q(q^4-1)", "Hashimoto carrier states"),
        CarrierCount("generation_slice", GEN_DIM, "q^3", "one generation slice"),
    ]


@dataclass(frozen=True)
class ToroidalCount:
    name: str
    value: int
    formula: str
    interpretation: str


def toroidal_counts() -> List[ToroidalCount]:
    return [
        ToroidalCount("torus_shared_edges", TORUS_EDGE, "C(Phi6,2)=C(7,2)", "shared Csaszar/Szilassi edge count"),
        ToroidalCount("flag_orbits", FLAG_ORBITS, "2q*Phi6=6*7", "shared flag orbit count"),
        ToroidalCount("flag_count", FLAG_COUNT, "k*Phi6=12*7", "shared flag count"),
        ToroidalCount("next_h6_edges", NEXT_EDGE, "C(k,2)=C(12,2)", "shared next h=2q edge invariant"),
        ToroidalCount("next_vertex_complete", NEXT_VERTEX_COMPLETE_FACES, "E - V + 2 - 2h", "faces for V=12,E=66,h=6"),
        ToroidalCount("next_face_complete", NEXT_FACE_COMPLETE_VERTICES, "E - F + 2 - 2h", "vertices for F=12,E=66,h=6"),
    ]


def simplex_count_carrier_audit() -> Dict[str, object]:
    checks = {
        "q4_completion": H1_DIM == Q4 == 81,
        "nonzero_q4_is_edge_color": NONZERO_Q4 == EDGES_PER_COLOR == 80,
        "w33_triangles_from_q4": W33_TRIANGLES == 2 * NONZERO_Q4 == 160,
        "w33_edges_from_q4": W33_EDGES == Q * NONZERO_Q4 == 240,
        "w33_directed_from_q4": W33_DIRECTED_EDGES == RANK_SEED * NONZERO_Q4 == 480,
        "generation_slicing": Q * GEN_DIM == H1_DIM == 81,
        "torus_edges": TORUS_EDGE == math.comb(PHI6, 2) == 21,
        "flag_orbits": FLAG_ORBITS == RANK_SEED * PHI6 == 42,
        "flag_count": FLAG_COUNT == K * PHI6 == 84,
        "flag_orbits_are_twice_torus_edges": FLAG_ORBITS == 2 * TORUS_EDGE,
        "flag_count_is_four_times_torus_edges": FLAG_COUNT == 4 * TORUS_EDGE,
        "flag_count_is_twice_flag_orbits": FLAG_COUNT == 2 * FLAG_ORBITS,
        "next_h_is_rank_seed": NEXT_H == RANK_SEED == 6,
        "next_edges_are_C_k_2": NEXT_EDGE == math.comb(K, 2) == 66,
        "next_edges_phi3J_plus_one": NEXT_EDGE == PHI3 * J + 1 == 66,
        "next_vertex_complete_faces": NEXT_VERTEX_COMPLETE_FACES == NEXT_EDGE - K + (2 - 2 * NEXT_H) == 44,
        "next_face_complete_vertices": NEXT_FACE_COMPLETE_VERTICES == NEXT_EDGE - K + (2 - 2 * NEXT_H) == 44,
        "toroidal_flag_count_is_12_times_7": FLAG_COUNT == K * PHI6,
        "fano_incidence_count_is_torus_edges": TORUS_EDGE == 21,
    }
    assert all(checks.values())

    return {
        "module": "PART_CLXX_SIMPLEX_COUNT_CARRIER_COMPILER",
        "source_hint": "full toroidal-triad page: flags 84, flag orbits 42, h=6 edge invariant 66, 5+2=7 realization closure",
        "source_links": {
            "CLXIX": "completed q^4 carrier and three-generation lift",
            "uploaded_toroidal_triad": "full Szilassi-Csaszar-Tetrahedron reference page",
        },
        "w33_atoms": {
            "q": Q,
            "v": V,
            "k": K,
            "lambda": LAM,
            "mu": MU,
            "Phi3": PHI3,
            "Phi4": PHI4,
            "Phi6": PHI6,
            "rank_seed_2q": RANK_SEED,
            "J": J,
            "J_inverse": J_INV,
            "q4": Q4,
            "q4_minus_1": NONZERO_Q4,
        },
        "carrier_counts": [asdict(r) for r in carrier_counts()],
        "toroidal_counts": [asdict(r) for r in toroidal_counts()],
        "bridge_identities": {
            "w33_counts": "triangles=2(q^4-1), edges=q(q^4-1), directed=2q(q^4-1)",
            "toroidal_flags": "edges=C(Phi6,2), flag_orbits=2q*Phi6, flags=k*Phi6",
            "next_closure": "h=2q, E=C(k,2)=Phi3*J+1=66",
        },
        "checks": checks,
        "theorem_statement": (
            "The W33 simplex counts and toroidal flag counts are two projections of the same q=3 carrier. "
            "The completed q^4 carrier gives q^4-1=80, so W33 has triangles=2(q^4-1), edges=q(q^4-1), "
            "and directed edges=2q(q^4-1).  The toroidal projection uses Phi6 and k: E_torus=C(Phi6,2)=21, "
            "flag orbits=2q*Phi6=42, flags=k*Phi6=84, and the next h=2q closure has E=C(k,2)=66=Phi3*J+1."
        ),
        "interpretive_note": (
            "This integrates the fuller toroidal page with the Fano/generation lift.  The 42/84 flag counts "
            "are not floating facts: they are Phi6 multiplied by the rank seed and by k.  The h=6 count 66 is "
            "both C(12,2) and Phi3 times the stabilizer residue plus one."
        ),
    }


def main() -> int:
    audit = simplex_count_carrier_audit()
    out = ROOT / "PART_CLXX_simplex_count_carrier_compiler_results.json"
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
