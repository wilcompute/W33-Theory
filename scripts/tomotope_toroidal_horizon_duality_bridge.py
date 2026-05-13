#!/usr/bin/env python3
"""Part DCXI: horizon duality bridge (linear vs quadratic transport scales).

This layer links:
  - DCX linear directional horizons (t_half=8, t_packet=14),
  - DCVI quadratic energy horizons (t_one=4, t_packet_energy=7).

Because quadratic energy uses rho^(2t) while linear residual uses rho^t,
the same threshold families satisfy an exact integer doubling law:

  t_linear = 2 * t_quadratic.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DCX_PATH = ROOT / "data" / "tomotope_toroidal_directional_phase_bridge.json"
DCVI_PATH = ROOT / "data" / "tomotope_toroidal_markov_energy_bridge.json"
OUT_PATH = ROOT / "data" / "tomotope_toroidal_horizon_duality_bridge.json"


@dataclass(frozen=True)
class DualitySummary:
    directional_half_horizon: int
    directional_packet_horizon: int
    energy_one_channel_horizon: int
    energy_packet_horizon: int
    half_duality_factor: float
    packet_duality_factor: float
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    dcx = json.loads(DCX_PATH.read_text(encoding="utf-8"))
    dcvi = json.loads(DCVI_PATH.read_text(encoding="utf-8"))

    th = int(dcx["summary"]["directional_half_horizon_steps"])
    tp = int(dcx["summary"]["directional_packet_horizon_steps"])
    eh = int(dcvi["summary"]["one_channel_horizon_steps"])
    ep = int(dcvi["summary"]["packet_energy_horizon_steps"])

    half_factor = th / eh if eh != 0 else float("inf")
    packet_factor = tp / ep if ep != 0 else float("inf")

    identities = {
        "upstream_dcx_identities_hold": bool(dcx["summary"]["all_identities_hold"]),
        "upstream_dcvi_identities_hold": bool(dcvi["summary"]["all_identities_hold"]),
        "directional_half_is_8": th == 8,
        "energy_one_channel_is_4": eh == 4,
        "directional_packet_is_14": tp == 14,
        "energy_packet_is_7": ep == 7,
        "half_doubling_law": th == 2 * eh,
        "packet_doubling_law": tp == 2 * ep,
        "ratio_half_exactly_two": half_factor == 2.0,
        "ratio_packet_exactly_two": packet_factor == 2.0,
    }

    summary = DualitySummary(
        directional_half_horizon=th,
        directional_packet_horizon=tp,
        energy_one_channel_horizon=eh,
        energy_packet_horizon=ep,
        half_duality_factor=half_factor,
        packet_duality_factor=packet_factor,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "identities": identities,
        "notes": (
            "DCXI duality: moving from linear directional decay rho^t to quadratic "
            "energy decay rho^(2t) halves the minimal integer horizons for matched "
            "threshold families, giving exact 8↔4 and 14↔7 correspondences."
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
