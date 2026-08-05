#!/usr/bin/env python3
from __future__ import annotations
import argparse,base64,hashlib,json,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
MANIFEST=json.loads((ROOT/'bootstrap/pass3388_3399/manifest.json').read_text())
def encoded_text(meta):
    if 'encoded_parts' in meta:
        return ''.join((ROOT/p).read_text(encoding='ascii') for p in meta['encoded_parts'])
    return (ROOT/meta['encoded_path']).read_text(encoding='ascii')
def main():
    p=argparse.ArgumentParser();p.add_argument('--output-root',type=Path,default=Path('/tmp/pass3388_3399_materialized'));a=p.parse_args()
    for target,meta in MANIFEST.items():
        encoded=encoded_text(meta);raw=zlib.decompress(base64.b64decode(encoded))
        assert hashlib.sha256(raw).hexdigest()==meta['sha256'];dst=a.output_root/target;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw)
        print(f'{target} {len(raw)} {meta["sha256"]}')
if __name__=='__main__':main()
