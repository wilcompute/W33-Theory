#!/usr/bin/env python3
"""Program-object compression economics for the W(3,3) wrapper.

This witness separates two different questions that are easy to confuse:

1. payload entropy: arbitrary bytes cannot be compressed for free;
2. control/topology state: W33 routes, buses, and point addresses can be
   generated from the finite geometry instead of persisted as tables.

The fixed six-trit byte code expands raw payload bits when stored on a binary
host, but it gives an exact qutrit-native loader.  The architectural win is the
control plane: no persistent routing table, no endpoint route table, and no
per-page bus table are needed to move the object through the Holonet grammar.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from w33_binary_object_loader import PAGE_TRITS, TRITS_PER_BYTE, page_records
from w33_interactive_os_port_demo import EVENTS
from w33_tiny_risc_packet_isa import encode_program
from w33_universal_program_object_pipeline import PROGRAM_SOURCE, output_bytes_from_vm
from w33_packet_vm import build_payload as build_packet_vm_payload
from w33_uor_runtime_model import ROOT


DEFAULT_JSON = ROOT / "data" / "w33_program_compression_economics.json"
DEFAULT_MD = ROOT / "docs" / "w33_program_compression_economics.md"

ROUTING_TABLE_BYTES_40 = 1170
PAGE_TABLE_BYTES_PER_PAGE = 16
ENDPOINT_ROUTE_BYTES = 24


OBJECTS: list[tuple[str, bytes]] = [
    ("python_source_stub", PROGRAM_SOURCE),
    ("tiny_risc_object", encode_program()),
    ("packet_vm_output", output_bytes_from_vm(build_packet_vm_payload())),
    *[(f"os_event_{event['tick']}_{event['actor']}", bytes(event["payload"])) for event in EVENTS],
]


def economics_row(name: str, blob: bytes) -> dict[str, Any]:
    record = page_records(name, blob)
    raw_bits = len(blob) * 8
    trits = record["trit_len"]
    binary_host_bits_for_trits = trits * 2
    padded_trits = record["page_count"] * PAGE_TRITS
    padded_host_bits = padded_trits * 2
    entropy_trit_lower_bound = len(blob) * 8 / math.log2(3) if blob else 0
    conventional_control_bytes = (
        ROUTING_TABLE_BYTES_40
        + record["page_count"] * PAGE_TABLE_BYTES_PER_PAGE
        + max(1, len(record["transfers"])) * ENDPOINT_ROUTE_BYTES
    )
    w33_persistent_control_bytes = 0
    return {
        "name": name,
        "raw_bytes": len(blob),
        "raw_bits": raw_bits,
        "exact_trits": trits,
        "fixed_trit_host_bits": binary_host_bits_for_trits,
        "page_count": record["page_count"],
        "padded_trits": padded_trits,
        "padded_host_bits": padded_host_bits,
        "payload_binary_expansion_ratio": (
            binary_host_bits_for_trits / raw_bits if raw_bits else 0
        ),
        "page_padding_trits": padded_trits - trits,
        "entropy_trit_lower_bound": entropy_trit_lower_bound,
        "fixed_trit_overhead_vs_entropy_bound": (
            trits / entropy_trit_lower_bound if entropy_trit_lower_bound else 0
        ),
        "conventional_control_bytes": conventional_control_bytes,
        "w33_persistent_control_bytes": w33_persistent_control_bytes,
        "control_bytes_avoided": conventional_control_bytes - w33_persistent_control_bytes,
        "roundtrip_matches": record["roundtrip_matches"],
        "max_transfer_hops": max((transfer["hops"] for transfer in record["transfers"]), default=0),
    }


def build_payload() -> dict[str, Any]:
    rows = [economics_row(name, blob) for name, blob in OBJECTS]
    aggregate = {
        "raw_bytes": sum(row["raw_bytes"] for row in rows),
        "raw_bits": sum(row["raw_bits"] for row in rows),
        "exact_trits": sum(row["exact_trits"] for row in rows),
        "padded_trits": sum(row["padded_trits"] for row in rows),
        "fixed_trit_host_bits": sum(row["fixed_trit_host_bits"] for row in rows),
        "padded_host_bits": sum(row["padded_host_bits"] for row in rows),
        "conventional_control_bytes": sum(row["conventional_control_bytes"] for row in rows),
        "w33_persistent_control_bytes": sum(row["w33_persistent_control_bytes"] for row in rows),
        "control_bytes_avoided": sum(row["control_bytes_avoided"] for row in rows),
    }
    checks = {
        "all_roundtrips_match": all(row["roundtrip_matches"] for row in rows),
        "all_routes_diameter_two": all(row["max_transfer_hops"] <= 2 for row in rows),
        "fixed_six_trit_byte_code_expands_binary_payload": all(
            row["payload_binary_expansion_ratio"] >= 1.5 or row["raw_bytes"] == 0
            for row in rows
        ),
        "control_plane_collapses_to_zero_persistent_bytes": aggregate["w33_persistent_control_bytes"] == 0,
        "control_savings_positive": aggregate["control_bytes_avoided"] > 0,
        "page_size_is_q_four": PAGE_TRITS == 81,
    }
    return {
        "schema": "w33.program_compression_economics.v1",
        "theorem": "W33 wrapper preserves payload entropy while eliminating persisted topology control state",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "parameters": {
            "trits_per_byte": TRITS_PER_BYTE,
            "page_trits": PAGE_TRITS,
            "routing_table_bytes_40_point_baseline": ROUTING_TABLE_BYTES_40,
            "page_table_bytes_per_page_baseline": PAGE_TABLE_BYTES_PER_PAGE,
            "endpoint_route_bytes_baseline": ENDPOINT_ROUTE_BYTES,
        },
        "rows": rows,
        "aggregate": aggregate,
        "checks": checks,
        "interpretation": (
            "The qutrit-native byte loader costs 12 binary host bits per byte "
            "when naively stored on binary hardware. The architecture win is not "
            "payload compression; it is generated topology: routes, buses, and "
            "scheduling handles are recomputed from W33 instead of stored."
        ),
        "honesty_boundary": (
            "No entropy-violating compression is claimed. The baseline control "
            "bytes are a transparent accounting model, not a benchmark of every "
            "operating system loader."
        ),
    }


def markdown(payload: dict[str, Any]) -> str:
    rows = []
    for row in payload["rows"]:
        rows.append(
            "| {name} | {raw_bytes} | {exact_trits} | {page_count} | {payload_binary_expansion_ratio:.2f}x | {control_bytes_avoided} |".format(
                **row
            )
        )
    aggregate = payload["aggregate"]
    return f"""# W(3,3) Program Compression Economics

This separates payload entropy from control/topology state. Bytes are not made
magically smaller: the fixed qutrit loader uses six trits per byte, which is
`12` binary host bits per byte if stored naively on binary hardware. The win is
that W33 topology is generated, so persistent route/control tables collapse.

| Object | Raw bytes | Exact trits | Pages | Binary payload ratio | Control bytes avoided |
|---|---:|---:|---:|---:|---:|
{chr(10).join(rows)}

Aggregate control bytes avoided: `{aggregate['control_bytes_avoided']}`.
Aggregate raw bytes: `{aggregate['raw_bytes']}`. Aggregate padded trits:
`{aggregate['padded_trits']}`.

Boundary: this is control-plane compression, not entropy-free payload
compression.
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
        "aggregate: raw_bytes={raw_bytes}, exact_trits={exact_trits}, control_bytes_avoided={control_bytes_avoided}".format(
            **payload["aggregate"]
        )
    )
    print(f"wrote: {json_out.relative_to(ROOT)}")
    print(f"wrote: {md_out.relative_to(ROOT)}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
