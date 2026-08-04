#!/usr/bin/env python3
from __future__ import annotations
import base64
import zlib
from pathlib import Path

root = Path(__file__).resolve().parent
payload = ''.join((root / f'materializer.b64.{i:02d}').read_text(encoding='ascii').strip() for i in range(5))
source = zlib.decompress(base64.b64decode(payload))
exec(compile(source, str(root / 'embedded_materializer.py'), 'exec'), {'__name__': '__main__'})
