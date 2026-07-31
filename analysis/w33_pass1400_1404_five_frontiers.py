#!/usr/bin/env python3
"""Canonical Passes 1400--1404 wrapper over the collision-neutral exact workers."""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import _selector_five_frontiers_impl as impl

DEFAULT_OUT = ROOT / "data" / "w33_pass1400_1404_five_frontiers.json"
MAP = {"1400":"1390", "1401":"1391", "1402":"1392", "1403":"1393", "1404":"1394"}

def canonicalize(result, public_id, internal_id):
    out = copy.deepcopy(result)
    if "theorem" in out:
        out["theorem"] = out["theorem"].replace(f"Pass {internal_id}", f"Pass {public_id}")
    out["internal_worker"] = internal_id
    out["canonical_pass"] = public_id
    out.pop("sha256", None)
    out["sha256"] = impl.sha(out)
    return out

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", choices=tuple(MAP))
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.worker:
        internal = MAP[args.worker]
        result = canonicalize(impl.run_worker(internal), args.worker, internal)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(f"PASS {args.worker} sha256={result['sha256']}")
        return
    if args.check:
        frozen = json.loads(args.output.read_text())
        assert frozen["schema"] == "w33.pass1400_1404.five_frontiers.v1"
        assert frozen["status"] == "PASS"
        print("PASS 1400-1404 frozen certificate", hashlib.sha256(args.output.read_bytes()).hexdigest())
        return
    raise SystemExit("Use --worker or --check")

if __name__ == "__main__":
    main()
