#!/usr/bin/env python3
"""Decode the 720 exact-cover nonlinear signatures to JSON."""
from __future__ import annotations
import argparse, base64, gzip, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'data'/'w33_pass1825_signatures720.json.gz.b64'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);args=ap.parse_args()
 payload=json.loads(gzip.decompress(base64.b64decode(SOURCE.read_text())).decode())
 text=json.dumps(payload,indent=2,sort_keys=True)+'\n'
 if args.output:args.output.write_text(text)
 else:print(text,end='')
if __name__=='__main__':main()
