#!/usr/bin/env python3
"""BT1209 -- lambda-lock demonstrator inference protocol.

This is the lab-facing version of BT1207.  It maps measurements to three
independent q-estimates and checks whether their uncertainty intervals overlap
at q=3.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class Estimate:
    channel: str
    value: float
    sigma: float
    lower_3sigma: float
    upper_3sigma: float
    q3_inside_3sigma: bool


def interval(value: float, sigma: float, nsigma: float = 3.0) -> tuple[float, float, bool]:
    lo = value - nsigma * sigma
    hi = value + nsigma * sigma
    return lo, hi, lo <= 3.0 <= hi


def drive_estimate(cos_theta: float, sigma_cos: float) -> Estimate:
    q = 1.0 / (1.0 + cos_theta)
    # dq/dc = -1/(1+c)^2 = -q^2
    sigma_q = abs(q * q) * sigma_cos
    lo, hi, ok = interval(q, sigma_q)
    return Estimate("drive", q, sigma_q, lo, hi, ok)


def chern_estimate(abs_chern: float, sigma_chern: float) -> Estimate:
    q = abs_chern + 1.0
    lo, hi, ok = interval(q, sigma_chern)
    return Estimate("chern", q, sigma_chern, lo, hi, ok)


def carrier_estimate(n_transverse: float, sigma_transverse: float) -> Estimate:
    q = n_transverse + 1.0
    lo, hi, ok = interval(q, sigma_transverse)
    return Estimate("carrier", q, sigma_transverse, lo, hi, ok)


def weighted_consensus(estimates: list[Estimate]) -> dict:
    weights = [1.0 / (e.sigma * e.sigma) if e.sigma > 0 else 1.0e18 for e in estimates]
    qbar = sum(w * e.value for w, e in zip(weights, estimates)) / sum(weights)
    sigma = math.sqrt(1.0 / sum(weights))
    lo, hi, ok = interval(qbar, sigma)
    max_pairwise_disagreement = max(abs(a.value - b.value) for a in estimates for b in estimates)
    return {
        "q_weighted": qbar,
        "sigma_weighted": sigma,
        "lower_3sigma": lo,
        "upper_3sigma": hi,
        "q3_inside_3sigma": ok,
        "max_pairwise_disagreement": max_pairwise_disagreement,
    }


def evaluate(cos_theta: float, sigma_cos: float, abs_chern: float, sigma_chern: float,
             n_transverse: float, sigma_transverse: float) -> dict:
    estimates = [
        drive_estimate(cos_theta, sigma_cos),
        chern_estimate(abs_chern, sigma_chern),
        carrier_estimate(n_transverse, sigma_transverse),
    ]
    consensus = weighted_consensus(estimates)
    return {
        "bt": 1209,
        "title": "Lambda-lock demonstrator inference protocol",
        "inputs": {
            "cos_theta_BC": cos_theta,
            "sigma_cos_theta_BC": sigma_cos,
            "abs_chern": abs_chern,
            "sigma_abs_chern": sigma_chern,
            "n_transverse": n_transverse,
            "sigma_n_transverse": sigma_transverse,
        },
        "estimates": [asdict(e) for e in estimates],
        "consensus": consensus,
        "pass_condition": "All three channels and the weighted consensus contain q=3 in their 3-sigma intervals.",
        "passes_lambda_lock_protocol": all(e.q3_inside_3sigma for e in estimates) and consensus["q3_inside_3sigma"],
        "falsifies_if": "Any channel excludes q=3 after calibrated systematics are included, or the three channels give incompatible q values.",
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--cos-theta", type=float, default=-2/3)
    p.add_argument("--sigma-cos", type=float, default=0.002)
    p.add_argument("--chern", type=float, default=2.0)
    p.add_argument("--sigma-chern", type=float, default=0.05)
    p.add_argument("--n-transverse", type=float, default=2.0)
    p.add_argument("--sigma-transverse", type=float, default=0.0)
    p.add_argument("--out", type=Path, default=Path("data/bt1209_lambda_lock_demonstrator_protocol.json"))
    args = p.parse_args()
    result = evaluate(args.cos_theta, args.sigma_cos, args.chern, args.sigma_chern,
                      args.n_transverse, args.sigma_transverse)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt": 1209, "passes": result["passes_lambda_lock_protocol"], "out": str(args.out)}, indent=2))


if __name__ == "__main__":
    main()
