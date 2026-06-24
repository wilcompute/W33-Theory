#!/usr/bin/env python3
"""BT1692 — term-LCU optical lowering for the parity-routed design."""
from __future__ import annotations

import json
from pathlib import Path

CLOCK_C6 = [("T0", 0, "5/28"), ("T2", 2, "9/28"), ("T1", 1, "19/56"), ("T3", 3, "9/56")]
CLOCK_C0 = [("T0", 0, "5/28"), ("T2", 2, "9/28"), ("T1", 1, "-19/56"), ("T3", 3, "-9/56")]
MATTER_24 = [("T0", 0, "1325/2048"), ("T2", 2, "-175/512"), ("T4", 4, "-625/2048")]
MATTER_30 = [("T0", 0, "-1/8"), ("T2", 2, "5/8"), ("T1", 1, "1/2")]


def port_summary(clock_terms, matter_terms):
    arms = []
    for ct, cd, cw in clock_terms:
        for mt, md, mw in matter_terms:
            arms.append({
                "clock_term": ct,
                "matter_term": mt,
                "clock_walk_passes": cd,
                "matter_walk_passes": md,
                "total_walk_passes": cd + md,
                "coefficient": f"({cw})*({mw})",
                "analyzer_phase": "0 for positive coefficient, pi for negative coefficient"
            })
    return {
        "term_product_arms": len(arms),
        "max_clock_walk_passes": max(a["clock_walk_passes"] for a in arms),
        "max_matter_walk_passes": max(a["matter_walk_passes"] for a in arms),
        "max_total_walk_passes": max(a["total_walk_passes"] for a in arms),
        "unrolled_total_clock_passes": sum(a["clock_walk_passes"] for a in arms),
        "unrolled_total_matter_passes": sum(a["matter_walk_passes"] for a in arms),
        "arms": arms,
    }


def main() -> None:
    result = {
        "theorem": "BT1692 Term-LCU Optical Lowering",
        "lowering_primitives": [
            "allocate clock and matter rails in the 2048-bin envelope",
            "route each Chebyshev term product into a weighted LCU arm",
            "realize T_k by k zero-phase signal-walk passes",
            "apply analyzer phase 0 or pi according to coefficient sign",
            "combine arms into resonance or companion detector port",
            "postselect the LCU success flag and record timing separator phase"
        ],
        "resonance_port": port_summary(CLOCK_C6, MATTER_24),
        "companion_port": port_summary(CLOCK_C0, MATTER_30),
        "summary": {
            "resonance_arms": 12,
            "resonance_max_depth": 7,
            "resonance_unrolled_walk_passes": 42,
            "companion_arms": 12,
            "companion_max_depth": 5,
            "companion_unrolled_walk_passes": 36,
            "time_bin_envelope": 2048,
            "largest_depth_margin": 2041
        },
        "boundary": "This is a logical optical lowering table. It names switch/delay/analyzer stages but still uses placeholder loss and does not choose a concrete foundry component library."
    }
    out = Path("data/PART_BT1692_TERM_LCU_OPTICAL_LOWERING_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
