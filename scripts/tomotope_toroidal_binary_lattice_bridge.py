#!/usr/bin/env python3
"""Part DCXIX: binary exponent-lattice bridge.

This part rewrites shell values in exponent coordinates relative to base 21:

  value = 21 * 2^n,  n in {0,1,2,3}.

Hence ladder values 21,42,84,168 become integer lattice points 0,1,2,3.
Operator identities become shift identities:

  D : n -> n+1,
  Q : n -> n-1,
  W : 1 -> 3,

with confluence:
  Q(W(1)) = D(1) = 2,
  W(1)    = D(D(1)) = 3.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DCXVII_PATH = ROOT / "data" / "tomotope_toroidal_universality_fixed_point_bridge.json"
DCXI_PATH = ROOT / "data" / "tomotope_toroidal_horizon_duality_bridge.json"
OUT_PATH = ROOT / "data" / "tomotope_toroidal_binary_lattice_bridge.json"


def _load_json_or_build(path: Path, module_name: str) -> dict[str, Any]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    module = __import__(module_name, fromlist=["build_bridge"])
    return module.build_bridge()


def _is_power_of_two(x: int) -> bool:
    return x > 0 and (x & (x - 1)) == 0


def _log2_int_power_of_two(x: int) -> int:
    # x must be a power of two
    return x.bit_length() - 1


@dataclass(frozen=True)
class LatticeSummary:
    base_shell: int
    exponent_base: int
    exponent_oriented: int
    exponent_quotient: int
    exponent_weighted: int
    linear_half_horizon: int
    linear_packet_horizon: int
    energy_half_horizon: int
    energy_packet_horizon: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    dcxvii = _load_json_or_build(
        DCXVII_PATH, "scripts.tomotope_toroidal_universality_fixed_point_bridge"
    )
    dcxi = _load_json_or_build(
        DCXI_PATH, "scripts.tomotope_toroidal_horizon_duality_bridge"
    )

    base = int(dcxvii["summary"]["base_shell"])
    oriented = int(dcxvii["summary"]["oriented_shell"])
    quotient = int(dcxvii["summary"]["quotient_shell"])
    weighted = int(dcxvii["summary"]["weighted_shell"])

    r_oriented = oriented // base
    r_quotient = quotient // base
    r_weighted = weighted // base

    e0 = 0
    e1 = _log2_int_power_of_two(r_oriented)
    e2 = _log2_int_power_of_two(r_quotient)
    e3 = _log2_int_power_of_two(r_weighted)

    # Operator actions on exponent lattice.
    D = lambda n: n + 1
    Q = lambda n: n - 1
    W = lambda n: 3 if n == 1 else None

    l_half = int(dcxi["summary"]["directional_half_horizon"])
    l_packet = int(dcxi["summary"]["directional_packet_horizon"])
    e_half = int(dcxi["summary"]["energy_one_channel_horizon"])
    e_packet = int(dcxi["summary"]["energy_packet_horizon"])

    identities = {
        "upstream_dcxvii_ok": bool(dcxvii["summary"]["all_identities_hold"]),
        "upstream_dcxi_ok": bool(dcxi["summary"]["all_identities_hold"]),
        "ratios_are_powers_of_two": all(
            _is_power_of_two(x) for x in [r_oriented, r_quotient, r_weighted]
        ),
        "exponents_are_0_1_2_3": (e0, e1, e2, e3) == (0, 1, 2, 3),
        "doubling_is_plus_one_shift": D(e0) == e1 and D(e1) == e2 and D(e2) == e3,
        "quotient_is_minus_one_shift": Q(e3) == e2 and Q(e2) == e1,
        "confluence_qw_equals_d": Q(W(1)) == D(1) == 2,
        "confluence_w_equals_dd": W(1) == D(D(1)) == 3,
        "horizon_pairs_exact": (l_half, l_packet, e_half, e_packet) == (8, 14, 4, 7),
        "horizon_gap_duality": (l_packet - l_half) == 2 * (e_packet - e_half) == 6,
    }

    summary = LatticeSummary(
        base_shell=base,
        exponent_base=e0,
        exponent_oriented=e1,
        exponent_quotient=e2,
        exponent_weighted=e3,
        linear_half_horizon=l_half,
        linear_packet_horizon=l_packet,
        energy_half_horizon=e_half,
        energy_packet_horizon=e_packet,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "values": {
            "base": base,
            "oriented": oriented,
            "quotient": quotient,
            "weighted": weighted,
        },
        "exponent_ladder": [e0, e1, e2, e3],
        "identities": identities,
        "notes": (
            "DCXIX lattice certificate: the shell bridge is an integer-shift system "
            "in binary exponent coordinates, with operator confluence and horizon-gap "
            "duality expressed as exact lattice equalities."
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
