#!/usr/bin/env python3
"""Canonical frozen-certificate check for Passes 3957-3964."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--frozen", type=Path, default=Path("data/PART_3957_3964_EXACT_ALGEBRA_MESH_CODE_PHOTON_results.json"))
    args = parser.parse_args()
    source = args.root / "analysis/w33_pass3957_3964_exact_algebra_mesh_code_photon.py"
    spec = importlib.util.spec_from_file_location("pass3957", source)
    if spec is None or spec.loader is None:
        raise SystemExit("cannot load exact verifier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    generated = json.loads(json.dumps(module.build_certificate(args.root), sort_keys=True))
    frozen_path = args.frozen if args.frozen.is_absolute() else args.root / args.frozen
    frozen = json.loads(frozen_path.read_text(encoding="utf-8"))
    if generated != frozen:
        raise SystemExit("certificate mismatch")
    print(f"PASS {generated['semantic_sha256']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
