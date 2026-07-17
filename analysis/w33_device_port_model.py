#!/usr/bin/env python3
"""Device-port model for the W(3,3) VM boundary.

A useful VM needs an OS boundary: keyboard events, disk blocks, serial control,
and real-time streams.  This witness treats those device interactions as typed
packets on the same W33 fabric used by program operations.

The model is deliberately small and falsifiable:

* endpoint identity is hashed to a W33 point address;
* transfer type chooses a boundary discipline;
* payload bytes are packed by the reversible trit-page loader;
* every host-to-device transfer records its W33 route and line buses.

No physical USB controller is claimed here.  The claim is architectural: device
I/O can be represented as the same point/line/spread packet grammar as compute.
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
from w33_uor_runtime_model import ROOT, all_lines, point_id


DEFAULT_JSON = ROOT / "data" / "w33_device_port_model.json"
DEFAULT_MD = ROOT / "docs" / "w33_device_port_model.md"


TRANSFER_CLASSES = {
    "control": {
        "discipline": "point-star syscall/control plane",
        "latency": "ordered",
        "delivery": "exact setup/status state",
    },
    "bulk": {
        "discipline": "line-bus payload stream",
        "latency": "elastic",
        "delivery": "lossless page transfer",
    },
    "interrupt": {
        "discipline": "urgent point-star event",
        "latency": "bounded",
        "delivery": "small event packet",
    },
    "isochronous": {
        "discipline": "reserved spread-clock stream",
        "latency": "clocked",
        "delivery": "timing before retry",
    },
}


DEVICES = [
    {
        "device": "keyboard",
        "endpoint": "kbd0/in",
        "transfer_class": "interrupt",
        "direction": "device_to_host",
        "payload": b"HELLO",
    },
    {
        "device": "disk",
        "endpoint": "disk0/block",
        "transfer_class": "bulk",
        "direction": "host_to_device",
        "payload": b"block-0001:holonet-object-page",
    },
    {
        "device": "serial",
        "endpoint": "tty0/control",
        "transfer_class": "control",
        "direction": "host_to_device",
        "payload": b"baud=115200;mode=8N1",
    },
    {
        "device": "phase-camera",
        "endpoint": "cam0/frame",
        "transfer_class": "isochronous",
        "direction": "device_to_host",
        "payload": b"frame:phase-bin:00000000",
    },
]


def point_from_label(label: str) -> int:
    digest = hashlib.sha256(label.encode("utf-8")).digest()
    return int.from_bytes(digest[:4], "big") % len(hn.POINTS)


def route_record(src_idx: int, dst_idx: int, lookup: dict[tuple[int, int], int]) -> dict[str, Any]:
    route = hn.route(hn.POINTS[src_idx], hn.POINTS[dst_idx])
    route_indices = [hn.POINTS.index(point) for point in route]
    line_buses = [
        lookup[(left, right)] for left, right in zip(route_indices, route_indices[1:])
    ]
    return {
        "route": [point_id(point) for point in route],
        "hops": len(route_indices) - 1,
        "line_buses": line_buses,
    }


def endpoint_record(device: dict[str, Any], process_idx: int, lookup: dict[tuple[int, int], int]) -> dict[str, Any]:
    endpoint_idx = point_from_label(
        f"{device['device']}:{device['endpoint']}:{device['transfer_class']}"
    )
    payload = bytes(device["payload"])
    loader = page_records(f"device:{device['endpoint']}", payload)
    route = route_record(process_idx, endpoint_idx, lookup)
    point_star = [point_id(point) for point in hn.neighbors(hn.POINTS[endpoint_idx])]
    transfer_class = TRANSFER_CLASSES[device["transfer_class"]]
    return {
        "device": device["device"],
        "endpoint": device["endpoint"],
        "transfer_class": device["transfer_class"],
        "direction": device["direction"],
        "endpoint_point_index": endpoint_idx,
        "endpoint_point": point_id(hn.POINTS[endpoint_idx]),
        "process_point_index": process_idx,
        "process_point": point_id(hn.POINTS[process_idx]),
        "payload_len": len(payload),
        "payload_sha256": hashlib.sha256(payload).hexdigest(),
        "payload_pages": loader["page_count"],
        "payload_roundtrip_matches": loader["roundtrip_matches"],
        "boundary_discipline": transfer_class["discipline"],
        "latency_model": transfer_class["latency"],
        "delivery_model": transfer_class["delivery"],
        "route": route,
        "endpoint_point_star_size": len(point_star),
        "endpoint_point_star_preview": point_star[:6],
    }


def build_payload() -> dict[str, Any]:
    lines = all_lines()
    lookup = line_lookup(lines)
    process_idx = point_from_label("holonet-user-process:pid0")
    endpoints = [endpoint_record(device, process_idx, lookup) for device in DEVICES]
    class_hist: dict[str, int] = {}
    for endpoint in endpoints:
        class_hist[endpoint["transfer_class"]] = class_hist.get(endpoint["transfer_class"], 0) + 1
    checks = {
        "all_transfer_classes_present": set(class_hist) == set(TRANSFER_CLASSES),
        "all_payloads_roundtrip": all(endpoint["payload_roundtrip_matches"] for endpoint in endpoints),
        "all_endpoint_points_valid": all(
            0 <= endpoint["endpoint_point_index"] < 40 for endpoint in endpoints
        ),
        "all_routes_diameter_two": all(endpoint["route"]["hops"] <= 2 for endpoint in endpoints),
        "all_routed_hops_have_line_buses": all(
            len(endpoint["route"]["line_buses"]) == endpoint["route"]["hops"]
            for endpoint in endpoints
        ),
        "all_point_stars_have_degree_k": all(
            endpoint["endpoint_point_star_size"] == 12 for endpoint in endpoints
        ),
    }
    return {
        "schema": "w33.device_port_model.v1",
        "theorem": "classical device ports can be represented as typed W33 boundary packets",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "process_point": point_id(hn.POINTS[process_idx]),
        "transfer_classes": TRANSFER_CLASSES,
        "endpoints": endpoints,
        "class_histogram": dict(sorted(class_hist.items())),
        "checks": checks,
        "interpretation": (
            "USB-like control, bulk, interrupt, and isochronous transfers become "
            "ordinary W33 routed packets with different scheduling disciplines. "
            "The OS boundary is therefore not separate from the Holonet fabric; "
            "it is the same packet grammar with endpoint-specific promises."
        ),
        "honesty_boundary": (
            "The devices are mock endpoints and the payloads are local byte "
            "strings. This proves an ABI model for ports, not a hardware driver."
        ),
    }


def markdown(payload: dict[str, Any]) -> str:
    rows = []
    for endpoint in payload["endpoints"]:
        rows.append(
            "| {device} | {endpoint} | {transfer_class} | `{endpoint_point}` | "
            "{payload_len} | {payload_pages} | {hops} |".format(
                **endpoint,
                hops=endpoint["route"]["hops"],
            )
        )
    return f"""# W(3,3) Device-Port Model

Device I/O is represented as boundary packets on the same fabric as compute.
Endpoint identity selects a W33 point; transfer type selects a scheduling
discipline; payload bytes are packed through the reversible trit-page loader.

| Device | Endpoint | Class | W33 point | Bytes | Pages | Hops |
|---|---|---|---|---:|---:|---:|
{chr(10).join(rows)}

The four transfer classes are `control`, `bulk`, `interrupt`, and
`isochronous`, mirroring the USB vocabulary while staying inside the Holonet
packet ABI.
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
    for endpoint in payload["endpoints"]:
        print(
            f"{endpoint['device']}/{endpoint['endpoint']}: "
            f"class={endpoint['transfer_class']}, point={endpoint['endpoint_point']}, "
            f"hops={endpoint['route']['hops']}, pages={endpoint['payload_pages']}"
        )
    print(f"wrote: {json_out.relative_to(ROOT)}")
    print(f"wrote: {md_out.relative_to(ROOT)}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
