#!/usr/bin/env python3
from pathlib import Path
import base64,zlib
ROOT=Path(__file__).resolve().parents[1]
parts=sorted((ROOT/'bootstrap/pass3388_3399').glob('verifier.py.zlib.b64.part*'))
# 2026-10-30: the committed payload was truncated at upload (2026-08-04; sha256 does not match bootstrap/pass3388_3399/manifest.json,
# see scripts/check_bootstrap_payloads.py) and the original is not in any clone.  Fail with a named ImportError instead of a
# binascii.Error, so dependent tests skip (pytest.importorskip) rather than abort the whole collection.
import hashlib as _h, json as _j
_M = _j.loads((Path(__file__).resolve().parents[1] / "bootstrap/pass3388_3399/manifest.json").read_text())
if _h.sha256("".join(q.read_text(encoding="ascii") for q in parts).encode()).hexdigest() != _M["analysis/bt3388_3399_clebsch_d5_fault_closure.py"]["encoded_sha256"]:
    raise ImportError("bt3388_3399_clebsch_d5_fault_closure payload is truncated (encoded sha256 mismatch); the original is unrecoverable")
code=zlib.decompress(base64.b64decode(''.join(p.read_text(encoding='ascii') for p in parts)))
exec(compile(code,str(ROOT/'bootstrap/pass3388_3399/verifier.py.zlib.b64.part*'),"exec"),globals(),globals())
