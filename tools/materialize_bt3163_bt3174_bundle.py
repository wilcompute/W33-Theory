#!/usr/bin/env python3
"""Materialize the byte-verified Passes 3163-3174 source bundle."""
from __future__ import annotations
import base64
import json
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS = sorted((ROOT / "data" / "bt3163_3174_bundle").glob("chunk_*.b85"))
EXPECTED_PARTS = 9
EXPECTED_FILES = 32


def main() -> int:
    if len(PARTS) != EXPECTED_PARTS:
        raise RuntimeError(f"expected {EXPECTED_PARTS} chunks, found {len(PARTS)}")
    payload = "".join(p.read_text(encoding="ascii") for p in PARTS)
    files = json.loads(zlib.decompress(base64.b85decode(payload)).decode("utf-8"))
    if len(files) != EXPECTED_FILES:
        raise RuntimeError(f"expected {EXPECTED_FILES} files, found {len(files)}")
    for rel, encoded in sorted(files.items()):
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(base64.b64decode(encoded))
    print(f"materialized {len(files)} Pass3163-3174 files from {len(PARTS)} chunks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
