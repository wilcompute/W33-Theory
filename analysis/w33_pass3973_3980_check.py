#!/usr/bin/env python3
"""Rebuild and verify the compressed Passes 3973-3980 certificates."""
from __future__ import annotations
import base64
import hashlib
import importlib.util
import json
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "analysis/w33_pass3973_3980_extremal_mesh_photon_tensor_monster.py"
CERT_PARTS = [
    ROOT / "data/.bootstrap/PART_3973_3980_CERT_00.b64",
    ROOT / "data/.bootstrap/PART_3973_3980_CERT_01.b64",
]
TENSOR_PATH = ROOT / "data/.bootstrap/PART_3973_3980_RANK48_TENSOR.b64"
MANIFEST = json.loads((ROOT / "data/PART_3973_3980_EXTREMAL_MESH_PHOTON_TENSOR_manifest.json").read_text(encoding="utf-8"))

def unpack(parts, compressed_sha, json_sha):
    encoded = "".join(path.read_text(encoding="ascii").strip() for path in parts)
    compressed = base64.b64decode(encoded, validate=True)
    assert hashlib.sha256(compressed).hexdigest() == compressed_sha
    raw = zlib.decompress(compressed)
    assert hashlib.sha256(raw).hexdigest() == json_sha
    return json.loads(raw)

def main():
    frozen = unpack(CERT_PARTS, MANIFEST["certificate"]["compressed_sha256"], MANIFEST["certificate"]["json_sha256"])
    tensor = unpack([TENSOR_PATH], MANIFEST["rank48_tensor"]["compressed_sha256"], MANIFEST["rank48_tensor"]["json_sha256"])
    spec = importlib.util.spec_from_file_location("pass3973", SOURCE)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rebuilt = module.build_certificate(ROOT)
    assert json.loads(json.dumps(rebuilt, sort_keys=True)) == frozen
    assert rebuilt["semantic_sha256"] == MANIFEST["semantic_sha256"]
    current_tensor = rebuilt["pass3976_rank48_literal_tensor"]
    assert tensor["tensor_sha256"] == current_tensor["tensor_sha256"]
    assert tensor["tensor_entries"] == current_tensor["tensor_entries"]
    print("PASS_3973_3980", rebuilt["semantic_sha256"], len(tensor["tensor_entries"]))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
