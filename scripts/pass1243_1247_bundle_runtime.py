#!/usr/bin/env python3
"""Hash-verified in-memory runtime for the Pass 1243-1247 exact source bundle.

The reviewed source archive is split across nine small text chunks under ``data/``.
This helper concatenates and verifies those chunks, reads the tar archive entirely
in memory, exposes bundled analysis modules through a narrow import hook, and
executes a selected canonical member without extracting paths to disk.
"""
from __future__ import annotations

import base64
from functools import lru_cache
import hashlib
import importlib.abc
import importlib.util
import io
from pathlib import Path
import sys
import tarfile
from types import ModuleType
from typing import Any, MutableMapping

ROOT = Path(__file__).resolve().parents[1]
PART_GLOB = "pass1243_1247_exact_bundle.part*"
EXPECTED_PARTS = 9
EXPECTED_ARCHIVE_SHA256 = "d2e1e9d4e6c520f8402d831d8bfa563a14f24e8d2ec4cea0faed87f13dca44e4"


@lru_cache(maxsize=1)
def archive_members() -> dict[str, bytes]:
    parts = sorted((ROOT / "data").glob(PART_GLOB))
    if len(parts) != EXPECTED_PARTS:
        raise RuntimeError(f"expected {EXPECTED_PARTS} bundle parts, found {len(parts)}")
    encoded = "".join(path.read_text(encoding="ascii") for path in parts)
    raw = base64.b64decode(encoded, validate=True)
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_ARCHIVE_SHA256:
        raise RuntimeError(f"archive SHA-256 mismatch: {digest}")
    members: dict[str, bytes] = {}
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as archive:
        for member in archive.getmembers():
            name = member.name.removeprefix("./")
            if name.startswith("/") or ".." in Path(name).parts:
                raise RuntimeError(f"unsafe bundle member: {name!r}")
            if not member.isfile():
                continue
            handle = archive.extractfile(member)
            if handle is None:
                raise RuntimeError(f"cannot read bundle member: {name}")
            members[name] = handle.read()
    return members


def read_member(member: str) -> bytes:
    try:
        return archive_members()[member]
    except KeyError as exc:
        raise FileNotFoundError(f"bundle member not found: {member}") from exc


class _BundleModuleLoader(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def find_spec(self, fullname: str, path: object = None, target: ModuleType | None = None):
        if "." in fullname:
            return None
        member = f"analysis/{fullname}.py"
        if member not in archive_members():
            return None
        return importlib.util.spec_from_loader(fullname, self, origin=str(ROOT / member))

    def create_module(self, spec):
        return None

    def exec_module(self, module: ModuleType) -> None:
        member = f"analysis/{module.__name__}.py"
        filename = str(ROOT / member)
        module.__file__ = filename
        source = read_member(member)
        exec(compile(source, filename, "exec"), module.__dict__, module.__dict__)


_IMPORTER = _BundleModuleLoader()


def install_importer() -> None:
    if not any(item is _IMPORTER for item in sys.meta_path):
        sys.meta_path.insert(0, _IMPORTER)


def execute_member(member: str, namespace: MutableMapping[str, Any]) -> None:
    install_importer()
    filename = str(ROOT / member)
    namespace.setdefault("__file__", filename)
    source = read_member(member)
    exec(compile(source, filename, "exec"), namespace, namespace)


if __name__ == "__main__":
    print({
        "status": "PASS",
        "parts": EXPECTED_PARTS,
        "archive_sha256": EXPECTED_ARCHIVE_SHA256,
        "members": sorted(archive_members()),
    })
