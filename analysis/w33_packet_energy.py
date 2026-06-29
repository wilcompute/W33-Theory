#!/usr/bin/env python3
"""Pass 48 - packet-scale ternary-vs-binary traffic.

Pass 47 computed the per-trit encoding tax.  This verifier pushes that tax
through one minimal worst-case Holonet control packet:

    16 route address reads + 48 body phase ticks + 8 Hesse/Pauli epilogue trits = 72.

The result is a bit-traffic accounting model, not a measured hardware power
number.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_packet_energy.json"


def load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def schema_size(packet: dict[str, Any], field: str) -> int:
    for row in packet["field_schema"]:
        if row["field"] == field:
            return int(row["size"])
    raise KeyError(field)


def build_certificate() -> dict[str, Any]:
    abi = load_json("data/bt1697_holonet_typed_packet_abi.json")
    per_trit = load_json("data/w33_ternary_energy.json")
    body_edges = schema_size(abi, "q6_body_edge")
    pulse_phases = schema_size(abi, "body_pulse_phase")
    hesse_size = schema_size(abi, "hesse_outcome")
    pauli_frame_size = schema_size(abi, "pauli_frame")

    route_hops = 2
    address_trits = 4
    endpoints_per_hop = 2
    route_address_reads = route_hops * endpoints_per_hop * address_trits
    body_phase_trits = body_edges * pulse_phases
    hesse_return_words = 3
    hesse_word_trits = round(math.log(hesse_size, 3))
    pauli_frame_trits = round(math.log(pauli_frame_size, 3))
    epilogue_trits = hesse_return_words * hesse_word_trits + pauli_frame_trits
    total_trits = route_address_reads + body_phase_trits + epilogue_trits

    info_bits = total_trits * math.log2(3)
    binary_host_bits = 2 * total_trits
    wasted_bits = binary_host_bits - info_bits
    tax = binary_host_bits / info_bits
    per_trit_tax = float(per_trit["bit_traffic_tax"])
    per_hop = {
        "route_address_reads_trits": route_address_reads // route_hops,
        "binary_bits": 2 * route_address_reads // route_hops,
        "ternary_information_bits": (route_address_reads // route_hops) * math.log2(3),
    }
    checks = {
        "abi_verified": abi["verified"] is True,
        "body_is_48_phase_trits": body_phase_trits == 48,
        "epilogue_is_8_trits": epilogue_trits == 8,
        "minimal_packet_is_72_trits": total_trits == 72,
        "packet_tax_matches_per_trit_tax": abs(tax - per_trit_tax) < 1e-3,
        "binary_host_uses_144_bits": binary_host_bits == 144,
    }
    return {
        "theorem": "Pass 48 Holonet packet energy traffic",
        "verified": all(checks.values()),
        "breakthrough": (
            "The per-trit 1.26x binary encoding tax becomes a per-minimal-packet "
            "tax on a 72-trit control transaction: a binary host moves 144 bits "
            "where the ternary information content is about 114.1 bits."
        ),
        "traffic_model": {
            "route_hops": route_hops,
            "route_address_reads_trits": route_address_reads,
            "body_phase_trits": body_phase_trits,
            "epilogue_trits": epilogue_trits,
            "total_packet_trits": total_trits,
            "per_hop": per_hop,
        },
        "binary_vs_ternary": {
            "ternary_information_bits": info_bits,
            "binary_host_bits": binary_host_bits,
            "wasted_bits": wasted_bits,
            "bit_traffic_tax": tax,
            "wasted_state_fraction_per_trit": per_trit["wasted_state_fraction"],
        },
        "source_certificates": [
            "data/bt1697_holonet_typed_packet_abi.json",
            "data/w33_ternary_energy.json",
        ],
        "claim_boundary": [
            "This is a traffic model for the minimal control packet, not a measured joule-per-packet hardware benchmark.",
            "The route model uses the worst-case diameter-2 Holonet path; adjacent nodes use one hop.",
            "Payload data scales linearly on top of this control envelope.",
        ],
        "checks": checks,
    }


def main() -> int:
    cert = build_certificate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(cert["theorem"])
    print(f"  verified: {cert['verified']}")
    print(
        "  packet traffic: "
        f"{cert['traffic_model']['total_packet_trits']} trits -> "
        f"{cert['binary_vs_ternary']['binary_host_bits']} binary host bits"
    )
    print(f"  wrote {OUT}")
    return 0 if cert["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
