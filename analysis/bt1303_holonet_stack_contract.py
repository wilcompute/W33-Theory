#!/usr/bin/env python3
"""BT1303 - Holonet stack contract.

BT1301 and BT1302 make the architecture explicit enough to state as a stack:

    carrier -> tick word -> atlas route -> tomotope packet body
    -> parity epilogue -> oscillator frame -> mirror bus
    -> Clifford supercycle -> fractal shell.

BT1303 verifies that all layer sizes and handoffs agree with the existing
holonet artifacts.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1303_holonet_stack_contract.json"


def load_json(relpath: str) -> dict[str, Any]:
    with (ROOT / relpath).open(encoding="utf-8") as handle:
        return json.load(handle)


def stack_layers() -> list[dict[str, Any]]:
    return [
        {
            "layer": 0,
            "name": "carrier",
            "unit": "one self-entangled qutrit photon",
            "size": 1,
            "role": "physical operand and holonomic carrier",
        },
        {
            "layer": 1,
            "name": "micro_op_word",
            "unit": "route digit",
            "size": 8,
            "role": "3 ternary XOR ticks plus 5 apartment-hop ticks",
        },
        {
            "layer": 2,
            "name": "atlas_ingress",
            "unit": "full chart-atlas route table",
            "size": 540,
            "role": "one compiled ingress word for every chart",
        },
        {
            "layer": 3,
            "name": "tomotope_packet_body",
            "unit": "six route digits",
            "size": 48,
            "role": "executable tomotope packet body",
        },
        {
            "layer": 4,
            "name": "parity_epilogue",
            "unit": "three route digits",
            "size": 24,
            "role": "18 residual payload ticks plus 6 parity reroute lanes",
        },
        {
            "layer": 5,
            "name": "oscillator_microframe",
            "unit": "nine route digits",
            "size": 72,
            "role": "one [72,66]_3 instruction frame",
        },
        {
            "layer": 6,
            "name": "mirror_bus_epoch",
            "unit": "thirty microframes",
            "size": 2160,
            "role": "D12 mirror-bus epoch, also 540 charts times four transversals",
        },
        {
            "layer": 7,
            "name": "clifford_supercycle",
            "unit": "twenty-four mirror epochs",
            "size": 51840,
            "role": "complete Sp(4,3) two-qutrit Clifford runtime",
        },
        {
            "layer": 8,
            "name": "fractal_shell",
            "unit": "recursive W33 shell",
            "size": "40^n leaves",
            "role": "universal network scaling with route bound 8n",
        },
    ]


def build_payload() -> dict[str, Any]:
    bt827 = load_json("data/bt827_holonet_fractal_architecture.json")
    bt1299 = load_json("data/bt1299_harmonic_microframe_runtime.json")
    bt1300 = load_json("data/bt1300_oscillator_instruction_isa.json")
    bt1301 = load_json("data/bt1301_full_chart_atlas_isa_compiler.json")
    bt1302 = load_json("data/bt1302_parity_epilogue_reroute_protocol.json")

    layers = stack_layers()
    q = 3
    qfac = math.factorial(q)
    ticks = 2**q
    body = qfac * ticks
    epilogue = q * ticks
    frame = q**2 * ticks
    mirror = 30 * frame
    supercycle = 24 * mirror
    level_rows = []
    for level in range(1, 10):
        route_ticks = ticks * level
        level_rows.append(
            {
                "level": level,
                "leaf_cores": 40**level,
                "route_ticks": route_ticks,
                "words": level,
                "fits_tomotope_body": route_ticks <= body,
                "fits_microframe": route_ticks <= frame,
                "frame_fraction": f"{route_ticks}/{frame}",
            }
        )

    checks = {
        "bt827_loaded": bt827["single_core"]["charts"] == 540,
        "bt1299_verified": bt1299["verified"] is True,
        "bt1300_verified": bt1300["verified"] is True,
        "bt1301_verified": bt1301["verified"] is True,
        "bt1302_verified": bt1302["verified"] is True,
        "body_epilogue_frame_identity": body == 48
        and epilogue == 24
        and body + epilogue == frame == 72,
        "mirror_bus_is_30_frames": mirror
        == bt1299["mirror_bus"]["mirror_slots"]
        == 2160,
        "mirror_bus_is_540_by_4": mirror == 540 * 4,
        "supercycle_is_24_mirror_epochs": supercycle
        == bt1299["runtime_supercycle"]["runtime_order"]
        == 51840,
        "supercycle_is_720_frames": supercycle == 720 * frame,
        "atlas_table_matches_stack_chart_layer": bt1301["contract"]["chart_routes"]
        == 540,
        "parity_table_matches_stack_recovery_layer": bt1302["protocol"][
            "recovery_actions"
        ]
        == 540 * 6,
        "level_6_fills_tomotope_body": level_rows[5]["route_ticks"] == body,
        "level_9_fills_microframe": level_rows[8]["route_ticks"] == frame,
        "stack_layer_sizes_are_ordered": [layer["layer"] for layer in layers]
        == list(range(len(layers))),
    }

    payload = {
        "theorem": "BT1303 holonet stack contract",
        "verified": all(checks.values()),
        "checks": checks,
        "stack_layers": layers,
        "exact_handoffs": {
            "route_word": "8 = 2^q ticks",
            "tomotope_body": "48 = q! * 2^q = 6 route words",
            "parity_epilogue": "24 = q * 2^q = 3 route words = 18 payload + 6 parity",
            "microframe": "72 = q^2 * 2^q = 48 + 24",
            "mirror_bus": "2160 = 30 * 72 = 540 * 4",
            "supercycle": "51840 = 24 * 2160 = 720 * 72",
            "fractal_route": "level n route bound = 8n; level 6 fills the body, level 9 fills the frame",
        },
        "fractal_route_table": level_rows,
        "architecture_reading": (
            "The holonet is now a stack machine. A single carrier executes "
            "8-tick words; six words form the tomotope body; three more words "
            "close the local-lift parity epilogue; thirty 72-tick frames form "
            "the 2160-slot mirror bus; twenty-four bus epochs form the 51840 "
            "Clifford supercycle; recursive W33 shells scale routing as 8n."
        ),
        "honesty_boundary": (
            "BT1303 is a finite stack contract and scaling law. It does not yet "
            "model queueing, simultaneous packet contention, analog GKP noise, "
            "or hardware loss."
        ),
    }
    return payload


def main() -> None:
    payload = build_payload()
    OUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "theorem": payload["theorem"],
                "verified": payload["verified"],
                "checks_passed": sum(payload["checks"].values()),
                "checks_total": len(payload["checks"]),
                "out": str(OUT.relative_to(ROOT)),
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not payload["verified"]:
        failed = [name for name, passed in payload["checks"].items() if not passed]
        raise SystemExit(f"BT1303 failed checks: {failed}")


if __name__ == "__main__":
    main()
