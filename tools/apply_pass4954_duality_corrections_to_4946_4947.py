#!/usr/bin/env python3
"""Re-apply the Pass4954/4955 substrate correction after the legacy 4945-4947 producer.

The legacy producer still computes the correct 120x120 and 40x40 arithmetic,
but it serializes historical labels that identify the Steiner 40-fiber quotient
with the standard W33 point graph.  Pass4954/4955 prove the corrected geometry:
maximum-cut triples are W33 points, Steiner triples are W33 lines/Q(4,3) points,
and the 0/2 triad curvature belongs to Q(4,3).

This small postprocessor is intentionally semantic: it preserves recomputed
counts from the legacy producer while replacing only the superseded labels and
adding the corrected point/line metadata before CI freezes generated evidence.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P4946 = ROOT / "data/PART_W33_PASS4946_MAXCUT_STEINER_DUAL_W33_INCIDENCE.json"
P4947 = ROOT / "data/PART_W33_PASS4947_W33_TRIAD_CURVATURE.json"


def write(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def main() -> int:
    old46 = json.loads(P4946.read_text())
    old47 = json.loads(P4947.read_text())

    assert old46["shells"]["maximum_cuts"] == 120
    assert old46["shells"]["Steiner_triangles"] == 120
    assert old46["cross_incidence"]["row_weight"] == 108
    assert old46["cross_incidence"]["column_weight"] == 108
    assert old46["cross_incidence"]["identical_row_classes"] == [40, 3]
    assert old46["cross_incidence"]["identical_column_classes"] == [40, 3]
    assert old46["quotient"]["zero_matrix_row_weight"] == 4
    assert old46["quotient"]["zero_matrix_column_weight"] == 4

    new46 = {
        "pass": 4946,
        "correction": "Pass4955 fixes the side labels: maximum-cut triples are W33 points; Steiner triples are W33 lines / Q(4,3) points.",
        "shells": old46["shells"],
        "cross_incidence": old46["cross_incidence"],
        "quotient": {
            "maximum_cut_triples": "40 W(3,3) points",
            "Steiner_triples": "40 W(3,3) lines, equivalently Q(4,3) points",
            "zero_matrix_row_weight": 4,
            "zero_matrix_column_weight": 4,
            "meaning": "Z=1-B on the 40x40 quotient is literal W(3,3) point-line incidence",
            "row_collinearity": "standard W(3,3) point graph",
            "column_collinearity": "Q(4,3) point graph = W(3,3) line-intersection graph",
            "rank": 25,
            "gram_spectrum": {"16": 1, "6": 24, "0": 15},
        },
        "theorem": "Although the 120 maximum cuts and 120 Steiner triangles are inequivalent PGSp G-sets, their cross-incidence has a canonical 3-to-1 collapse on both sides. The 120 maximum cuts collapse to the forty W(3,3) points; the Steiner columns collapse to the forty W(3,3) lines. On the resulting 40x40 quotient, the non-splitting relation is precisely W33 point-line incidence. Its row collinearity graph is W(3,3), while its column collinearity graph is the nonisomorphic odd-q dual Q(4,3).",
        "boundary": "Finite incidence theorem corrected by Pass4955. The quotient identifies point and line actions; it does not restore an equivariant bijection between the original 120-element shells.",
    }

    curvature = old47["curvature"]
    assert curvature == {
        "flat_identity": 1080,
        "reflection_transposition": 2160,
        "order3": 0,
    } or curvature == {
        "flat_identity": 1080,
        "order3": 0,
        "reflection_transposition": 2160,
    }

    new47 = {
        "pass": 4947,
        "correction": "Pass4954 identifies these 3240 complement triangles as independent triples of Q(4,3) points / triples of pairwise disjoint W33 lines, not independent triples of standard W33 points.",
        "Q43_independent_triads": 3240,
        "curvature": curvature,
        "geometric_classification": {
            "zero_common_neighbors": 1080,
            "two_common_neighbors": 2160,
            "equivalence": "matching holonomy is identity iff the Q(4,3) triad has zero common neighbors; it is a transposition iff the Q(4,3) triad has two common neighbors",
        },
        "standard_W33_point_graph_baseline": {
            "independent_triads": 3240,
            "one_common_neighbor": 2880,
            "four_common_neighbors": 360,
            "source": "Pass4953",
        },
        "theorem": "The S3 matching connection detects the intrinsic triad geometry of the Steiner quotient Q(4,3). Among its 3240 triples of pairwise noncollinear points, exactly 1080 have no common neighbor and carry flat identity holonomy; exactly 2160 have two common neighbors and carry reflection holonomy. No complement triangle has order-three curvature. These counts must not be quoted as the triad census of the standard W(3,3) point graph.",
        "boundary": "Finite Q(4,3) holonomy/triad theorem corrected by Pass4954. The numerical 1080 also occurs elsewhere in the repo, but no identification with those objects is claimed without an explicit equivariant map.",
    }

    write(P4946, new46)
    write(P4947, new47)
    print("PASS Pass4954 duality corrections re-applied to Pass4946/4947 generated evidence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
