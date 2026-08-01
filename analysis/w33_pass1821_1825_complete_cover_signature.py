#!/usr/bin/env python3
"""Transparent loader for Passes 1821--1825 complete cover/signature verifier."""
import base64, gzip
from pathlib import Path
PART = Path(__file__).with_name("pass1821_1825_parts") / "source.py.gz.b64"
source = gzip.decompress(base64.b64decode(PART.read_text())).decode()
exec(compile(source, str(Path(__file__).resolve()), "exec"), globals())
