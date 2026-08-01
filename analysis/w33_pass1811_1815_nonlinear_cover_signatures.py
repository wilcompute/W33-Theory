#!/usr/bin/env python3
"""Transparent loader for Passes 1811--1815 nonlinear cover signatures."""
import base64,gzip
from pathlib import Path
P=Path(__file__).with_name("pass1811_1815_parts")
blob="".join((P/f"part{i:02d}.b64").read_text().strip() for i in range(1))
source=gzip.decompress(base64.b64decode(blob)).decode()
exec(compile(source,str(Path(__file__).resolve()),"exec"),globals())
