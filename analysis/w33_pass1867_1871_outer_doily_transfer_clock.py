#!/usr/bin/env python3
"""Canonical Passes 1867-1871 outer-doily transfer-clock entry point.

The implementation was first published seconds after a parallel track reserved
Passes 1861-1866.  This wrapper moves the theorem to its collision-free
namespace without duplicating the exact matrix construction.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATION = ROOT / "analysis" / "w33_pass1861_1865_outer_doily_transfer_clock.py"


def load_implementation():
    spec = importlib.util.spec_from_file_location("outer_doily_transfer_clock_core", IMPLEMENTATION)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(output: Path | None = None) -> dict:
    result = load_implementation().main(None)
    result["schema"] = "w33.pass1867_1871.outer_doily_transfer_clock.v1"
    result.pop("sha256_without_hash_field", None)
    canonical = json.dumps(result, indent=2, sort_keys=True) + "\n"
    result["sha256_without_hash_field"] = hashlib.sha256(canonical.encode()).hexdigest()
    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


if __name__ == "__main__":
    output_path = ROOT / "data" / "w33_pass1867_1871_outer_doily_transfer_clock.json"
    result = main(output_path)
    print(json.dumps({
        "status": result["status"],
        "n_verified": result["n_verified"],
        "n_checks": result["n_checks"],
        "rank": result["rank"],
        "rank_mod2": result["rank_mod2"],
        "characteristic_polynomial": result["characteristic_polynomial"],
        "balanced_clock": result["balanced_clock"],
        "sha256_without_hash_field": result["sha256_without_hash_field"],
    }, indent=2))
