#!/usr/bin/env python3
"""Fuse Q6-style routing, tomotope packet body, and 2160 mirror bus into one recursive ABI.

The repo already has the ingredients:

* BT1697: typed packet fields, including Q6 body edge, 48 tomotope blocks,
  192 tomotope flags, and 2160 mirror slots.
* BT1698: the packet executes as 16 Q6/tomotope edges times 3 phases = 48 body
  ticks, plus a 24-tick Hesse/guard epilogue.
* BT1700: the packet recurses as 40^n leaf packets.
* w33_recursive_instance_compression: internal W33 infrastructure scales as
  I_n=(40^n-1)/39 instances.

This witness keeps those two scale counters separate and shows the shared ABI
factorization connecting them.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from bt1700_recursive_holonet_packet_compiler import build_certificate as build_bt1700


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "data" / "w33_q6_tomotope_recursive_packet_abi.json"
DEFAULT_MD = ROOT / "docs" / "w33_q6_tomotope_recursive_packet_abi.md"


def load_json(relpath: str) -> dict[str, Any]:
    with (ROOT / relpath).open(encoding="utf-8") as handle:
        return json.load(handle)


def field_size(bt1697: dict[str, Any], field: str) -> int:
    for row in bt1697["field_schema"]:
        if row["field"] == field:
            return int(row["size"])
    raise KeyError(field)


def build_payload(max_depth: int = 6) -> dict[str, Any]:
    bt1697 = load_json("data/bt1697_holonet_typed_packet_abi.json")
    bt1698 = load_json("data/bt1698_holonet_packet_state_machine.json")
    bt1700 = build_bt1700(max_depth=max_depth)
    recursive = load_json("data/w33_recursive_instance_compression.json")

    local = {
        "chart_word_states": field_size(bt1697, "chart_word"),
        "q6_body_edges": field_size(bt1697, "q6_body_edge"),
        "body_pulse_phases": field_size(bt1697, "body_pulse_phase"),
        "tomotope_packet_blocks": 48,
        "tomotope_flag_rows": field_size(bt1697, "tomotope_flag"),
        "guard_ticks": 24,
        "microframe_ticks": 72,
        "mirror_slots": field_size(bt1697, "mirror_slot"),
        "clifford_supercycle": field_size(bt1697, "clifford_supercycle"),
    }
    local["q6_body_ticks"] = local["q6_body_edges"] * local["body_pulse_phases"]
    local["tomotope_body_identity"] = (
        f"{local['q6_body_edges']}*{local['body_pulse_phases']} = "
        f"{local['q6_body_ticks']} = tomotope packet body"
    )
    local["mirror_factorizations"] = {
        "polar_sheet_times_tomotope_body": "45*48",
        "chart_times_four_slots": "540*4",
        "e8_coxeter_times_microframe": "30*72",
        "value": local["mirror_slots"],
    }

    infrastructure_rows = {
        row["level"]: row for row in recursive["recursive_rows"]
    }
    packet_rows = []
    for layer in bt1700["layers"]:
        depth = layer["depth"]
        if depth == 0:
            continue
        infra = infrastructure_rows.get(depth)
        packet_rows.append(
            {
                "depth": depth,
                "leaf_packets": layer["packet_count"],
                "w33_instances": infra["w33_instances"] if infra else None,
                "q6_chart_route_states": layer["chart_route_states"],
                "q6_route_bound": layer["route_bound_8n"],
                "tomotope_body_ticks": layer["body_ticks"],
                "guard_ticks": layer["guard_ticks"],
                "packet_microframe_ticks": layer["total_ticks"],
                "packet_scheduler_slots": layer["phase_scheduler_slots"],
                "packet_clifford_supercycle_slots": layer[
                    "clifford_supercycle_slots"
                ],
                "internal_mirror_capacity": infra["mirror_capacity"] if infra else None,
                "internal_mirror_one_chart_demand": infra[
                    "mirror_one_packet_per_chart_demand"
                ]
                if infra
                else None,
                "internal_mirror_utilization": infra["mirror_utilization"] if infra else None,
                "internal_route_table_bytes_avoided": infra[
                    "routing_table_bytes_avoided"
                ]
                if infra
                else None,
            }
        )

    checks = {
        "bt1697_verified": bt1697["verified"] is True,
        "bt1698_verified": bt1698["verified"] is True,
        "bt1700_verified": bt1700["verified"] is True,
        "recursive_instance_compression_passes": recursive["status"] == "PASS",
        "q6_body_is_16_edges_times_3_phases": local["q6_body_edges"] == 16
        and local["body_pulse_phases"] == 3
        and local["q6_body_ticks"] == 48,
        "microframe_is_48_plus_24": local["q6_body_ticks"] + local["guard_ticks"]
        == local["microframe_ticks"]
        == 72,
        "tomotope_flags_are_four_residues_per_body_block": local[
            "tomotope_flag_rows"
        ]
        == 4 * local["tomotope_packet_blocks"]
        == 192,
        "mirror_slots_have_all_three_factorizations": local["mirror_slots"]
        == 45 * 48
        == 540 * 4
        == 30 * 72
        == 2160,
        "clifford_supercycle_is_24_mirror_atlases": local["clifford_supercycle"]
        == 24 * local["mirror_slots"]
        == 51840,
        "packet_rows_preserve_2160_scheduler": all(
            row["packet_scheduler_slots"] == 2160 * row["leaf_packets"]
            for row in packet_rows
        ),
        "packet_rows_preserve_48_24_split": all(
            row["tomotope_body_ticks"] == 48 * row["leaf_packets"]
            and row["guard_ticks"] == 24 * row["leaf_packets"]
            for row in packet_rows
        ),
        "infrastructure_rows_keep_quarter_mirror_use": all(
            row["internal_mirror_utilization"] == "1/4" for row in packet_rows
        ),
        "depth6_fusion_row_matches_instance_compression": packet_rows[-1][
            "w33_instances"
        ]
        == 105_025_641
        and packet_rows[-1]["q6_route_bound"] == 48,
    }

    return {
        "schema": "w33.q6_tomotope_recursive_packet_abi.v1",
        "theorem": "Q6/tomotope recursive Holonet packet ABI fusion",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "local_abi": local,
        "scale_counters": {
            "leaf_packet_counter": "N(n)=40^n from BT1700",
            "internal_instance_counter": "I_n=(40^n-1)/39 from recursive instance compression",
            "boundary": (
                "N(n) counts leaf packet substitutions; I_n counts internal W33 "
                "infrastructure instances. Both reuse the same local factors "
                "48, 72, 2160, and 51840."
            ),
        },
        "recursive_rows": packet_rows,
        "checks": checks,
        "interpretation": (
            "Q6-style local motion supplies the 16-edge body walk; the three "
            "LOAD/FLIP/LATCH phases turn that walk into the 48-tick tomotope "
            "body; 45 polar sheets or 540 chart-four slots lift the body to the "
            "2160-slot mirror bus; 24 lifts give the 51840 Clifford/W(E6) "
            "supercycle. Recursion substitutes this same packet at 40^n leaves "
            "while the internal fabric grows as I_n W33 instances."
        ),
        "honesty_boundary": (
            "This is a typed finite ABI and scale-counter fusion. It does not "
            "assert that the Q6 graph, tomotope, and W33 instance counter are "
            "literally the same object; it proves the checked interface factors "
            "through the existing certificates."
        ),
    }


def markdown(payload: dict[str, Any]) -> str:
    local = payload["local_abi"]
    rows = []
    for row in payload["recursive_rows"]:
        rows.append(
            "| {depth} | {leaf_packets:,} | {w33_instances:,} | {q6_route_bound} | "
            "{tomotope_body_ticks:,} | {packet_scheduler_slots:,} | "
            "{internal_mirror_capacity:,} | {internal_mirror_utilization} |".format(
                **row
            )
        )
    return f"""# Q6 / Tomotope / 2160 Recursive Packet ABI

This witness fuses the local packet ABI with the recursive Holonet scaling law.

## Local Packet

- Q6-style body edges: `{local['q6_body_edges']}`
- Body phases per edge: `{local['body_pulse_phases']}`
- Tomotope body ticks: `{local['q6_body_ticks']}`
- Guard / Hesse epilogue ticks: `{local['guard_ticks']}`
- Microframe: `{local['microframe_ticks']}`
- Tomotope flags: `{local['tomotope_flag_rows']} = 48 x 4`
- Mirror bus: `{local['mirror_slots']} = 45 x 48 = 540 x 4 = 30 x 72`
- Clifford supercycle: `{local['clifford_supercycle']} = 24 x 2160`

## Recursive Fusion

| Depth | Leaf packets | W33 instances | Route bound | Tomotope body ticks | Packet scheduler slots | Internal mirror capacity | Internal mirror use |
|---:|---:|---:|---:|---:|---:|---:|---:|
{chr(10).join(rows)}

The key distinction is that `40^n` counts leaf packet substitutions, while
`I_n=(40^n-1)/39` counts internal W33 infrastructure instances.  The same local
ABI factors, however, appear on both sides: `48`, `72`, `2160`, and `51840`.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-depth", type=int, default=6)
    parser.add_argument("--json-out", default=str(DEFAULT_JSON))
    parser.add_argument("--md-out", default=str(DEFAULT_MD))
    args = parser.parse_args(argv)

    payload = build_payload(args.max_depth)
    json_out = Path(args.json_out)
    if not json_out.is_absolute():
        json_out = ROOT / json_out
    md_out = Path(args.md_out)
    if not md_out.is_absolute():
        md_out = ROOT / md_out
    json_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    md_out.write_text(markdown(payload), encoding="utf-8")

    last = payload["recursive_rows"][-1]
    print(f"status: {payload['status']}")
    print(
        "depth {depth}: leaf_packets={leaf_packets:,}, W33 instances={w33_instances:,}, "
        "route_bound={q6_route_bound}, scheduler={packet_scheduler_slots:,}".format(
            **last
        )
    )
    print(
        "local ABI: "
        f"{payload['local_abi']['q6_body_edges']}*{payload['local_abi']['body_pulse_phases']}="
        f"{payload['local_abi']['q6_body_ticks']}, mirror={payload['local_abi']['mirror_slots']}"
    )
    print(f"wrote: {json_out.relative_to(ROOT)}")
    print(f"wrote: {md_out.relative_to(ROOT)}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
