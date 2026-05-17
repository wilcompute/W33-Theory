#!/usr/bin/env python3
"""E6 -> SO(10) x U(1) charge-moment bridge.

This bridge turns the branching packet

    27 = 16_{-1} + 10_{+2} + 1_{-4}

into exact integer moment identities and connects them to existing W33/E8
count surfaces:

* M0 = sum(dim) = 27
* M1 = sum(dim * q) = 0
* M2 = sum(dim * q^2) = 72
* M3 = sum(dim * q^3) = 0

for one generation, and by q=3 generations:

* M0^(3gen) = 81
* M1^(3gen) = 0
* M2^(3gen) = 216
* M3^(3gen) = 0.

Notably, M2(one gen)=72 matches the E6 root count, while M0(3gen)=81
matches the g1 matter-sector count used throughout the W33/E8 chain.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "data" / "w33_e6_so10_charge_moment_bridge.json"


@dataclass(frozen=True)
class ChargeMomentSummary:
    generations: int
    one_gen_m0: int
    one_gen_m1: int
    one_gen_m2: int
    one_gen_m3: int
    three_gen_m0: int
    three_gen_m1: int
    three_gen_m2: int
    three_gen_m3: int
    all_identities_hold: bool


def _moment(packet: list[tuple[int, int]], power: int) -> int:
    return sum(dim * (charge**power) for dim, charge in packet)


def build_bridge() -> dict[str, Any]:
    # 27 = 16_{-1} + 10_{+2} + 1_{-4}
    packet = [(16, -1), (10, 2), (1, -4)]
    generations = 3

    m0 = _moment(packet, 0)
    m1 = _moment(packet, 1)
    m2 = _moment(packet, 2)
    m3 = _moment(packet, 3)

    m0_3 = generations * m0
    m1_3 = generations * m1
    m2_3 = generations * m2
    m3_3 = generations * m3

    # Existing exact decomposition surface used in root-refinement chain.
    e6_roots = 72
    a2_roots = 6
    g1_roots = 81
    g2_roots = 81
    total_roots = 240

    identities = {
        "branching_dimension_is_27": m0 == 27,
        "u1_linear_moment_cancels": m1 == 0,
        "u1_cubic_moment_cancels": m3 == 0,
        "quadratic_moment_is_72": m2 == 72,
        "three_generation_dimension_is_81": m0_3 == 81,
        "three_generation_linear_moment_cancels": m1_3 == 0,
        "three_generation_cubic_moment_cancels": m3_3 == 0,
        "three_generation_quadratic_moment_is_216": m2_3 == 216,
        "m2_matches_e6_root_count": m2 == e6_roots,
        "m0_three_gen_matches_g1_sector": m0_3 == g1_roots,
        "root_split_is_72_6_81_81": e6_roots + a2_roots + g1_roots + g2_roots == total_roots,
    }

    summary = ChargeMomentSummary(
        generations=generations,
        one_gen_m0=m0,
        one_gen_m1=m1,
        one_gen_m2=m2,
        one_gen_m3=m3,
        three_gen_m0=m0_3,
        three_gen_m1=m1_3,
        three_gen_m2=m2_3,
        three_gen_m3=m3_3,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "branching_packet": {
            "decomposition": [
                {"dim": 16, "u1_charge": -1},
                {"dim": 10, "u1_charge": 2},
                {"dim": 1, "u1_charge": -4},
            ],
            "label": "27 = 16_{-1} + 10_{+2} + 1_{-4}",
        },
        "moments": {
            "one_generation": {"m0": m0, "m1": m1, "m2": m2, "m3": m3},
            "three_generations": {"m0": m0_3, "m1": m1_3, "m2": m2_3, "m3": m3_3},
        },
        "root_split": {
            "e6_roots": e6_roots,
            "a2_roots": a2_roots,
            "g1_roots": g1_roots,
            "g2_roots": g2_roots,
            "total": total_roots,
            "identity": "240 = 72 + 6 + 81 + 81",
        },
        "identities": identities,
        "notes": (
            "Charge moments provide an exact arithmetic bridge from the SO(10)xU(1) "
            "branching packet to the root/matter count surfaces used in the W33-E8 chain."
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
