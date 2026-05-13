#!/usr/bin/env python3
"""Part DCV: phase-regime bridge for toroidal Markov damping.

Consumes DCIV horizon data and builds a finite-time regime table for
residual transport amplitudes:

  A_t = 7 * rho^t         (active packet-count scale)
  P_t = rho^t             (probability amplitude scale)

Thresholds:
  A_t <= 1      <=> active-packet-count resolved
  P_t <= 1/24   <=> packet-probability resolved

This yields three discrete regimes:
  - pre-count-resolution:           t < t_active
  - count-resolved/prob-unresolved: t_active <= t < t_prob
  - full packet-resolution:         t >= t_prob
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
HORIZON_PATH = ROOT / "data" / "tomotope_toroidal_markov_horizon_bridge.json"
OUT_PATH = ROOT / "data" / "tomotope_toroidal_markov_phase_regime_bridge.json"


@dataclass(frozen=True)
class RegimeSummary:
    spectral_radius: float
    active_horizon_steps: int
    probability_horizon_steps: int
    table_max_t: int
    pre_count_resolution_steps: int
    count_only_resolution_steps: int
    full_packet_resolution_steps: int
    all_identities_hold: bool


def _regime_label(t: int, t_active: int, t_prob: int) -> str:
    if t < t_active:
        return "pre_count_resolution"
    if t < t_prob:
        return "count_resolved_probability_unresolved"
    return "full_packet_resolution"


def build_bridge() -> dict[str, Any]:
    horizon = json.loads(HORIZON_PATH.read_text(encoding="utf-8"))
    hs = horizon["summary"]

    rho = float(hs["spectral_radius"])
    t_active = int(hs["active_packet_horizon_steps"])
    t_prob = int(hs["probability_horizon_steps"])

    table_max_t = t_prob + 3
    rows: list[dict[str, Any]] = []
    for t in range(table_max_t + 1):
        p_t = rho**t
        a_t = 7.0 * p_t
        rows.append(
            {
                "t": t,
                "probability_residual": p_t,
                "active_packet_residual": a_t,
                "active_resolved": a_t <= 1.0,
                "probability_resolved": p_t <= (1.0 / 24.0),
                "regime": _regime_label(t, t_active, t_prob),
            }
        )

    regime_counts = {
        "pre_count_resolution": sum(1 for r in rows if r["regime"] == "pre_count_resolution"),
        "count_resolved_probability_unresolved": sum(
            1 for r in rows if r["regime"] == "count_resolved_probability_unresolved"
        ),
        "full_packet_resolution": sum(1 for r in rows if r["regime"] == "full_packet_resolution"),
    }

    identities = {
        "upstream_horizon_identities_hold": bool(hs["all_identities_hold"]),
        "horizon_order": t_active <= t_prob,
        "active_crosses_at_t_active": (rows[t_active]["active_resolved"] is True)
        and (t_active == 0 or rows[t_active - 1]["active_resolved"] is False),
        "probability_crosses_at_t_prob": (rows[t_prob]["probability_resolved"] is True)
        and (t_prob == 0 or rows[t_prob - 1]["probability_resolved"] is False),
        "middle_regime_exists": t_active < t_prob,
        "middle_regime_count_matches_gap": (
            regime_counts["count_resolved_probability_unresolved"] == (t_prob - t_active)
        ),
        "pre_regime_count_matches_active_horizon": (
            regime_counts["pre_count_resolution"] == t_active
        ),
        "full_regime_nonempty": regime_counts["full_packet_resolution"] >= 1,
    }

    summary = RegimeSummary(
        spectral_radius=rho,
        active_horizon_steps=t_active,
        probability_horizon_steps=t_prob,
        table_max_t=table_max_t,
        pre_count_resolution_steps=regime_counts["pre_count_resolution"],
        count_only_resolution_steps=regime_counts["count_resolved_probability_unresolved"],
        full_packet_resolution_steps=regime_counts["full_packet_resolution"],
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "regime_counts": regime_counts,
        "table": rows,
        "identities": identities,
        "notes": (
            "DCV exposes the finite decay phases explicitly. For this chain, active "
            "packet-count resolution starts at t=4, while packet-probability resolution "
            "starts at t=7, giving a 3-step intermediate regime."
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
