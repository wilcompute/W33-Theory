#!/usr/bin/env python3
"""Archive-backed exact verifier for Passes 3821–3828.

The complete implementation is stored in three content-addressed base64 chunks
under ``.bootstrap``. The loader verifies the compressed archive SHA-256,
extracts it into a private temporary directory, points the embedded verifier at
the live repository root, and exposes its public API. Missing, reordered,
corrupted, or partial chunks cannot produce a certificate.
"""
from __future__ import annotations

import atexit
import base64
import hashlib
import os
import runpy
import shutil
import sys
import tarfile
import tempfile
from functools import lru_cache
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_SHA256 = "b296b8c4197e164b7759dde93d77b6a180d0b56fbd054e9791e29d1560ba6b95"
SEMANTIC_SHA256 = "b141dd0f82e4a6b1ee62d1c57f0e92bdfc9f58d3b32515f9521a0175fdca88a1"
CHUNKS = tuple(ROOT / ".bootstrap" / f"pass3821_bundle_{i:02d}.b64" for i in range(3))
TARGET = Path("analysis/w33_pass3821_3828_embedded.py")
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
    _EXTRACTED_ROOT = Path(tempfile.mkdtemp(prefix="w33-pass3821-"))
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
        try:
            bundle.extractall(_EXTRACTED_ROOT, members=members, filter="data")
        except TypeError:
            bundle.extractall(_EXTRACTED_ROOT, members=members)
    embedded = _EXTRACTED_ROOT / TARGET
    if not embedded.is_file():
        raise RuntimeError(f"embedded verifier absent: {TARGET}")
    old_path = list(sys.path)
    old_root = os.environ.get("W33_REPO_ROOT")
    try:
        os.environ["W33_REPO_ROOT"] = str(ROOT)
        sys.path.insert(0, str(_EXTRACTED_ROOT))
        namespace = runpy.run_path(str(embedded), run_name="w33_pass3821_3828_embedded")
    finally:
        sys.path[:] = old_path
        if old_root is None:
            os.environ.pop("W33_REPO_ROOT", None)
        else:
            os.environ["W33_REPO_ROOT"] = old_root
    if "build_certificate" not in namespace or "main" not in namespace:
        raise RuntimeError("embedded verifier lacks required public entry points")
    return namespace


def build_certificate() -> dict[str, object]:
    result = _embedded_globals()["build_certificate"]()
    if result.get("semantic_sha256") != SEMANTIC_SHA256:
        raise RuntimeError("embedded semantic certificate mismatch")
    return result


def main() -> int:
    old_root = os.environ.get("W33_REPO_ROOT")
    try:
        os.environ["W33_REPO_ROOT"] = str(ROOT)
        return int(_embedded_globals()["main"]())
    finally:
        if old_root is None:
            os.environ.pop("W33_REPO_ROOT", None)
        else:
            os.environ["W33_REPO_ROOT"] = old_root


if __name__ == "__main__":
    raise SystemExit(main())
