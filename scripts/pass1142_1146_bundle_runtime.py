#!/usr/bin/env python3
"""Read and execute one reviewed source member from the Pass 1142-1146 bundle.

The bundle is committed at data/pass1142_1146_source_bundle.b64.  This helper
never extracts paths to disk: it decodes the tar archive in memory, selects one
exact member name, compiles it with the canonical repository filename, and
executes it in the caller's namespace.
"""
from __future__ import annotations

import base64
import io
from pathlib import Path
import tarfile
from typing import MutableMapping, Any

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "data" / "pass1142_1146_source_bundle.b64"


def execute_member(member: str, namespace: MutableMapping[str, Any]) -> None:
    if member.startswith("/") or ".." in Path(member).parts:
        raise ValueError(f"unsafe bundle member: {member!r}")
    raw = base64.b64decode(BUNDLE.read_bytes(), validate=True)
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as archive:
        candidates = (member, f"./{member}")
        handle = None
        for name in candidates:
            try:
                handle = archive.extractfile(name)
            except KeyError:
                continue
            if handle is not None:
                break
        if handle is None:
            raise FileNotFoundError(f"bundle member not found: {member}")
        source = handle.read()
    filename = str(ROOT / member)
    namespace.setdefault("__file__", filename)
    exec(compile(source, filename, "exec"), namespace, namespace)
