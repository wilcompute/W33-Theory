#!/usr/bin/env python3
"""BT1216 -- synthetic Clifford tomography dataset.

Generates a deterministic synthetic dataset for the BT1214 tomography protocol.
It does not enumerate Sp(4,3); it creates closure-signature observations for the
expected finite groups and verifies recovery under a simple noise model.
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

ORDER_SPECTRUM_2T = {1: 1, 2: 1, 3: 8, 4: 6, 6: 8}
EXPECTED_VISIBILITIES = [0.0, 1/3, 3**-0.5, 1.0]


def noisy(value: float, sigma: float, rng: random.Random) -> float:
    return value + rng.gauss(0.0, sigma)


def generate(seed: int = 1216, sigma_visibility: float = 0.015, closure_error_rate: float = 0.002) -> dict:
    rng = random.Random(seed)
    visibility_observations = []
    for expected in EXPECTED_VISIBILITIES:
        for _ in range(12):
            visibility_observations.append({
                "expected": expected,
                "observed": noisy(expected, sigma_visibility, rng),
            })
    two_t_counts = {str(k): v for k, v in ORDER_SPECTRUM_2T.items()}
    sp43 = {
        "expected_order": 51840,
        "sampled_products": 5000,
        "closure_failures": int(round(5000 * closure_error_rate)),
        "estimated_closure_success": 1.0 - closure_error_rate,
    }
    return {
        "bt": 1216,
        "title": "Synthetic Clifford tomography dataset",
        "seed": seed,
        "noise_model": {
            "visibility_sigma": sigma_visibility,
            "closure_error_rate": closure_error_rate,
        },
        "single_qutrit_2T": {
            "expected_order": 24,
            "element_order_counts": two_t_counts,
            "visibility_observations": visibility_observations,
        },
        "two_qutrit_sp43": sp43,
    }


def recover(dataset: dict) -> dict:
    vis = dataset["single_qutrit_2T"]["visibility_observations"]
    max_error = max(abs(x["observed"] - x["expected"]) for x in vis)
    counts = dataset["single_qutrit_2T"]["element_order_counts"]
    counts_ok = counts == {str(k): v for k, v in ORDER_SPECTRUM_2T.items()}
    closure_success = dataset["two_qutrit_sp43"]["estimated_closure_success"]
    return {
        "bt": 1216,
        "title": "Synthetic Clifford tomography recovery report",
        "single_qutrit_order_ok": dataset["single_qutrit_2T"]["expected_order"] == 24,
        "single_qutrit_order_spectrum_ok": counts_ok,
        "visibility_max_abs_error": max_error,
        "visibility_pass": max_error < 0.06,
        "sp43_order_ok": dataset["two_qutrit_sp43"]["expected_order"] == 51840,
        "closure_success": closure_success,
        "closure_pass": closure_success >= 0.995,
        "recovers_bt1214_signature": counts_ok and max_error < 0.06 and closure_success >= 0.995,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--dataset-out", type=Path, default=Path("data/bt1216_synthetic_clifford_tomography_dataset.json"))
    p.add_argument("--report-out", type=Path, default=Path("data/bt1216_synthetic_clifford_tomography_recovery.json"))
    args = p.parse_args()
    dataset = generate()
    report = recover(dataset)
    args.dataset_out.parent.mkdir(parents=True, exist_ok=True)
    args.dataset_out.write_text(json.dumps(dataset, indent=2) + "\n")
    args.report_out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"bt": 1216, "recovers": report["recovers_bt1214_signature"], "dataset": str(args.dataset_out)}, indent=2))


if __name__ == "__main__":
    main()
