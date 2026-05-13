#!/usr/bin/env python3
"""Part DCIV: finite damping-horizon certificate for toroidal Markov transport.

Builds on DCIII (rho, gap, packet-resolution horizon) and adds two explicit
threshold horizons:

1) Probability-packet resolution:
     rho^t <= 1/24
2) Active packet-count resolution (7 active packets):
     7 * rho^t <= 1

Both are solved as minimal integer horizons with exact inequality checks.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RELAX_PATH = ROOT / "data" / "tomotope_toroidal_markov_relaxation_bridge.json"
OUT_PATH = ROOT / "data" / "tomotope_toroidal_markov_horizon_bridge.json"


def _min_horizon(base: float, threshold: float) -> int:
    t = 0
    while base**t > threshold:
        t += 1
    return t


@dataclass(frozen=True)
class HorizonSummary:
    spectral_radius: float
    probability_threshold: float
    active_packet_threshold: float
    probability_horizon_steps: int
    active_packet_horizon_steps: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    relax = json.loads(RELAX_PATH.read_text(encoding="utf-8"))
    summary = relax["summary"]
    upstream_ok = bool(summary["all_identities_hold"])

    rho = float(summary["spectral_radius"])
    prob_threshold = 1.0 / 24.0
    active_packet_threshold = 1.0 / 7.0

    t_prob = _min_horizon(rho, prob_threshold)
    t_active = _min_horizon(rho, active_packet_threshold)

    identities = {
        "upstream_relaxation_identities_hold": upstream_ok,
        "rho_between_zero_and_one": 0.0 < rho < 1.0,
        "probability_horizon_hits_threshold": rho**t_prob <= prob_threshold,
        "probability_horizon_is_minimal": (t_prob == 0) or (rho ** (t_prob - 1) > prob_threshold),
        "active_packet_horizon_hits_threshold": rho**t_active <= active_packet_threshold,
        "active_packet_horizon_is_minimal": (t_active == 0) or (rho ** (t_active - 1) > active_packet_threshold),
        "probability_horizon_expected_7": t_prob == 7,
        "active_packet_horizon_expected_4": t_active == 4,
        "active_horizon_no_later_than_probability_horizon": t_active <= t_prob,
    }

    result = HorizonSummary(
        spectral_radius=rho,
        probability_threshold=prob_threshold,
        active_packet_threshold=active_packet_threshold,
        probability_horizon_steps=t_prob,
        active_packet_horizon_steps=t_active,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(result),
        "identities": identities,
        "derived_values": {
            "rho_pow_probability_horizon": rho**t_prob,
            "rho_pow_active_packet_horizon": rho**t_active,
            "active_packet_bound_at_horizon": 7.0 * (rho**t_active),
            "active_packet_bound_before_horizon": 7.0 * (rho ** (t_active - 1)) if t_active > 0 else 7.0,
        },
        "notes": (
            "DCIV distinguishes two finite damping scales: one-packet probability "
            "resolution (1/24) at t=7 and one-active-packet-count resolution (1/7) "
            "at t=4."
        ),
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
