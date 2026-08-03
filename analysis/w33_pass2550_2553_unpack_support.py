#!/usr/bin/env python3
import base64,io,tarfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=''.join((ROOT/f'data/w33_pass2550_2553_support.part{i}.b64').read_text().strip() for i in range(1,4))
with tarfile.open(fileobj=io.BytesIO(base64.b64decode(s)),mode='r:gz') as t:
 t.extractall(ROOT,filter='data'); n=len(t.getmembers())
print('materialized',n,'support artifacts')
