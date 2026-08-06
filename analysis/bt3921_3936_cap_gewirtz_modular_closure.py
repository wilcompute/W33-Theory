#!/usr/bin/env python3
"""Content-addressed exact verifier for Passes 3921--3936."""
from __future__ import annotations
import base64,bz2,hashlib
from pathlib import Path
SOURCE_SHA256="ae8bb316ac29731fc387eeb437885c45b6123c801be664449153abfe4cb87d82"
PAYLOAD_SHA256="4362466552f00ca9fba91b669e869bfbeb683b4889c2c5cbeb62fd270846d6ec"
root=Path(__file__).resolve().parent
payload="".join("".join((root/f"_bt3921_3936_payload_{i}.txt").read_text().split()) for i in range(1,3))
compressed=base64.b85decode(payload.encode("ascii"))
assert hashlib.sha256(compressed).hexdigest()==PAYLOAD_SHA256
source=bz2.decompress(compressed)
assert hashlib.sha256(source).hexdigest()==SOURCE_SHA256
exec(compile(source,"analysis/bt3921_3936_cap_gewirtz_modular_closure.readable.py","exec"),globals())
