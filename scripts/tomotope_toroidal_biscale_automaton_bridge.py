#!/usr/bin/env python3
"""Part DCXX: bi-scale regime automaton bridge.

Combines two horizon systems:
  - linear directional: half=8, packet=14
  - quadratic energy:   half=4, packet=7

into a deterministic joint-state automaton over discrete time.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DCX_PATH = ROOT / "data" / "tomotope_toroidal_directional_phase_bridge.json"
DCVI_PATH = ROOT / "data" / "tomotope_toroidal_markov_energy_bridge.json"
OUT_PATH = ROOT / "data" / "tomotope_toroidal_biscale_automaton_bridge.json"


def _load_json_or_build(path: Path, module_name: str) -> dict[str, Any]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    module = __import__(module_name, fromlist=["build_bridge"])
    return module.build_bridge()


def _linear_regime(t: int, half: int, packet: int) -> str:
    if t < half:
        return "L_pre"
    if t < packet:
        return "L_mid"
    return "L_full"


def _energy_regime(t: int, half: int, packet: int) -> str:
    if t < half:
        return "E_pre"
    if t < packet:
        return "E_mid"
    return "E_full"


@dataclass(frozen=True)
class AutomatonSummary:
    linear_half_horizon: int
    linear_packet_horizon: int
    energy_half_horizon: int
    energy_packet_horizon: int
    distinct_joint_states: int
    first_linear_full_t: int
    first_energy_full_t: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    dcx = _load_json_or_build(DCX_PATH, "scripts.tomotope_toroidal_directional_phase_bridge")
    dcvi = _load_json_or_build(DCVI_PATH, "scripts.tomotope_toroidal_markov_energy_bridge")

    l_half = int(dcx["summary"]["directional_half_horizon_steps"])
    l_packet = int(dcx["summary"]["directional_packet_horizon_steps"])
    e_half = int(dcvi["summary"]["one_channel_horizon_steps"])
    e_packet = int(dcvi["summary"]["packet_energy_horizon_steps"])

    t_max = l_packet + 4
    timeline: list[dict[str, Any]] = []
    for t in range(t_max + 1):
        ls = _linear_regime(t, l_half, l_packet)
        es = _energy_regime(t, e_half, e_packet)
        timeline.append({"t": t, "linear": ls, "energy": es, "joint": f"{ls}|{es}"})

    joint_states = []
    seen = set()
    for row in timeline:
        j = row["joint"]
        if j not in seen:
            seen.add(j)
            joint_states.append(j)

    first_linear_full = next(r["t"] for r in timeline if r["linear"] == "L_full")
    first_energy_full = next(r["t"] for r in timeline if r["energy"] == "E_full")

    expected_joint_order = [
        "L_pre|E_pre",
        "L_pre|E_mid",
        "L_pre|E_full",
        "L_mid|E_full",
        "L_full|E_full",
    ]

    identities = {
        "upstream_dcx_ok": bool(dcx["summary"]["all_identities_hold"]),
        "upstream_dcvi_ok": bool(dcvi["summary"]["all_identities_hold"]),
        "horizons_exact": (l_half, l_packet, e_half, e_packet) == (8, 14, 4, 7),
        "energy_full_before_linear_full": first_energy_full < first_linear_full,
        "first_full_times_expected": (first_energy_full, first_linear_full) == (7, 14),
        "joint_state_count_is_5": len(joint_states) == 5,
        "joint_order_matches_expected": joint_states == expected_joint_order,
    }

    summary = AutomatonSummary(
        linear_half_horizon=l_half,
        linear_packet_horizon=l_packet,
        energy_half_horizon=e_half,
        energy_packet_horizon=e_packet,
        distinct_joint_states=len(joint_states),
        first_linear_full_t=first_linear_full,
        first_energy_full_t=first_energy_full,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "joint_state_order": joint_states,
        "timeline": timeline,
        "identities": identities,
        "notes": (
            "DCXX bi-scale automaton: combining linear and quadratic regime systems "
            "yields a 5-state deterministic cascade where energy reaches full resolution "
            "first (t=7), then linear reaches full resolution (t=14)."
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
