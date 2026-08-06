#!/usr/bin/env python3
"""Content-addressed exact verifier for Passes 3871--3886."""
from __future__ import annotations
import base64, bz2, hashlib
from pathlib import Path
SOURCE_SHA256 = "41d21ec652644f85d0649fdd8da8626ea4e1eaf84cc0a4fa3cd3e881d7b15d00"
PAYLOAD_SHA256 = "2a96b8ca6eda49390aaff0ea09bdd4eb40eb15a53b6105d356fc00b4ae1dadfc"
root = Path(__file__).resolve().parent
payload = "".join("".join((root / f"_bt3871_3886_payload_{i}.txt").read_text().split()) for i in (1, 2))
compressed = base64.b85decode(payload.encode("ascii"))
assert hashlib.sha256(compressed).hexdigest() == PAYLOAD_SHA256
source = bz2.decompress(compressed)
assert hashlib.sha256(source).hexdigest() == SOURCE_SHA256
exec(compile(source, "analysis/bt3871_3886_eight_front_closure.readable.py", "exec"), globals())
