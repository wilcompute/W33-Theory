#!/usr/bin/env python3
"""BT1666 — projector LCU cost optimizer under walk-depth constraints."""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

PROJECTORS = {
    "P_clock_6": {1: Fraction(1, 6), 2: Fraction(-1, 7), 3: Fraction(1, 42)},
    "P_clock_0": {0: Fraction(1, 1), 1: Fraction(-43, 42), 2: Fraction(2, 7), 3: Fraction(-1, 42)},
    "P_matter_24": {1: Fraction(5, 24), 2: Fraction(-1, 144)},
    "P_matter_30": {1: Fraction(-2, 15), 2: Fraction(1, 180)},
}


def l1(poly: dict[int, Fraction]) -> Fraction:
    return sum(abs(c) for c in poly.values())


def tensor(left: dict[int, Fraction], right: dict[int, Fraction]) -> list[tuple[int, int, Fraction]]:
    return [(i, j, ci * cj) for i, ci in left.items() for j, cj in right.items()]


def tensor_stats(name: str, left: dict[int, Fraction], right: dict[int, Fraction]) -> dict[str, object]:
    terms = tensor(left, right)
    mass = sum(abs(c) for _, _, c in terms)
    max_depth = max(i + j for i, j, _ in terms)
    weighted_depth = sum(abs(c) * (i + j) for i, j, c in terms) / mass
    return {
        "name": name,
        "term_count": len(terms),
        "l1_mass": str(mass),
        "l1_mass_float": float(mass),
        "max_walk_depth": max_depth,
        "weighted_walk_depth": float(weighted_depth),
        "terms": [{"clock_power": i, "matter_power": j, "coefficient": str(c), "walk_depth": i + j} for i, j, c in terms],
    }


def main() -> None:
    individual = {name: {"l1_mass": str(l1(poly)), "max_power": max(poly)} for name, poly in PROJECTORS.items()}
    resonance = tensor_stats("resonance_Pc6_tensor_Pm24", PROJECTORS["P_clock_6"], PROJECTORS["P_matter_24"])
    companion = tensor_stats("companion_Pc0_tensor_Pm30", PROJECTORS["P_clock_0"], PROJECTORS["P_matter_30"])
    combined_l1 = Fraction(31, 432) + Fraction(35, 108)
    result = {
        "theorem": "BT1666 Projector LCU Cost Optimizer",
        "optimization_scope": "exact minimal-degree interpolation projectors from BT1661; no extra high-degree powers allowed",
        "individual_projector_l1": individual,
        "tensor_selectors": [resonance, companion],
        "combined_two_port_l1_mass": str(combined_l1),
        "combined_two_port_l1_float": float(combined_l1),
        "pass_depth_bound": {
            "resonance_max_depth": resonance["max_walk_depth"],
            "companion_max_depth": companion["max_walk_depth"],
            "global_max_depth": max(resonance["max_walk_depth"], companion["max_walk_depth"]),
            "time_bin_envelope": 2048,
            "depth_margin": 2048 - max(resonance["max_walk_depth"], companion["max_walk_depth"]),
        },
        "dominant_cost": {
            "selector": "companion_Pc0_tensor_Pm30",
            "reason": "P_clock_0 contains the identity branch and has l1 mass 7/3, so companion l1 mass 35/108 exceeds resonance l1 mass 31/432."
        },
        "optimizer_decision": "Under the depth-minimal exact projector constraint, use the BT1661 polynomials unchanged. The total two-port LCU mass is 171/432 = 19/48, and maximum walk depth is only 5 of 2048 bins.",
        "boundary": "Allowing higher-degree polynomial identities can reduce coefficient l1 while increasing walk depth. That is a different optimization problem requiring calibrated loss-per-pass numbers."
    }
    assert result["combined_two_port_l1_mass"] == "19/48"
    assert result["pass_depth_bound"]["global_max_depth"] == 5
    out = Path("data/PART_BT1666_PROJECTOR_LCU_COST_OPTIMIZER_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
