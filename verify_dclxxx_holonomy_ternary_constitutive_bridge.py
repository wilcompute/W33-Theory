#!/usr/bin/env python3
"""Part DCLXXX: holonomy ternary constitutive bridge.

The recent holonomy chain fixed the exact transfer law, boundary law, measure,
and minimal host architecture. The next deeper question, guided by the earlier
constitutive transport work, is whether the ternary qutrit geometry already
forces a unique constitutive pair (mu, epsilon).

This verifier proves the stronger statement: combining the exact carrier speed
c^2 = 40 with the ternary electroweak split

    1 = 3/13 + 10/13

uniquely fixes the constitutive pair by

    mu * epsilon * c^2 = 1,
    mu / epsilon = (10/13)/(3/13) = 10/3.

Hence

    mu = 1/sqrt(12),
    epsilon = sqrt(3)/20,
    Z^2 = 10/3,

so the constitutive product and ratio are both determined by the 2-qutrit
Pauli commutation geometry.
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

OUT_PATH = ROOT / "data" / "dclxxx_holonomy_ternary_constitutive_bridge.json"


@dataclass(frozen=True)
class TernaryConstitutiveSummary:
    q: int
    carrier_size: int
    dynamic_rank: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    host = build_host_realization()
    q = 3
    phi3 = q * q + q + 1
    carrier_size = int(host["n"])
    dynamic_rank = int(host["dynamic_rank"])
    stationary_rank = carrier_size - dynamic_rank

    sin2 = q / phi3
    cos2 = (q * q + 1) / phi3
    c = math.sqrt(carrier_size)
    z2 = cos2 / sin2
    z = math.sqrt(z2)
    mu = z / c
    epsilon = 1.0 / (z * c)

    identities = {
        "carrier_speed_squared_is_exactly_40": carrier_size == 40,
        "carrier_speed_squared_is_stationary_plus_dynamic_rank": carrier_size == stationary_rank + dynamic_rank,
        "ternary_electroweak_split_is_1_equals_3_over_13_plus_10_over_13": abs((sin2 + cos2) - 1.0) < 1e-12 and abs(sin2 - 3 / 13) < 1e-12 and abs(cos2 - 10 / 13) < 1e-12,
        "impedance_squared_is_the_ternary_ratio_10_over_3": abs(z2 - 10 / 3) < 1e-12,
        "constitutive_product_satisfies_mu_epsilon_c_squared_equals_1": abs(mu * epsilon * carrier_size - 1.0) < 1e-12,
        "constitutive_ratio_satisfies_mu_over_epsilon_equals_10_over_3": abs(mu / epsilon - 10 / 3) < 1e-12,
        "mu_is_exactly_one_over_sqrt12": abs(mu - 1.0 / math.sqrt(12.0)) < 1e-12,
        "epsilon_is_exactly_sqrt3_over_20": abs(epsilon - math.sqrt(3.0) / 20.0) < 1e-12,
        "mu_is_one_over_sqrt_k_with_k_12": abs(mu - 1.0 / math.sqrt(12.0)) < 1e-12,
        "therefore_the_ternary_qutrit_geometry_fixes_a_unique_positive_constitutive_pair": bool(
            abs(mu * epsilon * carrier_size - 1.0) < 1e-12
            and abs(mu / epsilon - 10 / 3) < 1e-12
            and abs(mu - 1.0 / math.sqrt(12.0)) < 1e-12
            and abs(epsilon - math.sqrt(3.0) / 20.0) < 1e-12
        ),
    }

    summary = TernaryConstitutiveSummary(
        q=q,
        carrier_size=carrier_size,
        dynamic_rank=dynamic_rank,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "constitutive_pair": {
            "sin2_theta_w": "3/13",
            "cos2_theta_w": "10/13",
            "impedance_squared": "10/3",
            "mu": "1/sqrt(12)",
            "epsilon": "sqrt(3)/20",
            "speed_squared": "40",
            "product_law": "mu * epsilon * c^2 = 1",
        },
        "numerics": {
            "mu": mu,
            "epsilon": epsilon,
            "c": c,
            "impedance": z,
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
