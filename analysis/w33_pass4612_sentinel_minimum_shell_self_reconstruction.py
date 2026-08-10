#!/usr/bin/env python3
"""Canonical collision-free wrapper for protected Pass 4612."""
from __future__ import annotations
import json
from pathlib import Path
import w33_pass4597_sentinel_minimum_shell_self_reconstruction as impl
ROOT=Path(__file__).resolve().parents[1];impl.OUT=ROOT/'data/PART_W33_PASS4612_SENTINEL_MINIMUM_SHELL_SELF_RECONSTRUCTION.json'
def main():
    rc=impl.main();d=json.loads(impl.OUT.read_text());d['pass']=4612;impl.OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');return rc
if __name__=='__main__':raise SystemExit(main())
