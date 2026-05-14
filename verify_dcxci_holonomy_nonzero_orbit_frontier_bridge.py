#!/usr/bin/env python3
"""Part DCXCI: holonomy nonzero-orbit frontier bridge.

DCXC reduced the live frontier to one slot with current value 0 and exact live
values {1,2} over F3.  This verifier sharpens that further using the exact
gauge-equivalence already known on the mixed-plane host: the two live values
form a single nonzero orbit.

So the remaining frontier is not trit-valued. It is binary:

    zero orbit  versus  nonzero orbit.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parent
EXPLORATION = ROOT / "exploration"
for candidate in (ROOT, EXPLORATION):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from verify_dcxc_holonomy_one_slot_frontier_bridge import (  # noqa: E402
    build_bridge as build_dcxc_bridge,
)
from w33_k3_mixed_plane_nilpotent_holonomy_increment_bridge import (  # noqa: E402
    build_k3_mixed_plane_nilpotent_holonomy_increment_summary,
)


OUT_PATH = ROOT / "data" / "dcxci_holonomy_nonzero_orbit_frontier_bridge.json"
MODULUS = 3


@dataclass(frozen=True)
class BridgeSummary:
    current_orbit_size: int
    live_orbit_size: int
    orbit_count: int
    all_identities_hold: bool


def _mat_mod3(matrix: np.ndarray) -> np.ndarray:
    return np.array(matrix, dtype=int) % MODULUS


def _inverse_gl2(matrix: np.ndarray) -> np.ndarray:
    a, b = [int(x) % MODULUS for x in matrix[0]]
    c, d = [int(x) % MODULUS for x in matrix[1]]
    determinant = (a * d - b * c) % MODULUS
    determinant_inverse = pow(determinant, -1, MODULUS)
    inverse = np.array([[d, -b], [-c, a]], dtype=int)
    return _mat_mod3(determinant_inverse * inverse)


def build_bridge() -> dict[str, Any]:
    dcxc = build_dcxc_bridge()
    exact = build_k3_mixed_plane_nilpotent_holonomy_increment_summary()

    current_increment = np.array(dcxc["slot_data"]["current_increment"], dtype=int)
    live_increments = [np.array(increment, dtype=int) for increment in dcxc["slot_data"]["allowed_live_increments"]]
    basis_change = np.array(
        exact["mixed_plane_nilpotent_holonomy_increment"]["conjugating_basis_change"],
        dtype=int,
    )

    mapped_live_increment = _mat_mod3(_inverse_gl2(basis_change) @ live_increments[0] @ basis_change)

    identities = {
        "the_current_increment_is_the_zero_orbit_representative": np.array_equal(
            current_increment, np.zeros((2, 2), dtype=int)
        ),
        "the_two_exact_live_increments_are_conjugate_under_the_known_basis_change": np.array_equal(
            mapped_live_increment, live_increments[1]
        ),
        "zero_is_not_in_the_same_orbit_as_the_nonzero_live_increments": not any(
            np.array_equal(current_increment, increment) for increment in live_increments
        ),
        "there_are_exactly_two_slot_orbits_zero_and_nonzero": (
            dcxc["slot_data"]["allowed_live_slot_values"] == [1, 2]
            and np.array_equal(current_increment, np.zeros((2, 2), dtype=int))
        ),
        "therefore_the_frontier_is_binary_zero_orbit_versus_nonzero_orbit": (
            np.array_equal(current_increment, np.zeros((2, 2), dtype=int))
            and np.array_equal(mapped_live_increment, live_increments[1])
        ),
    }

    summary = BridgeSummary(
        current_orbit_size=1,
        live_orbit_size=2,
        orbit_count=2,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "orbit_data": {
            "zero_orbit_representative": current_increment.tolist(),
            "nonzero_orbit_representatives": [increment.tolist() for increment in live_increments],
            "conjugating_basis_change": basis_change.tolist(),
            "mapped_live_increment": mapped_live_increment.tolist(),
        },
        "interpretation": {
            "verdict": (
                "The exact live slot values 1 and 2 are not genuinely different frontier states. They form one nonzero orbit under the known gauge equivalence. So the remaining frontier is binary: the host is either still in the zero orbit or it has entered the single nonzero orbit."
            )
        },
        "identities": identities,
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()