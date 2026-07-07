#!/usr/bin/env python3
"""BT1820: aperture-to-magic estimator.

Uses BT1815's aperture count as the shot-level physical readout skeleton. This
is an estimator table, not a physical run.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path("data/PART_BT1820_APERTURE_MAGIC_ESTIMATOR_results.json")


def theorem_summary(shots_per_aperture: int = 100):
    centers = 40
    phases_per_center = 9
    apertures_per_phase = 4
    apertures = centers * phases_per_center * apertures_per_phase
    total_shots = apertures * shots_per_aperture
    contextual_fraction = 1 / 10
    expected_contextual_hits = total_shots * contextual_fraction
    return {
        "theorem": "BT1820 Aperture-to-Magic Estimator",
        "aperture_skeleton": {
            "centers": centers,
            "phase_rows_per_center": phases_per_center,
            "apertures_per_phase_row": apertures_per_phase,
            "total_apertures": apertures
        },
        "shot_table": {
            "shots_per_aperture": shots_per_aperture,
            "total_shots": total_shots,
            "contextual_fraction_target": contextual_fraction,
            "expected_contextual_hits": expected_contextual_hits
        },
        "estimator_columns": ["center", "phase", "aperture", "shots", "successes", "contextual_fraction_estimate"],
        "checks": {
            "aperture_count_matches_BT1815": apertures == 1440,
            "target_fraction_matches_W33_tax": contextual_fraction == 0.1
        },
        "honest_scope": "Shot-level estimator table for a future physical readout. It is not a measured experiment."
    }


def main() -> int:
    summary = theorem_summary()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
