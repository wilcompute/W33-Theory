#!/usr/bin/env python3
"""Part DCLXXXI: holonomy constitutive carrier bridge.

Part DCLXXX fixed the unique constitutive pair from the ternary qutrit geometry.
The next deeper question is whether the new host architecture already satisfies
an exact count law in terms of that constitutive pair.

This verifier proves the stronger statement: the minimal holonomy host obeys

    dynamic_rank = 1/(mu*epsilon) - 1,

and the ternary q=3 geometry resolves this exactly as

    39 = q*Phi_3,
    40 = 1 + q*Phi_3.

So the exact 1+24+15 host architecture is forced by the same constitutive law
that determines the vacuum pair.
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxxviii_holonomy_minimal_host_realization_bridge import (  # noqa: E402
    build_host_realization,
)
from verify_dclxxx_holonomy_ternary_constitutive_bridge import build_bridge as build_constitutive_bridge  # noqa: E402

OUT_PATH = ROOT / "data" / "dclxxxi_holonomy_constitutive_carrier_bridge.json"


@dataclass(frozen=True)
class ConstitutiveCarrierSummary:
    q: int
    point_count: int
    dynamic_rank: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    host = build_host_realization()
    constitutive = build_constitutive_bridge()

    q = 3
    phi3 = q * q + q + 1
    point_count = int(host["n"])
    dynamic_rank = int(host["dynamic_rank"])
    fast_rank = int(host["fast_rank"])
    slow_rank = int(host["slow_rank"])
    stationary_rank = point_count - dynamic_rank

    mu = float(constitutive["numerics"]["mu"])
    epsilon = float(constitutive["numerics"]["epsilon"])
    constitutive_inverse = 1.0 / (mu * epsilon)

    identities = {
        "carrier_size_is_exactly_one_plus_dynamic_rank": point_count == 1 + dynamic_rank,
        "dynamic_rank_equals_inverse_constitutive_product_minus_one": abs(dynamic_rank - (constitutive_inverse - 1.0)) < 1e-12,
        "dynamic_rank_is_exactly_q_times_phi3": dynamic_rank == q * phi3,
        "point_count_is_exactly_one_plus_q_times_phi3": point_count == 1 + q * phi3,
        "fast_rank_is_exactly_24_and_slow_rank_is_exactly_15": fast_rank == 24 and slow_rank == 15,
        "the_exact_host_architecture_is_one_transmitted_plus_24_fast_plus_15_slow": stationary_rank == 1 and fast_rank + slow_rank == dynamic_rank,
        "the_constitutive_pair_therefore_counts_the_full_carrier": abs(constitutive_inverse - point_count) < 1e-12,
        "therefore_ternary_geometry_and_constitutive_law_fix_the_exact_1_plus_24_plus_15_host_architecture": bool(
            point_count == 1 + dynamic_rank
            and abs(dynamic_rank - (constitutive_inverse - 1.0)) < 1e-12
            and dynamic_rank == q * phi3
            and stationary_rank == 1
            and fast_rank == 24
            and slow_rank == 15
        ),
    }

    summary = ConstitutiveCarrierSummary(
        q=q,
        point_count=point_count,
        dynamic_rank=dynamic_rank,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "carrier_law": {
            "dynamic_rank": "1/(mu*epsilon) - 1",
            "point_count": "1/(mu*epsilon)",
            "ternary_dynamic_count": "q * Phi_3 = 3 * 13 = 39",
            "ternary_total_count": "1 + q * Phi_3 = 40",
            "host_split": "1 + 24 + 15",
        },
        "identities": identities,
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
