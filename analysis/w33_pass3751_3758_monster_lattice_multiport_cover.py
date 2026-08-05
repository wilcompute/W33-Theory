#!/usr/bin/env python3
"""Archive-backed exact verifier for Passes 3751–3758.

The complete implementation is stored in five content-addressed base64 chunks
under ``.bootstrap/``.  This loader verifies the compressed archive SHA-256,
extracts it into a temporary directory, verifies that the embedded verifier is
not this loader, and executes the embedded source with the original arguments.

This layout is deliberately fail-closed: missing, reordered, corrupted, or
partially published chunks cannot produce a result.
"""
from __future__ import annotations

import base64
import hashlib
import runpy
import sys
import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_SHA256 = "649f8fd872b2fdd4da02d8a37fdc5fc23eb9aa53ed8a0678d3e707df5daac512"
SEMANTIC_SHA256 = "6271dafcc58467d6e758cdbcc9a1b220fe21693b3ace3c727fb5b5499be60ce6"
CHUNKS = tuple(ROOT / ".bootstrap" / f"pass3751_bundle_{i:02d}.b64" for i in range(5))
TARGET = Path("analysis/w33_pass3751_3758_monster_lattice_multiport_cover.py")


def _load_archive() -> bytes:
    missing = [str(path.relative_to(ROOT)) for path in CHUNKS if not path.is_file()]
    if missing:
        raise SystemExit(f"missing content-addressed source chunks: {missing}")
    try:
        encoded = b"".join(path.read_bytes().strip() for path in CHUNKS)
        archive = base64.b64decode(encoded, validate=True)
    except Exception as exc:
        raise SystemExit(f"invalid source-archive encoding: {exc}") from exc
    digest = hashlib.sha256(archive).hexdigest()
    if digest != ARCHIVE_SHA256:
        raise SystemExit(f"source archive SHA-256 mismatch: {digest}")
    return archive


def main() -> int:
    archive = _load_archive()
    with tempfile.TemporaryDirectory(prefix="w33-pass3751-") as tmp:
        tmp_root = Path(tmp)
        archive_path = tmp_root / "packet.tgz"
        archive_path.write_bytes(archive)
        with tarfile.open(archive_path, "r:gz") as bundle:
            members = bundle.getmembers()
            for member in members:
                destination = (tmp_root / member.name).resolve()
                if tmp_root.resolve() not in destination.parents and destination != tmp_root.resolve():
                    raise SystemExit(f"unsafe archive member: {member.name}")
            bundle.extractall(tmp_root, members=members)
        embedded = tmp_root / TARGET
        if not embedded.is_file():
            raise SystemExit(f"embedded verifier absent: {TARGET}")
        if embedded.read_bytes() == Path(__file__).read_bytes():
            raise SystemExit("embedded verifier unexpectedly equals archive loader")
        old_argv = sys.argv
        old_path = list(sys.path)
        try:
            sys.argv = [str(embedded), *old_argv[1:]]
            sys.path.insert(0, str(tmp_root))
            runpy.run_path(str(embedded), run_name="__main__")
        finally:
            sys.argv = old_argv
            sys.path[:] = old_path
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
