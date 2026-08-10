#!/usr/bin/env python3
"""Canonical wrapper for protected Passes 4616-4617 after namespace collisions."""
from __future__ import annotations
import json
from pathlib import Path
import w33_pass4592_4593_e6_sentinel_transport_closure as impl
ROOT=Path(__file__).resolve().parents[1]
impl.OUT92=ROOT/'data/PART_W33_PASS4616_EXPLICIT_45_E6_INTERTWINER.json'
impl.OUT93=ROOT/'data/PART_W33_PASS4617_SENTINEL_MINIMUM_SHELL_TRANSPORT.json'
def canon(path,newpass):
    d=json.loads(path.read_text());s=json.dumps(d,indent=2,sort_keys=True)
    s=s.replace('Pass4592','Pass4616').replace('Pass4593','Pass4617').replace('4592','4616').replace('4593','4617')
    d=json.loads(s);d['pass']=newpass;path.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
def main():
    rc=impl.main();canon(impl.OUT92,4616);canon(impl.OUT93,4617);return rc
if __name__=='__main__':raise SystemExit(main())
