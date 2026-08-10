#!/usr/bin/env python3
"""Canonical collision-free wrapper for protected Pass 4611."""
from __future__ import annotations
import json
from pathlib import Path
import w33_pass4596_qminus_hermitian_binary_rank_reformulation as impl
ROOT=Path(__file__).resolve().parents[1];impl.OUT=ROOT/'data/PART_W33_PASS4611_QMINUS_HERMITIAN_BINARY_RANK_REFORMULATION.json'
def main():
    rc=impl.main();d=json.loads(impl.OUT.read_text());d['pass']=4611;impl.OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');return rc
if __name__=='__main__':raise SystemExit(main())
