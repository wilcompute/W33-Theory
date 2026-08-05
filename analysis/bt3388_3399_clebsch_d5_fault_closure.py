#!/usr/bin/env python3
from pathlib import Path
import base64,zlib
ROOT=Path(__file__).resolve().parents[1]
parts=sorted((ROOT/'bootstrap/pass3388_3399').glob('verifier.py.zlib.b64.part*'))
code=zlib.decompress(base64.b64decode(''.join(p.read_text(encoding='ascii') for p in parts)))
exec(compile(code,str(ROOT/'bootstrap/pass3388_3399/verifier.py.zlib.b64.part*'),"exec"),globals(),globals())
