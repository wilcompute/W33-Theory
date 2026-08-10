#!/usr/bin/env python3
"""Canonical wrapper for protected Pass 4618."""
from __future__ import annotations
import json
from pathlib import Path
import w33_pass4594_outer_canonical_u6_factor as impl
ROOT=Path(__file__).resolve().parents[1];impl.OUT=ROOT/'data/PART_W33_PASS4618_OUTER_CANONICAL_U6_FACTOR.json'
def main():
    rc=impl.main();d=json.loads(impl.OUT.read_text());d['pass']=4618;impl.OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');return rc
if __name__=='__main__':raise SystemExit(main())
