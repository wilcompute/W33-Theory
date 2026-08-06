#!/usr/bin/env python3
"""Idempotently register Passes 4019-4024 without directly editing protected docs/index.html."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];M=ROOT/'data/w33_current_frontier_manifest_v1.json'
REQ='analysis/BT4019_BT4024_photonic_flat_band_h1_insert'
SEC={'kind':'id','token':'bt4019-4024-photonic-flat-band-h1','source':'analysis/BT4019_BT4024_photonic_flat_band_h1_index_insert.html'}
PAGE={'token':'passes-4019-4024-photonic-flat-band-h1','source':'docs/photon-flat-band-h1.html'}
def main():
 d=json.loads(M.read_text(encoding='utf-8'));r=d.setdefault('required_ordered_inputs',[])
 if REQ not in r:r.append(REQ)
 s=d.setdefault('public_sections',[])
 if not any(x.get('token')==SEC['token'] for x in s):s.append(SEC)
 p=d.setdefault('standalone_public_pages',[])
 if not any(x.get('token')==PAGE['token'] for x in p):p.append(PAGE)
 M.write_text(json.dumps(d,separators=(',',':'))+'\n',encoding='utf-8')
 print('PASS_4019_4024_FRONTIER',r.count(REQ),sum(x.get('token')==SEC['token'] for x in s),sum(x.get('token')==PAGE['token'] for x in p))
if __name__=='__main__':main()
