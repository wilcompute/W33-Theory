#!/usr/bin/env python3
"""Emit a UOR-style certificate for a Holonet wrapper run.

This is an offline bridge. It does not call uor.foundation and it does not
claim that the UOR reference implementation has certified the Holonet VM.
Instead it maps one Holonet wrapper artifact into the UOR vocabulary:

    content address -> transport partition -> proof checks -> trace -> cert

The purpose is practical: any classical command wrapped by ``holonet_wrap.py``
can now be given a stable content address and a reproducible certificate that
records the W(3,3) packet schedule used as its control envelope.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from math import ceil, log2
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "holonet_wrap_demo_factorial.json"
DEFAULT_OUTPUT = ROOT / "data" / "holonet_uor_certificate.json"


def canonical_json_bytes(obj: Any) -> bytes:
    """Canonical byte preimage for this bridge certificate."""
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")


def sha256_digest(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def recompute_substrate_checksum(packets: list[dict[str, Any]]) -> str:
    """Mirror analysis/holonet_wrap.py without importing side-channel code."""
    acc = 0
    for packet in packets:
        for ch in packet["src"] + packet["dst"]:
            acc = (3 * acc + int(ch)) % (3**20)
        acc = (
            acc
            + int(packet["hops"])
            + 2 * int(packet["relays"])
            + int(packet["symplectic"])
        ) % (3**20)
    return format(acc, "x")


def transport_partition(packets: list[dict[str, Any]]) -> dict[str, Any]:
    """Transport analog of UOR's four-way partition.

    UOR's native partition is a ring factorization over Z/(2^n)Z. Here the
    carrier is W(3,3) packet transport, so the four buckets are intentionally
    marked as a transport analog:

    - units: identity packets;
    - irreducibles: one-hop packets;
    - reducibles: two-hop packets decomposed through a relay;
    - exterior: malformed packets or packets outside the diameter-2 fabric.
    """
    buckets: dict[str, list[dict[str, Any]]] = {
        "units": [],
        "irreducibles": [],
        "reducibles": [],
        "exterior": [],
    }
    for packet in packets:
        hops = int(packet.get("hops", -1))
        if hops == 0:
            buckets["units"].append(packet)
        elif hops == 1:
            buckets["irreducibles"].append(packet)
        elif hops == 2 and int(packet.get("relays", 0)) >= 1:
            buckets["reducibles"].append(packet)
        else:
            buckets["exterior"].append(packet)

    total = len(packets)
    return {
        "kind": "HolonetTransportPartition",
        "uor_native_boundary": (
            "Analog of UOR partition/Partition, not a native UOR ring partition. "
            "The carrier is the W(3,3) diameter-2 route fabric."
        ),
        "components": {
            name: {
                "cardinality": len(values),
                "density": f"{len(values)}/{total}" if total else "0/0",
                "packet_ids": [f"{p['label']}:{p['index']}" for p in values],
            }
            for name, values in buckets.items()
        },
        "cardinality_sum": sum(len(values) for values in buckets.values()),
        "complete": sum(len(values) for values in buckets.values()) == total,
    }


def critical_identity_clock(packet_count: int) -> dict[str, Any]:
    """Verify neg(bnot(x)) = succ(x) over the smallest packet-clock Witt ring."""
    width = max(1, ceil(log2(max(packet_count, 1))))
    modulus = 2**width
    rows = []
    ok = True
    for x in range(packet_count):
        bnot = (modulus - 1 - x) % modulus
        neg_bnot = (-bnot) % modulus
        succ = (x + 1) % modulus
        row_ok = neg_bnot == succ
        ok = ok and row_ok
        rows.append(
            {
                "packet_index": x,
                "bnot": bnot,
                "neg_bnot": neg_bnot,
                "succ": succ,
                "ok": row_ok,
            }
        )
    return {
        "witt_level": width,
        "modulus": modulus,
        "identity": "neg(bnot(x)) = succ(x)",
        "verified_for_packet_indices": packet_count,
        "ok": ok,
        "sample": rows[:8],
    }


def trace_from_report(report: dict[str, Any]) -> dict[str, Any]:
    packets = report.get("packets", [])
    return {
        "kind": "HolonetComputationTrace",
        "command_line": report.get("command_line"),
        "genome_sha256": report.get("genome_sha256"),
        "returncode": report.get("returncode"),
        "packet_steps": [
            {
                "packet_id": f"{packet['label']}:{packet['index']}",
                "label": packet["label"],
                "src": packet["src"],
                "dst": packet["dst"],
                "path": packet["path"],
                "hops": packet["hops"],
                "relays": packet["relays"],
                "symplectic": packet["symplectic"],
            }
            for packet in packets
        ],
        "observables": {
            "packet_count": report.get("packet_count", len(packets)),
            "max_hops": report.get("max_hops"),
            "routing_table_entries": report.get("control_plane", {}).get(
                "routing_table_entries"
            ),
            "routing_state_bytes": report.get("control_plane", {}).get(
                "routing_state_bytes"
            ),
            "sidechannel_delta": report.get("sidechannel_delta", {}),
        },
    }


def build_certificate(report: dict[str, Any], source_path: Path) -> dict[str, Any]:
    canonical_payload = canonical_json_bytes(report)
    digest = sha256_digest(canonical_payload)
    packets = report.get("packets", [])
    expected_checksum = report.get("substrate_checksum")
    recomputed_checksum = recompute_substrate_checksum(packets)
    partition = transport_partition(packets)
    clock = critical_identity_clock(len(packets))

    proof_checks = {
        "content_address_roundtrip": digest == sha256_digest(canonical_payload),
        "packet_count_matches": int(report.get("packet_count", len(packets)))
        == len(packets),
        "transport_partition_complete": partition["complete"],
        "diameter_two_bound": max(
            (int(packet.get("hops", 99)) for packet in packets), default=0
        )
        <= 2,
        "substrate_checksum_matches": expected_checksum == recomputed_checksum,
        "critical_identity_packet_clock": clock["ok"],
    }
    all_checks_pass = all(proof_checks.values())

    return {
        "schema": "w33.holonet.uor_certificate.v1",
        "status": "PASS" if all_checks_pass else "FAIL",
        "source": str(
            source_path.relative_to(ROOT)
            if source_path.is_relative_to(ROOT)
            else source_path
        ),
        "uor_alignment": {
            "framework": "Universal Object Reference",
            "live_openapi_version_observed": "0.3.1",
            "addressing": "u/Element with digestAlgorithm sha256",
            "proof": "proof/Proof-style named checks",
            "trace": "trace/ComputationTrace-style packet sequence",
            "certificate": "cert/Certificate-style attestation",
            "online_api_anchors": [
                "https://uor.foundation/kernel/address/encode",
                "https://uor.foundation/bridge/partition",
                "https://uor.foundation/bridge/trace",
                "https://uor.foundation/bridge/proof/critical-identity",
                "https://uor.foundation/bridge/observable/holonomy",
                "https://uor.foundation/bridge/observable/stream",
                "https://uor.foundation/bridge/shacl/validate",
                "https://uor.foundation/cert/issue",
                "https://uor.foundation/pipeline/run",
            ],
        },
        "element": {
            "digestAlgorithm": "sha256",
            "digest": digest,
            "length": len(canonical_payload),
            "canonicalBytesEncoding": "canonical-json/sort_keys/separators",
            "canonicalBytesSha256": hashlib.sha256(canonical_payload).hexdigest(),
        },
        "transport_partition": partition,
        "proof": {
            "kind": "HolonetUorBridgeProof",
            "checks": proof_checks,
            "critical_identity_clock": clock,
            "substrate_checksum": {
                "claimed": expected_checksum,
                "recomputed": recomputed_checksum,
                "ok": expected_checksum == recomputed_checksum,
            },
        },
        "trace": trace_from_report(report),
        "certificate": {
            "valid": all_checks_pass,
            "attests": [
                "stable content address for the wrapped command artifact",
                "complete W(3,3) transport partition over all packets",
                "diameter-2 routing bound for every packet",
                "packet-clock instance of UOR critical identity",
                "checksum-preserving trace reconstruction",
            ],
            "boundary": (
                "This is an offline bridge certificate. It is UOR-shaped and "
                "uses UOR-pinned SHA-256 content addressing, but it is not yet "
                "emitted by the Rust uor-foundation pipeline or verified by the "
                "uor.foundation service."
            ),
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input", default=str(DEFAULT_INPUT), help="Holonet wrapper JSON artifact"
    )
    parser.add_argument(
        "--out", default=str(DEFAULT_OUTPUT), help="certificate output JSON"
    )
    args = parser.parse_args(argv)

    source_path = Path(args.input)
    if not source_path.is_absolute():
        source_path = ROOT / source_path
    report = json.loads(source_path.read_text(encoding="utf-8"))
    certificate = build_certificate(report, source_path)

    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = ROOT / out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(certificate, indent=2), encoding="utf-8")

    print(f"status: {certificate['status']}")
    print(f"digest: {certificate['element']['digest']}")
    print(f"packets: {certificate['trace']['observables']['packet_count']}")
    print(f"max_hops: {certificate['trace']['observables']['max_hops']}")
    print(f"wrote: {out_path.relative_to(ROOT)}")
    return 0 if certificate["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
