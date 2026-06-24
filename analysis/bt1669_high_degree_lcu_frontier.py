#!/usr/bin/env python3
"""BT1669 — high-degree LCU coefficient-mass versus walk-depth frontier.

This uses linear programming to minimize coefficient l1 mass of polynomial
projectors subject to exact interpolation on the graph spectra.  It extends BT1666
beyond minimal-degree projectors.

Boundary: smaller coefficient mass at high degree is not automatically better in
hardware.  High graph powers demand deeper walk/block-encoding circuits and more
phase precision.  This script reports the algebraic frontier only.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

SQRT2 = math.sqrt(2)
CLOCK_EIGS = [0.0, 3 - SQRT2, 3 + SQRT2, 6.0]
MATTER_EIGS = [0.0, 24.0, 30.0]
PER_WALK_SURVIVAL_BT1664 = 0.99201699


def min_l1_poly(eigs: list[float], target_index: int, degree: int) -> tuple[float, list[float]]:
    n = degree + 1
    objective = np.r_[np.zeros(n), np.ones(n)]
    aeq = []
    beq = []
    for k, lam in enumerate(eigs):
        aeq.append([lam**i for i in range(n)] + [0.0] * n)
        beq.append(1.0 if k == target_index else 0.0)
    aub = []
    bub = []
    for i in range(n):
        row = [0.0] * (2 * n)
        row[i] = 1.0
        row[n + i] = -1.0
        aub.append(row)
        bub.append(0.0)
        row = [0.0] * (2 * n)
        row[i] = -1.0
        row[n + i] = -1.0
        aub.append(row)
        bub.append(0.0)
    bounds = [(None, None)] * n + [(0, None)] * n
    res = linprog(
        objective,
        A_ub=np.array(aub),
        b_ub=np.array(bub),
        A_eq=np.array(aeq),
        b_eq=np.array(beq),
        bounds=bounds,
        method="highs",
    )
    if not res.success:
        raise RuntimeError(res.message)
    return float(res.fun), [float(x) for x in res.x[:n]]


def main() -> None:
    l1 = {"P_clock_6": {}, "P_clock_0": {}, "P_matter_24": {}, "P_matter_30": {}}
    coeffs = {}
    for degree in range(3, 10):
        l1["P_clock_6"][degree], coeffs[("P_clock_6", degree)] = min_l1_poly(CLOCK_EIGS, 3, degree)
        l1["P_clock_0"][degree], coeffs[("P_clock_0", degree)] = min_l1_poly(CLOCK_EIGS, 0, degree)
    for degree in range(2, 9):
        l1["P_matter_24"][degree], coeffs[("P_matter_24", degree)] = min_l1_poly(MATTER_EIGS, 1, degree)
        l1["P_matter_30"][degree], coeffs[("P_matter_30", degree)] = min_l1_poly(MATTER_EIGS, 2, degree)

    candidates = []
    for dc in range(3, 10):
        for dm in range(2, 9):
            res_l1 = l1["P_clock_6"][dc] * l1["P_matter_24"][dm]
            comp_l1 = l1["P_clock_0"][dc] * l1["P_matter_30"][dm]
            total = res_l1 + comp_l1
            depth = dc + dm
            candidates.append(
                {
                    "clock_degree": dc,
                    "matter_degree": dm,
                    "max_walk_depth": depth,
                    "resonance_l1": res_l1,
                    "companion_l1": comp_l1,
                    "combined_l1": total,
                    "survival_discounted_l1": total / (PER_WALK_SURVIVAL_BT1664**depth),
                }
            )

    best_by_depth = []
    for depth in sorted(set(c["max_walk_depth"] for c in candidates)):
        best = min((c for c in candidates if c["max_walk_depth"] == depth), key=lambda c: c["combined_l1"])
        best_by_depth.append(best)

    result = {
        "theorem": "BT1669 High-Degree LCU Tradeoff Frontier",
        "method": "linear-program l1 minimization over polynomial coefficients, constrained to exact spectral interpolation",
        "degree_ranges": {"clock": "3..9", "matter": "2..8"},
        "individual_l1_by_degree": {k: {str(d): v for d, v in val.items()} for k, val in l1.items()},
        "frontier_best_by_total_depth": [
            {
                "clock_degree": b["clock_degree"],
                "matter_degree": b["matter_degree"],
                "max_walk_depth": b["max_walk_depth"],
                "combined_l1": round(b["combined_l1"], 18),
                "survival_discounted_l1": round(b["survival_discounted_l1"], 18),
                "resonance_l1": round(b["resonance_l1"], 18),
                "companion_l1": round(b["companion_l1"], 18),
            }
            for b in best_by_depth
        ],
        "minimal_depth_baseline": best_by_depth[0],
        "best_reported_point": min(candidates, key=lambda c: c["survival_discounted_l1"]),
        "interpretation": "Coefficient l1 mass falls rapidly with higher polynomial degree, especially on the matter side, because the matter eigenvalues 24 and 30 are large. Under the placeholder BT1664 per-walk survival, the algebraic frontier favors deeper projectors within the tested range.",
        "boundary": "This is an algebraic LCU frontier. A physical optimizer must include block-encoding normalization, phase precision, calibration drift, and component-specific depth loss.",
    }
    assert result["frontier_best_by_total_depth"][0]["combined_l1"] == round(19 / 48, 18)
    out = Path("data/PART_BT1669_HIGH_DEGREE_LCU_FRONTIER_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
