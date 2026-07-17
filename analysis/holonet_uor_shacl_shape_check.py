#!/usr/bin/env python3
"""Local SHACL-style shape checks for Holonet-UOR certificates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from holonet_uor_live_adapter import (
    derive_clock_params,
    fetch_openapi,
    probe_request,
    reachable_probe_server,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUTS = [
    ROOT / "data" / "holonet_uor_certificate.json",
    ROOT / "data" / "holonet_uor_rule110_certificate.json",
]
DEFAULT_OUTPUT = ROOT / "data" / "holonet_uor_shacl_shape_report.json"


SHAPES = {
    "HolonetUorCertificateShape": {
        "required": [
            "schema",
            "status",
            "element",
            "transport_partition",
            "proof",
            "trace",
            "certificate",
        ],
    },
    "ElementShape": {
        "path": ["element"],
        "required": ["digestAlgorithm", "digest", "length", "canonicalBytesSha256"],
    },
    "ProofShape": {
        "path": ["proof"],
        "required": ["kind", "checks", "critical_identity_clock", "substrate_checksum"],
    },
    "TraceShape": {
        "path": ["trace"],
        "required": ["kind", "packet_steps", "observables"],
    },
    "TransportPartitionShape": {
        "path": ["transport_partition"],
        "required": ["kind", "components", "cardinality_sum", "complete"],
    },
}


def dig(obj: dict[str, Any], path: list[str] | None) -> Any:
    cur: Any = obj
    for part in path or []:
        cur = cur[part]
    return cur


def validate_shape(
    name: str, shape: dict[str, Any], obj: dict[str, Any]
) -> list[dict[str, Any]]:
    rows = []
    try:
        target = dig(obj, shape.get("path"))
    except Exception as exc:
        return [{"shape": name, "ok": False, "message": f"path missing: {exc}"}]
    for key in shape["required"]:
        rows.append(
            {
                "shape": name,
                "path": ".".join((shape.get("path") or []) + [key]),
                "ok": isinstance(target, dict) and key in target,
                "message": "required property present",
            }
        )
    return rows


def semantic_checks(obj: dict[str, Any]) -> list[dict[str, Any]]:
    packets = obj["trace"]["packet_steps"]
    partition = obj["transport_partition"]
    return [
        {
            "shape": "SemanticShape",
            "path": "status",
            "ok": obj.get("status") == "PASS"
            and obj.get("certificate", {}).get("valid") is True,
            "message": "certificate is valid PASS",
        },
        {
            "shape": "SemanticShape",
            "path": "element.digest",
            "ok": str(obj["element"].get("digest", "")).startswith("sha256:"),
            "message": "digest is sha256-prefixed",
        },
        {
            "shape": "SemanticShape",
            "path": "transport_partition.cardinality_sum",
            "ok": partition.get("cardinality_sum") == len(packets),
            "message": "partition cardinality equals packet step count",
        },
        {
            "shape": "SemanticShape",
            "path": "proof.checks",
            "ok": all(obj["proof"]["checks"].values()),
            "message": "all proof checks pass",
        },
        {
            "shape": "SemanticShape",
            "path": "trace.packet_steps",
            "ok": all(int(step["hops"]) <= 2 for step in packets),
            "message": "all packets obey diameter-two bound",
        },
    ]


def validate_certificate(path: Path, live: bool, server: str | None) -> dict[str, Any]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    for name, shape in SHAPES.items():
        rows.extend(validate_shape(name, shape, obj))
    rows.extend(semantic_checks(obj))
    live_probe = None
    if live and server:
        live_probe = probe_request(
            server,
            "/bridge/shacl/validate",
            {"method": "GET", "query": derive_clock_params(obj)},
        )
    return {
        "source": str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path),
        "conforms": all(row["ok"] for row in rows),
        "violations": [row for row in rows if not row["ok"]],
        "checked_constraints": len(rows),
        "live_uor_shacl_probe": live_probe,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out", default=str(DEFAULT_OUTPUT), help="shape report output JSON"
    )
    parser.add_argument(
        "--live", action="store_true", help="also call live UOR SHACL validate"
    )
    parser.add_argument("inputs", nargs="*", help="Holonet-UOR certificate JSON files")
    args = parser.parse_args(argv)

    inputs = [Path(p) for p in args.inputs] if args.inputs else DEFAULT_INPUTS
    server = reachable_probe_server(fetch_openapi()) if args.live else None
    results = []
    for path in inputs:
        if not path.is_absolute():
            path = ROOT / path
        results.append(validate_certificate(path, live=args.live, server=server))

    report = {
        "schema": "w33.holonet.uor_shacl_shape_report.v1",
        "status": "PASS" if all(row["conforms"] for row in results) else "FAIL",
        "mode": {"live": args.live, "server": server},
        "shape_count": len(SHAPES) + 1,
        "results": results,
        "boundary": (
            "Local SHACL-style validation of the Holonet-UOR certificate schema, "
            "with optional live UOR SHACL witness probing. This is not a Turtle "
            "SHACL graph export yet."
        ),
    }
    output = Path(args.out)
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"status: {report['status']}")
    print(f"certificates: {len(results)}")
    print(f"live: {args.live}")
    print(f"wrote: {output.relative_to(ROOT)}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
