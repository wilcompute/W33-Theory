#!/usr/bin/env python3
"""BT1667 — calibrated loss sweep for the BT1664 component budget.

The word calibrated here means parameterized by named component ranges, not by
measured lab data.  The sweep is meant to be replaced by a measured component CSV
when the optical build has fixed part numbers.
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

PC6 = {1: Fraction(1, 6), 2: Fraction(-1, 7), 3: Fraction(1, 42)}
PC0 = {0: Fraction(1, 1), 1: Fraction(-43, 42), 2: Fraction(2, 7), 3: Fraction(-1, 42)}
PM24 = {1: Fraction(5, 24), 2: Fraction(-1, 144)}
PM30 = {1: Fraction(-2, 15), 2: Fraction(1, 180)}


def tensor_terms(left: dict[int, Fraction], right: dict[int, Fraction]) -> list[tuple[int, int, Fraction]]:
    return [(i, j, ci * cj) for i, ci in left.items() for j, cj in right.items()]


def weighted_survival(left: dict[int, Fraction], right: dict[int, Fraction], params: dict[str, float]) -> float:
    terms = tensor_terms(left, right)
    mass = sum(abs(c) for _, _, c in terms)
    per_walk = params["switch"] * params["delay"] * params["phase_survival"]
    return sum(
        float(abs(c) / mass) * (per_walk ** (i + j)) * params["analyzer"] * params["detector"]
        for i, j, c in terms
    )


def snr(left: dict[int, Fraction], right: dict[int, Fraction], params: dict[str, float]) -> float:
    survival = weighted_survival(left, right, params)
    background = 1.0 - (1.0 - params["dark_per_bin"]) ** int(params["bins"])
    contrast = math.exp(-0.5 * params["phase_jitter"] ** 2) * (1 - 2 * params["parity_flip"]) * (1 - background)
    return contrast * math.sqrt(params["bins"] * survival)


def main() -> None:
    switch_grid = [0.90, 0.95, 0.98, 0.995]
    delay_grid = [0.90, 0.95, 0.99]
    detector_grid = [0.15, 0.30, 0.60, 0.85]
    parity_grid = [0.00, 0.10, 0.20, 0.35, 0.45]
    jitter_grid = [0.00, 0.10, 0.25, 0.50]
    base = {"phase_survival": 0.999, "analyzer": 0.98, "dark_per_bin": 1.0e-6, "bins": 2048}

    rows = []
    for switch in switch_grid:
        for delay in delay_grid:
            for detector in detector_grid:
                for parity in parity_grid:
                    for jitter in jitter_grid:
                        params = dict(base, switch=switch, delay=delay, detector=detector, parity_flip=parity, phase_jitter=jitter)
                        res_snr = snr(PC6, PM24, params)
                        comp_snr = snr(PC0, PM30, params)
                        rows.append(
                            {
                                "switch": switch,
                                "delay": delay,
                                "detector": detector,
                                "parity_flip": parity,
                                "phase_jitter": jitter,
                                "resonance_snr": round(res_snr, 6),
                                "companion_snr": round(comp_snr, 6),
                                "min_snr": round(min(res_snr, comp_snr), 6),
                                "pass": min(res_snr, comp_snr) >= 5.0,
                            }
                        )

    by_parity = []
    for parity in parity_grid:
        subset = [r for r in rows if r["parity_flip"] == parity]
        by_parity.append(
            {
                "parity_flip": parity,
                "cases": len(subset),
                "passes": sum(1 for r in subset if r["pass"]),
                "pass_rate": round(sum(1 for r in subset if r["pass"]) / len(subset), 6),
                "min_snr": min(r["min_snr"] for r in subset),
                "max_snr": max(r["min_snr"] for r in subset),
            }
        )

    by_detector = []
    for detector in detector_grid:
        subset = [r for r in rows if r["detector"] == detector]
        by_detector.append(
            {
                "detector": detector,
                "cases": len(subset),
                "passes": sum(1 for r in subset if r["pass"]),
                "pass_rate": round(sum(1 for r in subset if r["pass"]) / len(subset), 6),
                "min_snr": min(r["min_snr"] for r in subset),
                "max_snr": max(r["min_snr"] for r in subset),
            }
        )

    result = {
        "theorem": "BT1667 Calibrated Loss Sweep",
        "calibration_status": "range sweep over named component parameters; not measured hardware data",
        "grid": {
            "switch_survival": switch_grid,
            "delay_survival": delay_grid,
            "detector_efficiency": detector_grid,
            "parity_flip_probability": parity_grid,
            "phase_jitter_rms": jitter_grid,
            "fixed": base,
        },
        "summary": {
            "cases": len(rows),
            "passes": sum(1 for r in rows if r["pass"]),
            "fails": sum(1 for r in rows if not r["pass"]),
            "pass_rate": round(sum(1 for r in rows if r["pass"]) / len(rows), 6),
            "min_snr": min(r["min_snr"] for r in rows),
            "max_snr": max(r["min_snr"] for r in rows),
        },
        "by_parity_flip": by_parity,
        "by_detector_efficiency": by_detector,
        "worst_cases": sorted(rows, key=lambda r: r["min_snr"])[:10],
        "best_cases": sorted(rows, key=lambda r: r["min_snr"], reverse=True)[:10],
        "interpretation": "The separator is loss-tolerant until contrast is directly damaged by large parity/sign flips. In this grid all parity <=0.20 cases pass, while parity=0.45 cases fail.",
        "boundary": "This is a component-range sweep. A measured optical build should replace the grid with calibrated component distributions.",
    }
    assert result["summary"]["cases"] == 960
    assert result["summary"]["passes"] == 721
    assert result["summary"]["fails"] == 239
    out = Path("data/PART_BT1667_CALIBRATED_LOSS_SWEEP_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
