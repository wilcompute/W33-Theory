#!/usr/bin/env python3
from pathlib import Path
import base64,hashlib,json,zlib
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
manifest=json.loads((HERE/'manifest.json').read_text())
chunks=sorted(HERE.glob('chunk_*.b85'))
assert len(chunks)==manifest['chunks']
enc=''.join(x.read_text().strip() for x in chunks)
assert hashlib.sha256(enc.encode()).hexdigest()==manifest['encoded_sha256']
payload=zlib.decompress(base64.b85decode(enc.encode()))
assert hashlib.sha256(payload).hexdigest()==manifest['payload_sha256']
data=json.loads(payload)
assert data['schema']=='w33.pass3262_3273.bundle.v1'
for path,text in data['files'].items():
    target=ROOT/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)
    assert hashlib.sha256(target.read_bytes()).hexdigest()==manifest['files'][path]
print(f"materialized {len(data['files'])} files")
