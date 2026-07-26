#!/usr/bin/env python3
"""Offline unblinding entrypoint for Pass 1090 controller transcripts.
Requires a separately supplied escrow key file; never run inside acquisition control."""
from __future__ import annotations
import argparse,hashlib,json,hmac
from pathlib import Path

def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--manifest',required=True);p.add_argument('--transcript-summary',required=True);p.add_argument('--key-file',required=True);p.add_argument('--label',required=True);a=p.parse_args()
    manifest=json.loads(Path(a.manifest).read_text());summary=json.loads(Path(a.transcript_summary).read_text());key=Path(a.key_file).read_bytes()
    if sha(key)!=manifest['escrow_key_commitment_sha256']:raise SystemExit('FAIL CLOSED: escrow key commitment mismatch')
    expected=hmac.new(key,canon({'chain_root':summary['chain_root'],'event_count':summary['event_count'],'manifest_sha256':manifest['manifest_sha256']}),hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected,summary['signature_hmac_sha256']):raise SystemExit('FAIL CLOSED: transcript signature mismatch')
    print(json.dumps({'verified':True,'label':a.label,'chain_root':summary['chain_root'],'manifest_sha256':manifest['manifest_sha256']},indent=2))
if __name__=='__main__':main()
