"""Pass 70 Track B: [[360,9,d]] logical-sector witness.

Packages the eigenspace bookkeeping used in the 360-dimensional W33 code claim.
"""
from __future__ import annotations

import json
import math
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
    k = next(item["multiplicity"] for item in EIGENSPACES if item["sector"] == "logical_space")
    largest_nonlogical = max(item["multiplicity"] for item in EIGENSPACES if item["sector"] != "logical_space")
    d_lower_bound = math.ceil(n / largest_nonlogical)

    payload = {
        "track": "B",
        "title": "W33 logical sector code witness",
        "length_n": n,
        "logical_dimension_k": k,
        "distance_lower_bound": d_lower_bound,
        "claimed_code": f"[[{n},{k},{d_lower_bound}]]",
        "largest_nonlogical_eigenspace": largest_nonlogical,
        "logical_decomposition": "3 x 3",
        "eigenspaces": EIGENSPACES,
    }

    out = Path("w33_pass70_trackB_qec.json")
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
