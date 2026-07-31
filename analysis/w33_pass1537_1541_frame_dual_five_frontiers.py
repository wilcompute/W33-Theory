#!/usr/bin/env python3
"""Transparent loader for the exact Passes 1537-1541 verifier.

The source is split into plain-text fragments only to keep GitHub connector
writes reviewable. The fragments are concatenated byte-for-byte and compiled
under this canonical filename; there is no generated or hidden logic.
"""
from pathlib import Path

_PARTS = Path(__file__).with_name("pass1537_1541_parts")
_SOURCE = "".join(path.read_text() for path in sorted(_PARTS.glob("part*.pyfrag")))
exec(compile(_SOURCE, __file__, "exec"), globals())
