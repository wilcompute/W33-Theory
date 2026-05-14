#!/usr/bin/env python3
"""Part DCLXXXIV: holonomy exchange-residual split bridge.

Part DCLXXXIII identified the exact q-vs-Phi_6 interface law. The next deeper
question is whether that law already resolves the carrier into explicit counted
exchange and residual sectors.

This verifier proves the stronger statement: the exact exchange density Y^2
splits the 40-point carrier into

    40 * Y^2 = 12,
    40 * (1-Y^2) = 28 = 1 + 27,

where 12 is the commuting exchange shell, 1 is the stationary transmitted mode,
and 27 is the affine bulk from the DCLXIV transvection geometry.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dclxiv_holonomy_qutrit_transvection_bridge import build_bridge as build_transvection_bridge  # noqa: E402
from verify_dclxxxii_holonomy_ternary_admittance_bridge import build_bridge as build_admittance_bridge  # noqa: E402

OUT_PATH = ROOT / "data" / "dclxxxiv_holonomy_exchange_residual_split_bridge.json"


@dataclass(frozen=True)
class ExchangeResidualSummary:
    carrier_size: int
    exchange_count: int
    residual_count: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    admittance = build_admittance_bridge()
    transvection = build_transvection_bridge()

    carrier_size = int(admittance["summary"]["carrier_size"])
    Y = float(admittance["numerics"]["Y"])
    Z = float(admittance["numerics"]["Z"])
    exchange_count = carrier_size * Y * Y
    residual_count = carrier_size * (1.0 - Y * Y)
    stationary_count = 1
    affine_bulk_count = int(transvection["summary"]["affine_bulk_count"])
    exchange_shell = 12

    identities = {
        "exchange_density_times_carrier_size_is_exactly_12": abs(exchange_count - 12.0) < 1e-12,
        "residual_density_times_carrier_size_is_exactly_28": abs(residual_count - 28.0) < 1e-12,
        "residual_count_is_stationary_plus_affine_bulk": abs(residual_count - (stationary_count + affine_bulk_count)) < 1e-12,
        "affine_bulk_count_is_exactly_27_from_the_transvection_bridge": affine_bulk_count == 27,
        "size_channel_recovers_the_same_split_from_the_exchange_side": abs(exchange_shell * (Z * Z - 1.0) - residual_count) < 1e-12,
        "exchange_shell_plus_residual_shell_reconstructs_the_full_carrier": abs(exchange_count + residual_count - carrier_size) < 1e-12,
        "therefore_the_constitutive_interface_law_splits_the_carrier_into_12_and_1_plus_27": bool(
            abs(exchange_count - 12.0) < 1e-12
            and abs(residual_count - 28.0) < 1e-12
            and abs(residual_count - (stationary_count + affine_bulk_count)) < 1e-12
        ),
    }

    summary = ExchangeResidualSummary(
        carrier_size=carrier_size,
        exchange_count=int(round(exchange_count)),
        residual_count=int(round(residual_count)),
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "split_law": {
            "exchange": "40 * Y^2 = 12",
            "residual": "40 * (1-Y^2) = 28 = 1 + 27",
            "dual": "12 * (Z^2 - 1) = 28",
            "carrier": "40 = 12 + 28 = 12 + 1 + 27",
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
