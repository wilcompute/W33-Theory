#!/usr/bin/env python3
"""Executable loader for the transparent Pass 1365--1369 source fragments."""
from pathlib import Path

_SOURCE_DIR = Path(__file__).with_suffix(".src")
_SOURCE = "".join(
    (_SOURCE_DIR / f"part{index:02d}.pyfrag").read_text()
    for index in range(5)
)
exec(compile(_SOURCE, str(Path(__file__)), "exec"), globals(), globals())
