#!/usr/bin/env python3
"""Archive-backed exact verifier for Passes 3751–3758.

The complete implementation is stored in five content-addressed base64 chunks
under ``.bootstrap/``. This loader verifies the compressed archive SHA-256,
extracts the full packet into a private temporary directory, and exposes the
embedded verifier's public functions. Missing, reordered, corrupted, or partial
chunks cannot produce a result.
"""
from __future__ import annotations

import atexit
import base64
import hashlib
import runpy
import shutil
import sys
import tarfile
import tempfile
from functools import lru_cache
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_SHA256 = "649f8fd872b2fdd4da02d8a37fdc5fc23eb9aa53ed8a0678d3e707df5daac512"
SEMANTIC_SHA256 = "6271dafcc58467d6e758cdbcc9a1b220fe21693b3ace3c727fb5b5499be60ce6"
CHUNKS = tuple(ROOT / ".bootstrap" / f"pass3751_bundle_{i:02d}.b64" for i in range(5))
TARGET = Path("analysis/w33_pass3751_3758_monster_lattice_multiport_cover.py")
_EXTRACTED_ROOT: Path | None = None


def _load_archive() -> bytes:
    missing = [str(path.relative_to(ROOT)) for path in CHUNKS if not path.is_file()]
    if missing:
        raise RuntimeError(f"missing content-addressed source chunks: {missing}")
    try:
        encoded = b"".join(path.read_bytes().strip() for path in CHUNKS)
        archive = base64.b64decode(encoded, validate=True)
    except Exception as exc:
        raise RuntimeError(f"invalid source-archive encoding: {exc}") from exc
    digest = hashlib.sha256(archive).hexdigest()
    if digest != ARCHIVE_SHA256:
        raise RuntimeError(f"source archive SHA-256 mismatch: {digest}")
    return archive


def _cleanup() -> None:
    global _EXTRACTED_ROOT
    if _EXTRACTED_ROOT is not None:
        shutil.rmtree(_EXTRACTED_ROOT, ignore_errors=True)
        _EXTRACTED_ROOT = None


@lru_cache(maxsize=1)
def _embedded_globals() -> dict[str, Any]:
    global _EXTRACTED_ROOT
    archive = _load_archive()
    _EXTRACTED_ROOT = Path(tempfile.mkdtemp(prefix="w33-pass3751-"))
    atexit.register(_cleanup)
    archive_path = _EXTRACTED_ROOT / "packet.tgz"
    archive_path.write_bytes(archive)
    with tarfile.open(archive_path, "r:gz") as bundle:
        members = bundle.getmembers()
        root = _EXTRACTED_ROOT.resolve()
        for member in members:
            destination = (_EXTRACTED_ROOT / member.name).resolve()
            if destination != root and root not in destination.parents:
                raise RuntimeError(f"unsafe archive member: {member.name}")
        bundle.extractall(_EXTRACTED_ROOT, members=members)
    embedded = _EXTRACTED_ROOT / TARGET
    if not embedded.is_file():
        raise RuntimeError(f"embedded verifier absent: {TARGET}")
    if embedded.read_bytes() == Path(__file__).read_bytes():
        raise RuntimeError("embedded verifier unexpectedly equals archive loader")
    old_path = list(sys.path)
    try:
        sys.path.insert(0, str(_EXTRACTED_ROOT))
        namespace = runpy.run_path(str(embedded), run_name="w33_pass3751_3758_embedded")
    finally:
        sys.path[:] = old_path
    if "build_certificate" not in namespace or "main" not in namespace:
        raise RuntimeError("embedded verifier lacks required public entry points")
    return namespace


def build_certificate() -> dict[str, object]:
    """Execute and return the exact embedded certificate."""
    return _embedded_globals()["build_certificate"]()


def main() -> int:
    """Delegate the CLI to the exact embedded verifier."""
    return int(_embedded_globals()["main"]())


if __name__ == "__main__":
    raise SystemExit(main())
