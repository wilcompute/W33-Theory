#!/usr/bin/env python3
"""Idempotently register Passes 4005-4012 in the protected frontier JSON."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'data/w33_current_frontier_manifest_v1.json'
REQUIRED='analysis/BT4005_BT4012_exact_photon_revival_memory_insert'
PUBLIC={'kind':'id','token':'bt4005-4012-exact-photon-revival','source':'analysis/BT4005_BT4012_exact_photon_revival_memory_index_insert.html'}
PAGE={'token':'passes-4005-4012-exact-photon-revival-memory','source':'docs/exact-photon-revival-memory.html'}
def main():
 data=json.loads(PATH.read_text())
 required=data.setdefault('required_ordered_inputs',[])
 if REQUIRED not in required:required.append(REQUIRED)
 sections=data.setdefault('public_sections',[])
 if not any(x.get('token')==PUBLIC['token'] for x in sections):sections.append(PUBLIC)
 pages=data.setdefault('standalone_public_pages',[])
 if not any(x.get('token')==PAGE['token'] for x in pages):pages.append(PAGE)
 PATH.write_text(json.dumps(data,separators=(',',':'))+'\n')
 print('PASS_4005_4012_FRONTIER_RECONCILE',required.count(REQUIRED),sum(x.get('token')==PUBLIC['token'] for x in sections),sum(x.get('token')==PAGE['token'] for x in pages))
if __name__=='__main__':main()
