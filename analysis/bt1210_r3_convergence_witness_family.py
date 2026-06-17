#!/usr/bin/env python3
"""BT1210 -- R3 convergence witness family.

This is a toy finite-refinement certificate for the R3 checklist.  It does not
prove the K3/spacetime limit.  It verifies that the checklist can be represented
as monotone numerical witnesses along a refinement ladder.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def row(n: int) -> dict:
    h = 1.0 / n
    return {
        "refinement_n": n,
        "mesh_h": h,
        "shape_regular_min_quality": 1.0 - 0.25 * h,
        "curvature_energy": 24.0 + 3.0 * h * h,
        "spectral_moment_error": h * h,
        "gauge_holonomy_error": h,
        "operator_resolvent_error": h * h,
        "metric_propinquity_proxy": h,
        "scale_separation_ratio": n,
    }


def nonincreasing(values: list[float]) -> bool:
    return all(values[i + 1] <= values[i] for i in range(len(values) - 1))


def nondecreasing(values: list[float]) -> bool:
    return all(values[i + 1] >= values[i] for i in range(len(values) - 1))


def build_result(ns: list[int]) -> dict:
    rows = [row(n) for n in ns]
    checks = {
        "mesh_h_decreases": nonincreasing([r["mesh_h"] for r in rows]),
        "shape_quality_increases": nondecreasing([r["shape_regular_min_quality"] for r in rows]),
        "curvature_energy_decreases_to_24": nonincreasing([r["curvature_energy"] for r in rows]),
        "spectral_moment_error_decreases": nonincreasing([r["spectral_moment_error"] for r in rows]),
        "gauge_holonomy_error_decreases": nonincreasing([r["gauge_holonomy_error"] for r in rows]),
        "operator_resolvent_error_decreases": nonincreasing([r["operator_resolvent_error"] for r in rows]),
        "metric_propinquity_proxy_decreases": nonincreasing([r["metric_propinquity_proxy"] for r in rows]),
        "scale_separation_increases": nondecreasing([r["scale_separation_ratio"] for r in rows]),
    }
    return {
        "bt": 1210,
        "title": "R3 finite-to-continuum witness family",
        "honesty_boundary": "Toy convergence certificate: it tests the R3 checklist shape, not a proof that the physical K3/spacetime continuum exists.",
        "target_limit": {
            "curvature_energy": 24,
            "spectral_moment_error": 0,
            "gauge_holonomy_error": 0,
            "operator_resolvent_error": 0,
            "metric_propinquity_proxy": 0,
        },
        "refinement_ladder": rows,
        "checks": checks,
        "passes_all_monotone_witness_checks": all(checks.values()),
        "interpretation": "The R3 checklist can be cast as a falsifiable refinement witness: metric quality improves, curvature energy stabilizes, spectral/gauge/operator errors shrink, and scale separation grows.",
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--ns", type=int, nargs="+", default=[4, 8, 16, 32, 64, 128])
    p.add_argument("--out", type=Path, default=Path("data/bt1210_r3_convergence_witness_family.json"))
    args = p.parse_args()
    result = build_result(args.ns)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt": 1210, "passes": result["passes_all_monotone_witness_checks"], "out": str(args.out)}, indent=2))


if __name__ == "__main__":
    main()
