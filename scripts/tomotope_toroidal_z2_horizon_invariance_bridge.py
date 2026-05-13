#!/usr/bin/env python3
"""Part DCXVI: Z2 horizon-invariance bridge.

Proves that the swap involution from DCXIII preserves damping horizons:

  forward horizon == backward horizon,

for both linear directional thresholds (DCX), and remains compatible with the
linear/quadratic duality (DCXI).
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
Z2_PATH = ROOT / "data" / "tomotope_toroidal_z2_swap_symmetry_bridge.json"
DCX_PATH = ROOT / "data" / "tomotope_toroidal_directional_phase_bridge.json"
DCXI_PATH = ROOT / "data" / "tomotope_toroidal_horizon_duality_bridge.json"
OUT_PATH = ROOT / "data" / "tomotope_toroidal_z2_horizon_invariance_bridge.json"


def _load_z2_payload() -> dict[str, Any]:
    if Z2_PATH.exists():
        return json.loads(Z2_PATH.read_text(encoding="utf-8"))
    from scripts.tomotope_toroidal_z2_swap_symmetry_bridge import build_bridge

    return build_bridge()


def _load_dcx_payload() -> dict[str, Any]:
    if DCX_PATH.exists():
        return json.loads(DCX_PATH.read_text(encoding="utf-8"))
    from scripts.tomotope_toroidal_directional_phase_bridge import build_bridge

    return build_bridge()


def _load_dcxi_payload() -> dict[str, Any]:
    if DCXI_PATH.exists():
        return json.loads(DCXI_PATH.read_text(encoding="utf-8"))
    from scripts.tomotope_toroidal_horizon_duality_bridge import build_bridge

    return build_bridge()


@dataclass(frozen=True)
class HorizonInvarianceSummary:
    spectral_radius: float
    forward_half_horizon: int
    backward_half_horizon: int
    forward_packet_horizon: int
    backward_packet_horizon: int
    energy_half_horizon: int
    energy_packet_horizon: int
    all_identities_hold: bool


def _min_horizon(rho: float, count: int, threshold: float) -> int:
    t = 0
    while count * (rho**t) > threshold:
        t += 1
    return t


def build_bridge() -> dict[str, Any]:
    z2 = _load_z2_payload()
    dcx = _load_dcx_payload()
    dcxi = _load_dcxi_payload()

    rho = float(dcx["summary"]["spectral_radius"])
    forward = int(z2["summary"]["forward_count"])
    backward = int(z2["summary"]["backward_count"])

    half_threshold = 1.0 / 2.0
    packet_threshold = 1.0 / 48.0

    f_half = _min_horizon(rho, forward, half_threshold)
    b_half = _min_horizon(rho, backward, half_threshold)
    f_packet = _min_horizon(rho, forward, packet_threshold)
    b_packet = _min_horizon(rho, backward, packet_threshold)

    e_half = int(dcxi["summary"]["energy_one_channel_horizon"])
    e_packet = int(dcxi["summary"]["energy_packet_horizon"])

    identities = {
        "upstream_z2_identities_hold": bool(z2["summary"]["all_identities_hold"]),
        "upstream_dcx_identities_hold": bool(dcx["summary"]["all_identities_hold"]),
        "upstream_dcxi_identities_hold": bool(dcxi["summary"]["all_identities_hold"]),
        "forward_backward_counts_equal": forward == backward == 21,
        "half_horizon_swap_invariant": f_half == b_half,
        "packet_horizon_swap_invariant": f_packet == b_packet,
        "linear_horizons_expected": (f_half, f_packet) == (8, 14),
        "linear_horizons_match_dcx": (
            f_half == int(dcx["summary"]["directional_half_horizon_steps"])
            and f_packet == int(dcx["summary"]["directional_packet_horizon_steps"])
        ),
        "duality_half_preserved": f_half == 2 * e_half,
        "duality_packet_preserved": f_packet == 2 * e_packet,
    }

    summary = HorizonInvarianceSummary(
        spectral_radius=rho,
        forward_half_horizon=f_half,
        backward_half_horizon=b_half,
        forward_packet_horizon=f_packet,
        backward_packet_horizon=b_packet,
        energy_half_horizon=e_half,
        energy_packet_horizon=e_packet,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "identities": identities,
        "notes": (
            "DCXVI proves swap-invariance of directional damping horizons and confirms "
            "the same linear/quadratic duality survives under Z2 quotient symmetry."
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
