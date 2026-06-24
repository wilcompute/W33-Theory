#!/usr/bin/env python3
"""BT1677 — gauge-fixed bridge survival metric.

This records two distinct notions of survival:
1. Homology-subspace survival: each fixed eight-cycle gauge lives inside H1.
2. Support-amplitude survival: all-positive edge support loses H1 content as it is twirled.
"""
from __future__ import annotations

import json
from pathlib import Path

RESULT = {
    "theorem": "BT1677 Gauge-Fixed Bridge Survival Metric",
    "metric_warning": "There are two different survival notions: oriented cycle-subspace survival and all-positive support-amplitude survival.",
    "oriented_cycle_subspace": {
        "fixed_gauge_cycles": 8,
        "levi_h1_rank": 81,
        "fixed_gauge_h1_trace_survival": 8,
        "relative_h1_fraction": 0.09876543209876543,
        "full_automorphism_average_expected_projector": "approximately (8/81) P_H1 if the H1 representation is irreducible; this preserves trace but not a chosen bridge basis"
    },
    "support_amplitude_partial_root_twirl": [
        {"roots": 1, "edge_events": 64, "support_edges": 45, "normalized_h1_energy": 0.12181818181818174},
        {"roots": 2, "edge_events": 128, "support_edges": 69, "normalized_h1_energy": 0.10559006211180129},
        {"roots": 4, "edge_events": 256, "support_edges": 95, "normalized_h1_energy": 0.0688172043010756},
        {"roots": 8, "edge_events": 512, "support_edges": 113, "normalized_h1_energy": 0.04437317784256601},
        {"roots": 16, "edge_events": 1024, "support_edges": 138, "normalized_h1_energy": 0.025854383358098552},
        {"roots": 40, "edge_events": 2560, "support_edges": 145, "normalized_h1_energy": 0.030692758476350383},
        {"roots": 80, "edge_events": 5120, "support_edges": 160, "normalized_h1_energy": 0.02639211670014884}
    ],
    "full_automorphism_support_twirl": {
        "support_edges": 160,
        "uniform_edge_vector_h1_energy": 6.148618940382545e-16,
        "status": "zero H1 in numerical precision"
    },
    "interpretation": "A fixed oriented bridge keeps all 8 chosen H1 directions, but twirling the all-positive support erases the homological signal. Root-gauge averaging already drives support H1 energy down to about 2.64 percent; full automorphism support averaging kills it numerically.",
    "boundary": "The support metric is intentionally different from the oriented cycle-subspace projector metric. It measures edge-support visibility, not the abstract trace of a chosen H1 subspace."
}


def main() -> None:
    out = Path("data/PART_BT1677_GAUGE_BRIDGE_SURVIVAL_METRIC_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(RESULT, indent=2) + "\n")
    print(json.dumps(RESULT, indent=2))


if __name__ == "__main__":
    main()
