#!/usr/bin/env python3
"""Part DCLXXXIII: holonomy q-Phi6 interface bridge.

Part DCLXXXII compressed the constitutive data to the reciprocal dimensionless
pair (Y,Z). The next deeper question is whether those channels already resolve
into the primitive ternary invariants q and Phi_6.

This verifier proves the stronger statement:

    Y^2 = q/(q^2+1) = q/(q+Phi_6) = k/v,
    1-Y^2 = Phi_6/(q^2+1) = Phi_6/(q+Phi_6),
    Z^2 = (q^2+1)/q = (q+Phi_6)/q = v/k,
    Z^2 - 1 = Phi_6/q.

So the reciprocal constitutive pair is already the q-versus-Phi_6 ternary
interface law of the 2-qutrit carrier.
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

from verify_dclxxxii_holonomy_ternary_admittance_bridge import build_bridge as build_admittance_bridge  # noqa: E402

OUT_PATH = ROOT / "data" / "dclxxxiii_holonomy_q_phi6_interface_bridge.json"


@dataclass(frozen=True)
class QPhi6InterfaceSummary:
    q: int
    phi6: int
    carrier_size: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    admittance = build_admittance_bridge()
    q = int(admittance["summary"]["q"])
    carrier_size = int(admittance["summary"]["carrier_size"])
    k = 12
    phi6 = q * q - q + 1
    Y = float(admittance["numerics"]["Y"])
    Z = float(admittance["numerics"]["Z"])
    Y2 = Y * Y
    Z2 = Z * Z

    identities = {
        "exchange_channel_square_is_q_over_q_squared_plus_1": abs(Y2 - q / (q * q + 1)) < 1e-12,
        "exchange_channel_square_is_q_over_q_plus_phi6": abs(Y2 - q / (q + phi6)) < 1e-12,
        "exchange_channel_square_is_exactly_k_over_v": abs(Y2 - k / carrier_size) < 1e-12,
        "exchange_complement_is_phi6_over_q_squared_plus_1": abs((1.0 - Y2) - phi6 / (q * q + 1)) < 1e-12,
        "exchange_odds_are_q_over_phi6": abs((Y2 / (1.0 - Y2)) - q / phi6) < 1e-12,
        "size_channel_square_is_q_squared_plus_1_over_q": abs(Z2 - (q * q + 1) / q) < 1e-12,
        "size_channel_square_is_q_plus_phi6_over_q": abs(Z2 - (q + phi6) / q) < 1e-12,
        "size_channel_square_is_exactly_v_over_k": abs(Z2 - carrier_size / k) < 1e-12,
        "excess_size_channel_is_phi6_over_q": abs((Z2 - 1.0) - phi6 / q) < 1e-12,
        "therefore_the_constitutive_pair_is_already_the_q_vs_phi6_interface_law": bool(
            abs(Y2 - q / (q + phi6)) < 1e-12
            and abs((1.0 - Y2) - phi6 / (q + phi6)) < 1e-12
            and abs(Z2 - (q + phi6) / q) < 1e-12
            and abs((Z2 - 1.0) - phi6 / q) < 1e-12
        ),
    }

    summary = QPhi6InterfaceSummary(
        q=q,
        phi6=phi6,
        carrier_size=carrier_size,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "ternary_interface": {
            "exchange_square": "Y^2 = q/(q^2+1) = q/(q+Phi_6) = k/v",
            "exchange_complement": "1-Y^2 = Phi_6/(q^2+1) = Phi_6/(q+Phi_6)",
            "size_square": "Z^2 = (q^2+1)/q = (q+Phi_6)/q = v/k",
            "size_excess": "Z^2 - 1 = Phi_6/q",
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
