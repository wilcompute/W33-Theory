#!/usr/bin/env python3
"""Content-addressed loader for Passes 3973-3980 exact verifier."""
from __future__ import annotations
import base64
import hashlib
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARTS = [
    HERE / ".bootstrap/pass3973_source_00.b64",
    HERE / ".bootstrap/pass3973_source_01.b64",
]
COMPRESSED_SHA256 = "9464de8797ae9b4ec6d876f4298db868f068f14a853cd802f5ea4133347e6fe4"
SOURCE_SHA256 = "0fba5345203d56ff4aafc6da7a4ee784dd3091d14e08e486f93cb11b599b8941"
encoded = "".join(path.read_text(encoding="ascii").strip() for path in PARTS)
compressed = base64.b64decode(encoded, validate=True)
if hashlib.sha256(compressed).hexdigest() != COMPRESSED_SHA256:
    raise RuntimeError("Pass 3973 compressed source digest mismatch")
source = zlib.decompress(compressed)
if hashlib.sha256(source).hexdigest() != SOURCE_SHA256:
    raise RuntimeError("Pass 3973 verifier source digest mismatch")
namespace = {"__name__":"w33_pass3973_3980_impl", "__file__":str(Path(__file__).resolve())}
exec(compile(source, str(Path(__file__).resolve()), "exec"), namespace)
build_certificate = namespace["build_certificate"]
canonical_sha = namespace["canonical_sha"]
main = namespace["main"]
if __name__ == "__main__":
    raise SystemExit(main())
