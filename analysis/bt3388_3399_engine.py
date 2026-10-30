#!/usr/bin/env python3
from pathlib import Path
import base64,zlib
PAYLOAD=Path(__file__).resolve().parents[1]/"bootstrap/pass3388_3399/engine.py.zlib.b64"
# 2026-10-30: the committed payload was truncated at upload (2026-08-04; sha256 does not match bootstrap/pass3388_3399/manifest.json,
# see scripts/check_bootstrap_payloads.py) and the original is not in any clone.  Fail with a named ImportError instead of a
# binascii.Error, so dependent tests skip (pytest.importorskip) rather than abort the whole collection.
import hashlib as _h, json as _j
_M = _j.loads((Path(__file__).resolve().parents[1] / "bootstrap/pass3388_3399/manifest.json").read_text())
if _h.sha256(PAYLOAD.read_text(encoding="ascii").encode()).hexdigest() != _M["analysis/bt3388_3399_engine.py"]["encoded_sha256"]:
    raise ImportError("bt3388_3399_engine payload is truncated (encoded sha256 mismatch); the original verifier is unrecoverable")
code=zlib.decompress(base64.b64decode(PAYLOAD.read_text(encoding="ascii")))
exec(compile(code,str(PAYLOAD),"exec"),globals(),globals())
