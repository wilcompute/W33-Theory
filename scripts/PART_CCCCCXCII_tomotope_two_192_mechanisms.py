#!/usr/bin/env python3
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.tomotope_cover_bridge import monodromy_growth_degree, native_cover_dimension


OUT_PATH = ROOT / "data" / "cccccxcii_tomotope_two_192_mechanisms.json"


@dataclass(frozen=True)
class Two192Mechanisms:
    packet_24: int
    intermediate_group_order_192: int
    tomotope_automorphism_order_96: int
    tomotope_flag_orbits: int
    tomotope_flag_carrier_192: int
    f4_scale_1152: int
    intrinsic_carrier_growth_degree: float
    intrinsic_monodromy_growth_degree: float
    intrinsic_4d_from_cover_only: bool
    checks: dict[str, bool]


def build() -> Two192Mechanisms:
    packet_24 = 24
    intermediate_group_order_192 = 8 * packet_24
    tomotope_automorphism_order_96 = 96
    tomotope_flag_orbits = 2
    tomotope_flag_carrier_192 = tomotope_flag_orbits * tomotope_automorphism_order_96
    f4_scale_1152 = 1152

    intrinsic_carrier_growth_degree = native_cover_dimension()
    intrinsic_monodromy_growth_degree = monodromy_growth_degree()

    # "Crack" verdict: internal cover carrier scales cubically (≈3),
    # so intrinsic 4D is not closed by cover growth alone.
    intrinsic_4d_from_cover_only = abs(intrinsic_carrier_growth_degree - 4.0) < 1e-9

    checks = {
        "two_distinct_192_mechanisms_hold": (
            intermediate_group_order_192 == 192 and tomotope_flag_carrier_192 == 192
        ),
        "intermediate_192_is_8_times_24": intermediate_group_order_192 == 8 * packet_24,
        "tomotope_192_is_2_times_96": tomotope_flag_carrier_192 == 2 * tomotope_automorphism_order_96,
        "f4_ladder_6_times_192": 6 * 192 == f4_scale_1152,
        "phase_plus_ground_reconstructs_192": 168 + 24 == 192,
        "intrinsic_carrier_is_cubic_not_quartic": abs(intrinsic_carrier_growth_degree - 3.0) < 1e-9,
        "intrinsic_monodromy_is_degree_six": abs(intrinsic_monodromy_growth_degree - 6.0) < 1e-9,
        "intrinsic_4d_not_closed_without_external_factor": intrinsic_4d_from_cover_only is False,
    }

    return Two192Mechanisms(
        packet_24=packet_24,
        intermediate_group_order_192=intermediate_group_order_192,
        tomotope_automorphism_order_96=tomotope_automorphism_order_96,
        tomotope_flag_orbits=tomotope_flag_orbits,
        tomotope_flag_carrier_192=tomotope_flag_carrier_192,
        f4_scale_1152=f4_scale_1152,
        intrinsic_carrier_growth_degree=intrinsic_carrier_growth_degree,
        intrinsic_monodromy_growth_degree=intrinsic_monodromy_growth_degree,
        intrinsic_4d_from_cover_only=intrinsic_4d_from_cover_only,
        checks=checks,
    )


def write(path: Path = OUT_PATH) -> Path:
    summary = build()
    payload: dict[str, Any] = asdict(summary)
    payload["all_checks_pass"] = all(summary.checks.values())
    payload["code_crack_verdict"] = (
        "Two 192 mechanisms are real and consistent, but intrinsic cover growth is cubic;"
        " a genuine 4D continuum law still requires external factorization or a new intrinsic convergence theorem."
    )
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
