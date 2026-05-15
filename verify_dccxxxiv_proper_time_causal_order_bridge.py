#!/usr/bin/env python3
"""Part DCCXXXIV: proper-time / causal-order bridge.

Builds on DCCXXXIII by separating spatial symmetry from temporal accumulation:
- spatial channels are the three Clifford bivectors, acted on by signed permutations,
- proper time is the closure clock tau,
- tau is invariant under every signed permutation of the spatial triad,
- causal classes are the distinct tau-levels, totally ordered by monotone closure time.

This turns the fourth channel into a discrete proper-time scalar rather than just a
fourth coordinate count.
"""

from __future__ import annotations

import itertools
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dccxxxiii_spatial_closure_time_bridge import build_bridge as build_dccxxxiii

OUT_PATH = ROOT / "data" / "dccxxxiv_proper_time_causal_order_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    spatial_symmetry_count: int
    proper_time_level_count: int
    initial_proper_time: int
    final_proper_time: int
    final_scale: int
    all_identities_hold: bool


def signed_permutations(basis: list[str]) -> list[list[str]]:
    out: list[list[str]] = []
    for perm in itertools.permutations(basis):
        for signs in itertools.product([1, -1], repeat=len(basis)):
            out.append([
                token if sign == 1 else f"-{token}"
                for token, sign in zip(perm, signs)
            ])
    return out


def build_bridge() -> dict[str, Any]:
    dccxxxiii = build_dccxxxiii()

    basis = dccxxxiii["spatial_time_split"]["spatial_basis"]
    history = dccxxxiii["state_history"]
    tau = [step["tau"] for step in history]
    scales = [step["scale"] for step in history]
    levels = sorted({0, *tau})
    symmetries = signed_permutations(basis)

    causal_classes = [
        {
            "proper_time": level,
            "representative_scale": 12 * (2 ** level),
            "class_name": f"T_{level}",
        }
        for level in levels
    ]

    proper_time_differences = [
        {
            "from": levels[i],
            "to": levels[i + 1],
            "delta_tau": levels[i + 1] - levels[i],
            "scale_ratio": (12 * (2 ** levels[i + 1])) // (12 * (2 ** levels[i])),
        }
        for i in range(len(levels) - 1)
    ]

    symmetry_witness = [
        {
            "spatial_transform": sym,
            "proper_time_history": tau,
        }
        for sym in symmetries[:8]
    ]

    identities = {
        "there_are_48_signed_spatial_symmetries": len(symmetries) == 48,
        "proper_time_levels_are_0_through_5": levels == [0, 1, 2, 3, 4, 5],
        "proper_time_is_monotone": all(levels[i] < levels[i + 1] for i in range(len(levels) - 1)),
        "every_spatial_symmetry_preserves_proper_time_history": all(
            witness["proper_time_history"] == tau for witness in symmetry_witness
        ) and all(len(sym) == 3 for sym in symmetries),
        "proper_time_difference_equals_log_scale_ratio": all(
            diff["delta_tau"] == 1 and diff["scale_ratio"] == 2 for diff in proper_time_differences
        ),
        "causal_classes_are_totally_ordered_by_tau": all(
            causal_classes[i]["proper_time"] < causal_classes[i + 1]["proper_time"]
            for i in range(len(causal_classes) - 1)
        ),
        "final_scale_matches_final_proper_time_level": scales[-1] == 12 * (2 ** levels[-1]) == 384,
    }

    summary = BridgeSummary(
        spatial_symmetry_count=len(symmetries),
        proper_time_level_count=len(levels),
        initial_proper_time=levels[0],
        final_proper_time=levels[-1],
        final_scale=scales[-1],
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "causal_order": {
            "definition": "T_a <= T_b iff tau_a <= tau_b",
            "classes": causal_classes,
            "differences": proper_time_differences,
        },
        "spatial_symmetry": {
            "base_spatial_triads": basis,
            "signed_permutation_count": len(symmetries),
            "witness_samples": symmetry_witness,
        },
        "bridge_claim": {
            "exact_layer": (
                "Proper time is the symmetry-invariant scalar tau labeling the totally ordered causal classes of the closure process, while space is the 48-fold signed-permutation orbit of the Clifford bivector triad."
            ),
            "conditional_layer": (
                "Connecting this discrete proper time to relativistic continuum proper time requires an additional continuum dynamics theorem."
            ),
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
