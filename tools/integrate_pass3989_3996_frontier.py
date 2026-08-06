#!/usr/bin/env python3
"""Idempotently register Passes 3989-3996 in the protected public frontier manifest."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'data/w33_current_frontier_manifest_v1.json'
REQUIRED='analysis/BT3989_BT3996_physical_photon_causal_memory_insert'
SUPERSEDED='analysis/BT3989_BT3996_physical_incidence_photon_breakthrough_insert'
PUBLIC={'kind':'id','token':'bt3989-3996-physical-incidence-photon','source':'analysis/BT3989_BT3996_physical_incidence_photon_breakthrough_index_insert.html'}
PAGE={'token':'passes-3989-3996-physical-incidence-photon-processor','source':'docs/physical-incidence-photon-processor.html'}

def main():
    data=json.loads(PATH.read_text())
    required=data.setdefault('required_ordered_inputs',[])
    required[:]=[x for x in required if x!=SUPERSEDED]
    if REQUIRED not in required: required.append(REQUIRED)
    sections=data.setdefault('public_sections',[])
    if not any(x.get('token')==PUBLIC['token'] for x in sections): sections.append(PUBLIC)
    pages=data.setdefault('standalone_public_pages',[])
    if not any(x.get('token')==PAGE['token'] for x in pages): pages.append(PAGE)
    PATH.write_text(json.dumps(data,separators=(',',':'))+'\n')
    print('PASS_3989_3996_FRONTIER_RECONCILE',required.count(REQUIRED),required.count(SUPERSEDED),sum(x.get('token')==PUBLIC['token'] for x in sections),sum(x.get('token')==PAGE['token'] for x in pages))
if __name__=='__main__': main()
