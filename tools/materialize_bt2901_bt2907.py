#!/usr/bin/env python3
"""Materialize the readable Passes 2901--2907 release packet atomically."""
from __future__ import annotations
import base64, hashlib, json, zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / "tools" / "pass2901_2907_payload"


def main() -> None:
    payload = "".join(path.read_text(encoding="utf-8") for path in sorted(PARTS.glob("part*.txt")))
    bundle = json.loads(zlib.decompress(base64.b85decode(payload.encode())).decode())
    assert bundle["schema"] == "w33.pass2901_2907.bundle.v1"
    changed = []
    for entry in bundle["files"]:
        path = ROOT / entry["path"]
        content = entry["content"].encode()
        if hashlib.sha256(content).hexdigest() != entry["sha256"]:
            raise SystemExit(f"embedded digest mismatch: {entry['path']}")
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists() and path.read_bytes() == content:
            continue
        if path.exists():
            raise SystemExit(f"refusing to overwrite divergent file: {entry['path']}")
        path.write_bytes(content)
        changed.append(entry["path"])
    print("materialized:", ", ".join(changed) if changed else "none")


if __name__ == "__main__":
    main()
