#!/usr/bin/env python3
"""End-to-end W(3,3) program-object pipeline.

This integrates the three VM/OS witnesses:

1. arbitrary bytes enter as reversible trit pages;
2. executable bytecode samples run through the packet VM;
3. mock device ports cross the same W33 packet boundary;
4. output bytes are packed back into trit pages for exact reconstruction.

The result is a concrete architecture sketch for a wrapper around ordinary
programs: object bytes, execution events, device I/O, and returned bytes all
share one W33 addressing/routing discipline.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from w33_binary_object_loader import page_records
from w33_device_port_model import build_payload as build_device_payload
from w33_packet_vm import build_payload as build_vm_payload
from w33_uor_runtime_model import ROOT


DEFAULT_JSON = ROOT / "data" / "w33_universal_program_object_pipeline.json"
DEFAULT_MD = ROOT / "docs" / "w33_universal_program_object_pipeline.md"


PROGRAM_SOURCE = b"""def wrapped_program():\n    return sum(i*i for i in range(8))\n"""


def output_bytes_from_vm(vm_payload: dict[str, Any]) -> bytes:
    lines = []
    for sample in vm_payload["samples"]:
        lines.append(f"{sample['sample']}={sample['packet_vm_result']}")
    return ("\n".join(lines) + "\n").encode("utf-8")


def build_payload() -> dict[str, Any]:
    input_object = page_records("wrapped_program_source", PROGRAM_SOURCE)
    vm = build_vm_payload()
    devices = build_device_payload()
    output_object = page_records("wrapped_program_output", output_bytes_from_vm(vm))

    checks = {
        "input_bytes_roundtrip": input_object["roundtrip_matches"],
        "output_bytes_roundtrip": output_object["roundtrip_matches"],
        "packet_vm_passes": vm["status"] == "PASS" and all(vm["checks"].values()),
        "device_ports_pass": devices["status"] == "PASS" and all(devices["checks"].values()),
        "program_object_has_w33_pages": input_object["page_count"] >= 1,
        "output_object_has_w33_pages": output_object["page_count"] >= 1,
        "vm_results_exported_as_bytes": output_object["byte_len"] > 0,
        "all_layers_share_diameter_two_routing": (
            max(sample["max_route_hops"] for sample in vm["samples"]) <= 2
            and all(endpoint["route"]["hops"] <= 2 for endpoint in devices["endpoints"])
            and all(transfer["hops"] <= 2 for transfer in input_object["transfers"])
            and all(transfer["hops"] <= 2 for transfer in output_object["transfers"])
        ),
    }

    return {
        "schema": "w33.universal_program_object_pipeline.v1",
        "theorem": "program bytes, VM packet execution, device ports, and output bytes share one W33 ABI",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "pipeline": [
            "program bytes",
            "six-trit byte encoding",
            "81-trit W33-addressed pages",
            "packet VM execution events",
            "typed W33 device-port boundary",
            "output bytes",
        ],
        "input_object": {
            "name": input_object["name"],
            "byte_len": input_object["byte_len"],
            "trit_len": input_object["trit_len"],
            "page_count": input_object["page_count"],
            "sha256": input_object["sha256"],
            "roundtrip_matches": input_object["roundtrip_matches"],
            "page_points": [page["point_label"] for page in input_object["pages"]],
        },
        "vm_summary": {
            "status": vm["status"],
            "samples": [
                {
                    "sample": sample["sample"],
                    "packet_vm_result": sample["packet_vm_result"],
                    "static_packet_ops": sample["static_packet_ops"],
                    "executed_packet_steps": sample["executed_packet_steps"],
                    "max_route_hops": sample["max_route_hops"],
                }
                for sample in vm["samples"]
            ],
        },
        "device_summary": {
            "status": devices["status"],
            "class_histogram": devices["class_histogram"],
            "endpoints": [
                {
                    "device": endpoint["device"],
                    "endpoint": endpoint["endpoint"],
                    "transfer_class": endpoint["transfer_class"],
                    "endpoint_point": endpoint["endpoint_point"],
                    "hops": endpoint["route"]["hops"],
                    "payload_pages": endpoint["payload_pages"],
                }
                for endpoint in devices["endpoints"]
            ],
        },
        "output_object": {
            "name": output_object["name"],
            "byte_len": output_object["byte_len"],
            "trit_len": output_object["trit_len"],
            "page_count": output_object["page_count"],
            "sha256": output_object["sha256"],
            "roundtrip_matches": output_object["roundtrip_matches"],
            "page_points": [page["point_label"] for page in output_object["pages"]],
        },
        "checks": checks,
        "interpretation": (
            "This is the concrete wrapper shape: an ordinary program can be "
            "loaded as exact trit pages, its supported operations can execute "
            "as routed packet events, its ports can be treated as typed W33 "
            "boundary packets, and its output can be returned as exact bytes."
        ),
        "honesty_boundary": (
            "The executable VM currently covers the sampled Python opcode subset. "
            "The binary loader is arbitrary-byte reversible, but arbitrary native "
            "machine-code execution still requires a larger ISA lifter."
        ),
    }


def markdown(payload: dict[str, Any]) -> str:
    vm_rows = []
    for sample in payload["vm_summary"]["samples"]:
        vm_rows.append(
            "| {sample} | `{packet_vm_result}` | {static_packet_ops} | {executed_packet_steps} | {max_route_hops} |".format(
                **sample
            )
        )
    device_rows = []
    for endpoint in payload["device_summary"]["endpoints"]:
        device_rows.append(
            "| {device} | {endpoint} | {transfer_class} | `{endpoint_point}` | {hops} | {payload_pages} |".format(
                **endpoint
            )
        )
    return f"""# Universal Program Object Pipeline

The wrapper model is now end-to-end: program bytes load into W33-addressed trit
pages, supported bytecode executes as routed packet events, device ports enter
through typed W33 boundary packets, and output returns as exact bytes.

Input object: `{payload['input_object']['byte_len']}` bytes,
`{payload['input_object']['page_count']}` W33 pages. Output object:
`{payload['output_object']['byte_len']}` bytes,
`{payload['output_object']['page_count']}` W33 pages.

## Packet VM

| Sample | Result | Static packet ops | Executed packet steps | Max hops |
|---|---:|---:|---:|---:|
{chr(10).join(vm_rows)}

## Device Ports

| Device | Endpoint | Class | W33 point | Hops | Payload pages |
|---|---|---|---|---:|---:|
{chr(10).join(device_rows)}

Boundary: this is an executable architecture witness for the current opcode
subset and a reversible loader for arbitrary bytes. A larger ISA lifter is the
next step toward wrapping arbitrary host programs.
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
    print(
        "input: bytes={byte_len}, pages={page_count}, roundtrip={roundtrip_matches}".format(
            **payload["input_object"]
        )
    )
    print(
        "output: bytes={byte_len}, pages={page_count}, roundtrip={roundtrip_matches}".format(
            **payload["output_object"]
        )
    )
    for sample in payload["vm_summary"]["samples"]:
        print(
            f"vm {sample['sample']}: result={sample['packet_vm_result']!r}, "
            f"executed={sample['executed_packet_steps']}"
        )
    print(f"wrote: {json_out.relative_to(ROOT)}")
    print(f"wrote: {md_out.relative_to(ROOT)}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
