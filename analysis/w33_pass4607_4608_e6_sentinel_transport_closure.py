#!/usr/bin/env python3
"""Canonical collision-free wrapper for protected Passes 4607-4608."""
from __future__ import annotations
import json
from pathlib import Path
import w33_pass4592_4593_e6_sentinel_transport_closure as impl
ROOT=Path(__file__).resolve().parents[1]
impl.OUT92=ROOT/'data/PART_W33_PASS4607_EXPLICIT_45_E6_INTERTWINER.json'
impl.OUT93=ROOT/'data/PART_W33_PASS4608_SENTINEL_MINIMUM_SHELL_TRANSPORT.json'
def canon(path,newpass):
    d=json.loads(path.read_text());s=json.dumps(d,indent=2,sort_keys=True)
    s=s.replace('4592','4607').replace('4593','4608');d=json.loads(s);d['pass']=newpass
    path.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
def main():
    rc=impl.main();canon(impl.OUT92,4607);canon(impl.OUT93,4608);return rc
if __name__=='__main__':raise SystemExit(main())
