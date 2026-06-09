#!/usr/bin/env python3
"""BT602: Hashimoto-to-Bose-Mesner transfer map.

This script records the explicit scalar bridge from the W33 collinearity
adjacency spectrum to the Levi flag Bose-Mesner leakage sector model.

The current state is deliberately exact but conservative:
- the W33 adjacency side supplies the odd closed-walk transport M5/M3 = 244;
- the directed Hashimoto side supplies the nonbacktracking square (k-1)^2 = 121;
- the Bose-Mesner side sees the normalized scalar 244/121 as the raw cubic
  leakage transfer into the companion stack E1+E2+E3.

This is a transfer map of invariants, not yet a full intertwiner between the
480-dimensional directed-edge module and the 160-dimensional Levi flag module.
"""
from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path

# W33 collinearity data
adjacency_spectrum = [(12, 1), (2, 24), (-4, 15)]
d = 12
p = d - 1

# Levi flag Bose-Mesner sectors: dimensions/multiplicities from BT548-BT551.
sectors = {
    "E0": 1,
    "E1": 24,
    "E2": 30,
    "E3": 24,
    "E4": 81,
}
companion = ["E1", "E2", "E3"]
protected = ["E4"]
uniform = ["E0"]

def moment(power: int) -> int:
    return sum(mult * (lam ** power) for lam, mult in adjacency_spectrum)

M3 = moment(3)
M5 = moment(5)
transport = Fraction(M5, M3)
ihara_square = p * p
normalized_transport = transport / ihara_square
weighted_transport = Fraction(4, 5) * normalized_transport

# Primitive-sector transfer summary: the scalar maps are exact; the sector support
# statements come from BT596.
transfer_map = {
    "collinearity_odd_walk_transport": "M5/M3",
    "hashimoto_normalization": "1/(k-1)^2",
    "bose_mesner_raw_leakage_scalar": "244/121",
    "bose_mesner_weighted_leakage_scalar": "976/605",
    "raw_sector_support": ["E0", "E1", "E2", "E3", "E4"],
    "shadow_sector_support": companion,
    "repair_sector_support": ["E0", "E4"],
    "centered_repair_support": protected,
}

checks = {
    "sector_dimensions_sum_to_160": sum(sectors.values()) == 160,
    "M3_is_960": M3 == 960,
    "M5_is_234240": M5 == 234240,
    "transport_is_244": transport == 244,
    "ihara_square_is_121": ihara_square == 121,
    "normalized_transport_is_244_over_121": normalized_transport == Fraction(244, 121),
    "weighted_transport_is_976_over_605": weighted_transport == Fraction(976, 605),
    "companion_dimension_is_78": sum(sectors[s] for s in companion) == 78,
    "protected_dimension_is_81": sum(sectors[s] for s in protected) == 81,
}

result = {
    "bt": 602,
    "title": "Hashimoto-to-Bose-Mesner transfer map",
    "adjacency_spectrum": {str(lam): mult for lam, mult in adjacency_spectrum},
    "hashimoto_scale": {
        "degree": d,
        "nonbacktracking_outdegree": p,
        "ihara_square": ihara_square,
    },
    "odd_walk_transport": {
        "M3": M3,
        "M5": M5,
        "M5_over_M3": str(transport),
    },
    "bose_mesner_sectors": sectors,
    "transfer_map": transfer_map,
    "normalized_values": {
        "raw_leakage": str(normalized_transport),
        "weighted_leakage": str(weighted_transport),
    },
    "boundary": "This artifact maps exact scalar invariants and sector supports. A future BT should build an explicit linear intertwiner between directed-edge and Levi-flag modules.",
    "checks": checks,
    "all_identities_hold": all(checks.values()),
}

Path("data/PART_BT602_HASHIMOTO_BOSE_MESNER_TRANSFER_MAP_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps(result, indent=2))
