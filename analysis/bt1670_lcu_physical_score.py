#!/usr/bin/env python3
"""BT1670 compact LCU score table."""
from __future__ import annotations

import json
from pathlib import Path

PER_WALK = 0.99201699
EPS_CAL = 1.0e-6
RANGE_WEIGHT = 1.0e-3

FRONTIER = [
    (3, 2, 5, 0.3958333333333333, 3.2777777777777546, 43.00000000000039),
    (3, 3, 6, 0.01379243827160492, 5.797371031746029, 43.00000000000039),
    (3, 4, 7, 0.00048466435185185125, 10.145399305555548, 43.00000000000039),
    (3, 5, 8, 0.000017193662122770897, 16.305106026785705, 43.00000000000039),
    (3, 6, 9, 0.0000006163797260802462, 24.910578652033713, 43.00000000000039),
    (3, 7, 10, 0.000000022348393174392214, 36.79971846323162, 43.00000000000039),
    (3, 8, 11, 0.0000000008200465351901854, 53.076517014276384, 43.00000000000039),
    (4, 8, 12, 0.0000000003967234470325142, 55.21515543146652, 150.5000000000002),
    (5, 8, 13, 0.0000000003053477789468841, 204.5038232347199, 160.02531645569653),
    (6, 8, 14, 0.0000000002611876780840694, 1081.2733835062256, 222.25366262034345),
    (7, 8, 15, 0.00000000023497184846984034, 5099.766636425181, 335.6535769653362),
    (8, 8, 16, 0.00000000021857339296641894, 22793.067727163656, 522.6160674977968),
    (9, 8, 17, 0.00000000020822330410596202, 98887.50411072331, 823.1002532591317),
]


def score(l1: float, depth: int, sens: float, span: float) -> float:
    import math
    return (l1 / (PER_WALK ** depth)) * (1 + EPS_CAL * sens) * (1 + RANGE_WEIGHT * math.log10(max(1.0, span)))


def main() -> None:
    rows = []
    for dc, dm, depth, l1, sens, span in FRONTIER:
        rows.append({
            "clock_degree": dc,
            "matter_degree": dm,
            "max_walk_depth": depth,
            "combined_l1": l1,
            "calibration_sensitivity": sens,
            "dynamic_range": span,
            "physical_score": score(l1, depth, sens, span),
        })
    best = min(rows, key=lambda r: r["physical_score"])
    raw = min(rows, key=lambda r: r["combined_l1"])
    result = {
        "theorem": "BT1670 Full Physical LCU Optimizer",
        "model": "score = l1/per_walk^depth times calibration and finite-range penalties",
        "parameters": {"per_walk": PER_WALK, "eps_cal": EPS_CAL, "range_weight": RANGE_WEIGHT},
        "best_physical_point": best,
        "raw_l1_best_point": raw,
        "frontier": rows,
        "boundary": "This is a transparent proxy score. Replace the penalty constants with measured hardware limits."
    }
    assert best["clock_degree"] == 8 and best["matter_degree"] == 8
    assert raw["clock_degree"] == 9 and raw["matter_degree"] == 8
    out = Path("data/PART_BT1670_FULL_PHYSICAL_LCU_OPTIMIZER_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
