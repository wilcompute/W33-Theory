#!/usr/bin/env python3
from pathlib import Path
import base64,hashlib,json,zlib
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
m=json.loads((HERE/'manifest.json').read_text())
chunks=sorted(HERE.glob('chunk_*.b85'))
assert len(chunks)==m['chunks'],(len(chunks),m['chunks'])
enc=''.join(p.read_text().strip() for p in chunks)
assert hashlib.sha256(enc.encode()).hexdigest()==m['encoded_sha256']
payload=zlib.decompress(base64.b85decode(enc.encode()))
assert hashlib.sha256(payload).hexdigest()==m['payload_sha256']
obj=json.loads(payload)
assert set(obj)==set(m['files'])
for rel,text in obj.items():
 p=ROOT/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
 assert hashlib.sha256(p.read_bytes()).hexdigest()==m['files'][rel],rel
print(f"PASS {len(obj)}/{len(obj)} materialized hashes")
