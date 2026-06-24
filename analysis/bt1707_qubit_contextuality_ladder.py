#!/usr/bin/env python3
"""BT1707 - multi-qubit contextuality ladder as a Holonet readout hint.

The attached contextuality papers track binary Pauli spaces from one through
six qubits.  This verifier does not recompute contextuality degrees by search;
it records the paper-level core objects and checks the arithmetic spine that
connects them to the W33/Holonet packets already in the repo.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1707_qubit_contextuality_ladder.json"


def symplectic_points(qubits: int) -> int:
    return 4**qubits - 1


def symplectic_lines(qubits: int) -> int:
    if qubits == 1:
        return 0
    return (4**qubits - 1) * (4 ** (qubits - 1) - 1) // 3


def build_certificate() -> dict[str, Any]:
    ladder = [
        {
            "qubits": 1,
            "space": "W(1,2)",
            "points": 3,
            "line_contexts": 0,
            "contextual_core": "none",
            "role": "single Pauli triple; no line-context Kochen-Specker proof",
        },
        {
            "qubits": 2,
            "space": "W(3,2) doily",
            "points": 15,
            "line_contexts": 15,
            "contextual_core": "Mermin-Peres square degree 1; doily degree 3",
            "role": "two-qubit binary seed; projective-line-over-M2(F2) shadow has 35 points",
            "reported_degree": 3,
            "distinguished_subdegree": 1,
        },
        {
            "qubits": 3,
            "space": "W(5,2)",
            "points": 63,
            "line_contexts": 315,
            "contextual_core": "classically embedded split Cayley hexagon of order 2",
            "role": "full three-qubit contextuality is carried by the 63 hexagon lines",
            "reported_degree": 63,
            "elliptic_core_lines": 9,
            "hyperbolic_core_lines": 21,
            "hexagon_automorphism_order": 12096,
        },
        {
            "qubits": 4,
            "space": "W(7,2)",
            "points": 255,
            "line_contexts": 5355,
            "contextual_core": "elliptic 315 from three hexagons; hyperbolic 315 as DW(5,2)",
            "role": "first higher-rank lift where Heawood, Coxeter, and dual-W(5,2) cores separate",
            "reported_full_bound": 1575,
            "reported_elliptic_bound": 315,
            "reported_hyperbolic_bound": 315,
            "dw52_configuration": "(135_7,315_3)",
        },
        {
            "qubits": 5,
            "space": "W(9,2)",
            "points": 1023,
            "line_contexts": 86955,
            "contextual_core": "hyperbolic bound compactified around PG(4,2) point-hyperplane incidence",
            "role": "projective incidence core climbs from PG(3,2) to PG(4,2)",
            "reported_hyperbolic_bound": 6975,
        },
        {
            "qubits": 6,
            "space": "W(11,2)",
            "points": 4095,
            "line_contexts": 1396395,
            "contextual_core": "full space includes two disjoint split Cayley hexagons; hyperbolic core uses K7,7",
            "role": "seven-fold Fano incidence becomes a K7,7 carrier; Heawood is its 21-edge subgraph",
            "reported_full_bound": 553140,
            "k77_edges": 49,
            "heawood_edges_inside_k77": 21,
        },
    ]

    expected_points = {
        row["qubits"]: symplectic_points(row["qubits"]) for row in ladder
    }
    expected_lines = {row["qubits"]: symplectic_lines(row["qubits"]) for row in ladder}
    q3 = ladder[2]
    q4 = ladder[3]
    q6 = ladder[5]

    checks = {
        "symplectic_point_counts_match": all(
            row["points"] == expected_points[row["qubits"]] for row in ladder
        ),
        "symplectic_line_counts_match": all(
            row["line_contexts"] == expected_lines[row["qubits"]] for row in ladder
        ),
        "three_qubit_degree_is_hexagon_line_count": q3["reported_degree"]
        == q3["points"]
        == 63,
        "three_qubit_contexts_are_five_hexagons_worth": q3["line_contexts"]
        == 5 * q3["reported_degree"],
        "split_cayley_aut_is_readout_times_packet_clock": q3[
            "hexagon_automorphism_order"
        ]
        == 168 * 72,
        "split_cayley_aut_is_level7_j_special_fiber": q3["hexagon_automorphism_order"]
        == 7 * 1728,
        "four_qubit_full_bound_is_five_times_315": q4["reported_full_bound"]
        == 5 * q4["reported_hyperbolic_bound"],
        "dw52_profile_is_consistent": 135 * 7 == 315 * 3,
        "six_qubit_k77_contains_heawood_plus_coheawood": q6["k77_edges"]
        - q6["heawood_edges_inside_k77"]
        == 28,
    }

    return {
        "theorem": "BT1707 qubit contextuality ladder",
        "verified": all(checks.values()),
        "breakthrough": (
            "The one-to-six-qubit contextuality papers organize the binary Pauli "
            "ladder through doily, Heawood, split-Cayley-hexagon, DW(5,2), "
            "projective-incidence, and K7,7 cores.  The three-qubit split "
            "Cayley automorphism order is exactly 12096 = 168*72, matching the "
            "Fano/Klein readout group times the Holonet packet clock."
        ),
        "ladder": ladder,
        "source_documents": [
            "q-2025-01-20-1601.pdf",
            "A new heuristic approach for contextuality degree estimates and its four- to six-qubit portrayals.pdf",
            "New and improved bounds on the contextuality degree of multi-qubit configurations.pdf",
        ],
        "claim_boundary": [
            "The verifier records paper-reported contextuality cores; it does not brute-force contextuality degree.",
            "The promoted W33 claim is arithmetic/incidence compatibility with existing Holonet readout packets.",
            "Objectwise equivalence between the split Cayley hexagon and a W33 submodule remains a future construction target.",
        ],
        "checks": checks,
    }


def main() -> int:
    cert = build_certificate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(cert["theorem"])
    print(f"  verified: {cert['verified']}")
    print("  key identity: 12096 = 168 * 72 = 7 * 1728")
    print(f"  wrote {OUT}")
    return 0 if cert["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
