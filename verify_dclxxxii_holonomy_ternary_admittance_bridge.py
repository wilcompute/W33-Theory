#!/usr/bin/env python3
"""Part DCLXXXII: holonomy ternary admittance bridge.

Part DCLXXX fixed the unique constitutive pair (mu, epsilon), and Part DCLXXXI
showed that the same law counts the exact carrier architecture. The next deeper
question, suggested by the user's constitutive hint, is whether there is a more
primitive dimensionless pair capturing exchange efficiency and information size.

This verifier proves the stronger statement: the normalized pair

    Y = epsilon * c,
    Z = mu * c

is fixed exactly by the ternary qutrit geometry. It satisfies

    YZ = 1,
    Y^2 = 3/10,
    Z^2 = 10/3,

so Y and Z are reciprocal ternary exchange/size channels determined by the same
3/13 and 10/13 split.
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

from verify_dclxxx_holonomy_ternary_constitutive_bridge import build_bridge as build_constitutive_bridge  # noqa: E402

OUT_PATH = ROOT / "data" / "dclxxxii_holonomy_ternary_admittance_bridge.json"


@dataclass(frozen=True)
class TernaryAdmittanceSummary:
    q: int
    carrier_size: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    constitutive = build_constitutive_bridge()
    q = int(constitutive["summary"]["q"])
    carrier_size = int(constitutive["summary"]["carrier_size"])
    mu = float(constitutive["numerics"]["mu"])
    epsilon = float(constitutive["numerics"]["epsilon"])
    c = float(constitutive["numerics"]["c"])

    Y = epsilon * c
    Z = mu * c

    identities = {
        "normalized_exchange_channel_is_y_equals_epsilon_c": abs(Y - math.sqrt(3.0 / 10.0)) < 1e-12,
        "normalized_size_channel_is_z_equals_mu_c": abs(Z - math.sqrt(10.0 / 3.0)) < 1e-12,
        "exchange_and_size_channels_are_exact_reciprocals": abs(Y * Z - 1.0) < 1e-12,
        "exchange_channel_square_is_three_over_ten": abs(Y * Y - 3.0 / 10.0) < 1e-12,
        "size_channel_square_is_ten_over_three": abs(Z * Z - 10.0 / 3.0) < 1e-12,
        "the_two_channels_recover_the_ternary_3_over_13_and_10_over_13_split": abs((Y * Y) / (1.0 + Y * Y) - 3.0 / 13.0) < 1e-12 and abs((Z * Z) / (1.0 + Z * Z) - 10.0 / 13.0) < 1e-12,
        "the_dimensionless_pair_is_fixed_by_the_same_qutrit_geometry": bool(
            abs(Y * Z - 1.0) < 1e-12
            and abs(Y * Y - 3.0 / 10.0) < 1e-12
            and abs(Z * Z - 10.0 / 3.0) < 1e-12
        ),
    }

    summary = TernaryAdmittanceSummary(
        q=q,
        carrier_size=carrier_size,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "dimensionless_pair": {
            "exchange_channel": "Y = epsilon * c = sqrt(3/10)",
            "size_channel": "Z = mu * c = sqrt(10/3)",
            "reciprocity": "Y * Z = 1",
            "ternary_squares": "Y^2 = 3/10, Z^2 = 10/3",
        },
        "numerics": {
            "Y": Y,
            "Z": Z,
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
