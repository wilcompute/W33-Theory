#!/usr/bin/env python3
"""Part DCIII: relaxation-scale bridge for toroidal Markov transport.

Builds on DCII closed-form nontrivial modes

  lambda_k = 1/8 + (3/4) cos(2*pi*k/7),  k=1..6

and extracts:
  - the nontrivial spectral radius rho,
  - relaxation gap gamma = 1-rho,
  - smallest t with rho^t <= 1/24 (packet-resolution damping scale).
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
FOURIER_PATH = ROOT / "data" / "tomotope_toroidal_markov_fourier_bridge.json"
OUT_PATH = ROOT / "data" / "tomotope_toroidal_markov_relaxation_bridge.json"


def _nontrivial_modes() -> list[float]:
    modes = []
    for k in range(1, 7):
        modes.append(1.0 / 8.0 + (3.0 / 4.0) * math.cos(2.0 * math.pi * k / 7.0))
    return modes


@dataclass(frozen=True)
class RelaxationSummary:
    nontrivial_mode_count: int
    spectral_radius: float
    relaxation_gap: float
    packet_resolution: float
    packet_resolution_steps: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    fourier = json.loads(FOURIER_PATH.read_text(encoding="utf-8"))
    upstream_ok = bool(fourier["summary"]["all_identities_hold"])

    modes = _nontrivial_modes()
    rho = max(abs(x) for x in modes)
    gap = 1.0 - rho

    packet_resolution = 1.0 / 24.0
    t = 0
    while rho**t > packet_resolution:
        t += 1

    identities = {
        "upstream_fourier_identities_hold": upstream_ok,
        "spectral_radius_below_one": rho < 1.0,
        "relaxation_gap_positive": gap > 0.0,
        "rho_power_t_below_packet_resolution": rho**t <= packet_resolution,
        "rho_power_t_minus_1_above_packet_resolution": (t == 0) or (rho ** (t - 1) > packet_resolution),
        "damping_within_7_steps": t <= 7,
    }

    summary = RelaxationSummary(
        nontrivial_mode_count=6,
        spectral_radius=rho,
        relaxation_gap=gap,
        packet_resolution=packet_resolution,
        packet_resolution_steps=t,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "nontrivial_modes": modes,
        "identities": identities,
        "notes": (
            "Relaxation bridge: nontrivial toroidal transport modes contract at rate rho. "
            "The first step count where rho^t drops below packet resolution 1/24 gives "
            "the finite damping horizon for active-sector transport remnants."
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
