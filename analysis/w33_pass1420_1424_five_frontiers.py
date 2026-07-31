#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from pass1410_1414 import bridge_classification, linking_algebra, local_overorders, modular_ext, tensor_fourier

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "data" / "w33_pass1420_1424_five_frontiers.json"
WORKERS = ("1420", "1421", "1422", "1423", "1424")


def run_worker(worker):
    return {
        "1420": modular_ext.analyze,
        "1421": tensor_fourier.analyze,
        "1422": bridge_classification.analyze,
        "1423": local_overorders.analyze,
        "1424": linking_algebra.analyze,
    }[worker]()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", choices=WORKERS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.worker:
        result = run_worker(args.worker)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(f"PASS {args.worker} sha256={result['sha256']}")
        return
    if args.check:
        frozen = json.loads(args.output.read_text())
        assert frozen["schema"] == "w33.pass1420_1424.five_frontiers.v1"
        assert frozen["status"] == "PASS"
        print("PASS 1420-1424 frozen certificate", hashlib.sha256(args.output.read_bytes()).hexdigest())
        return
    raise SystemExit("Use --worker or --check")


if __name__ == "__main__":
    main()
