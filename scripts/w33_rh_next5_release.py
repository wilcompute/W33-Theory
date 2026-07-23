#!/usr/bin/env python3
"""Verify or regenerate the five post-Casey RH frontier certificates.

Default mode is read-only and fast. Pass ``--regenerate`` to rerun all five
numerical engines before verification.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE_NAMES = (
    "w33_weil_cocycle_positivity_certificate.json",
    "w33_prime_weight_discovery_certificate.json",
    "w33_infinite_phase_operator_certificate.json",
    "w33_debranges_cocycle_kernel_certificate.json",
    "w33_norm11_local_global_certificate.json",
)


def builders():
    from analysis.w33_debranges_cocycle_kernel import build_certificate as build_debranges
    from analysis.w33_infinite_phase_operator import build_certificate as build_operator
    from analysis.w33_norm11_local_global import build_certificate as build_norm11
    from analysis.w33_prime_weight_discovery import build_certificate as build_prime
    from analysis.w33_weil_cocycle_positivity import build_certificate as build_weil

    return dict(
        zip(
            CERTIFICATE_NAMES,
            (build_weil, build_prime, build_operator, build_debranges, build_norm11),
        )
    )


def verify_payload(filename: str, payload: dict) -> dict:
    checks = payload.get("checks", {})
    if payload.get("status") != "PASS" or not checks or not all(checks.values()):
        raise SystemExit(f"{filename}: certificate failed")
    return {"status": "PASS", "check_count": len(checks)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--regenerate", action="store_true")
    args = parser.parse_args()

    output_dir = ROOT / "data"
    output_dir.mkdir(parents=True, exist_ok=True)
    build_map = builders() if args.regenerate else {}
    summary = {}

    for filename in CERTIFICATE_NAMES:
        path = output_dir / filename
        if args.regenerate:
            payload = build_map[filename]()
            path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        else:
            payload = json.loads(path.read_text(encoding="utf-8"))
        summary[filename] = verify_payload(filename, payload)
        print(f"[PASS] {filename}: {summary[filename]['check_count']} checks")

    summary_path = output_dir / "w33_rh_next5_release_summary.json"
    summary_path.write_text(
        json.dumps({"status": "PASS", "certificates": summary}, indent=2),
        encoding="utf-8",
    )
    print(f"wrote {summary_path}")


if __name__ == "__main__":
    main()
