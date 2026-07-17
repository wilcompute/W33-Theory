#!/usr/bin/env python3
"""Probe UOR live holonomy with W33 S3/Z2 shadow payloads."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from holonet_uor_live_adapter import (
    fetch_openapi,
    probe_request,
    reachable_probe_server,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "w33_uor_holonomy_shadow_api_bridge.json"
DEFAULT_OUTPUT = ROOT / "data" / "w33_uor_holonomy_live_probe.json"


def classify(row: dict) -> str:
    if row.get("ok"):
        return "accepted"
    text = (row.get("error") or row.get("body_preview") or "").lower()
    if row.get("status") in {401, 403} or "cloudflare" in text:
        return "runtime_access_blocked"
    if row.get("status") == 405:
        return "runtime_method_boundary"
    return "runtime_failed"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input", default=str(DEFAULT_INPUT), help="holonomy bridge JSON"
    )
    parser.add_argument(
        "--out", default=str(DEFAULT_OUTPUT), help="live probe output JSON"
    )
    parser.add_argument(
        "--live", action="store_true", help="actually probe live UOR holonomy POST"
    )
    args = parser.parse_args(argv)

    source = Path(args.input)
    if not source.is_absolute():
        source = ROOT / source
    bridge = json.loads(source.read_text(encoding="utf-8"))
    server = reachable_probe_server(fetch_openapi()) if args.live else None

    rows = []
    for item in bridge["word_table"]:
        request = {"method": "POST", "json": item["uor_holonomy_payload"]}
        probe = (
            probe_request(server, "/bridge/observable/holonomy", request)
            if server
            else None
        )
        rows.append(
            {
                "word": item["word"],
                "z2_shadow": item["z2_shadow"],
                "payload": item["uor_holonomy_payload"],
                "submitted": bool(args.live),
                "classification": (
                    classify(probe) if probe else "prepared_not_submitted"
                ),
                "probe": probe,
            }
        )

    accepted = sum(1 for row in rows if row["classification"] == "accepted")
    report = {
        "schema": "w33.uor.holonomy_live_probe.v1",
        "status": "PASS",
        "mode": {"live": args.live, "server": server},
        "accepted_count": accepted,
        "prepared_count": len(rows),
        "rows": rows,
        "boundary": (
            "The S3->Z2 holonomy bridge is locally verified. This report records "
            "whether UOR's live holonomy POST endpoint currently accepts those "
            "payloads."
        ),
    }

    output = Path(args.out)
    if not output.is_absolute():
        output = ROOT / output
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"status: {report['status']}")
    print(f"prepared: {report['prepared_count']}")
    print(f"accepted: {report['accepted_count']}")
    print(f"wrote: {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
