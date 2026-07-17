#!/usr/bin/env python3
"""Build a live-UOR adapter plan from an offline Holonet-UOR certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CERT = ROOT / "data" / "holonet_uor_certificate.json"
DEFAULT_OUTPUT = ROOT / "data" / "holonet_uor_live_adapter_plan.json"
OPENAPI_URL = "https://uor.foundation/openapi.json"
BASE_URL = "https://uor.foundation"

REQUIRED_ENDPOINTS = {
    "/kernel/address/encode": "POST",
    "/bridge/partition": "POST",
    "/bridge/trace": "GET",
    "/bridge/proof/critical-identity": "GET",
    "/bridge/observable/holonomy": "POST",
    "/bridge/observable/stream": "POST",
    "/bridge/shacl/validate": "GET",
    "/cert/issue": "POST",
    "/pipeline/run": "POST",
}


def canonical_json_bytes(obj: Any) -> bytes:
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")


def fetch_openapi() -> dict[str, Any]:
    with urllib.request.urlopen(OPENAPI_URL, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def endpoint_catalog(openapi: dict[str, Any]) -> dict[str, Any]:
    paths = openapi.get("paths", {})
    catalog: dict[str, Any] = {}
    for path, method in REQUIRED_ENDPOINTS.items():
        operation = paths.get(path, {}).get(method.lower())
        catalog[path] = {
            "method": method,
            "present": operation is not None,
            "summary": operation.get("summary") if operation else None,
            "operationId": operation.get("operationId") if operation else None,
        }
    return catalog


def derive_clock_params(certificate: dict[str, Any]) -> dict[str, int]:
    digest_hex = certificate["element"]["digest"].split(":", 1)[1]
    n = int(certificate["proof"]["critical_identity_clock"]["witt_level"])
    return {"x": int(digest_hex[:4], 16) % (2**n), "n": n}


def packet_stream(certificate: dict[str, Any]) -> list[int]:
    stream: list[int] = []
    for step in certificate["trace"]["packet_steps"]:
        stream.extend([int(step["hops"]), int(step["relays"]), int(step["symplectic"])])
    return stream or [0, 0]


def holonomy_path(certificate: dict[str, Any]) -> list[int]:
    values = []
    for step in certificate["trace"]["packet_steps"][:12]:
        values.append(
            (int(step["hops"]) + 3 * int(step["symplectic"]) + int(step["relays"])) % 16
        )
    while len(values) < 3:
        values.append(0)
    return values


def build_requests(certificate: dict[str, Any]) -> dict[str, Any]:
    compact = canonical_json_bytes(certificate).decode("ascii")
    digest_hex = certificate["element"]["digest"].split(":", 1)[1]
    clock = derive_clock_params(certificate)
    host_bytes = [int(digest_hex[i : i + 2], 16) for i in range(0, 32, 2)]
    return {
        "/kernel/address/encode": {
            "method": "POST",
            "json": {"input": compact, "encoding": "utf8"},
        },
        "/bridge/partition": {
            "method": "POST",
            "json": {
                "input": certificate["element"]["digest"],
                "encoding": "utf8",
                "resolver": "EvaluationResolver",
            },
        },
        "/bridge/trace": {
            "method": "GET",
            "query": {"x": clock["x"], "n": clock["n"], "ops": "neg,bnot"},
        },
        "/bridge/proof/critical-identity": {
            "method": "GET",
            "query": clock,
        },
        "/bridge/observable/holonomy": {
            "method": "POST",
            "json": {"path": holonomy_path(certificate), "quantum": 1},
        },
        "/bridge/observable/stream": {
            "method": "POST",
            "json": {
                "stream": packet_stream(certificate),
                "window_size": 8,
                "metrics": ["stratum", "hamming", "curvature", "ring"],
                "quantum": 1,
            },
        },
        "/bridge/shacl/validate": {
            "method": "GET",
            "query": clock,
        },
        "/cert/issue": {
            "method": "POST",
            "json": {
                "certify": "derivation",
                "derivation_id": f"urn:uor:derivation:sha256:{digest_hex}",
            },
        },
        "/pipeline/run": {
            "method": "POST",
            "json": {
                "host_bytes": host_bytes,
                "target_type": "schema:Datum",
                "phase": "W4",
                "n": min(16, max(1, clock["n"])),
            },
        },
    }


def request_fingerprint(requests: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json_bytes(requests)).hexdigest()


def probe_request(
    base_url: str, path: str, request_spec: dict[str, Any]
) -> dict[str, Any]:
    url = base_url.rstrip("/") + path
    method = request_spec["method"]
    data = None
    headers = {
        "Accept": "application/json",
        "User-Agent": "w33-holonet-uor-adapter/1.0",
    }
    if method == "GET":
        query = urllib.parse.urlencode(request_spec.get("query", {}))
        if query:
            url += "?" + query
    else:
        data = json.dumps(request_spec.get("json", {})).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    opener = urllib.request.build_opener(NoMethodRewriteRedirectHandler)
    try:
        with opener.open(req, timeout=20) as response:
            body = response.read(6000).decode("utf-8", "replace")
            return {
                "ok": 200 <= response.status < 300,
                "status": response.status,
                "content_type": response.headers.get("content-type"),
                "body_preview": body[:2000],
            }
    except urllib.error.HTTPError as exc:
        body = exc.read(2000).decode("utf-8", "replace")
        return {"ok": False, "status": exc.code, "error": body[:1000]}
    except Exception as exc:
        return {"ok": False, "error": repr(exc)}


class NoMethodRewriteRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Preserve POST bodies across the UOR API's 302 function redirects."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[override]
        if req.get_method() == "POST" and code in {301, 302, 303, 307, 308}:
            return urllib.request.Request(
                newurl,
                data=req.data,
                headers=dict(req.header_items()),
                method=req.get_method(),
            )
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def first_server_url(openapi: dict[str, Any]) -> str:
    servers = openapi.get("servers") or []
    if servers and servers[0].get("url"):
        return str(servers[0]["url"])
    return BASE_URL


def reachable_probe_server(openapi: dict[str, Any]) -> str:
    for server in openapi.get("servers") or []:
        url = str(server.get("url", "")).rstrip("/")
        if not url:
            continue
        probe = probe_request(
            url,
            "/bridge/proof/critical-identity",
            {"method": "GET", "query": {"x": 1, "n": 4}},
        )
        if probe.get("ok"):
            return url
    return first_server_url(openapi)


def build_plan(certificate: dict[str, Any], probe_live: bool) -> dict[str, Any]:
    openapi = fetch_openapi()
    server_url = first_server_url(openapi)
    probe_server_url = reachable_probe_server(openapi) if probe_live else server_url
    catalog = endpoint_catalog(openapi)
    requests = build_requests(certificate)
    missing = [path for path, row in catalog.items() if not row["present"]]
    probes = {}
    if probe_live:
        for path in (
            "/bridge/proof/critical-identity",
            "/bridge/trace",
            "/bridge/observable/holonomy",
            "/bridge/observable/stream",
            "/pipeline/run",
        ):
            probes[path] = probe_request(probe_server_url, path, requests[path])
    live_probe_summary = {
        "attempted": len(probes),
        "ok": sum(1 for row in probes.values() if row.get("ok")),
        "failed": sum(1 for row in probes.values() if not row.get("ok")),
    }
    return {
        "schema": "w33.holonet.uor_live_adapter_plan.v1",
        "status": "PASS" if not missing else "FAIL",
        "openapi": {
            "url": OPENAPI_URL,
            "server_url": server_url,
            "probe_server_url": probe_server_url,
            "title": openapi.get("info", {}).get("title"),
            "version": openapi.get("info", {}).get("version"),
            "path_count": len(openapi.get("paths", {})),
        },
        "endpoint_catalog": catalog,
        "missing_required_endpoints": missing,
        "certificate_digest": certificate["element"]["digest"],
        "request_fingerprint": request_fingerprint(requests),
        "requests": requests,
        "live_probes": probes,
        "live_probe_summary": live_probe_summary,
        "boundary": (
            "This plan is endpoint-aware and payload-ready. By default it does "
            "not submit the full Holonet certificate to UOR; use --probe-live "
            "for bounded live checks and a future submitter for production. "
            "The current public API may expose endpoints in OpenAPI before all "
            "runtime routes accept external calls."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cert", default=str(DEFAULT_CERT), help="Holonet-UOR certificate JSON"
    )
    parser.add_argument(
        "--out", default=str(DEFAULT_OUTPUT), help="adapter-plan output JSON"
    )
    parser.add_argument(
        "--probe-live", action="store_true", help="make bounded live UOR API calls"
    )
    args = parser.parse_args(argv)

    cert_path = Path(args.cert)
    if not cert_path.is_absolute():
        cert_path = ROOT / cert_path
    certificate = json.loads(cert_path.read_text(encoding="utf-8"))
    plan = build_plan(certificate, probe_live=args.probe_live)

    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = ROOT / out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(plan, indent=2), encoding="utf-8")

    print(f"status: {plan['status']}")
    print(f"openapi: {plan['openapi']['title']} {plan['openapi']['version']}")
    present = len(REQUIRED_ENDPOINTS) - len(plan["missing_required_endpoints"])
    print(f"required endpoints present: {present}/{len(REQUIRED_ENDPOINTS)}")
    print(f"request fingerprint: {plan['request_fingerprint'][:24]}...")
    if args.probe_live:
        live_ok = sum(1 for row in plan["live_probes"].values() if row.get("ok"))
        print(f"live probes ok: {live_ok}/{len(plan['live_probes'])}")
    print(f"wrote: {out_path.relative_to(ROOT)}")
    return 0 if plan["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
