#!/usr/bin/env python3
"""Idempotently register both Passes 3989-3996 public theorem surfaces."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'data/w33_current_frontier_manifest_v1.json'
REQUIRED='analysis/BT3989_BT3996_physical_photon_causal_memory_insert'
SUPERSEDED={
  'analysis/BT3989_BT3996_physical_incidence_photon_breakthrough_insert',
  'analysis/BT3989_BT3996_combined_photon_breakthrough_insert',
}
PUBLIC_ITEMS=[
  {'kind':'id','token':'bt3989-3996-physical-incidence-photon','source':'analysis/BT3989_BT3996_physical_incidence_photon_breakthrough_index_insert.html'},
  {'kind':'id','token':'bt3989-3996-photon-causal-memory','source':'analysis/BT3989_BT3996_physical_photon_causal_memory_index_insert.html'},
]
PAGE_ITEMS=[
  {'token':'passes-3989-3996-physical-incidence-photon-processor','source':'docs/physical-incidence-photon-processor.html'},
  {'token':'passes-3989-3996-photon-causal-memory','source':'docs/photon-causal-memory-3989-3996.html'},
]

def append_by_token(items, value):
    matches=[item for item in items if item.get('token')==value['token']]
    if matches and matches != [value]:
        raise ValueError(f"conflicting token {value['token']}: {matches}")
    if not matches:
        items.append(value)

def main():
    data=json.loads(PATH.read_text())
    required=data.setdefault('required_ordered_inputs',[])
    required[:]=[x for x in required if x not in SUPERSEDED]
    if REQUIRED not in required:
        required.append(REQUIRED)
    sections=data.setdefault('public_sections',[])
    for item in PUBLIC_ITEMS:
        append_by_token(sections,item)
    pages=data.setdefault('standalone_public_pages',[])
    for item in PAGE_ITEMS:
        append_by_token(pages,item)
    PATH.write_text(json.dumps(data,separators=(',',':'))+'\n')
    stale=sum(required.count(x) for x in SUPERSEDED)
    print('PASS_3989_3996_FRONTIER_RECONCILE',required.count(REQUIRED),stale,
          [sum(x.get('token')==item['token'] for x in sections) for item in PUBLIC_ITEMS],
          [sum(x.get('token')==item['token'] for x in pages) for item in PAGE_ITEMS])
if __name__=='__main__': main()
