#!/usr/bin/env python3
"""BT1212 -- adversarial uncertainty model for the lambda-lock demonstrator.

BT1209 gave a clean Gaussian inference protocol.  BT1212 adds systematic error
channels and computes conservative adversarial intervals for q_drive and q_chern.
The carrier channel is treated as a fixed physical boundary condition.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class ChannelBudget:
    channel: str
    nominal_q: float
    statistical_sigma_q: float
    systematic_half_width_q: float
    adversarial_interval: list[float]
    q3_inside_adversarial_interval: bool


def q_drive(cos_theta: float) -> float:
    return 1.0 / (1.0 + cos_theta)


def drive_budget(cos_theta: float, stat_sigma_cos: float, systematic_cos_terms: dict[str, float]) -> ChannelBudget:
    q = q_drive(cos_theta)
    derivative = abs(q * q)
    stat_sigma_q = derivative * stat_sigma_cos
    sys_half_width_q = derivative * sum(abs(v) for v in systematic_cos_terms.values())
    lo = q - 3.0 * stat_sigma_q - sys_half_width_q
    hi = q + 3.0 * stat_sigma_q + sys_half_width_q
    return ChannelBudget("drive", q, stat_sigma_q, sys_half_width_q, [lo, hi], lo <= 3.0 <= hi)


def chern_budget(abs_chern: float, stat_sigma_chern: float, systematic_chern_terms: dict[str, float]) -> ChannelBudget:
    q = abs_chern + 1.0
    stat_sigma_q = stat_sigma_chern
    sys_half_width_q = sum(abs(v) for v in systematic_chern_terms.values())
    lo = q - 3.0 * stat_sigma_q - sys_half_width_q
    hi = q + 3.0 * stat_sigma_q + sys_half_width_q
    return ChannelBudget("chern", q, stat_sigma_q, sys_half_width_q, [lo, hi], lo <= 3.0 <= hi)


def carrier_budget(n_transverse: float = 2.0) -> ChannelBudget:
    q = n_transverse + 1.0
    return ChannelBudget("carrier", q, 0.0, 0.0, [q, q], q == 3.0)


def evaluate() -> dict:
    cos_theta = -2.0 / 3.0
    abs_chern = 2.0
    drive_systematics = {
        "phase_lock_drift_cos": 0.0015,
        "dispersion_bias_cos": 0.0008,
        "recirculation_path_calibration_cos": 0.0007,
    }
    chern_systematics = {
        "gap_closing_misidentification": 0.020,
        "berry_grid_discretization": 0.025,
        "finite_sample_transfer_bias": 0.030,
    }
    budgets = [
        drive_budget(cos_theta, 0.0020, drive_systematics),
        chern_budget(abs_chern, 0.050, chern_systematics),
        carrier_budget(2.0),
    ]
    robust_pass = all(b.q3_inside_adversarial_interval for b in budgets)
    return {
        "bt": 1212,
        "title": "Lambda-lock adversarial uncertainty model",
        "inputs": {
            "cos_theta_BC": "-2/3",
            "abs_chern": 2.0,
            "n_transverse": 2.0,
            "drive_systematics": drive_systematics,
            "chern_systematics": chern_systematics,
        },
        "budgets": [asdict(b) for b in budgets],
        "robust_lambda_lock_pass": robust_pass,
        "rule": "Accept only if q=3 lies inside every adversarial interval after combining 3-sigma statistical width with worst-case systematic half-width.",
        "most_dangerous_channel": max(budgets, key=lambda b: (b.adversarial_interval[1] - b.adversarial_interval[0])).channel,
        "interpretation": "The drive channel is most sensitive because dq/dcos(theta)=q^2=9 at the holonet point; small BC-angle calibration biases amplify into q-estimator uncertainty.",
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, default=Path("data/bt1212_lambda_lock_adversary_model.json"))
    args = p.parse_args()
    result = evaluate()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bt": 1212, "robust_pass": result["robust_lambda_lock_pass"], "out": str(args.out)}, indent=2))


if __name__ == "__main__":
    main()
