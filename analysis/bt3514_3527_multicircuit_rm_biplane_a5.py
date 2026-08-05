#!/usr/bin/env python3
from pathlib import Path
import base64,zlib
ROOT=Path(__file__).resolve().parents[1]
parts=sorted((ROOT/'bootstrap/pass3514_3527').glob('verifier.*.zlib.b64'))
code=zlib.decompress(base64.b64decode(''.join(p.read_text().strip() for p in parts)))
exec(compile(code,str(parts[0]),'exec'),globals(),globals())
