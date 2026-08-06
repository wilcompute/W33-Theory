#!/usr/bin/env python3
"""Idempotently register Passes 3997-4004 without touching protected docs/index.html."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'data/w33_current_frontier_manifest_v1.json'
REQ='analysis/BT3997_BT4004_photon_layout_fourier_stabilizers_insert'
SEC={'kind':'id','token':'bt3997-4004-photon-layout-fourier-stabilizers','source':'analysis/BT3997_BT4004_photon_layout_fourier_stabilizers_index_insert.html'}
PAGE={'token':'passes-3997-4004-photon-layout-delay-geometry-stabilizers','source':'docs/photon-layout-delay-geometry-stabilizers.html'}
def main():
 d=json.loads(P.read_text());r=d.setdefault('required_ordered_inputs',[])
 if REQ not in r:r.append(REQ)
 s=d.setdefault('public_sections',[])
 if not any(x.get('token')==SEC['token'] for x in s):s.append(SEC)
 p=d.setdefault('standalone_public_pages',[])
 if not any(x.get('token')==PAGE['token'] for x in p):p.append(PAGE)
 P.write_text(json.dumps(d,separators=(',',':'))+'\n')
 print('PASS_3997_4004_FRONTIER',r.count(REQ),sum(x.get('token')==SEC['token'] for x in s),sum(x.get('token')==PAGE['token'] for x in p))
if __name__=='__main__':main()
