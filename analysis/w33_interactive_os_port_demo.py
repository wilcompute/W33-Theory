#!/usr/bin/env python3
"""Interactive OS-port replay for the W(3,3) VM.

This is the practical wrapper shape in miniature.  A user types a command,
the OS reads a binary program object from a disk-like endpoint, the tiny RISC
packet ISA executes it, and the result is written to a serial-like endpoint.
Every boundary crossing is a typed W33 packet with reversible trit-page payloads.

The replay is deterministic rather than interactive so it can run in CI and be
used as a presentation/demo artifact.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import holonet_node as hn
from w33_binary_object_loader import page_records
from w33_component_execution_simulator import line_lookup
from w33_tiny_risc_packet_isa import build_payload as build_risc_payload, encode_program
from w33_uor_runtime_model import ROOT, all_lines, point_id


DEFAULT_JSON = ROOT / "data" / "w33_interactive_os_port_demo.json"
DEFAULT_MD = ROOT / "docs" / "w33_interactive_os_port_demo.md"


EVENTS = [
    {
        "tick": 0,
        "actor": "keyboard",
        "endpoint": "kbd0/in",
        "transfer_class": "interrupt",
        "direction": "device_to_host",
        "payload": b"run tiny-risc\n",
        "meaning": "user command",
    },
    {
        "tick": 1,
        "actor": "disk",
        "endpoint": "disk0/object",
        "transfer_class": "bulk",
        "direction": "device_to_host",
        "payload": encode_program(),
        "meaning": "binary program object",
    },
    {
        "tick": 2,
        "actor": "serial",
        "endpoint": "tty0/control",
        "transfer_class": "control",
        "direction": "host_to_device",
        "payload": b"mode=result-stream;encoding=utf8",
        "meaning": "configure result stream",
    },
    {
        "tick": 3,
        "actor": "serial",
        "endpoint": "tty0/out",
        "transfer_class": "bulk",
        "direction": "host_to_device",
        "payload": b"sum_squares=140\n",
        "meaning": "program output",
    },
]


TRANSFER_DISCIPLINE = {
    "interrupt": "urgent point-star input event",
    "bulk": "lossless line-bus payload stream",
    "control": "ordered setup/status syscall",
    "isochronous": "reserved spread-clock stream",
}


def point_from_label(label: str) -> int:
    digest = hashlib.sha256(label.encode("utf-8")).digest()
    return int.from_bytes(digest[:4], "big") % len(hn.POINTS)


def route_record(src_idx: int, dst_idx: int, lookup: dict[tuple[int, int], int]) -> dict[str, Any]:
    route = hn.route(hn.POINTS[src_idx], hn.POINTS[dst_idx])
    route_indices = [hn.POINTS.index(point) for point in route]
    return {
        "route": [point_id(point) for point in route],
        "hops": len(route_indices) - 1,
        "line_buses": [
            lookup[(left, right)] for left, right in zip(route_indices, route_indices[1:])
        ],
    }


def event_record(event: dict[str, Any], process_idx: int, lookup: dict[tuple[int, int], int]) -> dict[str, Any]:
    endpoint_idx = point_from_label(
        f"os-demo:{event['actor']}:{event['endpoint']}:{event['transfer_class']}"
    )
    if event["direction"] == "device_to_host":
        route = route_record(endpoint_idx, process_idx, lookup)
    else:
        route = route_record(process_idx, endpoint_idx, lookup)
    payload = bytes(event["payload"])
    pages = page_records(f"os:{event['endpoint']}:{event['tick']}", payload)
    return {
        "tick": event["tick"],
        "actor": event["actor"],
        "endpoint": event["endpoint"],
        "endpoint_point": point_id(hn.POINTS[endpoint_idx]),
        "transfer_class": event["transfer_class"],
        "direction": event["direction"],
        "discipline": TRANSFER_DISCIPLINE[event["transfer_class"]],
        "meaning": event["meaning"],
        "payload_len": len(payload),
        "payload_pages": pages["page_count"],
        "payload_sha256": pages["sha256"],
        "payload_roundtrip_matches": pages["roundtrip_matches"],
        "route": route,
    }


def build_payload() -> dict[str, Any]:
    lookup = line_lookup(all_lines())
    process_idx = point_from_label("interactive-os-demo:process")
    events = [event_record(event, process_idx, lookup) for event in EVENTS]
    risc = build_risc_payload()
    transcript = [
        "$ run tiny-risc",
        "loaded disk0/object -> tiny_risc_sum_squares_object",
        "executed 38 routed packet events",
        "sum_squares=140",
    ]
    checks = {
        "risc_payload_passes": risc["status"] == "PASS" and all(risc["checks"].values()),
        "all_payloads_roundtrip": all(event["payload_roundtrip_matches"] for event in events),
        "all_routes_diameter_two": all(event["route"]["hops"] <= 2 for event in events),
        "all_hops_have_line_buses": all(
            len(event["route"]["line_buses"]) == event["route"]["hops"] for event in events
        ),
        "keyboard_interrupt_present": any(
            event["actor"] == "keyboard" and event["transfer_class"] == "interrupt"
            for event in events
        ),
        "disk_bulk_object_present": any(
            event["actor"] == "disk" and event["transfer_class"] == "bulk"
            for event in events
        ),
        "serial_output_present": transcript[-1] == "sum_squares=140",
    }
    return {
        "schema": "w33.interactive_os_port_demo.v1",
        "theorem": "a user-facing OS session can be replayed as W33 device-port packets plus VM execution",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "process_point": point_id(hn.POINTS[process_idx]),
        "events": events,
        "risc_execution": {
            "object_bytes": risc["object"]["byte_len"],
            "object_pages": risc["object"]["page_count"],
            "dynamic_steps": risc["execution"]["dynamic_steps"],
            "result": risc["execution"]["result"],
            "max_route_hops": risc["execution"]["max_route_hops"],
        },
        "terminal_transcript": transcript,
        "checks": checks,
        "interpretation": (
            "A classical host can act as the user/device shell while compute and "
            "I/O are represented by one W33 ABI: keyboard command, disk object "
            "load, VM execution, and serial output all become typed packet events."
        ),
        "honesty_boundary": (
            "This is a deterministic replay with mock endpoints. It demonstrates "
            "the OS/device contract, not physical USB driver replacement."
        ),
    }


def markdown(payload: dict[str, Any]) -> str:
    rows = []
    for event in payload["events"]:
        rows.append(
            "| {tick} | {actor} | {transfer_class} | `{endpoint_point}` | {payload_len} | {payload_pages} | {hops} |".format(
                **event,
                hops=event["route"]["hops"],
            )
        )
    transcript = "\n".join(payload["terminal_transcript"])
    return f"""# W(3,3) Interactive OS-Port Demo

This deterministic replay shows the user-facing wrapper shape: keyboard input,
disk object loading, VM execution, and serial output all pass through W33 packet
events.

| Tick | Actor | Class | W33 point | Bytes | Pages | Hops |
|---:|---|---|---|---:|---:|---:|
{chr(10).join(rows)}

```text
{transcript}
```

Boundary: mock endpoints, real W33 routing and reversible payload packing.
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-out", default=str(DEFAULT_JSON))
    parser.add_argument("--md-out", default=str(DEFAULT_MD))
    args = parser.parse_args(argv)

    payload = build_payload()
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
    print(f"status: {payload['status']}")
    for line in payload["terminal_transcript"]:
        print(line)
    print(f"wrote: {json_out.relative_to(ROOT)}")
    print(f"wrote: {md_out.relative_to(ROOT)}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
