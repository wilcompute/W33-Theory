#!/usr/bin/env python3
"""Canonical Passes 1380--1384 wrapper for the exact Mackey verifier.

The exhaustive implementation is retained in `_mackey_selector_decomposition_impl`
so its remotely observed execution remains byte-identifiable. This wrapper only
renames the provisional result keys after a parallel namespace collision; no
mathematical computation or invariant is changed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import _mackey_selector_decomposition_impl as implementation

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / "data" / "w33_pass1380_1384_mackey_selector_decomposition_full.json"
KEY_MAP = {
    "pass1375_little_group_character_table": "pass1380_little_group_character_table",
    "pass1376_selector_permutation_character": "pass1381_selector_permutation_character",
    "pass1377_mackey_wedderburn_identification": "pass1382_mackey_wedderburn_identification",
    "pass1378_terwilliger_fusion_explanation": "pass1383_terwilliger_fusion_explanation",
    "pass1379_boundary": "pass1384_boundary",
}


def analyze():
    provisional = implementation.analyze()
    result = {
        "schema": "w33.pass1380_1384.mackey_selector_decomposition.v1",
        "status": provisional["status"],
    }
    for old, new in KEY_MAP.items():
        result[new] = provisional[old]
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    result = analyze()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    digest = hashlib.sha256(encoded.encode()).hexdigest()
    if args.check:
        if not args.output.exists() or args.output.read_text() != encoded:
            raise SystemExit(f"certificate drift: {args.output}")
    elif not args.verify_only:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded)
    print(f"PASS 1380-1384: Mackey selector decomposition sha256={digest}")


if __name__ == "__main__":
    main()
