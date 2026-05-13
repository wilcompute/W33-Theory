#!/usr/bin/env python3
"""Part DC: toroidal/tomotope Markov ground bridge.

This layer promotes the 7+1 packet split into a dynamical statement.

States:
  C1..C5,S1,S2,G  (7 active toroidal modes + 1 ground mode)

Transition design (all exact rationals):
  - From active mode i:
      self                1/8
      next on 7-cycle     3/8
      prev on 7-cycle     3/8
      ground              1/8
  - From ground mode G:
      stay in G           1/8
      to each active      1/8

The unique stationary distribution is uniform over 8 states:
  each state mass = 1/8,
  active aggregate mass = 7/8,
  ground mass = 1/8.

Multiplying by tomotope packet weight 192 gives:
  active weight  = 168,
  ground weight  = 24.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACKET_PATH = ROOT / "data" / "tomotope_toroidal_dual_packet_bridge.json"
OUT_PATH = ROOT / "data" / "tomotope_toroidal_markov_ground_bridge.json"


def _frac(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def _mat_vec_mul_row_vector(v: list[Fraction], p: list[list[Fraction]]) -> list[Fraction]:
    n = len(v)
    out = [Fraction(0, 1) for _ in range(n)]
    for j in range(n):
        out[j] = sum(v[i] * p[i][j] for i in range(n))
    return out


@dataclass(frozen=True)
class MarkovSummary:
    state_count: int
    active_state_count: int
    packet_total_weight: int
    stationary_active_mass_num: int
    stationary_active_mass_den: int
    stationary_ground_mass_num: int
    stationary_ground_mass_den: int
    stationary_active_weight: int
    stationary_ground_weight: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    packet = json.loads(PACKET_PATH.read_text(encoding="utf-8"))
    packet_total = int(packet["summary"]["tomotope_weight"])

    active = ["C1", "C2", "C3", "C4", "C5", "S1", "S2"]
    states = active + ["G"]
    n = len(states)
    g_idx = n - 1

    p = [[Fraction(0, 1) for _ in range(n)] for _ in range(n)]

    # Active rows: local cycle transport + ground leakage.
    for i in range(len(active)):
        p[i][i] = Fraction(1, 8)
        p[i][(i + 1) % len(active)] = Fraction(3, 8)
        p[i][(i - 1) % len(active)] = Fraction(3, 8)
        p[i][g_idx] = Fraction(1, 8)

    # Ground row: 1/8 stay, uniform 1/8 reinjection to each active mode.
    p[g_idx][g_idx] = Fraction(1, 8)
    for i in range(len(active)):
        p[g_idx][i] = Fraction(1, 8)

    row_sums = [sum(row) for row in p]

    # Exact stationary candidate: uniform over 8 states.
    pi = [Fraction(1, 8) for _ in range(n)]
    pi_p = _mat_vec_mul_row_vector(pi, p)

    active_mass = sum(pi[: len(active)])
    ground_mass = pi[g_idx]

    active_weight = int(active_mass * packet_total)
    ground_weight = int(ground_mass * packet_total)

    identities = {
        "all_rows_sum_to_one": all(value == Fraction(1, 1) for value in row_sums),
        "stationary_vector_fixed": pi_p == pi,
        "active_mass_is_7_over_8": active_mass == Fraction(7, 8),
        "ground_mass_is_1_over_8": ground_mass == Fraction(1, 8),
        "weights_are_168_and_24": (active_weight, ground_weight) == (168, 24),
        "active_weight_matches_packet_bridge": (
            active_weight == int(packet["summary"]["active_packet_weight"])
        ),
        "ground_weight_matches_packet_bridge": (
            ground_weight == int(packet["summary"]["ground_packet_weight"])
        ),
    }

    summary = MarkovSummary(
        state_count=n,
        active_state_count=len(active),
        packet_total_weight=packet_total,
        stationary_active_mass_num=active_mass.numerator,
        stationary_active_mass_den=active_mass.denominator,
        stationary_ground_mass_num=ground_mass.numerator,
        stationary_ground_mass_den=ground_mass.denominator,
        stationary_active_weight=active_weight,
        stationary_ground_weight=ground_weight,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "states": states,
        "transition_matrix": [[_frac(x) for x in row] for row in p],
        "row_sums": [_frac(value) for value in row_sums],
        "stationary_distribution": {states[i]: _frac(pi[i]) for i in range(n)},
        "identities": identities,
        "notes": (
            "The 7+1 toroidal/tomotope split is realized dynamically: in stationarity "
            "the chain carries 7/8 active mass and 1/8 ground mass, reproducing "
            "168/24 out of total packet weight 192."
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
