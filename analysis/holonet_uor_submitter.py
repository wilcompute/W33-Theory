#!/usr/bin/env python3
"""Submit or dry-run a Holonet-UOR adapter plan.

Default mode is deliberately non-mutating: it verifies that every request in
the plan is shaped, classifies POSTs as prepared, and can live-probe GET routes.
Use ``--live --allow-post`` only when the public UOR API is ready to accept the
POST surfaces advertised in OpenAPI.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from holonet_uor_live_adapter import (
    fetch_openapi,
    probe_request,
    reachable_probe_server,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = ROOT / "data" / "holonet_uor_live_adapter_plan.json"
DEFAULT_OUTPUT = ROOT / "data" / "holonet_uor_submitter_report.json"


def classify_probe(row: dict[str, Any]) -> str:
    if row.get("ok"):
        return "accepted"
    status = row.get("status")
    text = (row.get("error") or row.get("body_preview") or "").lower()
    if status == 546 or "worker_resource_limit" in text:
        return "runtime_resource_limit"
    if status in {401, 403} or "forbidden" in text or "cloudflare" in text:
        return "runtime_access_blocked"
    if status == 404:
        return "runtime_route_missing"
    if status == 405:
        return "runtime_method_boundary"
    return "runtime_failed"


def request_ready(path: str, spec: dict[str, Any]) -> dict[str, Any]:
    has_payload = bool(spec.get("json") or spec.get("query"))
    return {
        "path": path,
        "method": spec.get("method"),
        "has_payload": has_payload,
        "prepared": bool(spec.get("method")) and has_payload,
    }


def build_report(plan: dict[str, Any], live: bool, allow_post: bool) -> dict[str, Any]:
    openapi = fetch_openapi()
    probe_server = (
        reachable_probe_server(openapi)
        if live
        else plan["openapi"].get("probe_server_url")
    )
    submissions: dict[str, Any] = {}

    for path, spec in plan["requests"].items():
        method = spec["method"]
        ready = request_ready(path, spec)
        row: dict[str, Any] = {
            **ready,
            "submitted": False,
            "classification": "prepared_not_submitted",
        }
        if not live:
            submissions[path] = row
            continue
        if method == "POST" and not allow_post:
            row["classification"] = "prepared_post_not_submitted"
            row["reason"] = "use --allow-post to submit mutating/runtime POST surfaces"
            submissions[path] = row
            continue
        probe = probe_request(probe_server, path, spec)
        row["submitted"] = True
        row["probe"] = probe
        row["classification"] = classify_probe(probe)
        submissions[path] = row

    accepted = [
        path for path, row in submissions.items() if row["classification"] == "accepted"
    ]
    blocked = [
        path
        for path, row in submissions.items()
        if row["classification"]
        in {
            "runtime_resource_limit",
            "runtime_access_blocked",
            "runtime_method_boundary",
        }
    ]
    prepared = [path for path, row in submissions.items() if row.get("prepared")]

    return {
        "schema": "w33.holonet.uor_submitter_report.v1",
        "status": "PASS" if len(prepared) == len(plan["requests"]) else "FAIL",
        "mode": {
            "live": live,
            "allow_post": allow_post,
            "probe_server": probe_server,
        },
        "source_plan_fingerprint": plan.get("request_fingerprint"),
        "prepared_request_count": len(prepared),
        "accepted_live_count": len(accepted),
        "blocked_or_limited_count": len(blocked),
        "submissions": submissions,
        "production_gate": {
            "openapi_contract_present": plan.get("status") == "PASS",
            "all_requests_prepared": len(prepared) == len(plan["requests"]),
            "critical_identity_live_proof_accepted": submissions.get(
                "/bridge/proof/critical-identity", {}
            ).get("classification")
            in {"accepted", "prepared_not_submitted"},
            "post_surfaces_require_runtime_access": any(
                row["method"] == "POST" and row["classification"] != "accepted"
                for row in submissions.values()
            ),
        },
        "boundary": (
            "Dry-run mode proves payload readiness. Live mode records public API "
            "acceptance or runtime boundary per endpoint; it does not treat an "
            "OpenAPI contract as completed submission."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--plan", default=str(DEFAULT_PLAN), help="Holonet-UOR adapter plan JSON"
    )
    parser.add_argument(
        "--out", default=str(DEFAULT_OUTPUT), help="submitter report output JSON"
    )
    parser.add_argument(
        "--live", action="store_true", help="probe/submit live endpoints"
    )
    parser.add_argument(
        "--allow-post",
        action="store_true",
        help="allow POST endpoint submission in live mode",
    )
    args = parser.parse_args(argv)

    plan_path = Path(args.plan)
    if not plan_path.is_absolute():
        plan_path = ROOT / plan_path
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    report = build_report(plan, live=args.live, allow_post=args.allow_post)

    output = Path(args.out)
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"status: {report['status']}")
    print(f"prepared: {report['prepared_request_count']}/{len(plan['requests'])}")
    print(f"accepted live: {report['accepted_live_count']}")
    print(f"blocked/limited: {report['blocked_or_limited_count']}")
    print(f"wrote: {output.relative_to(ROOT)}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
