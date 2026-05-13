#!/usr/bin/env python3
"""Part DCX: directional phase-evolution bridge.

Combines:
  - DCIX directional split: forward=21, backward=21,
  - DCV phase regimes from rho^t thresholds.

For each discrete time t, define directional residuals:

  F_t = 21 * rho^t,
  B_t = 21 * rho^t,
  O_t = F_t + B_t = 42 * rho^t.

Thresholds per direction:
    F_t <= 1/2 and B_t <= 1/2   <=> rho^t <= 1/42   (t=8)
    F_t <= 1/48 and B_t <= 1/48 <=> rho^t <= 1/1008 (t=14)
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DIR_PATH = ROOT / "data" / "tomotope_toroidal_directional_split_bridge.json"
PHASE_PATH = ROOT / "data" / "tomotope_toroidal_markov_phase_regime_bridge.json"
OUT_PATH = ROOT / "data" / "tomotope_toroidal_directional_phase_bridge.json"


def _regime_label(t: int, t_half: int, t_packet: int) -> str:
    if t < t_half:
        return "direction_pre_half_resolution"
    if t < t_packet:
        return "direction_half_resolved_packet_unresolved"
    return "direction_full_packet_resolution"


@dataclass(frozen=True)
class DirectionalPhaseSummary:
    spectral_radius: float
    forward_count: int
    backward_count: int
    directional_half_horizon_steps: int
    directional_packet_horizon_steps: int
    table_max_t: int
    middle_regime_steps: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    directional = json.loads(DIR_PATH.read_text(encoding="utf-8"))
    phase = json.loads(PHASE_PATH.read_text(encoding="utf-8"))

    rho = float(phase["summary"]["spectral_radius"])
    forward = int(directional["summary"]["forward_oriented_count"])
    backward = int(directional["summary"]["backward_oriented_count"])

    # Per-direction thresholds.
    half_threshold = 1.0 / 2.0
    packet_threshold = 1.0 / 48.0

    t_half = 0
    while (forward * (rho**t_half)) > half_threshold:
        t_half += 1

    t_packet = 0
    while (forward * (rho**t_packet)) > packet_threshold:
        t_packet += 1

    table_max_t = t_packet + 3
    rows: list[dict[str, Any]] = []
    for t in range(table_max_t + 1):
        f_t = forward * (rho**t)
        b_t = backward * (rho**t)
        o_t = f_t + b_t
        rows.append(
            {
                "t": t,
                "forward_residual": f_t,
                "backward_residual": b_t,
                "oriented_residual": o_t,
                "forward_half_resolved": f_t <= half_threshold,
                "forward_packet_resolved": f_t <= packet_threshold,
                "regime": _regime_label(t, t_half, t_packet),
            }
        )

    regime_counts = {
        "direction_pre_half_resolution": sum(1 for r in rows if r["regime"] == "direction_pre_half_resolution"),
        "direction_half_resolved_packet_unresolved": sum(
            1 for r in rows if r["regime"] == "direction_half_resolved_packet_unresolved"
        ),
        "direction_full_packet_resolution": sum(
            1 for r in rows if r["regime"] == "direction_full_packet_resolution"
        ),
    }

    identities = {
        "upstream_directional_identities_hold": bool(directional["summary"]["all_identities_hold"]),
        "upstream_phase_identities_hold": bool(phase["summary"]["all_identities_hold"]),
        "forward_equals_backward": forward == backward == 21,
        "half_horizon_expected_8": t_half == 8,
        "packet_horizon_expected_14": t_packet == 14,
        "middle_regime_count_matches_gap": (
            regime_counts["direction_half_resolved_packet_unresolved"] == (t_packet - t_half)
        ),
        "half_cross_minimal": rows[t_half]["forward_half_resolved"]
        and (t_half == 0 or not rows[t_half - 1]["forward_half_resolved"]),
        "packet_cross_minimal": rows[t_packet]["forward_packet_resolved"]
        and (t_packet == 0 or not rows[t_packet - 1]["forward_packet_resolved"]),
    }

    summary = DirectionalPhaseSummary(
        spectral_radius=rho,
        forward_count=forward,
        backward_count=backward,
        directional_half_horizon_steps=t_half,
        directional_packet_horizon_steps=t_packet,
        table_max_t=table_max_t,
        middle_regime_steps=regime_counts["direction_half_resolved_packet_unresolved"],
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "regime_counts": regime_counts,
        "table": rows,
        "identities": identities,
        "notes": (
            "DCX aligns directional 21/21 transport with phase regimes: each direction "
            "crosses half-resolution at t=8 and packet-resolution at t=14, yielding a "
            "6-step intermediate window for linear directional residuals."
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
