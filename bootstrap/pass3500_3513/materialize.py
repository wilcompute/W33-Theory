#!/usr/bin/env python3
from pathlib import Path
import base64,zlib,hashlib,json
ROOT=Path(__file__).resolve().parents[2]
BOOT=ROOT/'bootstrap/pass3500_3513'
manifest=json.loads((BOOT/'manifest.json').read_text())
for stem,target,key in [
 ('verifier',BOOT/'verifier.py','source_sha256'),
 ('results',ROOT/'data/PART_BT3500_BT3513_MULTICIRCUIT_RM_BIPLANE_A5_results.json','results_sha256'),
]:
 parts=sorted(BOOT.glob(f'{stem}.*.zlib.b64'))
 raw=zlib.decompress(base64.b64decode(''.join(p.read_text().strip() for p in parts)))
 assert hashlib.sha256(raw).hexdigest()==manifest[key]
 target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
print('PASS materialized Passes 3500-3513 source and results')
