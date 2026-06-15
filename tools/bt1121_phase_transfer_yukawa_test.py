#!/usr/bin/env python3
"""BT1121 phase-transfer Koide/Yukawa diagnostic.

This is not a mass fit. It evaluates the phase-transfer map selected in BT1118:
reservoir phase/order theta feeds a Koide-radius square-root Yukawa vector.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def vector(theta: float, amplitude: float) -> list[float]:
    return [1.0 + amplitude * math.cos(theta + 2.0 * math.pi * g / 3.0) for g in range(3)]


def koide_Q(xs: list[float]) -> float:
    s1 = sum(xs)
    s2 = sum(x * x for x in xs)
    return s2 / (s1 * s1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--theta", type=float, default=0.2223, help="phase in radians")
    parser.add_argument("--epsilon", type=float, default=0.1, help="small reservoir projector amplitude")
    parser.add_argument("--out", default="data/bt1121_phase_transfer_yukawa_test.json")
    args = parser.parse_args()

    reservoir_weights = vector(args.theta, args.epsilon)
    yukawa_sqrt = vector(args.theta, math.sqrt(2.0))
    yukawa_Q = koide_Q(yukawa_sqrt)
    reservoir_Q = koide_Q(reservoir_weights)
    out = {
        "theorem": "BT1121 phase-transfer Yukawa diagnostic",
        "theta": args.theta,
        "epsilon": args.epsilon,
        "reservoir_weights": reservoir_weights,
        "reservoir_Q_if_naive_mass_map": reservoir_Q,
        "yukawa_sqrt_vector_phase_transfer": yukawa_sqrt,
        "yukawa_Q": yukawa_Q,
        "exact_koide_Q": 2.0 / 3.0,
        "koide_error": yukawa_Q - 2.0 / 3.0,
        "interpretation": "reservoir weights supply phase/order; Koide radius sqrt(2) supplies mass/Yukawa amplitude",
        "fit_claim": False,
    }
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
