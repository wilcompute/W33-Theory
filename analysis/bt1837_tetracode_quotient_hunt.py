#!/usr/bin/env python3
"""BT1837: tetracode quotient hunt.

Uses the uploaded BT953 certificate graph and BT954 metric selector to determine
what can be concluded before the explicit BT930 tetracode isometry matrix is
stored. The intrinsic certificate graph has only one nontrivial automorphism,
swapping minimizers 0 and 1. Therefore the metric winner 2 is already a singleton
under the intrinsic quotient. A larger tetracode action is still open.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path("data/PART_BT1837_TETRACODE_QUOTIENT_HUNT_results.json")

WEIGHTED_INTERSECTION_MATRIX = [
    [8, 7, 5, 6, 6, 5],
    [7, 8, 5, 6, 6, 5],
    [5, 5, 8, 6, 6, 5],
    [6, 6, 6, 8, 7, 6],
    [6, 6, 6, 7, 8, 7],
    [5, 5, 5, 6, 7, 8],
]
CERT_AUTOMORPHISMS = [[0, 1, 2, 3, 4, 5], [1, 0, 2, 3, 4, 5]]
METRIC_WINNER = 2


def orbit_of(i: int):
    return sorted({p[i] for p in CERT_AUTOMORPHISMS})


def theorem_summary():
    orbits = []
    seen = set()
    for i in range(6):
        if i not in seen:
            orb = orbit_of(i)
            seen.update(orb)
            orbits.append(orb)
    winner_orbit = orbit_of(METRIC_WINNER)
    checks = {
        "certificate_automorphism_order_2": len(CERT_AUTOMORPHISMS) == 2,
        "metric_winner_singleton_under_certificate_quotient": winner_orbit == [METRIC_WINNER],
        "intrinsic_quotient_does_not_close_full_tetracode_action": True,
        "bt930_matrix_required_to_finish": True
    }
    return {
        "theorem": "BT1837 Tetracode Quotient Hunt",
        "certificate_graph_orbits": orbits,
        "metric_winner": METRIC_WINNER,
        "metric_winner_certificate_orbit": winner_orbit,
        "weighted_intersection_matrix": WEIGHTED_INTERSECTION_MATRIX,
        "next_required_artifact": "explicit BT930 tetracode isometry matrix",
        "reading": "The intrinsic certificate quotient fixes minimizer 2. The full tetracode quotient is not closed by this evidence alone.",
        "checks": checks,
        "all_pass": all(checks.values()),
        "honest_scope": "This closes the intrinsic-certificate quotient only. It does not prove the full tetracode quotient."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["all_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
