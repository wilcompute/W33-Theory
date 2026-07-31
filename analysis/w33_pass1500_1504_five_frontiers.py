#!/usr/bin/env python3
"""Canonical exact workers for Passes 1500--1504."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CERTIFICATE = ROOT / "data" / "w33_pass1500_1504_five_frontiers.json"
WORKERS = ("1500", "1501", "1502", "1503", "1504")
EXPECTED_SHA256 = {
    "1500": "ccdc1e773121897bf87c03d7eaf40dd46b9daf0272f45b779c76fba643f6f3e6",
    "1501": "45ffc89206d187b1d6ed8bf6d74f19580ec6aaf8e89fe76d2145b1e53bd4add2",
    "1502": "cf30ef9d35441f22a1cb39380fb3bcdd00ae73cf592d2b7b337a0d4823b1b564",
    "1503": "c96cd9f52681256db4795e1c17fc8352951fa11f02a0d354d2b0efe52611328d",
    "1504": "60105b7a9d3b73cc714d5b828c5a9a6296af0fa383247884ba109ee60c137956",
}


def run_worker(worker: str) -> dict:
    from pass1500_1504 import (
        bridge_classification, linking_algebra, local_overorders, modular_ext, tensor_fourier
    )
    fn = {
        "1500": modular_ext.analyze,
        "1501": tensor_fourier.analyze,
        "1502": bridge_classification.analyze,
        "1503": local_overorders.analyze,
        "1504": linking_algebra.analyze,
    }[worker]
    result = fn()
    assert result["theorem"].startswith(f"Pass {worker} ")
    assert result["sha256"] == EXPECTED_SHA256[worker]
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", choices=WORKERS)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--certificate", type=Path, default=DEFAULT_CERTIFICATE)
    args = parser.parse_args()

    if args.worker:
        result = run_worker(args.worker)
        output = args.output or ROOT / "data" / f"pass{args.worker}.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(f"PASS {args.worker} sha256={result['sha256']}")
        return

    if args.check:
        frozen = json.loads(args.certificate.read_text())
        assert frozen["schema"] == "w33.pass1500_1504.five_frontiers.v1"
        assert frozen["status"] == "PASS"
        assert frozen["worker_sha256"] == EXPECTED_SHA256
        digest = hashlib.sha256(args.certificate.read_bytes()).hexdigest()
        print(f"PASS 1500-1504 frozen certificate sha256={digest}")
        return

    raise SystemExit("Use --worker or --check")


if __name__ == "__main__":
    main()
