#!/usr/bin/env python3
"""Idempotently register Passes 4013-4018 without touching protected docs/index.html."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/'data/w33_current_frontier_manifest_v1.json'
REQ='analysis/BT4013_BT4018_incidence_link_h1_memory_insert'
SECTION={'kind':'id','token':'bt4013-4018-incidence-link-h1-memory','source':'analysis/BT4013_BT4018_incidence_link_h1_memory_index_insert.html'}
PAGE={'token':'passes-4013-4018-incidence-link-h1-memory','source':'docs/photon-incidence-link-h1-memory.html'}
def main():
 data=json.loads(MANIFEST.read_text(encoding='utf-8'));required=data.setdefault('required_ordered_inputs',[])
 if REQ not in required:required.append(REQ)
 sections=data.setdefault('public_sections',[])
 if not any(x.get('token')==SECTION['token'] for x in sections):sections.append(SECTION)
 pages=data.setdefault('standalone_public_pages',[])
 if not any(x.get('token')==PAGE['token'] for x in pages):pages.append(PAGE)
 MANIFEST.write_text(json.dumps(data,separators=(',',':'))+'\n',encoding='utf-8')
 print('PASS_4013_4018_FRONTIER',required.count(REQ),sum(x.get('token')==SECTION['token'] for x in sections),sum(x.get('token')==PAGE['token'] for x in pages))
if __name__=='__main__':main()
