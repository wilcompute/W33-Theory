#!/usr/bin/env python3
"""Transparent loader for Passes 1701--1705 exact verifier fragments."""
import base64, gzip
from pathlib import Path
PARTS = Path(__file__).with_name("pass1701_1705_parts")
source = (PARTS / "part00.pyfrag").read_text() + (PARTS / "part01.pyfrag").read_text()
source += gzip.decompress(base64.b64decode((PARTS / "remainder.pyfrag.gz.b64").read_text())).decode()
exec(compile(source, str(Path(__file__).resolve()), "exec"), globals())
