#!/usr/bin/env python3
"""Content-addressed loader for the exact Passes 3913-3920 verifier."""
import base64
import hashlib
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / "data" / "PART_3913_3920_SOURCE.parts"
encoded = "".join(p.read_text().strip() for p in sorted(PARTS.glob("part*.b85")))
compressed = base64.b85decode(encoded.encode())
assert hashlib.sha256(compressed).hexdigest() == "9223a454686c6a805af06f02c082af45ee0e4f8fc81f31d13a75c6df44403da9"
source = zlib.decompress(compressed)
assert hashlib.sha256(source).hexdigest() == "4340cdebef01ed02fd6d640263ccac115e37eb5267ed60bebc422be755f686c9"
exec(compile(source, __file__, "exec"), globals(), globals())
