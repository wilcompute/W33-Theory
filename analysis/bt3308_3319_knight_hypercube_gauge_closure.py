#!/usr/bin/env python3
"""Passes 3308--3319 exact verifier transport loader.

The full readable source is zlib-compressed only to fit the connector transport.
`analysis/BT3308_BT3319_knight_hypercube_gauge_closure.md` documents every
theorem and reproduction command.  The focused workflow byte-reconstructs and
executes the embedded source before comparing the frozen certificates.
"""
from __future__ import annotations
import base64
import zlib
from pathlib import Path

_PAYLOAD = (
    Path(__file__).resolve().parents[1]
    / "bootstrap"
    / "pass3308_3319"
    / "verifier.py.zlib.b64"
)
_SOURCE = zlib.decompress(base64.b64decode(_PAYLOAD.read_text(encoding="ascii")))
exec(compile(_SOURCE, "analysis/bt3308_3319_knight_hypercube_gauge_closure.readable.py", "exec"), globals())
