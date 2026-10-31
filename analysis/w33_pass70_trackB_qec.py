"""Pass 70 Track B: audit of the 360-dimensional spectral ledger.

The multiplicities sum to 360 and one labelled sector has multiplicity 9, but
spectral multiplicities alone do not construct a stabilizer code or determine
its distance.
"""
from __future__ import annotations

import json
from pathlib import Path


EIGENSPACES = [
    {"eigenvalue": 8, "multiplicity": 1, "sector": "vacuum"},
    {"eigenvalue": 3, "multiplicity": 40, "sector": "gauge_bosons"},
    {"eigenvalue": -4, "multiplicity": 9, "sector": "logical_space"},
    {"eigenvalue": "(1+sqrt(97))/2", "multiplicity": 15, "sector": "quark_lepton_doublets"},
    {"eigenvalue": "(1-sqrt(97))/2", "multiplicity": 15, "sector": "quark_lepton_doublets_conjugate"},
    {"eigenvalue": "(-1+sqrt(97))/2", "multiplicity": 15, "sector": "conjugate_sector"},
    {"eigenvalue": "(-1-sqrt(97))/2", "multiplicity": 15, "sector": "conjugate_sector_dual"},
    {"eigenvalue": 0, "multiplicity": 250, "sector": "bulk_modes"},
]


def main() -> None:
    n = sum(item["multiplicity"] for item in EIGENSPACES)
    distinguished_multiplicity = next(
        item["multiplicity"] for item in EIGENSPACES if item["sector"] == "logical_space"
    )
    largest_nonlogical = max(item["multiplicity"] for item in EIGENSPACES if item["sector"] != "logical_space")
    heuristic_ceil_ratio = (n + largest_nonlogical - 1) // largest_nonlogical

    payload = {
        "track": "B",
        "title": "W33 360-dimensional spectral-ledger audit",
        "length_n": n,
        "distinguished_multiplicity": distinguished_multiplicity,
        "logical_dimension_k": None,
        "distance_lower_bound": None,
        "claimed_code": None,
        "retracted_claims": ["[[360,9,9]]", "[[360,9,1]]"],
        "largest_nonlogical_eigenspace": largest_nonlogical,
        "heuristic_ceil_ratio": heuristic_ceil_ratio,
        "logical_decomposition": "3 x 3",
        "stabilizer_matrices_constructed": False,
        "distance_computed": False,
        "audit_note": (
            "The ledger certifies only the multiplicity identity 360 = "
            "1+40+9+15+15+15+15+250. A multiplicity labelled logical_space "
            "is not a code dimension, and ceil(360/250)=2 is not a distance bound."
        ),
        "audit_pass": n == 360 and distinguished_multiplicity == 9 and heuristic_ceil_ratio == 2,
        "eigenspaces": EIGENSPACES,
    }

    out = Path("w33_pass70_trackB_qec.json")
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
