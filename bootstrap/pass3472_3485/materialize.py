#!/usr/bin/env python3
import base64,hashlib,io,json,tarfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
M=json.loads((HERE/'manifest.json').read_text())
enc=b''.join((HERE/f'payload_{i:02d}.part').read_bytes() for i in range(M['parts'])).decode()
assert hashlib.sha256(enc.encode()).hexdigest()==M['encoded_sha256']
payload=base64.b64decode(enc);assert hashlib.sha256(payload).hexdigest()==M['payload_sha256']
with tarfile.open(fileobj=io.BytesIO(payload),mode='r:gz') as tf:
 for member in tf.getmembers():
  p=Path(member.name);assert not p.is_absolute() and '..' not in p.parts
  data=tf.extractfile(member).read();assert hashlib.sha256(data).hexdigest()==M['files'][member.name]
  target=ROOT/member.name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
for f,h in M['files'].items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h
print('PASS_MATERIALIZED_PASS3472_3485',len(M['files']))
