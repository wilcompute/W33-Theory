#!/usr/bin/env python3
"""Collision-safe entrypoint for Passes 3769-3786.

The exhaustive implementation was published immediately before a parallel
agent occupied Passes 3751-3758.  This entrypoint executes that exact source,
retags the certificate into the clean 3769-3786 namespace, and recomputes the
content-addressed semantic hash.  No mathematical result is copied by hand.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATION = ROOT / "analysis" / "w33_pass3751_3768_gq_veldkamp_axial_lattice_monster.py"
OUTPUT = ROOT / "data" / "PART_3769_3786_GQ_VELDKAMP_AXIAL_LATTICE_MONSTER_results.json"
OLD_HASH = "f401d08e08c1f5898d363e2e371bfffb9ec0227b18486de4e9a4c72109d47b0b"
NEW_HASH = "8d3f383e362f30e58d8c482f48e2ac2b77414922366ba8053633859d6206313a"


def build():
    module = runpy.run_path(str(IMPLEMENTATION))
    result = module["build"]()
    assert result["semantic_sha256"] == OLD_HASH
    result["schema"] = "w33.pass3769_3786.gq_veldkamp_axial_lattice_monster.v1"
    result.pop("semantic_sha256")
    semantic = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["semantic_sha256"] = sha256(semantic).hexdigest()
    assert result["semantic_sha256"] == NEW_HASH
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    result = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("PASS_3769_3786", result["semantic_sha256"])


if __name__ == "__main__":
    main()
