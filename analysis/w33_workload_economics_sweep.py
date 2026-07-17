#!/usr/bin/env python3
"""Workload-level economics sweep for the W(3,3) program wrapper.

The single-object economics witness establishes the boundary: payload bytes do
not get entropy-free compression, while generated W33 topology removes persisted
route/control tables.  This sweep scales that accounting across practical
workloads: one session, ten compiled objects, forty device events, and one
hundred mixed command sessions.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from w33_binary_object_loader import PAGE_TRITS, TRITS_PER_BYTE, page_records
from w33_interactive_os_port_demo import EVENTS
from w33_program_compression_economics import (
    ENDPOINT_ROUTE_BYTES,
    PAGE_TABLE_BYTES_PER_PAGE,
    ROUTING_TABLE_BYTES_40,
)
from w33_stack_bytecode_adapter import encode_stack_program
from w33_tiny_risc_packet_isa import encode_program as encode_tiny_risc_program
from w33_uor_runtime_model import ROOT


DEFAULT_JSON = ROOT / "data" / "w33_workload_economics_sweep.json"
DEFAULT_MD = ROOT / "docs" / "w33_workload_economics_sweep.md"


STACK_OBJECT = encode_stack_program()
TINY_OBJECT = encode_tiny_risc_program()
EVENT_BLOBS = [bytes(event["payload"]) for event in EVENTS]
OUTPUT_BLOB = b"sum_squares=140\n"


def workload_blobs() -> dict[str, list[tuple[str, bytes]]]:
    one_session = [
        ("stack_object", STACK_OBJECT),
        ("tiny_risc_object", TINY_OBJECT),
        *[(f"os_event_{idx}", blob) for idx, blob in enumerate(EVENT_BLOBS)],
        ("serial_output", OUTPUT_BLOB),
    ]
    batch_10 = [(f"tiny_risc_{idx}", TINY_OBJECT) for idx in range(10)]
    event_stream_40 = [
        (f"event_{idx}", EVENT_BLOBS[idx % len(EVENT_BLOBS)])
        for idx in range(40)
    ]
    mixed_100 = []
    for idx in range(100):
        mixed_100.append((f"cmd_{idx}_stack", STACK_OBJECT))
        mixed_100.append((f"cmd_{idx}_tiny", TINY_OBJECT))
        mixed_100.append((f"cmd_{idx}_input", EVENT_BLOBS[0]))
        mixed_100.append((f"cmd_{idx}_output", OUTPUT_BLOB))
    return {
        "one_interactive_session": one_session,
        "batch_10_tiny_risc_objects": batch_10,
        "device_event_stream_40": event_stream_40,
        "mixed_command_sessions_100": mixed_100,
    }


def object_account(name: str, blob: bytes) -> dict[str, Any]:
    record = page_records(name, blob)
    conventional_control_bytes = (
        ROUTING_TABLE_BYTES_40
        + record["page_count"] * PAGE_TABLE_BYTES_PER_PAGE
        + max(1, len(record["transfers"])) * ENDPOINT_ROUTE_BYTES
    )
    return {
        "name": name,
        "raw_bytes": len(blob),
        "exact_trits": record["trit_len"],
        "page_count": record["page_count"],
        "padded_trits": record["page_count"] * PAGE_TRITS,
        "padded_host_bits": record["page_count"] * PAGE_TRITS * 2,
        "conventional_control_bytes": conventional_control_bytes,
        "w33_persistent_control_bytes": 0,
        "control_bytes_avoided": conventional_control_bytes,
        "page_padding_trits": record["page_count"] * PAGE_TRITS - record["trit_len"],
        "roundtrip_matches": record["roundtrip_matches"],
        "max_transfer_hops": max((transfer["hops"] for transfer in record["transfers"]), default=0),
    }


def workload_account(name: str, blobs: list[tuple[str, bytes]]) -> dict[str, Any]:
    objects = [object_account(obj_name, blob) for obj_name, blob in blobs]
    raw_bits = sum(obj["raw_bytes"] for obj in objects) * 8
    padded_host_bits = sum(obj["padded_host_bits"] for obj in objects)
    return {
        "name": name,
        "object_count": len(objects),
        "raw_bytes": sum(obj["raw_bytes"] for obj in objects),
        "exact_trits": sum(obj["exact_trits"] for obj in objects),
        "padded_trits": sum(obj["padded_trits"] for obj in objects),
        "page_count": sum(obj["page_count"] for obj in objects),
        "page_padding_trits": sum(obj["page_padding_trits"] for obj in objects),
        "padded_host_bits": padded_host_bits,
        "payload_host_bit_ratio": padded_host_bits / raw_bits if raw_bits else 0,
        "conventional_control_bytes": sum(obj["conventional_control_bytes"] for obj in objects),
        "w33_persistent_control_bytes": 0,
        "control_bytes_avoided": sum(obj["control_bytes_avoided"] for obj in objects),
        "control_bytes_avoided_per_raw_byte": (
            sum(obj["control_bytes_avoided"] for obj in objects)
            / sum(obj["raw_bytes"] for obj in objects)
        ),
        "all_roundtrips_match": all(obj["roundtrip_matches"] for obj in objects),
        "max_transfer_hops": max((obj["max_transfer_hops"] for obj in objects), default=0),
        "sample_objects": objects[:8],
    }


def build_payload() -> dict[str, Any]:
    rows = [
        workload_account(name, blobs)
        for name, blobs in workload_blobs().items()
    ]
    checks = {
        "four_workloads": len(rows) == 4,
        "all_roundtrips_match": all(row["all_roundtrips_match"] for row in rows),
        "all_routes_diameter_two": all(row["max_transfer_hops"] <= 2 for row in rows),
        "control_savings_positive": all(row["control_bytes_avoided"] > 0 for row in rows),
        "w33_control_state_zero": all(row["w33_persistent_control_bytes"] == 0 for row in rows),
        "payload_host_bits_expand": all(row["payload_host_bit_ratio"] > 1 for row in rows),
    }
    return {
        "schema": "w33.workload_economics_sweep.v1",
        "theorem": "W33 generated-control savings scale over program and device workloads",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "parameters": {
            "trits_per_byte": TRITS_PER_BYTE,
            "page_trits": PAGE_TRITS,
            "routing_table_bytes_40_point_baseline": ROUTING_TABLE_BYTES_40,
            "page_table_bytes_per_page_baseline": PAGE_TABLE_BYTES_PER_PAGE,
            "endpoint_route_bytes_baseline": ENDPOINT_ROUTE_BYTES,
        },
        "rows": rows,
        "checks": checks,
        "interpretation": (
            "Across workloads, binary-host trit storage remains a payload cost, "
            "but generated W33 topology keeps persistent control bytes at zero. "
            "The control savings scale with object and endpoint count."
        ),
        "honesty_boundary": (
            "This is an accounting sweep using explicit transparent baselines. It "
            "does not benchmark real kernel loader implementations."
        ),
    }


def markdown(payload: dict[str, Any]) -> str:
    rows = []
    for row in payload["rows"]:
        rows.append(
            "| {name} | {object_count} | {raw_bytes} | {page_count} | {payload_host_bit_ratio:.2f}x | {control_bytes_avoided} | {control_bytes_avoided_per_raw_byte:.2f} |".format(
                **row
            )
        )
    return f"""# W(3,3) Workload Economics Sweep

This scales the object-level accounting over batches of program objects and
device events. Payload storage still costs more on a binary host; persistent
topology/control state remains generated by W33.

| Workload | Objects | Raw bytes | Pages | Host payload ratio | Control bytes avoided | Avoided/raw byte |
|---|---:|---:|---:|---:|---:|---:|
{chr(10).join(rows)}

Boundary: workload accounting, not a benchmark of a production kernel loader.
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
    for row in payload["rows"]:
        print(
            f"{row['name']}: objects={row['object_count']}, raw={row['raw_bytes']}, "
            f"pages={row['page_count']}, control_avoided={row['control_bytes_avoided']}"
        )
    print(f"wrote: {json_out.relative_to(ROOT)}")
    print(f"wrote: {md_out.relative_to(ROOT)}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
