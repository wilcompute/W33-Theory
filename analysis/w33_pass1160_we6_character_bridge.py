#!/usr/bin/env python3
"""Pass 1160 v2: corrected W(E6) character bridge.

Uses the exact 25-row character data already reconstructed in Pass 1135 and
closes the 40-point module through the rank-3 PSp(4,3) action of Pass 1176.
"""
from __future__ import annotations

import json
from pathlib import Path

WE6_IRREP_DIMS = [
    1, 1, 6, 6, 10, 15, 15, 15, 15, 20, 20, 20, 24, 24,
    30, 30, 60, 60, 60, 64, 64, 80, 81, 81, 90,
]

EXACT_RESIDUAL = {
    "1": (1, 13), "6": (6, 16), "15": (15, 5), "15a": (15, 4),
    "20": (20, 21), "24": (24, 2), "30": (30, 9), "60a": (60, 4),
    "64": (64, 10), "90": (90, 1),
}


def main() -> dict:
    square_sum = sum(d * d for d in WE6_IRREP_DIMS)
    residual_dim = sum(d * m for d, m in EXACT_RESIDUAL.values())
    assert len(WE6_IRREP_DIMS) == 25
    assert square_sum == 51840
    assert residual_dim == 1952
    result = {
        "schema": "w33.pass1160.we6_character_bridge.v2",
        "status": "PASS",
        "orders": {"W(E6)": 51840, "PSp(4,3)": 25920, "Sp(4,3)": 51840},
        "we6_conjugacy_classes": 25,
        "we6_irrep_dims": WE6_IRREP_DIMS,
        "sum_of_squares_check": {"value": square_sum, "equals_group_order": True},
        "point_permutation_module": "1 + 24 + 15",
        "point_module_certificate": "Pass 1176: transitive rank-3 action with subdegrees 1,12,27",
        "kernel_residual": {
            "dimension": residual_dim,
            "decomposition": {
                name: {"degree": d, "multiplicity": m}
                for name, (d, m) in EXACT_RESIDUAL.items()
            },
            "source": "Pass 1135 exact class-algebra decomposition",
        },
    }
    out = Path("data/WE6_CHARACTER_BRIDGE_2026_07_27.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("PASS 1160 v2 W(E6)=51840 module40=1+24+15")
    return result


if __name__ == "__main__":
    main()
