#!/usr/bin/env python3
"""Part DCVI: quadratic transport-energy bridge.

Define the oriented-channel residual energy proxy:

  E_t = 42 * rho^(2t),

where 42 is the oriented toroidal transport count and rho is the nontrivial
spectral radius from DCIII.

This gives minimal integer horizons for:
  - one-channel energy threshold: E_t <= 1,
  - packet-probability energy threshold: E_t <= 1/24.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RELAX_PATH = ROOT / "data" / "tomotope_toroidal_markov_relaxation_bridge.json"
STEP_PATH = ROOT / "data" / "tomotope_toroidal_step_transport_bridge.json"
OUT_PATH = ROOT / "data" / "tomotope_toroidal_markov_energy_bridge.json"


def _min_horizon(base: float, threshold: float) -> int:
    t = 0
    while base**t > threshold:
        t += 1
    return t


@dataclass(frozen=True)
class EnergySummary:
    spectral_radius: float
    oriented_transport_count: int
    energy_decay_base: float
    one_channel_horizon_steps: int
    packet_energy_horizon_steps: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    relax = json.loads(RELAX_PATH.read_text(encoding="utf-8"))
    step = json.loads(STEP_PATH.read_text(encoding="utf-8"))

    upstream_ok = bool(relax["summary"]["all_identities_hold"]) and bool(step["summary"]["all_identities_hold"])
    rho = float(relax["summary"]["spectral_radius"])
    oriented = int(step["summary"]["oriented_transport_count"])

    base = rho * rho
    one_channel_threshold = 1.0 / oriented
    packet_threshold = 1.0 / (24.0 * oriented)

    t_one = _min_horizon(base, one_channel_threshold)
    t_packet = _min_horizon(base, packet_threshold)

    identities = {
        "upstream_identities_hold": upstream_ok,
        "base_between_zero_and_one": 0.0 < base < 1.0,
        "one_channel_horizon_hits": (base**t_one) <= one_channel_threshold,
        "one_channel_horizon_minimal": (t_one == 0) or (base ** (t_one - 1) > one_channel_threshold),
        "packet_horizon_hits": (base**t_packet) <= packet_threshold,
        "packet_horizon_minimal": (t_packet == 0) or (base ** (t_packet - 1) > packet_threshold),
        "expected_one_channel_horizon_4": t_one == 4,
        "expected_packet_horizon_7": t_packet == 7,
        "packet_horizon_not_earlier": t_packet >= t_one,
    }

    summary = EnergySummary(
        spectral_radius=rho,
        oriented_transport_count=oriented,
        energy_decay_base=base,
        one_channel_horizon_steps=t_one,
        packet_energy_horizon_steps=t_packet,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "thresholds": {
            "one_channel_threshold": one_channel_threshold,
            "packet_energy_threshold": packet_threshold,
        },
        "derived_values": {
            "energy_at_one_channel_horizon": oriented * (base**t_one),
            "energy_before_one_channel_horizon": oriented * (base ** (t_one - 1)) if t_one > 0 else oriented,
            "energy_at_packet_horizon": oriented * (base**t_packet),
            "energy_before_packet_horizon": oriented * (base ** (t_packet - 1)) if t_packet > 0 else oriented,
        },
        "identities": identities,
        "notes": (
            "DCVI tracks quadratic transport energy E_t=42*rho^(2t). The one-channel "
            "energy horizon is t=4 and the packet-probability energy horizon is t=7, "
            "mirroring the count/probability split at the quadratic mode level."
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
