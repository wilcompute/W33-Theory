#!/usr/bin/env python3
"""Local mock runtime for the Holonet-UOR adapter plan.

The public UOR OpenAPI contract advertises the POST surfaces we need, but the
current public runtime blocks several of them. This file gives demos a
deterministic local stand-in for the whole path:

    address -> partition -> trace -> proof -> holonomy -> stream -> cert -> pipeline

It is intentionally labeled as a mock runtime, not as UOR Foundation output.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = ROOT / "data" / "holonet_uor_live_adapter_plan.json"
DEFAULT_CERT = ROOT / "data" / "holonet_uor_certificate.json"
DEFAULT_OUTPUT = ROOT / "data" / "holonet_uor_mock_runtime_report.json"


def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def as_byte_stream(value: str) -> list[int]:
    return list(value.encode("utf-8"))


def simulate_address_encode(request: dict[str, Any]) -> dict[str, Any]:
    text = request["json"]["input"]
    payload = text.encode(request["json"].get("encoding", "utf8"))
    digest = sha256_hex(payload)
    return {
        "@type": "u:Address",
        "u:digestAlgorithm": "sha256",
        "u:digest": f"sha256:{digest}",
        "u:length": len(payload),
        "u:glyph": [
            {"index": idx, "byte": byte, "hex": f"{byte:02x}"}
            for idx, byte in enumerate(payload[:64])
        ],
        "u:glyphTruncated": len(payload) > 64,
    }


def classify_byte(byte: int) -> str:
    if byte == 0:
        return "exterior"
    if byte % 2 == 1:
        return "units"
    if byte & (byte - 1) == 0:
        return "irreducibles"
    return "reducibles"


def simulate_partition(
    request: dict[str, Any], certificate: dict[str, Any]
) -> dict[str, Any]:
    if request["json"].get("input") == certificate["element"]["digest"]:
        return {
            "@type": "partition:Partition",
            "partition:source": "HolonetTransportPartition",
            "partition:components": certificate["transport_partition"]["components"],
            "partition:boundary": certificate["transport_partition"][
                "uor_native_boundary"
            ],
        }
    buckets = {"units": [], "irreducibles": [], "reducibles": [], "exterior": []}
    for idx, byte in enumerate(as_byte_stream(str(request["json"].get("input", "")))):
        buckets[classify_byte(byte)].append(idx)
    return {
        "@type": "partition:Partition",
        "partition:source": "MockBytePartition",
        "partition:components": {
            name: {"cardinality": len(values), "indices": values}
            for name, values in buckets.items()
        },
    }


def op_value(value: int, n: int, op: str) -> int:
    modulus = 2**n
    if op == "neg":
        return (-value) % modulus
    if op == "bnot":
        return (modulus - 1 - value) % modulus
    if op == "succ":
        return (value + 1) % modulus
    if op == "pred":
        return (value - 1) % modulus
    raise ValueError(f"unsupported op {op!r}")


def simulate_trace(request: dict[str, Any]) -> dict[str, Any]:
    query = request.get("query", {})
    n = int(query.get("n", 1))
    value = int(query.get("x", 0)) % (2**n)
    ops = [op for op in str(query.get("ops", "neg,bnot")).split(",") if op]
    frames = [{"step": 0, "op": "input", "value": value, "bits": f"{value:0{n}b}"}]
    drift = 0
    for idx, op in enumerate(ops, start=1):
        prev = value
        value = op_value(value, n, op)
        drift += (prev ^ value).bit_count()
        frames.append({"step": idx, "op": op, "value": value, "bits": f"{value:0{n}b}"})
    return {
        "@type": "trace:ExecutionTrace",
        "trace:frameCount": len(frames),
        "trace:totalHammingDrift": drift,
        "trace:frames": frames,
    }


def simulate_proof(request: dict[str, Any]) -> dict[str, Any]:
    query = request.get("query", {})
    n = int(query.get("n", 1))
    x = int(query.get("x", 0)) % (2**n)
    bnot = op_value(x, n, "bnot")
    neg_bnot = op_value(bnot, n, "neg")
    succ = op_value(x, n, "succ")
    return {
        "@type": ["proof:Proof", "proof:CriticalIdentityProof"],
        "proof:verified": neg_bnot == succ,
        "proof:criticalIdentity": "neg(bnot(x)) = succ(x)",
        "proof:witness": {
            "x": x,
            "n": n,
            "bnot_x": bnot,
            "neg_bnot_x": neg_bnot,
            "succ_x": succ,
        },
    }


def simulate_holonomy(request: dict[str, Any]) -> dict[str, Any]:
    path = [int(x) for x in request["json"].get("path", [])]
    quantum = max(1, int(request["json"].get("quantum", 1)))
    modulus = 2 ** min(quantum + 3, 16)
    acc = 0
    for idx, value in enumerate(path):
        acc = (acc + (idx + 1) * value) % modulus
    return {
        "@type": "observable:HolonomyObservable",
        "observable:pathLength": len(path),
        "observable:ringModulus": modulus,
        "observable:holonomyValue": acc,
        "observable:z2Shadow": acc % 2,
    }


def simulate_stream(request: dict[str, Any]) -> dict[str, Any]:
    stream = [int(x) for x in request["json"].get("stream", [])]
    window = int(request["json"].get("window_size", 8))
    rows = []
    for start in range(0, max(0, len(stream) - window + 1)):
        values = stream[start : start + window]
        rows.append(
            {
                "start": start,
                "sum": sum(values),
                "ring": sum(values) % 256,
                "hamming": sum((a ^ b).bit_count() for a, b in zip(values, values[1:])),
                "curvature": max(values) - min(values) if values else 0,
            }
        )
    return {
        "@type": "observable:StreamObservable",
        "observable:windowSize": window,
        "observable:windowCount": len(rows),
        "observable:windows": rows[:64],
        "observable:truncated": len(rows) > 64,
    }


def simulate_shacl(request: dict[str, Any]) -> dict[str, Any]:
    proof = simulate_proof({"query": request.get("query", {})})
    return {
        "@type": "sh:ValidationReport",
        "sh:conforms": bool(proof["proof:verified"]),
        "uor:checkedShape": "proof:CriticalIdentityProofShape",
        "uor:witness": proof["proof:witness"],
    }


def simulate_cert_issue(request: dict[str, Any]) -> dict[str, Any]:
    body = request["json"]
    cert_payload = canonical_bytes(body)
    return {
        "@type": "cert:Certificate",
        "cert:valid": True,
        "cert:certifies": body.get("certify", "derivation"),
        "cert:derivationId": body.get("derivation_id"),
        "cert:digest": f"sha256:{sha256_hex(cert_payload)}",
    }


def simulate_pipeline(request: dict[str, Any]) -> dict[str, Any]:
    body = request["json"]
    host = body.get("host_bytes", [])
    host_values = host if isinstance(host, list) else [host]
    digest = sha256_hex(bytes(int(x) % 256 for x in host_values))
    return {
        "@type": "schema:PipelineResult",
        "pipeline:stages": ["Datum", "Validated", "Grounded", "Triad", "Certified"],
        "pipeline:targetType": body.get("target_type", "schema:Datum"),
        "pipeline:phase": body.get("phase", "W4"),
        "pipeline:n": body.get("n", 8),
        "pipeline:hostByteCount": len(host_values),
        "pipeline:digest": f"sha256:{digest}",
        "pipeline:grade": "A",
    }


SIMULATORS = {
    "/kernel/address/encode": simulate_address_encode,
    "/bridge/partition": simulate_partition,
    "/bridge/trace": simulate_trace,
    "/bridge/proof/critical-identity": simulate_proof,
    "/bridge/observable/holonomy": simulate_holonomy,
    "/bridge/observable/stream": simulate_stream,
    "/bridge/shacl/validate": simulate_shacl,
    "/cert/issue": simulate_cert_issue,
    "/pipeline/run": simulate_pipeline,
}


def simulate(plan: dict[str, Any], certificate: dict[str, Any]) -> dict[str, Any]:
    responses: dict[str, Any] = {}
    for path, request in plan["requests"].items():
        simulator = SIMULATORS[path]
        if path == "/bridge/partition":
            response = simulator(request, certificate)
        else:
            response = simulator(request)
        responses[path] = {
            "status": "PASS",
            "method": request["method"],
            "response": response,
        }
    return {
        "schema": "w33.holonet.uor_mock_runtime_report.v1",
        "status": (
            "PASS"
            if all(row["status"] == "PASS" for row in responses.values())
            else "FAIL"
        ),
        "source_plan_fingerprint": plan.get("request_fingerprint"),
        "responses": responses,
        "pipeline_complete": all(path in responses for path in SIMULATORS),
        "boundary": (
            "Local deterministic UOR-shaped runtime for Holonet demos. It is a "
            "mock of advertised endpoint semantics, not a replacement for the "
            "UOR Foundation service."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", default=str(DEFAULT_PLAN), help="adapter plan JSON")
    parser.add_argument(
        "--cert", default=str(DEFAULT_CERT), help="Holonet-UOR certificate JSON"
    )
    parser.add_argument(
        "--out", default=str(DEFAULT_OUTPUT), help="mock runtime output JSON"
    )
    args = parser.parse_args(argv)

    plan_path = Path(args.plan)
    cert_path = Path(args.cert)
    if not plan_path.is_absolute():
        plan_path = ROOT / plan_path
    if not cert_path.is_absolute():
        cert_path = ROOT / cert_path
    report = simulate(
        json.loads(plan_path.read_text(encoding="utf-8")),
        json.loads(cert_path.read_text(encoding="utf-8")),
    )
    output = Path(args.out)
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"status: {report['status']}")
    print(f"responses: {len(report['responses'])}")
    print(f"pipeline complete: {report['pipeline_complete']}")
    print(f"wrote: {output.relative_to(ROOT)}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
