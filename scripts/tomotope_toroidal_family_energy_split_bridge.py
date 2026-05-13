#!/usr/bin/env python3
"""Part DCVIII: Csaszar/Szilassi family energy split bridge.

From DCVII and DCVI:
  - oriented transport shell = 21 + 21,
  - quadratic residual energy E_t = 42 * rho^(2t).

This part certifies exact per-family split:
  E_C(t) = 21 * rho^(2t),
  E_S(t) = 21 * rho^(2t),
  E_t    = E_C(t) + E_S(t).

It also tracks minimal horizons for family-level thresholds:
  E_family <= 1/2  and  E_family <= 1/48.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EDGE_PAIR_PATH = ROOT / "data" / "tomotope_toroidal_edge_pair_bridge.json"
RELAX_PATH = ROOT / "data" / "tomotope_toroidal_markov_relaxation_bridge.json"
OUT_PATH = ROOT / "data" / "tomotope_toroidal_family_energy_split_bridge.json"


def _min_horizon(base: float, threshold: float) -> int:
    t = 0
    while base**t > threshold:
        t += 1
    return t


@dataclass(frozen=True)
class FamilyEnergySummary:
    spectral_radius: float
    energy_decay_base: float
    csaszar_edges: int
    szilassi_edges: int
    oriented_edges_total: int
    family_half_channel_horizon_steps: int
    family_packet_horizon_steps: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    edge_pair = json.loads(EDGE_PAIR_PATH.read_text(encoding="utf-8"))
    relax = json.loads(RELAX_PATH.read_text(encoding="utf-8"))

    rho = float(relax["summary"]["spectral_radius"])
    base = rho * rho

    cs_edges = int(edge_pair["summary"]["csaszar_edges"])
    sz_edges = int(edge_pair["summary"]["szilassi_edges"])
    oriented = int(edge_pair["summary"]["oriented_transport_count"])

    # Family thresholds correspond to half of oriented shell thresholds.
    half_channel_threshold = 1.0 / cs_edges  # 1/21 -> E_family <= 1/2 means base^t <= 1/42; easier use explicit check below
    # Use direct family-energy thresholds:
    # 21*base^t <= 1/2  <=> base^t <= 1/42
    family_half_threshold = 1.0 / 42.0
    # 21*base^t <= 1/48 <=> base^t <= 1/1008
    family_packet_threshold = 1.0 / 1008.0

    t_half = _min_horizon(base, family_half_threshold)
    t_packet = _min_horizon(base, family_packet_threshold)

    identities = {
        "upstream_edge_pair_identities_hold": bool(edge_pair["summary"]["all_identities_hold"]),
        "upstream_relaxation_identities_hold": bool(relax["summary"]["all_identities_hold"]),
        "csaszar_edges_21": cs_edges == 21,
        "szilassi_edges_21": sz_edges == 21,
        "oriented_total_42": oriented == 42,
        "oriented_equals_dual_family_sum": oriented == cs_edges + sz_edges,
        "family_energies_equal": cs_edges == sz_edges,
        "family_half_horizon_expected_4": t_half == 4,
        "family_packet_horizon_expected_7": t_packet == 7,
        "family_horizon_order": t_half <= t_packet,
        "family_energy_half_hits": cs_edges * (base**t_half) <= 0.5,
        "family_energy_half_minimal": (t_half == 0) or (cs_edges * (base ** (t_half - 1)) > 0.5),
        "family_energy_packet_hits": cs_edges * (base**t_packet) <= (1.0 / 48.0),
        "family_energy_packet_minimal": (t_packet == 0)
        or (cs_edges * (base ** (t_packet - 1)) > (1.0 / 48.0)),
    }

    summary = FamilyEnergySummary(
        spectral_radius=rho,
        energy_decay_base=base,
        csaszar_edges=cs_edges,
        szilassi_edges=sz_edges,
        oriented_edges_total=oriented,
        family_half_channel_horizon_steps=t_half,
        family_packet_horizon_steps=t_packet,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "derived_values": {
            "family_energy_at_half_horizon": cs_edges * (base**t_half),
            "family_energy_before_half_horizon": cs_edges * (base ** (t_half - 1)) if t_half > 0 else cs_edges,
            "family_energy_at_packet_horizon": cs_edges * (base**t_packet),
            "family_energy_before_packet_horizon": cs_edges * (base ** (t_packet - 1)) if t_packet > 0 else cs_edges,
            "combined_energy_at_half_horizon": oriented * (base**t_half),
            "combined_energy_at_packet_horizon": oriented * (base**t_packet),
            "family_half_threshold": 0.5,
            "family_packet_threshold": 1.0 / 48.0,
            "base_half_threshold": family_half_threshold,
            "base_packet_threshold": family_packet_threshold,
            "base_inverse_cs_edges": half_channel_threshold,
        },
        "identities": identities,
        "notes": (
            "DCVIII certifies equal family shares in quadratic transport energy: "
            "Csaszar and Szilassi each carry 21*rho^(2t), exactly half of the oriented "
            "42*rho^(2t) shell at every step."
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
