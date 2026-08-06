#!/usr/bin/env python3
"""Content-addressed exact verifier for Passes 3913--3928."""
from __future__ import annotations
import base64,bz2,hashlib
from pathlib import Path
SOURCE_SHA256="b6a1cd166f5886bd71866f09effe596a40475ed4587d3a906faf7c2bb4421cbf"
PAYLOAD_SHA256="c397cb88d371ad52de66cfa81ba1633ddce2f9a21024033f27a92650fbad6020"
root=Path(__file__).resolve().parent
payload="".join("".join((root/f"_bt3913_3928_payload_{i}.txt").read_text().split()) for i in range(1,3))
compressed=base64.b85decode(payload.encode("ascii"))
assert hashlib.sha256(compressed).hexdigest()==PAYLOAD_SHA256
source=bz2.decompress(compressed)
assert hashlib.sha256(source).hexdigest()==SOURCE_SHA256
exec(compile(source,"analysis/bt3913_3928_cap_gewirtz_modular_closure.readable.py","exec"),globals())
