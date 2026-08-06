#!/usr/bin/env python3
"""Inspect the published Passes 3821-3828 exact verifier API."""
from __future__ import annotations
import importlib.util, inspect, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'analysis/w33_pass3821_3828_maxcode_mesh_scheme_ovoid.py'
spec=importlib.util.spec_from_file_location('p3821',path)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
ns=mod._embedded_globals()
out={}
for k,v in sorted(ns.items()):
    if k.startswith('__'): continue
    item={'type':type(v).__name__}
    if callable(v):
        try:item['signature']=str(inspect.signature(v))
        except Exception:item['signature']='?'
    out[k]=item
print(json.dumps(out,indent=2,sort_keys=True))
